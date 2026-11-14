"""A repository is renamed by one explicit command once its work is finished (a-repository-is-renamed-by-one-explicit-command;
record 0060; plan.22, record.4): crew kit rename <old> <new> renames every record a reader matches the repository by, the
plan's decision-record sources, requests.rec and the run record's entries on the drive's branch, in one commit with its
kit.rename entry (plan.rename_branch, rename_rec), refused while the repository's work stands (rename_standing) or a host
still keeps the old name (rename_kept), naming what stands (rename_refusal). The rename's one commit under a real recfix
is the contract tier's (tests/contract/test_recfix.py)."""
import json

import pytest

import plan
import runner

from facts import STANDING, FactsWrite, flume_fixture, keeping, known, plan_text

KIT_RENAME = """\
Id: 20261105T120000Z-1-deneb-1-1
At: 2026-11-05T12:00:00Z
Host: deneb
By: chuck
Act: kit.rename
On: kit/timber
From: kit/tailrace
Repo: timber
Count: 21
"""


class TestWhatAFieldBecomes:
    """Decision 1: each field a reader matches a repository by, renamed in its form; everything else as written."""

    def test_each_object_built_on_the_name_takes_the_new_name(self):
        for was, now in [("kit/tailrace", "kit/timber"), ("land/tailrace", "land/timber"), ("queue/tailrace", "queue/timber"),
                         ("record/tailrace/0017", "record/timber/0017"), ("fix/main/tailrace/cargo-lock", "fix/main/timber/cargo-lock")]:
            assert plan.renamed_object(was, "tailrace", "timber") == now
            assert plan.renamed_field("On", was, "tailrace", "timber") == now
            assert plan.renamed_object(was, "agentplot/tailrace", "agentplot/timber") == now

    def test_a_forge_address_keeps_its_owner_unless_the_new_name_is_an_address(self):
        assert plan.renamed_kit("agentplot/flywheel-cloud", "flywheel-cloud", "boomdrive-cloud") == "agentplot/boomdrive-cloud"
        assert plan.renamed_kit("flywheel-cloud", "flywheel-cloud", "boomdrive-cloud") == "boomdrive-cloud"
        assert plan.renamed_kit("agentplot/flywheel-cloud", "flywheel-cloud", "madswan/boomdrive-cloud") == "madswan/boomdrive-cloud"
        assert plan.renamed_kit("flywheel-cloud", "agentplot/flywheel-cloud", "agentplot/boomdrive-cloud") == "agentplot/boomdrive-cloud"
        assert plan.renamed_field("Repo", "agentplot/flywheel-cloud", "flywheel-cloud", "boomdrive-cloud") == "agentplot/boomdrive-cloud"

    def test_an_object_of_another_repository_is_as_it_was(self):
        for obj in ("kit/tailrace-web", "land/tailrace-web", "record/tailrace-web/0017", "fix/main/tailrace-web/x", "unit/tailrace",
                    "bolt/tailrace", "proposal/170"):
            assert plan.renamed_object(obj, "tailrace", "timber") == obj
        assert plan.renamed_kit("tailrace-web", "tailrace", "timber") == "tailrace-web"

    def test_a_sources_decision_record_is_renamed_and_its_words_kept(self):
        source = "agentplot/flywheel-cloud:docs/adr/0017 (the seam), as agentplot/crew:docs/adr/0060 rules"
        assert plan.renamed_field("Source", source, "flywheel-cloud", "boomdrive-cloud") == \
            "agentplot/boomdrive-cloud:docs/adr/0017 (the seam), as agentplot/crew:docs/adr/0060 rules"
        for words in ("flywheel-cloud's seam, as the user said", "signals/2026-11-07-agentplot-planner-cbc41169/01"):
            assert plan.renamed_source(words, "flywheel-cloud", "boomdrive-cloud") == words

    def test_a_key_and_any_other_field_is_as_it_was(self):
        assert plan.renamed_field("Key", "land/tailrace", "tailrace", "timber") == "land/tailrace"
        assert plan.renamed_field("Goal", "tailrace is built", "tailrace", "timber") == "tailrace is built"

    def test_a_kit_rename_entry_is_left_whole(self):
        text = plan.record.DESCRIPTOR + KIT_RENAME
        assert plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "timber", "trc") == (text, 0)
        assert plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "tailrace", "trc") == (text, 0)

    def test_a_text_naming_no_old_name_is_returned_byte_for_byte(self):
        text = plan.record.DESCRIPTOR + "Id: 1\nAt: 2026-11-05T12:00:00Z\nAct: bolt.land\nOn: bolt/crew-bolt\nRepo:  crew\n\n\n# a comment\n"
        assert plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "tailrace", "timber") == (text, 0)

    def test_a_record_is_renamed_field_by_field_and_counted_once(self):
        text = (plan.record.DESCRIPTOR + "Id: 1\nAct: card.post\nOn: kit/tailrace\nOn: land/tailrace\nKey: land/tailrace\nWhy: tailrace\n\n"
                + KIT_RENAME + "\nId: 3\nAct: bolt.land\nRepo: agentplot/tailrace\n")
        renamed, n = plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "tailrace", "timber")
        assert n == 2
        assert renamed == (plan.record.DESCRIPTOR + "Id: 1\nAct: card.post\nOn: kit/timber\nOn: land/timber\nKey: land/tailrace\nWhy: tailrace\n\n"
                           + KIT_RENAME + "\nId: 3\nAct: bolt.land\nRepo: agentplot/timber\n")


