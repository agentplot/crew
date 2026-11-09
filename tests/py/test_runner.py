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
            "request 1 is a reorder, and a request is a launch, a retry, a drop, a priority, a land, a preview or a confirm")

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


KEYS = ["change--a/3f9a61c2/stage/construct/1/delivered", "change--a/3f9a61c2/stage/code/1/delivered"]


class TestConfirmRequest:
    """A confirm asks the runner that holds a launch to confirm to Flume, as a role's address, each end of its place the
    role's turn took (design Decision 4; drive-state "A launch names everything the runner passes to Flume")."""

    def test_a_confirm_of_a_launch_with_two_deliveries_is_written_in_the_files_order_and_passes(self):
        """drive-state, A confirm in a turn's end."""
        have = held(rec(1, "launch"), *[rec(n, "priority", Of=1, Priority=n) for n in range(2, 8)])
        r = rec(8, "confirm", Of=1, Recipient="madswan/planner", Delivery=KEYS)
        assert r.fields == [("Request", "8"), ("Act", "confirm"), ("Work", "unit/a"), ("Recipient", "madswan/planner"), ("Of", "1"),
                            ("Delivery", KEYS[0]), ("Delivery", KEYS[1]), ("Date", AT), ("By", BY)]
        assert runner.request_refusal(have, r) is None
        assert runner.request_refusal(have, rec(8, "confirm", Of=1, Recipient="wldn-2/ops", Delivery=KEYS[:1])) is None

    def test_a_confirm_with_no_key_or_no_recipient_is_refused_naming_what_it_lacks(self):
        """drive-state, A confirm with no key, or for no role."""
        have = held(rec(1, "launch"))
        assert runner.request_refusal(have, rec(2, "confirm", Of=1, Recipient="madswan/planner")) == (
            "confirm 2 for unit/a names no Delivery: a confirm carries Request, Act, Work, Date, By, Of, Recipient, Delivery")
        assert runner.request_refusal(have, rec(2, "confirm", Of=1, Delivery=KEYS)) == (
            "confirm 2 for unit/a names no Recipient: a confirm carries Request, Act, Work, Date, By, Of, Recipient, Delivery")

    @pytest.mark.parametrize("recipient", ["madswan/coder", "madswan", "boomdrive", "madswan/planner/x", "Madswan/planner"])
    def test_a_confirm_for_no_roles_address_is_refused_naming_the_recipient(self, recipient):
        """drive-state, A confirm with no key, or for no role: madswan/coder is no role of crew's."""
        assert runner.request_refusal(held(rec(1, "launch")), rec(2, "confirm", Of=1, Recipient=recipient, Delivery=KEYS)) == (
            f"confirm 2 for unit/a names {recipient} as its recipient, and a confirm is for the address of one of crew's roles, "
            "<label>/design, planner, reviewer, ops or operator")

    def test_a_confirm_of_no_launch_or_of_another_works_is_refused(self):
        have = held(rec(1, "launch"), rec(2, "drop", Of=1))
        assert runner.request_refusal(have, rec(3, "confirm", Of=9, Recipient="madswan/planner", Delivery=KEYS)) == (
            "confirm 3 for unit/a names request 9, which is no launch: requests.rec does not hold it")
        assert runner.request_refusal(have, rec(3, "confirm", Of=2, Recipient="madswan/planner", Delivery=KEYS)) == (
            "confirm 3 for unit/a names request 2, which is no launch")
        assert runner.request_refusal(have, rec(3, "confirm", "unit/b", Of=1, Recipient="madswan/planner", Delivery=KEYS)) == (
            "confirm 3 for unit/b names launch 1, which is unit/a's")

    def test_a_confirm_of_a_bolts_base_place_is_bolt_work(self):
        """drive-state, A bolt's work is its base place's and its preview's: the base place's ends are owed to ops's
        address as every place crew launches is, so ops's turn confirms them as bolt/<bolt>'s; a preview of it is no launch."""
        have = held(rec(1, "launch", "bolt/b", **BOLT), rec(2, "preview", "bolt/b", **PREVIEW))
        assert runner.request_refusal(have, rec(3, "confirm", "bolt/b", Of=1, Recipient="madswan/ops", Delivery=KEYS)) is None
        assert runner.request_refusal(have, rec(3, "confirm", "bolt/b", Of=2, Recipient="madswan/ops", Delivery=KEYS)) == (
            "confirm 3 for bolt/b names request 2, which is no launch")

    def test_a_confirm_carrying_what_it_does_not_take_is_refused(self):
        assert runner.request_refusal(held(rec(1, "launch")), rec(2, "confirm", Of=1, Recipient="madswan/planner", Delivery=KEYS,
                                                                  Stage="code")) == (
            "confirm 2 for unit/a carries Stage, which a confirm does not take")

    def test_the_descriptor_takes_a_confirm_and_its_deliveries_after_words(self):
        lines = runner.REQUESTS.splitlines()
        allowed = next(l for l in lines if l.startswith("%allowed:")).split()[1:]
        assert allowed[allowed.index("Words") + 1] == "Delivery" and allowed == list(runner.FIELDS)
        assert next(l for l in lines if l.startswith("%type: Act enum")).split()[-1] == "confirm"
        assert "or a confirm, as the role whose address is Recipient, of each Delivery" in next(l for l in lines if l.startswith("%doc:"))


