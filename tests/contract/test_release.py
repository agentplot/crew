"""What crew assumes of git when it reads a checkout's version (host-holds-and-updates "A checkout reads each release tag
at the commit it was cut from"): crew.git_version lists the release tags by version with for-each-ref, peels each to
its commit, reads each commit's parents and subject with one git log, and takes the newest whose source, a release
commit's parent or else the tag's own commit, merge-base finds HEAD at or after, counting the commits past it with
rev-list. The history is the one CI's release job makes: a release commit cut from main's pushed commit, detached,
committed `chore(release): <tag>` and tagged, main moving on past it, and an older tag on main's own commit."""
import json

import pytest

import crew


@pytest.fixture
def history(repo):
    """Main A, P, P+1, P+2: v0.55.0 an annotated tag on A, as a release made before crew's release commits names main's
    own commit; v0.56.0 a lightweight tag on R, the release commit cut from P that writes plugin/release.json as
    set-version.sh does; and v9.9, a tag of v's that names no release, on main's tip."""
    a = repo.commit("feat: a", {"plugin/release.json": json.dumps({"version": "0.0.0"}) + "\n"})
    repo.git("tag", "-a", "-m", "v0.55.0", "v0.55.0", a)
    p = repo.commit("feat: p")
    repo.git("checkout", "-q", "--detach", p)
    r = repo.commit("chore(release): v0.56.0", {"plugin/release.json": json.dumps({"version": "0.56.0"}) + "\n"})
    repo.git("tag", "v0.56.0", r)
    repo.git("checkout", "-q", "main")
    repo.commit("fix: one past p")
    tip = repo.commit("feat: two past p")
    repo.git("tag", "v9.9", tip)
    return {"A": a, "P": p, "R": r, "tip": tip}


def at(repo, commit):
    repo.git("checkout", "-q", "--detach", commit)
    return crew.git_version(str(repo.path))


def test_main_past_a_release_reads_the_tag_and_the_commits_past_its_source(repo, history):
    """crew.git_version: git log's %P names the release commit's parent, and rev-list counts from it, not from the tag."""
    assert crew.git_version(str(repo.path)) == (history["tip"], "v0.56.0+2")


def test_main_at_the_commit_a_release_was_cut_from_reads_the_tag(repo, history):
    """crew.git_version: merge-base --is-ancestor holds for a commit and itself, and rev-list counts nothing."""
    assert at(repo, history["P"]) == (history["P"], "v0.56.0")


def test_a_checkout_of_the_tag_reads_the_tag(repo, history):
    """crew.git_version: for-each-ref gives a lightweight tag's commit as its objectname."""
    assert at(repo, history["R"]) == (history["R"], "v0.56.0")


def test_a_branch_past_a_tag_on_mains_own_commit_reads_that_tag(repo, history):
    """crew.git_version: --sort=-v:refname lists v0.56.0 first, merge-base finds its source no ancestor of the branch,
    and v0.55.0, an annotated tag, is peeled by %(*objectname) to the commit it names."""
    repo.git("checkout", "-q", "-b", "side", history["A"])
    head = [repo.commit(f"feat: side {n}") for n in range(3)][-1]
    assert crew.git_version(str(repo.path)) == (head, "v0.55.0+3")


def test_a_checkout_with_no_release_tag_reads_its_commit_and_no_version(repo):
    """crew.git_version: for-each-ref lists nothing, and HEAD's commit is still read."""
    head = repo.commit("feat: a")
    repo.git("tag", "v1.0", head)
    assert crew.git_version(str(repo.path)) == (head, None)
