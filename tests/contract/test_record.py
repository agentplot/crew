"""What crew assumes of recutils and git for its run record, each case naming what assumes it: a day's file a host began
under an older descriptor, before a card's Card and Key were allowed, takes an entry with them that recsel reads, and
record.unpushed writes that day to the branch under the descriptor that allows them, which recfix --check passes
(record.emit, record.unpushed, the card hook's entries); and a chain of entries plan.land pushes to a bare repository
standing for GitHub lands as one commit per entry, each changing its day's file alone, made again on top of another
clone's push that moved the branch between its fetch and its push, and on a branch moved before each of three pushes,
after a growing wait before each fresh fetch (plan.land, record.reach, state.1); and a first-parent
log's parents, Crew-Entry trailers and subjects, root commit and all, read a branch below a plan write whose entry is
still in flight though another host's entry landed after it, naming that write and its agent, and at its tip once the
entry arrives (plan.read_point, plan.fetch, read.5); and a plan write, its commit and then its entry's, is read at the
tip it leaves once it returns, while one given no act moves nothing (plan.write, plan.2)."""
import datetime
import re
import subprocess

import pytest

import crew
import plan
import record


@pytest.fixture
def runs(tmp_path, monkeypatch):
    monkeypatch.setattr(record, "ROOT", tmp_path / "crew")
    monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
    monkeypatch.setenv("CREW_AGENT", "swb-1-conductor")
    d = tmp_path / "crew" / "wldn" / "runs" / "mac-studio"
    d.mkdir(parents=True)
    return d


def test_an_older_days_file_takes_a_cards_fields_and_is_pushed_under_the_descriptor_that_allows_them(runs, tmp_path):
    day = record.path_for("wldn", "mac-studio", datetime.datetime.now(datetime.timezone.utc).date().isoformat())
    day.write_text(re.sub(r" Card Key[^\n]*\n", "\n", record.DESCRIPTOR))
    assert "Card" not in day.read_text()
    assert record.emit("wldn", "card.post", ["unit/x"], Card="req_old-1", Key="verify/x/20261007-1400")
    got = subprocess.run(["recsel", "-t", "Entry", "-e", "Act = 'card.post'", "-P", "Card,Key", str(day)], capture_output=True, text=True)
    assert got.stdout.split() == ["req_old-1", "verify/x/20261007-1400"]
    (*_, text), = record.unpushed("wldn", lambda path: None)[0]
    f = tmp_path / "pushed.rec"
    f.write_text(text)
    assert subprocess.run(["recfix", "--check", str(f)], capture_output=True).returncode == 0
    assert subprocess.run(["recsel", "-t", "Entry", "-P", "Card", str(f)], capture_output=True, text=True).stdout.strip() == "req_old-1"


def test_an_older_days_file_takes_a_lands_request_and_is_pushed_under_the_descriptor_that_allows_it(runs, tmp_path):
    """run-record "A day's file an older crew began" (crew-lands-each-bolt-through-flumes-base-place, Decision 4): the
    host's day file began under a descriptor allowing no Request, and crew records an asked bolt.submit with Request 57
    in it, which recsel reads, and the day pushed carries the descriptor that allows it and passes recfix --check
    (record.emit, record.unpushed, plan.lands_change)."""
    day = record.path_for("wldn", "mac-studio", datetime.datetime.now(datetime.timezone.utc).date().isoformat())
    day.write_text(record.DESCRIPTOR.replace(" Request", ""))
    assert "Request" not in day.read_text()
    assert record.emit("wldn", "bolt.submit", ["bolt/y"], Card="req_k1", Head="abc1234", Request="57", Outcome="asked")
    got = subprocess.run(["recsel", "-t", "Entry", "-e", "Act = 'bolt.submit'", "-P", "Request", str(day)], capture_output=True, text=True)
    assert got.stdout.strip() == "57"
    (*_, text), = record.unpushed("wldn", lambda path: None)[0]
    f = tmp_path / "pushed.rec"
    f.write_text(text)
    assert re.search(r"^%allowed:.* Request\b", text, re.M)
    assert subprocess.run(["recfix", "--check", str(f)], capture_output=True).returncode == 0
    assert subprocess.run(["recsel", "-t", "Entry", "-P", "Request", str(f)], capture_output=True, text=True).stdout.strip() == "57"