PREVIEW = dict(Host="deneb", Repo="crew", Branch="bolt/y", Revision="abc1234" + "0" * 33)


class TestPreviewRequest:
    """A preview names its host, its work, its repository, its branch and its revision, and Done: yes to put it away
    (drive-state "A preview names its host, its work, its repository, its branch and its revision"; Decision 1)."""

    def test_a_previews_fields_are_written_in_the_files_order_and_its_done_as_yes(self):
        given = runner.preview_fields("deneb", "crew", "bolt/y", PREVIEW["Revision"])
        assert rec(8, "preview", "bolt/y", **given).fields == [
            ("Request", "8"), ("Act", "preview"), ("Host", "deneb"), ("Work", "bolt/y"), ("Repo", "crew"), ("Branch", "bolt/y"),
            ("Revision", PREVIEW["Revision"]), ("Date", AT), ("By", BY)]
        done = rec(9, "preview", "bolt/y", **runner.preview_fields("deneb", "crew", "bolt/y", PREVIEW["Revision"], done=True))
        assert done.get("Done") == "yes"
        assert [f for f, _ in done.fields].index("Done") == [f for f, _ in done.fields].index("Revision") + 1

    def test_a_preview_of_a_bolt_and_one_of_a_unit_pass(self):
        """drive-state "A preview of a landings row's bolt"; and a batch line's, of its unit."""
        assert runner.request_refusal([], rec(1, "preview", "bolt/y", **PREVIEW)) is None
        have = held(rec(1, "preview", "bolt/y", **PREVIEW))
        assert runner.request_refusal(have, rec(2, "preview", "unit/a", **dict(PREVIEW, Branch="change/a"))) is None
        assert runner.request_refusal(have, rec(2, "preview", "bolt/y", **dict(PREVIEW, Done="yes"))) is None

    def test_a_preview_naming_no_host_is_refused_saying_whose_runner_brings_it_up(self):
        """drive-state "A preview naming no host"."""
        assert runner.request_refusal([], rec(1, "preview", "bolt/y", **dict(PREVIEW, Host=None))) == (
            "preview 1 for bolt/y names no Host: a preview names the host whose runner brings it up, the one whose runner "
            "reported the work it serves")

    @pytest.mark.parametrize("field", ["Repo", "Branch", "Revision"])
    def test_a_preview_naming_no_repo_branch_or_revision_is_refused_naming_it(self, field):
        assert runner.request_refusal([], rec(1, "preview", "bolt/y", **dict(PREVIEW, **{field: None}))) == (
            f"preview 1 for bolt/y names no {field}: a preview carries Request, Act, Work, Date, By, Host, Repo, Branch, Revision")

    def test_a_preview_carrying_what_it_does_not_take_is_refused_naming_the_fields(self):
        """drive-state "A preview carrying what it does not take"."""
        assert runner.request_refusal([], rec(1, "preview", "bolt/y", Kind="change", Stream="madswan", **PREVIEW)) == (
            "preview 1 for bolt/y carries Kind, Stream, which a preview does not take")

    def test_a_preview_of_other_work_or_marked_done_otherwise_is_refused(self):
        assert runner.request_refusal([], rec(1, "preview", "chore/c", **PREVIEW)) == (
            "preview 1 serves chore/c, and a preview serves bolt/<bolt>, a landings row's, or unit/<unit>, a batch line's")
        assert runner.request_refusal([], rec(1, "preview", "bolt/y", **dict(PREVIEW, Done="no"))) == (
            "preview 1 for bolt/y is marked Done: no, and a preview is put away by Done: yes alone")

    def test_a_bolts_work_is_its_base_places_and_its_previews_alone(self):
        """drive-state "A bolt's work on any other request": bolt/<bolt> serves the bolt's base place, its launch of
        crew's kind and the acts on it, and a landings row's preview; a launch of it of any other kind is refused, and a
        retry or drop naming a preview by Of names no launch."""
        assert runner.request_refusal([], rec(1, "launch", "bolt/y")) == (
            "launch 1 of bolt/y names Kind change: a bolt's base place is of crew's kind crew/bolt")
        have = held(rec(1, "preview", "bolt/y", **PREVIEW))
        assert runner.request_refusal(have, rec(2, "retry", "bolt/y", Of=1, Words="Again.")) == (
            "retry 2 for bolt/y names request 1, which is no launch")
        assert runner.request_refusal(have, rec(2, "drop", "bolt/y", Of=1)) == (
            "drop 2 for bolt/y names request 1, which is no launch")

    def test_a_bolts_preview_and_its_base_places_land_stand_side_by_side(self):
        """drive-state "A preview and a land of one bolt": a land names the base place's launch by Of, never the
        preview of the same work."""
        have = held(rec(1, "launch", "bolt/y", **dict(BOLT, Name="y")), rec(2, "preview", "bolt/y", **PREVIEW))
        assert runner.request_refusal(have, rec(3, "land", "bolt/y", Of=1)) is None
        assert runner.request_refusal(have, rec(3, "land", "bolt/y", Of=2)) == "land 3 for bolt/y names request 2, which is no launch"

    def test_the_descriptor_takes_a_preview_last_its_done_and_its_fields_after_base(self):
        lines = runner.REQUESTS.splitlines()
        assert "%type: Act enum launch retry drop priority land preview confirm" in lines
        assert lines[lines.index("%type: Submission bool") + 1] == "%type: Done bool"
        allowed = next(l for l in lines if l.startswith("%allowed:")).split()[1:]
        assert allowed[allowed.index("Base") + 1:allowed.index("Base") + 4] == ["Branch", "Revision", "Done"]
        assert allowed == list(runner.FIELDS)
        assert "# drop, priority or land of a place launched; or a preview of a branch at a" in lines


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


