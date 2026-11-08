"""What crew assumes of git when it reads a kit's policy (kit.py, plan.19)."""
import subprocess

import kit


def test_the_remote_a_bolt_lives_on_is_read_from_the_policy_main_holds(repo):
    """plan.POLICY (plan.19): the remote a bolt lives on is the one the policy committed on main names, read by git show
    of main's commit, not the main checkout's files (kit.bolt_remote)."""
    import plan
    text = '[branches."bolt/*"]\nrequired = ["#check-full"]\nremote = "origin"\n'
    repo.commit("chore: policy", {".config/sluice.toml": text})
    (repo.path / ".config" / "sluice.toml").write_text('[branches."bolt/*"]\nrequired = ["#check-full"]\n')
    r = subprocess.run(["bash", "-c", plan.POLICY, "crew", str(repo.path), kit.DECLARATION], capture_output=True, text=True)
    said, ref, _ = kit.policy_said(r.stdout, "k", "h")
    assert (ref, kit.bolt_remote(said, "bolt/b")) == ("main", "origin")
