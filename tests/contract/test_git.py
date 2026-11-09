"""What crew assumes of git, each case naming what assumes it."""
import base64
import os
import shlex
import shutil
import subprocess
import time

import pytest


def test_merge_tree_names_the_conflicting_paths_and_writes_no_ref(repo):
    """plan.forecast_rows, the landings card's forecast of its rows (rail-cards "The landings card forecasts each row's
    conflicts"): git merge-tree --write-tree --name-only exits 1 on a conflict and lists the conflicting paths after
    the tree, and moves no ref."""
    repo.commit("main", {"a": "1\n"})
    repo.git("checkout", "-q", "-b", "one")
    repo.commit("one", {"a": "one\n"})
    repo.git("checkout", "-q", "-b", "two", "main")
    repo.commit("two", {"a": "two\n"})
    refs = repo.git("for-each-ref")
    r = subprocess.run(["git", "-C", str(repo.path), "merge-tree", "--write-tree", "--name-only", "one", "two"],
                       capture_output=True, text=True)
    assert r.returncode == 1
    lines = r.stdout.splitlines()
    assert lines[1] == "a"
    assert repo.git("for-each-ref") == refs


def onto(place, bolt, *heads):
    """plan.ONTO as rebase_dependents runs it in a dependent's place: <place> <the bolt's ref> [<head left out>...]."""
    import plan
    return subprocess.run(["bash", "-c", plan.ONTO, "crew", str(place), bolt, *heads], capture_output=True, text=True)


def settled_and_merged(repo, tmp_path, moved=False, own=None):
    """unit/a's change, and unit/b's place, which took a's head as crew's take does, by a merge, a fast-forward unless
    the bolt moved after a's place was made (moved), and added a commit of its own (own, else a file of b's own); then
    the bolt changes a's line,
    and a's settle rebases a onto it, resolving the line and revising a's design in the same commit, and a merges.
    Returns b's place and the head it took, which crew records as the construct's Took."""
    repo.commit("main", {"shared.txt": "one\ntwo\nthree\n", "f": "f\n"})
    repo.git("branch", "bolt/t")
    repo.git("checkout", "-q", "-b", "unit/a", "bolt/t")
    took = repo.commit("feat(a): its change", {"a/design.md": "z\n", "shared.txt": "one\ntwo, as a has it\nthree\n"})
    if moved:
        repo.git("checkout", "-q", "bolt/t")
        repo.commit("feat(x): its line", {"f": "x\n"})
    place = tmp_path / "place"
    repo.git("worktree", "add", "-q", "-b", "unit/b", str(place), "bolt/t")
    in_place = lambda *a: subprocess.run(["git", "-C", str(place), *a], check=True, capture_output=True)
    in_place("merge", "-q", "--no-edit", "-m", "chore(b): build on a as it stands", "unit/a")
    for name, text in (own or {"b.md": "b\n"}).items():
        (place / name).write_text(text)
        in_place("add", name)
    in_place("commit", "-qm", "feat(b): its own")
    repo.git("checkout", "-q", "bolt/t")
    repo.commit("feat: the bolt's line",
                {"shared.txt": "one\ntwo, as the bolt has it\nthree\n", **({"f": "x, then y\n"} if moved else {})})
    repo.git("checkout", "-q", "unit/a")
    assert subprocess.run(["git", "-C", str(repo.path), "rebase", "-q", "bolt/t"], capture_output=True).returncode != 0
    (repo.path / "shared.txt").write_text("one\ntwo, as a has it, and as the bolt has it\nthree\n")
    (repo.path / "a" / "design.md").write_text("z, as it stands on the bolt\n")
    repo.git("add", "shared.txt", "a/design.md")
    subprocess.run(["git", "-C", str(repo.path), "rebase", "--continue"], check=True, capture_output=True,
                   env=dict(os.environ, GIT_EDITOR="true"))
    repo.git("checkout", "-q", "bolt/t")
    repo.git("merge", "-q", "--no-ff", "unit/a", "-m", "Merge a")
    return place, took


def unmerged(place):
    return subprocess.run(["git", "-C", str(place), "diff", "--name-only", "--diff-filter=U"], capture_output=True,
                          text=True).stdout.split()


