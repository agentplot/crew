"""A bolt lands on the user's send, carried to the runner as a land, and its outcome is read from the runner's report
(crew-lands-each-bolt-through-flumes-base-place, Decisions 6 and 7; plan.21): plan.landing_entry, what crew records of
a landing once the runner's report decides it; plan.landing_read, the first read that records it and acts on it, a
landing closing the bolt at Flume's commit, a failed check holding its row, a conflict launching the take-main fix
once, a stop keeping the row's box; crew bolt land of a started bolt (plan.bolt_land); the run record's states of a
landing (plan.stops, refusals, landing_phase); and the bolt's landing card, its reading and preview, raised once the
bolt reads proven (record 0031 §1)."""
import argparse
import base64
import contextlib
import datetime
import io
import json
import pathlib
import re

import pytest

from facts import START, at

import plan

OLD, NEW, TIP = "a" * 40, "b" * 40, "c" * 40
WHOLE = dict(repo="o/switchboard-kit", base="abc1234" + "0" * 33, main="/kit/main", host="box")  # where a bolt's diff is read whole


def submitted(bolt, head=TIP, **f):
    return dict({"Act": "bolt.submit", "On": [f"bolt/{bolt}"], **({"Head": head} if head else {})}, **f)


class TestTheStops:
    """Decision 2: a stop is a bolt.submit marked Outcome stopped with its Head and Why and no Refused, read from each
    bolt's last one (plan.stops), and holds nothing of a refusal (plan.refusals); at another head it says nothing
    (plan.stopped_at)."""
    STOP = submitted("b", Why="sluice itself failed (its lock could not be taken)", Outcome="stopped")

    def test_each_bolts_last_stop_is_read(self):
        entries = [submitted("b", Why="tests:logic could not run: no engine", Outcome="stopped"), self.STOP,
                   submitted("c", head="d" * 40, Why="sluice's record has #9 withdrawn", Outcome="stopped")]
        assert plan.stops(entries) == {"b": (TIP, "sluice itself failed (its lock could not be taken)"),
                                       "c": ("d" * 40, "sluice's record has #9 withdrawn")}
        assert plan.refusals(entries) == {}

    def test_a_later_landing_or_refusal_supersedes_it(self):
        landed = submitted("b", Why="bolt(b): landed on main at bbbbbbb")
        refused = submitted("b", Refused="sluice: bolt/b conflicts with main")
        assert plan.stops([self.STOP, landed]) == {} and plan.stops([self.STOP, refused]) == {}
        assert plan.refusals([self.STOP, refused]) == {"b": (TIP, "sluice: bolt/b conflicts with main")}
        stopped = dict(self.STOP, Submission="9")  # a submission of its own, which sluice stopped
        assert plan.stops([refused, stopped]) == {"b": (TIP, self.STOP["Why"])} and plan.refusals([refused, stopped]) == {}

    def test_a_stop_that_submitted_nothing_leaves_a_sent_back_landing_the_bolts_fix(self):
        """bolt-teams "No land is posted again until a fix moves the head sent back": a stop an older crew recorded at the head
        sent back, of a submit that submitted nothing (the Willdan box's 22:28Z stop of 2026-11-06), leaves the refusal
        standing and says no stop; a refusal naming no head leaves it too; a stop at another head, or anything queued,
        lifts it. The landing's state reads rejected through it (landing_phase)."""
        refused = submitted("b", Refused="#1474 failed: tests:logic on 1234567", Submission="1474")
        crews = submitted("b", head=None, Refused="bolt/b was not submitted: sluice sent its landing back")
        assert plan.refusals([refused, self.STOP]) == {"b": (TIP, "#1474 failed: tests:logic on 1234567")} and plan.stops([refused, self.STOP]) == {}
        assert plan.sent_back([refused, crews, self.STOP]) == {"b": {"head": TIP, "words": "#1474 failed: tests:logic on 1234567", "n": "1474"}}
        assert plan.landing_phase([refused, crews, self.STOP], "b") == dict(state="rejected", n="1474", head=TIP,
                                                                             words="#1474 failed: tests:logic on 1234567")
        assert plan.refusals([refused, dict(self.STOP, Head="e" * 40)]) == {}
        assert plan.refusals([refused, submitted("b", Why="bolt(b): queued on main as #1480", Outcome="queued", Submission="1480")]) == {}
        assert plan.refusals([refused, submitted("b", Why="crew can't tell whether bolt/b will land: sluice holds it as pull request #268")]) == {}

    def test_a_stop_with_no_head_gives_none(self):
        assert plan.stops([submitted("b", head=None, Why="bolt/b was not submitted on box: wt-submit is missing", Outcome="stopped")]) == {}

    def test_a_stop_says_its_words_only_at_its_head(self):
        got = plan.stops([self.STOP])
        assert plan.stopped_at(got, "b", TIP[:7]) == self.STOP["Why"]
        assert plan.stopped_at(got, "b", "e" * 40) is None and plan.stopped_at(got, "c", TIP) is None


class APlan:
    """A plan holding the named bolts, each held by swb-1 and of kit k."""
    def __init__(self, *bolts):
        self.bolts_ = set(bolts)

    def bolt(self, name):
        return {"Bolt": name, "Repo": "k"} if name in self.bolts_ else None


class TestARefusedClose:
    """Decision 4: a refused close is recorded only when no bolt.land refused since the bolt's landing carries the same
    words (plan.close_refused_new)."""
    LANDED = submitted("b", Outcome="landed", Submission="412")
    WORDS = "chore tidy-b has not landed on main: it is ready"

    def refused(self, words, bolt="b"):
        return {"Act": "bolt.land", "On": [f"bolt/{bolt}"], "Refused": words}

    def test_the_first_refusal_since_the_landing_is_new(self):
        assert plan.close_refused_new([self.LANDED], "b", self.WORDS)
        assert plan.close_refused_new([self.refused(self.WORDS), self.LANDED], "b", self.WORDS)  # one before the landing

    def test_the_same_words_again_are_not(self):
        assert not plan.close_refused_new([self.LANDED, self.refused(self.WORDS)], "b", self.WORDS)
        assert not plan.close_refused_new([self.LANDED, self.refused(self.WORDS), self.refused("x", bolt="z")], "b", self.WORDS)

    def test_other_words_are(self):
        assert plan.close_refused_new([self.LANDED, self.refused(self.WORDS)], "b", "wldn/main could not be read")
        assert plan.close_refused_new([self.LANDED, self.refused("other"), self.refused("x"), ], "b", "other")


class TestTheCardsClose:
    """crew bolt land closes the bolt's landing card on its team's host (plan.16, record 0032 §3): with where GitHub's
    main holds the landing and that every host's folder follows by the timer, under whichever landing key the conductor
    holds one."""

    def test_the_card_closes_naming_githubs_main_sluices_submission_and_the_timer(self):
        assert plan.landed_words("c" * 40, "46") == (
            "landed on GitHub's main at ccccccc (#46); every host's folder follows by swancloud's timer within minutes")

    def test_the_close_names_the_commit_landed_and_says_nothing_of_a_preview(self):
        """rail-cards "A landed row" (record 0043): a card about a landed revision carries its commit, and no preview."""
        landed = plan.landed_words("1a2b3c4" + "0" * 33, "46")
        assert "1a2b3c4" in landed and "preview" not in landed.lower() and "bring it up" not in landed

    def test_a_head_sluice_did_not_make_is_named_without_a_number(self):
        for n in ("", None, "46 47", "x"):
            assert plan.landed_words("c" * 40, n) == (
                "landed on GitHub's main at ccccccc; every host's folder follows by swancloud's timer within minutes")

    def test_the_conductors_open_cards_under_the_bolts_landing_keys_old_and_new(self):
        post = lambda key, card, by="swb-1-conductor": {"Act": "card.post", "Key": key, "Card": card, "By": by}
        entries = [post("land/b/abc1234", "req_1"), post("land/b", "req_2"), post("land/b/abc9999", "req_3"),
                   {"Act": "card.close", "Card": "req_3", "Key": "land/b/abc9999", "By": "swb-1-conductor"},
                   post("land/b", "req_4", by="swb-2-conductor"), post("land/bb", "req_5"), post("proposal/1", "req_6")]
        assert plan.landing_card_keys(entries, "b", "swb-1-conductor") == ["land/b", "land/b/abc1234"]
        assert plan.landing_card_keys(entries, "c", "swb-1-conductor") == []