def branch(host="deneb", runner_rec=None, answers="", places="", repositories=None, previews=None):
    """A runner's branch's files parsed as plan.runners parses them, each given as the records after its descriptor;
    repositories.rec and previews.rec only where given, a branch without them reporting no repositories and having
    answered no preview."""
    run = runner.RUNNER + (f"\nHost: {host}\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n" if runner_rec is None else runner_rec)
    return dict({"runner.rec": plan.Plan(run), "answers.rec": plan.Plan(runner.ANSWERS + answers), "places.rec": plan.Plan(runner.PLACES + places)},
                **({"repositories.rec": plan.Plan(runner.REPOSITORIES + repositories)} if repositories is not None else {}),
                **({"previews.rec": plan.Plan(runner.PREVIEWS + previews)} if previews is not None else {}))


def previewed(n, outcome, text=None, status=None, listed=None, words=None, at="2026-11-08T12:03:00Z"):
    """previews.rec's record of the runner's answer to preview request n, as Boomdrive's write.rs writes it: sluice's
    answer and listing each JSON on one line, given as a value or as the text itself."""
    j = lambda v: v if isinstance(v, str) else json.dumps(v)
    return (f"\nRequest: {n}\nOutcome: {outcome}\n" + (f"Text: {j(text)}\n" if text is not None else "")
            + (f"Status: {j(status)}\n" if status is not None else "") + (f"Listed: {listed}\n" if listed else "")
            + (f"Words: {words}\n" if words else "") + f"At: {at}\n")


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


UP = {"name": "crew-y", "branch": "bolt/y", "revision": "abc1234", "state": "up", "made": "2026-11-08T12:02:00Z",
      "addresses": {"web": "http://deneb:4310", "api": "http://deneb:4311"}}


class TestHostReadPreviews:
    """A runner's previews.rec is read by request number under the descriptor crew holds byte for byte; one crew can't
    read hides that runner, and a preview's JSON crew can't read marks that preview alone (drive-state "crew reads
    each host's runner from that runner's own branch"; Decision 3)."""

    def test_the_descriptor_is_boomdrives_byte_for_byte(self):
        assert runner.PREVIEWS == (
            "%rec: Preview\n%key: Request\n%type: Request int\n%type: Outcome enum held done refused\n%type: Listed enum yes no\n"
            "%type: At date\n%mandatory: Request Outcome At\n%allowed: Request Outcome Text Status Listed Words At\n")
        assert runner.FILES["previews.rec"] == "Preview"

    def test_a_runners_previews_are_read_by_their_requests_numbers(self):
        """drive-state "A preview the runner answered"."""
        r = runner.host_read("madswan", "deneb", TIP, branch(previews=previewed(12, "done", text=UP, status=UP, listed="yes")
                                                            + previewed(13, "held", words="sluice is at its bound")
                                                            + previewed(14, "refused", words="no [preview] at abc1234")), {})
        assert r["why"] is None
        assert r["previews"][12] == {"outcome": "done", "text": UP, "status": UP, "listed": True, "words": None,
                                     "at": "2026-11-08T12:03:00Z", "why": None}
        assert (r["previews"][13]["outcome"], r["previews"][13]["listed"], r["previews"][13]["words"]) == ("held", None, "sluice is at its bound")
        assert (r["previews"][14]["outcome"], r["previews"][14]["text"]) == ("refused", None)
        assert runner.host_read("madswan", "deneb", TIP, branch(previews=previewed(12, "done", text=UP, listed="no")), {})["previews"][12]["listed"] is False

    def test_a_runner_with_no_previews_file_has_answered_none(self):
        """drive-state "A runner that has answered no preview"."""
        r = runner.host_read("madswan", "deneb", TIP, branch(), {})
        assert (r["why"], r["previews"]) == (None, {})

    @pytest.mark.parametrize("previews, why", [
        (previewed(12, "held") + previewed(12, "done", text=UP), "previews.rec holds request 12 twice"),
        ("\nOutcome: held\nAt: 2026-11-08T12:03:00Z\n", "previews.rec holds a record with no request's number")])
    def test_a_request_twice_or_missing_hides_the_runner_naming_the_file(self, previews, why):
        """drive-state "A previews file crew can't read"."""
        assert runner.host_read("madswan", "deneb", TIP, branch(previews=previews), {})["why"] == (
            f"deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: {why}")

    def test_a_record_before_its_rec_hides_the_runner(self):
        files = dict(branch(), **{"previews.rec": plan.Plan("Request: 12\nOutcome: held\nAt: 2026-11-08T12:03:00Z\n")})
        assert runner.host_read("madswan", "deneb", TIP, files, {})["why"] == (
            "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: previews.rec holds a record before its %rec: Preview")

    def test_a_status_that_is_no_json_marks_that_preview_alone(self):
        """drive-state "A preview's listing that is no JSON"."""
        r = runner.host_read("madswan", "deneb", TIP, branch(previews=previewed(12, "done", text=UP, status="{not json", listed="yes")
                                                            + previewed(13, "done", text=UP, status=UP, listed="yes")), {})
        assert r["why"] is None and r["previews"][13]["why"] is None
        assert (r["previews"][12]["status"], r["previews"][12]["text"]) == (None, UP)
        assert r["previews"][12]["why"].startswith(
            "madswan/runner/deneb at 5e1f0c2: previews.rec's Status of the preview of request 12 is no JSON (")

    def test_a_previews_file_recfix_refused_hides_the_runner_naming_the_file(self):
        r = runner.host_read("madswan", "deneb", TIP, dict(branch(), **{"previews.rec": None}),
                             {"previews.rec": "previews.rec fails recfix --check: previews.rec: 12: error: invalid enum value in field 'Outcome'"})
        assert r["why"] == ("deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: previews.rec fails recfix --check: "
                            "previews.rec: 12: error: invalid enum value in field 'Outcome'")
        assert "previews" not in r