def requests(*recs):
    """requests.rec's text holding each request, (n, work, given), as crew writes it (runner.request_fields)."""
    return runner.REQUESTS + "".join("\n" + "\n".join(plan.Rec("Request", runner.request_fields(
        n, "launch", work, given, "2026-11-04T23:00:00Z", "chuck@deneb")).lines()) + "\n" for n, work, given in recs)


def fix_of_main(n, repo, name):
    """A launch of a fix of repo's main, as crew writes it (runner.request_refusal: its submission held)."""
    return (n, f"fix/main/{repo}/{name}", dict(Repo=repo, Kind="fix", Name=name, Base="main", Priority=1, Intent=f"madswan/{name}",
                                               Recipient="madswan/ops", Hold="submission", Brief=f"Fix {name}."))


def entry(n, act, on=(), frm=(), **fields):
    """A run-record entry's text as record.emit writes it, its id the n-th of deneb's on 2026-10-30."""
    lines = [f"Id: 20261030T1000{n:02d}Z-deneb-1-{n}", f"At: 2026-10-30T10:00:{n:02d}Z", "Host: deneb", "By: chuck", f"Act: {act}"]
    lines += [f"On: {o}" for o in on] + [f"From: {o}" for o in frm] + [f"{k}: {v}" for k, v in fields.items()]
    return "\n".join(lines) + "\n"


def runs(*entries):
    """A run-record file's text on the branch: the descriptor, then each entry."""
    return plan.record.DESCRIPTOR + "\n".join(entries)


# madswan's branch before flywheel-cloud is renamed boomdrive-cloud (Task notes 1.2): request 3, a fix of flywheel-cloud's
# main; a runs file holding its landing, its closed landings card and an entry on the fix; a second runs file naming
# nothing of it; a crew unit whose Source names a decision record of flywheel-cloud; and a closed proposal whose Do names it.
SEAM_REQUESTS = requests(fix_of_main(3, "flywheel-cloud", "x"))
DAY = runs(entry(1, "bolt.land", on=["bolt/you-sign-in-to-staging"], Repo="flywheel-cloud", Head="a" * 40),
           entry(2, "card.post", on=["kit/flywheel-cloud"], Card="req_1", Key="land/flywheel-cloud"),
           entry(3, "card.close", on=["land/flywheel-cloud"], Card="req_1", Key="land/flywheel-cloud", State="closed"),
           entry(4, "fix.start", on=["fix/main/flywheel-cloud/x"]))
QUIET = runs(entry(5, "bolt.land", on=["bolt/crew-bolt"], Repo="crew", Head="b" * 40))
PROPOSALS = """\
%rec: Proposal
%key: Proposal

Proposal: 160
State: approved
Do: unit add one-seam "One seam." --repo flywheel-cloud
"""


def madswan_branch(bolts=()):
    """madswan's write over that branch, its plan holding crew's bolt and each of bolts, (name, repo, started), and deneb's
    runner reporting request 3's place landed."""
    text = plan_text(bolts=[("crew-bolt", "crew", False), *bolts], units=[("crew-unit", "crew", "crew-bolt", [])])
    text = text.replace("Unit: crew-unit\n", "Unit: crew-unit\nSource: agentplot/flywheel-cloud:docs/adr/0017, the seam\n")
    text = text.replace("Goal: Goal of crew-bolt.", "Goal: crew reads flywheel-cloud's seam.")
    return FactsWrite(text, label="madswan", runners=reading(launched={3: "landed"}), files={
        "requests.rec": SEAM_REQUESTS, "runs/deneb/2026-10-30.rec": DAY, "runs/deneb/2026-10-31.rec": QUIET, "proposals.rec": PROPOSALS})


