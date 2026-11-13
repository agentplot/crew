"""No try of crew's call to a remote outlasts its limit (remote-limit; drive-state's stopped fetch and push), with real
processes, git and bash: what gather.tried assumes of a process group and its ending, a remote that takes the call and
never answers, and FETCH's bash try on every bash the host has (boomdrivedev/blueprints design/weir/requirements.md 69 and
C.3; weir-bounded; sluice record 0109). Each wait is on a condition with a generous bound (tests.8): a try is said
stopped within twenty seconds, well inside the silent remote's sixty, and a process it started is gone within ten."""
import os
import pathlib
import shutil
import subprocess
import time

import pytest

import gather
from crew import Refusal

TRY = 20.0  # the most a case waits for a try said stopped
GONE = 10.0  # the most a case waits for a process the try started to be gone


def alive(pid):
    """Whether a process is there, as kill -0 reads it."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def gone(pid, within=GONE):
    """Whether a process is gone within a bound, looked at until it is."""
    until = time.monotonic() + within
    while alive(pid):
        if time.monotonic() >= until:
            return False
        time.sleep(0.05)
    return True


def pid_in(path, within=GONE):
    """The process id a command wrote to a file, once it is there."""
    until = time.monotonic() + within
    while not (path.exists() and path.read_text().strip()):
        assert time.monotonic() < until, f"nothing wrote a process id to {path}"
        time.sleep(0.05)
    return int(path.read_text().split()[0])


def timed(*args, **kwargs):
    began = time.monotonic()
    got = gather.tried(*args, **kwargs)
    return got, time.monotonic() - began


class TestATry:
    """remote-limit: A try runs to its limit in a process group of its own; a try that ends within its limit gives its
    exit and all it printed. gather.tried assumes a group outlives its leader while a child of it lives, killpg reaches
    every process of the group, and SIGTERM's trap runs in the grace (weir-bounded's output)."""

    def test_a_process_that_never_ends_is_ended_with_its_group(self, tmp_path):
        pidfile = tmp_path / "sleep.pid"
        (code, out, err, stopped), took = timed(
            ["bash", "-c", f'echo begun; echo said >&2; sleep 60 & echo $! > "{pidfile}"; sleep 60'], limit=0.3)
        assert stopped and took < TRY
        assert out == "begun\n" and err == "said\n"
        assert gone(pid_in(pidfile))

    def test_a_process_asked_to_end_says_so_in_its_grace(self):
        (code, out, err, stopped), took = timed(["bash", "-c", "trap 'echo asked; exit 0' TERM; sleep 60 & wait"], limit=0.3)
        assert stopped and took < TRY
        assert out == "asked\n"

    def test_a_process_that_will_not_end_is_killed(self, tmp_path):
        pidfile = tmp_path / "loop.pid"
        (code, out, err, stopped), took = timed(
            ["bash", "-c", f"trap '' TERM; echo $$ > \"{pidfile}\"; while :; do sleep 0.1; done"], limit=0.3)
        assert stopped
        assert gather.GRACE + 0.3 <= took < TRY
        assert gone(pid_in(pidfile))

    def test_a_child_that_outlives_its_leader_is_ended_at_the_limit(self):
        (code, out, err, stopped), took = timed(["bash", "-c", "sleep 60 >/dev/null 2>&1 </dev/null & echo $!; exit 0"], limit=0.3)
        assert stopped and took < TRY
        assert code == 0
        assert gone(int(out.split()[0]))

    def test_a_process_that_ends_gives_its_exit_and_all_it_printed(self):
        code, out, err, stopped = gather.tried(["bash", "-c", "echo out; echo err >&2; exit 3"], limit=10)
        assert not stopped
        assert (code, out, err) == (3, "out\n", "err\n")

    def test_the_input_the_caller_gives_is_read(self):
        code, out, err, stopped = gather.tried(["cat"], input="asked", limit=10)
        assert not stopped
        assert (code, out) == (0, "asked")

    def test_with_no_input_the_command_reads_nothing(self):
        code, out, err, stopped = gather.tried(["cat"], limit=10)
        assert (code, out, stopped) == (0, "", False)

    def test_a_command_that_cannot_start(self, tmp_path):
        code, out, err, stopped = gather.tried([str(tmp_path / "no-such-command")], limit=10)
        assert (code, out, stopped) == (None, "", False) and err


def silent(tmp_path):
    """weir's silent remote, one that takes the call and never answers, reached with no network: a script git runs as
    its ssh, ssh.variant simple so it runs once with no probe, which writes its process id, one line a call, and then
    becomes a sleep 60. Gives the script's address for core.sshCommand and the file it writes to."""
    script, pids = tmp_path / "silent.sh", tmp_path / "silent.pid"
    script.write_text(f"#!/bin/sh\necho $$ >> '{pids}'\nexec sleep 60\n")
    script.chmod(0o755)
    return f"'{script}'", pids


