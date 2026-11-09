"""Facts for the logic tier, built as crew's readers return them, so a case reads as its scenario."""
import hashlib

ALICE = ("Alice", "alice@example.com")


def commit(subject, author=ALICE, body="", sha=None):
    """A commit as plan.commits_beyond reads it: sha, short sha, subject, and who (author name, email, message).
    Two commits with the same subject, author and body are the same commit replayed; give each its own sha."""
    message = subject + ("\n\n" + body if body else "") + "\n"
    sha = sha or hashlib.sha1(f"{subject}{author}{body}{id(message)}".encode()).hexdigest()
    return {"sha": sha, "short": sha[:7], "subject": subject, "who": (author[0], author[1], message)}


def replayed(c, subject=None, author=None):
    """The commit replayed with a new sha: the same message and author unless reworded or re-authored."""
    return commit(subject or c["subject"], author or c["who"][:2])


import datetime
import pathlib

START = datetime.datetime(2026, 10, 12, 10, 0, 0, tzinfo=datetime.timezone.utc)
BEFORE, AFTER = START - datetime.timedelta(minutes=1), START + datetime.timedelta(minutes=1)


def saved(name):
    """A report or proof file saved since the stage began, as newest_saved returns it."""
    return pathlib.Path("/reports") / name


def plan_of(bolts=None, units=None):
    """A plan.rec as plan.Plan reads it: bolts as {bolt: started or not}, a started one marked Path: flume, units as
    {unit: bolt or None}, in order."""
    import plan
    text = "%rec: Bolt\n\n" + "".join(f"Bolt: {b}\n" + ("Path: flume\n" if t else "") + "\n" for b, t in (bolts or {}).items())
    text += "%rec: Unit\n\n" + "".join(f"Unit: {u}\n" + (f"Bolt: {b}\n" if b else "") + "\n" for u, b in (units or {}).items())
    return plan.Plan(text)


def at(minutes):
    """A run-record time, minutes after START."""
    return (START + datetime.timedelta(minutes=minutes)).strftime("%Y-%m-%dT%H:%M:%SZ")


def constructed(unit, sha, minutes=0):
    """A run-record entry: unit's construct delivered its change at sha."""
    return {"Act": "stage.end", "Ended": "delivered", "On": [f"stage/{unit}/construct", f"unit/{unit}"],
            "Delivered": f"unit/{unit}@{sha}", "At": at(minutes)}


def reviewed(n, units, minutes=0):
    """A run-record entry: batch n delivered, holding each (unit, its bolt, sha), as review.batch names it, or, in an entry
    written before, its team (units_of_batch reads the middle name as written)."""
    return {"Act": "review.batch", "Batch": str(n), "Units": " ".join(f"{u}:{t}@{s}" for u, t, s in units), "At": at(minutes), "On": []}


def card_closed(key, card, minutes=0, state="closed", refused=None):
    """A run-record entry: the card under key closed, as crew records it once the user answered it ("closed"), sent its
    reading session ("withdrawn"), or as Pending You lost it to its owner ("lost"); refused, a close Pending You refused."""
    return {"Act": "card.close", "Key": key, "Card": card, "State": None if refused else state, "Refused": refused, "At": at(minutes),
            "On": [key]}


def told(minutes=0):
    """A run-record entry: the planner was told a batch is due."""
    return {"Act": "batch.due", "At": at(minutes), "On": []}


def keeping(at, *repos):
    """A drive's keeping as the teams file gives it (record 0064): its herdr session's folder at, keeping each repository
    (owner/name) it lists in its `repos`, each kit's main checkout at <at>/<name>/main, where crew acts on a kit no
    runner has taken work of (crew.kit_kept, plan.main_kit). Merged into a drive's entry."""
    return {"folder": at, "repos": list(repos)}


def kept_by(fleet, label, at, *repos):
    """fleet with drive label's folder at, keeping repos there (keeping)."""
    return dict(fleet, drives=dict(fleet["drives"], **{label: dict(fleet["drives"][label], **keeping(at, *repos))}))


# The hosts crew reaches, as the teams file's `hosts` gives them: each by its name, its ssh name the same.
HOSTS = {"mac-studio": {"ssh": "mac-studio", "kind": "darwin"}, "deneb": {"ssh": "deneb", "kind": "darwin"},
         "chuck-herdr-alpha": {"ssh": "chuck-herdr-alpha", "kind": "nixos"}}