def asked(n, revision="abc1234", done=False, work="bolt/y", host="deneb"):
    """A preview request as crew card preview writes it."""
    return rec(n, "preview", work, **runner.preview_fields(host, "crew", "bolt/y" if work == "bolt/y" else "change/a", revision, done))


def deneb(answers="", previews=""):
    """The partition's runners as crew read them: deneb's alone, with these answers and previews."""
    return {"deneb": runner.host_read("madswan", "deneb", TIP, branch(answers=answers, previews=previews), {})}


class TestPreviewReport:
    """A preview is read from the runner on the host it names alone (drive-state "A preview is read from the runner on
    the host it names"; Decisions 2, 3 and 6)."""

    def test_each_outcome_of_previews_rec(self):
        r = asked(12)
        held_ = runner.preview_report(deneb(previews=previewed(12, "held", words="sluice is at its bound")), r)
        assert held_ == {"host": "deneb", "head": "abc1234", "at": "2026-11-08T12:03:00Z", "state": "held", "words": "sluice is at its bound"}
        refused = runner.preview_report(deneb(previews=previewed(12, "refused", words="no [preview] at abc1234")), r)
        assert (refused["state"], refused["words"]) == ("refused", "no [preview] at abc1234")
        up = runner.preview_report(deneb(previews=previewed(12, "done", text=UP, status=UP, listed="yes")), r)
        assert up == {"host": "deneb", "head": "abc1234", "at": "2026-11-08T12:03:00Z", "state": "up", "name": "crew-y",
                      "addresses": UP["addresses"]}
        failed = runner.preview_report(deneb(previews=previewed(12, "done", text=UP, status=dict(UP, state="failed"), listed="yes")), r)
        assert (failed["state"], "addresses" in failed, "output" in failed) == ("failed", False, False)

    def test_sluices_listing_wins_over_its_answer(self):
        """drive-state "A preview the runner answered": the listing's state, else the answer's."""
        report = runner.preview_report(deneb(previews=previewed(12, "done", text=dict(UP, state="starting"), status=UP, listed="yes")), asked(12))
        assert report["state"] == "up"
        report = runner.preview_report(deneb(previews=previewed(12, "done", text=dict(UP, state="starting"))), asked(12))
        assert (report["state"], report["addresses"]) == ("starting", UP["addresses"])

    def test_listed_no_reads_unlisted(self):
        report = runner.preview_report(deneb(previews=previewed(12, "done", text=UP, status=UP, listed="no")), asked(12))
        assert report["state"] == "unlisted"

    def test_a_refused_answer_is_read_as_refused_in_the_runners_words(self):
        """drive-state "A runner before previews"."""
        words = "its Act preview, which crew's implementation does not read"
        report = runner.preview_report(deneb(answers=answer(12, "refused", words=words)), asked(12))
        assert (report["state"], report["words"]) == ("refused", words)

    def test_no_answer_reads_asked(self):
        assert runner.preview_report(deneb(answers=answer(11, "launched", "/p")), asked(12)) == {
            "host": "deneb", "head": "abc1234", "state": "asked"}

    def test_the_host_unread_reads_unread(self):
        unread = {"deneb": runner.host_read("madswan", "deneb", TIP, dict(branch(), **{"previews.rec": None}),
                                            {"previews.rec": "previews.rec fails recfix --check"})}
        report = runner.preview_report(unread, asked(12))
        assert (report["state"], report["why"]) == (
            "unread", "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: previews.rec fails recfix --check")
        report = runner.preview_report({}, asked(12))
        assert (report["state"], report["why"]) == ("unread", "no runner answers on deneb, the host preview 12 names")
        report = runner.preview_report(deneb(previews=previewed(12, "done", status="{not json", listed="yes")), asked(12))
        assert report["state"] == "unread" and "previews.rec's Status of the preview of request 12 is no JSON" in report["why"]

    @pytest.mark.parametrize("doc, why", [
        (dict(UP, state="stopped"), 'gives state "stopped", which crew does not read'),
        (dict(UP, addresses=["http://deneb:4310"]), "gives addresses that are no object of text"),
        (dict(UP, name=7), "gives no name crew reads")])
    def test_a_field_crew_does_not_read_reads_unread_naming_it(self, doc, why):
        report = runner.preview_report(deneb(previews=previewed(12, "done", status=doc, listed="yes")), asked(12))
        assert report["state"] == "unread" and report["why"].endswith(why)
        assert report["why"].startswith("madswan/runner/deneb's previews.rec, request 12: sluice's preview")

    def test_an_ask_stands_until_a_done_or_a_refusal_and_again_after_a_bring_up(self):
        """drive-state "Put away, then asked again"."""
        one = held(asked(12))
        assert runner.previews_standing(one, deneb()) == {("deneb", "crew", "abc1234"): one[0]}
        two = held(asked(12), asked(13, done=True))
        assert runner.previews_standing(two, deneb()) == {}
        three = held(asked(12), asked(13, done=True), asked(14))
        assert runner.previews_standing(three, deneb()) == {("deneb", "crew", "abc1234"): three[2]}
        assert runner.previews_standing(one, deneb(previews=previewed(12, "refused", words="no"))) == {}
        assert runner.previews_standing(one, deneb(answers=answer(12, "refused", words="no"))) == {}
        assert runner.previews_standing(one, {}) == {("deneb", "crew", "abc1234"): one[0]}
        other = held(asked(12), asked(13, revision="def5678", done=True))
        assert list(runner.previews_standing(other, deneb())) == [("deneb", "crew", "abc1234")]

    def test_ask_step_keeps_a_standing_ask_and_asks_again_after_a_failure(self):
        ask = asked(12)
        assert runner.ask_step(None, None) == "ask"
        for state in ("asked", "held", "waiting", "starting", "up"):
            assert runner.ask_step(ask, {"state": state}) == "keep"
        for state in ("refused", "failed", "unlisted", "unread"):
            assert runner.ask_step(ask, {"state": state}) == "ask"

    def test_preview_word_of_each_shape(self):
        h = {"head": "abc1234"}
        assert runner.preview_word(dict(h, branch="bolt/y", state="ask")) == "ask"
        assert [runner.preview_word(dict(h, host="deneb", state=s)) for s in ("asked", "held", "failed", "refused", "unlisted")] == [
            "asked", "held", "failed", "refused", "unlisted"]
        assert [runner.preview_word(dict(h, name="n", addresses={}, state=s)) for s in ("waiting", "starting", "up")] == ["coming", "coming", "up"]
        assert runner.preview_word(dict(h, why="crew can't read it")) == "unread"
        assert runner.preview_word(dict(h, state="unread", why="crew can't read it")) == "unread"
        assert runner.preview_word(None) is None


