"""What crew assumes of recutils and git for its run record, each case naming what assumes it: a day's file a host began
under an older descriptor, before a card's Card and Key were allowed, takes an entry with them that recsel reads, and
record.unpushed writes that day to the branch under the descriptor that allows them, which recfix --check passes
(record.emit, record.unpushed, the card hook's entries); and a chain of entries plan.land pushes to a bare repository
standing for GitHub lands as one commit per entry, each changing its day's file alone, made again on top of another
clone's push that moved the branch between its fetch and its push, and on a branch moved before each of three pushes,
after a growing wait before each fresh fetch (plan.land, record.reach, state.1); and an older crew's write in two
steps, its commit and then its entry's, is read at the tip, another host's entry landing between them, its entry
absent from the run record there until its own commit lands (plan.tip_of, record.at, read.5); and a plan write's
commit is the tip it leaves once it returns,
holding its entry in its host's day file, naming no commit, while one given no act moves nothing, and a write refused
because another command of the same host pushed an entry to that day's file lands on top with both entries whole
(plan.write, plan.carried, plan.2, state.1; an-act-carries-its-entry-in-its-own-commit)."""
import datetime
import pathlib
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


def test_an_older_crews_two_step_write_is_read_at_the_tip_its_entry_absent_until_its_own_commit_lands(github, tmp_path):
    """drive-state "A decision reads the drive's branch at its tip" (an-act-carries-its-entry-in-its-own-commit,
    Decision 7): an older crew's write, its commit naming an entry and the entry its next commit, with another host's
    entry landing between the two; tip_of reads the tip, and the run record at the tip (record.at) lacks the write's
    entry until its own commit lands, then holds it."""
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "--branch", "wldn/main", str(github), str(other))
    land, theirs = "20261030T140103Z-263678-deneb-74395-2", "20261030T140104Z-101010-mac-studio-512-1"

    def entry(eid, host):
        f = other / "runs" / host / "2026-10-30.rec"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text((f.read_text() if f.exists() else record.DESCRIPTOR) + f"\nId: {eid}\nAt: 2026-10-30T14:01:0{eid[14]}Z\nAct: bolt.land\n")
        git(other, "add", "runs")
        git(other, "commit", "-q", "-m", f"runs({host}): bolt.land\n\nCrew-Entry: {eid}")
        git(other, "push", "-q", "origin", "wldn/main")
    (other / "plan.rec").write_text(plan.HEADER + "\n")
    git(other, "commit", "-q", "-am", f"plan(y): land the bolt (wldn-ops)\n\nCrew-Entry: {land}")
    git(other, "push", "-q", "origin", "wldn/main")
    entry(theirs, "mac-studio")  # another host's entry lands between the write and its own
    tip = plan.tip_of("WilldanGroup/crew-state", "wldn/main", fresh=True)
    assert tip == git(github, "rev-parse", "wldn/main") and plan.show("WilldanGroup/crew-state", tip, "plan.rec") == plan.HEADER + "\n"
    assert [e["Id"] for e in record.at("WilldanGroup/crew-state", tip, "2026-10-30")] == [theirs]
    entry(land, "deneb")
    tip = plan.tip_of("WilldanGroup/crew-state", "wldn/main", fresh=True)
    assert tip == git(github, "rev-parse", "wldn/main")
    assert sorted(e["Id"] for e in record.at("WilldanGroup/crew-state", tip, "2026-10-30")) == sorted([land, theirs])


def write_bolt(fleet, monkeypatch, change=None):
    monkeypatch.setattr(crew, "load", lambda: fleet)
    monkeypatch.setattr(plan, "state_of", lambda fleet, label: ("WilldanGroup/crew-state", f"{label}/main"))

    def add(w):
        w.plan.insert(plan.Rec("Bolt", [("Bolt", "b"), ("Repo", "switchboard-kit"), ("Goal", "A goal.")]))
        return (change or (lambda w: []))(w)
    return add