class TestTheLandingsPoint:
    """crew raises a bolt's landing card once the bolt reads proven (rail-cards, record 0031 §1, record 0025): every
    unit and chore merged, its head the landing of its work as the runner reports it, no fix in flight on it, and every
    unit's latest change in a batch; then which act follows each event."""
    GREEN = ("green", "its head abc1234 is b's landing, as the runner reports it")
    NONE = ("none", "its head abc1234 is no landing of its work that the runner reports")
    WORK = [("a", "unit", "merged"), ("b", "unit", "merged"), ("c", "chore", "merged")]

    def unready(self, work=WORK, verified=GREEN, fixes=()):
        return plan.landing_unready(work, verified, list(fixes))

    def test_a_green_bolt_whose_every_unit_and_chore_merged_reads_proven(self):
        assert self.unready() is None
        assert self.unready(self.WORK + [("d", "unit", "landed")]) is None

    @pytest.mark.parametrize("work, verified, fixes, why", [
        ([("a", "unit", "verify")] + WORK[1:], GREEN, (), "unit a has not merged: it is verify"),
        ([], GREEN, (), "it holds no units or chores"),
        ([("a", "unit", "landed")], GREEN, (), "every unit and chore of it has landed"),
        (WORK, NONE, (), "its verification is not green: its head abc1234 is no landing of its work that the runner reports"),
        (WORK, GREEN, ("fix/y/zone-gap",), "fix/y/zone-gap is in flight on it")])
    def test_until_then_no_card_is_raised(self, work, verified, fixes, why):
        assert self.unready(work, verified, fixes) == why

    def test_a_fix_in_flight_holds_it(self):
        """The landing's point waits for no fix of the bolt in flight (runner.fixes_in_flight, its cases test_fix's)."""
        assert self.unready(fixes=["fix/y/gap"]) == "fix/y/gap is in flight on it"
        assert self.unready(fixes=[]) is None

    def test_its_facts_wait_for_every_units_latest_change_to_have_been_in_a_batch(self):
        pr = plan.pull_of("swb-1-unit-2 (pull/23)", "WilldanGroup/switchboard-kit")
        facts = plan.landing_facts("y", "switchboard-kit", self.WORK, "abc1234", "2026-10-17T10:00:00Z", set(), {}, {"a": 4, "b": 5}, 2, pr)
        assert facts == dict(bolt="y", kit="switchboard-kit", units=["a", "b"], chores=["c"], batches={"a": 4, "b": 5}, head="abc1234",
                             at="2026-10-17T10:00:00Z", moved=2, pr={"number": 23, "url": "https://github.com/WilldanGroup/switchboard-kit/pull/23"})
        assert plan.landing_facts("y", "switchboard-kit", self.WORK, "abc1234", None, {"b"}, {}, {"a": 4}, 0, None) is None

    def test_its_facts_wait_for_the_users_answer_on_each_batch_card_that_holds_a_units_latest_change(self):
        """briefs.12: the user, 2026-10-19, on card req_5ff4d31d: "Wait for my answer on the batch card", after crew's
        small-leftovers-of-crew landed (#71) while batch 7's card, which held its unit, was unanswered."""
        assert plan.landing_facts("y", "switchboard-kit", self.WORK, "abc1234", None, set(), {"b": 7}, {"a": 6, "b": 7}, 0, None) is None
        assert plan.landing_facts("y", "switchboard-kit", self.WORK, "abc1234", None, set(), {"q": 7}, {"a": 6, "b": 7}, 0, None)["units"] == ["a", "b"]

    def test_a_chore_is_in_no_batch_and_holds_no_landing(self):
        facts = plan.landing_facts("y", "switchboard-kit", [("c", "chore", "merged")], "abc1234", None, set(), {}, {}, 0, None)
        assert (facts["units"], facts["chores"], facts["batches"]) == ([], ["c"], {})

    def test_sluices_pull_request_is_the_one_its_submission_at_the_head_went_through(self):
        assert plan.pull_of("swb-1-unit-2 (unit/a)", "o/k") is None and plan.pull_of("", "o/k") is None

    def test_a_landing_reading_is_its_cover_each_units_change_in_the_plans_order_then_the_diff(self):
        """card-sessions "A landing's session opens its page, its units' changes and its diff, each file whole": two units and a chore,
        each unit's Markdown named for it in a change's reading order, the diff numbered after the last unit."""
        a = [("tasks.md", "a's tasks"), ("specs/x/spec.md", "a's spec"), ("proposal.md", "a's proposal"), ("design.md", "a's design")]
        b = [("proposal.md", "b's proposal")]
        files = plan.landing_reading("y", "switchboard-kit", "def5678" + "0" * 33, ["a", "b"], ["c"], [("a", a), ("b", b)],
                                     "diff --git a/x b/x\n", WHOLE)
        assert [n for n, _ in files] == ["00-y.md", "01-a-proposal.md", "01-a-design.md", "01-a-specs-x-spec.md", "01-a-tasks.md",
                                         "02-b-proposal.md", "03-y-diff.txt"]
        assert files[1][1] == "a's proposal" and files[-1][1] == "diff --git a/x b/x\n"

    def test_a_bolt_of_chores_alone_reads_as_its_cover_and_its_diff(self):
        files = plan.landing_reading("y", "k", "def5678", [], ["c", "d"], [], "diff --git a/x b/x\n", WHOLE)
        assert [n for n, _ in files] == ["00-y.md", "01-y-diff.txt"]
        assert plan.landing_reading("y", "k", "def5678", [], ["c"], [], "", WHOLE)[-1][1] == (
            "The bolt changes nothing against main outside its change folders.\n")

    def test_the_cover_names_every_unit_and_chore_and_says_the_reading_lands_nothing(self):
        cover = plan.landing_reading("y", "switchboard-kit", "def5678" + "0" * 33, ["a", "b"], ["c"],
                                     [("a", [("proposal.md", "")]), ("b", [("proposal.md", "")])], "", WHOLE)[0][1]
        assert cover.startswith("# Bolt y, landing on switchboard-kit's main\n\nWhat lands, at its head def5678:\n\n- a\n- b\n- c (chore)\n")
        assert "This reading lands nothing: approving the landing card is the word to land" in cover
        assert "reaches main-level ops as notes on the landing card, and a note naming a defect holds the landing for a fix" in cover

    def test_a_landings_reading_is_written_into_its_heads_folder_from_the_kit_at_the_head(self, monkeypatch, tmp_path):
        """card-sessions "A bolt of two units and a chore": each unit's change read at the head, and the diff from where
        the bolt last met main to its head, less the change folders."""
        held = {"a": [("proposal.md", "a's proposal")], "b": [("tasks.md", "b's tasks"), ("proposal.md", "b's proposal")]}
        asked = []
        monkeypatch.setattr(plan, "change_held", lambda main, ref, u: asked.append((main, ref, u)) or held.get(u))
        monkeypatch.setattr(plan, "kit_git", lambda fleet, t, where, *args: asked.append((where, *args)) or (0, "diff --git a/x b/x"))
        fleet = {"drives": {}, "hosts": {}}
        f = dict(bolt="y", kit="switchboard-kit", units=["a", "b"], chores=["c"], head="def5678" + "0" * 33, base="abc1234",
                 host="box", main="/kit/main")
        folder = tmp_path / "def5678"
        folder.mkdir()
        (folder / "01-old-proposal.md").write_text("an older head's")
        paths = plan.landing_write(fleet, f, folder)
        assert [pathlib.Path(p).name for p in paths] == ["00-y.md", "01-a-proposal.md", "02-b-proposal.md", "02-b-tasks.md", "03-y-diff.txt"]
        assert sorted(p.name for p in folder.iterdir()) == sorted(pathlib.Path(p).name for p in paths)
        assert (folder / "03-y-diff.txt").read_text() == "diff --git a/x b/x\n"
        assert asked[:2] == [("/kit/main", f["head"], "a"), ("/kit/main", f["head"], "b")]
        assert asked[2] == ("/kit/main", "diff", "--no-color", "--no-ext-diff", "abc1234", f["head"], "--", ".", ":(exclude)openspec/changes")

    def test_a_unit_whose_change_the_head_does_not_hold_refuses_and_nothing_is_written(self, monkeypatch, tmp_path):
        monkeypatch.setattr(plan, "change_held", lambda main, ref, u: None)
        monkeypatch.setattr(plan, "kit_git", lambda *a: pytest.fail("the diff was read after a change crew could not read"))
        fleet = {"drives": {}, "hosts": {}}
        f = dict(bolt="y", kit="k", units=["a"], chores=[], head="def5678" + "0" * 33, base="abc1234", host="box", main="/kit/main")
        with pytest.raises(plan.Refusal, match="unit a's change is not on bolt y at def5678, open or archived, in /kit/main on box"):
            plan.landing_write(fleet, f, tmp_path / "def5678")
        assert not (tmp_path / "def5678").exists()

    @staticmethod
    def section(path, size):
        """git's diff of one new file, path, about size bytes long."""
        head = f"diff --git a/{path} b/{path}\nnew file mode 100644\n--- /dev/null\n+++ b/{path}\n@@ -0,0 +1 @@\n"
        return head + ("+" + "x" * 98 + "\n") * ((size - len(head)) // 100)

    def test_a_diff_past_plannotators_limit_is_read_in_parts_each_of_whole_files_in_gits_order(self):
        """card-sessions "A diff past plannotator's limit for one file" (wldn's switchboard-kit bolt
        a-deploy-row-follows-its-stack-to-the-end, whose reading plannotator refused on 2026-11-06: "File too large to
        annotate (max 2MB)"): five files' changes of 0.9 MB each, 4.5 MB in all, come in three parts, none over the
        most plannotator opens, each holding whole files' changes, and nothing is left out."""
        mb = 1024 * 1024
        diff = "".join(self.section(f"src/f{i}.ts", int(0.9 * mb)) for i in range(5))
        files = plan.landing_reading("y", "switchboard-kit", "def5678" + "0" * 33, [], ["c"], [], diff, WHOLE)
        assert [n for n, _ in files] == ["00-y.md", "01-y-diff-1-of-3.txt", "01-y-diff-2-of-3.txt", "01-y-diff-3-of-3.txt"]
        parts = [text for _, text in files[1:]]
        assert all(len(text.encode()) <= plan.PLANNOTATOR_MOST for text in parts)
        assert "".join(parts) == diff
        assert [len(re.findall(r"(?m)^diff --git ", text)) for text in parts] == [2, 2, 1]
        assert "That diff comes in 3 files, each holding whole files' changes in git's order, since plannotator opens no file over 2 MB." in files[0][1]
        assert "Left out" not in files[0][1]

    def test_a_file_whose_own_change_passes_the_limit_is_named_in_its_place_and_on_the_page_with_where_to_read_it(self):
        """card-sessions "One file's change past plannotator's limit", as sluice core.43 names a request's commits past
        the forge's limit: the file's change is cut nowhere, a line stands in its place, and the page names it, its
        size, how many and where to read it whole; every other file's change is in the reading whole."""
        mb = 1024 * 1024
        small, big = self.section("README.md", 4000), self.section("vendor/bundle.js", int(2.5 * mb))
        files = plan.landing_reading("y", "switchboard-kit", "def5678" + "0" * 33, [], ["c"], [], small + big + small, WHOLE)
        assert [n for n, _ in files] == ["00-y.md", "01-y-diff.txt"]
        said = files[1][1]
        assert said.startswith(small) and said.endswith(small)
        assert said[len(small):-len(small)] == ("vendor/bundle.js: its change, 2.5 MB, passes the 2 MB plannotator opens in one "
                                                "file, so it is not in this reading; its first page says where to read it whole.\n")
        cover = files[0][1]
        assert "That diff comes in" not in cover
        assert ("Left out of this reading, 1 file whose change alone passes the 2 MB plannotator opens in one file, each "
                "named in its place in the diff:\n\n- `vendor/bundle.js`, 2.5 MB\n") in cover
        assert (f"Read it whole in GitHub's compare view of the bolt against main, "
                f"https://github.com/o/switchboard-kit/compare/{WHOLE['base']}...def5678{'0' * 33}, or on box with "
                f"`git -C /kit/main diff {WHOLE['base']} def5678{'0' * 33} -- <path>`.") in cover

    def test_a_diff_of_exactly_the_limit_is_one_file_and_one_byte_more_two(self):
        """plannotator 0.28.48 opens a file of exactly its most and refuses one a byte longer."""
        one = self.section("a.txt", 1024 * 1024)
        head = "diff --git a/b.txt b/b.txt\n+"
        fits = head + "x" * (plan.PLANNOTATOR_MOST - len(one) - len(head) - 1) + "\n"
        assert len((one + fits).encode()) == plan.PLANNOTATOR_MOST
        assert plan.diff_parts(one + fits) == ([one + fits], [])
        passes = head + "x" * (plan.PLANNOTATOR_MOST - len(one) - len(head)) + "\n"
        assert plan.diff_parts(one + passes) == ([one, passes], [])

    def test_a_file_is_named_by_its_path_or_by_both_sides_as_git_wrote_them(self):
        assert plan.diff_path("diff --git a/src/x y.ts b/src/x y.ts\nindex 1..2\n") == "src/x y.ts"
        assert plan.diff_path("diff --git a/old.ts b/new.ts\nrename from old.ts\n") == "a/old.ts b/new.ts"
        assert plan.diff_path('diff --git "a/caf\\303\\251" "b/caf\\303\\251"\n') == '"a/caf\\303\\251" "b/caf\\303\\251"'

    def test_a_size_is_said_in_plannotators_mb_rounded_up_so_one_past_its_most_never_reads_as_it(self):
        assert [plan.megabytes(n) for n in (plan.PLANNOTATOR_MOST, plan.PLANNOTATOR_MOST + 1, 2_621_440, 1)] == [
            "2 MB", "2.1 MB", "2.5 MB", "0.1 MB"]

    def test_a_landings_reading_past_the_limit_is_written_every_file_within_it(self, monkeypatch, tmp_path):
        """The case the box met: a bolt whose diff passes plannotator's limit is written as files plannotator opens,
        each within its most bytes on disk, so its reading opens."""
        mb = 1024 * 1024
        diff = self.section("src/a.ts", int(1.5 * mb)) + self.section("src/b.ts", int(1.5 * mb)) + self.section("gen/c.json", 3 * mb)
        monkeypatch.setattr(plan, "change_held", lambda main, ref, u: [("proposal.md", "a's proposal")])
        monkeypatch.setattr(plan, "kit_git", lambda fleet, t, where, *args: (0, diff.strip()))
        fleet = {"drives": {}, "hosts": {}}
        f = dict(bolt="y", kit="switchboard-kit", units=["a"], chores=[], head="def5678" + "0" * 33, base="abc1234",
                 host="box", main="/kit/main", repo="o/switchboard-kit")
        paths = [pathlib.Path(p) for p in plan.landing_write(fleet, f, tmp_path / "def5678")]
        assert [p.name for p in paths] == ["00-y.md", "01-a-proposal.md", "02-y-diff-1-of-2.txt", "02-y-diff-2-of-2.txt"]
        assert all(p.stat().st_size <= plan.PLANNOTATOR_MOST for p in paths)
        assert "- `gen/c.json`, 3 MB" in paths[0].read_text()
        assert paths[3].read_text().startswith("diff --git a/src/b.ts b/src/b.ts\n")
        assert "gen/c.json: its change, 3 MB, passes the 2 MB plannotator opens in one file" in paths[3].read_text()

    def test_a_proven_bolts_card_waits_on_its_batches_and_says_which(self):
        """briefs.12, as crew card session land/<bolt> says why the bolt has no card yet."""
        assert plan.batch_waits(["a", "b", "c"], {"a"}, {"b": 7, "c": 8}) == (
            "a has not been in a batch, which is due; the user has not answered batches 7 and 8")
        assert plan.batch_waits(["a", "b"], {"a", "b"}, {}) == "a or b have not been in a batch, which is due"
        assert plan.batch_waits(["a"], set(), {"a": 7}) == "the user has not answered batch 7"
        assert plan.batch_waits(["a"], set(), {"q": 7}) is None

    FRESH = dict(bolt="y", head="def5678", host="mac-studio")

    def test_a_first_refused_reading_is_tried_again_with_the_landing_read_afresh(self):
        """card-sessions "The first start fails and the second opens": the fresh facts are the card's from then."""
        assert plan.landing_retry("plannotator did not list land/y's session within 10 seconds", (self.FRESH, None), None) == (
            "again", self.FRESH)

    def test_a_bolt_that_no_longer_reads_proven_raises_nothing(self):
        """card-sessions "The bolt no longer reads proven at the second try"."""
        assert plan.landing_retry("plannotator ended before land/y's session was ready", (None, "fix/y/gap is in flight on it"),
                                  None) == ("none", None)

    def test_a_fresh_read_that_is_refused_leaves_the_first_reason_standing(self):
        """read.1: what the second read could not read is not guessed past."""
        why = "plannotator did not list land/y's session within 10 seconds"
        assert plan.landing_retry(why, None, "bolt y's kit could not be read: ssh: timed out") == ("stand", why)

    def test_which_act_follows_each_event(self):
        assert plan.landing_act("proven", head="abc1234" + "0" * 33) == ("change", "Its head is now abc1234")
        assert plan.landing_act("fix", words="The zone list misses one zone.") == ("close", None, "held for a fix: The zone list misses one zone.")
        assert plan.landing_act("landed", words="landed on GitHub's main at c0ffee1 (#3); every host's folder follows") == (
            "close", "landed on GitHub's main at c0ffee1 (#3); every host's folder follows", None)


class TestThePreview:
    """What a card's preview is asked by, and its change note, from facts alone (rail-cards, record 0043; Decisions 4
    and 6 of a-cards-preview-is-asked-of-the-runner)."""
    HEAD = "abc1234" + "0" * 33

    @pytest.mark.parametrize("p, note", [
        ({"head": HEAD, "host": "deneb", "state": "asked"}, "y: Its preview of abc1234 is asked of the runner on deneb"),
        ({"head": HEAD, "host": "deneb", "state": "held"}, "y: Its preview of abc1234 waits for room on deneb"),
        ({"head": HEAD, "state": "starting", "addresses": {}}, "y: Its preview of abc1234 is coming up"),
        ({"head": HEAD, "state": "up", "addresses": {}}, "y: Its preview of abc1234 is up"),
        ({"head": HEAD, "host": "deneb", "state": "failed"}, "y: Its preview of abc1234 did not come up"),
        ({"head": HEAD, "host": "deneb", "state": "refused", "words": "no"}, "y: Its preview of abc1234 could not be brought up"),
        ({"head": HEAD, "why": "deneb's runner can't be read"}, "y: Its preview of abc1234 could not be brought up"),
        ({"head": HEAD, "host": "deneb", "state": "unlisted"}, "y: Its preview of abc1234 is gone"),
        ({"branch": "bolt/y", "head": HEAD, "state": "ask", "released": HEAD}, "y: Its preview of abc1234 is put away"),
    ])
    def test_a_previews_note_says_what_the_card_now_says_of_it(self, p, note):
        """"Brought up" and Decision 4's notes: the note names the thing and what its preview now is."""
        assert plan.asked_note("y", p) == note

    def test_a_previews_change_is_a_change_of_the_card_in_its_words(self):
        assert plan.landing_act("preview", head=self.HEAD, words="Its preview of abc1234 is up") == ("change", "Its preview of abc1234 is up")

    def test_a_thing_the_card_does_not_carry_is_refused_naming_those_it_does(self):
        """"A thing the card does not carry"."""
        assert plan.preview_target("land/crew", "y", {"y": ("bolt/y", self.HEAD), "z": None}) == ("bolt/y", self.HEAD)
        with pytest.raises(plan.Refusal, match="land/crew carries no w to bring up: it carries y and z"):
            plan.preview_target("land/crew", "w", {"y": None, "z": None})
        with pytest.raises(plan.Refusal, match="batch/7 carries no a/demo to bring up: it carries nothing that must run"):
            plan.preview_target("batch/7", "a/demo", {})

    def test_the_cards_owner_brings_up_what_it_carries_and_a_person_may_too(self):
        """"Asked by anyone but the owner"."""
        kits = ("crew",)
        assert plan.preview_owner("land/crew", "swancloud", kits) == "swancloud-ops"
        assert plan.preview_owner("batch/7", "swancloud", kits) == "swancloud-planner"
        for key in ("land/y", "proposal/3", "deploy/prod"):
            with pytest.raises(plan.Refusal, match=f"{key} carries nothing crew brings up"):
                plan.preview_owner(key, "swancloud", kits)
        assert plan.preview_caller("swancloud-ops", "swancloud-ops", "land/crew") is None
        assert plan.preview_caller("chuck@mac-studio", "swancloud-ops", "land/crew") is None
        assert plan.preview_caller("crw-1-conductor", "swancloud-ops", "land/crew") == (
            "land/crew is swancloud-ops's card: swancloud-ops brings up what it carries, on the user's words on it")


def policy(text, origin="yes"):
    """What POLICY prints of a kit's main: GitHub's main holding text, or, with origin "no", its own main holding it."""
    b = base64.b64encode(text.encode()).decode() if text is not None else "-"
    if origin == "no":
        return f"ORIGIN=no\nGITHUB=-\nOWN={OLD}\nAT_GITHUB=-\nAT_OWN={b}\n"
    return f"ORIGIN=yes\nFETCHED=ok\nGITHUB={OLD}\nOWN={OLD}\nAT_GITHUB={b}\nAT_OWN=-\n"


def ran(code, out="", err=""):
    return type("R", (), {"returncode": code, "stdout": out, "stderr": err})()


class TestTheLandingsAsks:
    """A bolt's landing, as crew's read of the runner's report records it, asks the planner and the design agent that
    run as their kinds in the landing's commit, and one that did not land asks main-level ops with Flume's or the
    runner's words, keyed by the land's request (design Decisions 5 and 12; role-runs "A landing refused or stopped is
    an ask of ops" and "Main-level ops's run lands nothing"); a role that stands is asked nothing."""

    def fleet(self, **runs):
        import crew
        return {"drives": {"swancloud": {"label": "swancloud", "machine": "deneb", "blueprints": ["afterthought/blueprints"], "roles": {},
                                             "runs": dict(dict.fromkeys(crew.KIND_ROLES, "standing"), **runs)}}, "hosts": {}}

    @pytest.fixture
    def w(self, monkeypatch):
        from facts import FactsWrite
        monkeypatch.setattr(plan.crew, "this_host", lambda: "deneb")
        w = FactsWrite("", None)
        w.label = "swancloud"
        return w

    def test_a_landing_asks_the_planner_and_the_design_agent_each_naming_the_bolt(self, w):
        """role-runs, A landing: the landing's write holds an ask of the planner and one of the design agent."""
        import asks
        plan.landed_asks(w, self.fleet(planner="on-demand", design="on-demand"), "swancloud", "b", "bolt b landed on k's main at bbbbbbb")
        got, _ = asks.parse(w.files["asks.rec"])
        assert [(a["Role"], a["From"], a["What"], a["Names"], a["Key"], a["Words"]) for a in got] == [
            ("planner", "crew", "landed", "bolt/b", "landed/b", "bolt b landed on k's main at bbbbbbb"),
            ("design", "crew", "landed", "bolt/b", "landed/b", "bolt b landed on k's main at bbbbbbb")]
        assert len(w.asked) == 2

    def test_a_landing_asks_only_the_roles_that_run_as_their_kinds(self, w):
        import asks
        plan.landed_asks(w, self.fleet(design="on-demand"), "swancloud", "b", "landed")
        assert [a["Role"] for a in asks.parse(w.files["asks.rec"])[0]] == ["design"]
        from facts import FactsWrite
        none = FactsWrite("", None)
        none.label = "swancloud"
        plan.landed_asks(none, self.fleet(), "swancloud", "b", "landed")
        assert none.files == {} and none.asked == []

    @pytest.fixture
    def asked(self, monkeypatch):
        got = []
        monkeypatch.setattr(plan, "ask_write", lambda fleet, label, role, what, frm, names=None, key=None, words=None:
                            got.append((label, role, what, frm, names, key, words)))
        return got

    def test_a_landing_that_did_not_land_asks_ops_with_flumes_words_keyed_by_the_lands_request(self, asked):
        """role-runs, A landing that conflicts: crew's read writes an ask of ops with Flume's words, keyed by the land."""
        plan.unlanded_ask(self.fleet(ops="on-demand"), "swancloud", "y", "k", "412", "bolt/y did not land: #412 conflict: README.md")
        assert asked == [("swancloud", "ops", "landed", "crew", "bolt/y", "request/k/412", "bolt/y did not land: #412 conflict: README.md")]

    def test_one_stopped_with_no_submission_is_keyed_by_nothing(self, asked):
        plan.unlanded_ask(self.fleet(ops="on-demand"), "swancloud", "y", "k", None, "stopped")
        assert asked[0][5] is None

    def test_ops_that_stands_is_asked_nothing(self, asked):
        plan.unlanded_ask(self.fleet(planner="on-demand"), "swancloud", "y", "k", "412", "words")
        assert asked == []

    def test_an_ask_crew_could_not_write_is_said_and_the_read_goes_on(self, monkeypatch, capsys):
        monkeypatch.setattr(plan, "ask_write", lambda *a, **k: plan.fail("could not fetch swancloud/main"))
        plan.unlanded_ask(self.fleet(ops="on-demand"), "swancloud", "y", "k", "412", "words")
        assert capsys.readouterr().err == "could not ask swancloud-ops that bolt/y did not land: could not fetch swancloud/main\n"


# ------------------------------------------------------------------------- a landing read from the runner's report

COMMIT = "a7c3e9f1b2d4c6e8a0b1c3d5e7f9a1b3c5d7e9f0"


def base_run(fixture=None, more=None, land=True, refused=None):
    """y's base place, request 1 of crew, and its land, request 2, the runner on deneb answering the launch with the
    base place at the Flume 0.17.0 fixture named (tests/py/flume-0.17.0/bolt-*.json), or another version's named with
    its folder, and the land as given."""
    import runner
    from facts import ran
    from test_runner import BOLT, held, rec
    requests = held(rec(1, "launch", "bolt/y", **dict(BOLT, Name="y")), *([rec(2, "land", "bolt/y", Of=1)] if land else []))
    named = fixture if fixture and "/" in fixture else f"flume-0.17.0/{fixture}"
    reads = ran({1: named} if fixture else {}, label="swancloud", unplaced=more if more is not None else {2: "-"},
                refused=refused)
    return requests, reads


ASKED = dict(Act="bolt.submit", On=["bolt/y"], Card="req_k1", Head=TIP, Request="2", Outcome="asked")


def test_a_fix_while_the_landing_is_under_test_is_refused_naming_its_entry():
    """bolt-teams "A fix while the landing is queued": the runner carries y's base place with its submission #412 under
    test, and crew fix y logic is refused naming #412, its land's request beside it, at the tip it is applied to
    (plan.phase_at)."""
    import runner
    from facts import FactsWrite
    requests, reads = base_run("bolt-submitted")
    text = runner.REQUESTS + "".join("\n" + "\n".join(r.lines()) + "\n" for r in requests)
    w = FactsWrite("%rec: Bolt\n\nBolt: y\nRepo: crew\nPath: flume\n\n%rec: Unit\n\n", files={"requests.rec": text},
                   runners=reads, label="swancloud", entries=[ASKED])
    assert plan.landing_hold(plan.phase_at(w, "y"), "y", "fix y--logic").startswith(
        "bolt y has its landing #412 in the merge queue (request 2), so fix y--logic does not join it until its outcome is read")


class TestTheLandingsRecord:
    """bolt-teams "A landing's outcome is read from the runner's report" (Decision 6): what crew records of a landing
    once the runner's report decides it (plan.landing_entry), once per land, from the land it posted."""

    def entry(self, fixture, entries=(ASKED,), **more):
        import runner
        requests, reads = base_run(fixture, **more)
        l = runner.landing_of(requests[0], runner.lands_of(requests, requests[0]), reads)
        return l, plan.landing_entry(list(entries), "y", l)

    def test_a_landing_is_recorded_landed_with_its_land_and_the_head_it_carried(self):
        """run-record "A landing whose entry Flume names": the landed bolt.submit carries Submission 412."""
        l, got = self.entry("bolt-landed")
        assert got == dict(Request="2", Head=TIP, Submission="412", Outcome="landed",
                           Why=f"bolt(y): landed on main at {COMMIT[:7]}, as the runner reports it")

    def test_a_failed_check_and_a_conflict_are_recorded_refused_in_flumes_words(self):
        _, failed = self.entry("bolt-failed")
        assert failed["Refused"] == "landing refused, a check failed: check-full failed: tests:logic 3 failed (tests/py/test_landing.py)"
        _, conflict = self.entry("bolt-conflict")
        assert conflict["Refused"].startswith("landing refused in conflict with main at 9f1c2ab: bolt/the-runner-lands-each-bolt conflicts")
        assert (failed["Head"], failed["Request"], failed["Submission"]) == (TIP, "2", "412")

    def test_a_stop_is_recorded_stopped_with_its_words(self):
        _, got = self.entry("bolt-withdrawn")
        assert (got["Outcome"], got["Why"], got.get("Refused")) == ("stopped", "the merge queue withdrew the submission", None)

    def test_a_land_the_runner_refused_is_recorded_stopped_with_no_submission(self):
        """run-record "A land the runner refused": the runner answered land 2 of y refused, a place on bolt/y live,
        Flume naming no submission; the bolt.submit carries no Submission."""
        _, got = self.entry("bolt-submitted", more={}, refused={2: "flume refused it: a place on bolt/y is live"})
        assert (got["Outcome"], got["Why"], got["Request"], got["Submission"]) == (
            "stopped", "flume refused it: a place on bolt/y is live", "2", None)

    def test_one_recorded_already_and_one_undecided_are_recorded_nothing(self):
        _, got = self.entry("bolt-failed")
        assert self.entry("bolt-failed", entries=(ASKED, dict(ASKED, Outcome=None, Refused=got["Refused"])))[1] is None
        assert self.entry("bolt-submitted")[1] is None
        assert self.entry("bolt-submitted", more={})[1] is None  # its land not yet answered: asked


class TestTheFirstReadActs:
    """bolt-teams "A landing is recorded by the first act that reads it in the runner's report" (Decision 7):
    plan.landing_read, on whichever host reads it, with no ssh: a landing closes the bolt at Flume's commit in ops's
    name; a failed check asks ops with Flume's words, its row held by the record (refusals); a conflict launches the
    take-main fix once, keyed by main's revision; a stop asks ops and keeps the row's box (stops); a second read records
    nothing more."""

    @pytest.fixture(autouse=True)
    def acts(self, monkeypatch):
        import crew
        import record
        self.emitted, self.closed, self.asked, self.taken = [], [], [], []

        def no_host(*a, **k):
            raise AssertionError("a landing's read reaches no host")
        monkeypatch.setattr(crew, "on_machine", no_host)
        monkeypatch.setattr(plan, "host_run", no_host)
        from facts import writes_at
        self.tip = []  # the run record at the tip a write is applied to, which read() sets and each write joins
        self.emitted = writes_at(monkeypatch, self.tip)
        monkeypatch.setattr(record, "emit", lambda label, act, on=(), *a, **f: self.emitted.append(dict(f, Act=act, On=list(on))))
        monkeypatch.setattr(plan, "plan_of", lambda fleet, label: plan.Plan("%rec: Bolt\n\nBolt: y\nRepo: crew\nPath: flume\n\n%rec: Unit\n\n"))
        monkeypatch.setattr(plan, "bolt_land", lambda fleet, a, by=None, close_why=None, card=True: self.closed.append((a.bolt, by, close_why, card)))
        monkeypatch.setattr(plan, "unlanded_ask", lambda fleet, label, bolt, kit, n, words: self.asked.append((bolt, kit, n, words)))
        monkeypatch.setattr(plan, "take_main_launch", lambda fleet, label, t, bolt, conflict: self.taken.append((bolt, conflict)))
        monkeypatch.setenv("CREW_AGENT", "swancloud-planner")

    def read(self, fixture, entries=(ASKED,), card=True, **more):
        self.tip[:] = list(entries) + [e for e in self.tip if e not in entries]
        return plan.landing_read({}, "swancloud", "y", base_run(fixture, **more), list(entries), card)

    def test_a_landing_closes_the_bolt_at_flumes_commit_in_ops_name(self):
        assert self.read("bolt-landed", card=False)[0] is True
        (e,) = self.emitted
        assert (e["Act"], e["Outcome"], e["Request"], e["Submission"], e["by"]) == ("bolt.submit", "landed", "2", "412", "swancloud-ops")
        assert self.closed == [("y", "swancloud-ops", "plan(y): land the bolt, landed at a7c3e9f as the runner reports it, read by "
                                "swancloud-planner", False)]
        assert self.asked == [] and self.taken == []

    def test_a_landing_whose_close_is_refused_is_recorded_landed_all_the_same(self, monkeypatch):
        def refused(fleet, a, by=None, close_why=None, card=True):
            raise plan.Refusal("chore c was added to y since it was checked; it has not landed")
        monkeypatch.setattr(plan, "bolt_land", refused)
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: list(self.tip))
        assert self.read("bolt-landed")[0] is True
        submit, close = self.emitted
        assert (submit["Act"], submit["Outcome"], submit["Submission"], submit["by"]) == ("bolt.submit", "landed", "412", "swancloud-ops")
        assert (close["Act"], close["refused"]) == ("bolt.land", "chore c was added to y since it was checked; it has not landed")

    def test_two_reads_at_once_record_once(self, monkeypatch):
        """bolt-teams "Two reads at once": the second read's write is applied to a tip that holds the first's entry, so
        it writes nothing, asks nothing, and a close the first made is no refusal of the second's."""
        self.read("bolt-failed")
        first = list(self.tip)
        plan.landing_read({}, "swancloud", "y", base_run("bolt-failed"), [ASKED], True)  # read below the first's write
        assert [e["Act"] for e in self.emitted] == ["bolt.submit"] and len(self.asked) == 1 and self.tip == first
        landed = [ASKED, dict(ASKED, Outcome="landed", Request="2"), {"Act": "bolt.land", "On": ["bolt/y"], "Head": COMMIT}]
        assert plan.closed_already([{"Act": "bolt.start", "On": ["bolt/y"]}] + landed, "y")
        assert not plan.closed_already([{"Act": "bolt.start", "On": ["bolt/y"]}, dict(landed[2], Refused="no")], "y")

    def test_a_failed_check_is_recorded_once_and_asks_ops_with_flumes_words(self):
        assert self.read("bolt-failed")[0] is False
        (e,) = self.emitted
        assert e["refused"].startswith("landing refused, a check failed: check-full failed") and e["Head"] == TIP
        assert self.asked == [("y", "crew", "2", e["refused"])] and self.taken == [] and self.closed == []
        self.read("bolt-failed", entries=(ASKED, dict(ASKED, Outcome=None, Refused=e["refused"])))
        assert len(self.emitted) == 1 and len(self.asked) == 1
        assert plan.refusals([ASKED, dict(ASKED, Outcome=None, Refused=e["refused"])]) == {"y": (TIP, e["refused"])}

    def test_a_conflict_launches_the_take_main_fix_with_mains_revision_and_flumes_words(self):
        self.read("bolt-conflict")
        (bolt, (main, words, request)), = self.taken
        assert (bolt, main, request) == ("y", "9f1c2ab07d6e5f4a3b2c1d0e9f8a7b6c5d4e3f21", 2) and "conflicts with main" in words

    def test_a_conflict_flumes_landing_fix_takes_in_is_recorded_and_nothing_taken_or_asked(self):
        """bolt-teams "Flume's fix takes main in" (crews-bolt-kind-names-its-landing-fix, Decision 4): y's landing refused
        for a conflict with y-1 live; the refusal is recorded, no take-main fix launched and ops asked nothing."""
        assert self.read("flume-0.19.0/bolt-conflict-fixing")[0] is False
        (e,) = self.emitted
        assert e["Act"] == "bolt.submit" and e["refused"].startswith("landing refused in conflict with main at 9f1c2ab")
        assert self.taken == [] and self.asked == []

    def test_a_failure_whose_landing_fix_is_due_is_recorded_and_nothing_asked(self):
        """bolt-teams "Flume's fix due"."""
        self.read("flume-0.19.0/bolt-failed-fix-due")
        (e,) = self.emitted
        assert e["refused"].startswith("landing refused, a check failed") and self.taken == [] and self.asked == []

    def test_past_the_bound_ops_is_asked_once_in_flumes_words_and_nothing_taken(self):
        """bolt-teams "Past the bound" and "Read twice past the bound": one ask of ops naming the three landing fixes
        and Flume's words, keyed by the land's request, no launch, and a second read asks nothing more."""
        self.read("flume-0.19.0/bolt-failed-spent")
        (e,) = self.emitted
        assert self.asked == [("y", "crew", "2", "Flume ran 3 of its 3 landing fixes on bolt y, and its landing was refused: "
                                                "check-full failed: tests:logic 3 failed (tests/py/test_landing.py)")]
        assert self.taken == []
        self.read("flume-0.19.0/bolt-failed-spent", entries=(ASKED, dict(ASKED, Outcome=None, Refused=e["refused"])))
        assert len(self.emitted) == 1 and len(self.asked) == 1 and self.taken == []

    def test_a_landing_fix_dropped_asks_ops_once_naming_the_drop_and_nothing_taken(self):
        """bolt-teams "A fix dropped": a conflict whose fix y-1 was dropped asks ops naming the drop, no take-main fix."""
        self.read("flume-0.19.0/bolt-conflict-dropped")
        ((bolt, kit, n, words),) = self.asked
        assert (bolt, kit, n) == ("y", "crew", "2") and self.taken == []
        assert words.startswith("Flume's landing fix y-1 was dropped, and bolt y's landing was refused: bolt/y conflicts with main")

    def test_a_stop_keeps_the_rows_box_and_asks_ops(self):
        self.read("bolt-withdrawn")
        (e,) = self.emitted
        stopped = dict(ASKED, Outcome="stopped", Why=e["why"])
        assert plan.stops([ASKED, stopped]) == {"y": (TIP, "the merge queue withdrew the submission")}
        assert plan.refusals([ASKED, stopped]) == {} and self.asked[0][2] == "2"

    def test_a_land_the_runner_refused_is_a_stop_in_its_words(self):
        self.read("bolt-submitted", more={}, refused={2: "flume refused it: a place on bolt/y is live"})
        (e,) = self.emitted
        assert (e["Outcome"], e["why"]) == ("stopped", "flume refused it: a place on bolt/y is live")

    def test_a_launch_refused_for_a_kind_its_host_has_not_locked_reads_unlaunched_and_appends_nothing(self):
        """bolt-teams "A kind its host has not locked": the runner answered y's launch refused in Flume's words naming
        the lock; a read of y says so, records nothing and appends no request, so nothing launches it again."""
        import runner
        requests, reads = base_run(refused={1: "flume refused the launch: crew/bolt@1 is not locked on deneb"})
        launch = runner.launch_of(requests, "bolt/y")
        assert runner.landing_of(launch, runner.lands_of(requests, launch), reads) == {
            "outcome": "unlaunched", "words": "flume refused the launch: crew/bolt@1 is not locked on deneb", "refused": True}
        assert plan.landing_read({}, "swancloud", "y", (requests, reads), [ASKED], True) == (
            False, "its base place is unlaunched: the runner refused its launch: flume refused the launch: crew/bolt@1 is not "
                   "locked on deneb; crew bolt start runs it again")
        assert self.emitted == [] and self.closed == [] and self.asked == [] and self.taken == []

    def test_three_bolts_on_one_send_two_land_and_the_conflicting_one_takes_main_in(self):
        """bolt-teams "Three bolts on one send": lands of y, z and w posted in that order; the runner reports y and w
        landed and z refused in conflict; y and w are closed and z's take-main fix is launched, none holding another."""
        import runner
        from facts import ran
        from test_runner import BOLT, held, rec
        requests = held(*[rec(n, "launch", f"bolt/{b}", **dict(BOLT, Name=b)) for n, b in ((1, "y"), (2, "z"), (3, "w"))],
                        *[rec(n + 3, "land", f"bolt/{b}", Of=n) for n, b in ((1, "y"), (2, "z"), (3, "w"))])
        reads = ran({1: "flume-0.17.0/bolt-landed", 2: "flume-0.17.0/bolt-conflict", 3: "flume-0.17.0/bolt-landed"},
                    label="swancloud", unplaced={4: "-", 5: "-", 6: "-"})
        self.tip[:] = [dict(Act="bolt.submit", On=[f"bolt/{b}"], Card="req_k1", Head=TIP, Request=str(n), Outcome="asked")
                       for n, b in ((4, "y"), (5, "z"), (6, "w"))]
        mp = pytest.MonkeyPatch()
        mp.setattr(plan, "plan_of", lambda fleet, label: plan.Plan(
            "%rec: Bolt\n\n" + "".join(f"Bolt: {b}\nRepo: crew\nPath: flume\n\n" for b in "yzw") + "%rec: Unit\n\n"))
        try:
            got = [plan.landing_read({}, "swancloud", b, (requests, reads), list(self.tip), True)[0] for b in "yzw"]
        finally:
            mp.undo()
        assert got == [True, False, True]
        assert [c[0] for c in self.closed] == ["y", "w"] and [t[0] for t in self.taken] == ["z"]
        assert [(e["On"], e.get("Outcome"), bool(e.get("refused"))) for e in self.emitted] == [
            (["bolt/y"], "landed", False), (["bolt/z"], None, True), (["bolt/w"], "landed", False)]

    def test_undecided_or_unknown_it_records_nothing(self):
        assert self.read("bolt-submitted") == (False, "landing #412 under test")
        assert self.read("bolt-submitted", more={})[1] == "landing asked, request 2"
        assert self.emitted == [] and self.closed == [] and self.asked == []

    def test_a_bolt_started_before_bolts_were_base_places_is_said_so_and_read_no_further(self, monkeypatch):
        """w, with no launch of its own, its kit's main not holding its work (TestALandingReadOnMainCloses reads one main
        holds)."""
        import runner
        monkeypatch.setattr(plan, "main_tip", lambda repo: "e" * 40)
        monkeypatch.setattr(plan, "main_holds", lambda repo, tip, commits: dict.fromkeys(commits, 1))
        got = plan.landing_read({}, "swancloud", "w", base_run("bolt-landed"), [ASKED])
        assert got == (False, runner.legacy_said("w")) and self.emitted == []