def kit_with_github(repo, tmp_path):
    """A kit's main checkout whose origin is a bare GitHub stand-in, and another clone that pushes to it."""
    repo.commit("chore: start", {"README.md": "r\n"})
    origin = tmp_path / "github.git"
    subprocess.run(["git", "clone", "-q", "--bare", str(repo.path), str(origin)], check=True)
    repo.git("remote", "add", "origin", str(origin)); repo.git("fetch", "-q", "origin")
    subprocess.run(["git", "clone", "-q", str(origin), str(tmp_path / "other")], check=True)

    def pushed(name):
        o = tmp_path / "other"
        subprocess.run(["git", "-C", str(o), "pull", "-q", "--rebase", "origin", "main"], check=True)
        (o / name).write_text(name)
        subprocess.run(["git", "-C", str(o), "add", name], check=True)
        subprocess.run(["git", "-C", str(o), "commit", "-qm", f"feat: {name}"], check=True)
        subprocess.run(["git", "-C", str(o), "push", "-q", "origin", "main"], check=True)
    return pushed


def main_at(repo):
    """plan.MAIN in the kit's main checkout: what kit.main_now decides main now from, and that decision."""
    import kit
    import plan
    r = subprocess.run(["bash", "-c", plan.MAIN, "crew", str(repo.path)], capture_output=True, text=True)
    return r, kit.main_now(r.stdout, "k", "h")


