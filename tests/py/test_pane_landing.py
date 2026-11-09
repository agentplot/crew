"""A landing stopped on the user's own words in main-level ops's pane (main-level "A stop said in ops's pane is read
as the user's words"; rail-cards "A bolt stopped in ops's pane is shown as left"): crew bolt leave records the stop at
the bolt's head holding none of the words, once crew reads them in ops's own transcript as the user's
(plan.leave_word_refusal), and raises the kit's card. The user's words in ops's pane land nothing
(crew-lands-each-bolt-through-flumes-base-place, Decision 4): a landing is the user's send on the kit's landings card,
which test_landings and test_card_commands cover; reading the words in a transcript is test_transcript's."""
import argparse

import pytest

import transcript

import plan


OLD, NEW = "a" * 40, "b" * 40
AT = {"label": "swancloud", "machine": "deneb", "stream": "swancloud", "kit": {"name": "crew", "dir": "/k", "main": "/k/main", "repo": "o/crew"}}
STOP = "Hold the phone bolt, don't land it yet"


def heard(asserted_by="user", grade="verified", uuid="u-7", reason=None):
    """A verdict on the words, as transcript.check gives it."""
    if grade == "unverified":
        return transcript.unverified(reason)
    return transcript.Verdict(grade, raw=b'{"type": "user"}', n=4, value={"uuid": uuid} if uuid else {},
                              asserted_by=asserted_by if grade == "verified" else "unknown")


class Plan:
    def bolt(self, name):
        return {"Bolt": name, "Repo": "crew"}


def submitted(bolt="y", frm=None, refused=None, by="swancloud-ops", at="2026-10-22T21:04:00Z", host="deneb"):
    e = {"Act": "bolt.submit", "On": [f"bolt/{bolt}"], "From": [frm] if frm else [], "By": by, "At": at, "Host": host}
    return dict(e, Refused=refused) if refused else e


@pytest.fixture
def leave(monkeypatch):
    """crew bolt leave on stand-ins for what it reaches: the plan, ops's transcript, each bolt's row as the host its work
    runs on reads it (rows, a bolt with none reading unproven), this host's run record and the raise of the kit's card."""
    got = {"emitted": [], "raised": [], "verdict": heard(), "at": {"y": AT, "z": AT},
           "rows": {"y": dict(bolt="y", box=True, facts=dict(head=NEW)), "z": dict(bolt="z", box=True, facts=dict(head=OLD))}}
    monkeypatch.setattr(plan, "CONTEXT", {})
    monkeypatch.setattr(plan, "locate", lambda fleet, kind, name, label: ("swancloud", "crew", "tip", Plan()))
    monkeypatch.setattr(plan, "default_label", lambda fleet, a: "swancloud")
    monkeypatch.setattr(plan, "bolt_at", lambda fleet, label, b, run=None: got["at"].get(b["Bolt"]))
    monkeypatch.setattr(plan, "land_read", lambda fleet, label, p, b, t: (
        (got["rows"][b["Bolt"]], None) if b["Bolt"] in got["rows"] else (None, "lands once its verification is green; now failed")))
    monkeypatch.setattr(plan.CardActs, "heard", lambda self, words: (got["verdict"], "s-1"))
    monkeypatch.setattr(plan.record, "emit", lambda label, act, on, **f: got["emitted"].append(dict(f, Act=act, On=on)) or "eid")
    monkeypatch.setattr(plan.record, "who", lambda: "swancloud-ops")
    monkeypatch.setattr(plan, "land_hand", lambda fleet, label, kit, note=None: got["raised"].append((label, kit, note)))

    def run(excerpt=STOP, bolts=("y",)):
        plan.bolt_leave({"drives": {}}, argparse.Namespace(bolt=list(bolts), label=None, excerpt=excerpt))
        return got
    got["run"] = run
    return got


class TestTheStop:
    """main-level "A stop said in ops's pane is read as the user's words", "A stop crew cannot read as the user's words
    is refused" and "A stop is recorded holding none of the user's words"; rail-cards "A bolt stopped in ops's pane is
    shown as left"."""

    def test_the_users_words_record_a_stop_at_the_bolts_head_holding_none_of_them_and_raise_its_kits_card(self, leave):
        got = leave["run"]()
        [e] = got["emitted"]
        assert (e["Act"], e["On"], e["Head"], e["frm"], e["Chars"]) == ("bolt.leave", ["bolt/y"], NEW, ["session/s-1/u-7"], len(STOP))
        assert STOP not in repr(e)
        assert got["raised"] == [("swancloud", "crew", "y was stopped on your words in swancloud-ops's pane")]

    def test_two_bolts_of_one_kit_raise_its_card_once(self, leave):
        got = leave["run"](bolts=("y", "z"))
        assert [(e["On"], e["Head"]) for e in got["emitted"]] == [(["bolt/y"], NEW), (["bolt/z"], OLD)]
        assert got["raised"] == [("swancloud", "crew", "y and z were stopped on your words in swancloud-ops's pane")]

    @pytest.mark.parametrize("v", [heard("agent:swancloud-operator"), heard(grade="refused"), heard("crew"), heard("tool"),
                                   heard(grade="found"), heard(grade="unverified", reason="no transcript for session s-1")])
    def test_words_crew_does_not_read_as_the_users_record_no_stop_as_a_landing_on_them_is_refused(self, leave, v):
        leave["verdict"] = v
        with pytest.raises(plan.Refusal) as e:
            leave["run"]()
        assert str(e.value) == plan.leave_word_refusal("y", v)
        assert STOP not in str(e.value) and leave["emitted"] == [] and leave["raised"] == []

    def test_another_agents_tell_is_named(self, leave):
        assert plan.leave_word_refusal("y", heard("agent:swancloud-operator")) == (
            "crew records no stop of bolt y: the words are swancloud-operator's, passed on with crew tell, and not the user's; "
            "tell swancloud-operator that the user stops a landing on its kit's landings card or in main-level ops's pane")

    def test_blank_words_ask_for_the_users(self, leave):
        with pytest.raises(plan.Refusal, match="crew bolt leave needs the user's words"):
            leave["run"]("  ")
        assert leave["emitted"] == []

    def test_a_bolt_not_started_or_not_proven_has_no_landing_to_stop(self, leave):
        leave["at"].pop("z")
        with pytest.raises(plan.Refusal, match="bolt z is not started, so it has no landing to stop"):
            leave["run"](bolts=("y", "z"))
        leave["at"]["z"], leave["rows"] = AT, {"y": leave["rows"]["y"]}
        with pytest.raises(plan.Refusal, match="bolt z does not read proven, so it has no landing to stop: lands once its "
                                               "verification is green; now failed"):
            leave["run"](bolts=("y", "z"))
        assert leave["emitted"] == [] and leave["raised"] == []

    def test_a_stop_stands_through_an_older_crews_landing_on_the_users_words(self):
        """No word in a pane lands a bolt (record 0056 point 5): an older crew's bolt.submit on the user's words lifts no
        stop, which only the user's tick on the card lifts (left_now)."""
        stop = dict(Act="bolt.leave", On=["bolt/y"], Head=NEW, From=["session/s-1/u-7"], Chars=len(STOP))
        assert plan.left_of([stop], "land/crew", {"y": NEW}) == {"y": NEW[:7]}
        assert plan.left_of([stop, submitted(frm="session/s-1/u-9")], "land/crew", {"y": NEW}) == {"y": NEW[:7]}
