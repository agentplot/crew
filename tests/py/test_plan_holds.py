"""A hold on a drive's or a kit's landings (bolt-plan "A hold on a drive or a kit is put and lifted through crew",
main-level "Main-level ops puts a hold on the user's words in its pane, and lifts none", run-record "The mark's lift
and the holds each leave one entry holding none of their words"; Decision 6 of a-proven-bolt-lands-on-proof): crew plan
hold and crew plan go applied to a plan in memory, crew's own check of the Hold records, the hold standing on a kit
(plan.hold_on), and who may run each (plan.may_write). That no land is posted while one stands is test_landings'."""
import argparse

import pytest
from facts import FLEET, FactsWrite, known, plan_text

import plan

KIT, BOARD = "switchboard-kit", "breadboard-kit"
WORDS = "Cutover"


@pytest.fixture(autouse=True)
def user(monkeypatch):
    monkeypatch.setenv("CREW_AGENT", "chuck@mac-studio")


def fresh():
    return FactsWrite(plan_text(bolts=[("console-pages", KIT, True), ("board-builds", BOARD, True), ("apex-zones", KIT, None)],
                                units=[("a-console-page", KIT, "console-pages", [])]))


def op(w, do):
    a = plan.do_args("wldn", do) if not do.startswith("plan ") else plan.parser(plan.Strict).parse_args(plan.shlex.split(do))
    a.label = a.label or "wldn"
    return plan.OPS[(a.cmd, a.sub)](known(w), a)


def applied(w, do):
    o = op(w, do)
    o.change(w)
    plan.check(w.plan)
    return o


def holds(w):
    return [(h.get("Kit"), h.get("Why")) for h in w.plan.holds()]


def refusal(w, do):
    before = w.plan.text()
    with pytest.raises(plan.Refusal) as e:
        applied(w, do)
    assert w.plan.text() == before
    return str(e.value)


class TestPut:
    def test_a_kit_held_is_a_hold_record_and_its_entry_holds_none_of_the_words(self):
        """bolt-plan "A kit held": a Hold naming the kit with its words, the entry a plan.hold on kit/<kit>."""
        w = fresh()
        o = applied(w, f'plan hold "{WORDS}" --repo {KIT}')
        assert holds(w) == [(KIT, WORDS)]
        assert (o.act, o.on, o.frm) == ("plan.hold", [f"kit/{KIT}"], [])
        assert w.subject == f"plan({KIT}): hold {KIT}'s landings" and WORDS not in w.subject + o.subject
        assert plan.hold_on(w.plan, KIT) == dict(kit=KIT, why=WORDS) and plan.hold_on(w.plan, BOARD) is None

    def test_the_drive_held_is_a_hold_naming_no_kit_and_holds_every_kit(self):
        """bolt-plan "The drive held": a Hold naming no kit, its entry on plan/<label>."""
        w = fresh()
        o = applied(w, f'plan hold "{WORDS}"')
        assert holds(w) == [(None, WORDS)] and (o.act, o.on) == ("plan.hold", ["plan/wldn"])
        assert WORDS not in w.subject
        assert plan.hold_on(w.plan, KIT) == plan.hold_on(w.plan, BOARD) == dict(kit=None, why=WORDS)

    def test_a_kits_own_hold_is_named_beside_the_drives(self):
        w = fresh()
        applied(w, f'plan hold "{WORDS}"')
        applied(w, f'plan hold "Its own" --repo {KIT}')
        assert plan.hold_on(w.plan, KIT) == dict(kit=KIT, why="Its own")
        assert plan.hold_on(w.plan, BOARD) == dict(kit=None, why=WORDS)
        assert plan.holds_of(w.plan) == [dict(kit=None, why=WORDS), dict(kit=KIT, why="Its own")]

    def test_a_second_hold_on_the_same_kit_changes_its_words(self):
        w = fresh()
        applied(w, f'plan hold "{WORDS}" --repo {KIT}')
        applied(w, f'plan hold "Cutover, then the move" --repo {KIT}')
        assert holds(w) == [(KIT, "Cutover, then the move")]
        assert w.subject == f"plan({KIT}): change the words of the hold on {KIT}'s landings"

    def test_a_kit_the_drive_does_not_name_is_refused(self):
        assert refusal(fresh(), f'plan hold "{WORDS}" --repo atlas-kit') == (
            "wldn's plan and landings name no kit atlas-kit, so it has no landings to hold")

    def test_a_plan_from_before_the_holds_takes_their_record_set_at_its_next_write(self):
        """bolt-plan "A branch from before the mark and the holds": in_step adds the Hold descriptor where the branch has
        none, once."""
        old = plan.Plan(plan.HEADER.split("\n%rec: Hold")[0] + "\n")
        assert "%rec: Hold" not in old.text()
        assert plan.in_step(old) is True and "%rec: Hold\n" in old.text() and "%allowed: Kit Why" in old.text()
        assert plan.in_step(old) is False