class TestWhatTheRenameRenames:
    """Decision 1: rename_branch renames the plan's sources, requests.rec and every run-record file at the tip, and
    replaces only the files it changed."""

    def test_flywheel_cloud_renamed_boomdrive_cloud_across_madswans_records(self):
        w = madswan_branch()
        n = plan.rename_branch(w, "flywheel-cloud", "boomdrive-cloud")
        rq = plan.Plan(w.files["requests.rec"]).recs("Request")[0]
        assert (rq.get("Repo"), rq.get("Work")) == ("boomdrive-cloud", "fix/main/boomdrive-cloud/x")
        day = plan.Plan(w.files["runs/deneb/2026-10-30.rec"]).recs("Entry")
        assert [(e.get("Repo"), e.all("On"), e.get("Key")) for e in day] == [
            ("boomdrive-cloud", ["bolt/you-sign-in-to-staging"], None), (None, ["kit/boomdrive-cloud"], "land/flywheel-cloud"),
            (None, ["land/boomdrive-cloud"], "land/flywheel-cloud"), (None, ["fix/main/boomdrive-cloud/x"], None)]
        assert w.plan.unit("crew-unit").get("Source") == "agentplot/boomdrive-cloud:docs/adr/0017, the seam"
        assert w.plan.bolt("crew-bolt").get("Goal") == "crew reads flywheel-cloud's seam."
        assert (w.files["runs/deneb/2026-10-31.rec"], w.files["proposals.rec"]) == (QUIET, PROPOSALS)
        assert sorted(w.files) == ["proposals.rec", "requests.rec", "runs/deneb/2026-10-30.rec", "runs/deneb/2026-10-31.rec"]
        assert n == 6 and w.renaming == [("flywheel-cloud", "boomdrive-cloud")]

    def test_a_hold_on_the_kit_is_renamed_with_it_and_still_holds_it(self):
        """plan.22 (Decision 6 of a-proven-bolt-lands-on-proof): a Hold names its kit by the name the drive's kits give it,
        so a rename renames the Hold's Kit with the rest, and the hold still stands on the kit by its new name; the drive's
        hold and another kit's are left as they are."""
        w = madswan_branch()
        w.plan = plan.Plan(w.plan.text() + "\n%rec: Hold\n\nKit: flywheel-cloud\nWhy: Cutover\n\nKit: crew\nWhy: Its own\n\nWhy: The move\n")
        assert plan.rename_branch(w, "flywheel-cloud", "boomdrive-cloud") == 7
        assert plan.holds_of(w.plan) == [dict(kit="boomdrive-cloud", why="Cutover"), dict(kit="crew", why="Its own"),
                                         dict(kit=None, why="The move")]
        assert plan.hold_on(w.plan, "boomdrive-cloud") == dict(kit="boomdrive-cloud", why="Cutover")

    def test_only_the_files_it_changed_are_replaced(self):
        w = madswan_branch()
        replaced = []
        w.replace = lambda path, text: replaced.append(path)
        plan.rename_branch(w, "flywheel-cloud", "boomdrive-cloud")
        assert replaced == ["requests.rec", "runs/deneb/2026-10-30.rec"]

    def test_a_name_no_record_holds_renames_nothing_and_records_no_rename(self):
        w = madswan_branch()
        text = w.plan.text()
        assert plan.rename_branch(w, "rocs-kit", "rocs") == 0
        assert (w.plan.text(), w.files["requests.rec"], w.files["runs/deneb/2026-10-30.rec"], w.renaming) == (
            text, SEAM_REQUESTS, DAY, [])


class TestAppendOnly:
    """Decision 6: requests.rec is changed only by appending, or by a rename's write, a request changing by its
    repository's name alone."""

    def renamed(self):
        return SEAM_REQUESTS.replace("Repo: flywheel-cloud", "Repo: boomdrive-cloud").replace(
            "Work: fix/main/flywheel-cloud/x", "Work: fix/main/boomdrive-cloud/x")

    def test_a_renames_write_with_request_3_renamed_passes(self, monkeypatch):
        assert plan.appended_refusal(SEAM_REQUESTS, self.renamed(), [("flywheel-cloud", "boomdrive-cloud")]) is None
        w = madswan_branch()
        plan.rename_branch(w, "flywheel-cloud", "boomdrive-cloud")
        monkeypatch.setattr(plan, "show", lambda repo, tip, path: SEAM_REQUESTS if path == "requests.rec" else None)
        plan.appended(w)
        w.renaming.clear()
        with pytest.raises(plan.Refusal, match="^request 3 would be changed in requests.rec"):
            plan.appended(w)

    def test_the_same_change_with_no_rename_on_the_write_is_refused(self):
        assert plan.appended_refusal(SEAM_REQUESTS, self.renamed()) == (
            "request 3 would be changed in requests.rec, and a request is never changed or removed: a later request "
            "retries, drops or reprioritises what it launched")

    def test_a_renames_write_that_also_changes_request_3s_name_is_refused(self):
        now = self.renamed().replace("Name: x", "Name: y")
        assert plan.appended_refusal(SEAM_REQUESTS, now, [("flywheel-cloud", "boomdrive-cloud")]).startswith(
            "request 3 would be changed in requests.rec, and a request is never changed or removed")

    def test_an_append_beside_a_rename_passes(self):
        now = self.renamed() + "\n" + "\n".join(plan.Rec("Request", runner.request_fields(
            4, "drop", "fix/main/boomdrive-cloud/x", dict(Of=3), "2026-11-07T12:00:00Z", "chuck@deneb")).lines()) + "\n"
        assert plan.appended_refusal(SEAM_REQUESTS, now, [("flywheel-cloud", "boomdrive-cloud")]) is None