# Every role of a drive stands, its flume false throughout.
STANDING = {r: False for r in ("design", "planner", "reviewer", "ops", "operator")}
# The teams file at version 6 as crew.load reads it: wldn's main level runs on mac-studio, its folder /w keeping its
# kits, every role on account madswan.
FLEET = {"drives": {"wldn": dict({"label": "wldn", "machine": "mac-studio", "review": {"every": 5, "hours": 4}, "flume": STANDING,
                                  "accounts": {r: "madswan" for r in STANDING}},
                                 **keeping("/w", "WilldanGroup/atlas-kit", "WilldanGroup/breadboard-kit", "WilldanGroup/switchboard-kit"))},
         "hosts": {"mac-studio": HOSTS["mac-studio"]}, "consoles": {}}


KITS = ("switchboard-kit", "breadboard-kit")


def kits_of(found):
    """Each drive's kits as the rail's read holds them (plan.kits_at), from its plan alone, a read's found as
    plan.plans gives it: a case that needs a kit its landings name gives it itself."""
    import plan
    return {l: plan.drive_kits(p, []) for l, _, _, p in found}


def plan_text(bolts=(), units=()):
    """plan.rec text with its descriptors: bolts as (name, repo, started), a started one marked Path: flume, units as
    (name, repo, bolt or None, [after...]), in order, a fifth "chore" making it a chore, whose words are "Chore <name>."."""
    text = "%rec: Bolt\n%key: Bolt\n\n" + "".join(
        f"Bolt: {b}\nRepo: {r}\nGoal: Goal of {b}.\n" + ("Path: flume\n" if t else "") + "\n" for b, r, t in bolts)
    text += "%rec: Unit\n%key: Unit\n\n" + "".join(
        f"Unit: {u}\nRepo: {r}\n" + (f"Bolt: {b}\n" if b else "") + ("Kind: chore\n" if kind else "")
        + (f"Intent: Chore {u}.\n" if kind else f"Intent: Unit {u}.\n") + "".join(f"After: {x}\n" for x in after) + "\n"
        for u, r, b, after, *kind in units)
    return text


class FactsWrite:
    """A plan.Write over a plan in memory: its files given, which it lists (paths) and reads (texts) as the branch's at
    its tip, each host's runner as given (runners, {host: its reading as runner.host_read gives it}), the run record at
    its tip as given (entries, oldest first, none unless given; logged, which a case may set after), the drive's
    kits read from those entries, and a refusal for a missing bolt or unit that reads no git for the commit that removed
    it."""

    def __new__(cls, text, files=None, runners=None, label="wldn", entries=()):
        import plan
        import runner

        class W(plan.Write):
            def text(self, path):
                return self.files.get(path)

            def paths(self, prefix):
                return sorted(p for p in self.files if p.startswith(prefix))

            def texts(self, paths):
                return [self.files.get(p) for p in paths]

            def gone(self, kind, name, word=None):
                plan.fail(f"no {word or kind.lower()} {name} in {self.label}/main")

            def runners(self):
                return dict(runners or {})

            def entries(self):
                return list(self.logged)

            def kits(self):
                return plan.drive_kits(self.plan, self.logged)
        w = W(None, label, None, plan.Plan(text))
        w.files, w.logged = dict(files or {}), list(entries)
        return w


def writes_at(monkeypatch, tip, text="%rec: Bolt\n\n%rec: Unit\n\n", label="swancloud"):
    """plan.write stood in for by a write applied to a tip in memory: each change applied to a FactsWrite over text,
    whose run record is tip (a list, oldest first, that each write's entries join, so a later write is applied to the
    tip an earlier one left), a change that raises plan.Unposted writing nothing; each write's entries, its act's and
    each also, as record.parse gives them with a refusal as refused and a Why as why, appended to the list returned."""
    import plan
    written = []

    def write(fleet, label_, change, subject, body="", act=None, on=(), frm=(), fields=None, by=None, why=None):
        w = FactsWrite(text, label=label, entries=list(tip))
        change(w)
        es = [dict({**(fields or {}), **w.fields}, Act=w.act or act, On=list(on) + w.on, by=by, why=w.why or why)]
        es += [dict({k: v for k, v in more.items() if k != "why"}, Act=a, On=list(o), by=by, why=more.get("why") or w.why or why)
               for _, a, o, more in w.also]
        for e in es:
            tip.append(dict({k: v for k, v in e.items() if k not in ("refused", "why", "by")},
                            **({"Refused": e["refused"]} if e.get("refused") else {}), **({"Why": e["why"]} if e.get("why") else {})))
        written.extend(es)
        return "c" * 40
    monkeypatch.setattr(plan, "write", write)
    return written