def test_a_days_file_begun_now_allows_them(runs):
    assert record.emit("wldn", "card.post", ["unit/y"], Card="req_new-1", Key="verify/y/20261007-1500")
    day, = runs.glob("*.rec")
    assert subprocess.run(["recfix", "--check", str(day)], capture_output=True).returncode == 0


def test_two_entries_written_at_once_by_two_processes_are_both_whole_and_the_file_passes_recfix(tmp_path):
    """record.emit: the descriptor goes in by a link and each entry in one append, so processes writing at once never
    interleave (record.4)."""
    import os
    import pathlib
    import sys
    lib = pathlib.Path(record.__file__).parent
    env = dict(os.environ, CREW_SESSION="")
    env.pop("CREW_AGENT", None)
    ps = [subprocess.Popen([sys.executable, str(lib / "record.py"), "emit", "--label", "wldn", "--act", f"test.{n}", "--on", f"unit/{n}"], env=env)
          for n in ("one", "two")]
    assert [p.wait() for p in ps] == [0, 0]
    f, = pathlib.Path(os.environ["HOME"]).glob(".local/state/crew/wldn/runs/*/*.rec")
    assert subprocess.run(["recfix", "--check", str(f)], capture_output=True).returncode == 0
    got = subprocess.run(["recsel", "-t", "Entry", "-C", "-P", "Act", str(f)], capture_output=True, text=True).stdout.split()
    assert sorted(got) == ["test.one", "test.two"]


def git(where, *args, input=None):
    r = subprocess.run(["git", "-C", str(where), *args], capture_output=True, text=True, input=input)
    assert r.returncode == 0, f"git {' '.join(args)}: {r.stderr.strip()}"
    return r.stdout.strip()


@pytest.fixture
def github(tmp_path, monkeypatch, runs):
    """A bare repository standing for WilldanGroup/crew-state on GitHub, its wldn/main holding a plan, and crew's cache
    and this command's reading of the branch in scratch."""
    bare = tmp_path / "crew-state.git"
    git(tmp_path, "init", "-q", "--bare", str(bare))
    w = tmp_path / "seed"
    git(tmp_path, "init", "-q", str(w))
    (w / "plan.rec").write_text(plan.HEADER)
    git(w, "add", "plan.rec")
    git(w, "commit", "-q", "-m", "plan: start (chuck@mac-studio)")
    git(w, "push", "-q", str(bare), "HEAD:refs/heads/wldn/main")
    monkeypatch.setattr(plan, "url", lambda repo: str(bare))
    monkeypatch.setattr(plan, "CACHE", tmp_path / "cache")
    monkeypatch.setattr(plan, "READ", plan.Reading())
    return bare


DAY = "2026-10-12"


def two_entries(runs):
    (runs / f"{DAY}.rec").write_text(record.DESCRIPTOR + "".join(
        f"\nId: 20261012T10000{n}Z-000000-mac-studio-1-{n}\nAt: {DAY}T10:00:0{n}Z\nHost: mac-studio\nBy: swb-1-conductor\nAct: tell\n"
        f"On: agent/wldn-planner\nChars: {n}\n" for n in (1, 2)))


def chain_at(tip):
    """What record.reach hands plan.land: the entries the branch lacks at the tip, one commit each."""
    chain, _ = record.unpushed("wldn", lambda path: plan.show("WilldanGroup/crew-state", tip, path))
    return [({path: text}, record.entry_message(lines, "swb-1-conductor")) for _, lines, path, text in chain]


