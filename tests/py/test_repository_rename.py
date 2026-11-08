"""A repository is renamed by one explicit command once its work is finished (a-repository-is-renamed-by-one-explicit-command;
record 0060; plan.22, record.4): crew kit rename <old> <new> renames every record a reader matches the repository by, the
plan's decision-record sources, requests.rec and the run record's entries on the drive's branch, in one commit with its
kit.rename entry (plan.rename_branch, rename_rec), refused while the repository's work stands (rename_standing) or a host
still keeps the old name (rename_kept), naming what stands (rename_refusal). The rename's one commit under a real recfix
is the contract tier's (tests/contract/test_recfix.py)."""
import plan

KIT_RENAME = """\
Id: 20261105T120000Z-1-deneb-1-1
At: 2026-11-05T12:00:00Z
Host: deneb
By: chuck
Act: kit.rename
On: kit/timber
From: kit/tailrace
Repo: timber
Count: 21
"""


class TestWhatAFieldBecomes:
    """Decision 1: each field a reader matches a repository by, renamed in its form; everything else as written."""

    def test_each_object_built_on_the_name_takes_the_new_name(self):
        for was, now in [("kit/tailrace", "kit/timber"), ("land/tailrace", "land/timber"), ("queue/tailrace", "queue/timber"),
                         ("record/tailrace/0017", "record/timber/0017"), ("fix/main/tailrace/cargo-lock", "fix/main/timber/cargo-lock")]:
            assert plan.renamed_object(was, "tailrace", "timber") == now
            assert plan.renamed_field("On", was, "tailrace", "timber") == now
            assert plan.renamed_object(was, "agentplot/tailrace", "agentplot/timber") == now

    def test_a_forge_address_keeps_its_owner_unless_the_new_name_is_an_address(self):
        assert plan.renamed_kit("agentplot/flywheel-cloud", "flywheel-cloud", "boomdrive-cloud") == "agentplot/boomdrive-cloud"
        assert plan.renamed_kit("flywheel-cloud", "flywheel-cloud", "boomdrive-cloud") == "boomdrive-cloud"
        assert plan.renamed_kit("agentplot/flywheel-cloud", "flywheel-cloud", "madswan/boomdrive-cloud") == "madswan/boomdrive-cloud"
        assert plan.renamed_kit("flywheel-cloud", "agentplot/flywheel-cloud", "agentplot/boomdrive-cloud") == "agentplot/boomdrive-cloud"
        assert plan.renamed_field("Repo", "agentplot/flywheel-cloud", "flywheel-cloud", "boomdrive-cloud") == "agentplot/boomdrive-cloud"

    def test_an_object_of_another_repository_is_as_it_was(self):
        for obj in ("kit/tailrace-web", "land/tailrace-web", "record/tailrace-web/0017", "fix/main/tailrace-web/x", "unit/tailrace",
                    "bolt/tailrace", "proposal/170"):
            assert plan.renamed_object(obj, "tailrace", "timber") == obj
        assert plan.renamed_kit("tailrace-web", "tailrace", "timber") == "tailrace-web"

    def test_a_sources_decision_record_is_renamed_and_its_words_kept(self):
        source = "agentplot/flywheel-cloud:docs/adr/0017 (the seam), as agentplot/crew:docs/adr/0060 rules"
        assert plan.renamed_field("Source", source, "flywheel-cloud", "boomdrive-cloud") == \
            "agentplot/boomdrive-cloud:docs/adr/0017 (the seam), as agentplot/crew:docs/adr/0060 rules"
        for words in ("flywheel-cloud's seam, as the user said", "signals/2026-11-07-agentplot-planner-cbc41169/01"):
            assert plan.renamed_source(words, "flywheel-cloud", "boomdrive-cloud") == words

    def test_a_key_and_any_other_field_is_as_it_was(self):
        assert plan.renamed_field("Key", "land/tailrace", "tailrace", "timber") == "land/tailrace"
        assert plan.renamed_field("Goal", "tailrace is built", "tailrace", "timber") == "tailrace is built"

    def test_a_kit_rename_entry_is_left_whole(self):
        text = plan.record.DESCRIPTOR + KIT_RENAME
        assert plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "timber", "trc") == (text, 0)
        assert plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "tailrace", "trc") == (text, 0)

    def test_a_text_naming_no_old_name_is_returned_byte_for_byte(self):
        text = plan.record.DESCRIPTOR + "Id: 1\nAt: 2026-11-05T12:00:00Z\nAct: bolt.land\nOn: bolt/crew-bolt\nRepo:  crew\n\n\n# a comment\n"
        assert plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "tailrace", "timber") == (text, 0)

    def test_a_record_is_renamed_field_by_field_and_counted_once(self):
        text = (plan.record.DESCRIPTOR + "Id: 1\nAct: card.post\nOn: kit/tailrace\nOn: land/tailrace\nKey: land/tailrace\nWhy: tailrace\n\n"
                + KIT_RENAME + "\nId: 3\nAct: bolt.land\nRepo: agentplot/tailrace\n")
        renamed, n = plan.rename_rec(text, plan.RENAMED_FIELDS["runs/"], "tailrace", "timber")
        assert n == 2
        assert renamed == (plan.record.DESCRIPTOR + "Id: 1\nAct: card.post\nOn: kit/timber\nOn: land/timber\nKey: land/tailrace\nWhy: tailrace\n\n"
                           + KIT_RENAME + "\nId: 3\nAct: bolt.land\nRepo: agentplot/timber\n")
