"""No try of crew's call to a remote outlasts its limit (remote-limit; drive-state's stopped fetch and push): the
family's limit and words (boomdrivedev/blueprints design/weir/requirements.md 69 and C.3; weir-bounded; sluice record
0109), which of the state repository's calls are tries, what a stopped fetch and a stopped push refuse, and that every
kit fetch is gather's or FETCH's origin_fetch, each decided on plain facts with no process started."""
import types

import pytest

import crew
import gather
import plan
import record
from crew import Refusal
from facts import FLEET

REACH = record.reach  # the push itself, which conftest stands in for in every case


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


STOPPED_FETCH = ("git fetch with https://github.com/afterthought/crew-state.git was still going after 30s, the most a try "
                 "may take, and was stopped")


class TestAStoppedFetch:
    """drive-state: A stopped fetch of a drive's branch fails the read, at once, never tried again for a lock and never
    read as a branch the repository lacks (read.1)."""

    REPO = "afterthought/crew-state"

    def faked(self, monkeypatch, tmp_path, stderr):
        import plan
        import types
        monkeypatch.setattr(plan, "CACHE", tmp_path)
        monkeypatch.setattr(plan, "READ", plan.Reading())
        monkeypatch.setattr(plan.time, "sleep", lambda s: (_ for _ in ()).throw(AssertionError("a stopped fetch waits for nothing")))
        calls = []

        def git(repo, *args, input=None, env=None, check=True):
            calls.append(args)
            return types.SimpleNamespace(returncode=1, stdout="", stderr=stderr, stopped=True)
        monkeypatch.setattr(plan, "git", git)
        return plan, calls

    def test_a_stopped_fetch_of_one_branch_refuses_once(self, monkeypatch, tmp_path):
        import pytest
        from crew import Refusal
        plan, calls = self.faked(monkeypatch, tmp_path, f"error: cannot lock ref 'refs/crew/madswan/main'; {STOPPED_FETCH}")
        with pytest.raises(Refusal) as e:
            plan.tip_of(self.REPO, "madswan/main")
        assert str(e.value) == (f"could not fetch madswan/main of {self.REPO} over https: error: cannot lock ref "
                                f"'refs/crew/madswan/main'; {STOPPED_FETCH}")
        assert [a[0] for a in calls] == ["fetch"]

    def test_a_stopped_fetch_of_one_branch_is_no_branch_the_repository_lacks(self, monkeypatch, tmp_path):
        import pytest
        from crew import Refusal
        plan, calls = self.faked(monkeypatch, tmp_path, f"fatal: couldn't find remote ref refs/heads/madswan/main; {STOPPED_FETCH}")
        with pytest.raises(Refusal, match="could not fetch madswan/main of afterthought/crew-state over https: .*was stopped"):
            plan.tip_of(self.REPO, "madswan/main")
        assert len(calls) == 1

    def test_a_stopped_fetch_of_several_branches_reads_none_absent(self, monkeypatch, tmp_path):
        import pytest
        from crew import Refusal
        plan, calls = self.faked(monkeypatch, tmp_path, f"fatal: couldn't find remote ref refs/heads/wldn/main; {STOPPED_FETCH}")
        alone = []
        monkeypatch.setattr(plan, "tip_of", lambda *a, **k: alone.append(a))
        with pytest.raises(Refusal) as e:
            plan.tips_of(self.REPO, ["madswan/main", "wldn/main"])
        assert str(e.value) == (f"could not fetch madswan/main, wldn/main of {self.REPO} over https: fatal: couldn't find "
                                f"remote ref refs/heads/wldn/main; {STOPPED_FETCH}")
        assert len(calls) == 1 and alone == []
        assert plan.READ.tip(self.REPO, "madswan/main") is None and plan.READ.tip(self.REPO, "wldn/main") is None


STOPPED_PUSH = ("git push with https://github.com/afterthought/crew-state.git was still going after 30s, the most a try "
                "may take, and was stopped")