def test_a_plan_writes_commit_is_the_tip_holding_its_entry_and_one_given_no_act_moves_nothing(github, runs, monkeypatch):
    """plan.2, read.5 (an-act-carries-its-entry-in-its-own-commit, Decision 1): the write's commit is the tip once it
    returns, its tree's day file of its host holding its entry, which names no commit and which its trailer names, and
    the host's own file holds the entry too; a write given no act, whose commit would name an entry nothing writes, is
    refused with the branch where it was."""
    fleet = {"drives": {}, "hosts": {}}
    change = write_bolt(fleet, monkeypatch)
    sha = plan.write(fleet, "wldn", change, "plan(b): new bolt", act="bolt.new", on=["bolt/b"])
    assert git(github, "rev-parse", "wldn/main") == sha
    eid = git(github, "log", "-1", "--format=%(trailers:key=Crew-Entry,valueonly)", sha)
    day = f"runs/mac-studio/{datetime.datetime.now(datetime.timezone.utc).date().isoformat()}.rec"
    assert sorted(git(github, "diff-tree", "--no-commit-id", "--name-only", "-r", sha).split()) == sorted([day, "plan.rec"])
    entry, = record.parse(git(github, "show", f"{sha}:{day}") + "\n")
    assert (entry["Id"], entry["Act"], entry["On"], entry["Commit"]) == (eid, "bolt.new", ["bolt/b"], [])
    assert record.parse((runs / pathlib.PurePath(day).name).read_text()) == [entry]
    assert plan.tip_of("WilldanGroup/crew-state", "wldn/main", fresh=True) == sha
    with pytest.raises(crew.Refusal):
        plan.write(fleet, "wldn", change, "plan(b): new bolt")
    assert git(github, "rev-parse", "wldn/main") == sha


def test_a_write_refused_for_another_commands_entry_in_its_days_file_lands_on_top_with_both_entries_whole(github, runs, monkeypatch, tmp_path):
    """state.1, record.4 (Decision 1): another command on the same host pushes its entry to that day's file between
    this write's fetch and its push; git refuses the push, and the write applied again on the new tip carries its entry
    beside the other's, which stays as it was, and the day's file passes recfix --check."""
    day = f"runs/mac-studio/{datetime.datetime.now(datetime.timezone.utc).date().isoformat()}.rec"
    other = tmp_path / "other"
    git(tmp_path, "clone", "-q", "--branch", "wldn/main", str(github), str(other))
    theirs = (f"Id: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-000000-mac-studio-9-1\n"
              "At: 2026-11-10T09:00:00Z\nHost: mac-studio\nBy: wldn-planner\nAct: tell\nOn: agent/wldn-design\nChars: 5\n")
    tips = []

    def push_theirs(w):
        tips.append(w.tip)
        if len(tips) == 1:  # the tell's entry reaches the branch between this write's fetch and its push
            f = other / day
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(record.with_entries(None, {theirs.split("\n")[0][4:]: theirs}))
            git(other, "add", "runs")
            git(other, "commit", "-q", "-m", f"runs(mac-studio): tell agent/wldn-design (wldn-planner)\n\nCrew-Entry: {theirs.split(chr(10))[0][4:]}")
            git(other, "push", "-q", "origin", "wldn/main")
        return []
    fleet = {"drives": {}, "hosts": {}}
    sha = plan.write(fleet, "wldn", write_bolt(fleet, monkeypatch, push_theirs), "plan(b): new bolt", act="bolt.new", on=["bolt/b"])
    assert len(tips) == 2 and tips[1] == git(other, "rev-parse", "HEAD") == git(github, "rev-parse", f"{sha}~1")
    text = git(github, "show", f"{sha}:{day}") + "\n"
    eid = git(github, "log", "-1", "--format=%(trailers:key=Crew-Entry,valueonly)", sha)
    assert theirs in text and sorted(e["Id"] for e in record.parse(text)) == sorted([theirs.split("\n")[0][4:], eid])
    f = tmp_path / "landed.rec"
    f.write_text(text)
    assert subprocess.run(["recfix", "--check", str(f)], capture_output=True).returncode == 0