def test_two_holds_on_one_kit_or_the_drive_are_refused_by_crews_check():
    """bolt-plan "Two holds on one kit"."""
    for kit in (f"Kit: {KIT}\n", ""):
        p = plan.Plan(plan_text() + f"%rec: Hold\n\n{kit}Why: one\n\n{kit}Why: two\n")
        with pytest.raises(plan.Refusal) as e:
            plan.check(p)
        assert str(e.value) == ("the plan holds 2 holds on " + (f"kit {KIT}" if kit else "the whole drive")
                                + ", and it may hold one at most: crew plan hold changes the words of the one standing")


class TestLift:
    def held(self, *dos):
        w = fresh()
        for do in dos:
            applied(w, do)
        return w

    def test_a_lift_removes_the_hold_and_hands_a_raise_of_its_kits_card(self, monkeypatch):
        """bolt-plan "Lifted": the hold gone, a plan.go on kit/<kit>, and a raise of land/<kit> handed (land_hand)."""
        handed = []
        monkeypatch.setattr(plan, "land_hand", lambda fleet, label, kit, note=None: handed.append((label, kit, note)))
        w = self.held(f'plan hold "{WORDS}" --repo {KIT}')
        o = applied(w, f"plan go --repo {KIT}")
        assert holds(w) == [] and (o.act, o.on) == ("plan.go", [f"kit/{KIT}"])
        o.after("WilldanGroup/crew-state", "a" * 40)
        assert handed == [("wldn", KIT, f"the hold on {KIT}'s landings was lifted")]

    def test_the_drives_lift_raises_each_kit_with_a_started_bolt(self, monkeypatch):
        handed = []
        monkeypatch.setattr(plan, "land_hand", lambda fleet, label, kit, note=None: handed.append(kit))
        w = self.held(f'plan hold "{WORDS}"')
        o = applied(w, "plan go")
        assert holds(w) == [] and o.on == ["plan/wldn"]
        o.after("WilldanGroup/crew-state", "a" * 40)
        assert handed == [KIT, BOARD]

    def test_nothing_to_lift_is_refused_naming_the_drives_hold(self):
        """bolt-plan "Nothing to lift"."""
        assert refusal(self.held(), "plan go --repo atlas-kit") == "no hold names atlas-kit, so there is none to lift"
        assert refusal(self.held(f'plan hold "{WORDS}"'), "plan go --repo atlas-kit") == (
            "no hold names atlas-kit, so there is none to lift: the hold on the landings of wldn's every kit stands, which crew "
            "plan go --label wldn lifts")
        assert refusal(self.held(f'plan hold "{WORDS}" --repo {KIT}'), "plan go") == (
            "no hold names the whole drive wldn, so there is none to lift")


def may(monkeypatch, agent, argv):
    monkeypatch.setenv("CREW_AGENT", agent)
    a = plan.parser().parse_args(argv)
    try:
        plan.may_write(FLEET, (a.cmd, a.sub), a)
        return None
    except plan.Refusal as e:
        return str(e)