def reading(host="deneb", launched=None, refused=None, bad=()):
    """host's runner of madswan as crew reads it (runner.host_read): each launch in launched, {request's number: a Flume
    status fixture of tests/py/flume-0.3.6}, answered launched and its place carried at the fixture's own place; each in
    refused, {number: words}, answered refused; and each in bad answered launched with a status that is no JSON."""
    answers, places = "", ""
    for n, name in (launched or {}).items():
        status = json.loads(flume_fixture(name).read_text())
        where = status["status"]["places"][0]["place"].split("@")[0]
        answers += f"\nRequest: {n}\nOutcome: launched\nPlace: {where}\nAt: 2026-11-07T10:01:00Z\n"
        places += f"\nRequest: {n}\nPlace: {where}\nAt: 2026-11-07T10:02:00Z\nStatus: {json.dumps(status)}\n"
    for n in bad:
        answers += f"\nRequest: {n}\nOutcome: launched\nPlace: /p/{n}\nAt: 2026-11-07T10:01:00Z\n"
        places += f"\nRequest: {n}\nPlace: /p/{n}\nAt: 2026-11-07T10:02:00Z\nStatus: not json\n"
    answers += "".join(f"\nRequest: {n}\nOutcome: refused\nWords: {w}\nAt: 2026-11-07T10:01:00Z\n" for n, w in (refused or {}).items())
    files = {"runner.rec": plan.Plan(runner.RUNNER + f"\nHost: {host}\nVersion: 0.1.0\nSince: 2026-11-07T09:00:00Z\n"),
             "answers.rec": plan.Plan(runner.ANSWERS + answers), "places.rec": plan.Plan(runner.PLACES + places)}
    return {host: runner.host_read("madswan", host, "5e1f0c2a" + "0" * 32, files, {})}


def unit_launch(n, unit, repo="tailrace", bolt="trc-1"):
    """A launch of a unit's place in repo, as a start writes it (runner.reach)."""
    return (n, f"unit/{unit}", dict(Repo=repo, Kind="change", Name=unit, Base=f"bolt/{bolt}", Priority=1, Intent=f"madswan/{bolt}",
                                    Recipient="madswan/planner", Brief=f"Build {unit}."))


def role_launch(n, repo, name):
    """A launch of the design agent's work in repo, as crew writes a role's (runner.request_refusal: its host and stream)."""
    return (n, f"role/design/{name}", dict(Host="deneb", Repo=repo, Kind="change", Name=name, Base="main", Stream="madswan",
                                           Priority=1, Intent=f"madswan/{name}", Recipient="madswan/design", Brief=f"Record {name}."))


def recs(text, kind="Request"):
    return plan.Plan(text).recs(kind)


def card(n, act, key, by="madswan-ops", state=None):
    """A card.post or card.close entry under key, as record.parse gives it, card req_<n>."""
    e = {"Id": f"20261107T1000{n:02d}Z-deneb-1-{n}", "At": f"2026-11-07T10:00:{n:02d}Z", "Act": act, "On": [key], "From": [],
         "Card": f"req_{n // 10}", "Key": key, "By": by}
    return dict(e, State=state) if state else e


def proposal(n, *dos, state="open"):
    return plan.Rec("Proposal", [("Proposal", str(n)), ("Case", "A case."), *[("Do", d) for d in dos], ("State", state)])


def standing(old="tailrace", text=None, requests_=(), reads=None, entries=(), proposals=(), own=None):
    return plan.rename_standing(old, plan.Plan(text or plan_text()), recs(requests(*requests_)), reads or {}, list(entries),
                                list(proposals), own)


