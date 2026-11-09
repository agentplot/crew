"""crew's side of the runner's interface (the change teams-cross-to-flume-as-their-bolts-land, Decision 4): the requests
crew appends to requests.rec on the drive's branch, numbered once and never changed or removed, each checked by
crew's own rules (runner.request_refusal, runner.append_refusal) as well as recfix, and written by a plan write's change
function (plan.request); each host's runner as crew reads it from its own branch (runner.host_read); and a crossed
piece's stage from its launch, the runner's answer and Flume's status of its place (runner.stage_of, Decision 8), on
flume 0.3.6's own status (tests/py/flume-0.3.6/). recfix's side, the commit and the fetch are the contract tier's
(tests/contract/test_recfix.py, tests/contract/test_git.py)."""
import json
import pathlib

import pytest

from crew import Refusal
from facts import FactsWrite, flume_plan, madswan_fleet, ran
import plan
import runner

AT, BY = "2026-10-31T12:00:00Z", "madswan-dispatch-deneb"
LAUNCH = dict(Repo="afterthought/crew", Kind="change", Base="bolt/b", Priority=2, Intent="madswan/b", Recipient="madswan/planner",
              Brief="Build it.")
# A bolt's own launch, its base place, as a start appends it first (crew-lands-each-bolt-through-flumes-base-place,
# Decision 3): crew's kind, cut from main, ops its recipient, and no Brief or After.
BOLT = dict(Repo="afterthought/crew", Kind="crew/bolt", Name="b", Base="main", Priority=2, Intent="madswan/b",
            Recipient="madswan/ops", Brief=None)


def rec(n, act, work="unit/a", **given):
    """A request as plan.request makes it, a launch carrying every field a launch needs unless given otherwise: a kit's
    work names no host or stream, a runner whose configuration names its repository taking it (the user's ruling of
    2026-11-01)."""
    if act == "launch":
        given = dict(dict(LAUNCH, Name=work.split("/")[-1]), **given)
    return plan.Rec("Request", runner.request_fields(n, act, work, given, AT, BY))


def held(*recs):
    """requests.rec holding these requests, as the plan's records."""
    return plan.Plan(runner.REQUESTS + "".join("\n" + "\n".join(r.lines()) + "\n" for r in recs)).recs("Request")


class TestRequests:
    """A request is numbered once, carries what its act needs and names what it acts on (Decision 4)."""

    def test_a_requests_fields_are_written_in_the_files_order_and_a_flag_as_yes(self):
        r = rec(3, "retry", Words="Read the plan again.", Submission=True, Of=1, Stage=None)
        assert r.fields == [("Request", "3"), ("Act", "retry"), ("Work", "unit/a"), ("Of", "1"),
                            ("Submission", "yes"), ("Words", "Read the plan again."), ("Date", AT), ("By", BY)]
        assert rec(2, "launch", "unit/b", After=[1, "4"]).all("After") == ["1", "4"]

    def test_never_renumbered(self):
        """requests.rec holds requests 1 to 7 and a drop is written: it is request 8."""
        seven = held(rec(1, "launch"), *[rec(n, "priority", Of=1, Priority=n) for n in range(2, 8)])
        assert runner.next_request(seven) == 8
        assert runner.request_refusal(seven, rec(8, "drop", Of=1)) is None
        assert runner.request_refusal(seven, rec(7, "drop", Of=1)) == (
            "request 7 is not the next in requests.rec: it holds requests 1 to 7, so the next is 8")
        assert runner.request_refusal([], rec(2, "launch")) == "request 2 is not the next in requests.rec: it holds none, so the next is 1"

    def test_a_launch_with_no_brief_is_refused(self):
        why = runner.request_refusal([], rec(1, "launch", Brief=None))
        assert why.startswith("launch 1 for unit/a names no Brief: a launch carries Request, Act, Work, Date, By, Repo, Kind, "
                              "Name, Base, Priority")

    def test_a_kits_launch_names_no_host_or_stream_and_a_roles_names_both(self):
        """A runner whose configuration names a kit's repository takes its work in the stream its host maps it to, and crew
        names neither (settled with the user 2026-11-01); a role's work runs on its main level's host in its stream."""
        kit = ("launch 1 of unit/a names a Host or a Stream: a kit's work is taken by a runner whose configuration names its "
               "repository, in the stream its host's Flume configuration maps the repository to, and crew names neither")
        assert runner.request_refusal([], rec(1, "launch", Host="deneb")) == kit
        assert runner.request_refusal([], rec(1, "launch", Stream="madswan")) == kit
        role = dict(Repo="afterthought/blueprints", Kind="chore", Base="main", Intent="madswan-design", Recipient="madswan/design")
        assert runner.request_refusal([], rec(1, "launch", "role/design/r", Host="deneb", Stream="madswan", **role)) is None
        assert runner.request_refusal([], rec(1, "launch", "role/design/r", **role)) == (
            "launch 1 of role/design/r names no Host or no Stream: a role's work runs on the host and in the stream its role runs in")

    def test_a_retry_of_nothing_is_refused_naming_the_request(self):
        """A retry would name request 9, which is no launch."""
        have = held(rec(1, "launch"))
        assert runner.request_refusal(have, rec(2, "retry", Of=9)) == (
            "retry 2 for unit/a names request 9, which is no launch: requests.rec does not hold it")
        have = held(rec(1, "launch"), rec(2, "drop", Of=1))
        assert runner.request_refusal(have, rec(3, "retry", Of=2)) == "retry 3 for unit/a names request 2, which is no launch"

    def test_a_retry_drop_or_priority_names_a_launch_of_its_own_work_and_no_host(self):
        """It is taken by the runner that took the launch it names, so it names no host of its own."""
        have = held(rec(1, "launch"))
        assert runner.request_refusal(have, rec(2, "drop", "unit/b", Of=1)) == "drop 2 for unit/b names launch 1, which is unit/a's"
        assert runner.request_refusal(have, rec(2, "priority", Of=1, Priority=3, Host="alpha")) == (
            "priority 2 for unit/a carries Host, which a priority does not take")
        assert runner.request_refusal(have, rec(2, "priority", Of=1)).startswith("priority 2 for unit/a names no Priority")

    def test_a_request_carries_nothing_its_act_does_not_take(self):
        have = held(rec(1, "launch"))
        assert runner.request_refusal(have, rec(2, "drop", Of=1, Words="Gone.", Stream="madswan")) == (
            "drop 2 for unit/a carries Stream, Words, which a drop does not take")
        assert runner.request_refusal([], rec(1, "reorder")) == (
            "request 1 is a reorder, and a request is a launch, a retry, a drop, a priority or a land")

    def test_the_work_is_named_as_crew_names_it(self):
        for work in ("bolt/b", "unit/a", "chore/bump", "fix/b/tidy", "fix/main/crew/red", "role/design/record-0053"):
            assert runner.WORK.match(work)
        assert runner.request_refusal([], rec(1, "launch", "unit/A")) == (
            "launch 1 serves unit/A, and a request serves bolt/<bolt>, unit/<unit>, chore/<chore>, fix/<bolt>/<name>, "
            "fix/main/<kit>/<name> or role/<role>/<name>")
        assert runner.request_refusal([], rec(1, "launch", "role/design")).startswith("launch 1 serves role/design")
        assert runner.request_refusal([], rec(1, "launch", "bolt/B", **BOLT)).startswith("launch 1 serves bolt/B")

    def test_an_after_names_launches_of_the_same_bolt_written_before_it(self):
        have = held(rec(1, "launch"), rec(2, "launch", "unit/c", Base="bolt/other"), rec(3, "priority", Of=1, Priority=1))
        assert runner.request_refusal(have, rec(4, "launch", "unit/b", After=[1])) is None
        assert runner.request_refusal(have, rec(4, "launch", "unit/b", After=[2])) == (
            "launch 4 of unit/b on bolt/b comes after launch 2, which is on bolt/other: an After names work of the same bolt")
        assert runner.request_refusal(have, rec(4, "launch", "unit/b", After=[3])) == "launch 4 of unit/b comes after request 3, which is no launch"
        assert runner.request_refusal(have, rec(4, "launch", "unit/b", After=[5])) == "launch 4 of unit/b comes after request 5, which is no launch"

    def test_a_fix_of_main_holds_its_submission(self):
        fix = dict(Base="main", Intent="madswan/main/crew", Recipient="madswan/ops", Name="main--red")
        assert runner.request_refusal([], rec(1, "launch", "fix/main/crew/red", Hold="submission", **fix)) is None
        assert runner.request_refusal([], rec(1, "launch", "fix/main/crew/red", **fix)) == (
            "launch 1 of fix/main/crew/red is a fix of main, which is launched with its submission held (Hold: submission) until the "
            "user's send (state.3)")

    def test_a_retry_starts_a_stage_or_submits_again(self):
        have = held(rec(1, "launch"))
        assert runner.request_refusal(have, rec(2, "retry", Of=1, Stage="code", Words="Yes.")) is None
        assert runner.request_refusal(have, rec(2, "retry", Of=1, Submission=True)) is None
        assert runner.request_refusal(have, rec(2, "retry", Of=1, Stage="code", Submission=True)) == (
            "retry 2 of unit/a names stage code and the submission: a retry starts a stage again or submits again")