def test_a_chain_of_two_entries_lands_as_two_commits_each_changing_its_days_file_alone(github, runs):
    two_entries(runs)
    before = git(github, "rev-parse", "wldn/main")
    sha = plan.land("WilldanGroup/crew-state", "wldn/main", None, chain_at)
    assert git(github, "rev-parse", "wldn/main") == sha
    commits = git(github, "rev-list", "--reverse", f"{before}..wldn/main").split()
    assert len(commits) == 2
    for c, n in zip(commits, (1, 2)):
        assert git(github, "diff-tree", "--no-commit-id", "--name-only", "-r", c) == f"runs/mac-studio/{DAY}.rec"
        assert git(github, "log", "-1", "--format=%(trailers:key=Crew-Entry,valueonly)", c) == f"20261012T10000{n}Z-000000-mac-studio-1-{n}"
    f = runs.parent / "landed.rec"
    f.write_text(git(github, "show", f"wldn/main:runs/mac-studio/{DAY}.rec") + "\n")
    assert subprocess.run(["recfix", "--check", str(f)], capture_output=True).returncode == 0
    assert git(github, "show", f"{commits[0]}:runs/mac-studio/{DAY}.rec").count("Id: ") == 1


def test_a_push_refused_because_another_clone_pushed_first_makes_the_chain_again_on_top(github, runs, tmp_path):
    two_entries(runs)
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "--branch", "wldn/main", str(github), str(other))
    tips = []

    def make(tip):
        tips.append(tip)
        if len(tips) == 1:  # another host writes the plan between this command's fetch and its push
            (other / "plan.rec").write_text(plan.HEADER + "\n")
            git(other, "commit", "-q", "-am", "plan: another host's write (wldn-planner)")
            git(other, "push", "-q", "origin", "wldn/main")
        return chain_at(tip)
    sha = plan.land("WilldanGroup/crew-state", "wldn/main", None, make)
    theirs = git(other, "rev-parse", "HEAD")
    assert len(tips) == 2 and tips[1] == theirs
    assert git(github, "rev-parse", "wldn/main") == sha and git(github, "rev-list", "--count", "--first-parent", f"{sha}~2..{sha}") == "2"
    assert git(github, "rev-parse", f"{sha}~2") == theirs
    assert git(github, "show", f"wldn/main:runs/mac-studio/{DAY}.rec").count("Id: ") == 2


def test_a_branch_busy_for_three_pushes_is_outwaited_each_wait_longer_and_made_before_a_fresh_fetch(github, runs, tmp_path, monkeypatch):
    """plan.land on a branch taking commits faster than one replay (state.1; madswan/main, 2026-10-27): git refuses
    the push of a chain made on a tip another clone has since moved, and land waits a growing moment before it fetches
    afresh, so it lands once the other clone is quiet, on top of its last commit."""
    two_entries(runs)
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "--branch", "wldn/main", str(github), str(other))
    events = []
    fetch = plan.tip_of
    monkeypatch.setattr(plan, "tip_of", lambda repo, ref, fresh=False: events.append("fetch" if fresh else "read") or fetch(repo, ref, fresh))
    monkeypatch.setattr(plan.time, "sleep", lambda s: events.append(s))
    monkeypatch.setattr("random.random", lambda: 0.0)

    def make(tip):
        if events.count("read") + events.count("fetch") <= 3:  # another host writes between this fetch and this push
            (other / "plan.rec").write_text((other / "plan.rec").read_text() + "\n")
            git(other, "commit", "-q", "-am", "plan: another host's write (wldn-planner)")
            git(other, "push", "-q", "origin", "wldn/main")
        return chain_at(tip)
    sha = plan.land("WilldanGroup/crew-state", "wldn/main", None, make)
    theirs = git(other, "rev-parse", "HEAD")
    waits = [w for w in events if isinstance(w, float)]
    assert events == ["read", waits[0], "fetch", waits[1], "fetch", waits[2], "fetch"]
    assert waits == [plan.replay_wait(n, 0.0) for n in range(3)] and waits[0] < waits[1] < waits[2]
    assert git(github, "rev-parse", "wldn/main") == sha and git(github, "rev-parse", f"{sha}~2") == theirs
    assert git(github, "rev-list", "--count", f"{git(other, 'rev-parse', 'HEAD~3')}..{theirs}") == "3"
    assert git(github, "show", f"wldn/main:runs/mac-studio/{DAY}.rec").count("Id: ") == 2


