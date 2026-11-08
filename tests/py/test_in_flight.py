"""Every plan write is an act with its entry, and a read below the branch's tip says so (plan.2, read.5; the fix
every-plan-write-is-an-act-with-its-entry): a write given no act is refused before it reads or pushes anything, since its
commit would name a run-record entry nothing writes; every write crew makes names its act; and of a read below the
tip, the write it waits on, that write's agent, the words a command says of it, and those words before a refusal, whose
last line stays the refusal. Each on plain facts (code.7). A real write read whole once it returns is the contract tier's
(tests/contract/test_record.py); the commands' wiring, t-journey-plan's."""
import ast
import pathlib

import pytest

import crew
import plan

REPO = "WilldanGroup/crew-state"
# wldn/main as read on 2026-11-07, newest first: 18883a31f approved proposal 1009 (18:01:26Z), e0d5a954b proposed 1010
# (17:47:23Z), 16f19a887 cleared a unit's mark naming an entry no act wrote (17:46:34Z), and below it the same process's
# stage.end, whose entry the branch holds.
APPROVE, PROPOSE, CLEARED, END = (s + "0" * 31 for s in ("18883a31f", "e0d5a954b", "16f19a887", "0c1d2e3f4"))
BELOW = "1" * 40
IDS = {APPROVE: "20261107T180126Z-120000-chuck-herdr-alpha-77-1", PROPOSE: "20261107T174723Z-110000-chuck-herdr-alpha-66-1",
       CLEARED: "20261107T174633Z-983370-chuck-herdr-alpha-2601180-2", END: "20261107T174623Z-500000-chuck-herdr-alpha-2601180-1"}
COMMITS = [(APPROVE, PROPOSE, [IDS[APPROVE]]), (PROPOSE, CLEARED, [IDS[PROPOSE]]), (CLEARED, END, [IDS[CLEARED]]), (END, BELOW, [IDS[END]])]
DAY = "runs/chuck-herdr-alpha/2026-11-07.rec"
SUBJECT = "plan(production-stands-stage-in-devs-account): the-copy-acting-for-a-class-is-one-declared-value constructed again, its mark cleared (swb-2-conductor)"
SAID = ("wldn/main was read at 0c1d2e3, below its tip 18883a3: the write 16f19a8 by swb-2-conductor is on the branch without its "
        "run-record entry yet, so nothing from 16f19a8 on was read (read.5)")


def held(*commits):
    """The day's run-record file at the tip, holding the entries of the commits named."""
    return {DAY: "".join(f"Id: {IDS[c]}\nAct: x\n\n" for c in commits)}


# ------------------------------------------------------------------------------------------- every write is an act

def test_a_write_given_no_act_is_refused_before_it_reads_or_pushes_anything(monkeypatch):
    """The reading of 2026-11-07: wldn/main's 16f19a887 named Crew-Entry 20261107T174633Z-983370-chuck-herdr-alpha-2601180-2,
    which no run record held, since the write that cleared the mark was given no act; every decision after it read the
    branch at its parent for sixteen minutes. A write with no act now writes nothing."""
    touched = []
    monkeypatch.setattr(plan, "state_of", lambda fleet, label: touched.append("read") or (REPO, f"{label}/main"))
    monkeypatch.setattr(plan, "land", lambda *a: touched.append("pushed"))
    with pytest.raises(crew.Refusal) as e:
        plan.write({}, "wldn", lambda w: [], "plan(b): u constructed again, its mark cleared")
    assert str(e.value) == ('crew does not write "plan(b): u constructed again, its mark cleared": a write names its act, whose '
                            "run-record entry its commit names and the write itself records, and this one names none (plan.2)")
    assert touched == []
    assert plan.unacted("unit.unmark", "plan(b): u constructed again, its mark cleared") is None


def test_every_plan_write_crew_makes_names_its_act():
    """plan.write's callers, read from plan.py itself: each names act=, so none is refused at run time and none commits an
    entry nothing writes. On crew main, the give of a bolt, a unit marked amended so its construct runs again, and that
    mark cleared were the three that named none; this line has none of the three."""
    tree = ast.parse(pathlib.Path(plan.__file__).read_text())
    # a plan write takes the fleet, the label, the change and the subject; a session's write() of its own takes none
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "write"
             and len(n.args) >= 4]
    assert len(calls) > 10
    assert [n.lineno for n in calls if not any(k.arg == "act" for k in n.keywords)] == []