class TestWhatStands:
    """Decision 2: each piece of the old name's work that stands, and apart what crew could not read."""

    def test_a_bolt_named_as_not_landed(self):
        text = plan_text(bolts=[("trc-1", "tailrace", False), ("crew-bolt", "crew", False)],
                         units=[("trc-u", "tailrace", "trc-1", [])])
        assert standing(text=text) == (["bolt trc-1 has not landed"], [])

    def test_a_queued_chore(self):
        text = plan_text(units=[("trc-queued", "agentplot/tailrace", None, [], "chore"), ("crew-queued", "crew", None, [])])
        assert standing(text=text) == (["chore trc-queued waits in tailrace's queue"], [])

    def test_a_fix_of_main_not_landed_named_with_its_stage(self):
        fixes = [fix_of_main(n, "tailrace", x) for n, x in ((1, "x"), (2, "landed"), (3, "dropped"), (4, "refused"))]
        reads = reading(launched={1: "code", 2: "landed", 3: "dropped"}, refused={4: "no stream maps tailrace"})
        assert standing(requests_=fixes, reads=reads) == (["fix/main/tailrace/x (request 1) is at code"], [])

    def test_a_roles_work_not_landed(self):
        assert standing(requests_=[role_launch(1, "agentplot/tailrace", "record-0061")], reads=reading()) == (
            ["role/design/record-0061 (request 1) is launching"], [])

    def test_a_live_place_and_none_over(self):
        reads = reading(launched={4: "code", 5: "landed"})
        found = standing(requests_=[unit_launch(1, "a", "crew", "crew-bolt"), unit_launch(2, "b", "crew", "crew-bolt"),
                                    unit_launch(3, "c", "crew", "crew-bolt"), unit_launch(4, "trc-live"), unit_launch(5, "trc-over")],
                         reads=reads)
        place = json.loads(flume_fixture("code").read_text())["status"]["places"][0]["place"]
        assert found == ([f"place {place} of request 4 (unit/trc-live) is live on deneb"], [])

    def test_a_status_that_is_no_json_and_an_unread_runner_are_unread(self):
        reads = dict(reading(bad=[1]), **{"vega": {"host": "vega", "why": "vega's runner can't be read: madswan/runner/vega at 1234567: x"}})
        stands, unread = standing(requests_=[unit_launch(1, "trc-a")], reads=reads)
        assert stands == [] and len(unread) == 2
        assert unread[0].startswith("madswan/runner/deneb at 5e1f0c2: places.rec's status of the place of request 1 is no JSON")
        assert unread[1] == "vega's runner can't be read: madswan/runner/vega at 1234567: x"

    def test_open_and_lost_cards_and_none_closed(self):
        entries = [card(10, "card.post", "land/tailrace"), card(20, "card.post", "record/tailrace/17", by="madswan-design"),
                   card(30, "card.post", "record/agentplot/tailrace", by="madswan-design"),
                   card(40, "card.post", "record/tailrace/18/abc1234", by="madswan-design"), card(41, "card.close", "record/tailrace/18/abc1234",
                                                                                               state="lost"),
                   card(50, "card.post", "land/tailrace-web"), card(60, "card.post", "land/crew")]
        assert standing(entries=entries) == ([
            "madswan-ops's card land/tailrace is open", "madswan-design's card record/tailrace/17 is open",
            "madswan-design's card record/tailrace/18/abc1234 was lost to its owner, and the rail raises it again"], [])

    def test_a_closed_card_names_nothing(self):
        entries = [card(10, "card.post", "land/tailrace"), card(11, "card.close", "land/tailrace", state="closed")]
        assert standing(entries=entries) == ([], [])

    def test_an_unanswered_unsettled_batch_holding_a_landed_unit_and_none_settled(self):
        land = {"Id": "1", "At": "2026-11-07T09:00:00Z", "Act": "bolt.land", "On": ["bolt/trc-1", "unit/trc-u"], "From": [],
                "Repo": "tailrace"}
        batch = lambda n, units: {"Id": str(n), "At": f"2026-11-07T09:{n:02d}:00Z", "Act": "review.batch", "Batch": str(n),
                                  "Units": units, "On": [f"batch/{n}"], "From": []}
        entries = [batch(12, "trc-u:trc-1@abc1234 other-u:other@def5678"), batch(13, "trc-u:trc-1@abc1234"), land]
        assert standing(entries=entries) == (["batch 12 is unanswered and holds trc-u"], [])

    def test_open_proposals_naming_it_and_none_else(self):
        props = [proposal(170, 'unit add x "X is built." --repo tailrace'), proposal(171, "unit add y \"Y.\" --repo crew "
                                                                                          "--source agentplot/tailrace:docs/adr/0017"),
                 proposal(172, 'bolt new z "tailrace is fast, as the user asked." --repo crew'), proposal(173, "kit rename tailrace timber"),
                 proposal(174, 'unit add w "W." --repo tailrace', state="approved"), proposal(175, "kit rename tailrace timber")]
        assert standing(proposals=props, own="173") == (["proposal 170 is open and names tailrace", "proposal 171 is open and names tailrace",
                                                         "proposal 175 is open and names tailrace"], [])

    def test_nothing_standing(self):
        text = plan_text(bolts=[("crew-bolt", "crew", False)], units=[("crew-unit", "crew", "crew-bolt", [])])
        assert standing(text=text, requests_=[fix_of_main(1, "tailrace", "x")], reads=reading(launched={1: "landed"}),
                        entries=[card(10, "card.post", "land/tailrace"), card(11, "card.close", "land/tailrace", state="closed")]) == ([], [])