class TestPreviewsPutAway:
    """The asks to put away are those no row, no work and no grace keeps (Decision 7; rail-cards "A preview is released
    on the user's done and when its card or row ends", "A moved head releases the preview of the old one")."""

    def asks(self, *reqs):
        return runner.previews_standing(held(*reqs), deneb())

    def test_a_row_that_can_land_at_the_head_keeps_its_ask(self):
        asks = self.asks(asked(12))
        assert runner.previews_put_away(asks, {("deneb", "crew", "abc1234")}, set()) == []

    def test_a_head_moved_puts_the_old_one_away(self):
        """rail-cards "The head moves with a preview up"."""
        asks = self.asks(asked(12))
        assert [r.get("Request") for r in runner.previews_put_away(asks, {("deneb", "crew", "def5678")}, set())] == ["12"]

    def test_a_held_or_gone_row_puts_it_away(self):
        """rail-cards "A fix holds the landing", "The bolt lands with its preview up": the row carries it no more."""
        asks = self.asks(asked(12), asked(13, revision="def5678", work="unit/a"))
        assert [r.get("Request") for r in runner.previews_put_away(asks, set(), set())] == ["12", "13"]

    def test_a_work_whose_card_stands_keeps_it(self):
        asks = self.asks(asked(12), asked(13, revision="def5678", work="unit/a"))
        assert [r.get("Request") for r in runner.previews_put_away(asks, set(), {"unit/a"})] == ["12"]

    def test_an_ask_under_the_grace_is_kept_and_one_over_it_put_away(self):
        """rail-cards "A card closed elsewhere": two minutes."""
        import datetime
        asks = self.asks(asked(12))
        at = datetime.datetime(2026, 10, 31, 12, 0, tzinfo=datetime.timezone.utc)
        assert runner.previews_put_away(asks, set(), set(), now=at + datetime.timedelta(seconds=90), grace=120) == []
        assert [r.get("Request") for r in runner.previews_put_away(asks, set(), set(), now=at + datetime.timedelta(seconds=150), grace=120)] == ["12"]

    def test_a_persons_preview_no_request_names_is_never_put_away(self):
        """rail-cards "A preview crew did not ask for"; and one the runner refused stands not, so has no done."""
        assert runner.previews_put_away(self.asks(), set(), set()) == []
        refused = runner.previews_standing(held(asked(12)), deneb(previews=previewed(12, "refused", words="no")))
        assert runner.previews_put_away(refused, set(), set()) == []