def known(w, stages=None, taken=(), n=None, chores_taken=(), fleet=None, standing=()):
    """A plan command's reads as a logic case gives them (plan.Reads): each unit's or chore's stage as given, else ready;
    a name free unless the kit's main holds a change (taken) or a chore (chores_taken) by it, or Flume's branch for it
    stands in a repository a launch of it would be made in (standing, as runner.branch_refusal takes them: [{"host",
    "dir", "refs": {branch: commit}}]); work a held bolt needs ahead of its first unit or chore not merged."""
    import plan
    import runner

    class Known(plan.Proposed):
        direct = n is None

        def of(self, name):
            st = (stages or {}).get(name, "ready")
            return {"stage": st, "worktree": f"/kit/places/{name}" if st not in ("ready", "waiting", "unknown") else None,
                    "open": [], "head": None, "why": "its host did not answer" if st == "unknown" else None}

        def stages(self, label, p, bolts):
            return self

        def stage(self, label, p, name):
            return self.of(name)

        def free(self, label, kit, names, kind="unit"):
            for x in names:  # by the decision name_free makes, on the changes and chores the kit's main is given to hold
                why = plan.name_taken(kit, x, taken, chores_taken)
                not why or plan.fail(why)
            why = runner.branch_refusal(kit, kind, names, list(standing))  # and branch_free's, on the branches given
            not why or plan.fail(why)

        def first_open(self, label, p, bolt):
            return next((u.name() for u in p.work_of(bolt) if self.of(u.name())["stage"] not in ("merged", "landed")), None)

        def kit(self, kit):  # the drive the command runs as, as plan.plan_for has it given a label
            return self.label
    return Known(fleet or FLEET, w.label, w, n)


def apply(w, *dos, ctx=None):
    """Each Do line, as a proposal holds it, built and applied in order to the write's plan, then crew's own rules
    checked: what plan.apply_all and check_ops do, without recfix's process."""
    import plan
    for do in dos:
        a = plan.do_args(w.label, do)
        plan.OPS[(a.cmd, a.sub)](ctx or known(w, n=1), a).change(w)
    plan.check(w.plan)
    return w


def units_of(w, bolt=None, repo=None):
    """The plan's units and chores in a bolt, or in a repo's queue, in order."""
    return [u.name() for u in w.plan.work() if (u.get("Bolt") == bolt if bolt else not u.get("Bolt") and u.get("Repo") == repo)]


CREW_KIT = {"name": "crew", "repo": "afterthought/crew"}


def madswan_fleet():
    """madswan's fleet as crew.load reads it, its main level on deneb, whose runner takes crew's work (afterthought/crew)
    in stream madswan, as ran reports it."""
    return {"drives": {"madswan": {"label": "madswan", "machine": "deneb"}}, "hosts": {}}


# Where madswan's started bolts of crew run, as plan.bolt_at gives it from the runner's report (ran): deneb, stream
# madswan, crew's folder there, which a kit read there (crew_read) says what main and a bolt hold of.
CREW_AT = {"label": "madswan", "machine": "deneb", "stream": "madswan", "kit": dict(CREW_KIT, main="/crew/main", dir="/crew")}


# The commit flume-0.3.6/landed.json's place landed, so a bolt whose head it is and whose pieces stand landed there
# reads green: its head is its work's landing, as the runner reports it (runner.verification).
LANDED = "d185a879b51dba33555c036392b50443f4dfc5e8"


def crew_read(main=(), chores=(), bolts=None):
    """A survey of deneb (plan.survey's answer) holding crew's kit as read there: main's changes and chores, and each
    bolt in bolts, {bolt: its facts over a bolt holding nothing yet, its head LANDED}."""
    empty = {"exists": True, "at": "origin/bolt/x", "changes": [], "archived": [], "open": {}, "chores": [], "worktree": None,
             "head": LANDED, "head_at": "2026-10-31T12:00:00Z"}
    k = {"ok": True, "main": list(main), "chores": list(chores), "places": {}, "chore_places": {}, "fixes": [],
         "bolts": {b: dict(empty, at=f"origin/bolt/{b}", **facts) for b, facts in (bolts or {}).items()}}
    return {"deneb": {"ok": True, "kits": {"/crew/main": k}}}


def flume_plan(bolts=(), work=()):
    """madswan's plan.rec text, every bolt and piece of work in crew: bolts as (name, started, Path or None), a started
    one marked Path: flume, work as (name, bolt or None, [after], kind, [sources]), kind "chore" or "unit", each in
    order and intended `Build <name>.`."""
    out = "%rec: Bolt\n%key: Bolt\n\n" + "".join(
        f"Bolt: {b}\nRepo: crew\nGoal: Goal of {b}.\n" + (f"Path: {p or 'flume'}\n" if p or t else "") + "\n"
        for b, t, p in bolts)
    return out + "%rec: Unit\n%key: Unit\n\n" + "".join(
        f"Unit: {u}\nRepo: crew\n" + (f"Bolt: {b}\n" if b else "") + ("Kind: chore\n" if kind == "chore" else "")
        + f"Intent: Build {u}.\n" + "".join(f"After: {x}\n" for x in after) + "".join(f"Source: {x}\n" for x in sources) + "\n"
        for u, b, after, kind, sources in work)