def test_a_landing_reads_githubs_main_after_a_fetch_however_far_the_hosts_own_main_lags(repo, tmp_path):
    """plan.bolt_land through MAIN (plan.8, plan.14, plan.18): the commit main holds now is GitHub's, origin/main after a
    fetch, which the landing records, against a bare remote whose main is ahead of the host's own; a kit with no origin
    says its own main's; a fetch that fails is refused, naming it (read.1)."""
    head = repo.commit("main", {"README": "r\n"})
    assert main_at(repo)[1] == ("main", head, None)
    pushed = kit_with_github(repo, tmp_path)
    repo.commit("feat: local", {"local": "l\n"}); pushed("later")
    github = subprocess.run(["git", "-C", str(tmp_path / "other"), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    assert main_at(repo)[1] == ("origin/main", github, None)
    repo.git("remote", "set-url", "origin", str(tmp_path / "gone.git"))
    r, (ref, sha, why) = main_at(repo)
    assert r.returncode == 0 and ref is None and why.startswith("cannot fetch k from GitHub on h, so cannot read its main now: fatal:"), why


def script(name, *args, cwd=None):
    import plan
    return subprocess.run(["bash", "-c", getattr(plan, name), "crew", *args], capture_output=True, text=True, cwd=cwd)


def two_bolts(repo, tmp_path):
    """A kit whose bolts live on GitHub, as the Willdan box's breadboard-kit stood on 2026-11-06 (signal
    2026-11-07-wldn-ops-052d0a47/01): bolt/deleting and bolt/popover made from main there, deleting holding one landing,
    #214, of its unit's commit, pushed from another clone as sluice lands from any host, the host's own copies of both
    left at main. Returns (git run in the other clone, its folder, landing 214's sha)."""
    policy = '[branches."bolt/*"]\nrequired = ["#check-full"]\nremote = "origin"\n'
    repo.commit("main", {".config/sluice.toml": policy})
    repo.git("branch", "bolt/deleting"); repo.git("branch", "bolt/popover")
    subprocess.run(["git", "clone", "-q", "--bare", str(repo.path), str(tmp_path / "github.git")], check=True)
    repo.git("remote", "add", "origin", str(tmp_path / "github.git"))
    other = tmp_path / "other"
    subprocess.run(["git", "clone", "-q", str(tmp_path / "github.git"), str(other)], check=True)
    o = lambda *a: subprocess.run(["git", "-C", str(other), *a], check=True, capture_output=True, text=True).stdout.strip()
    o("checkout", "-q", "-b", "unit/x", "origin/bolt/deleting")
    (other / "deleting").write_text("an app being deleted says so\n")
    o("add", "deleting"); o("commit", "-qm", "feat: a deleted app reads deleting")
    o("checkout", "-q", "-b", "bolt/deleting", "origin/bolt/deleting")
    o("merge", "-q", "--no-ff", "-m", "chore(land): #214 unit/x", "unit/x")
    o("push", "-q", "origin", "bolt/deleting")
    repo.git("fetch", "-q", "origin")
    return o, other, o("rev-parse", "HEAD")


def carries(repo, bolt, tip, into=""):
    """plan.CARRIES as bolts_carried runs it in the kit's main checkout, read by kit.carries_of and decided by
    gather.carried_bolts: {bolt: [its landings the tip holds]}."""
    import gather
    import kit
    r = script("CARRIES", str(repo.path), bolt, tip, into)
    assert r.returncode == 0, r.stderr
    holds, lines, why = kit.carries_of(r.stdout, bolt)
    assert why is None, why
    return gather.carried_bolts(holds, lines, bolt)


def test_a_bolt_holding_another_bolts_landing_carries_it_until_main_holds_it_and_the_other_carries_nothing(repo, tmp_path):
    """plan.bolts_carried through CARRIES (plan.8): bolt/popover's landing #216 merged a unit built on deleting's
    landing 214, so the popover bolt, read on GitHub after a fetch, carries deleting's work and the deleting bolt
    carries nothing of popover's; once main holds deleting's landing, popover carries nothing."""
    o, other, l214 = two_bolts(repo, tmp_path)
    o("checkout", "-q", "-b", "unit/pop", l214)
    (other / "pop").write_text("one popover\n")
    o("add", "pop"); o("commit", "-qm", "docs(openspec): propose who-can-open-an-app")
    o("checkout", "-q", "-b", "bolt/popover", "origin/bolt/popover")
    o("merge", "-q", "--no-ff", "-m", "chore(land): #216 unit/pop", "unit/pop")
    o("push", "-q", "origin", "bolt/popover")
    head = o("rev-parse", "HEAD")
    assert carries(repo, "popover", head) == {"deleting": [l214]}
    assert carries(repo, "deleting", l214) == {}
    o("checkout", "-q", "-B", "main", "origin/main")
    o("merge", "-q", "--no-ff", "-m", "chore(land): bolt/deleting", "bolt/deleting")
    o("push", "-q", "origin", "main")
    assert carries(repo, "popover", head) == {}


def test_a_bolt_github_deleted_after_it_landed_is_read_as_carrying_nothing_and_its_tracking_ref_kept(repo, tmp_path):
    """CARRIES prunes nothing (read.1): once bolt/deleting has landed on main and GitHub deletes its branch, the host's
    tracking ref of it stays, so no other read loses it mid-read, and its line beyond main is empty, so popover, which
    holds its landing, carries nothing."""
    o, other, l214 = two_bolts(repo, tmp_path)
    o("checkout", "-q", "-B", "bolt/popover", "origin/bolt/popover")
    o("merge", "-q", "--no-ff", "-m", "chore(land): #216 bolt/deleting's work", l214)
    o("push", "-q", "origin", "bolt/popover")
    head = o("rev-parse", "HEAD")
    o("checkout", "-q", "-B", "main", "origin/main")
    o("merge", "-q", "--no-ff", "-m", "chore(land): bolt/deleting", "bolt/deleting")
    o("push", "-q", "origin", "main", ":bolt/deleting")
    assert carries(repo, "popover", head) == {}
    assert repo.git("rev-parse", "refs/remotes/origin/bolt/deleting") == l214


def test_mains_policy_is_read_from_origin_main_as_last_fetched_ahead_of_the_hosts_own(repo, tmp_path):
    """plan.BOLT_HOME (plan.18), which bolts_local_said runs in a bolt's kit: a kit with an origin has its main's policy,
    AT_MAIN, read from origin/main as this host last fetched it, fetching nothing itself, not from the host's own main,
    which lags it (kit.bolt_home)."""
    import kit
    kit_with_github(repo, tmp_path)
    repo.git("branch", "bolt/b")
    o = tmp_path / "other"
    (o / ".config").mkdir()
    text = '[branches."bolt/*"]\nrequired = ["#check-full"]\nremote = "origin"\n'
    (o / ".config" / "sluice.toml").write_text(text)
    subprocess.run(["git", "-C", str(o), "add", ".config/sluice.toml"], check=True)
    subprocess.run(["git", "-C", str(o), "commit", "-qm", "chore: policy"], check=True)
    subprocess.run(["git", "-C", str(o), "push", "-q", "origin", "main"], check=True)

    def home():
        r = script("BOLT_HOME", str(repo.path), "b", kit.DECLARATION)
        assert r.returncode == 0, r.stderr
        return kit.said_of(r.stdout)["AT_MAIN"], kit.bolt_home(r.stdout, "b")

    assert home() == ("-", (None, None))
    repo.git("fetch", "-q", "origin")
    at, lives = home()
    assert (base64.b64decode(at).decode(), lives) == (text, (None, "origin"))
    assert not (repo.path / ".config" / "sluice.toml").exists()


def forecast_from_place(repo, tmp_path, bolt="t"):
    """plan.FORECAST_PLACE in the kit's main checkout, with a stand-in sluice that records the worktree it was asked
    to forecast from, the branch that worktree is on and its head, and answers with no conflict."""
    import plan
    bin_ = tmp_path / "bin"
    bin_.mkdir(exist_ok=True)
    (bin_ / "sluice").write_text(
        '#!/usr/bin/env bash\n'
        f'[ "$*" = "submit main --check --worktree $5 --json" ] || exit 64\n'
        f'echo "$5 $(git -C "$5" symbolic-ref --short HEAD) $(git -C "$5" rev-parse HEAD)" >> {tmp_path}/asked\n'
        'printf \'{"conflict": null, "head": "%s", "onto": "o", "ahead": []}\' "$(git -C "$5" rev-parse HEAD)"\n')
    (bin_ / "sluice").chmod(0o755)
    path = repo.path.parent / "places" / f"forecast-{bolt}"
    r = subprocess.run(["bash", "-c", plan.FORECAST_PLACE, "crew", str(repo.path), str(path), bolt], capture_output=True,
                       text=True, env=dict(os.environ, PATH=f"{bin_}:{os.environ['PATH']}"))
    assert r.returncode == 0, r.stderr
    return path, plan.place_checked(bolt, r.stdout, r.stderr), r.stdout


def test_a_units_change_is_read_from_mains_commit_into_a_folder(repo, tmp_path):
    """plan.change_folder through change_written (plan.18): a change that no place or bolt worktree holds is read as the
    kit's main holds it at a commit, open or else archived, its Markdown written into the session's folder, not read
    from the main checkout's files; a change main does not hold is None."""
    import plan
    repo.commit("main", {"README": "r\n"})
    sha = repo.commit("docs(openspec): archive a", {"openspec/changes/archive/2026-10-16-a/proposal.md": "p\n",
                                                     "openspec/changes/archive/2026-10-16-a/specs/x/spec.md": "s\n",
                                                     "openspec/changes/archive/2026-10-16-a/.openspec.yaml": "y\n"})
    repo.git("checkout", "-q", "HEAD~1")
    into = tmp_path / "card" / "change"
    assert plan.change_written(str(repo.path), sha, "a", into) == str(into)
    assert sorted(str(f.relative_to(into)) for f in into.rglob("*") if f.is_file()) == ["proposal.md", "specs/x/spec.md"]
    assert (into / "proposal.md").read_text() == "p\n"
    assert plan.change_written(str(repo.path), sha, "b", tmp_path / "none") is None


def test_a_landings_verdict_is_its_trailer(repo):
    """gather.kit (tests.5, record 0025): sluice's verdict on a landing is the Sluice-Result trailer of its merge
    commit, read with git log's trailer format; a commit sluice did not make has none."""
    import gather
    repo.commit("main", {"README": "r\n"})
    assert gather.run(["git", "log", "-1", "--format=%(trailers:key=Sluice-Result,valueonly)", "HEAD"], str(repo.path)).strip() == ""
    repo.commit("chore(land): #9 unit/a\n\nSluice-Submission: 9\nSluice-From: swb-1-unit-1 (unit/a)\nSluice-Tested: abc\n"
                "Sluice-Result: passed (9 run, 0 replayed)")
    assert gather.run(["git", "log", "-1", "--format=%(trailers:key=Sluice-Result,valueonly)", "HEAD"], str(repo.path)).strip() == (
        "passed (9 run, 0 replayed)")


BOLTS_ON_ORIGIN = '[branches."bolt/*"]\nrequired = ["#check-full"]\nremote = "origin"\n'


def github_main(tmp_path):
    return subprocess.run(["git", "--git-dir", str(tmp_path / "github.git"), "rev-parse", "main"],
                          capture_output=True, text=True).stdout.strip()


def work_kit(repo, monkeypatch):
    """A kit whose main checkout is repo, which the runner on this host reported taking its work in (plan.kit_at), and
    bolt/z cut from main holding its own commit; bolt_work reads the bolt there, a kit with no origin reading its own
    main (plan.bolt_work)."""
    import crew
    import plan
    monkeypatch.setattr(crew, "this_host", lambda: "here")
    kit = {"name": "k", "repo": "o/k", "main": str(repo.path), "dir": str(repo.path)}
    monkeypatch.setattr(plan, "kit_at", lambda fleet, label, name, run=None: {"label": label, "machine": "here", "kit": kit})
    fleet = {"drives": {"p": {"label": "p", "machine": "here", "teams": []}}, "teams": {}, "hosts": {}}
    repo.commit("chore: start", {"a.txt": "one\n"})
    repo.git("switch", "-q", "-c", "bolt/z")
    repo.commit("feat: the bolt's own", {"a.txt": "one, as the bolt has it\n"})
    repo.git("switch", "-q", "main")
    return fleet


def own_work(fleet, sent):
    import plan
    got = plan.bolt_work(fleet, "p", "k", {"z": (sent[:7], None)})["z"]
    assert got["why"] is None, got["why"]
    return [s for _, s in got["gained"]], [s for _, s in got["lost"]]


def merged_in(repo, branch, message, resolved=None):
    """branch merged into the branch checked out with --no-ff, a conflict resolved in the merge commit as resolved
    says, {path: text}."""
    r = subprocess.run(["git", "-C", str(repo.path), "merge", "-q", "--no-ff", branch, "-m", message], capture_output=True, text=True)
    if r.returncode:
        assert resolved, r.stdout + r.stderr
        for name, text in resolved.items():
            (repo.path / name).write_text(text)
            repo.git("add", "--", name)
        repo.git("commit", "-q", "--no-edit")
    return repo.git("rev-parse", "HEAD")


def test_a_bolt_that_took_main_in_with_a_conflict_resolved_holds_the_same_work_of_its_own(repo, monkeypatch):
    """plan.bolt_work (rail-cards, Decision 1): a take-main fix merges main, resolving a conflict in its merge commit,
    and sluice merges the fix into the bolt with --no-ff: git log --no-merges both ways, main excluded, lists nothing,
    so the user's send at the bolt's old head stands."""
    fleet = work_kit(repo, monkeypatch)
    sent = repo.git("rev-parse", "bolt/z")
    repo.commit("feat: main's own", {"a.txt": "one, as main has it\n"})
    repo.git("switch", "-q", "-c", "fix/z/take-main", "bolt/z")
    merged_in(repo, "main", "Merge main", {"a.txt": "one, as both have it\n"})
    repo.git("switch", "-q", "bolt/z")
    merged_in(repo, "fix/z/take-main", "Merge fix/z/take-main")
    assert repo.git("rev-parse", "bolt/z") != sent
    assert own_work(fleet, sent) == ([], [])


def test_a_fix_that_commits_a_change_is_work_the_bolt_gained(repo, monkeypatch):
    """plan.bolt_work (rail-cards "A fix adds a commit"): the fix's own commit is listed as gained, by its subject."""
    fleet = work_kit(repo, monkeypatch)
    sent = repo.git("rev-parse", "bolt/z")
    repo.git("switch", "-q", "-c", "fix/z/lease", "bolt/z")
    repo.commit("fix: keep the lease", {"lease.txt": "kept\n"})
    repo.git("switch", "-q", "bolt/z")
    merged_in(repo, "fix/z/lease", "Merge fix/z/lease")
    assert own_work(fleet, sent) == (["fix: keep the lease"], [])


def test_two_take_main_merges_from_one_tip_neither_an_ancestor_of_the_other_hold_the_same_work(repo, monkeypatch):
    """plan.bolt_work (rail-cards "The host's copy is brought level", plan.19's e104bcf and d64278b): the host's copy
    took main in at one commit and GitHub's at a later one, from the same tip, so neither head is an ancestor of the
    other; neither holds a non-merge commit of its own the other and main lack."""
    fleet = work_kit(repo, monkeypatch)
    tip = repo.git("rev-parse", "bolt/z")
    repo.commit("feat: main's first", {"b.txt": "b\n"})
    repo.git("switch", "-q", "--detach", tip)
    host = merged_in(repo, "main", "Merge main into the host's copy")
    repo.git("switch", "-q", "main")
    repo.commit("feat: main's second", {"c.txt": "c\n"})
    repo.git("switch", "-q", "bolt/z")
    github = merged_in(repo, "main", "Merge main into GitHub's copy")
    for one, other in ((host, github), (github, host)):
        assert subprocess.run(["git", "-C", str(repo.path), "merge-base", "--is-ancestor", one, other]).returncode == 1
    assert own_work(fleet, host) == ([], [])


def runner_files(host, answers="", places=""):
    """A runner's branch as a host's runner writes it (runner.RUNNER, ANSWERS, PLACES)."""
    import runner
    return {"runner.rec": runner.RUNNER + f"\nHost: {host}\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n",
            "answers.rec": runner.ANSWERS + answers, "places.rec": runner.PLACES + places}


def test_the_runners_branches_come_with_the_drives_branch_in_one_fetch_and_each_hosts_is_read_at_its_tip(state, monkeypatch):
    """plan.tip_of's fetch of <label>/main brings <label>/runner/* with it (plan.beside, plan.12), and plan.runners reads
    each host's three files at its tip in crew's cache with no fetch of its own, checked by recfix (Decision 4 of
    teams-cross-to-flume-as-their-bolts-land): deneb's answer and place for request 3 are read; alpha, which has no
    branch, is named; a host whose file recfix refuses hides only its own work; and a host's branch gone from the
    repository is gone from the cache at the next fetch."""
    import json
    import plan
    import runner
    status = json.dumps({"status": {"places": [{"place": "/crew/places/change--a", "phase": "live"}], "host": {}}})
    deneb = state.push("madswan/runner/deneb", runner_files(
        "deneb", "\nRequest: 3\nOutcome: launched\nPlace: /crew/places/change--a\nAt: 2026-10-31T12:01:00Z\n",
        f"\nRequest: 3\nPlace: /crew/places/change--a\nAt: 2026-10-31T12:02:00Z\nStatus: {status}\n"))
    state.push("madswan/runner/gamma", dict(runner_files("gamma"), **{"answers.rec": runner.ANSWERS + "\nRequest: 1\nOutcome: queued\nAt: 2026-10-31T12:01:00Z\n"}))
    state.push("swancloud/runner/deneb", runner_files("deneb"))  # another drive's runner on the same repository
    fetches = []
    git = plan.git
    monkeypatch.setattr(plan, "git", lambda repo, *args, **k: (fetches.append(args) if args[0] == "fetch" else None, git(repo, *args, **k))[1])

    reads = plan.runners(state.REPO, state.LABEL)
    assert len(fetches) == 1 and "+refs/heads/madswan/runner/*:refs/crew/madswan/runner/*" in fetches[0] and "--prune" in fetches[0]
    assert sorted(reads) == ["deneb", "gamma"]
    d = reads["deneb"]
    assert (d["why"], d["tip"], d["runner"].get("Version")) == (None, deneb, "0.1.0")
    assert d["answers"][3].get("Outcome") == "launched" and d["places"][3]["status"] == json.loads(status)
    assert reads["gamma"]["why"].startswith("gamma's runner can't be read: madswan/runner/gamma at ")
    assert "answers.rec fails recfix --check" in reads["gamma"]["why"]
    assert runner.of_host(reads, state.LABEL, "alpha")["why"] == "no runner answers on alpha: madswan/runner/alpha does not exist"
    assert plan.runners(state.REPO, state.LABEL) is reads and len(fetches) == 1

    state.drop("madswan/runner/gamma")
    plan.tip_of(state.REPO, "madswan/main", fresh=True)
    plan.READ.memory.clear()
    assert sorted(plan.runners(state.REPO, state.LABEL)) == ["deneb"]
    subprocess.run(["git", "-C", str(plan.cache(state.REPO)), "pack-refs", "--all"], check=True)
    plan.READ.memory.clear()
    assert plan.runner_tips(state.REPO, state.LABEL) == {"deneb": deneb}


def test_the_followers_fetch_brings_every_branch_of_a_repository_in_one_and_a_branch_not_made_costs_the_rest_nothing(state, monkeypatch):
    """plan.tips_of, the host's follower's one fetch of a repository at its clock's tick (Decision 3 of
    a-followers-tick-reads-nothing-while-nothing-moved; sluice core.31, the remote's one fetch a tick): madswan/main and
    swancloud/main, each with its runners' branches, in one git fetch, read from the cache's files after; with a
    drive's branch not made yet, the fetch that cannot find it is made again without it, the one there read and the
    other None."""
    import plan
    swan = state.push("swancloud/main", {"plan.rec": plan.HEADER}, "plan: start (chuck@deneb)")
    ran = state.push("swancloud/runner/deneb", {"runner.rec": "%rec: Runner\n"})
    mad = state.git("rev-parse", "refs/heads/madswan/main")
    fetches = []
    git = plan.git
    monkeypatch.setattr(plan, "git", lambda repo, *args, **k: (fetches.append(args) if args[0] == "fetch" else None, git(repo, *args, **k))[1])

    assert plan.tips_of(state.REPO, ["madswan/main", "swancloud/main"]) == {"madswan/main": mad, "swancloud/main": swan}
    assert len(fetches) == 1 and "+refs/heads/swancloud/runner/*:refs/crew/swancloud/runner/*" in fetches[0]
    assert plan.tip_here(state.REPO, "swancloud/main") == swan and plan.runner_tips(state.REPO, "swancloud", fetch=False) == {"deneb": ran}
    fetches.clear()
    assert plan.tips_of(state.REPO, ["madswan/main", "wldn/main"]) == {"madswan/main": mad, "wldn/main": None}
    assert len(fetches) == 2 and "+refs/heads/wldn/main:refs/crew/wldn/main" not in fetches[1], "a branch not made yet was asked again"


def change_files(out):
    """CHANGE_AT's output as plan.change_at reads it: [(path under the change, content)], in the order printed."""
    parts = out.split("\0")
    return list(zip(parts[0:-1:2], parts[1::2]))


def test_a_change_is_read_at_its_commit_open_or_archived_and_markdown_alone(repo):
    """plan.CHANGE_AT, which a batch's reading reads each unit's change with (batch_folder_write, change_at): a unit
    given through Flume is batched once its change is archived on its bolt, at the commit holding it so, and its change
    is read there from the archive's dated folder, as an open change is read from its own; a file not Markdown is left
    out, and a commit holding no change by the name prints nothing."""
    open_at = repo.commit("docs(a): the change", {"openspec/changes/a/proposal.md": "# a\n", "openspec/changes/a/tasks.md": "- [ ] 1.1 x\n",
                                                  "openspec/changes/a/.openspec.yaml": "schema: spec-driven\n"})
    r = script("CHANGE_AT", str(repo.path), open_at, "a")
    assert r.returncode == 0 and change_files(r.stdout) == [("proposal.md", "# a\n"), ("tasks.md", "- [ ] 1.1 x\n")]
    (repo.path / "openspec/changes/archive").mkdir()
    repo.git("mv", "openspec/changes/a", "openspec/changes/archive/2026-10-31-a")
    archived = repo.commit("docs(a): archive the change")
    r = script("CHANGE_AT", str(repo.path), archived, "a")
    assert r.returncode == 0 and change_files(r.stdout) == [("proposal.md", "# a\n"), ("tasks.md", "- [ ] 1.1 x\n")]
    r = script("CHANGE_AT", str(repo.path), archived, "b")
    assert (r.returncode, r.stdout) == (0, "")


def test_a_branch_flume_kept_is_read_standing_in_its_repository_and_a_name_beside_it_is_not(repo, tmp_path):
    """plan.BRANCHES and runner.refs_standing, which plan.branch_free reads a unit's or chore's place branch with before
    it is planned (flume 3, 67): in the repository Flume cuts its places in, a bare clone as the runner keeps one or a
    checkout, a branch a dropped place left, and one a live place's worktree holds, each read standing at its commit;
    a name beside it (change/a-b) and a ref below another (change/b/old) are not that branch; and git's own
    `worktree add -b`, Flume's place profile's make, refuses a branch that stands, which is the refusal crew reads ahead
    of. A folder that is no repository exits non-zero, which branches_in refuses with git's words (read.1)."""
    import runner
    repo.commit("chore: start", {"README.md": "r\n"})
    repo.git("branch", "change/a")
    repo.git("checkout", "-q", "change/a")
    kept = repo.commit("feat: work the drop kept", {"a": "a\n"})
    repo.git("checkout", "-q", "main")
    repo.git("branch", "change/a-b")
    repo.git("branch", "change/b/old")
    repo.git("worktree", "add", "-q", "-b", "chore/live", str(tmp_path / "live"))
    live = repo.git("rev-parse", "chore/live")
    subprocess.run(["git", "clone", "-q", "--bare", str(repo.path), str(tmp_path / "clone.git")], check=True)
    wanted = ["change/a", "change/b", "chore/live", "chore/c"]
    for folder in (str(repo.path), str(tmp_path / "clone.git")):
        r = script("BRANCHES", folder, *[f"refs/heads/{b}" for b in wanted])
        assert r.returncode == 0, r.stderr
        assert runner.refs_standing(r.stdout, wanted) == {"change/a": kept, "chore/live": live}
    r = subprocess.run(["git", "-C", str(repo.path), "worktree", "add", "-q", "-b", "change/a", str(tmp_path / "again"), "main"],
                       capture_output=True, text=True)
    assert r.returncode != 0 and "already exists" in r.stderr
    r = script("BRANCHES", str(tmp_path / "nowhere"), "refs/heads/change/a")
    assert r.returncode != 0


class TestTheRunnersClone:
    """drive-state "crew fetches nothing in the runner's clone" (agentplot/boomdrive core.14): a script crew runs in a
    checkout the host's teams file names is told fetch=no (plan.fetch_told), runs no git fetch, so it reads with no remote
    to reach and moves no ref, and reads origin's tracking refs as the runner last fetched them; GitHub moved since is read
    once the runner's own fetch brings it."""

    def run(self, repo, name, *args):
        import plan
        fleet = {"repositories": {"host": "h", "named": {"o/k": {"dir": str(repo.path), "checkout": str(repo.path)}}}}
        text = plan.fetch_told(fleet, "h", str(repo.path), getattr(plan, name))
        assert text.startswith("fetch=no\n")
        return subprocess.run(["bash", "-c", text, "crew", *args], capture_output=True, text=True)

    def refs(self, repo):
        return repo.git("for-each-ref", "--format=%(refname) %(objectname)", "refs/remotes")

    def test_main_now_is_origin_main_as_the_runner_last_fetched_it(self, repo, tmp_path):
        import kit
        repo.commit("main", {"README": "r\n"})
        pushed = kit_with_github(repo, tmp_path)
        last = repo.git("rev-parse", "origin/main")
        pushed("later")
        before = self.refs(repo)
        repo.git("remote", "set-url", "origin", str(tmp_path / "gone.git"))
        r = self.run(repo, "MAIN", str(repo.path))
        assert r.returncode == 0 and "FETCHED=runner" in r.stdout, r.stderr
        assert kit.main_now(r.stdout, "k", "h") == ("origin/main", last, None)
        assert self.refs(repo) == before
        repo.git("remote", "set-url", "origin", str(tmp_path / "github.git"))
        repo.git("fetch", "-q", "origin")  # the runner's own fetch
        assert kit.main_now(self.run(repo, "MAIN", str(repo.path)).stdout, "k", "h") == ("origin/main", github_main(tmp_path), None)
        r = subprocess.run(["bash", "-c", "fetch=maybe\n" + __import__("plan").MAIN, "crew", str(repo.path)], capture_output=True, text=True)
        assert kit.main_now(r.stdout, "k", "h")[2].startswith("cannot fetch k from GitHub on h, so cannot read its main now: crew told "
                                                              "this script fetch=maybe, which is neither yes nor no")

    def test_what_a_tip_carries_is_read_at_the_branches_as_the_runner_last_fetched_them(self, repo, tmp_path):
        import gather
        import kit
        o, other, l214 = two_bolts(repo, tmp_path)
        o("checkout", "-q", "-b", "unit/pop", l214)
        (other / "pop").write_text("one popover\n")
        o("add", "pop"); o("commit", "-qm", "docs(openspec): propose who-can-open-an-app")
        o("checkout", "-q", "-b", "bolt/popover", "origin/bolt/popover")
        o("merge", "-q", "--no-ff", "-m", "chore(land): #216 unit/pop", "unit/pop")
        o("push", "-q", "origin", "bolt/popover")
        head = o("rev-parse", "HEAD")
        repo.git("fetch", "-q", "origin")  # the runner's own fetch
        o("checkout", "-q", "-B", "main", "origin/main")
        o("merge", "-q", "--no-ff", "-m", "chore(land): bolt/deleting", "bolt/deleting")
        o("push", "-q", "origin", "main")
        before = self.refs(repo)

        def carried():
            r = self.run(repo, "CARRIES", str(repo.path), "popover", head, "")
            assert r.returncode == 0, r.stderr
            holds, lines, why = kit.carries_of(r.stdout, "popover")
            assert why is None, why
            return gather.carried_bolts(holds, lines, "popover")
        assert carried() == {"deleting": [l214]}
        assert self.refs(repo) == before
        repo.git("fetch", "-q", "origin")  # the runner's own fetch brings main's landing of deleting
        assert carried() == {}