# boomdrive's a-boomdrive-release-reports-its-own-version on 2026-11-12 as y: its head, main's commit that landed it, and
# an older crew's entries, its landing queued as #154 at the head and then stopped there with no submission.
HEAD, ON_MAIN = "62d2f06" + "0" * 33, "6cfc4ae" + "0" * 33
OLDER = [{"Act": "bolt.start", "On": ["bolt/y"], "At": "2026-11-11T20:00:00Z"}, submitted("y", HEAD, Outcome="queued", Submission="154"),
         submitted("y", HEAD, Outcome="stopped", Why="boomdrive's main checkout on deneb has no branch main and no origin")]
READ_ON_MAIN = {"outcome": "landed", "by": "main", "kit": "boomdrive", "commit": ON_MAIN, "head": HEAD, "submission": "154", "request": None}


class TestALandingReadOnMainIsRecorded:
    """bolt-teams "A bolt read landed on main is recorded and closed by the first act that reads it" (a-landed-bolt-is-
    closed-and-offered-no-more, Decision 5): plan.landing_entry records a landing read on main once, landed, naming the
    head its newest landing carried and the submission still pending, which ends an older crew's queued landing and its
    stop."""

    def test_an_older_crews_landing_is_recorded_landed_with_its_submission_and_head(self):
        assert plan.landing_entry(OLDER, "y", READ_ON_MAIN) == dict(
            Request=None, Head=HEAD, Submission="154", Outcome="landed",
            Why="bolt(y): landed on boomdrive's main at 6cfc4ae, as GitHub's main holds it")
        assert plan.outcome_fields(plan.landing_entry(OLDER, "y", READ_ON_MAIN)) == dict(
            Head=HEAD, Submission="154", Outcome="landed", why="bolt(y): landed on boomdrive's main at 6cfc4ae, as GitHub's main holds it")

    def test_its_entry_ends_the_queued_landing_and_the_stop(self):
        assert plan.landing_phase(OLDER, "y")["state"] == "queued" and plan.stops(OLDER)["y"][0] == HEAD
        recorded = OLDER + [submitted("y", HEAD, **{k: v for k, v in plan.landing_entry(OLDER, "y", READ_ON_MAIN).items() if v})]
        assert plan.landing_phase(recorded, "y") is None and "y" not in plan.stops(recorded)
        assert plan.landing_pending(recorded, "y") is None

    def test_the_same_read_again_records_nothing(self):
        recorded = OLDER + [submitted("y", HEAD, **{k: v for k, v in plan.landing_entry(OLDER, "y", READ_ON_MAIN).items() if v})]
        assert plan.landing_entry(recorded, "y", READ_ON_MAIN) is None