class TestWhatAHostKeeps:
    """bolt-plan "A host's keeping is its runner's repositories, and otherwise the teams file's"; Decision 3: a host's keeping is its runner's report
    where it gives one, else what the teams file keeps there (record 0064)."""

    def test_a_runner_reporting_it(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/tailrace": "/r/tailrace", "agentplot/timber": "/r/timber"},
                                                       ["agentplot/timber"])}) == (["deneb's runner keeps agentplot/tailrace"], [])

    def test_the_runners_report_wins_over_the_teams_file(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/timber": "/r/timber"}, ["agentplot/tailrace"])}) == ([], [])

    def test_a_runner_reporting_none_read_by_the_teams_file(self):
        """A runner that reports no repositories: deneb's runner branch holds no repositories.rec and a drive on deneb
        lists agentplot/tailrace."""
        assert plan.rename_kept("tailrace", {"deneb": (None, ["agentplot/tailrace", "afterthought/crew"])}) == (
            ["deneb's teams file keeps agentplot/tailrace"], [])

    def test_a_runner_reporting_none_on_a_host_the_teams_file_gives_no_keeping_for_is_unread(self):
        """What crew can't read: a runner's host that reports no repositories, is not the host the rename runs on, and
        runs no drive of the teams file."""
        assert plan.rename_kept("tailrace", {"vega": (None, None)}) == (
            [], ["vega's runner reports no repositories, and vega is neither the host the teams file is written on nor one a "
                 "drive runs on, so crew can't read whether it keeps tailrace"])

    def test_an_unreadable_runner_is_unread(self):
        why = "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: repositories.rec holds agentplot/timber twice"
        assert plan.rename_kept("tailrace", {"deneb": (why, ["agentplot/tailrace"])}) == ([], [why])

    def test_the_main_level_host_with_no_runner_branch_by_the_teams_file(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/timber": "/r/timber"}, []), "mac-studio": (None, ["tailrace"])}) == (
            ["mac-studio's teams file keeps tailrace"], [])

    def test_two_repositories_by_the_name_both_named(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/tailrace": "/a", "afterthought/tailrace": "/b"}, None)}) == (
            ["deneb's runner keeps afterthought/tailrace", "deneb's runner keeps agentplot/tailrace"], [])
        assert plan.rename_kept("agentplot/tailrace", {"deneb": ({"agentplot/tailrace": "/a", "afterthought/tailrace": "/b"}, None)}) == (
            ["deneb's runner keeps agentplot/tailrace"], [])

    def test_no_host_keeping_it(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/timber": "/r/timber"}, None),
                                             "mac-studio": (None, ["agentplot/tailrace-web"])}) == ([], [])


class TestRefused:
    """Decision 4: each refusal, in order, its message whole."""

    def refusal(self, old="tailrace", new="timber", bolts=("crew-bolt",), stands=(), unread=(), kept=(), unkept=(), count=None):
        return plan.rename_refusal("madswan", old, new, list(bolts), list(stands), list(unread), list(kept), list(unkept), count)

    def test_one_repository(self):
        assert self.refusal(new="agentplot/tailrace", stands=["bolt trc-1 has not landed"]) == \
            "tailrace and agentplot/tailrace name one repository: a rename gives it another name"

    def test_a_bolts_name(self):
        assert self.refusal(new="crew-bolt", stands=["bolt trc-1 has not landed"]) == (
            "crew-bolt is the name of bolt crew-bolt of madswan, so land/crew-bolt would name the bolt and not the repository: "
            "a repository and a bolt of one drive take different names")

    def test_work_standing_both_named_in_one_message(self):
        assert self.refusal(stands=["bolt trc-1 has not landed", "madswan-ops's card land/tailrace is open"],
                            kept=["deneb's runner keeps agentplot/tailrace"]) == (
            "crew can't rename tailrace while its work stands: bolt trc-1 has not landed; madswan-ops's card land/tailrace is open; "
            "its work lands or is dropped first")
        assert self.refusal(stands=["bolt trc-1 has not landed"], unread=["vega's runner can't be read: x"]) == (
            "crew can't rename tailrace while its work stands: bolt trc-1 has not landed; its work lands or is dropped first, "
            "and crew can't read whether more of it stands: vega's runner can't be read: x")

    def test_unread_work(self):
        assert self.refusal(unread=["vega's runner can't be read: x", "crew can't tell how far fix/main/tailrace/x (request 9) has got: y"]) == (
            "crew can't rename tailrace: it can't read whether its work stands: vega's runner can't be read: x; "
            "crew can't tell how far fix/main/tailrace/x (request 9) has got: y")

    def test_a_host_keeping_it(self):
        assert self.refusal(kept=["deneb's runner keeps agentplot/tailrace", "mac-studio's teams file keeps agentplot/tailrace"], count=0) == (
            "crew can't rename tailrace while a host keeps it: deneb's runner keeps agentplot/tailrace; mac-studio's teams file keeps "
            "agentplot/tailrace; tailrace is removed from the runner, Flume and sluice before crew renames its records")
        assert self.refusal(kept=["deneb's runner keeps agentplot/tailrace"], unkept=["vega: z"]) == (
            "crew can't rename tailrace while a host keeps it: deneb's runner keeps agentplot/tailrace, and crew can't read whether "
            "another keeps it: vega: z; tailrace is removed from the runner, Flume and sluice before crew renames its records")

    def test_unread_keeping(self):
        said = "vega's runner reports no repositories, and vega is neither the host the teams file is written on nor one a drive runs on"
        assert self.refusal(unkept=[said]) == (
            f"crew can't rename tailrace: it can't read whether a host keeps it: {said}; tailrace is removed from the runner, "
            "Flume and sluice before crew renames its records")

    def test_no_record_naming_it(self):
        assert self.refusal(old="rocs-kit", new="rocs", count=0) == (
            "no record of madswan's names rocs-kit: neither its plan's sources, its requests nor its run record")

    def test_none_when_all_is_clear(self):
        assert self.refusal() is None and self.refusal(count=3) is None