def calls(pids):
    """The process ids the silent remote wrote, one a call."""
    return [int(l) for l in pids.read_text().split()] if pids.exists() else []


class TestTheStateRepository:
    """drive-state: A stopped fetch of a drive's branch fails the read; a stopped push fails the write and is never
    replayed. The state repository's address, https://github.com/<owner>/<name>.git as plan.url gives it, is turned to
    the silent remote by url.insteadOf in the case's home, and the limit is 300 ms, set on gather for the case: plan.git
    assumes git's remote helper, the ssh it runs, is of the try's process group, so the group's ending ends the call."""

    REPO, REF = "afterthought/crew-state", "madswan/main"
    ADDRESS = "https://github.com/afterthought/crew-state.git"

    @pytest.fixture
    def remote(self, tmp_path, monkeypatch):
        import plan
        ssh, pids = silent(tmp_path)
        home = pathlib.Path(os.environ["HOME"])
        with (home / ".gitconfig").open("a") as f:
            f.write(f'[url "ssh://silent.invalid/"]\n\tinsteadOf = https://github.com/\n[core]\n\tsshCommand = {ssh}\n'
                    "[ssh]\n\tvariant = simple\n")
        monkeypatch.setattr(plan, "CACHE", tmp_path / "cache")
        monkeypatch.setattr(plan, "READ", plan.Reading())
        monkeypatch.setattr(gather, "TRY_FOR", 0.3)
        return plan, pids

    def test_a_state_repository_that_never_answers(self, remote):
        plan, pids = remote
        began = time.monotonic()
        with pytest.raises(Refusal) as e:
            plan.tip_of(self.REPO, self.REF)
        assert time.monotonic() - began < TRY
        said = str(e.value)
        assert said.startswith(f"could not fetch {self.REF} of {self.REPO} over https: ")
        assert said.endswith(f"git fetch with {self.ADDRESS} was still going after 300ms, the most a try may take, and was stopped")
        (pid,) = calls(pids)
        assert gone(pid)

    def test_a_state_repository_that_takes_no_push(self, remote):
        plan, pids = remote
        plan.READ.keep_tip(self.REPO, self.REF, "")  # the branch held as none, so nothing is fetched first
        began = time.monotonic()
        with pytest.raises(Refusal) as e:
            plan.land(self.REPO, self.REF, "plan.rec", lambda tip: (plan.HEADER, "plan: start (crew)"))
        assert time.monotonic() - began < TRY
        said = str(e.value)
        assert said.startswith(f"the push of {self.REF} to {self.REPO} failed: ")
        assert said.endswith(f"git push with {self.ADDRESS} was still going after 300ms, the most a try may take, and was "
                             "stopped; it is not pushed again, and the next write reads whether it landed")
        (pid,) = calls(pids)
        assert gone(pid)


def bashes():
    """Every distinct bash the host has among bash on the path and /bin/bash, a Mac's being 3.2."""
    found = {}
    for b in (shutil.which("bash"), "/bin/bash"):
        if b and os.path.exists(b):
            found.setdefault(os.path.realpath(b), b)
    return list(found.values())


def shortened(script):
    """A script's text with FETCH's limit shortened to 300 ms, the one line that sets it."""
    assert script.count("try_for_ms=30000\n") == 1
    return script.replace("try_for_ms=30000\n", "try_for_ms=300\n")


