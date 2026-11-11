"""No try of crew's call to a remote outlasts its limit (remote-limit; drive-state's stopped fetch and push), with real
processes, git and bash: what gather.tried assumes of a process group and its ending, a remote that takes the call and
never answers, and FETCH's bash try on every bash the host has (agentplot/blueprints design/weir/requirements.md 69 and
C.3; weir-bounded; sluice record 0109). Each wait is on a condition with a generous bound (tests.8): a try is said
stopped within twenty seconds, well inside the silent remote's sixty, and a process it started is gone within ten."""
import os
import time

import gather

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