FLUME = pathlib.Path(__file__).parent / "flume-0.3.6"


def flume_fixture(name):
    """A Flume status fixture's path: tests/py/flume-0.3.6/<name>.json, or one named with its folder, as
    "flume-0.17.0/kept-open", under tests/py."""
    return (FLUME.parent if "/" in name else FLUME) / f"{name}.json"


def ran(launched=None, held=(), host="deneb", label="madswan", repository="/crew/main", unplaced=None, refused=None,
        keeps=("afterthought/crew",)):
    """A host's runner as crew reads it from its branch (runner.host_read): each launch in launched, {request's number:
    the Flume status fixture its place stands at (flume_fixture: tests/py/flume-0.3.6/<name>.json, or another version's
    named with its folder)}, answered launched and carried in places.rec at the fixture's own place, its repository given
    as repository, and its stream the drive's label, as its host's Flume configuration maps it; each in unplaced,
    {request's number: its place}, answered launched at that place with no status of it carried yet; each in held
    answered held, with the runner's words where held is {request's number: words}; and each in refused, {request's
    number: the runner's words}, answered refused. Its repositories.rec names each forge address in keeps at repository,
    the kit's folder on host where crew reads it (runner.where, Decision 1 of a-bolts-landing-on-main-reads-landed); a
    runner given no repository, or keeps None, reports no repositories."""
    import json
    import plan
    import runner
    answers, places = "", ""
    for n, name in (launched or {}).items():
        status = json.loads(flume_fixture(name).read_text())
        for p in status["status"]["places"]:
            p.update(repository=repository, stream={"name": label, "from": "intent"})
        where = status["status"]["places"][0]["place"].split("@")[0]
        answers += f"\nRequest: {n}\nOutcome: launched\nPlace: {where}\nAt: 2026-10-31T12:01:00Z\n"
        places += f"\nRequest: {n}\nPlace: {where}\nAt: 2026-10-31T12:02:00Z\nStatus: {json.dumps(status)}\n"
    answers += "".join(f"\nRequest: {n}\nOutcome: launched\nPlace: {where}\nAt: 2026-10-31T12:01:00Z\n" for n, where in (unplaced or {}).items())
    words = held if isinstance(held, dict) else dict.fromkeys(held)
    answers += "".join(f"\nRequest: {n}\nOutcome: held\n" + (f"Words: {w}\n" if w else "") + "At: 2026-10-31T12:01:00Z\n"
                       for n, w in words.items())
    answers += "".join(f"\nRequest: {n}\nOutcome: refused\nWords: {w}\nAt: 2026-10-31T12:01:00Z\n" for n, w in (refused or {}).items())
    files = {"runner.rec": plan.Plan(runner.RUNNER + f"\nHost: {host}\nVersion: 0.1.0\nSince: 2026-10-31T11:00:00Z\n"),
             "answers.rec": plan.Plan(runner.ANSWERS + answers), "places.rec": plan.Plan(runner.PLACES + places)}
    if repository is not None and keeps is not None:
        files["repositories.rec"] = plan.Plan(runner.REPOSITORIES + "".join(f"\nRepository: {a}\nFolder: {repository}\n" for a in keeps))
    return {host: runner.host_read(label, host, "5e1f0c2a" + "0" * 32, files, {})}


def launched(bolts, work=(), fleet=None, planned=(), base=True):
    """madswan's plan (flume_plan) with each bolt in bolts started and its work launched as a start launches it
    (plan.reach_places), then, with base, each bolt's base place (runner.bolt_launch), after its pieces so their
    numbers are those a case names, unanswered, a bolt of this crew's and not one started before bolts were base
    places; and each bolt in planned planned and not started: (the plan, requests.rec's records as the writes leave
    them). The requests name their writer: set CREW_AGENT first."""
    import plan
    import runner
    fleet = fleet or madswan_fleet()
    w = FactsWrite(flume_plan([(b, None, None) for b in [*bolts, *planned]], work), label="madswan")
    for b in bolts:
        w.plan.bolt(b).set("Path", "flume")
        plan.reach_places(fleet, w, b)
    for b in bolts if base else ():  # each bolt's base place, after its pieces so their numbers stand, unanswered
        act, work_, given = runner.bolt_launch(w.plan, b, "madswan")
        plan.request(w, act, work_, **given)
    return w.plan, plan.Plan(w.files.get("requests.rec") or runner.REQUESTS).recs("Request")
