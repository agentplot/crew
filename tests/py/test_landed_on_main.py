"""A started bolt whose work its kit's main holds reads landed (bolt-teams "A bolt whose work is on its kit's main reads
landed"; a-landed-bolt-is-closed-and-offered-no-more, Decisions 1, 2 and 7): plan.landing_head, the newest head a
landing of the bolt carried since its newest start; plan.main_asks and plan.on_main, whether main holds every piece's
landing commit and that head; plan.main_tip, the kit's main fetched once per command and only handed in to the
follower's read. git's own answers are the contract tier's (tests/contract/test_git.py, TestMainHolds)."""
import pytest

import plan

# boomdrive's a-boomdrive-release-reports-its-own-version on 2026-11-12: its head, the landing commit GitHub's main
# holds for it (second parent the head), and the commit its unit's place landed at on the bolt.
HEAD, LANDED, UNIT = "62d2f06" + "0" * 33, "6cfc4ae" + "0" * 33, "896e642" + "0" * 33


def submit(bolt="y", **f):
    return dict({"Act": "bolt.submit", "On": [f"bolt/{bolt}"]}, **f)


# The two bolt.submit entries an older crew wrote for it: queued as #154 at the head, then stopped at the head with no
# submission, naming a host's checkout gone since the rename.
QUEUED = submit(Outcome="queued", Submission="154", Head=HEAD, At="2026-11-12T00:21:46Z")
STOPPED = submit(Outcome="stopped", Head=HEAD, At="2026-11-12T00:23:43Z",
                 Why="boomdrive's main checkout on deneb has no branch main and no origin")


class TestLandingHead:
    """Decision 1: the Head of the bolt's newest bolt.submit since its newest start naming one, whatever its outcome,
    with the submission or request of the landing still pending (plan.landing_pending)."""

    def test_an_older_crews_queued_then_stopped_landing_gives_its_head_and_submission(self):
        assert plan.landing_head([{"Act": "bolt.start", "On": ["bolt/y"]}, QUEUED, STOPPED], "y") == {
            "head": HEAD, "submission": "154", "request": None}

    def test_a_land_asked_at_a_newer_head_after_a_stop_gives_that_head_and_its_request(self):
        newer = "a1b2c3d" + "0" * 33
        asked = submit(Outcome="asked", Request="57", Head=newer, Card="req_k1")
        assert plan.landing_head([submit(Outcome="stopped", Head=HEAD, Why="stopped"), asked], "y") == {
            "head": newer, "submission": None, "request": "57"}

    def test_entries_before_the_newest_start_are_not_read(self):
        """A bolt's name is free again once it lands: y landed once at HEAD, and was started again since."""
        before = [{"Act": "bolt.start", "On": ["bolt/y"]}, QUEUED, submit(Outcome="landed", Submission="154", Head=HEAD),
                  {"Act": "bolt.land", "On": ["bolt/y"], "Head": LANDED}]
        assert plan.landing_head(before + [{"Act": "bolt.start", "On": ["bolt/y"]}], "y") is None
        assert plan.landing_head(before + [{"Act": "bolt.give", "On": ["bolt/y"]}], "y") is None

    def test_no_bolt_submit_naming_a_head_gives_none(self):
        assert plan.landing_head([], "y") is None
        assert plan.landing_head([submit(Outcome="stopped", Why="no head"), submit("z", Outcome="queued", Head=HEAD)], "y") is None
