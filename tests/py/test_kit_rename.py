"""A plan an earlier rename left is read as written (plan.22): a plan command given a kit by --repo writes it as
given, through no rename, and says nothing of one (bolt-plan "A command given a kit writes it as given"). And madswan's
started bolt you-sign-in-to-staging, its kit renamed by a rename made before a-repository-is-renamed-by-one-explicit-command,
is read in the folder the runner reports keeping its kit in, as the plan names the kit (Decision 7 of
a-kit-renamed-on-its-host-is-renamed-across-the-plan; runner.where). Each case starts from the plan and the kit.rename
entry an earlier rename left (earlier); the rename itself, crew kit rename, is tests/py/test_repository_rename.py's."""
import argparse
import json
import re

import pytest

import plan
import runner

from facts import FLUME, STANDING, FactsWrite, apply, crew_read, keeping, known, plan_text

# madswan's plan as afterthought/crew-state held it on 2026-11-05 (design's Context): 21 records in tailrace, three bolts
# and eighteen units, one of them queued; the started bolt you-sign-in-to-staging and its merged unit in flywheel-cloud;
# and crew's own.
TAILRACE = [f"trc-{n}" for n in (1, 2, 3)]
STAGING, SEAM = "you-sign-in-to-staging", "one-seam-turns-every-credential-into-a-principal"
UNITS = [(f"tailrace-work-{b}-{n}", "tailrace", b, []) for b in TAILRACE for n in range(1, 7)][:17] + [("trc-queued", "tailrace", None, [])]


def madswan(extra_units=()):
    return plan_text(bolts=[(b, "tailrace", False) for b in TAILRACE] + [(STAGING, "flywheel-cloud", True), ("crew-bolt", "crew", False)],
                     units=UNITS + [(SEAM, "flywheel-cloud", STAGING, []), ("crew-unit", "crew", "crew-bolt", [])] + list(extra_units))


def fleet(*repos):
    """madswan's fleet, its main level on deneb, its folder keeping repos (owner/name) there, as the teams file gives
    them (record 0064)."""
    return {"drives": {"madswan": dict({"label": "madswan", "machine": "deneb", "runs": STANDING}, **keeping("/d/agentplot", *repos))},
            "hosts": {"deneb": {"ssh": "deneb", "kind": "darwin"}}}


@pytest.fixture(autouse=True)
def on_deneb(monkeypatch):
    """crew runs on deneb, madswan's main-level host, so the teams file it reads is deneb's."""
    import crew
    monkeypatch.setattr(crew, "this_host", lambda: "deneb")


# deneb's keeping after the user's rename of 2026-11-05: the new names, and neither old one.
RENAMED = fleet("agentplot/boomdrive", "agentplot/boomdrive-cloud", "agentplot/boomdrive-web", "agentplot/flywheel",
                "agentplot/flywheel-next", "agentplot/timber", "afterthought/crew")

# Request 1, the launch of one-seam in flywheel-cloud, as madswan's requests.rec holds it.
REQUESTS = runner.REQUESTS + "\n" + "\n".join(plan.Rec("Request", runner.request_fields(1, "launch", f"unit/{SEAM}", dict(
    Repo="flywheel-cloud", Kind="change", Name=SEAM, Base=f"bolt/{STAGING}", Priority=1, Intent=f"madswan/{STAGING}",
    Recipient="madswan/planner", Brief=f"Build {SEAM}."), "2026-11-04T23:00:00Z", "chuck@deneb")).lines()) + "\n"


def renamed(old, new):
    """The kit.rename entry crew kit rename <old> <new> left, as record.parse gives it."""
    return {"Id": "20261105T120000Z-1-deneb-1-1", "At": "2026-11-05T12:00:00Z", "Act": "kit.rename", "On": [f"kit/{new}"],
            "From": [f"kit/{old}"], "Commit": [], "Repo": new, "Count": "21"}


def written(text=None, entries=()):
    return FactsWrite(text or madswan(), files={"requests.rec": REQUESTS}, label="madswan", entries=entries)