UNIT = "896e642" + "0" * 33  # the commit y's unit a's place landed at on bolt/y


class TestALandingReadOnMainCloses:
    """bolt-teams "A bolt read landed on main is recorded and closed by the first act that reads it" (a-landed-bolt-is-
    closed-and-offered-no-more, Decision 5), beside TestTheFirstReadActs: plan.landing_read of a bolt whose landing the
    runner's report does not read landed, one with no launch of its own among them, records it landed and closes it in
    ops's name once its kit's main holds its work, asking ops nothing; main not holding it leaves today's outcomes.
    main_tip, main_holds and landed_by stand for git, and nothing reaches a host."""
    FLEET = {"drives": {"madswan": {"label": "madswan", "machine": "deneb"}}, "hosts": {}}

    @pytest.fixture(autouse=True)
    def acts(self, monkeypatch):
        import crew
        import record
        from facts import writes_at

        def no_host(*a, **k):
            raise AssertionError("a landing's read reaches no host")
        monkeypatch.setattr(crew, "on_machine", no_host)
        monkeypatch.setattr(plan, "host_run", no_host)
        self.mp, self.tip, self.closed, self.asked, self.taken = monkeypatch, list(OLDER), [], [], []
        self.emitted = writes_at(monkeypatch, self.tip, label="madswan")
        monkeypatch.setattr(record, "emit", lambda label, act, on=(), *a, **f: self.emitted.append(dict(f, Act=act, On=list(on))))
        monkeypatch.setattr(plan, "bolt_land", lambda fleet, a, by=None, close_why=None, card=True: self.closed.append((a.bolt, by, close_why, card)))
        monkeypatch.setattr(plan, "unlanded_ask", lambda fleet, label, bolt, kit, n, words: self.asked.append((bolt, kit, n, words)))
        monkeypatch.setattr(plan, "take_main_launch", lambda fleet, label, t, bolt, conflict: self.taken.append((bolt, conflict)))
        monkeypatch.setenv("CREW_AGENT", "madswan-planner")
        self.held = {HEAD: 0, UNIT: 0}
        monkeypatch.setattr(plan, "main_tip", lambda repo: "e" * 40)
        monkeypatch.setattr(plan, "main_holds", lambda repo, tip, commits: {c: self.held.get(c, 1) for c in commits})
        monkeypatch.setattr(plan, "landed_by", lambda repo, tip, commits: ON_MAIN)

    def read(self, launched, base=False, more=(), **ran_):
        """landing_read of y, started, holding unit a launched as request 1, and, with base, y's base place as request
        2, with the requests in more beside them and deneb's runner as facts.ran gives it."""
        from facts import launched as launch, ran
        p, requests = launch(["y"], work=[("a", "y", [], "unit", [])], fleet=self.FLEET, base=base)
        self.mp.setattr(plan, "plan_of", lambda fleet, label: p)
        return plan.landing_read(self.FLEET, "madswan", "y", (requests + list(more), ran(launched, **ran_)), list(self.tip), True)

    def stopped(self):
        from test_runner import held, rec
        return dict(base=True, more=held(rec(3, "land", "bolt/y", Of=2)), commits={1: UNIT},
                    refused={3: "flume refused it: a place on bolt/y is live"})

    def test_a_bolt_with_no_launch_of_its_own_on_main_is_recorded_and_closed(self):
        got = self.read({1: "flume-0.20.0/landed-held"}, commits={1: UNIT})
        assert got == (True, "landed at 6cfc4ae, as its kit's main holds it")
        (e,) = self.emitted
        assert (e["Act"], e["Outcome"], e["Submission"], e["Head"], e["by"], e["why"]) == (
            "bolt.submit", "landed", "154", HEAD, "madswan-ops", "bolt(y): landed on crew's main at 6cfc4ae, as GitHub's main holds it")
        assert self.closed == [("y", "madswan-ops", "plan(y): land the bolt, landed at 6cfc4ae as its kit's main holds it on "
                                "GitHub, read by madswan-planner", True)]
        assert self.asked == [] and self.taken == []
        assert plan.landing_phase(self.tip, "y") is None and "y" not in plan.stops(self.tip)

    def test_a_base_place_reported_stopped_on_main_is_closed_and_ops_asked_nothing(self):
        assert self.read({1: "flume-0.20.0/landed-held", 2: "flume-0.17.0/bolt-submitted"}, **self.stopped())[0] is True
        assert [(e["Act"], e["Outcome"]) for e in self.emitted] == [("bolt.submit", "landed")]
        assert [c[0] for c in self.closed] == ["y"] and self.asked == []

    def test_main_not_holding_it_leaves_todays_outcomes(self):
        import runner
        self.held[UNIT] = 1
        assert self.read({1: "flume-0.20.0/landed-held"}, commits={1: UNIT}) == (False, runner.legacy_said("y"))
        assert self.emitted == [] and self.closed == []
        assert self.read({1: "flume-0.20.0/landed-held", 2: "flume-0.17.0/bolt-submitted"}, **self.stopped())[0] is False
        assert [(e["Act"], e["Outcome"]) for e in self.emitted] == [("bolt.submit", "stopped")]
        assert self.closed == [] and len(self.asked) == 1