def test_crew_runs_no_sluice_command_for_a_preview():
    """Decision 9 of a-cards-preview-is-asked-of-the-runner (record 0056 point 1; roles.3): crew asks the runner for a
    card's preview and runs no sluice command for one, reads no kit's [preview], and keeps no preview record of its
    own. Read from crew's command core: no `preview`, `previews` or `release` of a preview handed to sluice_read, nor a
    sluice preview, previews or release command line (the tidy's `sluice release --worktree` of a place is no
    preview's); no previewed( call; no ~/.local/state/crew/previews path."""
    import re
    root = pathlib.Path(__file__).resolve().parents[2] / "plugin"
    texts = {p: p.read_text() for p in sorted((root / "lib").glob("*.py")) + [root / "bin" / "crew"]}
    found = []
    for p, text in texts.items():
        for n, line in enumerate(text.splitlines(), 1):
            if (re.search(r"sluice_read\([^)]*[\"'](preview|previews)[\"']", line)
                    or re.search(r"sluice_read\([^)]*[\"']release[\"'](?![^)]*--worktree)", line)
                    or re.search(r"sluice (preview|previews)\b", line)
                    or re.search(r"sluice release(?! --worktree)\b", line)
                    or re.search(r"[\"']sluice[\"'],\s*[\"'](preview|previews|release)[\"']", line)
                    or "previewed(" in line or ".local/state/crew/previews" in line):
                found.append(f"{p.relative_to(root)}:{n}: {line.strip()}")
    assert found == []


FLUME = pathlib.Path(__file__).parent / "flume-0.3.6"
FLUME_17 = pathlib.Path(__file__).parent / "flume-0.17.0"
FLUME_20 = pathlib.Path(__file__).parent / "flume-0.20.0"
HELD = "/Users/chuck/.local/share/flume/places/0132f9d25666/change--crew-runs-from-its-own-file-alone"
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


def flume_17(name, n=362, work="unit/pull-requests-are-queued-on-the-forge", base="bolt/sluice-runs-one-host-process"):
    """A place of flume 0.17.0's status (tests/py/flume-0.17.0/<name>.json) and its piece's stage as stage_of reads it,
    its launch request n on deneb answered launched at that place and the status carried on one line in places.rec."""
    status = json.loads((FLUME_17 / f"{name}.json").read_text())
    p = status["status"]["places"][0]
    r = runner.host_read("agentplot", "deneb", TIP, branch(answers=answer(n, "launched", p["place"]), places=placed(n, status, p["place"])), {})
    launch = held(rec(n, "launch", work, Base=base))[0]
    return p, runner.stage_of(work, launch, r["answers"][n], r["places"][n], True)