class TestBoltRequests:
    """A bolt's own launch, its pieces' and its land are checked before they are appended (bolt-teams "A bolt's launch,
    its pieces' and its land are checked before they are appended"; drive-state "A launch names everything the runner
    passes to Flume"; crew-lands-each-bolt-through-flumes-base-place, Decisions 3, 4 and 9)."""

    def bolt(self, n=1, **given):
        return rec(n, "launch", "bolt/b", **dict(BOLT, **given))

    def test_a_bolts_own_launch_is_crews_kind_on_main_with_no_brief_or_after(self):
        assert runner.request_refusal([], self.bolt()) is None
        assert self.bolt().get("Brief") is None and self.bolt().get("Kind") == "crew/bolt"

    def test_a_bolts_launch_naming_another_kind_base_a_brief_or_an_after_is_refused_naming_the_field(self):
        assert runner.request_refusal([], self.bolt(Kind="change")) == (
            "launch 1 of bolt/b names Kind change: a bolt's base place is of crew's kind crew/bolt")
        assert runner.request_refusal([], self.bolt(Base="bolt/b")) == (
            "launch 1 of bolt/b names Base bolt/b: a bolt's base place is cut from main")
        assert runner.request_refusal([], self.bolt(Brief="Land it.")) == (
            "launch 1 of bolt/b names a Brief: a bolt's base place runs no agent, so it carries none")
        have = held(rec(1, "launch", "bolt/other", **dict(BOLT, Name="other")))
        assert runner.request_refusal(have, self.bolt(2, After=[1])) == (
            "launch 2 of bolt/b names After 1: a bolt's base place lands after every place on its branch, so it comes after no launch")

    def test_no_other_launch_names_crews_kind(self):
        have = held(self.bolt())
        assert runner.request_refusal(have, rec(2, "launch", Kind="crew/bolt")) == (
            "launch 2 of unit/a names Kind crew/bolt, which is a bolt's base place's alone, of bolt/<bolt>")

    def test_a_kind_recfix_does_not_hold_is_named_by_recfix_not_here(self):
        """Kind is a regexp in the descriptor, since recutils' enum takes no slash, delimited by #, since recutils ends a
        regexp at its delimiter's next occurrence, escaped or not (Decision 3; tests/contract/test_recfix.py)."""
        assert "%type: Kind regexp #^(change|chore|fix|crew/bolt)$#" in runner.REQUESTS
        assert "%type: Act enum launch retry drop priority land" in runner.REQUESTS

    def test_its_pieces_follow_it_naming_no_after_on_it(self):
        have = held(self.bolt())
        assert runner.request_refusal(have, rec(2, "launch")) is None
        assert runner.request_refusal(held(self.bolt(), rec(2, "launch")), rec(3, "launch", "unit/b", After=[2])) is None

    def test_a_fix_on_a_bolt_started_before_bolts_were_base_places_is_appended(self):
        """Its units' launches stand on bolt/b and no launch of bolt/b does (Decision 9): a fix, a take-main fix among
        them, is still launched on its branch."""
        have = held(rec(1, "launch"), rec(2, "launch", "chore/c"))
        fix = rec(3, "launch", "fix/b/take-main-9f1c2ab", Kind="fix", Name="b--take-main-9f1c2ab")
        assert runner.request_refusal(have, fix) is None

    def test_a_land_names_a_bolts_or_a_fix_of_mains_launch_and_nothing_else(self):
        fix = dict(Base="main", Intent="madswan/main/crew", Recipient="madswan/ops", Name="main--red", Hold="submission", Kind="fix")
        have = held(self.bolt(), rec(2, "launch"), rec(3, "launch", "fix/main/crew/red", **fix))
        assert runner.request_refusal(have, rec(4, "land", "bolt/b", Of=1)) is None
        assert runner.request_refusal(have, rec(4, "land", "fix/main/crew/red", Of=3)) is None
        assert runner.request_refusal(have, rec(4, "land", "bolt/b", Of=1)) is None
        assert runner.request_refusal(have, rec(4, "land", "bolt/b")) == "land 4 for bolt/b names no Of: a land carries Request, Act, Work, Date, By, Of"
        assert runner.request_refusal(have, rec(4, "land", "bolt/b", Of=1, Words="Land it.")) == (
            "land 4 for bolt/b carries Words, which a land does not take")

    def test_a_land_of_a_units_launch_is_refused_naming_the_launch(self):
        have = held(self.bolt(), rec(2, "launch"))
        assert runner.request_refusal(have, rec(3, "land", "unit/a", Of=2)) == (
            "land 3 for unit/a names launch 2, which is no bolt's or fix of main's: a land is the user's send of a bolt or of a fix of main")
        assert runner.request_refusal(have, rec(3, "land", "bolt/b", Of=2)) == "land 3 for bolt/b names launch 2, which is unit/a's"
        assert runner.request_refusal(have, rec(3, "land", "bolt/b", Of=9)) == (
            "land 3 for bolt/b names request 9, which is no launch: requests.rec does not hold it")


class TestAppended:
    """A request is never changed or removed: a write only appends (Decision 4)."""

    def test_a_write_that_appends_passes_and_one_that_changes_or_removes_a_request_is_refused(self):
        one, two = rec(1, "launch"), rec(2, "drop", Of=1)
        assert runner.append_refusal([one.fields], [one.fields, two.fields]) is None
        changed = rec(1, "launch", Brief="Build it otherwise.")
        assert runner.append_refusal([one.fields, two.fields], [changed.fields, two.fields]).startswith(
            "request 1 would be changed in requests.rec, and a request is never changed or removed")
        assert runner.append_refusal([one.fields, two.fields], [one.fields]).startswith("request 2 would be removed from requests.rec")
        assert runner.append_refusal([one.fields, two.fields], [two.fields, one.fields]).startswith("request 1 would be changed")


