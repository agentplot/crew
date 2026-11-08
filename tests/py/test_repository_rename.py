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

from facts import FactsWrite, flume_fixture, plan_text

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


def madswan_branch():
    text = plan_text(bolts=[("crew-bolt", "crew", False)], units=[("crew-unit", "crew", "crew-bolt", [])])
    text = text.replace("Unit: crew-unit\n", "Unit: crew-unit\nSource: agentplot/flywheel-cloud:docs/adr/0017, the seam\n")
    text = text.replace("Goal: Goal of crew-bolt.", "Goal: crew reads flywheel-cloud's seam.")
    return FactsWrite(text, label="madswan", files={"requests.rec": SEAM_REQUESTS, "runs/deneb/2026-10-30.rec": DAY,
                                                     "runs/deneb/2026-10-31.rec": QUIET, "proposals.rec": PROPOSALS})


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
    """Decision 3: a host's keeping is its runner's report where it gives one, else its spaces in the hosts file."""

    def test_a_runner_reporting_it(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/tailrace": "/r/tailrace", "agentplot/timber": "/r/timber"},
                                                       ["agentplot/timber"])}) == (["deneb's runner keeps agentplot/tailrace"], [])

    def test_the_runners_report_wins_over_the_spaces(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/timber": "/r/timber"}, ["agentplot/tailrace"])}) == ([], [])

    def test_a_runner_reporting_none_read_by_its_hosts_spaces(self):
        assert plan.rename_kept("tailrace", {"deneb": (None, ["agentplot/tailrace", "afterthought/crew"])}) == (
            ["deneb's spaces keep agentplot/tailrace"], [])

    def test_a_runner_reporting_none_on_a_host_the_hosts_file_doesnt_list_is_unread(self):
        assert plan.rename_kept("tailrace", {"vega": (None, None)}) == (
            [], [f"vega's runner reports no repositories and {plan.crew.HOSTS} lists no vega, so crew can't read whether it keeps tailrace"])

    def test_an_unreadable_runner_is_unread(self):
        why = "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: repositories.rec holds agentplot/timber twice"
        assert plan.rename_kept("tailrace", {"deneb": (why, ["agentplot/tailrace"])}) == ([], [why])

    def test_the_main_level_host_with_no_runner_branch_by_its_spaces(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/timber": "/r/timber"}, []), "mac-studio": (None, ["tailrace"])}) == (
            ["mac-studio's spaces keep tailrace"], [])

    def test_two_repositories_by_the_name_both_named(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/tailrace": "/a", "afterthought/tailrace": "/b"}, None)}) == (
            ["deneb's runner keeps afterthought/tailrace", "deneb's runner keeps agentplot/tailrace"], [])
        assert plan.rename_kept("agentplot/tailrace", {"deneb": ({"agentplot/tailrace": "/a", "afterthought/tailrace": "/b"}, None)}) == (
            ["deneb's runner keeps agentplot/tailrace"], [])

    def test_no_host_keeping_it(self):
        assert plan.rename_kept("tailrace", {"deneb": ({"agentplot/timber": "/r/timber"}, None),
                                             "mac-studio": (None, ["agentplot/tailrace-web"])}) == ([], [])