def fleet(*repos):
    """madswan's fleet, its main level on deneb, its folder keeping repos (owner/name) there, as the teams file gives
    them (record 0064)."""
    return {"drives": {"madswan": dict({"label": "madswan", "machine": "deneb", "runs": STANDING}, **keeping("/d/agentplot", *repos))},
            "hosts": {"deneb": {"ssh": "deneb", "kind": "darwin"}}}


@pytest.fixture(autouse=True)
def on_deneb(monkeypatch):
    """crew runs on deneb, madswan's main-level host, so the teams file it reads is deneb's."""
    import crew
    monkeypatch.setattr(crew, "this_host", lambda: "deneb")


# deneb's keeping once flywheel-cloud is removed and before boomdrive-cloud is added back (record 0060's order).
REMOVED = fleet("agentplot/timber", "afterthought/crew")


def command(w, do="kit rename flywheel-cloud boomdrive-cloud", f=REMOVED, n=None):
    """crew kit rename as plan.OPS builds it, run directly (n None) or inside proposal n, on the write's facts."""
    return plan.OPS[("kit", "rename")](known(w, fleet=f, n=n), plan.do_args("madswan", do))


class TestTheCommand:
    """Decisions 2 to 5: crew kit rename pushes its host's kept entries, refuses on the tip's facts, and renames every
    record in one write with Repo and Count on its entry."""

    @pytest.fixture(autouse=True)
    def reach(self, monkeypatch):
        self.reached = []
        monkeypatch.setattr(plan.record, "reach", lambda label, eid=None: self.reached.append(label) or 0)

    def test_a_direct_run_over_finished_work_renames_and_fills_repo_and_count(self, capsys):
        w = madswan_branch()
        op = command(w)
        op.change(w)
        plan.check(w.plan)
        assert (op.act, op.subject, op.on, op.frm, op.fields) == (
            "kit.rename", "plan(kit): rename flywheel-cloud boomdrive-cloud", ["kit/boomdrive-cloud"], ["kit/flywheel-cloud"],
            {"Repo": "boomdrive-cloud", "Count": "6"})
        assert plan.Plan(w.files["requests.rec"]).recs("Request")[0].get("Repo") == "boomdrive-cloud"
        assert w.renaming == [("flywheel-cloud", "boomdrive-cloud")]
        op.after("afterthought/crew-state", "0" * 40)
        assert capsys.readouterr().out == "flywheel-cloud is boomdrive-cloud in madswan's records: 6 records renamed\n"

    def test_a_started_bolt_refuses_naming_it_with_the_write_as_it_was(self):
        w = madswan_branch(bolts=[("you-sign-in-to-staging", "flywheel-cloud", True)])
        text, files = w.plan.text(), dict(w.files)
        with pytest.raises(plan.Refusal, match="^crew can't rename flywheel-cloud while its work stands: bolt you-sign-in-to-staging "
                                               "has not landed; its work lands or is dropped first$"):
            command(w).change(w)
        assert (w.plan.text(), w.files, w.renaming) == (text, files, [])

    def test_a_host_keeping_the_old_name_refuses(self):
        w = madswan_branch()
        with pytest.raises(plan.Refusal, match="^crew can't rename flywheel-cloud while a host keeps it: deneb's teams file keeps "
                                               "agentplot/flywheel-cloud; flywheel-cloud is removed from the runner"):
            command(w, f=fleet("agentplot/flywheel-cloud")).change(w)

    def test_prepare_pushes_this_hosts_kept_entries_before_the_change(self):
        w = madswan_branch()
        op = command(w)
        assert op.prepare() is None and self.reached == ["madswan"]

    def test_an_approvals_own_proposal_names_nothing_against_it(self):
        w = madswan_branch()
        w.files["proposals.rec"] = plan.PROPOSALS + "\n" + "\n".join(proposal(7, "kit rename flywheel-cloud boomdrive-cloud").lines()) + "\n"
        op = command(w, n=7)
        op.change(w)
        assert op.fields == {"Repo": "boomdrive-cloud", "Count": "6"}
        w = madswan_branch()
        w.files["proposals.rec"] = plan.PROPOSALS + "\n" + "\n".join(proposal(7, "kit rename flywheel-cloud boomdrive-cloud").lines()) + "\n"
        with pytest.raises(plan.Refusal, match="proposal 7 is open and names flywheel-cloud"):
            command(w).change(w)


