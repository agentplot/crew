"""A repository is renamed by one explicit command once its work is finished (a-repository-is-renamed-by-one-explicit-command;
record 0060; plan.22, record.4): crew kit rename <old> <new> renames every record a reader matches the repository by, the
plan's decision-record sources, requests.rec and the run record's entries on the drive's branch, in one commit with its
kit.rename entry (plan.rename_branch, rename_rec), refused while the repository's work stands (rename_standing) or a host
still keeps the old name (rename_kept), naming what stands (rename_refusal). The rename's one commit under a real recfix
is the contract tier's (tests/contract/test_recfix.py)."""
import plan
import runner

from facts import FactsWrite, plan_text

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


def requests(*recs):
    """requests.rec's text holding each request, (n, work, given), as crew writes it (runner.request_fields)."""
    return runner.REQUESTS + "".join("\n" + "\n".join(plan.Rec("Request", runner.request_fields(
        n, "launch", work, given, "2026-11-04T23:00:00Z", "chuck@deneb")).lines()) + "\n" for n, work, given in recs)


def fix_of_main(n, repo, name):
    """A launch of a fix of repo's main, as crew writes it (runner.request_refusal: its submission held)."""
    return (n, f"fix/main/{repo}/{name}", dict(Repo=repo, Kind="fix", Name=name, Base="main", Priority=1, Intent=f"madswan/{name}",
                                               Recipient="madswan/ops", Hold="submission", Brief=f"Fix {name}."))


def entry(n, act, on=(), frm=(), **fields):
    """A run-record entry's text as record.emit writes it, its id the n-th of deneb's on 2026-10-30."""
    lines = [f"Id: 20261030T1000{n:02d}Z-deneb-1-{n}", f"At: 2026-10-30T10:00:{n:02d}Z", "Host: deneb", "By: chuck", f"Act: {act}"]
    lines += [f"On: {o}" for o in on] + [f"From: {o}" for o in frm] + [f"{k}: {v}" for k, v in fields.items()]
    return "\n".join(lines) + "\n"


def runs(*entries):
    """A run-record file's text on the branch: the descriptor, then each entry."""
    return plan.record.DESCRIPTOR + "\n".join(entries)


# madswan's branch before flywheel-cloud is renamed boomdrive-cloud (Task notes 1.2): request 3, a fix of flywheel-cloud's
# main; a runs file holding its landing, its closed landings card and an entry on the fix; a second runs file naming
# nothing of it; a crew unit whose Source names a decision record of flywheel-cloud; and a closed proposal whose Do names it.
SEAM_REQUESTS = requests(fix_of_main(3, "flywheel-cloud", "x"))
DAY = runs(entry(1, "bolt.land", on=["bolt/you-sign-in-to-staging"], Repo="flywheel-cloud", Head="a" * 40),
           entry(2, "card.post", on=["kit/flywheel-cloud"], Card="req_1", Key="land/flywheel-cloud"),
           entry(3, "card.close", on=["land/flywheel-cloud"], Card="req_1", Key="land/flywheel-cloud", State="closed"),
           entry(4, "fix.start", on=["fix/main/flywheel-cloud/x"]))
QUIET = runs(entry(5, "bolt.land", on=["bolt/crew-bolt"], Repo="crew", Head="b" * 40))
PROPOSALS = """\
%rec: Proposal
%key: Proposal

Proposal: 160
State: approved
Do: unit add one-seam "One seam." --repo flywheel-cloud
"""


def madswan_branch():
    text = plan_text(bolts=[("crew-bolt", "crew", False)], units=[("crew-unit", "crew", "crew-bolt", [])])
    text = text.replace("Unit: crew-unit\n", "Unit: crew-unit\nSource: agentplot/flywheel-cloud:docs/adr/0017, the seam\n")
    text = text.replace("Goal: Goal of crew-bolt.", "Goal: crew reads flywheel-cloud's seam.")
    return FactsWrite(text, label="madswan", files={"requests.rec": SEAM_REQUESTS, "runs/deneb/2026-10-30.rec": DAY,
                                                     "runs/deneb/2026-10-31.rec": QUIET, "proposals.rec": PROPOSALS})


class TestWhatTheRenameRenames:
    """Decision 1: rename_branch renames the plan's sources, requests.rec and every run-record file at the tip, and
    replaces only the files it changed."""

    def test_flywheel_cloud_renamed_boomdrive_cloud_across_madswans_records(self):
        w = madswan_branch()
        n = plan.rename_branch(w, "flywheel-cloud", "boomdrive-cloud")
        rq = plan.Plan(w.files["requests.rec"]).recs("Request")[0]
        assert (rq.get("Repo"), rq.get("Work")) == ("boomdrive-cloud", "fix/main/boomdrive-cloud/x")
        day = plan.Plan(w.files["runs/deneb/2026-10-30.rec"]).recs("Entry")
        assert [(e.get("Repo"), e.all("On"), e.get("Key")) for e in day] == [
            ("boomdrive-cloud", ["bolt/you-sign-in-to-staging"], None), (None, ["kit/boomdrive-cloud"], "land/flywheel-cloud"),
            (None, ["land/boomdrive-cloud"], "land/flywheel-cloud"), (None, ["fix/main/boomdrive-cloud/x"], None)]
        assert w.plan.unit("crew-unit").get("Source") == "agentplot/boomdrive-cloud:docs/adr/0017, the seam"
        assert w.plan.bolt("crew-bolt").get("Goal") == "crew reads flywheel-cloud's seam."
        assert (w.files["runs/deneb/2026-10-31.rec"], w.files["proposals.rec"]) == (QUIET, PROPOSALS)
        assert sorted(w.files) == ["proposals.rec", "requests.rec", "runs/deneb/2026-10-30.rec", "runs/deneb/2026-10-31.rec"]
        assert n == 6 and w.renaming == [("flywheel-cloud", "boomdrive-cloud")]

    def test_only_the_files_it_changed_are_replaced(self):
        w = madswan_branch()
        replaced = []
        w.replace = lambda path, text: replaced.append(path)
        plan.rename_branch(w, "flywheel-cloud", "boomdrive-cloud")
        assert replaced == ["requests.rec", "runs/deneb/2026-10-30.rec"]

    def test_a_name_no_record_holds_renames_nothing_and_records_no_rename(self):
        w = madswan_branch()
        text = w.plan.text()
        assert plan.rename_branch(w, "rocs-kit", "rocs") == 0
        assert (w.plan.text(), w.files["requests.rec"], w.files["runs/deneb/2026-10-30.rec"], w.renaming) == (
            text, SEAM_REQUESTS, DAY, [])