class TestALandingIsRecordedInTheRunRecordAsAsked:
    """bolt-teams "A bolt's landing reads queued, rejected or landing again from the run record" (Decision 7): while a land crew posted stands undecided in
    the run record, the bolt's landing reads asked with its request, and no unit, chore or fix joins it."""

    def test_asked_until_its_outcome_is_recorded(self):
        assert plan.landing_phase([ASKED], "y") == dict(state="asked", n="2", head=TIP)
        assert plan.phase_said(plan.landing_phase([ASKED], "y"), TIP) == "landing asked, request 2"
        assert plan.landing_hold(plan.landing_phase([ASKED], "y"), "y", "unit a").startswith(
            "bolt y has its landing asked of the runner (request 2), so unit a does not join it until its outcome is read")
        landed = dict(ASKED, Outcome="landed")
        assert plan.landing_phase([ASKED, landed], "y") is None
        refused = dict(ASKED, Outcome=None, Refused="landing refused, a check failed: x")
        assert plan.landing_phase([ASKED, refused], "y")["state"] == "rejected"


class TestCrewBoltLandOfAStartedBolt:
    """bolt-plan "A landed bolt leaves the plan with its units" (Decision 7) and bolt-teams "crew bolt land closes a
    started bolt only once its base place reads landed": crew bolt land closes a started bolt once its landing reads
    landed from the runner's report, at Flume's commit, the record Flume holds for the runner after it tidies the base
    place among them, with its age and split from the run record, deleting no branch; or once its kit's main on GitHub
    holds its work, at main's commit that landed it, a bolt started before bolts were base places among them
    (a-landed-bolt-is-closed-and-offered-no-more, Decision 5); refused, recording nothing, naming its outcome and why
    main does not hold its work otherwise, no landing commit's trailer read for it and no kit's folder on any host.
    main_tip, main_holds and landed_by stand for git, main holding what held names."""
    PLAN = "%rec: Bolt\n\nBolt: y\nRepo: crew\nPath: flume\n\n%rec: Unit\n\nUnit: a\nRepo: crew\nBolt: y\nIntent: A.\n\n"

    @pytest.fixture(autouse=True)
    def world(self, monkeypatch):
        import crew
        self.written, self.changes, self.held = [], [], {}
        monkeypatch.setattr(plan, "main_tip", lambda repo: "e" * 40)
        monkeypatch.setattr(plan, "main_holds", lambda repo, tip, commits: {c: self.held.get(c, 1) for c in commits})
        monkeypatch.setattr(plan, "landed_by", lambda repo, tip, commits: ON_MAIN)

        def no_host(*a, **k):
            raise AssertionError("crew bolt land of a started bolt reaches no host")
        monkeypatch.setattr(crew, "on_machine", no_host)
        monkeypatch.setattr(plan, "host_run", no_host)
        monkeypatch.setattr(plan, "locate", lambda fleet, kind, name, label: ("swancloud", "o/state", "tip", plan.Plan(self.PLAN)))
        monkeypatch.setattr(plan, "default_label", lambda fleet, a: "swancloud")
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: [])
        monkeypatch.setattr(plan, "write", lambda fleet, label, change, subject, **k: (self.written.append((subject, k)),
                                                                                       self.changes.append(change)))
        monkeypatch.setattr(plan, "launched_at", lambda *a, **k: None)
        monkeypatch.setattr(plan, "land_hand", lambda *a, **k: None)

        def no_kit(*a, **k):
            raise AssertionError("crew bolt land of a started bolt reads no kit on any host, its checkout of main among them")
        monkeypatch.setattr(plan, "stages_for", no_kit)
        monkeypatch.setattr(plan, "survey", no_kit)

    def land(self, monkeypatch, run, bolt="y"):
        monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: run)
        return plan.bolt_land({}, argparse.Namespace(cmd="bolt", sub="land", bolt=bolt, label="swancloud"), by="swancloud-ops")

    def test_a_landed_bolt_closes_at_flumes_commit(self, monkeypatch):
        self.land(monkeypatch, base_run("bolt-landed"))
        (subject, k), = self.written
        assert subject == "plan(y): land the bolt" and k["act"] == "bolt.land"
        assert (k["fields"]["Repo"], k["fields"]["Head"]) == ("crew", COMMIT) and k["by"] == "swancloud-ops"

    @pytest.mark.parametrize("fixture, said", [
        ("bolt-submitted", "landing #412 under test"),
        ("bolt-failed", "landing refused, a check failed: check-full failed"),
        (None, "its base place is not launched")])
    def test_a_bolt_not_read_landed_is_refused_naming_its_outcome_and_records_nothing(self, monkeypatch, fixture, said):
        with pytest.raises(plan.Refusal) as e:
            self.land(monkeypatch, base_run(fixture))
        assert str(e.value).startswith("bolt y has not landed, so crew bolt land closes nothing of it: " + said)
        assert self.written == []

    def test_a_bolt_with_no_land_asked_says_so(self, monkeypatch):
        with pytest.raises(plan.Refusal, match="no land of it has been asked of the runner: it lands on the user's send"):
            self.land(monkeypatch, base_run("bolt-submitted", land=False, more={}))

    def unit_merged(self, more=(), **ran_):
        """y's unit a launched as request 1 on bolt/y, its place landed there at UNIT, and the requests in more beside
        it, deneb's runner as facts.ran gives it."""
        from facts import ran
        from test_runner import held, rec
        return held(rec(1, "launch", "unit/a", Base="bolt/y"), *more), ran({1: "flume-0.20.0/landed-held"}, label="swancloud",
                                                                            commits={1: UNIT}, **ran_)

    def test_a_bolt_started_before_bolts_were_base_places_is_refused_while_main_lacks_its_work(self, monkeypatch):
        """bolt-teams "crew bolt land refuses it" (a bolt started before bolts were base places): y has no launch
        of its own, and its unit a's place landed on bolt/y at a commit main does not hold; crew bolt land refuses it in
        runner.legacy_said's words and main's, reading no kit's folder (no_kit) and recording nothing."""
        import runner
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: list(OLDER))
        self.held = {HEAD: 0}
        with pytest.raises(plan.Refusal) as e:
            self.land(monkeypatch, self.unit_merged())
        assert str(e.value) == (f"{runner.legacy_said('y')}, and crew's main does not hold its work: unit a has not landed on "
                                "crew's main: its place landed on bolt/y at 896e642, which main does not hold, so crew bolt "
                                "land closes nothing of it here") and self.written == []

    def test_a_bolt_started_before_bolts_were_base_places_closes_once_main_holds_its_work(self, monkeypatch):
        """bolt-teams "crew bolt land closes it once main holds its work": an older crew's landing of y queued as #154
        and stopped at 62d2f06, and GitHub's main holding that head and a's commit, landed by 6cfc4ae; crew bolt land
        closes y at 6cfc4ae in ops's name, its bolt.submit landed in the same commit."""
        import crew
        from facts import FactsWrite
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: list(OLDER))
        monkeypatch.setattr(plan, "landed_asks", lambda *a, **k: None)
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        self.held = {HEAD: 0, UNIT: 0}
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.land(monkeypatch, self.unit_merged())
        (subject, k), = self.written
        assert subject == "plan(y): land the bolt" and (k["fields"]["Repo"], k["fields"]["Head"], k["by"]) == ("crew", ON_MAIN, "swancloud-ops")
        assert "y has landed at crew's 6cfc4ae, as GitHub's main holds it" in out.getvalue()
        w = FactsWrite(self.PLAN, label="swancloud", entries=OLDER)
        self.changes[0](w)
        [(_, act, on, fields)] = w.also
        assert (act, on, fields) == ("bolt.submit", ["bolt/y"], dict(
            Head=HEAD, Submission="154", Outcome="landed", why="bolt(y): landed on crew's main at 6cfc4ae, as GitHub's main holds it"))

    def test_a_stopped_base_place_closes_once_main_holds_its_head_and_its_chores_commit(self, monkeypatch):
        """bolt-teams "A landing main holds": the runner reports y's landing stopped at 9c1e4b7, and GitHub's main holds
        9c1e4b7 and the commit y's chore c landed at on bolt/y; crew bolt land closes y at main's commit that landed it."""
        from facts import ran
        from test_runner import BOLT, held, rec
        stop, chore = "9c1e4b7" + "0" * 33, "c40e000" + "0" * 33
        self.PLAN = "%rec: Bolt\n\nBolt: y\nRepo: crew\nPath: flume\n\n%rec: Unit\n\nUnit: c\nRepo: crew\nBolt: y\nKind: chore\nIntent: C.\n\n"
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: [
            {"Act": "bolt.start", "On": ["bolt/y"], "At": "2026-11-11T20:00:00Z"}, dict(ASKED, Head=stop, Request="3"),
            submitted("y", stop, Request="3", Outcome="stopped", Why="flume refused it: a place on bolt/y is live")])
        self.held = {stop: 0, chore: 0}
        requests = held(rec(1, "launch", "chore/c", Base="bolt/y", Kind="chore"), rec(2, "launch", "bolt/y", **dict(BOLT, Name="y")),
                        rec(3, "land", "bolt/y", Of=2))
        reads = ran({1: "flume-0.20.0/landed-held", 2: "flume-0.17.0/bolt-submitted"}, label="swancloud", commits={1: chore},
                    refused={3: "flume refused it: a place on bolt/y is live"})
        self.land(monkeypatch, (requests, reads))
        (subject, k), = self.written
        assert subject == "plan(y): land the bolt" and (k["fields"]["Repo"], k["fields"]["Head"]) == ("crew", ON_MAIN)

    def test_a_base_place_held_for_the_runner_landed_closes_at_flumes_commit(self, monkeypatch):
        """bolt-teams "A base place held for the runner": Flume landed y's base place and tidied it, holding its
        record for the runner, flume 0.20.0's tidied phase, which the runner carries as its status; GitHub deleted
        bolt/y. crew bolt land closes y at the record's commit, as the runner reports it."""
        from facts import ran
        from test_runner import BOLT, held, rec
        requests = held(rec(1, "launch", "bolt/y", **dict(BOLT, Name="y")), rec(2, "land", "bolt/y", Of=1))
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.land(monkeypatch, (requests, ran({1: "flume-0.20.0/landed-held"}, label="swancloud", commits={1: COMMIT})))
        (subject, k), = self.written
        assert subject == "plan(y): land the bolt" and (k["fields"]["Repo"], k["fields"]["Head"]) == ("crew", COMMIT)
        assert "y has landed at crew's a7c3e9f, as the runner reports it" in out.getvalue()

    def test_a_base_place_the_runner_no_longer_carries_is_refused_whatever_main_holds(self, monkeypatch):
        """bolt-teams "A landing main holds that the runner does not report": the runner carries no status of y's base
        place, as a place tidied before its host's runner carried its end leaves it, and y's kit's main holds a commit
        whose Sluice-From names bolt/y, but neither y's head nor the commit its unit a landed at on bolt/y; crew bolt
        land is refused naming its landing as the runner reports it, asked, and why main does not hold its work,
        recording nothing and reading no kit's folder (no_kit): no trailer is read."""
        from test_runner import BOLT, held, rec
        requests, reads = self.unit_merged((rec(2, "launch", "bolt/y", **dict(BOLT, Name="y")), rec(3, "land", "bolt/y", Of=2)),
                                           unplaced={2: "/flume/places/bolt--y"})
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: [{"Act": "bolt.start", "On": ["bolt/y"]}, dict(ASKED, Request="3")])
        self.held = {"5ab1ce0" + "0" * 33: 0}  # sluice's landing commit naming bolt/y, which nothing asks
        with pytest.raises(plan.Refusal) as e:
            self.land(monkeypatch, (requests, reads))
        assert str(e.value) == ("bolt y has not landed, so crew bolt land closes nothing of it: landing asked, request 3; nor "
                                "does crew's main hold its work: unit a has not landed on crew's main: its place landed on "
                                "bolt/y at 896e642, which main does not hold")
        assert self.written == []