class TestRunAgain:
    """Decisions 1 and 5: run again, the rename renames what an earlier one left, and leaves every kit.rename entry whole."""

    @pytest.fixture(autouse=True)
    def reach(self, monkeypatch):
        monkeypatch.setattr(plan.record, "reach", lambda label, eid=None: 0)

    def test_what_an_earlier_rename_left_is_renamed_and_its_entry_kept(self):
        earlier = entry(9, "kit.rename", on=["kit/boomdrive-cloud"], frm=["kit/flywheel-cloud"], Repo="boomdrive-cloud", Count="2")
        day = runs(entry(1, "bolt.land", on=["bolt/you-sign-in-to-staging", "unit/one-seam"], Repo="flywheel-cloud"),
                   entry(2, "bolt.land", on=["bolt/second"], Repo="agentplot/flywheel-cloud"), earlier)
        text = plan_text(bolts=[("third", "boomdrive-cloud", False)], units=[("x", "boomdrive-cloud", "third", [])])
        w = FactsWrite(text, label="madswan", files={"requests.rec": requests(unit_launch(3, "one-seam", "flywheel-cloud", "staging")),
                                                     "runs/deneb/2026-10-30.rec": day})
        op = command(w)
        op.change(w)
        assert op.fields == {"Repo": "boomdrive-cloud", "Count": "3"} and w.plan.text() == plan.Plan(text).text()
        assert plan.Plan(w.files["requests.rec"]).recs("Request")[0].get("Repo") == "boomdrive-cloud"
        assert w.files["runs/deneb/2026-10-30.rec"] == runs(
            entry(1, "bolt.land", on=["bolt/you-sign-in-to-staging", "unit/one-seam"], Repo="boomdrive-cloud"),
            entry(2, "bolt.land", on=["bolt/second"], Repo="agentplot/boomdrive-cloud"), earlier)

    def test_a_later_rename_leaves_the_earlier_entry_whole(self):
        earlier = entry(9, "kit.rename", on=["kit/timber"], frm=["kit/tailrace"], Repo="timber", Count="8")
        day = runs(entry(1, "bolt.land", on=["bolt/trc-1"], Repo="timber"), earlier)
        w = FactsWrite(plan_text(), label="madswan", files={"runs/deneb/2026-10-30.rec": day})
        op = command(w, "kit rename timber trc", f=fleet("agentplot/trc"))
        op.change(w)
        assert op.fields == {"Repo": "trc", "Count": "1"}
        assert w.files["runs/deneb/2026-10-30.rec"] == runs(entry(1, "bolt.land", on=["bolt/trc-1"], Repo="trc"), earlier)


class TestADriveIsNeverRenamed:
    """Decision 8 (drive-state "A drive is never renamed"): a label changed in the teams file is one drive removed
    and another added, and crew kit rename renames a repository within one drive alone."""

    AFTERTHOUGHT = {"drives": {"afterthought": {"label": "afterthought", "machine": "deneb", "state": "afterthought/crew-state",
                                                    "runs": STANDING}}, "hosts": {}}

    def test_a_former_label_is_no_drive_and_the_new_label_its_own_branch(self):
        with pytest.raises(plan.Refusal, match="^no drive 'swancloud'. drives: afterthought$"):
            plan.crew.drive_of(self.AFTERTHOUGHT, "swancloud")
        assert plan.state_of(self.AFTERTHOUGHT, "afterthought") == ("afterthought/crew-state", "afterthought/main")

    def test_kit_rename_renames_a_repository_within_its_drive_alone(self):
        a = plan.do_args("madswan", "kit rename tailrace timber --label madswan")
        assert {k: v for k, v in vars(a).items() if k not in ("do",)} == {
            "cmd": "kit", "sub": "rename", "old": "tailrace", "new": "timber", "label": "madswan"}
        with pytest.raises(plan.Refusal, match="names drive afterthought, and the proposal is madswan's"):
            plan.do_args("madswan", "kit rename tailrace timber --label afterthought")
        for argv in (["drive", "rename", "swancloud", "afterthought"], ["label", "rename", "swancloud", "afterthought"]):
            with pytest.raises(plan.Refusal):
                plan.parser(plan.Strict).parse_args(argv)
        assert not [k for k in plan.OPS if k[1] == "rename" and k != ("kit", "rename")]
