"""The guard crew runs crew behind on another host, run by a real `sh` (tests.11): where the host's login path finds no
`crew` it names the host, its first argument, on standard error and exits 127, running nothing; else it execs the crew
it finds with the arguments, whose exit code is its own. What assumes it: `crew.NO_CREW` and `crew_there`, whose line
every command that runs crew on another host runs (crew_argv, reach, read_agent), and found_answer and bash's `there`,
which say the failure as they say any of the command there (read.1)."""
import os
import subprocess

import crew

BOX = "chuck-herdr-alpha"


def guarded(*args):
    """crew_there's argv for the box less its `env …` assignments, so that the scratch PATH need hold no `env`: the
    guard, the host's name and `crew` with its arguments, run by the system's own sh."""
    argv = crew.crew_there(BOX, "swancloud-planner", "wldn", "deneb:s1", list(args))
    assert argv[:2] == ["sh", "-c"] and argv[4] == "env"
    return ["/bin/sh", *argv[1:4], *argv[argv.index("crew"):]]


def run(argv, path):
    return subprocess.run(argv, env={"PATH": str(path)}, capture_output=True, text=True)


def test_a_host_whose_login_path_finds_no_crew_is_named_and_nothing_runs(tmp_path):
    empty = tmp_path / "bin"
    empty.mkdir()
    r = run(guarded("main", "status", "wldn"), empty)
    assert (r.returncode, r.stdout, r.stderr) == (127, "", f"{BOX} has no crew on its login path, so crew can't run there\n")


def test_the_crew_the_login_path_finds_is_run_with_the_arguments_and_its_exit_code_is_its_own(tmp_path):
    path = tmp_path / "bin"
    path.mkdir()
    installed = path / "crew"
    installed.write_text('#!/bin/sh\nprintf \'%s|\' "$@"\nexit 3\n')
    os.chmod(installed, 0o755)
    r = run(guarded("send", "wldn", "words with spaces"), path)
    assert (r.returncode, r.stdout, r.stderr) == (3, "send|wldn|words with spaces|", "")