class TestWho:
    def test_the_user_puts_and_lifts(self, monkeypatch):
        assert may(monkeypatch, "chuck@mac-studio", ["plan", "hold", WORDS, "--repo", KIT]) is None
        assert may(monkeypatch, "chuck@mac-studio", ["plan", "go", "--repo", KIT]) is None

    def test_ops_puts_a_hold_on_the_users_words_read_as_theirs(self, monkeypatch):
        """main-level "The user's words typed in ops's pane": read in ops's own transcript (hold_heard), the entry naming
        the record they were read from and holding none of them."""
        monkeypatch.setenv("CREW_AGENT", "wldn-ops")
        said = "Pause landings on switchboard for the cutover"
        heard = []

        def words(acts, w, refusal):
            heard.append(w)
            return "session/s1/u1"
        monkeypatch.setattr(plan, "pane_words", words)
        monkeypatch.setattr(plan, "CardActs", lambda fleet: None)
        assert may(monkeypatch, "wldn-ops", ["plan", "hold", WORDS, "--repo", KIT, "--excerpt", said]) is None
        w = fresh()
        o = applied(w, f'plan hold "{WORDS}" --repo {KIT} --excerpt "{said}"')
        assert heard == [said] and o.frm == ["session/s1/u1"] and holds(w) == [(KIT, WORDS)]
        assert said not in " ".join([o.subject, w.subject] + o.on + o.frm)

    def test_ops_hold_of_words_not_the_users_is_refused(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "wldn-ops")
        v = argparse.Namespace(grade="refused", asserted_by="", board=False)
        assert plan.hold_word_refusal(f"{KIT}'s landings", v).startswith(
            f"crew puts no hold on {KIT}'s landings: the words are not in a record your session received")

        def words(acts, w, refusal):
            plan.fail(refusal(v))
        monkeypatch.setattr(plan, "pane_words", words)
        monkeypatch.setattr(plan, "CardActs", lambda fleet: None)
        with pytest.raises(plan.Refusal, match="crew puts no hold on"):
            op(fresh(), f'plan hold "{WORDS}" --repo {KIT} --excerpt "Hold it"')

    def test_ops_hold_with_no_words_of_the_users_is_refused(self, monkeypatch):
        """main-level "No words of the user's"."""
        assert may(monkeypatch, "wldn-ops", ["plan", "hold", WORDS, "--repo", KIT]) == (
            "crew plan hold needs the user's words: --excerpt \"<their words in your pane, as they wrote them>\"; a hold is the "
            "user's, put in your name only on their own words")

    def test_ops_lift_is_refused_as_the_users(self, monkeypatch):
        """main-level "Ops lifts a hold"."""
        assert may(monkeypatch, "wldn-ops", ["plan", "go", "--repo", KIT]) == (
            "wldn-ops lifts no hold: the lift, crew plan go, is the user's alone, since it lets lands be posted; tell the user")

    @pytest.mark.parametrize("agent", ["wldn-planner", "wldn-design", "wldn-operator"])
    def test_the_planner_and_the_design_agent_are_refused_naming_the_user_and_ops(self, monkeypatch, agent):
        """bolt-plan "The planner holds"."""
        assert may(monkeypatch, agent, ["plan", "hold", WORDS, "--label", "wldn"]) == (
            f"{agent} puts no hold on landings: the user puts it, or wldn-ops on the user's own words in its pane")
        assert may(monkeypatch, agent, ["plan", "go", "--label", "wldn"]).startswith(f"{agent} lifts no hold: ")


@pytest.mark.parametrize("do", [f'plan hold "{WORDS}" --repo {KIT}', f"plan go --repo {KIT}"])
def test_a_proposal_holding_a_hold_or_its_lift_is_refused(do):
    """plan-proposals "A hold in a proposal"."""
    with pytest.raises(plan.Refusal) as e:
        plan.do_args("wldn", do)
    assert str(e.value).startswith("a proposal holds only the plan's commands (") and str(e.value).endswith(f", not `{do}`")
    assert ("plan", "hold") not in plan.PROPOSABLE and ("plan", "go") not in plan.PROPOSABLE