@pytest.mark.parametrize("bash", bashes())
class TestOriginFetch:
    """remote-limit: A kit's fetch of its origin is a try. FETCH's origin_fetch tries its git fetch through bounded, on
    the host where its git runs, under every bash the host has: MAIN, CARRIES and ORIGIN_FETCH, on a kit whose origin is
    weir's silent remote, ssh://silent.invalid/kit.git with the silent script in the kit's own config, say the stopped
    try in gather.stopped's words, and the call's process is gone. bounded assumes bash gives a job started with job
    control on a process group of its own, inside a command substitution too, and reaps it as it waits."""

    @pytest.fixture
    def kit(self, repo, tmp_path):
        ssh, pids = silent(tmp_path)
        repo.commit("chore: start", {"README.md": "r\n"})
        repo.git("remote", "add", "origin", "ssh://silent.invalid/kit.git")
        repo.git("config", "core.sshCommand", ssh)
        repo.git("config", "ssh.variant", "simple")
        return repo, pids

    def ran(self, bash, script, *args):
        began = time.monotonic()
        r = subprocess.run([bash, "-c", shortened(script), "crew", *args], capture_output=True, text=True, timeout=60)
        return r, time.monotonic() - began

    def words(self):
        return gather.stopped("git fetch", "origin", 0.3)

    def test_main_now_on_an_origin_that_never_answers(self, bash, kit):
        import plan
        repo, pids = kit
        r, took = self.ran(bash, plan.MAIN, str(repo.path))
        assert took < TRY and r.returncode == 0
        assert "ORIGIN=yes" in r.stdout.splitlines()
        assert f"FETCHED={self.words()}" in r.stdout.splitlines()
        (pid,) = calls(pids)
        assert gone(pid)

    def test_what_a_tip_carries_on_an_origin_that_never_answers(self, bash, kit):
        import plan
        repo, pids = kit
        tip = repo.git("rev-parse", "HEAD")
        r, took = self.ran(bash, plan.CARRIES, str(repo.path), "te", tip)
        assert took < TRY and r.returncode == 0
        assert r.stdout.splitlines() == [f"READ={self.words()}"]
        (pid,) = calls(pids)
        assert gone(pid)

    def test_origin_fetch_on_an_origin_that_never_answers(self, bash, kit):
        import plan
        repo, pids = kit
        r, took = self.ran(bash, plan.ORIGIN_FETCH, str(repo.path))
        assert took < TRY
        assert r.returncode != 0 and r.stdout == ""
        assert r.stderr == self.words() + "\n"
        (pid,) = calls(pids)
        assert gone(pid)

    def test_origin_fetch_from_an_origin_that_answers(self, bash, repo, tmp_path):
        import plan
        origin = tmp_path / "origin.git"
        subprocess.run(["git", "init", "-q", "--bare", str(origin)], check=True)
        sha = repo.commit("chore: start", {"README.md": "r\n"})
        repo.git("push", "-q", str(origin), "HEAD:refs/heads/main")
        repo.git("remote", "add", "origin", str(origin))
        r, took = self.ran(bash, plan.ORIGIN_FETCH, str(repo.path))
        assert (r.returncode, r.stdout, r.stderr) == (0, "", "")
        assert repo.git("rev-parse", "refs/remotes/origin/main") == sha


class TestGathersFetch:
    """remote-limit: gather on an origin that never answers. gather.fetched, run on a kit's host by gather's read, is
    one try (gather.tried), and a stopped one is the kit's fetch failure in the family's words, naming origin and the
    limit, 300 ms here, set on gather for the case."""

    def test_gather_on_an_origin_that_never_answers(self, repo, tmp_path, monkeypatch):
        ssh, pids = silent(tmp_path)
        repo.commit("chore: start", {"README.md": "r\n"})
        repo.git("remote", "add", "origin", "ssh://silent.invalid/kit.git")
        repo.git("config", "core.sshCommand", ssh)
        repo.git("config", "ssh.variant", "simple")
        monkeypatch.setattr(gather, "TRY_FOR", 0.3)
        began = time.monotonic()
        said = gather.fetched(str(repo.path))
        assert time.monotonic() - began < TRY
        assert said == "git fetch with origin was still going after 300ms, the most a try may take, and was stopped"
        (pid,) = calls(pids)
        assert gone(pid)