class TestAStoppedPush:
    """drive-state: A stopped push fails the write and is never replayed; the next write reads whether it landed, and a
    run-record entry it carried stays on the host for its next push (state.1, plan.1, record.2)."""

    REPO, REF = "afterthought/crew-state", "madswan/main"

    @pytest.fixture
    def branch(self, monkeypatch, tmp_path):
        """The state repository's branch at a, held by the command; a push stops until the case lets it land, and a
        fetch finds the branch at b, the stopped push having landed."""
        monkeypatch.setattr(plan, "CACHE", tmp_path / "cache")
        monkeypatch.setattr(plan, "READ", plan.Reading())
        plan.READ.keep_tip(self.REPO, self.REF, "a" * 40)
        events, made = [], []
        state = {"stops": True}

        def git(repo, *args, input=None, env=None, check=True):
            events.append(args[0])
            if args[0] == "push":
                return (types.SimpleNamespace(returncode=1, stdout="", stderr=STOPPED_PUSH, stopped=True) if state["stops"]
                        else types.SimpleNamespace(returncode=0, stdout="", stderr="", stopped=False))
            if args[0] == "fetch":
                return types.SimpleNamespace(returncode=0, stdout="", stderr="", stopped=False)
            if args[0] == "rev-parse":
                return "b" * 40
            return types.SimpleNamespace(returncode=0, stdout="", stderr="", stopped=False) if not check else ""
        monkeypatch.setattr(plan, "git", git)
        monkeypatch.setattr(plan, "checked", lambda files: None)
        monkeypatch.setattr(plan, "commit", lambda repo, parent, files, message: made.append(parent) or f"c-{parent[:1]}")
        monkeypatch.setattr(plan.time, "sleep", lambda s: events.append(("sleep", s)))
        monkeypatch.setattr("random.random", lambda: 0.5)
        return events, made, state

    def test_a_stopped_push_is_not_replayed(self, branch):
        events, made, state = branch
        tips = []
        with pytest.raises(Refusal) as e:
            plan.land(self.REPO, self.REF, "plan.rec", lambda tip: tips.append(tip) or ("text", "plan: x (crew)"))
        assert str(e.value) == (f"the push of {self.REF} to {self.REPO} failed: {STOPPED_PUSH}; it is not pushed again, and "
                                "the next write reads whether it landed")
        assert tips == ["a" * 40] and made == ["a" * 40]
        assert events == ["push"]

    def test_a_stopped_push_that_landed_is_read_at_the_next_write(self, branch):
        events, made, state = branch
        with pytest.raises(Refusal):
            plan.land(self.REPO, self.REF, "plan.rec", lambda tip: ("text", "plan: x (crew)"))
        events.clear()
        assert plan.tip_of(self.REPO, self.REF) == "b" * 40
        assert events == ["fetch", "rev-parse"]
        state["stops"], tips, made[:] = False, [], []
        plan.land(self.REPO, self.REF, "plan.rec", lambda tip: tips.append(tip) or ("text", "plan: y (crew)"))
        assert tips == ["b" * 40] and made == ["b" * 40]

    def test_an_entry_whose_push_stopped_stays_on_the_host_said_once(self, branch, monkeypatch, tmp_path, capsys):
        events, made, state = branch
        monkeypatch.setattr(record, "ROOT", tmp_path / "crew")
        monkeypatch.setattr(record, "_session", ...)
        monkeypatch.setattr(record, "reach", REACH)
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        monkeypatch.setattr(crew, "load", lambda: FLEET)
        monkeypatch.setenv("CREW_SESSION", "")
        monkeypatch.delenv("CREW_AGENT", raising=False)
        monkeypatch.setattr(plan, "state_of", lambda fleet, label: (self.REPO, f"{label}/main"))
        monkeypatch.setattr(plan, "show", lambda repo, tip, path: None)
        eid = record.emit("madswan", "card.close", ["proposal/170"])
        assert capsys.readouterr().err.splitlines() == [
            f"crew: entry {eid} did not reach {self.REF} of {self.REPO}: the push of {self.REF} to {self.REPO} failed: "
            f"{STOPPED_PUSH}; it is not pushed again, and the next write reads whether it landed; mac-studio keeps it and "
            "pushes it with its next entry"]
        assert events.count("push") == 1 and "fetch" not in events and not any(isinstance(e, tuple) for e in events)
        host = tmp_path / "crew" / "madswan" / "runs" / "mac-studio"
        assert [e["Id"] for e in record.parse(next(host.glob("*.rec")).read_text())] == [eid]