def earlier(old, new, text=None):
    """madswan's write as a rename made before a-repository-is-renamed-by-one-explicit-command left it: every Bolt and Unit
    record naming old naming new, and its kit.rename entry in the run record."""
    renamed_text = re.sub(rf"^Repo: {re.escape(old)}$", f"Repo: {new}", text or madswan(), flags=re.M)
    return written(renamed_text, entries=[renamed(old, new)])


class TestAKitAsGiven:
    """bolt-plan "A command given a kit writes it as given": a plan command given a kit by --repo writes it as given,
    through no rename, and says nothing of one."""

    def test_a_kit_given_by_repo_is_written_as_given(self, capsys):
        w = written(entries=[renamed("tailrace", "timber")])
        a = plan.do_args("madswan", 'bolt new y "Y is built." --repo tailrace')
        op = plan.OPS[("bolt", "new")](known(w, fleet=RENAMED, n=1), a)
        op.change(w)
        assert op.after is None
        assert w.plan.bolt("y").get("Repo") == "tailrace" and capsys.readouterr().out == ""

    def test_a_chore_given_another_name_of_its_bolts_kit_is_refused(self):
        w = earlier("tailrace", "timber")
        text = w.plan.text()
        with pytest.raises(plan.Refusal, match="^bolt trc-1 is in timber, not tailrace$"):
            apply(w, 'chore add bump "Bump it." --bolt trc-1 --repo tailrace', ctx=known(w, fleet=RENAMED, n=1))
        assert w.plan.text() == text

    def test_a_name_no_rename_renamed_is_written_as_given_and_says_nothing(self, capsys):
        w = written(entries=[renamed("tailrace", "timber")])
        op = plan.OPS[("bolt", "new")](known(w, fleet=RENAMED, n=1), argparse.Namespace(
            bolt="y", goal="Y.", repo="crew", source=[], before=None))
        op.change(w)
        assert w.plan.bolt("y").get("Repo") == "crew" and capsys.readouterr().out == ""


# Where deneb's runner keeps flywheel-cloud's clone, which Flume's status of one-seam's place still names, and the
# folder the clone was renamed to (design's Context; runbook 3.5, step 3).
OLD = "/Users/chuck/.local/share/flywheel/repositories/agentplot/flywheel-cloud"
NEW = "/Users/chuck/.local/share/flywheel/repositories/agentplot/boomdrive-cloud"
PLACE = f"/Users/chuck/.local/share/flume/places/5d2c7e914b0a/change--{SEAM}"
COMMIT = "84393d4" + "0" * 33  # one-seam's landing on bolt/you-sign-in-to-staging, its first seven as read


def deneb(kept=(("agentplot/boomdrive-cloud", NEW), ("agentplot/timber", "/Users/chuck/.local/share/flywheel/repositories/agentplot/timber"))):
    """deneb's runner of madswan as crew reads it (runner.host_read): request 1 answered launched, its place carried once
    Flume tidied it, landed at COMMIT, a flume 0.3.6 status (tests/py/flume-0.3.6/landed.json) naming the old clone's
    folder; and repositories.rec naming each repository it keeps (kept) by its forge address with its folder, as the
    runner reports them once it keeps the renamed clone (R2)."""
    status = json.loads((FLUME / "landed.json").read_text())
    p = status["status"]["places"][0]
    p.update(place=f"{PLACE}@1793474400", repository=OLD, name=SEAM, branch=f"change/{SEAM}", base=f"bolt/{STAGING}",
             stream={"name": "madswan", "from": "intent"})
    p["phase"]["tidied"]["over"]["landed"]["commit"] = COMMIT
    files = {"runner.rec": plan.Plan(runner.RUNNER + "\nHost: deneb\nVersion: 0.1.0\nSince: 2026-11-04T22:00:00Z\n"),
             "answers.rec": plan.Plan(runner.ANSWERS + f"\nRequest: 1\nOutcome: launched\nPlace: {PLACE}\nAt: 2026-11-04T23:01:00Z\n"),
             "places.rec": plan.Plan(runner.PLACES + f"\nRequest: 1\nPlace: {PLACE}\nAt: 2026-11-05T00:23:12Z\nStatus: {json.dumps(status)}\n"),
             "repositories.rec": plan.Plan(runner.REPOSITORIES + "".join(f"\nRepository: {a}\nFolder: {f}\n" for a, f in kept))}
    return {"deneb": runner.host_read("madswan", "deneb", "4a3524e5" + "0" * 32, files, {})}


