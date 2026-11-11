"""No try of crew's call to a remote outlasts its limit (remote-limit; drive-state's stopped fetch and push): the
family's limit and words (agentplot/blueprints design/weir/requirements.md 69 and C.3; weir-bounded; sluice record
0109), which of the state repository's calls are tries, what a stopped fetch and a stopped push refuse, and that every
kit fetch is gather's or FETCH's origin_fetch, each decided on plain facts with no process started."""
import gather


class TestTheFamilysLimit:
    """remote-limit: The limit and the grace are the family's; a stopped try is named with its call, its remote and its
    limit."""

    def test_the_limit_and_grace_are_the_familys(self):
        assert gather.TRY_FOR == 30
        assert gather.GRACE == 2

    def test_a_limit_in_seconds_or_milliseconds(self):
        assert gather.span(30) == "30s"
        assert gather.span(30.0) == "30s"
        assert gather.span(0.3) == "300ms"
        assert gather.span(1.5) == "1500ms"

    def test_a_stopped_trys_words(self):
        assert gather.stopped("git fetch", "origin", 30) == (
            "git fetch with origin was still going after 30s, the most a try may take, and was stopped")

    def test_a_stopped_trys_failure_follows_gits_last_line(self):
        assert gather.stopped("git fetch", "origin", 30, "a\nfatal: x\n") == (
            "fatal: x; git fetch with origin was still going after 30s, the most a try may take, and was stopped")

    def test_nothing_on_standard_error_gives_the_words_alone(self):
        assert gather.stopped("git push", "https://github.com/o/n.git", 0.3, "\n  \n") == (
            "git push with https://github.com/o/n.git was still going after 300ms, the most a try may take, and was stopped")


def fake_cache(monkeypatch, tmp_path):
    """crew's cache of a repo as files, so plan.cache makes none; plan.CACHE under the case's scratch folder."""
    import plan
    (tmp_path / "afterthought/crew-state.git").mkdir(parents=True)
    (tmp_path / "afterthought/crew-state.git/HEAD").write_text("ref: refs/heads/main\n")
    monkeypatch.setattr(plan, "CACHE", tmp_path)


class TestTheStateRepositorysTries:
    """remote-limit: The state repository's calls to its remote are tries; every other call runs to its end."""

    REPO, ADDRESS = "afterthought/crew-state", "https://github.com/afterthought/crew-state.git"

    def faked(self, monkeypatch, tmp_path, answer=(0, "out\n", "", False)):
        import plan
        import subprocess
        import types
        fake_cache(monkeypatch, tmp_path)
        tries, runs = [], []

        def tried(argv, cwd=None, input=None, env=None, limit=None):
            tries.append({"argv": argv, "limit": limit, "input": input})
            return answer

        def run(argv, **kw):
            runs.append(argv)
            return types.SimpleNamespace(returncode=0, stdout="local\n", stderr="")
        monkeypatch.setattr(plan.gather, "tried", tried)
        monkeypatch.setattr(subprocess, "run", run)
        return plan, tries, runs

    def test_a_fetch_a_listing_and_a_push_are_tries(self, monkeypatch, tmp_path):
        plan, tries, runs = self.faked(monkeypatch, tmp_path)
        for args in (("fetch", "--quiet", "--no-tags", self.ADDRESS, "+refs/heads/x:refs/crew/x"),
                     ("ls-remote", "--heads", self.ADDRESS, "refs/heads/x"),
                     ("push", "--quiet", self.ADDRESS, "abc:refs/heads/x")):
            r = plan.git(self.REPO, *args, check=False)
            assert (r.returncode, r.stdout, r.stopped) == (0, "out\n", False)
        assert [t["argv"][3:] for t in tries] == [["fetch", "--quiet", "--no-tags", self.ADDRESS, "+refs/heads/x:refs/crew/x"],
                                                  ["ls-remote", "--heads", self.ADDRESS, "refs/heads/x"],
                                                  ["push", "--quiet", self.ADDRESS, "abc:refs/heads/x"]]
        assert all(t["limit"] == plan.gather.TRY_FOR for t in tries)
        assert runs == []

    def test_the_limit_is_read_at_the_call(self, monkeypatch, tmp_path):
        plan, tries, runs = self.faked(monkeypatch, tmp_path)
        monkeypatch.setattr(plan.gather, "TRY_FOR", 0.3)
        plan.git(self.REPO, "fetch", self.ADDRESS, check=False)
        assert tries[0]["limit"] == 0.3

    def test_a_local_call_runs_to_its_end(self, monkeypatch, tmp_path):
        plan, tries, runs = self.faked(monkeypatch, tmp_path)
        assert plan.git(self.REPO, "rev-parse", "refs/crew/x") == "local"
        assert plan.git(self.REPO, "commit-tree", "t", "-m", "m") == "local"
        assert plan.git(self.REPO, "update-ref", "refs/crew/x", "abc", check=False).stopped is False
        assert [a[3] for a in runs] == ["rev-parse", "commit-tree", "update-ref"]
        assert tries == []

    def test_a_stopped_result_never_reads_exit_0(self, monkeypatch, tmp_path):
        plan, tries, runs = self.faked(monkeypatch, tmp_path, answer=(0, "half an answer\n", "remote: x\n", True))
        r = plan.git(self.REPO, "fetch", "--quiet", self.ADDRESS, "+refs/heads/x:refs/crew/x", check=False)
        assert r.stopped and r.returncode != 0 and r.stdout == ""
        assert r.stderr == (f"remote: x; git fetch with {self.ADDRESS} was still going after 30s, the most a try may take, "
                            "and was stopped")

    def test_check_refuses_a_stopped_call_naming_the_word_the_repository_and_the_failure(self, monkeypatch, tmp_path):
        import pytest
        from crew import Refusal
        plan, tries, runs = self.faked(monkeypatch, tmp_path, answer=(-15, "", "", True))
        with pytest.raises(Refusal) as e:
            plan.git(self.REPO, "push", "--quiet", self.ADDRESS, "abc:refs/heads/x")
        assert str(e.value) == (f"git push in crew's cache of {self.REPO} failed: git push with {self.ADDRESS} was still "
                                "going after 30s, the most a try may take, and was stopped")
