"""What crew assumes of its own toolchain, each case naming what assumes it: tests/suite runs crew's tasks (`moon exec`,
the `check-full` tag) with the moon crew's .prototools pins, crew's own choice (record 0023, point 5), installed by
proto under crew's own proto home in the git common dir (devenv.nix), never a moon of the user's; and crew's tests run
on Python 3.13, the minor every host runs crew on (code.1), with pytest synced from tests/pyproject.toml. Each run of
crew's tools through the shell, `devenv shell -- <command>`, gets the same (tests.7, record 0024). The toolchain crew's
policy names (.config/sluice.toml) only activates: the script it prints installs nothing. The flake's checks are the
moon project nix's four tasks, each tagged check-full, which tests/suite and sluice's #check-full select; they run the
nix, nixfmt, statix and deadnix the shell carries, and read the flake's inputs where the shell fetched them, by
CREW_FLAKE_INPUTS, with no network (flake.3, nix/moon.yml, nix/check.sh)."""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tomllib


def test_the_tests_run_on_the_python_minor_every_host_runs_crew_on_with_pytest():
    import pytest  # noqa: F401, the tests' own runner, from tests/pyproject.toml
    assert sys.version_info[:2] == (3, 13)


def test_moon_is_protos_from_crews_own_home_at_the_version_prototools_pins():
    moon, home = shutil.which("moon"), os.environ.get("PROTO_HOME", "")
    assert home and moon and moon.startswith(home + os.sep), f"moon is {moon}, not proto's under crew's own home {home}"
    prototools = pathlib.Path(__file__).resolve().parents[2] / ".prototools"
    pin = re.search(r'^moon = "([^"]+)"', prototools.read_text(), re.M).group(1)
    said = subprocess.run([moon, "--version"], capture_output=True, text=True).stdout
    assert said.strip() == f"moon {pin}", f"crew's toolchain runs {said.strip()}, and .prototools pins moon {pin}"


def test_the_toolchain_crews_policy_names_only_activates():
    """sluice's equip and Flume's readiness source the script this prints, sluice's inside its executor (sluice 147,
    C.2), and the kit standard's toolchain.8 says sourcing it installs nothing: devenv.nix's enterShell only activates,
    and its task crew:proto:install, which the script leaves out, installs a missing pin."""
    root = pathlib.Path(__file__).resolve().parents[2]
    toolchain = tomllib.loads((root / ".config/sluice.toml").read_text())["tests"]["toolchain"]
    script = subprocess.run(toolchain, cwd=root, capture_output=True, text=True, check=True, timeout=600).stdout
    assert "proto activate" in script, f"`{' '.join(toolchain)}` prints a script that activates no proto pin"
    installs = [line.strip() for line in script.splitlines() if "proto install" in line]
    assert not installs, f"`{' '.join(toolchain)}` prints a script that runs proto install: {installs}"


def test_the_shell_carries_the_flakes_tools_and_gives_its_inputs_store_paths():
    """nix/moon.yml's format, lint, typecheck and test run nixfmt, statix, deadnix and nix from the shell, never the
    host's; nix/check.sh reads each input of flake.lock from CREW_FLAKE_INPUTS, offline and against no store, so each
    must name a path the shell fetched (flake.3, nix/inputs.nix)."""
    for tool in ("nix", "nixfmt", "statix", "deadnix"):
        found = shutil.which(tool)
        assert found and found.startswith("/nix/store/"), f"{tool} is {found}, not the shell's from the Nix store"
    root = pathlib.Path(__file__).resolve().parents[2]
    lock = json.loads((root / "flake.lock").read_text())
    nodes = sorted(n for n in lock["nodes"] if n != lock["root"])
    given = os.environ.get("CREW_FLAKE_INPUTS")
    assert given, "the shell gives no CREW_FLAKE_INPUTS"
    paths = json.loads(given)
    assert sorted(paths) == nodes, f"CREW_FLAKE_INPUTS names {sorted(paths)}, and flake.lock locks {nodes}"
    for name, path in paths.items():
        assert path.startswith("/nix/store/") and os.path.isdir(path), f"CREW_FLAKE_INPUTS gives {name} {path}, which is no fetched source"


def test_moon_gives_the_project_nix_its_four_checks_each_tagged_check_full():
    """tests/suite with no name runs `:#check-full`, and sluice's #check-full resolves to every project's check-full
    tasks, so the flake's checks gate a change only while moon, in crew's checkout, gives the project nix format, lint,
    typecheck and test, each tagged check-full (flake.3, tests.5)."""
    root = pathlib.Path(__file__).resolve().parents[2]
    # moon reads MOON_* as options, and a moon task hands its own to this test: only crew's moon home goes through.
    env = {k: v for k, v in os.environ.items() if not k.startswith("MOON_") or k == "MOON_HOME"}
    r = subprocess.run(["moon", "query", "tasks", "--project", "nix"], cwd=root, env=env, capture_output=True,
                       text=True, stdin=subprocess.DEVNULL, timeout=600)
    assert r.returncode == 0, f"moon query tasks --project nix exited {r.returncode}: {r.stderr}"
    tasks = json.loads(r.stdout).get("tasks", {}).get("nix", {})
    tagged = {name: task.get("tags") or [] for name, task in tasks.items()}
    assert sorted(tagged) == ["format", "lint", "test", "typecheck"], f"moon gives the project nix {sorted(tagged)}"
    untagged = [name for name, tags in sorted(tagged.items()) if "check-full" not in tags]
    assert not untagged, f"the project nix's {untagged} carry no check-full tag"