class TestPlanRequest:
    """plan.request appends a request from inside a write's change function, so it reaches the branch in the write's own
    commit (state.1): numbered the next, by the writer, refused whole by crew's rules."""

    def test_two_requests_of_one_write_are_numbered_in_turn_after_those_the_branch_holds(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", BY)
        w = FactsWrite("%rec: Bolt\n%key: Bolt\n")
        assert plan.request(w, "launch", "bolt/b", **BOLT) == 1
        assert plan.request(w, "launch", "unit/a", Name="a", **LAUNCH) == 2
        assert plan.request(w, "launch", "unit/b", Name="b", After=[2], **LAUNCH) == 3
        rs = plan.Plan(w.files["requests.rec"]).recs("Request")
        assert [(r.get("Request"), r.get("Work"), r.all("After"), r.get("By")) for r in rs] == [
            ("1", "bolt/b", [], BY), ("2", "unit/a", [], BY), ("3", "unit/b", ["2"], BY)]
        assert w.files["requests.rec"].startswith(runner.REQUESTS)
        w2 = FactsWrite("%rec: Bolt\n%key: Bolt\n", files={"requests.rec": w.files["requests.rec"]})
        assert plan.request(w2, "drop", "unit/b", Of=3) == 4

    def test_a_refused_request_leaves_the_writes_files_as_they_were(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", BY)
        w = FactsWrite("%rec: Bolt\n%key: Bolt\n")
        plan.request(w, "launch", "bolt/b", **BOLT)
        plan.request(w, "launch", "unit/a", Name="a", **LAUNCH)
        text = w.files["requests.rec"]
        with pytest.raises(Refusal, match="^retry 3 for unit/a names request 9, which is no launch"):
            plan.request(w, "retry", "unit/a", Of=9, Words="Go on.")
        assert w.files["requests.rec"] == text

    def test_a_branch_whose_file_was_made_before_a_field_was_allowed_takes_crews_descriptor(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", BY)
        old = runner.REQUESTS.replace(" Hold After Brief", " After Brief") + "\n" + "\n".join(rec(1, "launch").lines()) + "\n"
        w = FactsWrite("%rec: Bolt\n%key: Bolt\n", files={"requests.rec": old})
        plan.request(w, "drop", "unit/a", Of=1)
        assert w.files["requests.rec"].startswith(runner.REQUESTS)


TIP = "5e1f0c2a" + "0" * 32
STATUS = {"status": {"places": [{"place": "/crew/places/change--a", "phase": "live"}], "host": {}}}


def branch(host="deneb", runner_rec=None, answers="", places="", repositories=None):
    """A runner's branch's files parsed as plan.runners parses them, each given as the records after its descriptor;
    repositories.rec only where repositories are given, a branch without it reporting none."""
    run = runner.RUNNER + (f"\nHost: {host}\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n" if runner_rec is None else runner_rec)
    return dict({"runner.rec": plan.Plan(run), "answers.rec": plan.Plan(runner.ANSWERS + answers), "places.rec": plan.Plan(runner.PLACES + places)},
                **({"repositories.rec": plan.Plan(runner.REPOSITORIES + repositories)} if repositories is not None else {}))


def kept(*repos):
    """repositories.rec's records after its descriptor, each repository (address, folder) its runner keeps."""
    return "".join(f"\nRepository: {a}\nFolder: {f}\n" for a, f in repos)


def answer(n, outcome, place=None, words=None):
    return f"\nRequest: {n}\nOutcome: {outcome}\n" + (f"Place: {place}\n" if place else "") + (f"Words: {words}\n" if words else "") + "At: 2026-10-31T12:01:00Z\n"


def placed(n, status, place="/crew/places/change--a"):
    return f"\nRequest: {n}\nPlace: {place}\nAt: 2026-10-31T12:02:00Z\nStatus: {status if isinstance(status, str) else json.dumps(status)}\n"


class TestHostRead:
    """A host's runner is read from <label>/runner/<host> at its tip; one that can't be read hides that host's work
    alone, named (read.1, read.3)."""

    def test_a_runners_answers_and_places_are_read_by_their_requests_numbers(self):
        r = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", "/crew/places/change--a") + answer(4, "held"),
                                                            places=placed(3, STATUS)), {})
        assert (r["host"], r["branch"], r["tip"], r["why"]) == ("deneb", "madswan/runner/deneb", TIP, None)
        assert r["runner"].get("Version") == "0.1.0"
        assert {n: a.get("Outcome") for n, a in r["answers"].items()} == {3: "launched", 4: "held"}
        assert r["places"] == {3: {"place": "/crew/places/change--a", "at": "2026-10-31T12:02:00Z", "status": STATUS, "why": None}}

    def test_a_runner_that_has_answered_nothing_reads_no_answers_and_no_places(self):
        files = dict(branch(), **{"answers.rec": None, "places.rec": None})
        r = runner.host_read("madswan", "deneb", TIP, files, {})
        assert (r["why"], r["answers"], r["places"]) == (None, {}, {})

    def test_the_repositories_a_runner_keeps_are_read_by_their_forge_addresses(self):
        """drive-state "The repositories a runner keeps" (roles.9: where a kit lives on a host is its runner's report):
        madswan/runner/deneb's repositories.rec names agentplot/boomdrive-cloud at /r/boomdrive-cloud; a branch with no
        repositories.rec reports none, and one whose file holds no record reports that it keeps none."""
        r = runner.host_read("madswan", "deneb", TIP, branch(repositories=kept(("agentplot/boomdrive-cloud", "/r/boomdrive-cloud"),
                                                                              ("afterthought/crew", "/r/crew"))), {})
        assert (r["why"], r["repositories"]) == (None, {"agentplot/boomdrive-cloud": "/r/boomdrive-cloud", "afterthought/crew": "/r/crew"})
        assert runner.host_read("madswan", "deneb", TIP, branch(), {})["repositories"] is None
        assert runner.host_read("madswan", "deneb", TIP, branch(repositories=""), {})["repositories"] == {}

    def test_a_repositories_file_recfix_refused_hides_the_host_naming_the_file(self):
        r = runner.host_read("madswan", "deneb", TIP, dict(branch(), **{"repositories.rec": None}),
                             {"repositories.rec": "repositories.rec fails recfix --check: repositories.rec: 7: error: duplicated key value in field 'Repository'"})
        assert r["why"] == ("deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: repositories.rec fails recfix --check: "
                            "repositories.rec: 7: error: duplicated key value in field 'Repository'")
        assert "repositories" not in r

    def test_a_host_with_no_branch_is_named(self):
        assert runner.of_host({}, "madswan", "alpha") == {
            "host": "alpha", "branch": "madswan/runner/alpha", "tip": None, "why": "no runner answers on alpha: madswan/runner/alpha does not exist"}

    def test_a_file_recfix_refused_hides_the_host_naming_the_file(self):
        r = runner.host_read("madswan", "deneb", TIP, dict(branch(), **{"places.rec": None}),
                             {"places.rec": "places.rec fails recfix --check: places.rec: 4: error: invalid integer"})
        assert r["why"] == "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: places.rec fails recfix --check: places.rec: 4: error: invalid integer"
        assert "answers" not in r

    @pytest.mark.parametrize("files, why", [
        (dict(branch(), **{"runner.rec": None}), "it holds no runner.rec"),
        (branch(runner_rec="\nHost: alpha\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n"), "runner.rec names host alpha"),
        (branch(runner_rec=""), "runner.rec holds 0 Runner records, and names one"),
        (dict(branch(), **{"answers.rec": plan.Plan("Request: 3\nOutcome: launched\n")}), "answers.rec holds a record before its %rec: Answer"),
        (branch(answers=answer(3, "held") + answer(3, "launched")), "answers.rec holds request 3 twice"),
        (branch(places=placed("x", STATUS)), "places.rec holds a record with no request's number"),
        (branch(repositories=kept(("agentplot/boomdrive-cloud", "/r/a"), ("agentplot/boomdrive-cloud", "/r/b"))),
         "repositories.rec holds agentplot/boomdrive-cloud twice"),
        (branch(repositories="\nFolder: /r/a\n"), "repositories.rec holds a record with no repository's address"),
        (branch(repositories="\nRepository: agentplot/timber\n"), "repositories.rec holds agentplot/timber with no folder"),
        (dict(branch(), **{"repositories.rec": plan.Plan("Repository: agentplot/timber\nFolder: /r/timber\n")}),
         "repositories.rec holds a record before its %rec: Repository")])
    def test_a_branch_crew_cant_read_names_what(self, files, why):
        assert runner.host_read("madswan", "deneb", TIP, files, {})["why"] == f"deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: {why}"

    def test_a_status_that_is_no_json_marks_its_place_alone(self):
        r = runner.host_read("madswan", "deneb", TIP, branch(places=placed(3, "{not json") + placed(4, STATUS, "/crew/places/chore-b")), {})
        assert r["why"] is None and r["places"][4]["status"] == STATUS
        assert r["places"][3]["status"] is None
        assert r["places"][3]["why"].startswith("madswan/runner/deneb at 5e1f0c2: places.rec's status of the place of request 3 is no JSON (")


FLUME = pathlib.Path(__file__).parent / "flume-0.3.6"
FLUME_17 = pathlib.Path(__file__).parent / "flume-0.17.0"
CODE ="/Users/chuck/Code/github_afterthought/crew/places/change--teams-cross-to-flume-as-their-bolts-land"
WORDS = ("check-full failed on bolt/crew-runs-its-work-through-flume with change/teams-cross-to-flume-as-their-bolts-land "
         "merged: tests:logic (1 failed: tests/py/test_runner.py::TestStageOf::test_a_crossed_piece_reads_its_stage)")


def fixture(name):
    return (FLUME / f"{name}.json").read_text()


def path_of(name):
    """The place's location in a fixture, the runner's Place, without a tidied place's @<when>."""
    return json.loads(fixture(name))["status"]["places"][0]["place"].split("@")[0]


def stage(name=None, outcome="launched", base="bolt/crew-runs-its-work-through-flume", work="unit/teams-cross-to-flume-as-their-bolts-land"):
    """A piece's stage as stage_of reads it, its launch request 3 on deneb answered as given and its place's status
    the fixture named, carried on one line in places.rec and read back by host_read."""
    where = path_of(name) if name else None
    r = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, outcome, where) if outcome else "",
                                                        places=placed(3, json.dumps(json.loads(fixture(name))), where) if name else ""), {})
    launch = held(rec(1, "launch", "unit/x"), rec(2, "launch", "chore/y"), rec(3, "launch", work, Base=base, After=[1, 2]))[2]
    return runner.stage_of(work, launch, r["answers"].get(3), r["places"].get(3), r["why"] or True, ["unit/x", "chore/y"])