class TestAKitsFetch:
    """remote-limit: A kit's fetch of its origin is a try; the limit and the grace are the family's, set in FETCH once
    each from gather's and read from no setting; every kit fetch is gather's or FETCH's origin_fetch."""

    def test_the_bash_try_takes_gathers_limit_and_grace(self):
        lines = plan.FETCH.splitlines()
        assert lines.count("try_for_ms=30000") == 1 and plan.FETCH.count("try_for_ms=") == 1
        assert lines.count("grace_ms=2000") == 1 and plan.FETCH.count("grace_ms=") == 1
        assert "${try_for_ms" not in plan.FETCH and "${grace_ms" not in plan.FETCH
        assert f"try_for_ms={round(gather.TRY_FOR * 1000)}" in lines and f"grace_ms={round(gather.GRACE * 1000)}" in lines

    def test_no_setting_reaches_the_limit(self):
        import inspect
        import re
        for name, text in [("gather.tried", inspect.getsource(gather.tried)), ("gather.stopped", inspect.getsource(gather.stopped)),
                           ("gather.span", inspect.getsource(gather.span)), ("plan.FETCH", plan.FETCH)]:
            for word in (r"environ", r"getenv", r"\bopen\(", r"teams"):  # open( a file, never Popen(
                assert not re.search(word, text), (name, word)

    def test_no_kit_fetch_through_kit_git_or_gathers_ran(self):
        import pathlib
        import re
        src = pathlib.Path(plan.__file__).read_text()
        assert re.findall(r"kit_git\([^)]*\"fetch\"", src) == []
        here = pathlib.Path(gather.__file__).read_text()
        assert re.findall(r"\bran\(\s*\[[^\]]*\"fetch\"", here) == []
        assert re.findall(r"subprocess\.\w+\(\s*\[[^\]]*\"fetch\"", here) == []
        assert len(re.findall(r"\btried\(\s*\[\"git\", \"fetch\"", here)) == 1  # gather's own fetch, gather.fetched

    def test_no_script_fetches_but_through_fetch(self):
        scripts = {n: v for n, v in vars(plan).items()
                   if n.isupper() and n != "GATHER" and isinstance(v, str) and "git fetch" in v}  # GATHER: gather.py's own text
        assert {"FETCH", "MAINS", "MAIN", "CARRIES", "ORIGIN_FETCH"} <= set(scripts)
        for name, text in scripts.items():
            assert name == "FETCH" or (plan.FETCH in text and "git fetch" not in text.replace(plan.FETCH, "")), name
        assert plan.ORIGIN_FETCH == plan.FETCH + 'cd "$1" || exit 1\norigin_fetch\n'

    def test_the_forecasts_fetch_runs_origin_fetch_on_the_kits_host(self, monkeypatch):
        told, ran = [], []
        monkeypatch.setattr(plan, "kit_git", lambda fleet, t, main, *args, ok=(0,): (0, "") if args[0] == "remote" else 1 / 0)
        monkeypatch.setattr(crew, "fetches_in", lambda fleet, host, main: True)
        monkeypatch.setattr(plan, "fetch_told", lambda fleet, host, main, script: told.append((host, main, script)) or "told")
        monkeypatch.setattr(plan, "host_run", lambda fleet, host, script, *args: ran.append((host, script, *args)) or "")
        t = {"machine": "box", "kit": {"main": "/w/kit/main", "dir": "/w/kit"}}
        assert plan.origin_fetched(FLEET, t, "/w/kit/main") is True
        assert told == [("box", "/w/kit/main", plan.ORIGIN_FETCH)]
        assert ran == [("box", "told", "/w/kit/main")]

    def test_a_kits_stopped_fetch_fails_the_read_naming_its_host(self, monkeypatch):
        words = gather.stopped("git fetch", "origin", 30)
        monkeypatch.setattr(plan, "kit_git", lambda fleet, t, main, *args, ok=(0,): (0, ""))
        monkeypatch.setattr(crew, "fetches_in", lambda fleet, host, main: True)
        monkeypatch.setattr(crew, "on_machine", lambda fleet, host, argv: types.SimpleNamespace(returncode=124, stdout="",
                                                                                                stderr=words + "\n"))
        t = {"machine": "box", "kit": {"main": "/w/kit/main", "dir": "/w/kit"}}
        with pytest.raises(Refusal) as e:
            plan.origin_fetched(FLEET, t, "/w/kit/main")
        assert str(e.value) == f"on box: {words}"