class TestTheStartedBoltLands:
    """Decision 7: once madswan's plan renames flywheel-cloud boomdrive-cloud and deneb's runner reports the renamed clone,
    you-sign-in-to-staging is read and landed there, its kit as the plan names it, with nothing launched again."""

    @pytest.fixture(autouse=True)
    def here(self, monkeypatch):
        monkeypatch.setattr(plan.crew, "this_host", lambda: "deneb")

    def rows(self, w, run):
        """The rail's land rows (plan.rail_rows) of madswan's plan as the write leaves it, the bolt's head one-seam's landing, green,
        read by deneb in the renamed clone's folder: a survey of any other folder does not hold the kit."""
        k = crew_read(bolts={STAGING: {"head": COMMIT, "head_at": "2026-11-05T00:30:00Z"}})["deneb"]["kits"]["/crew/main"]
        sv = {"deneb": {"ok": True, "kits": {NEW: k}}}
        return [r for r in plan.rail_rows(RENAMED, [("madswan", "afterthought/crew-state", "tip", w.plan)], sv, [], {}, None,
                                          {"madswan": run}) if r["group"] == "land"]

    def test_one_seam_reads_merged_and_the_bolt_lands_in_the_renamed_clone_on_land_boomdrive_cloud(self):
        """request 1, launched under flywheel-cloud, is read as written, the bolt's launches found by its branch;
        one-seam reads merged at 84393d4 from deneb's place, the bolt is read in the folder deneb's runner reports for
        agentplot/boomdrive-cloud over the place's stale one, and it is a row of land/boomdrive-cloud; requests.rec is
        as it was. Started on 2026-11-04 with no launch of bolt/you-sign-in-to-staging, it was started before bolts
        were base places, so its row has no box and says it lands under the crew that started it
        (crew-lands-each-bolt-through-flumes-base-place, Decision 9)."""
        w = earlier("flywheel-cloud", "boomdrive-cloud")
        assert w.files == {"requests.rec": REQUESTS}
        requests = plan.Plan(REQUESTS).recs("Request")
        run = (requests, deneb())
        s = runner.piece_stage(requests, run[1], runner.launch_of(requests, f"unit/{SEAM}"))
        assert (s["stage"], s["commit"]) == ("merged", COMMIT)
        at = plan.bolt_at(RENAMED, "madswan", w.plan.bolt(STAGING), run)
        assert (at["machine"], at["stream"], at["kit"]) == ("deneb", "madswan", {"name": "boomdrive-cloud", "repo": "boomdrive-cloud",
                                                                                 "main": NEW, "dir": NEW})
        rows = self.rows(w, run)
        assert [(r["key"], r["bolts"]) for r in rows] == [("land/boomdrive-cloud", [{"bolt": STAGING, "host": "deneb", "can": False, "head": COMMIT, "stays": False}])]
        assert rows[0]["what"][1] == (f"{STAGING}, on deneb, in Flume stream madswan: {STAGING} was started before bolts were "
                                      "base places and lands under the crew that started it")

    def test_before_the_rename_the_bolt_is_refused_naming_it_and_nothing_lands(self):
        """Decision 7's last step: with the plan still naming flywheel-cloud, deneb's runner reports no repository by it, so
        the bolt is refused naming deneb, what it keeps and crew kit rename, and no row offers it to land."""
        w = written()
        run = (plan.Plan(REQUESTS).recs("Request"), deneb())
        with pytest.raises(plan.Refusal, match=f"^the runner on deneb took bolt {STAGING}'s work and keeps no flywheel-cloud: it keeps "
                                               "agentplot/boomdrive-cloud, agentplot/timber, so crew can't tell where flywheel-cloud is "
                                               "there; if flywheel-cloud was renamed on its host, crew kit rename flywheel-cloud <new>"):
            plan.bolt_at(RENAMED, "madswan", w.plan.bolt(STAGING), run)
        assert self.rows(w, run) == []
