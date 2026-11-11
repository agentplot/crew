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