# ------------------------------------------------------------------------------------- a read below the tip says so

def test_the_write_a_read_waits_on_is_the_oldest_in_flight_and_the_read_is_unchanged():
    """decision_at reads wldn/main below 16f19a887, as it did, and the write it waits on is 16f19a887 itself."""
    texts = held(APPROVE, PROPOSE, END)
    assert plan.decision_at(COMMITS, texts) == END
    assert plan.waited_on(COMMITS, texts) == CLEARED
    assert [c[0] for c in plan.in_flight(COMMITS, texts)] == [CLEARED]
    assert plan.decision_at(COMMITS, {}) == BELOW and plan.waited_on(COMMITS, {}) == END  # the oldest of all in flight
    whole = held(APPROVE, PROPOSE, CLEARED, END)
    assert plan.decision_at(COMMITS, whole) == APPROVE and plan.waited_on(COMMITS, whole) is None
    # a branch whose first commit is in flight is read at its tip, waiting on nothing; and no commits, nothing
    assert plan.decision_at([(CLEARED, None, [IDS[CLEARED]])], {}) == CLEARED and plan.waited_on([(CLEARED, None, [IDS[CLEARED]])], {}) is None
    assert plan.waited_on([], {}) is None


def test_a_writes_agent_is_its_subjects_and_a_subject_naming_none_says_so():
    assert plan.writer_of(SUBJECT) == "swb-2-conductor"
    assert plan.writer_of("runs(chuck-herdr-alpha): stage.end stage/u/construct (swb-2-conductor)") == "swb-2-conductor"
    assert plan.writer_of("plan: start") is None and plan.writer_of("") is None and plan.writer_of(None) is None
    assert plan.below_said("wldn/main", APPROVE, END, CLEARED, SUBJECT) == SAID
    assert plan.below_said("wldn/main", APPROVE, END, CLEARED, "plan: by hand") == (
        "wldn/main was read at 0c1d2e3, below its tip 18883a3: the write 16f19a8, whose subject names no agent, is on the "
        "branch without its run-record entry yet, so nothing from 16f19a8 on was read (read.5)")


def test_a_commands_latest_read_of_a_branch_is_what_it_says_and_a_read_at_the_tip_takes_it_back():
    r = plan.Reading()
    assert r.below() == []
    r.keep_below(REPO, "wldn/main", PROPOSE, END, (CLEARED, SUBJECT))
    r.keep_below(REPO, "wldn/main", APPROVE, END, (CLEARED, SUBJECT))  # read again, the tip moved, still below the write
    r.keep_below(REPO, "swancloud/main", "3" * 40, "4" * 40, ("5" * 40, "plan: x (swancloud-planner)"))
    assert r.below() == [dict(ref="wldn/main", tip=APPROVE, at=END, write=CLEARED, subject=SUBJECT),
                         dict(ref="swancloud/main", tip="3" * 40, at="4" * 40, write="5" * 40, subject="plan: x (swancloud-planner)")]
    r.keep_below(REPO, "wldn/main", "6" * 40, "6" * 40, None)  # read at its tip once the entry arrived
    r.keep_below(REPO, "swancloud/main", None, None, None)  # a branch not there
    assert r.below() == []


def test_a_refusal_after_a_read_below_the_tip_says_so_first_and_an_answer_says_so_on_standard_error(monkeypatch, capsys):
    """crew plan answer 1010 and crew plan proposed 1010 answered "no proposal 1010 in wldn/main" while proposals.rec held
    it open, read at e0d5a954b's grandparent; now the refusal says where the branch was read and what it waits on, its
    own words still its last line."""
    r = plan.Reading()
    monkeypatch.setattr(plan, "READ", r)
    assert plan.below_read("no proposal 1010 in wldn/main") == "no proposal 1010 in wldn/main"
    assert plan.below_read() == "" and capsys.readouterr().err == ""
    r.keep_below(REPO, "wldn/main", APPROVE, END, (CLEARED, SUBJECT))
    assert plan.below_read("no proposal 1010 in wldn/main") == f"{SAID}\nno proposal 1010 in wldn/main"
    assert plan.below_read() == ""
    out = capsys.readouterr()
    assert out.err == SAID + "\n" and out.out == ""
