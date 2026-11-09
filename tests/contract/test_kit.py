"""What crew assumes of git when it reads a kit's policy (kit.py, plan.19)."""
import subprocess

import kit


def home(repo, bolt="b"):
    """plan.BOLT_HOME in the kit's main checkout for bolt/<bolt>: what it printed, and kit.bolt_home's read of it."""
    import plan
    r = subprocess.run(["bash", "-c", plan.BOLT_HOME, "crew", str(repo.path), bolt, kit.DECLARATION], capture_output=True,
                       text=True)
    assert r.returncode == 0, r.stderr
    return kit.said_of(r.stdout), kit.bolt_home(r.stdout, bolt)


def test_the_remote_mains_bolts_live_on_is_read_from_the_policy_mains_commit_holds(repo):
    """plan.BOLT_HOME (plan.19), which bolts_local_said runs in a bolt's kit: the remote main's bolt branches live on is
    the one the policy committed on main names, read by git show of main's commit, not the main checkout's files; a main
    with no policy says none, and a bolt whose own commit holds no policy lives on its host (kit.bolt_home)."""
    repo.commit("main", {"README": "r\n"})
    repo.git("branch", "bolt/b")
    assert home(repo) == ({"LOCAL": repo.git("rev-parse", "bolt/b"), "TRACKED": "-", "AT_LOCAL": "-", "AT_TRACKED": "-",
                           "AT_MAIN": "-"}, (None, None))
    text = '[branches."bolt/*"]\nrequired = ["#check-full"]\nremote = "origin"\n'
    repo.commit("chore: policy", {".config/sluice.toml": text})
    (repo.path / ".config" / "sluice.toml").write_text('[branches."bolt/*"]\nrequired = ["#check-full"]\n')
    assert home(repo)[1] == (None, "origin")