class TestStageOf:
    """A crossed piece reads its stage from its launch, the runner's answer and Flume's status of its place, in Decision
    8's order, every field of Flume's guarded (read.2)."""

    def test_a_host_unread_or_a_piece_with_no_launch_is_unknown_naming_why(self):
        assert runner.stage_of("unit/a", None, None, None, "no runner answers on alpha: madswan/runner/alpha does not exist") == {
            "stage": "unknown", "why": "no runner answers on alpha: madswan/runner/alpha does not exist"}
        assert runner.stage_of("unit/a", None, None, None, True) == {"stage": "unknown", "why": "unit/a has no launch in requests.rec"}

    def test_unanswered_it_is_launching_and_answered_but_not_yet_placed_too(self):
        assert stage(None, outcome=None) == {"stage": "launching"}
        r = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", "/crew/places/change--a")), {})
        assert runner.stage_of("unit/a", rec(3, "launch"), r["answers"][3], None, True) == {"stage": "launching", "place": "/crew/places/change--a"}

    def test_held_for_its_after_work_it_is_waiting_on_that_work(self):
        assert stage(None, outcome="held") == {"stage": "waiting", "after": ["unit/x", "chore/y"]}

    def test_a_launch_with_no_after_the_runner_holds_is_launching_with_its_words_and_never_held_for_after_work(self):
        """bolt-plan "A claimed launch is not held for After work": deneb's runner answers launch 88 of
        every-fleet-mac-joins-the-tailnet-as-a-host, whose launch names no After, held with its claim's words, as Boomdrive
        claims every launch it takes (crew-control-plane, Decision 18) and holds one its stream has no room for; it reads
        launching with the runner's words, which its line says, and a held answer without words reads launching too."""
        claim = "claimed by deneb's runner; launching once no other runner has claimed it"
        r = runner.host_read("afterthought", "deneb", TIP, branch(answers=answer(88, "held", words=claim)), {})
        launch = held(rec(88, "launch", "unit/every-fleet-mac-joins-the-tailnet-as-a-host", Base="bolt/a-fleet-hosts-tailnet-key-never-expires"))[0]
        got = runner.stage_of("unit/every-fleet-mac-joins-the-tailnet-as-a-host", launch, r["answers"][88], None, True)
        assert got == {"stage": "launching", "words": claim}
        assert runner.piece_said(got) == ("launching", f"held by the runner: {claim}")
        bare = runner.host_read("afterthought", "deneb", TIP, branch(answers=answer(88, "held")), {})
        assert runner.stage_of("unit/a", launch, bare["answers"][88], None, True) == {"stage": "launching"}
        assert runner.piece_said({"stage": "launching"}) == ("launching", "")

    def test_a_stop_short_whose_agent_flume_0_17_keeps_open_needs_its_answer(self):
        """bolt-plan "A stop-short whose agent is kept open", on flume 0.17.0's own status (tests/py/flume-0.17.0/): the
        place's code ended short needing an answer, its agent kept open for it (waiting_on why answer with open_until,
        the end stage/code/1/ended-short), not stalled; it reads needs at code with the agent's words, and crew answer
        retries code with the answer's words, which reaches the session kept open as a tell answering it does (flume 42,
        49, 198)."""
        status = json.loads((FLUME_17 / "kept-open.json").read_text())
        p = status["status"]["places"][0]
        r = runner.host_read("agentplot", "deneb", TIP, branch(answers=answer(323, "launched", p["place"]),
                                                               places=placed(323, status, p["place"])), {})
        launch = held(rec(323, "launch", "unit/the-flake-configures-each-tool-by-its-own-module",
                          Base="bolt/the-boomdrive-flake-configures-the-whole-host"))[0]
        got = runner.stage_of("unit/the-flake-configures-each-tool-by-its-own-module", launch, r["answers"][323], r["places"][323], True)
        assert (got["stage"], got["of"], got["found"], got["stalled"], got["place"], got["tasks"]) == ("needs", "code", False, False, p["place"], (0, 15))
        assert got["words"] == p["stages"][1]["end"]["words"] and got["words"].startswith(
            "The code stage of the-flake-configures-each-tool-by-its-own-module cannot start:")
        assert p["waiting_on"]["open_until"] and [e["key"] for e in p["ends"]][-1] == "stage/code/1/ended-short"
        assert runner.answer_retry("unit/the-flake-configures-each-tool-by-its-own-module", got) == ("stage", "code")

    def test_refused_by_the_runner_it_is_refused_with_its_words(self):
        r = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "refused", words="no repository afterthought/crew in this runner's configuration")), {})
        assert runner.stage_of("unit/a", rec(3, "launch"), r["answers"][3], None, True) == {
            "stage": "refused", "words": "no repository afterthought/crew in this runner's configuration"}

    def test_a_launch_answered_done_is_an_answer_crew_cant_read(self):
        r = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "done")), {})
        assert runner.stage_of("unit/a", rec(3, "launch"), r["answers"][3], None, True)["why"] == (
            "the runner answered launch 3 of unit/a done, and a launch is answered held, launched or refused")

    def test_a_stage_waiting_for_room_is_queued(self):
        assert stage("queued") == {"stage": "queued", "of": "construct", "place": path_of("queued"), "tasks": (0, 0)}

    def test_a_stage_begun_is_its_name_and_code_says_its_tasks(self):
        assert stage("construct") == {"stage": "construct", "place": path_of("construct"), "tasks": (0, 0)}
        assert stage("code") == {"stage": "code", "place": CODE, "tasks": (6, 26)}

    def test_stopped_short_asking_it_needs_an_answer_with_the_agents_words_and_says_it_stalled(self):
        got = stage("stopped-short")
        question = json.loads(fixture("stopped-short"))["status"]["places"][0]["stages"][1]["end"]["words"]
        assert (got["stage"], got["of"], got["words"], got["found"], got["stalled"]) == ("needs", "code", question, False, True)
        assert got["words"].startswith("Head 118ec46 is ready for your flume:live run (6.1).")

    def test_waiting_on_its_caller_it_waits_with_flumes_words(self):
        got = stage("on-hold")
        assert got == {"stage": "waits", "of": "code", "why": "on_hold", "words": "Wait for the user's approval of the proposal on its Pending You card.",
                       "held": False, "place": path_of("on-hold"), "tasks": (0, 28)}

    def test_left_waiting_past_flumes_bound_it_is_stalled(self):
        got = stage("stalled")
        assert (got["stage"], got["of"], got["why"], got["words"]) == ("stalled", "code", "lost", None)

    def test_sent_back_after_a_failed_submission_it_is_at_its_stage_with_sluices_words(self):
        assert stage("sent-back") == {"stage": "code", "words": WORDS, "sent_back": 1, "verdict": "failed", "place": CODE, "tasks": (26, 26)}

    def test_submitted_it_names_sluices_number(self):
        assert stage("submitted") == {"stage": "submitted", "submission": "413", "place": CODE, "tasks": (26, 26)}

    def test_landed_on_its_bolt_it_is_merged_and_on_main_landed_with_the_commit(self):
        assert stage("landed") == {"stage": "merged", "commit": "d185a879b51dba33555c036392b50443f4dfc5e8", "place": CODE}
        main = stage("landed", base="main", work="fix/main/crew/red")
        assert (main["stage"], main["commit"]) == ("landed", "d185a879b51dba33555c036392b50443f4dfc5e8")

    def test_dropped_it_is_dropped(self):
        assert stage("dropped") == {"stage": "dropped", "place": CODE}

    def test_a_status_with_no_entry_for_its_place_or_no_json_is_unknown(self):
        r = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", "/elsewhere"), places=placed(3, fixture("code").replace("\n", " "), "/elsewhere")), {})
        assert runner.stage_of("unit/a", rec(3, "launch"), r["answers"][3], r["places"][3], True) == {
            "stage": "unknown", "place": "/elsewhere", "why": "Flume's status of unit/a's place, as the runner carried it, holds no place /elsewhere"}
        r = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", "/p"), places=placed(3, "[", "/p")), {})
        got = runner.stage_of("unit/a", rec(3, "launch"), r["answers"][3], r["places"][3], True)
        assert got["stage"] == "unknown" and "places.rec's status of the place of request 3 is no JSON" in got["why"]

    @pytest.mark.parametrize("change", [
        lambda p: p.pop("phase"), lambda p: p.update(phase={"tidied": "soon"}), lambda p: p.update(stages="all"),
        lambda p: p.update(tasks=[{"text": "1.1", "ticked": "yes"}]), lambda p: p.update(submission=["x"]),
        lambda p: p.update(waiting_on="answer"), lambda p: p.update(current=3)])
    def test_a_field_of_another_shape_reads_none_and_never_becomes_text(self, change):
        status = json.loads(fixture("code"))
        change(status["status"]["places"][0])
        f = runner.flume_facts(status, CODE)
        assert f is not None and all(v is None or isinstance(v, (str, int, tuple, dict)) for v in f.values())
        got = runner.stage_of("unit/a", rec(3, "launch"), plan.Rec("Answer", [("Request", "3"), ("Outcome", "launched")]),
                              {"place": CODE, "status": status, "why": None}, True)
        assert got["stage"] in ("code", "unknown") and "None" not in (got.get("why") or "")

    def test_a_launch_is_read_from_the_runner_that_took_it(self):
        """madswan/runner/deneb holds an answer and a place for request 3, and madswan/runner/alpha can't be read: request
        3's work reads its stage from deneb's place, since crew names no host on a launch and the runner that took it is
        the one whose answers hold it; requests 1 and 2, which deneb has not taken, read unknown naming alpha's runner,
        which may have; with alpha read and holding neither they read launching; and a launch two runners took reads
        unknown naming both (the user's ruling of 2026-11-01; read.1)."""
        deneb = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", CODE),
                                                                 places=placed(3, json.loads(fixture("code")), CODE)), {})
        silent = runner.host_read("madswan", "alpha", TIP, {}, {"runner.rec": "recfix refused it"})
        requests = held(rec(1, "launch", "unit/b"), rec(2, "launch", "chore/c"), rec(3, "launch", "unit/teams-cross-to-flume-as-their-bolts-land"))

        def of(work, reads):
            return runner.piece_stage(requests, reads, runner.launch_of(requests, work))
        reads = {"deneb": deneb, "alpha": silent}
        assert of("unit/teams-cross-to-flume-as-their-bolts-land", reads)["stage"] == "code"
        why = "no runner crew read has taken request 1, and alpha's runner can't be read: madswan/runner/alpha at 5e1f0c2: recfix refused it"
        assert of("unit/b", reads) == {"stage": "unknown", "why": why}
        quiet = {"deneb": deneb, "alpha": runner.host_read("madswan", "alpha", TIP, branch("alpha"), {})}
        assert of("unit/b", quiet) == of("chore/c", quiet) == {"stage": "launching"}
        both = {"deneb": deneb, "alpha": runner.host_read("madswan", "alpha", TIP, branch("alpha", answers=answer(3, "launched", CODE)), {})}
        assert of("unit/teams-cross-to-flume-as-their-bolts-land", both) == {"stage": "unknown", "why": (
            "request 3 was taken by the runners on alpha and deneb, whose configurations each name its repository, so crew "
            "can't tell which place is its work")}
        assert of("unit/b", {})["why"].startswith("no runner answers for the partition")


class TestABasePlacesStatus:
    """What flume_facts reads of a bolt's base place, crew/bolt@1, as flume 0.17.0 shapes its status
    (tests/py/flume-0.17.0/bolt-*.json; crew-lands-each-bolt-through-flumes-base-place, Decision 6): no stage, its
    submission's entry and state, the verdict and its words, what it waits on its caller for, and its landed commit."""
    PLACE = "/Users/chuck/.local/share/flume/places/f3a444f5e38a/bolt--the-runner-lands-each-bolt"

    def facts(self, name):
        return runner.flume_facts(json.loads((FLUME_17 / f"{name}.json").read_text()), self.PLACE)

    def test_submitted_under_test_names_the_entry_and_waits_on_nobody(self):
        f = self.facts("bolt-submitted")
        assert (f["phase"], f["current"], f["entry"], f["entry_state"], f["verdict"], f["waiting"]) == (
            "live", None, "412", "under_test", None, None)

    def test_landed_names_its_commit(self):
        f = self.facts("bolt-landed")
        assert (f["phase"], f["over"], f["commit"], f["verdict"]) == ("over", "landed", "a7c3e9f1b2d4c6e8a0b1c3d5e7f9a1b3c5d7e9f0", "landed")

    def test_failed_carries_sluices_words_and_waits_on_its_caller(self):
        f = self.facts("bolt-failed")
        assert (f["verdict"], f["verdict_words"], f["waiting"], f["entry_state"]) == (
            "failed", "check-full failed: tests:logic 3 failed (tests/py/test_landing.py)", "submission", "failed")
        assert f["waiting_words"].startswith("the submission failed: check-full failed")

    def test_conflict_names_its_words_and_waits_on_its_caller(self):
        f = self.facts("bolt-conflict")
        assert (f["verdict"], f["waiting"], f["entry_state"]) == ("conflict", "submission", "conflict")
        assert "conflicts with main at 9f1c2ab on plugin/lib/plan.py" in f["verdict_words"]

    def test_withdrawn_has_no_words_of_sluices_but_flumes(self):
        f = self.facts("bolt-withdrawn")
        assert (f["verdict"], f["verdict_words"], f["waiting"], f["waiting_words"]) == (
            "withdrawn", None, "submission", "the merge queue withdrew the submission")