def test_a_branch_is_read_below_a_write_whose_entry_is_in_flight_and_at_its_tip_once_it_arrives(github, tmp_path):
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "--branch", "wldn/main", str(github), str(other))
    seed = git(other, "rev-parse", "HEAD")
    land, theirs = "20261030T140103Z-263678-deneb-74395-2", "20261030T140104Z-101010-mac-studio-512-1"

    def entry(eid, host):
        f = other / "runs" / host / "2026-10-30.rec"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text((f.read_text() if f.exists() else record.DESCRIPTOR) + f"\nId: {eid}\nAct: bolt.land\n")
        git(other, "add", "runs")
        git(other, "commit", "-q", "-m", f"runs({host}): bolt.land\n\nCrew-Entry: {eid}")
        git(other, "push", "-q", "origin", "wldn/main")
    (other / "plan.rec").write_text(plan.HEADER + "\n")
    git(other, "commit", "-q", "-am", f"plan(y): land the bolt (wldn-ops)\n\nCrew-Entry: {land}")
    written = git(other, "rev-parse", "HEAD")
    git(other, "push", "-q", "origin", "wldn/main")
    entry(theirs, "mac-studio")  # another host's entry lands between the write and its own
    assert plan.fetch("WilldanGroup/crew-state", "wldn/main", fresh=True) == seed
    assert plan.READ.below() == [dict(ref="wldn/main", tip=git(github, "rev-parse", "wldn/main"), at=seed, write=written,
                                      subject="plan(y): land the bolt (wldn-ops)")]
    entry(land, "deneb")
    assert plan.fetch("WilldanGroup/crew-state", "wldn/main", fresh=True) == git(github, "rev-parse", "wldn/main")
    assert plan.READ.below() == []


def test_a_plan_write_is_read_at_the_tip_it_leaves_once_it_returns_and_one_given_no_act_moves_nothing(github, runs, monkeypatch):
    """plan.2, read.5 (every-plan-write-is-an-act-with-its-entry): the write's commit names its entry, the write records
    it, and its own commit follows before the write returns, so no decision after it reads the branch below it; a write
    given no act, whose commit would name an entry nothing writes, is refused with the branch where it was."""
    fleet = {"partitions": {}, "hosts": {}}
    monkeypatch.setattr(crew, "load", lambda: fleet)
    monkeypatch.setattr(plan, "state_of", lambda fleet, label: ("WilldanGroup/crew-state", f"{label}/main"))

    def change(w):
        w.plan.insert(plan.Rec("Bolt", [("Bolt", "b"), ("Repo", "switchboard-kit"), ("Goal", "A goal.")]))
        return []
    sha = plan.write(fleet, "wldn", change, "plan(b): new bolt", act="bolt.new", on=["bolt/b"])
    tip = git(github, "rev-parse", "wldn/main")
    eid = git(github, "log", "-1", "--format=%(trailers:key=Crew-Entry,valueonly)", sha)
    assert git(github, "rev-parse", f"{tip}~1") == sha and tip != sha
    assert git(github, "log", "-1", "--format=%(trailers:key=Crew-Entry,valueonly)", tip) == eid
    day = git(github, "diff-tree", "--no-commit-id", "--name-only", "-r", tip)
    entry = [e for e in record.parse(git(github, "show", f"{tip}:{day}") + "\n") if e["Id"] == eid]
    assert [(e["Act"], e["On"], e["Commit"]) for e in entry] == [("bolt.new", ["bolt/b"], [f"WilldanGroup/crew-state@{sha}"])]
    assert plan.fetch("WilldanGroup/crew-state", "wldn/main", fresh=True) == tip and plan.READ.below() == []
    with pytest.raises(crew.Refusal):
        plan.write(fleet, "wldn", change, "plan(b): new bolt")
    assert git(github, "rev-parse", "wldn/main") == tip