def held_for_the_runner(name, base="bolt/crew-names-each-drive-once", work="unit/crew-runs-from-its-own-file-alone", n=1140):
    """A piece's stage as stage_of reads it from a record Flume 0.20.0 holds for the runner after it tidies the place
    (tests/py/flume-0.20.0/<name>.json), its launch request n on deneb answered launched at the place's location and the
    record carried on one line in places.rec at its location@at, as the runner carries it."""
    status = json.loads((FLUME_20 / f"{name}.json").read_text())
    p = status["status"]["places"][0]
    where = p["place"].split("@")[0]
    r = runner.host_read("agentplot", "deneb", TIP, branch(answers=answer(n, "launched", where), places=placed(n, status, where)), {})
    launch = held(rec(n, "launch", work, Base=base))[0]
    return runner.stage_of(work, launch, r["answers"][n], r["places"][n], True)


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

    def test_a_place_past_its_bound_waits_on_its_caller_at_the_stage_it_waits_to_retry(self):
        """bolt-plan "A place past its bound", on flume 0.17.0's own status (tests/py/flume-0.17.0/past-bound.json):
        request 362's place as deneb's runner carried it at 05:27:38Z on 2026-11-08, its fourth verify delivered and its
        submission #24 in conflict, gone back three times, as often as its kind allows, so Flume says it waits on its
        caller to retry code past its bound; it reads waits at code with Flume's words, never at verify (Decision 1)."""
        p, got = flume_17("past-bound")
        assert (p["current"], p["stages"][2]["state"], p["waiting_on"]["why"]) == ("verify", "delivered", "past_bound")
        assert got == {"stage": "waits", "of": "code", "why": "past_bound", "words": p["waiting_on"]["words"], "held": False,
                       "place": p["place"], "tasks": (37, 37)}
        assert got["words"].startswith("the submission conflicted with its base: [sluice] #24 conflicts on bolt/sluice-runs-one-host-process")
        assert runner.piece_said(got) == ("waits", "waits on its caller at code: " + got["words"].splitlines()[0])
        assert runner.piece_said(got)[1].endswith("sluice wait 24 shows it.")

    def test_a_place_waiting_on_a_retry_of_its_submission_waits_at_its_submission(self):
        """bolt-plan "A submission that waits on its retry", on flume 0.17.0's status made from request 362's
        (tests/py/flume-0.17.0/submission-refused.json): its verify delivered and its submission refused by the merge
        queue, so Flume says it waits on its caller to retry its submission, naming no stage; it reads waits with no
        stage, unheld, and its line says it waits at its submission with Flume's words."""
        p, got = flume_17("submission-refused")
        assert got == {"stage": "waits", "of": None, "why": "submission", "words": p["waiting_on"]["words"], "held": False,
                       "place": p["place"], "tasks": (37, 37)}
        assert runner.piece_said(got) == ("waits", "waits on its caller at its submission: the merge queue refused the submission: "
                                          + p["submission"]["verdict"]["refused"]["reason"])

    def test_a_refusal_without_its_carry_says_when_its_runner_last_carried_it(self):
        """crew answer's refusal of a live place in code with no question, given no carry of the runner's (Decision 2 of
        a-place-waiting-on-its-caller-reads-waiting): it names the stage as its runner last carried it, with no host or
        time, and never that there is nothing to answer."""
        how, why = runner.answer_retry("unit/a", {"stage": "code", "place": "/crew/places/change--a", "tasks": (3, 7)})
        assert how is None and why == (
            "unit/a's place /crew/places/change--a was at code when its runner last carried it, with no question and nothing it "
            "waited on its caller for: a wait Flume has told of since reaches crew with that runner's next carry, so answer "
            "again once crew bolts shows the place waiting")
        assert runner.answer_retry("unit/a", {"stage": "code", "place": "/p"}, ("deneb", "2026-11-08T05:26:37Z"))[1].startswith(
            "unit/a's place /p was at code when deneb's runner carried it, at 2026-11-08T05:26:37Z, with no question")

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

    def test_a_landing_held_for_the_runner_is_merged_at_its_commit(self):
        """bolt-plan "A landing held for the runner", on flume 0.20.0's own record (tests/py/flume-0.20.0/): Flume landed
        the place and tidied it, holding its record for the runner, `{"tidied":{"over":{"landed":…},"pending_for":
        ["boomdrive"]}}` at `<location>@<at>`, and the runner carries it as the place's status; the piece reads merged at
        the record's commit on its bolt, and landed at it for a launch on main (design Decision 1)."""
        assert held_for_the_runner("landed-held") == {"stage": "merged", "commit": "f564d22041933732ee004aa33d1b629a97272cd9", "place": HELD}
        main = held_for_the_runner("landed-held", base="main", work="fix/main/crew/red")
        assert (main["stage"], main["commit"]) == ("landed", "f564d22041933732ee004aa33d1b629a97272cd9")

    def test_a_drop_held_for_the_runner_is_dropped(self):
        """bolt-plan "A drop held for the runner": the place's work over dropped, tidied and held for boomdrive."""
        assert held_for_the_runner("dropped-held") == {"stage": "dropped", "place": HELD}

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

    def test_a_live_landing_fix_is_a_fix_in_flight_on_its_bolt(self):
        """bolt-teams "A live landing fix holds its bolt" (Decision 5): fixes_in_flight on y's base place with y-1 live
        for a conflict gives y-1 taking main in at the refused entry's base; once y-1 has landed, nothing."""
        rs = held(rec(1, "launch", "bolt/y", **dict(BOLT, Name="y")))
        assert runner.fixes_in_flight([], "y", rs, ran({1: "flume-0.19.0/bolt-conflict-fixing"})) == {
            "y-1": "Take main into the bolt: Flume's landing fix y-1 merges main at 9f1c2ab"}
        assert runner.fixes_in_flight([], "y", rs, ran({1: "flume-0.19.0/bolt-fixed-landed"})) == {}
        assert runner.fixes_in_flight([], "y", rs, ran({1: "flume-0.19.0/bolt-forecast-fixing"})) == {
            "y-1": "Take main into the bolt: Flume's landing fix y-1 merges main at 9f1c2ab"}
        assert runner.fixes_in_flight([], "y", rs, ran({1: "flume-0.17.0/bolt-conflict"})) == {}

    def test_a_live_failed_checks_landing_fix_is_worded_for_the_checks(self):
        status = status_19("bolt-failed-fix-due")
        status["status"]["places"][0]["fixes"] = [{"number": 1, "name": "y-1", "place": Y_FIX, "cause": {"failed": {"submission": "412"}},
                                                   "launched": 1794176400, "ended": "live"}]
        f = runner.flume_facts(status, Y)
        assert runner.landing_fix_note(f, f["fixes"][0]) == (
            "Flume's landing fix y-1 makes the failed checks pass: check-full failed: tests:logic 3 failed (tests/py/test_landing.py)")

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
    verification is its work's landing at its head, as the runner reports it alone"; runner.verification): green once some
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
    repositories.rec reports it where it reports its repositories, else as Flume's status of its newest place of the
    work names it, and the stream as that status names it (roles.9; drive-state
    "A runner that reports no repositories")."""

    def test_the_host_folder_and_stream_of_the_newest_launch_taken(self):
        """deneb's repositories.rec names afterthought/crew: the folder is the one it reports, the stream the place's;
        the same reading with no repositories.rec takes the folder its place's status names."""
        code = json.loads(fixture("code"))
        report = kept(("afterthought/crew", "/Users/chuck/Code/github_afterthought/crew"))
        deneb = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", CODE), places=placed(3, code, CODE),
                                                                repositories=report), {})
        alpha = runner.host_read("madswan", "alpha", TIP, branch("alpha", answers=answer(1, "launched", "/old"), repositories=kept(
            ("afterthought/crew", "/a/crew"))), {})
        launches = held(rec(1, "launch"), rec(2, "launch", "unit/b"), rec(3, "launch", "unit/c"))
        assert runner.where({"deneb": deneb, "alpha": alpha}, launches, "bolt b", "afterthought/crew") == (
            {"host": "deneb", "dir": "/Users/chuck/Code/github_afterthought/crew", "stream": "default"}, None)
        assert runner.where({"alpha": alpha}, launches, "bolt b", "afterthought/crew") == ({"host": "alpha", "dir": "/a/crew", "stream": None}, None)
        bare = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(3, "launched", CODE), places=placed(3, code, CODE)), {})
        assert runner.where({"deneb": bare, "alpha": alpha}, launches, "bolt b", "afterthought/crew") == (
            {"host": "deneb", "dir": code["status"]["places"][0]["repository"], "stream": "default"}, None)

    def test_a_runner_that_reports_no_repositories_is_read_by_its_newest_place_of_the_work(self):
        """drive-state "A runner that reports no repositories": deneb's runner answers launch 1 of x's unit a and carries
        Flume's status of its place, naming its repository /w/crew, and its branch holds no repositories.rec: x is read
        in /w/crew on deneb, as crew main reads it; carrying no place of the work, its folder is None, which the callers
        refuse naming deneb (plan.launched_at, plan.kit_at, launch_repositories)."""
        code = json.loads(fixture("code"))
        code["status"]["places"][0]["repository"] = "/w/crew"
        deneb = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(1, "launched", CODE), places=placed(1, code, CODE)), {})
        assert runner.where({"deneb": deneb}, held(rec(1, "launch")), "bolt x", "crew") == (
            {"host": "deneb", "dir": "/w/crew", "stream": "default"}, None)
        bare = runner.host_read("madswan", "deneb", TIP, branch(answers=answer(1, "launched", CODE)), {})
        assert runner.where({"deneb": bare}, held(rec(1, "launch")), "bolt x", "crew") == (
            {"host": "deneb", "dir": None, "stream": None}, None)

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

    def test_a_landings_words_end_with_what_its_landing_fix_does(self):
        """crew-board "A bolt's head line names its landing fix" (Decision 6): the words the run record keeps and crew
        bolts prints end with the landing fix's clause, on each fixture of flume 0.19.0."""
        said = lambda name, lands=1: runner.landing_said(self.of(f"flume-0.19.0/{name}", lands))
        conflict = "landing refused in conflict with main at 9f1c2ab: bolt/y conflicts with main at 9f1c2ab on plugin/lib/plan.py, plugin/lib/runner.py"
        failed = "landing refused, a check failed: check-full failed: tests:logic 3 failed (tests/py/test_landing.py)"
        assert said("bolt-conflict-fixing") == f"{conflict}; Flume's landing fix y-1 takes main in"
        assert said("bolt-failed-fix-due") == f"{failed}; Flume launches its landing fix"
        assert said("bolt-failed-spent") == f"{failed}; Flume ran its 3 landing fixes, and it waits on ops"
        assert said("bolt-conflict-dropped") == f"{conflict}; Flume's landing fix y-1 was dropped, and it waits on ops"
        assert said("bolt-fixed-landed") == f"{conflict}; Flume's landing fix y-1 has landed at 5a6b7c8"
        assert said("bolt-forecast-fixing", lands=0) == "Flume's landing fix y-1 takes main in"
        assert runner.landing_said(self.of("flume-0.17.0/bolt-failed")) == failed

    def test_a_failed_checks_landing_fix_names_no_command_for_ops(self):
        """bolt-teams "A check fails with Flume's landing fix": z did not land, in Flume's words, and Flume's landing
        fix z-1 makes the failed checks pass, naming no command for ops."""
        l = self.of("flume-0.19.0/bolt-failed-fix-due")
        l["fix"] = dict(l["fix"], due=False, live={"name": "z-1", "cause": "failed", "note": ""})
        got = runner.landing_said(l, "z", "a" * 40)
        assert got == ("landing refused at aaaaaaa, a check failed, the bolt's, open for work: check-full failed: tests:logic 3 "
                       "failed (tests/py/test_landing.py); Flume's landing fix z-1 makes the failed checks pass")
        assert "crew fix" not in got

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

    def test_not_while_a_landing_fix_is_live_and_once_it_has_ended(self, monkeypatch):
        """bolt-teams "Not while a landing fix is live" (crews-bolt-kind-names-its-landing-fix, Decision 5): x's base
        place lists its landing fix live, so its refused drop is not asked again; once the fix has ended, one is."""
        w, rs = self.dropped(monkeypatch)
        refused = {4: "flume refused it: a place on bolt/x is live"}
        live = ran({1: "flume-0.19.0/bolt-conflict-fixing", 2: "dropped"}, refused=refused)
        assert runner.base_drop_due(w.plan, rs, live) == []
        ended = ran({1: "flume-0.19.0/bolt-fixed-landed", 2: "dropped"}, refused=refused)
        assert runner.base_drop_due(w.plan, rs, ended) == [("drop", "bolt/x", {"Of": "1"})]

    def test_a_bolt_still_in_the_plan_or_one_with_no_drop_is_asked_nothing(self):
        p = plan.Plan(flume_plan([("x", None, "flume")]))
        rs = held(rec(1, "launch", "bolt/x", **dict(BOLT, Name="x")), rec(2, "drop", "bolt/x", Of=1))
        refused = ran({1: "flume-0.17.0/bolt-submitted"}, refused={2: "no"})
        assert runner.base_drop_due(p, rs, refused) == []
        assert runner.base_drop_due(plan.Plan(flume_plan([])), rs[:1], refused) == []