FLUME_19 = pathlib.Path(__file__).parent / "flume-0.19.0"
Y = "/Users/chuck/.local/share/flume/places/f3a444f5e38a/bolt--y"
Y_FIX = "/Users/chuck/.local/share/flume/places/f3a444f5e38a/fix--y-1"
MAIN_9F = "9f1c2ab07d6e5f4a3b2c1d0e9f8a7b6c5d4e3f21"


def status_19(name):
    return json.loads((FLUME_19 / f"{name}.json").read_text())


class TestBasePlaceFixes:
    """bolt-teams "A bolt's landing fix is read from its base place's status" (crews-bolt-kind-names-its-landing-fix,
    Decision 3): flume_facts reads a base place's fix kind, its bound and each fix Flume launched for it, as flume 0.19.0
    shapes them (tests/py/flume-0.19.0/), each guarded, and reads none from flume 0.17.0's status, which names none."""

    def facts(self, name, status=None):
        return runner.flume_facts(status or status_19(name), Y)

    def fixes(self, name):
        f = self.facts(name)
        return [(x["name"], x["cause"], x["submission"], x["ended"]) for x in f["fixes"]]

    def test_a_conflict_whose_fix_is_live(self):
        f = self.facts("bolt-conflict-fixing")
        assert (f["fix_kind"], f["fix_limit"], f["fixes_unread"], f["verdict"], f["entry"]) == ("flume/fix@1", 3, (), "conflict", "412")
        assert f["fixes"] == ({"number": 1, "name": "y-1", "place": Y_FIX, "cause": "conflicted", "submission": "412",
                               "head": None, "onto": None, "ended": "live", "commit": None, "reason": None},)

    def test_a_failure_whose_fix_is_due(self):
        f = self.facts("bolt-failed-fix-due")
        assert (f["fix_kind"], f["fix_limit"], f["fixes"], f["verdict"], f["entry"]) == ("flume/fix@1", 3, (), "failed", "412")

    def test_a_failure_past_its_bound(self):
        f = self.facts("bolt-failed-spent")
        assert self.fixes("bolt-failed-spent") == [("y-1", "conflicted", "412", "landed"), ("y-2", "failed", "413", "landed"),
                                                   ("y-3", "forecast", None, "refused")]
        assert f["fixes"][0]["commit"] == "1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e"
        assert f["fixes"][2]["reason"] == "the place fix--y-3 could not be made: its worktree's folder stands"
        assert (f["entry"], f["verdict"]) == ("415", "failed") and f["waiting_words"].endswith("Its kind's 3 fixes were launched, as many as it allows")

    def test_a_forecast_fix_names_the_revisions_it_was_formed_on(self):
        f = self.facts("bolt-forecast-fixing")
        assert (f["entry"], f["verdict"]) == (None, None)
        (x,) = f["fixes"]
        assert (x["name"], x["cause"], x["head"], x["onto"], x["submission"], x["ended"]) == (
            "y-1", "forecast", "4e8d2c1a9b7f6e5d4c3b2a1908f7e6d5c4b3a291", MAIN_9F, None, "live")

    def test_a_fix_dropped_and_a_fix_landed(self):
        assert self.fixes("bolt-conflict-dropped") == [("y-1", "conflicted", "412", "dropped")]
        assert self.fixes("bolt-fixed-landed") == [("y-1", "conflicted", "412", "landed")]
        assert self.facts("bolt-fixed-landed")["fixes"][0]["commit"] == "5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b"

    @pytest.mark.parametrize("name", sorted(p.stem for p in FLUME_17.glob("bolt-*.json")))
    def test_flume_0_17_names_no_fix_kind_and_no_fixes(self, name):
        f = runner.flume_facts(json.loads((FLUME_17 / f"{name}.json").read_text()), TestABasePlacesStatus.PLACE)
        assert (f["fix_kind"], f["fix_limit"], f["fixes"], f["fixes_unread"]) == (None, None, (), ())

    def test_a_fix_crew_cant_read_whole_is_left_out_and_named(self):
        status = status_19("bolt-failed-spent")
        fixes = status["status"]["places"][0]["fixes"]
        fixes[0]["ended"] = "abandoned"
        fixes[1]["cause"] = {"retried": {"submission": "413"}}
        fixes.append("y-4")
        f = self.facts(None, status)
        assert [x["name"] for x in f["fixes"]] == ["y-3"]
        assert f["fixes_unread"] == ("y-1", "y-2", "fix 4 of 4")

    def test_a_field_of_another_shape_reads_none(self):
        status = status_19("bolt-conflict-fixing")
        p = status["status"]["places"][0]
        p["fix_limit"], p["fix_kind"] = "3", {"identity": "flume/fix@1"}
        f = self.facts(None, status)
        assert (f["fix_limit"], f["fix_kind"]) == (None, None)
        p["fix_limit"], p["fixes"] = True, {"y-1": "live"}
        f = self.facts(None, status)
        assert (f["fix_limit"], f["fixes"], f["fixes_unread"]) == (None, (), ())


class TestVerification:
    """A bolt's verification is its work's landing at its head, as the runner reports it (merge-gate "A bolt's
    verification is its work's landing at its head, as the runner reports it"; runner.verification): green once some
    unit, chore or fix of it reads merged or landed at the head's commit, none for any other head, unknown with no
    head."""

    HEAD = "d185a879b51dba33555c036392b50443f4dfc5e8"
    OTHER = "0123abc" + "0" * 33

    def merged(self, commit=HEAD, **more):
        return dict({"stage": "merged", "place": "p", "commit": commit}, **more)

    def test_a_unit_landed_at_the_head_reads_green_naming_the_head_and_the_work(self):
        assert runner.verification(self.HEAD, [("unit/a", self.merged(self.OTHER)), ("unit/b", self.merged())]) == (
            "green", "its head d185a87 is b's landing, as the runner reports it")

    def test_a_chore_landed_at_the_head_reads_green(self):
        assert runner.verification(self.HEAD, [("unit/a", {"stage": "code"}), ("chore/tidy", self.merged())]) == (
            "green", "its head d185a87 is tidy's landing, as the runner reports it")

    def test_a_fix_landed_beside_the_queue_reads_as_any_landing_of_its_work(self):
        """A landing beside, a take-main fix's among them, is a landing like any other: sluice lands beside only when no
        required check reads its changes (sluice clause 140)."""
        assert runner.verification(self.HEAD, [("unit/a", self.merged(self.OTHER)), ("fix/b/take-main", self.merged())]) == (
            "green", "its head d185a87 is b--take-main's landing, as the runner reports it")

    def test_a_piece_read_from_its_bolts_landing_says_so(self):
        piece = self.merged(on="bolt", branch="change/a", landed="2026-11-08T10:00:00Z")
        assert runner.verification(self.HEAD, [("unit/a", piece)]) == (
            "green", "its head d185a87 is a's landing, as its landing on the bolt names it")

    def test_a_piece_merged_at_another_commit_leaves_the_head_no_landing(self):
        assert runner.verification(self.HEAD, [("unit/a", self.merged(self.OTHER))]) == (
            "none", "its head d185a87 is no landing of its work that the runner reports")

    def test_a_piece_with_no_commit_matches_nothing(self):
        assert runner.verification(self.HEAD, [("unit/a", self.merged(None)), ("unit/b", {"stage": "submitted", "submission": "41"})])[0] == "none"
        assert runner.verification(self.HEAD, [("unit/a", {"stage": "code", "commit": self.HEAD})])[0] == "none"

    def test_a_bolt_with_no_pieces_reads_none(self):
        assert runner.verification(self.HEAD, []) == (
            "none", "its head d185a87 is no landing of its work that the runner reports")

    def test_no_head_reads_unknown(self):
        assert runner.verification(None, [("unit/a", self.merged())]) == ("unknown", "no head crew can read")
        assert runner.verification("", [])[0] == "unknown"


