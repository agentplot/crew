"""A bolt's landing is read from its kit's main (bolt-plan "A bolt's landing is read from its kit's main"; Decision 2 of
a-bolts-landing-on-main-reads-landed): sluice's landing of a bolt on main's first-parent line names bolt/<bolt> in its
Sluice-From, or, landed through a pull request, names `<agent> (pull/<n>)` and has as its second parent the head crew
submitted (sluice clause 23), as swancloud's 4acecf09 did on 2026-11-08; only a landing made at or after the bolt's first
launch is its own. gather.main_landing decides it from main's log as git prints it; plan.landing_sought gives what the
kit's read seeks, from the partition's requests and the run record's bolt.submit entries."""
import gather
import plan

LANDING = "4acecf09" + "0" * 32
BASE = "b45e0000" + "0" * 32
HEAD = "900527e9" + "0" * 32
SINCE = "2026-11-08T10:00:00Z"
AT = 1794153765  # 2026-11-08T16:02:45Z, 4acecf09's committer time


def line(commit, parents, at, *frm):
    """One commit of main's first-parent log as gather.LANDED prints it."""
    return f"{commit}\x1f{' '.join(parents)}\x1f{at}\x1f" + "\x1d".join(frm) + "\x1e\n"


class TestMainLanding:
    def test_a_landing_through_a_pull_request_is_found_by_the_head_crew_submitted(self):
        """bolt-plan "A bolt landed through a pull request, its branch gone": 4acecf09, Sluice-From afterthought-ops
        (pull/377), its second parent 900527e9, the head of x's bolt.submit."""
        log = line("c" * 40, ["d" * 40], AT + 60) + line(LANDING, [BASE, HEAD], AT, "afterthought-ops (pull/377)")
        assert gather.main_landing(log, "x", [HEAD], SINCE) == {"commit": LANDING, "at": "2026-11-08T16:02:45Z", "base": BASE, "head": HEAD}
        assert gather.main_landing(log, "x", [], SINCE) is None

    def test_a_landing_that_names_the_bolts_branch_is_found_with_no_head(self):
        """bolt-plan "A landing that names the bolt's branch": a Flume base place's, bolt/x (bolt/x), and a worktree's,
        ops (bolt/x)."""
        for frm in ("bolt/x (bolt/x)", "ops (bolt/x)"):
            got = gather.main_landing(line(LANDING, [BASE, HEAD], AT, frm), "x", [], SINCE)
            assert (got["commit"], got["base"], got["head"]) == (LANDING, BASE, HEAD)

    def test_a_landing_before_the_bolts_first_launch_is_none_of_its(self):
        """bolt-plan "An earlier bolt of the same name": an x that landed and left the plan."""
        assert gather.main_landing(line(LANDING, [BASE, HEAD], AT, "bolt/x (bolt/x)"), "x", [HEAD], "2026-11-08T17:00:00Z") is None

    def test_a_commit_of_one_parent_is_no_landing(self):
        assert gather.main_landing(line(LANDING, [BASE], AT, "bolt/x (bolt/x)"), "x", [BASE], SINCE) is None

    def test_the_newest_of_two_is_taken(self):
        log = line("e" * 40, [LANDING, "f" * 40], AT + 600, "ops (bolt/x)") + line(LANDING, [BASE, HEAD], AT, "ops (bolt/x)")
        assert gather.main_landing(log, "x", [HEAD], SINCE)["commit"] == "e" * 40

    def test_another_branch_by_a_name_like_the_bolts_is_none_of_its(self):
        log = line(LANDING, [BASE, HEAD], AT, "bolt/xy (bolt/xy)") + line("e" * 40, [BASE, "f" * 40], AT, "change/x (change/x)")
        assert gather.main_landing(log, "x", [], SINCE) is None

    def test_a_since_it_cannot_read_finds_none(self):
        assert gather.main_landing(line(LANDING, [BASE, HEAD], AT, "bolt/x (bolt/x)"), "x", [HEAD], None) is None