class TestWhere:
    """Where a bolt's or a kit's work runs is what the runner that took it reported (the user's ruling of 2026-11-01;
    runner.where): the host whose runner took its newest launch taken, the kit's folder as that runner's
    repositories.rec reports it, or as Flume's status of its place there names it where it reports none, and the
    stream as that status names it (roles.9)."""

    def test_the_host_folder_and_stream_of_the_newest_launch_taken(self):
        """A runner that reports no repositories: the folder is the one Flume's status of its place names."""
        code = json.loads(fixture("code"))
        deneb = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", CODE), places=placed(3, code, CODE)), {})
        alpha = runner.host_read("madswan", "alpha", TIP, branch("alpha", answers=answer(1, "launched", "/old")), {})
        launches = held(rec(1, "launch"), rec(2, "launch", "unit/b"), rec(3, "launch", "unit/c"))
        assert runner.where({"deneb": deneb, "alpha": alpha}, launches, "bolt b", "afterthought/crew") == (
            {"host": "deneb", "dir": "/Users/chuck/Code/github_afterthought/crew", "stream": "default"}, None)
        assert runner.where({"alpha": alpha}, launches, "bolt b", "afterthought/crew") == ({"host": "alpha", "dir": None, "stream": None}, None)

    def test_work_no_runner_has_taken_is_nowhere_and_two_runners_are_told_apart_by_none(self):
        silent = runner.host_read("madswan", "alpha", TIP, {}, {"runner.rec": "recfix refused it"})
        assert runner.where({"alpha": silent}, held(rec(1, "launch")), "bolt b", "crew") == (None, (
            "no runner has reported taking bolt b's work yet, so crew can't tell where it runs; alpha's runner can't be read: "
            "madswan/runner/alpha at 5e1f0c2: recfix refused it"))
        two = {h: runner.host_read("madswan", h, TIP, branch(h, answers=answer(1, "launched", CODE)), {}) for h in ("alpha", "deneb")}
        assert runner.where(two, held(rec(1, "launch")), "bolt b", "crew") == (None, (
            "crew can't tell where bolt b's work runs: request 1 was taken by the runners on alpha and deneb, whose "
            "configurations each name its repository"))

    def test_the_folder_a_runner_reports_wins_over_a_places_stale_status(self):
        """drive-state "A kit renamed under its place": deneb carries request 1's place, Flume's status naming its
        repository /r/flywheel-cloud, its repositories.rec names agentplot/boomdrive-cloud at /r/boomdrive-cloud, and the
        bolt's kit reads boomdrive-cloud: the bolt is read in /r/boomdrive-cloud, its stream still the place's; with the
        place not carried yet, the folder is still the reported one."""
        code = json.loads(fixture("code"))
        code["status"]["places"][0]["repository"] = "/r/flywheel-cloud"
        report = kept(("agentplot/boomdrive-cloud", "/r/boomdrive-cloud"), ("agentplot/timber", "/r/timber"))
        deneb = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(1, "launched", CODE), places=placed(1, code, CODE),
                                                                repositories=report), {})
        launches = held(rec(1, "launch", Repo="flywheel-cloud"))
        assert runner.where({"deneb": deneb}, launches, "bolt you-sign-in-to-staging", "boomdrive-cloud") == (
            {"host": "deneb", "dir": "/r/boomdrive-cloud", "stream": "default"}, None)
        assert runner.where({"deneb": deneb}, launches, "boomdrive-cloud", "agentplot/boomdrive-cloud")[0]["dir"] == "/r/boomdrive-cloud"
        bare = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(1, "launched", CODE), repositories=report), {})
        assert runner.where({"deneb": bare}, launches, "bolt you-sign-in-to-staging", "boomdrive-cloud") == (
            {"host": "deneb", "dir": "/r/boomdrive-cloud", "stream": None}, None)

    def test_a_runner_that_does_not_keep_the_kit_leaves_it_unread_naming_what_it_keeps_and_the_rename(self):
        """drive-state "A runner that does not keep the kit": deneb's repositories.rec names only
        agentplot/boomdrive-cloud, and the bolt's kit reads flywheel-cloud with no rename; a runner whose file holds
        no record keeps no repository; nothing is read from the place's status (read.1)."""
        code = json.loads(fixture("code"))
        code["status"]["places"][0]["repository"] = "/r/flywheel-cloud"
        launches = held(rec(1, "launch", Repo="flywheel-cloud"))

        def of(report):
            deneb = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(1, "launched", CODE), places=placed(1, code, CODE),
                                                                    repositories=report), {})
            return runner.where({"deneb": deneb}, launches, "bolt you-sign-in-to-staging", "flywheel-cloud")
        assert of(kept(("agentplot/boomdrive-cloud", "/r/boomdrive-cloud"))) == (None, (
            "the runner on deneb took bolt you-sign-in-to-staging's work and keeps no flywheel-cloud: it keeps "
            "agentplot/boomdrive-cloud, so crew can't tell where flywheel-cloud is there; if flywheel-cloud was renamed on "
            "its host, crew kit rename flywheel-cloud <new> names it so in the plan"))
        assert of("")[1].startswith("the runner on deneb took bolt you-sign-in-to-staging's work and keeps no flywheel-cloud: "
                                    "it keeps no repository, so")

    def test_two_repositories_by_the_kits_name_are_told_apart_by_its_forge_address_or_refused(self):
        report = kept(("afterthought/crew", "/r/crew"), ("someone/crew", "/r/someone-crew"))
        deneb = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(1, "launched", CODE), repositories=report), {})
        launches = held(rec(1, "launch"))
        assert runner.where({"deneb": deneb}, launches, "bolt b", "afterthought/crew")[0]["dir"] == "/r/crew"
        assert runner.where({"deneb": deneb}, launches, "bolt b", "crew") == (None, (
            "the runner on deneb keeps afterthought/crew and someone/crew by the name crew, so crew can't tell which holds "
            "bolt b's work"))


class TestLaunchOf:
    """A piece's stage is read from its newest launch that no drop names (Decision 8): an amendment of a held launch is
    a drop and a launch anew (Decision 7)."""

    def test_the_newest_launch_not_dropped_is_the_ones_read(self):
        rs = held(rec(1, "launch"), rec(2, "launch", "unit/b", After=[1]), rec(3, "drop", Of=1), rec(4, "launch", Brief="Build it, amended."))
        assert runner.launch_of(rs, "unit/a").get("Request") == "4"
        assert runner.launch_of(rs, "unit/b").get("Request") == "2"
        assert runner.launch_of(rs, "chore/c") is None
        assert runner.launch_of(held(rec(1, "launch"), rec(2, "drop", Of=1)), "unit/a") is None
        assert runner.after_work(rs, rs[1]) == ["unit/a"]


def test_a_place_over_as_done_or_in_a_phase_crew_does_not_read_is_unknown_saying_so():
    """A kind that lands ends landed or dropped; a place Flume says is done, or in a phase crew does not know, is unknown,
    in Flume's words (read.1)."""
    for phase, why in (({"tidied": {"over": "done", "at": 1, "pending_for": []}}, "says its work is done, and a place of a kind that lands ends landed or dropped"),
                       ({"resting": {}}, "gives phase resting, which crew does not read")):
        status = json.loads(fixture("code"))
        status["status"]["places"][0]["phase"] = phase
        got = runner.stage_of("unit/a", rec(3, "launch"), plan.Rec("Answer", [("Request", "3"), ("Outcome", "launched")]),
                              {"place": CODE, "status": status, "why": None}, True)
        assert got["stage"] == "unknown" and got["why"] == f"Flume's status of unit/a's place {CODE} {why}"


class TestPriorities:
    """A launch's priority is its bolt's place among the plan's started bolts, counted from the end, and a write that
    launches or reorders bolts sends each priority the plan's order changed (Decision 6)."""
    FLEET = madswan_fleet()

    @staticmethod
    def write(*bolts):
        """madswan's plan with each bolt (name, Path or None) holding one unit named after it, its work built by crw-4."""
        return FactsWrite(flume_plan([(b, None, p) for b, p in bolts], [(f"{b}-unit", b, [], "unit", []) for b, _ in bolts]),
                          label="madswan")

    @staticmethod
    def priorities(w):
        """Each launch's work and the priority its requests last set, in the order launched."""
        rs = plan.Plan(w.files["requests.rec"]).recs("Request")
        last = {}
        for r in rs:
            if r.get("Act") == "launch":
                last[r.get("Request")] = [r.get("Work"), r.get("Priority")]
            elif r.get("Act") == "priority":
                last[r.get("Of")][1] = r.get("Priority")
        return [tuple(v) for v in last.values()]

    def start(self, w, bolt):
        """What a start appends: the bolt's base place's launch, then its pieces' (Decision 3)."""
        w.plan.bolt(bolt).set("Path", "flume")
        act, work, given = runner.bolt_launch(w.plan, bolt, w.label)
        plan.request(w, act, work, **given)
        plan.reach_places(self.FLEET, w, bolt)

    def test_the_first_bolt_in_the_plan_has_the_highest(self):
        """x and y are started, t between them and z after them planned: a planned bolt has no priority."""
        p = plan.Plan(flume_plan([("x", None, "flume"), ("t", None, None), ("y", None, "flume"), ("z", None, None)]))
        assert [runner.priority_of(p, b) for b in ("x", "t", "y", "z", "gone")] == [2, None, 1, None, None]

    def test_two_bolts_started_in_order(self, monkeypatch):
        """x is started and then y, x above y in the plan: x's pieces' launches carry a higher priority than y's, each
        naming crew's repository and no host or stream, intent madswan/<bolt> and recipient madswan/planner, after its
        bolt's base place's launch, whose recipient is madswan/ops and whose priority is set at its launch alone, since
        a base place takes no room in its stream."""
        monkeypatch.setenv("CREW_AGENT", BY)
        w = self.write(("x", None), ("y", None))
        self.start(w, "x")
        self.start(w, "y")
        assert self.priorities(w) == [("bolt/x", "1"), ("unit/x-unit", "2"), ("bolt/y", "1"), ("unit/y-unit", "1")]
        launches = [r for r in plan.Plan(w.files["requests.rec"]).recs("Request") if r.get("Act") == "launch"]
        assert [(r.get("Repo"), r.get("Host"), r.get("Stream"), r.get("Intent"), r.get("Recipient")) for r in launches] == [
            ("crew", None, None, "madswan/x", "madswan/ops"), ("crew", None, None, "madswan/x", "madswan/planner"),
            ("crew", None, None, "madswan/y", "madswan/ops"), ("crew", None, None, "madswan/y", "madswan/planner")]

    def test_a_third_started_raises_those_above_it(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", BY)
        w = self.write(("x", None), ("y", None), ("z", None))
        for b in ("x", "y", "z"):
            self.start(w, b)
        assert [p for p in self.priorities(w) if p[0].startswith("unit/")] == [("unit/x-unit", "3"), ("unit/y-unit", "2"), ("unit/z-unit", "1")]

    def test_a_reorder_sends_only_what_changed(self, monkeypatch):
        """crew bolt order puts z above y: requests.rec gains a priority for each launched place of y and z, whose
        priorities changed, and none for x's."""
        from facts import apply, known
        monkeypatch.setenv("CREW_AGENT", BY)
        w = self.write(("x", None), ("y", None), ("z", None))
        for b in ("x", "y", "z"):
            self.start(w, b)
        n = len(plan.Plan(w.files["requests.rec"]).recs("Request"))
        apply(w, "bolt order z --before y", ctx=known(w, fleet=self.FLEET))
        new = plan.Plan(w.files["requests.rec"]).recs("Request")[n:]
        assert [(r.get("Act"), r.get("Work"), r.get("Priority")) for r in new] == [
            ("priority", "unit/y-unit", "1"), ("priority", "unit/z-unit", "2")]
        apply(w, "bolt order z --before y", ctx=known(w, fleet=self.FLEET))
        assert len(plan.Plan(w.files["requests.rec"]).recs("Request")) == n + 2

    def test_a_reorder_on_a_branch_with_no_requests_writes_none(self):
        from facts import apply, known
        w = self.write(("x", None), ("y", None))
        apply(w, "bolt order y --first", ctx=known(w, fleet=self.FLEET))
        assert "requests.rec" not in w.files

    def test_a_dropped_launch_a_fix_of_main_and_a_bolt_gone_take_no_priority(self):
        p = plan.Plan(flume_plan([("x", None, "flume"), ("y", None, "flume")]))
        fix = dict(Base="main", Intent="madswan/main/crew", Recipient="madswan/ops", Name="main--red", Hold="submission")
        rs = held(rec(1, "launch", Base="bolt/x"), rec(2, "drop", Of=1), rec(3, "launch", "unit/b", Base="bolt/gone"),
                  rec(4, "launch", "fix/main/crew/red", **fix), rec(5, "launch", "unit/c", Base="bolt/y", Priority=7),
                  rec(6, "priority", "unit/c", Of=5, Priority=1))
        assert runner.priorities(p, rs) == []
        assert [(r.get("Request"), n) for r, n in runner.priorities(p, rs[:5])] == [("5", 1)]


class TestBoltLaunch:
    """A start launches the bolt's base place, then its pieces (bolt-teams "A start launches the bolt's base place before
    its pieces", "A start run again launches a bolt whose launch the runner refused"; Decision 3): runner.bolt_launch's
    fields, reach's pieces after it naming no After on it, its priority, and runner.restart for a bolt whose own launch
    the runner refused, and for none other."""
    FLEET = madswan_fleet()

    def write(self, *bolts):
        return FactsWrite(flume_plan([(b, None, None) for b in bolts], [("a", "x", [], "unit", []), ("b", "x", ["a"], "unit", []),
                                                                         ("c", "y", [], "unit", [])]), label="madswan")

    def start(self, w, bolt):
        w.plan.bolt(bolt).set("Path", "flume")
        act, work, given = runner.bolt_launch(w.plan, bolt, w.label)
        n = plan.request(w, act, work, **given)
        return n, plan.reach_places(self.FLEET, w, bolt)

    def test_the_launch_is_crews_kind_on_main_with_ops_its_recipient_and_no_brief_or_after(self):
        w = self.write("x")
        w.plan.bolt("x").set("Path", "flume")
        assert runner.bolt_launch(w.plan, "x", "madswan") == ("launch", "bolt/x", {
            "Repo": "crew", "Kind": "crew/bolt", "Name": "x", "Base": "main", "Priority": 1, "Intent": "madswan/x",
            "Recipient": "madswan/ops"})

    def test_its_pieces_follow_it_on_its_branch_naming_no_after_on_it(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", BY)
        w = self.write("x")
        n, launched = self.start(w, "x")
        rs = plan.Plan(w.files["requests.rec"]).recs("Request")
        assert (n, launched) == (1, [(2, "unit/a"), (3, "unit/b")])
        assert [(r.get("Work"), r.get("Base"), r.all("After")) for r in rs] == [
            ("bolt/x", "main", []), ("unit/a", "bolt/x", []), ("unit/b", "bolt/x", ["2"])]

    def test_its_priority_is_its_bolts_place_in_the_plan(self):
        w = self.write("x", "y")
        for b in ("x", "y"):
            w.plan.bolt(b).set("Path", "flume")
        assert [runner.bolt_launch(w.plan, b, "madswan")[2]["Priority"] for b in ("x", "y")] == [2, 1]

    def requests(self, *answers):
        """requests.rec after x's start, its base place request 1 and its units 2 and 3, and the runner answering as
        given (facts.ran's keywords)."""
        reqs = held(rec(1, "launch", "bolt/x", **dict(BOLT, Name="x")), rec(2, "launch", "unit/a", Base="bolt/x"),
                    rec(3, "launch", "unit/b", Base="bolt/x", After=[2]))
        return reqs

    def test_restarted_after_a_refusal_its_unlaunched_pieces_are_dropped_and_it_is_launched_anew(self):
        w = self.write("x")
        w.plan.bolt("x").set("Path", "flume")
        reads = ran(refused={1: "crew/bolt@1 is not locked on deneb"}, launched={3: "code"})
        asked, why = runner.restart(w.plan, self.requests(), reads, "x", "madswan")
        assert why is None
        assert [(act, work, given.get("Of"), given.get("Kind")) for act, work, given in asked] == [
            ("drop", "unit/a", "2", None), ("launch", "bolt/x", None, "crew/bolt")]

    @pytest.mark.parametrize("reads", [ran(), ran(held={1: None}), ran(launched={1: "flume-0.17.0/bolt-submitted"})])
    def test_no_restart_for_a_launch_unanswered_held_or_launched(self, reads):
        w = self.write("x")
        w.plan.bolt("x").set("Path", "flume")
        assert runner.restart(w.plan, self.requests(), reads, "x", "madswan") == (None, "bolt x is started already")

    def test_no_restart_for_a_bolt_with_no_launch_of_its_own_or_whose_runner_crew_cant_read(self):
        w = self.write("x")
        w.plan.bolt("x").set("Path", "flume")
        legacy = held(rec(1, "launch", "unit/a", Base="bolt/x"))
        assert runner.restart(w.plan, legacy, ran(), "x", "madswan") == (
            None, "bolt x is started already, before bolts were base places, and lands under the crew that started it")
        unread = {"deneb": runner.host_read("madswan", "deneb", TIP, {}, {})}
        asked, why = runner.restart(w.plan, self.requests(), unread, "x", "madswan")
        assert asked is None and why.startswith("bolt x is started already, and crew can't tell whether the runner refused its launch")


class TestLandingOf:
    """bolt-teams "A landing's outcome is read from the runner's report" (crew-lands-each-bolt-through-flumes-base-place,
    Decision 6): runner.landing_of reads a bolt's landing from its base place as the runner that took its launch
    reports it, one case per row of the design's table, on flume 0.17.0's base-place shapes (tests/py/flume-0.17.0/)."""
    PLACE = "/Users/chuck/.local/share/flume/places/f3a444f5e38a/bolt--the-runner-lands-each-bolt"

    def requests(self, lands=1):
        return held(rec(1, "launch", "bolt/b", **BOLT), *[rec(1 + n, "land", "bolt/b", Of=1) for n in range(1, lands + 1)])

    def of(self, reads, lands=1):
        rs = self.requests(lands)
        return runner.landing_of(rs[0], runner.lands_of(rs, rs[0]), reads)

    def test_a_launch_unanswered_held_or_refused_is_unlaunched_with_the_runners_words(self):
        assert self.of(ran(label="madswan")) == {"outcome": "unlaunched"}
        assert self.of(ran(held={1: "no room"})) == {"outcome": "unlaunched", "words": "no room"}
        assert self.of(ran(refused={1: "crew/bolt@1 is not locked"})) == {"outcome": "unlaunched", "words": "crew/bolt@1 is not locked",
                                                                         "refused": True}

    def test_no_land_standing_is_none(self):
        assert self.of(ran({1: "flume-0.17.0/bolt-submitted"}), lands=0) == {"outcome": "none"}

    def test_the_newest_land_unanswered_is_asked_with_its_request(self):
        assert self.of(ran({1: "flume-0.17.0/bolt-submitted"}), lands=2) == {"outcome": "asked", "request": 3}

    def test_a_land_answered_but_not_yet_submitted_by_flume_is_still_asked(self):
        """The place's submissions fewer than the lands the runner carried: Flume's verdict is an earlier land's."""
        assert self.of(ran({1: "flume-0.17.0/bolt-conflict"}, unplaced={2: "-", 3: "-"}), lands=2) == {"outcome": "asked", "request": 3}

    def test_the_runner_refusing_the_land_is_stopped_in_its_words(self):
        got = self.of(ran({1: "flume-0.17.0/bolt-submitted"}, refused={2: "flume refused it: a place on bolt/b is live"}))
        assert got == {"outcome": "stopped", "request": 2, "by": "runner", "words": "flume refused it: a place on bolt/b is live"}

    def test_a_submission_under_test_is_submitted_with_its_entry(self):
        got = self.of(ran({1: "flume-0.17.0/bolt-submitted"}, unplaced={2: "-"}))
        assert got == {"outcome": "submitted", "request": 2, "entry": "412", "state": "under_test"}
        assert runner.landing_said(got) == "landing #412 under test"

    def test_the_place_over_landed_is_landed_with_its_commit(self):
        got = self.of(ran({1: "flume-0.17.0/bolt-landed"}, unplaced={2: "-"}))
        assert got == {"outcome": "landed", "commit": "a7c3e9f1b2d4c6e8a0b1c3d5e7f9a1b3c5d7e9f0", "entry": "412", "request": 2}
        assert runner.landing_said(got) == "landed at a7c3e9f"

    def test_a_failed_check_is_refused_the_bolts_with_flumes_words(self):
        got = self.of(ran({1: "flume-0.17.0/bolt-failed"}, unplaced={2: "-"}))
        assert got == {"outcome": "refused", "request": 2, "why": "failed", "entry": "412",
                       "words": "check-full failed: tests:logic 3 failed (tests/py/test_landing.py)", "fix": {"by": "crew"}}

    def test_a_conflict_is_refused_naming_the_files_and_mains_revision(self):
        got = self.of(ran({1: "flume-0.17.0/bolt-conflict"}, unplaced={2: "-"}))
        assert (got["outcome"], got["why"], got["files"], got["main"]) == (
            "refused", "conflict", ["plugin/lib/plan.py", "plugin/lib/runner.py"], "9f1c2ab07d6e5f4a3b2c1d0e9f8a7b6c5d4e3f21")
        assert "conflicts with main at 9f1c2ab" in got["words"]

    def test_a_submission_withdrawn_is_stopped_in_flumes_words(self):
        got = self.of(ran({1: "flume-0.17.0/bolt-withdrawn"}, unplaced={2: "-"}))
        assert got == {"outcome": "stopped", "request": 2, "by": "flume", "words": "the merge queue withdrew the submission", "entry": "412"}

    def test_a_runner_or_a_submission_crew_cant_read_is_unknown_naming_why(self):
        unread = {"deneb": runner.host_read("madswan", "deneb", TIP, {}, {"answers.rec": "recfix refused it"})}
        got = self.of(unread)
        assert got["outcome"] == "unknown" and "recfix refused it" in got["why"]
        status = json.loads((FLUME_17 / "bolt-submitted.json").read_text())
        status["status"]["places"][0]["submission"]["read"] = {"could_not_read": {"reason": "sluice did not answer"}}
        reading = ran({1: "flume-0.17.0/bolt-submitted"}, unplaced={2: "-"})["deneb"]
        reading["places"][1]["status"] = status
        assert self.of({"deneb": reading}) == {"outcome": "unknown", "request": 2,
                                               "why": "Flume could not read bolt/b's submission: sluice did not answer"}

    def test_the_place_over_dropped_is_dropped(self):
        status = json.loads((FLUME_17 / "bolt-submitted.json").read_text())
        status["status"]["places"][0]["phase"] = {"over": {"over": "dropped", "kept": None}}
        reading = ran({1: "flume-0.17.0/bolt-submitted"})["deneb"]
        reading["places"][1]["status"] = status
        assert self.of({"deneb": reading}) == {"outcome": "dropped"}

    def test_a_field_of_another_shape_never_becomes_text(self):
        status = json.loads((FLUME_17 / "bolt-failed.json").read_text())
        status["status"]["places"][0]["submission"]["verdict"] = {"failed": {"words": 7}}
        status["status"]["places"][0]["waiting_on"]["words"] = None
        reading = ran({1: "flume-0.17.0/bolt-failed"}, unplaced={2: "-"})["deneb"]
        reading["places"][1]["status"] = status
        got = self.of({"deneb": reading})
        assert got["outcome"] == "refused" and "None" not in repr(got["words"]) and got["words"] == ""


class TestLandingFix:
    """bolt-teams "A bolt's landing fix is read from its base place's status" (crews-bolt-kind-names-its-landing-fix,
    Decision 3): landing_of gives a bolt's landing with its base place's landing fix as fix, and for a refusal whose
    its way on is, one case per row of the design's table, on flume 0.19.0's shapes (tests/py/flume-0.19.0/) and flume
    0.17.0's, which name no fix kind."""

    def of(self, name, lands=1):
        return TestLandingOf().of(ran({1: name}, unplaced={n: "-" for n in range(2, lands + 2)}), lands=lands)

    def test_a_status_naming_no_fix_kind_leaves_the_way_on_crews(self):
        got = self.of("flume-0.17.0/bolt-failed")
        assert (got["outcome"], got["why"], got["fix"]) == ("refused", "failed", {"by": "crew"})
        assert "fix" not in self.of("flume-0.17.0/bolt-landed") and "fix" not in self.of("flume-0.17.0/bolt-submitted", lands=0)
        assert runner.landing_fix(None) is None
        assert runner.landing_fix(runner.flume_facts(json.loads((FLUME_17 / "bolt-failed.json").read_text()), TestLandingOf.PLACE)) is None

    def test_a_conflict_whose_landing_fix_is_live_is_flumes(self):
        got = self.of("flume-0.19.0/bolt-conflict-fixing")
        assert (got["outcome"], got["why"], got["main"], got["entry"]) == ("refused", "conflict", MAIN_9F, "412")
        fix = got["fix"]
        assert (fix["by"], fix["kind"], fix["limit"], fix["ran"], fix["live"]["name"], fix["named"]["name"]) == (
            "flume", "flume/fix@1", 3, 1, "y-1", "y-1")
        assert "due" not in fix and "why" not in fix

    def test_a_failure_with_no_fix_yet_is_flumes_and_due(self):
        fix = self.of("flume-0.19.0/bolt-failed-fix-due")["fix"]
        assert (fix["by"], fix.get("due"), fix["ran"], fix["live"]) == ("flume", True, 0, None)

    def test_a_failure_past_the_bound_is_its_callers(self):
        got = self.of("flume-0.19.0/bolt-failed-spent")
        fix = got["fix"]
        assert (got["outcome"], got["entry"], fix["by"], fix["why"], fix["ran"], fix["limit"], fix["live"]) == (
            "refused", "415", "caller", "spent", 3, 3, None)
        assert "named" not in fix

    def test_a_fix_dropped_is_its_callers_naming_the_drop(self):
        fix = self.of("flume-0.19.0/bolt-conflict-dropped")["fix"]
        assert (fix["by"], fix["why"], fix["named"]["name"], fix["named"]["ended"]) == ("caller", "dropped", "y-1", "dropped")

    def test_a_fix_whose_launch_was_refused_is_its_callers(self):
        status = status_19("bolt-conflict-dropped")
        status["status"]["places"][0]["fixes"][0].update(ended="refused", reason="no place could be made")
        lf = runner.landing_fix(runner.flume_facts(status, Y))
        fix = runner.landing_way(lf, "412")
        assert (fix["by"], fix["why"], fix["named"]["reason"]) == ("caller", "refused", "no place could be made")

    def test_a_fix_landed_for_the_refusal_is_flumes(self):
        fix = self.of("flume-0.19.0/bolt-fixed-landed")["fix"]
        assert (fix["by"], fix["named"]["name"], fix["named"]["ended"], fix["live"]) == ("flume", "y-1", "landed", None)

    def test_a_forecast_fix_live_with_no_land_posted(self):
        got = self.of("flume-0.19.0/bolt-forecast-fixing", lands=0)
        assert got["outcome"] == "none" and got["fix"]["live"]["name"] == "y-1" and got["fix"]["live"]["cause"] == "forecast"
        assert "by" not in got["fix"]

    def test_a_bound_crew_cant_read_is_its_callers(self):
        lf = dict(runner.landing_fix(runner.flume_facts(status_19("bolt-failed-fix-due"), Y)), limit=None)
        assert runner.landing_way(lf, "412")["by"] == "caller"


class TestBaseDrop:
    """bolt-teams "A bolt's drop drops its base place last" and "A base place's drop the runner refused is asked again
    once nothing on its branch is live" (Decision 8): a drop of a started bolt appends its pieces' drops and then its
    base place's (plan.op_bolt_drop, reach), and once the runner refused the base place's drop, the next plan write that
    finds the bolt gone from the plan, its launch standing and no piece of it live asks the drop again
    (runner.base_drop_due), once for each refusal."""
    FLEET = madswan_fleet()

    def dropped(self, monkeypatch):
        """x started, its base place request 1 and unit a's request 2, then dropped: the requests the drop appends."""
        from facts import apply, known
        monkeypatch.setenv("CREW_AGENT", BY)
        w = FactsWrite(flume_plan([("x", None, None)], [("a", "x", [], "unit", [])]), label="madswan", runners=ran())
        w.plan.bolt("x").set("Path", "flume")
        act, work, given = runner.bolt_launch(w.plan, "x", "madswan")
        plan.request(w, act, work, **given)
        plan.reach_places(self.FLEET, w, "x")
        apply(w, 'bolt drop x "Not now."', ctx=known(w, fleet=self.FLEET))
        return w, plan.Plan(w.files["requests.rec"]).recs("Request")

    def test_a_drop_drops_its_pieces_and_then_its_base_place_last(self, monkeypatch):
        _, rs = self.dropped(monkeypatch)
        assert [(r.get("Request"), r.get("Act"), r.get("Work"), r.get("Of")) for r in rs][2:] == [
            ("3", "drop", "unit/a", "2"), ("4", "drop", "bolt/x", "1")]

    def test_a_refused_base_drop_is_asked_again_once_no_piece_is_live_and_once_for_each_refusal(self, monkeypatch):
        w, rs = self.dropped(monkeypatch)
        refused = ran({1: "flume-0.17.0/bolt-submitted", 2: "dropped"}, refused={4: "flume refused it: a place on bolt/x is live"})
        assert runner.base_drop_due(w.plan, rs, refused) == [("drop", "bolt/x", {"Of": "1"})]
        live = ran({1: "flume-0.17.0/bolt-submitted", 2: "code"}, refused={4: "flume refused it: a place on bolt/x is live"})
        assert runner.base_drop_due(w.plan, rs, live) == []
        asked = held(*rs, rec(5, "drop", "bolt/x", Of=1))
        assert runner.base_drop_due(w.plan, asked, refused) == []
        assert runner.base_drop_due(w.plan, rs, ran({1: "flume-0.17.0/bolt-submitted", 2: "dropped"})) == []

    def test_a_bolt_still_in_the_plan_or_one_with_no_drop_is_asked_nothing(self):
        p = plan.Plan(flume_plan([("x", None, "flume")]))
        rs = held(rec(1, "launch", "bolt/x", **dict(BOLT, Name="x")), rec(2, "drop", "bolt/x", Of=1))
        refused = ran({1: "flume-0.17.0/bolt-submitted"}, refused={2: "no"})
        assert runner.base_drop_due(p, rs, refused) == []
        assert runner.base_drop_due(plan.Plan(flume_plan([])), rs[:1], refused) == []
