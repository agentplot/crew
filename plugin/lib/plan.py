#!/usr/bin/env python3
"""plan.py: the bolt plan, one recutils plan.rec per drive, on the drive's branch of its state repository.

A drive is a body of work, its main level and its loop, named by its label. Its state is the files on the branch <label>/main of the
state repository the teams file names for it (`state`): plan.rec, moves.rec, proposals.rec, the signals agents record
under signals/, and the run record under runs/<host>/.
The plan holds only intent: Bolt and Unit records, a Unit record marked Kind: chore being a chore (plan.11). Every
stage is read from the kits. The planner changes it only
by a proposal (proposals.rec) the user approves; who else writes it directly is may_write's table. A write fetches the branch
over https, applies itself to the tip, checks each file it changed with recfix (the plan with crew's own rules
too), commits through a temporary index in crew's own bare cache of the repo (no working tree is touched), and
pushes without force. A push that is refused because someone wrote first is applied again to the new tip, up to
five times. Each fetch and push a write makes is one try, ended at the family's limit of thirty seconds with
everything it started (gather.tried; weir 69 and C.3, sluice record 0109): a stopped push fails the write and is not
applied again, and the next write reads whether it landed. A kit's fetch of its origin is such a try too (FETCH). A
write that changes several files is one commit; its run-record entry follows it as a commit of its own.

  crew state init <label>                    create <label>/main in the state repository, adopting plan/<label> and
                                             the moves where the drive's blueprints repos have them
  crew drive set <label> --state S --blueprints B... --machine H --session N --folder F --repos R... --accounts <role> <a>...
           --runs <role> standing|on-demand... --review <after_changes> <after_hours> --hosts <host> <ssh> <kind>...
           [--roles <role> <key> <v>]... [--console F] [--repositories <repo> <dir> <checkout>]... [--json]
                                             the drive named in this host's teams file from its flags, every key a flag
                                             with no default, the rest of the file kept, nothing written where it is a
                                             link, a file crew cannot read at all moved aside once, and one at crew's own
                                             version never moved aside: the set mends what it replaces there, refused
                                             only where a check still fails once the drive is set or a part of it is of
                                             a shape the set cannot keep; its drive.set entry written once the file is;
                                             then <label>/main made as crew state init makes it, pushing the entry, a
                                             state not made refused as a state.init that the same command again makes;
                                             run on the host it is invoked on, never forwarded, at Boomdrive's setup's
                                             asking where Nix does not link the file
  crew bolts [<bolt>] [--label L] [--json]   every bolt, unit and chore of the plans, each one's stage read from its kit,
                                             and each merge and landing standing in sluice with its number and state
  crew rail [--label L]                      what waits on the user: open proposals, review batches and bolts to
                                             land, each with when it began to wait, what answers it and
                                             its card key, with whether a card is open for it; then the open cards
                                             whose row is gone; its sweep posts again, on its owner's host, each row's
                                             card and still-proposed record's another host holds or its owner lost,
                                             saying the older copy is dead, and tries again the reading of a batch's, a
                                             long proposal's or a kit's landings card that stands without it, ten
                                             minutes on, a landings card's rows' each where its bolt's work runs
  crew record <kit> <number> --proposed|--accepted|--rejected [--settled-in-pane --excerpt "<words>"] [--alternatives <file>]
                                             the design agent's record at each turn of its status, read on the kit's
                                             main, raising its card unless settled in the pane, the user's yes read in
                                             the design agent's transcript as theirs, a choice when a rule decided,
                                             saying an older copy is dead when another host holds one, changing it on
                                             a revision and closing it on accepted or rejected
  crew card session|end <key> [<unit>]       a plannotator session on what the rail row with that card key asks the
                                             user to read, started on this host with no browser and its link printed,
                                             a batch's on the main level's host and a landing's where its bolt's work
                                             runs, as the runner that took it reported; a reading
                                             started anew, or given again to a card standing without it, changing its
                                             open card to carry the link, each try recorded; and its end, which a
                                             card's close brings too. crew card wait is refused, naming crew card
                                             read <key>, which gives what the user decided in it
  crew card answer batch/<n> --excerpt "<words>"
                                             the user's answer to a batch in their own words in the planner's or the
                                             operator's pane, recorded once crew reads the words in that agent's own
                                             transcript as the user's, no words in the run record: the batch's card
                                             closed with them, and the planner told
                                             them when the operator ran it
  crew bolt new <bolt> "<goal>" --repo <kit> [--source S]... [--before <bolt>]
  crew bolt start <bolt> [--label L]         the bolt's work started through Flume, making no branch and reading no
                                             host: its base place asked of the runner, of crew's kind crew/bolt on
                                             main, and a launch of each unit and chore appended after it; the user's,
                                             or a proposal's; run again on a bolt whose launch the runner refused,
                                             launched anew
  crew bolt order <bolt> --before <bolt>|--first|--last
  crew bolt drop <bolt> "<reason>" [--requeue]
                                             the bolt and its units out of the plan, or with --requeue its units
                                             queued, each of its launches still standing dropped either way and its
                                             base place's last; it asks nothing of any host, and crew deletes no
                                             branch: Flume tidies the base place and sluice ends its branch
  crew bolt land <bolt>                      a started bolt closed once the runner reports its base place landed, at
                                             Flume's commit, refused naming its landing otherwise, recording nothing;
                                             a bolt never started lands once each unit's change is on its kit's main
  crew bolt submit <bolt>... [--excerpt "<the user's words>"] [--label L]
                                             refused at once, before it reads anything: a bolt lands on the user's
                                             send of its row on its kit's landings card, which crew carries to the
                                             runner as a land
  crew unit add <unit> "<intent>" --bolt <bolt>|--repo <kit> [--source S]... [--after U]... [--before U] [--signal ID]
                                             [--unblocks <bolt>]
  crew unit split <unit> "<narrowed intent>" --into <unit> "<intent>" [--into ...]
  crew unit amend <unit> "<new intent>"      a unit's intent replaced; one whose place is launched is marked amended
                                             and its construct retried with the amendment's words, as the write's own
                                             request
  crew unit order <unit> --before <unit>|--first|--last
  crew unit after <unit> <unit>...|--none
  crew unit move <unit> <bolt>|queue [--unblocks <bolt>]
  crew unit drop <unit> "<reason>"
  crew chore add <chore> "<words>" --bolt <bolt>|--repo <kit> [--source S]... [--after U]... [--before U] [--signal ID]
                                             [--unblocks <bolt>]
  crew chore order|after|move|drop ...       as a unit's, of a chore: planned maintenance that changes nothing a spec
                                             says must be true, built in its bolt as Flume's chore kind
  crew plan propose <file> [--replaces <n>]  the planner's proposal: a Case and the plan commands it would run (Do);
                                             crew raises its card in the planner's name, or changes the card of the
                                             one it replaces
  crew plan proposed [<n>] [--json] [--open] the open proposals, or one as the user reads it; --open writes that to a
                                             file on this host and opens it in plannotator
  crew plan card <n>                         the proposal's Pending You card as JSON, from the branch alone, and its
                                             picture, a PNG crew draws, written on this host
  crew plan approve <n> [--clear <unit>...]  the proposal applied as read, in one commit, but for the new units the
                                             user left out
  crew plan answer <n> <question> <answer>... [--note "<text>"]
                                             one answer of the proposal's card, kept on this host; the change is
                                             applied with its boxes as they stand once every question is answered
  crew plan drop <n> "<reason>"              the proposal closed unapplied
  crew signal <slug> "<what it asserts>" --excerpt "<the words, verbatim>"|--excerpt-file <path> [--kind K] [--subject a,b]
                                             a finding, as a capture and its signal on the drive's branch: an
                                             agent's excerpt checked against its own Claude transcript and graded, the
                                             user's note at a shell its own excerpt
  crew signal show <id>                      a signal with its capture's provenance and its move, from either home
  crew signal move <id> attach|challenge|new-territory|answered|drop [--target T] [--reason R]
                                             curation's move for a signal, in moves.rec on the drive's branch

A signal recorded through crew is on the drive's branch, under signals/; one the daily pass read from a meeting or
a channel is in the drive's first blueprints repo. An id is looked up in that order. Every command that takes a
signal's id takes its full id, <capture>/<NN>-<slug>, or its short one, <capture>/<NN>, such as
2026-10-20-swancloud-planner-72efd8ec/01: the one signal of that capture numbered NN, written by its full id.

A command that names no drive reads them all, or the agent's own (CREW_LABEL); --label names one.
"""
import argparse, base64, bisect, contextlib, datetime, fcntl, io, json, os, pathlib, re, shlex, subprocess, sys, time
# getpass, hashlib, shutil, tempfile and urllib.parse are imported where they are used: every crew command starts this
# module afresh, and those five (OpenSSL, the compression modules) were a third of its start.
from signal import SIGTERM
# Run as the command, this module is the plan the modules it imports import, so the command holds one reading of the
# branch, its entries' pushes among its steps, and fetches it once (plan.12), rather than a second copy fetching anew.
if __name__ == "__main__":
    sys.modules.setdefault("plan", sys.modules[__name__])

LIB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(LIB))
import asks  # noqa: E402
import crew  # noqa: E402
import gather  # noqa: E402
import kit  # noqa: E402
import record  # noqa: E402
import runner  # noqa: E402
import transcript  # noqa: E402
import cards  # noqa: E402
from cards import joined, new_units  # noqa: E402
from crew import Refusal, Stopped, fail  # noqa: E402
from picture import cut  # noqa: E402

# The waits, in seconds, before a refused write's replays, one before each replay's fresh fetch: each the double of the
# one before up to eight, so a branch taking a commit every few seconds is outwaited rather than given up on (state.1),
# and 23.5 in all at most, so a command whose write and entry are both replayed to the end still answers (code.9).
REPLAY_WAITS = (0.5, 1.0, 2.0, 4.0, 8.0, 8.0)
REPLAYS = len(REPLAY_WAITS)
# How many times a fetch is made again when another command on this host moved crew's cache's ref of the branch while it
# fetched, which git refuses as a ref that is at another commit than it read: every act pushes its entry (read.5), so
# commands on one host fetch and push side by side.
LOCK_TRIES = 5
# What a command found out before it wrote or was refused: the drive whose run record its entry goes in.
CONTEXT = {}
CACHE = pathlib.Path.home() / ".cache/crew/git"
HEADER = """\
# The drive's bolts and their units and chores: what is to be built, in
# which bolt, in what order. Nothing here says how far anything has got: `crew
# bolts` reads that from the kits. Written only by `crew bolt`, `crew unit` and
# `crew chore`.
# A Source is a path in the drive's first blueprints repo, or
# <owner>/<name>:<path> in another.

%rec: Bolt
%doc: Work on branch bolt/<Bolt> of Repo, marked Path: flume once crew bolt start has started it, whose Flume places build it.
%key: Bolt
%type: Bolt regexp /^[a-z0-9][a-z0-9-]*$/
%type: Path enum flume
%mandatory: Repo Goal
%allowed: Bolt Repo Goal Source Path
%unique: Repo Goal

%rec: Unit
%doc: One OpenSpec change named Unit, built in a Flume place of its bolt's; or, marked Kind: chore, a chore: planned maintenance with no change, its Intent its words, built in a Flume place of the chore kind.
%key: Unit
%type: Unit regexp /^[a-z0-9][a-z0-9-]*$/
%type: Bolt rec Bolt
%type: Kind enum chore
%mandatory: Repo Intent
%allowed: Unit Repo Bolt Kind Intent After Source Amended
%unique: Repo Bolt Kind Intent
"""
MOVES = """\
# The drive's curation moves: one per signal, appended through crew and
# never merged. A Signal is a signal's id: signals/<id>.md on this branch, or
# in the drive's first blueprints repo.

%rec: Move
%doc: A curation move over one signal, stored with its inputs.
%key: Signal
%mandatory: Signal Move Date By
%allowed: Signal Move Target Reason Date By
%type: Move enum attach challenge new-territory answered drop route
%type: Date date
"""


def need_recutils():
    """Every plan command checks for recutils before anything else."""
    for c in ("recsel", "recfix"):
        if not any(os.access(os.path.join(d, c), os.X_OK) for d in os.environ.get("PATH", "").split(os.pathsep) if d):
            sys.exit(f"crew's plan needs recutils, and {c} is not on PATH: install the recutils package "
                     "(crew's devenv.nix declares it; on a host, swancloud's packages)")


# ---------------------------------------------------------------------------------------------------- records

FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9_]*):(.*)$")


class Rec:
    """One record: its record set and its fields in order. A comment line inside a record is kept as field '#'."""

    def __init__(self, kind, fields):
        self.kind, self.fields = kind, fields

    def get(self, f):
        return next((v for n, v in self.fields if n == f), None)

    def all(self, f):
        return [v for n, v in self.fields if n == f]

    def drop(self, f):
        self.fields = [(n, v) for n, v in self.fields if n != f]

    def add(self, f, v, after=None):
        """Add a field, after the last field named `after` when there is one, else after the last of its own name."""
        at = None
        for i, (n, _) in enumerate(self.fields):
            if n == f or (after and n == after):
                at = i
        self.fields.insert(len(self.fields) if at is None else at + 1, (f, v))

    def set(self, f, v, after=None):
        if self.get(f) is None:
            self.add(f, v, after)
        else:
            first = next(i for i, (n, _) in enumerate(self.fields) if n == f)
            self.fields = [(n, w) for i, (n, w) in enumerate(self.fields) if n != f or i == first]
            self.fields[first] = (f, v)

    def name(self):
        return self.get(self.kind)

    def lines(self):
        out = []
        for n, v in self.fields:
            if n == "#":
                out.append(v)
                continue
            first, *rest = v.split("\n")
            out.append(f"{n}: {first}" if first else f"{n}:")
            out += [f"+ {l}" if l else "+" for l in rest]
        return out


def is_chore(u):
    """Whether a record of the plan's Unit set is a chore, marked Kind: chore (plan.11), rather than a unit."""
    return u.get("Kind") == "chore"


def kind_of(u):
    """A Unit record's kind as crew names it: chore or unit, which is also its command and its run-record object."""
    return "chore" if is_chore(u) else "unit"


class Plan:
    """plan.rec as paragraphs: the comments and record descriptors kept as written, and the records in file order."""

    def __init__(self, text):
        self.paras, kind, cur = [], None, []
        for line in text.split("\n") + [""]:
            if line.strip():
                cur.append(line)
                continue
            if not cur:
                continue
            if any(FIELD.match(l) for l in cur):
                fields = []
                for l in cur:
                    m = FIELD.match(l)
                    if l.startswith("#"):
                        fields.append(("#", l))
                    elif l.startswith("+"):
                        n, v = fields[-1]
                        fields[-1] = (n, v + "\n" + (l[2:] if l.startswith("+ ") else l[1:]))
                    elif m:
                        v = m.group(2)
                        fields.append((m.group(1), v[1:] if v.startswith(" ") else v))
                self.paras.append(Rec(kind, fields))
            else:
                for l in cur:
                    if l.startswith("%rec:"):
                        kind = l[5:].strip().split()[0]
                self.paras.append(cur)
            cur = []

    def text(self):
        return "\n\n".join("\n".join(p.lines() if isinstance(p, Rec) else p) for p in self.paras) + "\n"

    def recs(self, kind):
        return [p for p in self.paras if isinstance(p, Rec) and p.kind == kind]

    def bolts(self):
        return self.recs("Bolt")

    def work(self):
        """Every record of the Unit set, units and chores, in file order: the work built in bolts (plan.11)."""
        return self.recs("Unit")

    def units(self):
        return [u for u in self.work() if not is_chore(u)]

    def chores(self):
        return [u for u in self.work() if is_chore(u)]

    def bolt(self, name):
        return next((b for b in self.bolts() if b.name() == name), None)

    def item(self, name):
        """The unit or chore by that name: one key holds both."""
        return next((u for u in self.work() if u.name() == name), None)

    def unit(self, name):
        u = self.item(name)
        return u if u is not None and not is_chore(u) else None

    def chore(self, name):
        u = self.item(name)
        return u if u is not None and is_chore(u) else None

    def work_of(self, bolt):
        return [u for u in self.work() if u.get("Bolt") == bolt]

    def units_of(self, bolt):
        return [u for u in self.units() if u.get("Bolt") == bolt]

    def queue(self, repo=None):
        """The queued work of a repo, or of every repo: units and chores with no bolt, in order."""
        return [u for u in self.work() if not u.get("Bolt") and repo in (None, u.get("Repo"))]

    def group(self, u):
        """The work built in order with this unit or chore: its bolt's, or its repo's queue."""
        return self.work_of(u.get("Bolt")) if u.get("Bolt") else self.queue(u.get("Repo"))

    def remove(self, rec):
        self.paras.remove(rec)

    def end_of(self, kind):
        """Where a new record of a set goes: after its last record, or after its descriptor when it has none."""
        recs = self.recs(kind)
        if recs:
            return self.paras.index(recs[-1]) + 1
        for i, p in enumerate(self.paras):
            if not isinstance(p, Rec) and any(l.startswith("%rec:") and l[5:].split()[0] == kind for l in p):
                return i + 1
        fail(f"the plan declares no %rec: {kind}")

    def insert(self, rec, before=None, after=None):
        if rec in self.paras:
            self.paras.remove(rec)
        if before is not None:
            at = self.paras.index(before)
        elif after is not None:
            at = self.paras.index(after) + 1
        else:
            at = self.end_of(rec.kind)
        self.paras.insert(at, rec)

    def place_last(self, u):
        """Put a unit at the end of its group: after the last unit of its bolt, or of its repo's queue."""
        others = [o for o in self.group(u) if o is not u]
        self.insert(u, after=others[-1] if others else None)


def recfix(text, what):
    """recfix --check on a plan or moves file, read from its standard input; the message names what was checked."""
    r = subprocess.run(["recfix", "--check"], input=text, capture_output=True, text=True)
    if r.returncode:
        said = (r.stderr or r.stdout).strip()
        fail(f"{what} fails recfix --check: " + re.sub(r"(?m)^stdin:", pathlib.Path(what).name + ":", said))


def checked(files):
    """recfix --check on every file a commit holds, {path: text}: a .rec file whole, and a signal's or a capture's
    markdown by its frontmatter, which is one record. A comment stands in for the opening ---, so recfix's line
    numbers are the file's."""
    for path, text in files.items():
        if path.endswith(".md"):
            m = re.match(r"^---\n(.*?\n)---\n", text, re.S)
            m or fail(f"{path} has no frontmatter")
            recfix("#\n" + m.group(1), path)
        else:
            recfix(text, path)


def declares(p):
    """The record set a paragraph of the plan declares, or None for a record or a comment."""
    return None if isinstance(p, Rec) else next((l[5:].split()[0] for l in p if l.startswith("%rec:")), None)


def in_step(plan, header=HEADER):
    """Bring each record descriptor of a plan, or of another of crew's files with its header, in step with crew's own
    (HEADER), so a branch started before a field was allowed takes it on its next write, still allowing what the
    branch's own allowed (still_allowed). Returns whether any changed."""
    want = {declares(p): p for p in Plan(header).paras if declares(p)}
    changed = False
    for i, p in enumerate(plan.paras):
        k = declares(p)
        new = still_allowed(p, want[k]) if k in want else p
        if new != p:
            plan.paras[i], changed = new, True
    return changed


def still_allowed(have, want):
    """crew's descriptor of a record set (want), still allowing each field the branch's own (have) allowed and crew's
    no longer does, a Bolt's Team and a Proposal's Agreed among them, so records that carry one pass recfix --check
    with nothing stripped from them (Decision 9 of the-team-machinery-leaves; plan.1, state.2)."""
    def allowed(p):
        return next((l.split()[1:] for l in p if l.startswith("%allowed:")), [])
    extra = [f for f in allowed(have) if f not in allowed(want)]
    return [l + "".join(f" {f}" for f in extra) if extra and l.startswith("%allowed:") else l for l in want]


def check(plan):
    """crew's own rules, which recfix cannot check: a unit's or chore's bolt exists in the same repo, and its After
    names units or chores of the same bolt, with no cycle; a chore is never marked amended (plan.11)."""
    bolts = {b.name(): b for b in plan.bolts()}
    units = {u.name(): u for u in plan.work()}
    for u in plan.work():
        b, k = u.get("Bolt"), kind_of(u)
        if b:
            b in bolts or fail(f"{k} {u.name()} names bolt {b}, which the plan does not hold")
            bolts[b].get("Repo") == u.get("Repo") or fail(f"{k} {u.name()} is in {u.get('Repo')} and its bolt {b} in {bolts[b].get('Repo')}")
        not (is_chore(u) and u.get("Amended")) or fail(f"chore {u.name()} is marked amended, and a chore has no amendment: "
                                                      "its words change by a drop and an add")
        for a in u.all("After"):
            a in units or fail(f"{k} {u.name()} comes after {a}, which the plan does not hold")
            b or fail(f"{k} {u.name()} is queued, so it can come after nothing; dependencies are within a bolt")
            units[a].get("Bolt") == b or fail(f"{k} {u.name()} comes after {a}, which is in {units[a].get('Bolt') or 'the queue'}, not {b}")
    seen, done = set(), set()

    def visit(n, path):
        if n in done:
            return
        n not in seen or fail("units would come after each other in a cycle: " + " -> ".join(path + [n]))
        seen.add(n)
        for a in units[n].all("After"):
            visit(a, path + [n])
        done.add(n)
    for n in units:
        visit(n, [])


# -------------------------------------------------------------------------------------------------- transport

def url(repo):
    """Every plan read and write goes over https: gh's credential helper on a Mac, the token helper on a box.
    Never ssh, which on a Mac waits on 1Password."""
    return f"https://github.com/{repo}.git"


def gitenv(extra=None):
    env = {k: v for k, v in os.environ.items() if k not in (
        "GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_QUARANTINE_PATH")}
    env["GIT_TERMINAL_PROMPT"] = "0"
    return dict(env, **(extra or {}))


def cache(repo):
    """crew's bare cache of a repo, which holds the objects a write commits and has no working tree."""
    c = CACHE / f"{repo}.git"
    if not (c / "HEAD").exists():
        c.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init", "-q", "--bare", str(c)], check=True, env=gitenv())
    return c


REMOTE_WORDS = ("fetch", "ls-remote", "push")


def reaches_remote(args):
    """Whether a git call in crew's cache of a state repository reaches its remote, and so is one try to the family's
    limit (weir 69, C.3): a fetch, a listing or a push, by the call's word, since crew's cache reaches no remote by any
    other. A decision on plain facts (code.7)."""
    return bool(args) and args[0] in REMOTE_WORDS


def was_stopped(r):
    """Whether a git call's result (git) is a try stopped at its limit; a result with no word of it was not."""
    return getattr(r, "stopped", False) is True


class Ran:
    """What a git call in crew's cache gave: its exit, what it printed, and whether it was a try stopped at its limit.
    A stopped try's returncode is never 0, its stderr is its failure in the family's words and its stdout is empty."""

    def __init__(self, returncode, stdout, stderr, stopped=False):
        self.returncode, self.stdout, self.stderr, self.stopped = returncode, stdout, stderr, stopped


def git(repo, *args, input=None, env=None, check=True):
    """git in crew's bare cache of a repo: a call that reaches the remote (reaches_remote) run as one try to the family's
    limit, gather.TRY_FOR read at the call, naming its remote by the address it is given, the call's first argument
    after its word that is not an option (gather.tried, weir 69, C.3); every other call run to its end. With check, a
    failure refuses naming the word, the repo and git's words or the stopped try's; else the result (Ran)."""
    argv = ["git", "-C", str(cache(repo)), *args]
    if reaches_remote(args):
        limit = gather.TRY_FOR
        code, out, err, stopped = gather.tried(argv, input=input, env=gitenv(env), limit=limit)
        if stopped:
            remote = next((a for a in args[1:] if not a.startswith("-")), repo)
            r = Ran(code or 1, "", gather.stopped(f"git {args[0]}", remote, limit, err), True)
        else:
            r = Ran(127 if code is None else code, out, err)
    else:
        done = subprocess.run(argv, input=input, capture_output=True, text=True, env=gitenv(env))
        r = Ran(done.returncode, done.stdout, done.stderr)
    if check and r.returncode:
        fail(f"git {args[0]} in crew's cache of {repo} failed: {r.stderr.strip()}")
    return r if not check else r.stdout.strip()


class Reading:
    """What one command has read on this host, kept for its later steps, so the command fetches each branch and reads
    each kit once however many steps it has (plan.12): the tip of each branch it fetched or pushed, and each kit's
    answer by host, in this process's memory, every crew command being one process. Inside fresh() nothing is served
    from it, so a wait looks again each time; what is read there is still kept. A reading is never a service or state:
    it is gone with its command (state.4)."""

    def __init__(self):
        # follower: the host's follower's Kept, handed in for its refresh, which serves what has not moved since its
        # last read; None for any other command
        self.memory, self.bypass, self.follower = {}, 0, None

    def held(self, name):
        return self.memory.get(name)

    def keep(self, name, value):
        self.memory[name] = value

    @staticmethod
    def tip_name(repo, ref):
        return "tip-" + re.sub(r"[^A-Za-z0-9.-]", lambda m: f"_{ord(m.group()):x}_", f"{repo} {ref}")

    def tip(self, repo, ref):
        return None if self.bypass else self.held(self.tip_name(repo, ref))

    def keep_tip(self, repo, ref, sha):
        self.keep(self.tip_name(repo, ref), sha)

    def forget_tip(self, repo, ref):
        """A branch's tip this command held, forgotten, so its next read fetches: after a push stopped at its limit,
        which may have landed or not (land)."""
        self.memory.pop(self.tip_name(repo, ref), None)

    def kits(self, host):
        return {} if self.bypass else self.held(f"kits-{host}.json") or {}

    def keep_kits(self, host, answers):
        self.keep(f"kits-{host}.json", dict(self.held(f"kits-{host}.json") or {}, **answers))

    def drop_kit(self, host, main):
        """A step that made or removed a worktree in a kit, or committed in one: the next step reads that kit again."""
        kits = self.held(f"kits-{host}.json") or {}
        if main in kits:
            del kits[main]
            self.keep(f"kits-{host}.json", kits)

    @staticmethod
    def sweep():
        """A reading folder that a killed command of an older crew left, when its steps were processes of their own,
        goes once it is a day old."""
        root = pathlib.Path.home() / ".cache/crew/reads"
        try:
            old = [d for d in root.iterdir() if re.fullmatch(r".{8}", d.name) and d.is_dir() and time.time() - d.stat().st_mtime >= 86400]
        except OSError:
            return
        if old:
            import shutil
            for d in old:
                shutil.rmtree(d, ignore_errors=True)

    @contextlib.contextmanager
    def fresh(self):
        self.bypass += 1
        try:
            yield
        finally:
            self.bypass -= 1


READ = Reading()


def kit_served(kept, stamp, req):
    """The answer the follower kept for a kit that it may serve in place of a gather (plan.12's reading of 2026-10-28):
    kept is (the request it answered, its answer with the stamp it was read at) or None, stamp the kit's stamp now;
    the answer when the stamp now is read and is the one it was read at and the request is the same, else None, and
    the kit is asked of its host. A decision on plain facts (code.7)."""
    if not kept or not kept[1] or stamp is None:
        return None
    then, answer = kept
    return answer if answer.get("stamp") == stamp and then == req else None


# The state branch's paths whose blobs a refresh reads at a moved tip in one cat-file: its plan, proposals and moves,
# its signals and its run record's days the rail reads (BATCH_DAYS); a path past them is read when asked.
def wanted(path, since):
    return ("/" not in path and path.endswith(".rec")) or path.startswith("signals/") or (
        path.startswith("runs/") and path.endswith(".rec") and pathlib.PurePath(path).stem >= since)


class Kept:
    """What the host's follower keeps between its refreshes, in its own process and never written (plan.12's reading
    of 2026-10-28, state.4): each kit's answer, with the request it answered and the stamp it was read at, by host;
    each branch tip's files by blob, the blobs' text, and the blobs whose recfix check passed; and what Pending You
    answered of the cards at the clock's last tick. It is keyed by the stamps and commits it was read at, so nothing is
    served once they move (read.1); what a refresh did not use is dropped at its end (settle)."""

    def __init__(self):
        self.kits, self.used, self.stamps = {}, {}, {}
        self.listings, self.blobs, self.checked, self.tips = {}, {}, set(), set()
        # cards: the clock's last ask of Pending You after the cards (cards_fetched), (found, why), with the cards read
        # in their owners' names third when any was (owners_read), which every card sweep judges with until the next
        # tick; None while no tick has asked, when the read's sweep asks on its tick
        self.cards = None
        # listed: herdr's listing of the askers of the questions the sweep judges, read on the clock's tick beside the
        # cards (askers_listed), {name: (listed, why)}; None while no tick has read it
        self.listed = None

    def served(self, host, main, req):
        return kit_served(self.kits.get(host, {}).get(main), self.stamps.get((host, main)), req)

    def use(self, host, main, req, answer):
        """A kit this refresh read, served or gathered, answer None when its host did not answer: what the next check
        stamps."""
        self.used.setdefault(host, {})[main] = (req, answer)

    def listing(self, repo, tip):
        """Each file at the tip by its blob, {path: blob}: one ls-tree at a tip not yet read, kept while a refresh reads
        it; the blobs of the paths a refresh reads (wanted) not yet held are read then, in one cat-file."""
        key = (repo, tip)
        self.tips.add(key)
        if key not in self.listings:
            self.listings[key] = files = blobs_at(repo, tip)
            since = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=BATCH_DAYS + 1)).isoformat()
            new = sorted({b for p, b in files.items() if wanted(p, since) and b not in self.blobs})
            self.blobs.update(zip(new, cat_file(repo, new)))
        return self.listings[key]

    def text(self, repo, blob):
        if blob not in self.blobs:
            self.blobs[blob] = cat_file(repo, [blob])[0]
        return self.blobs[blob]

    def settle(self):
        """A refresh's end: the kits it read are what it keeps, and the tips it did not read go with their blobs."""
        self.kits, self.used = self.used, {}
        self.listings = {k: v for k, v in self.listings.items() if k in self.tips}
        self.tips = set()
        live = {b for files in self.listings.values() for b in files.values()}
        self.blobs = {b: t for b, t in self.blobs.items() if b in live}
        self.checked &= live


def blobs_at(repo, tip, prefix=None):
    """Each file at a tip, or under prefix, by its blob, {path: blob}, in one ls-tree."""
    files = {}
    for line in git(repo, "ls-tree", "-r", tip, *(["--", prefix] if prefix else [])).splitlines():
        meta, _, path = line.partition("\t")
        _, kind, blob = meta.split()
        if kind == "blob":
            files[path] = blob
    return files


def kept_listing(repo, tip):
    """The follower's listing of a tip (Kept.listing) when it is reading and tip names a commit, else None."""
    k = READ.follower
    return k.listing(repo, tip) if k is not None and tip and crew.SHA.fullmatch(tip) else None


def cat_file(repo, names):
    """The text of each object named, a blob or <tip>:<path>, in crew's cache of the repo, in one git cat-file --batch:
    a list in order, None for one that is not there or is no blob."""
    if not names:
        return []
    r = subprocess.run(["git", "-C", str(cache(repo)), "cat-file", "--batch"], input="".join(f"{n}\n" for n in names).encode(),
                       capture_output=True, env=gitenv())
    r.returncode == 0 or fail(f"git cat-file in crew's cache of {repo} failed: {r.stderr.decode(errors='replace').strip()}")
    out, data, i = [], r.stdout, 0
    for _ in names:
        nl = data.index(b"\n", i)
        head, i = data[i:nl], nl + 1
        if head.endswith((b" missing", b" ambiguous")):
            out.append(None)
            continue
        _, kind, size = head.rsplit(b" ", 2)
        out.append(data[i:i + int(size)].decode("utf-8", "replace") if kind == b"blob" else None)
        i += int(size) + 1
    return out


def paths_at(repo, tip, prefix):
    """The paths under prefix at a tip, in order: from the follower's listing when it reads, else one ls-tree."""
    files = kept_listing(repo, tip)
    if files is not None:
        return sorted(p for p in files if p.startswith(prefix))
    return git(repo, "ls-tree", "-r", "--name-only", tip, "--", prefix).splitlines()


def tip_of(repo, ref, fresh=False):
    """The tip of a branch of the repo: the one this command already holds, else fetched now over https and kept; or
    None when the repo has no such branch, which is not kept, so a later step looks again, unless the follower handed
    in its cache's word that there is none (""). fresh fetches even when a tip is held: after a refused push, and
    after any push that is not a write's own. A write lands on it (land), and a decision reads the branch at it, every
    act there with its entries, which its commit carries (read.5). A fetch stopped at the family's limit (git) refuses
    at once, naming the branch, the repo and the stopped try: never fetched again for a lock, never read as a branch the
    repo lacks (read.1)."""
    held = None if fresh else READ.tip(repo, ref)
    if held is not None:
        return held or None
    with_it = beside(ref)
    for n in range(LOCK_TRIES):
        r = git(repo, "fetch", "--quiet", "--no-tags", *(["--prune"] if with_it else []), url(repo), f"+refs/heads/{ref}:refs/crew/{ref}",
                *with_it, check=False)
        if was_stopped(r) or not (r.returncode and "cannot lock ref" in r.stderr):
            break
        time.sleep(0.1 * (n + 1))
    if was_stopped(r):
        fail(f"could not fetch {ref} of {repo} over https: {r.stderr.strip()}")
    if r.returncode:
        if "couldn't find remote ref" in r.stderr:
            return None
        fail(f"could not fetch {ref} of {repo} over https: {r.stderr.strip()}")
    tip = tip_here(repo, ref) or git(repo, "rev-parse", f"refs/crew/{ref}")  # the cache's files, else git
    READ.keep_tip(repo, ref, tip)
    return tip


def tips_of(repo, refs):
    """Several branches of the repo fetched now over https in one fetch, each with what it brings beside it (beside),
    the host's follower's one fetch of a repository at its clock's tick, carrying every branch it reads of it (plan.12;
    sluice's core.31, the remote's one fetch a tick): {ref: tip}, None for a branch the repo does not have. A fetch
    git refuses for a branch it cannot find is made again without the branch it names, which reads None, so a branch
    not yet made costs the rest one fetch more and nothing else; one naming no branch asked for fetches each alone
    (tip_of); any other failure refuses, naming the repo. A fetch stopped at the family's limit (git) refuses at once,
    whatever git wrote before it was stopped: no branch is read as absent and none is fetched alone (read.1)."""
    refs, out = list(dict.fromkeys(refs)), {}
    while refs:
        specs = [s for ref in refs for s in [f"+refs/heads/{ref}:refs/crew/{ref}", *beside(ref)]]
        prune = any(beside(ref) for ref in refs)
        for n in range(LOCK_TRIES):
            r = git(repo, "fetch", "--quiet", "--no-tags", *(["--prune"] if prune else []), url(repo), *specs, check=False)
            if was_stopped(r) or not (r.returncode and "cannot lock ref" in r.stderr):
                break
            time.sleep(0.1 * (n + 1))
        if was_stopped(r):
            fail(f"could not fetch {', '.join(refs)} of {repo} over https: {r.stderr.strip()}")
        if not r.returncode:
            break
        if "couldn't find remote ref" not in r.stderr:
            fail(f"could not fetch {', '.join(refs)} of {repo} over https: {r.stderr.strip()}")
        gone = next((ref for ref in refs if re.search(rf"couldn't find remote ref (refs/heads/)?{re.escape(ref)}\s*$", r.stderr, re.M)), None)
        if gone is None:
            return dict(out, **{ref: tip_of(repo, ref, fresh=True) for ref in refs})
        out[gone] = None
        refs.remove(gone)
    for ref in refs:
        out[ref] = tip_here(repo, ref) or git(repo, "rev-parse", f"refs/crew/{ref}")  # the cache's files, else git
        READ.keep_tip(repo, ref, out[ref])
    return out


def beside(ref):
    """What a fetch of a branch brings with it, in the same fetch (plan.12): for a drive's branch, <label>/main, its
    runners' branches, <label>/runner/*, which crew reads and never writes (state.5), pruned of a host's branch gone
    from the repository; nothing for any other branch (Decision 4 of teams-cross-to-flume-as-their-bolts-land)."""
    m = re.fullmatch(r"([a-z0-9][a-z0-9-]*)/main", ref)
    return [f"+refs/heads/{m.group(1)}/runner/*:refs/crew/{m.group(1)}/runner/*"] if m and m.group(1) != "plan" else []


def runner_tips(repo, label, fetch=True):
    """Each host's runner branch of the drive as crew's cache of its state repository holds it, as this command's
    fetch of <label>/main brought it (tip_of, beside), or with fetch False as the cache holds it now, as the follower's
    clock last fetched it (plan.12): {host: commit}. Read from the cache's files with no process, its loose refs over
    packed-refs, as tip_here reads a branch; through git for-each-ref only when the files can't say."""
    if fetch:
        tip_of(repo, f"{label}/main")
    c, prefix = CACHE / f"{repo}.git", f"refs/crew/{label}/runner/"
    tips = crew.files_refs(c, prefix) if (c / "HEAD").exists() else {}
    if tips is None:
        tips = dict(l.split(" ", 1) for l in git(repo, "for-each-ref", "--format=%(refname) %(objectname)", prefix).splitlines())
    return {name[len(prefix):]: sha for name, sha in tips.items() if crew.NAME.match(name[len(prefix):])}


def drive_hosts(fleet, label, fetch=True):
    """A drive's hosts (Decision 5 of the-team-machinery-leaves): its main level's machine and every host whose
    runner answers for it, its branch <label>/runner/<host> in the drive's state repository as this command's
    fetch brought it, or with fetch False as crew's cache holds it now (runner_tips), each once, sorted; the hosts its
    kits' work runs on, as the runners report it, which crew looks up no other way (the user's ruling of 2026-11-01)."""
    repo, _ = state_of(fleet, label)
    return sorted({crew.drive_of(fleet, label)["machine"], *runner_tips(repo, label, fetch)})


def hosts_of(fleet, label, runs):
    """A drive's hosts as a read holds them (Decision 5 of the-team-machinery-leaves): its main level's machine and
    each host whose runner the read read beside its plan (runs, rail_runs), each once, sorted; reading nothing (code.7)."""
    return sorted({crew.drive_of(fleet, label)["machine"], *((runs or {}).get(label, ([], {}))[1])})


def runners(repo, label):
    """Each host's runner of the drive, read at the tip of its branch that this command's fetch of <label>/main
    brought (runner_tips; Decision 4 of teams-cross-to-flume-as-their-bolts-land): {host: runner.host_read's reading},
    every host's files read in one cat-file (the follower's kept blobs when it reads), each checked by recfix. A host
    with no branch is not in it, and runner.of_host names it. Kept for the command by the tips it read."""
    tips = runner_tips(repo, label)
    name = f"runners-{repo}-{label}-" + ",".join(f"{h}@{t}" for h, t in sorted(tips.items()))
    if READ.held(name) is not None:
        return READ.held(name)
    paths = [(h, f) for h in sorted(tips) for f in runner.FILES]
    shown = [show(repo, tips[h], f) for h, f in paths] if all(kept_listing(repo, tips[h]) is not None for h in tips) else \
        cat_file(repo, [f"{tips[h]}:{f}" for h, f in paths])
    texts, out = dict(zip(paths, shown)), {}
    for h in sorted(tips):
        files, refused = {}, {}
        for f in runner.FILES:
            text = texts[(h, f)]
            try:
                text is None or recfix(text, f)
            except Refusal as e:
                refused[f] = str(e)
            files[f] = Plan(text) if text is not None and f not in refused else None
        out[h] = runner.host_read(label, h, tips[h], files, refused)
    READ.keep(name, out)
    return out


def tip_here(repo, ref):
    """A branch's tip as crew's cache of the repo holds it, refs/crew/<ref>, read from the cache's files with no process
    (crew.files_ref), the follower's look and check (plan.12): its commit, "" when the cache holds none, a branch not
    fetched, not started or no cache yet; through git rev-parse only when the files can't say, and None when git
    can't read it either (read.1)."""
    c = CACHE / f"{repo}.git"
    if not (c / "HEAD").exists():
        return ""
    got = crew.files_ref(c, f"refs/crew/{ref}")
    if got is not None:
        return got
    r = subprocess.run(["git", "-C", str(c), "rev-parse", "--verify", "-q", f"refs/crew/{ref}^{{commit}}"], capture_output=True,
                       text=True, env=gitenv())
    return r.stdout.strip() if r.returncode == 0 else "" if r.returncode == 1 and not r.stderr.strip() else None


def show(repo, tip, path):
    """A file's text at a tip, None when it is not there: the follower's kept blob when it reads and the blob is held."""
    files = kept_listing(repo, tip)
    if files is not None:
        return READ.follower.text(repo, files[path]) if path in files else None
    r = git(repo, "show", f"{tip}:{path}", check=False)
    return r.stdout if r.returncode == 0 else None


def commit(repo, parent, files, message):
    """A commit of files' new text ({path: text}) on top of parent, made through a temporary index: no working tree
    is touched, and no other path changes."""
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        idx = {"GIT_INDEX_FILE": str(pathlib.Path(d) / "index")}
        git(repo, "read-tree", *([parent] if parent else ["--empty"]), env=idx)
        # Every file's blob in one hash-object, and every path into the index in one update-index.
        paths, texts = list(files), []
        for i, path in enumerate(paths):
            texts.append(pathlib.Path(d) / f"blob-{i}")
            texts[-1].write_text(files[path])
        blobs = git(repo, "hash-object", "-w", "--stdin-paths", input="".join(f"{t}\n" for t in texts)).split("\n")
        git(repo, "update-index", "--add", "--index-info", input="".join(f"100644 {b}\t{p}\n" for b, p in zip(blobs, paths)), env=idx)
        tree = git(repo, "write-tree", env=idx)
    return git(repo, "commit-tree", tree, *(["-p", parent] if parent else []), "-F", "-", input=message)


def replay_wait(n, draw):
    """How long a refused write waits, in seconds, before its nth replay's fresh fetch (from 0): REPLAY_WAITS' nth,
    spread over its upper half by draw, a number in [0, 1) drawn afresh for each wait, so commands refused at one moment
    replay at different moments rather than in step. Never more than the nth, so the whole wait is bounded by their
    sum (code.7, code.9)."""
    return REPLAY_WAITS[n] * (1 + draw) / 2


def land(repo, ref, path, make):
    """make(tip) gives a file's new text (or, with path None, {path: text}) and the commit message, or refuses; or a
    chain of them, a list, each committed on the one before, as the run record's entries are, one commit each. Every
    file a commit holds is checked first. The first attempt starts from the tip the command holds; the last commit is
    pushed without force, and when the push is refused because the branch moved, the write waits a growing moment
    (replay_wait), the branch is fetched afresh and make runs again on the new tip, the whole chain made again, up to
    REPLAYS times, so a busy branch is outwaited (plan.1, state.1); a write still refused is refused, and an entry so
    refused is kept for the host's next push (record.reach, record.2). The command then holds the commit it pushed, so
    its later steps read its own write (tip_of). A push stopped at the family's limit (git; weir C.3) is no refusal of
    the branch, since it may have landed: the write refuses at once with the stopped try, waiting for nothing, fetching
    nothing and making nothing again, and forgets the tip it held, so the next read fetches and the next write is
    applied on the tip it finds, every check made again there (plan.1); an entry it carried stays on the host for its
    next push, as a refused one does (record.2)."""
    tip, waited = tip_of(repo, ref), 0.0
    for n in range(1 + REPLAYS):
        made = make(tip)
        sha = tip
        for text, message in made if isinstance(made, list) else [made]:
            files = text if path is None else {path: text}
            checked(files)
            sha = commit(repo, sha, files, message)
        r = git(repo, "push", "--quiet", url(repo), f"{sha}:refs/heads/{ref}", check=False)
        if r.returncode == 0:
            # The cache's own mark of the tip: another command on this host moving it at the same moment refuses
            # nothing the push made, and the next fetch sets it.
            git(repo, "update-ref", f"refs/crew/{ref}", sha, check=False)
            READ.keep_tip(repo, ref, sha)
            return sha
        if was_stopped(r):
            # No refusal of the branch: the push may have landed, so it is never made again here, and the next read
            # fetches to see (weir C.3).
            READ.forget_tip(repo, ref)
            fail(f"the push of {ref} to {repo} failed: {r.stderr.strip()}; it is not pushed again, and the next write reads "
                 "whether it landed")
        if n < REPLAYS:  # the last refusal waits for no replay, and is still fetched to tell a moved branch
            import random  # here, as the module's rarer imports are: only a refused push draws
            wait = replay_wait(n, random.random())
            time.sleep(wait)
            waited += wait
        moved = tip_of(repo, ref, fresh=True)
        if moved == tip:
            fail(f"the push of {ref} to {repo} failed: {r.stderr.strip()}")
        tip = moved
    fail(f"{ref} of {repo} kept moving: the write was applied {1 + REPLAYS} times, waiting {waited:.1f} s in all between "
         "them, and each push was refused")


def agent():
    """Who is writing: the agent crew started (CREW_AGENT), or the role's run the command's Flume place is, named as
    the role (crew.caller), else the user at this host."""
    import getpass
    return crew.caller() or f"{getpass.getuser()}@{crew.this_host()}"


# ---------------------------------------------------------------------------------------------------- the plan

def state_of(fleet, label):
    """A drive's state repository and its branch there: <owner>/<name> and <label>/main."""
    return crew.drive_of(fleet, label)["state"], f"{label}/main"


def read(repo, ref, tip):
    """plan.rec at a commit of a branch, refused when it fails its schema, naming the commit; a blob the follower kept
    as passing is not checked again."""
    text = show(repo, tip, "plan.rec")
    text is not None or fail(f"{ref} of {repo} at {tip[:7]} has no plan.rec")
    blob = (kept_listing(repo, tip) or {}).get("plan.rec")
    if blob is None or blob not in READ.follower.checked:
        try:
            recfix(text, "plan.rec")
        except Refusal as e:
            fail(f"{ref} of {repo} at {tip[:7]}: {e}")
        if blob is not None:
            READ.follower.checked.add(blob)
    return Plan(text)


def removed_by(repo, tip, kind, name):
    """The commit that removed a record, for a write whose subject is gone."""
    out = git(repo, "log", "-1", "--format=%h %s", "-G", f"^{kind}: {re.escape(name)}$", tip, "--", "plan.rec")
    return out or None


class Write:
    """What a change sees: the drive's state at the tip it is applied to (the plan, and any other file it reads or
    replaces), and how to refuse with the commit that removed something."""

    def __init__(self, repo, label, tip, plan):
        self.repo, self.label, self.tip, self.plan, self.subject = repo, label, tip, plan, None
        self.files = {}  # every other file the change replaced, {path: text}, committed with the plan
        self.on, self.frm = [], []  # objects only the change can name, for the write's run-record entry
        self.asked, self.held = [], []  # the asks the change wrote in its commit (ask_lines), and the keys it found held
        # the act its entry is, where the change decides it at the tip it is applied to, and each further entry of its
        # one commit, (id, act, on, fields), its fields with its "why" and "frm" where it has its own and its id None
        # where the write makes it, carried in the commit and named there beside the act's (carried)
        self.act, self.also = None, []
        self.why, self.fields = None, {}  # the entry's Why and fields where only the tip the change is applied to says them
        self.renaming = []  # each rename this write makes, (old, new), through which appended reads requests.rec

    def text(self, path):
        """A file of the branch as the change has left it: replaced, else at the tip, else None."""
        return self.files[path] if path in self.files else show(self.repo, self.tip, path)

    def paths(self, prefix):
        """The branch's files under prefix as the change has left them: at the tip (paths_at), with any it added, sorted."""
        return sorted(set(paths_at(self.repo, self.tip, prefix) if self.tip else []) | {p for p in self.files if p.startswith(prefix)})

    def texts(self, paths):
        """Files of the branch as the change has left them (text), those at the tip read in one cat-file, as landings_at reads
        the run record whole (plan.12); None for one that is not there."""
        at = [p for p in paths if p not in self.files]
        got = dict(zip(at, cat_file(self.repo, [f"{self.tip}:{p}" for p in at]) if at and self.tip else [None] * len(at)))
        return [self.files[p] if p in self.files else got[p] for p in paths]

    def replace(self, path, text):
        self.files[path] = text

    def runners(self):
        """The drive's runners as this command read them beside the plan, each at its branch's tip (runners)."""
        return runners(self.repo, self.label)

    def taker(self, launch):
        """The host whose runner took a launch, as this command read the runners (runner.taken), or None while crew
        can't tell or none has."""
        reading = runner.taken(self.runners(), runner.number(launch.get("Request")))[0] if launch is not None else None
        return reading["host"] if reading else None

    def entries(self):
        """The drive's run record from BATCH_DAYS back as the branch holds it at the tip the change is applied to,
        each entry once, oldest first, as drive_entries reads it from the branch's tip (read.5), so a check of it
        is made again on each replay (plan.1)."""
        if getattr(self, "_entries", None) is None:
            since = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=BATCH_DAYS)).isoformat()
            seen = {}
            for e in record.at(self.repo, self.tip, since):
                seen.setdefault(e["Id"], e)
            self._entries = sorted(seen.values(), key=lambda e: (e["At"], e["Id"]))
        return self._entries

    def kits(self):
        """The drive's kits (drive_kits), in the plan as the change has left it so far, with the landings the
        run record holds at the tip it is applied to."""
        return drive_kits(self.plan, landings_at(self.repo, self.tip) if self.tip else [])

    def bolt(self, name):
        return self.plan.bolt(name) or self.gone("Bolt", name)

    def unit(self, name):
        return self.plan.unit(name) or self.gone("Unit", name)

    def item(self, name):
        """The unit or chore by that name, which a command's After or --before may name either way round."""
        return self.plan.item(name) or self.gone("Unit", name, "unit or chore")

    def of(self, a):
        """The unit or chore a unit or chore command names (a.unit), refused when it is of the other kind (plan.11)."""
        u = self.plan.item(a.unit) or self.gone("Unit", a.unit, a.cmd)
        why = kind_refusal(kind_of(u), a.cmd, a.sub, a.unit)
        return u if not why else fail(why)

    def gone(self, kind, name, word=None):
        by = removed_by(self.repo, self.tip, kind, name)
        fail(f"no {word or kind.lower()} {name} in {self.label}/main of {self.repo}" + (f": {by} removed it" if by else ""))


def message(subject, body, eid):
    """A commit message: the subject, the body where there is one, and the Crew-Entry trailer naming the run-record
    entry that describes the commit, or one trailer for each of several, an act's and each ask written with it."""
    eids = [e for e in (eid if isinstance(eid, list) else [eid]) if e]
    return subject + (f"\n\n{body}" if body else "") + ("\n\n" + "\n".join(f"Crew-Entry: {e}" for e in eids) if eids else "") + "\n"


def unacted(act, subject):
    """Why a plan write is refused before it reads or pushes anything, or None (plan.2, read.5): it names no act, so
    its commit would name a run-record entry that nothing writes."""
    if act:
        return None
    return (f"crew does not write \"{subject}\": a write names its act, whose run-record entry its commit names and the "
            "write itself records, and this one names none (plan.2)")


def write(fleet, label, change, subject, body="", act=None, on=(), frm=(), fields=None, by=None, why=None):
    """Apply change(Write) to the tip of the drive's branch, its plan's record descriptors first brought in step
    with crew's, commit every file it changed, each checked first, and push, replaying on a refused push. change returns the bolts it touched.
    Every write is an act (plan.2), and its commit carries the act's run-record entry (carried): naming on and frm and
    whatever the change added to them, with the act's own fields, added to this host's runs/<host>/<day>.rec in the
    commit's own files and made again on each replay (state.1), so the branch never holds the act without its entry
    (read.5); one given no act is refused before anything is read or pushed (unacted), since its commit would name an
    entry nothing writes. by, the role an act of crew's own is in the name of, and why, the entry's Why in place of the
    subject's, which the change may give instead, with fields of its own, where only the tip it is applied to says them
    (Write). Each ask the change wrote in its commit (ask_lines) and each further act of it (Write.also) has its entry
    carried and named beside the act's; a key the change found held is said. No carried entry names a commit, the one
    carrying it being its commit. Once the push is accepted, each carried entry is appended to this host's own file
    (record.append, record.4), and what of the host's entries a refused push left is pushed after it, each a commit of
    its own (record.reach, said: a refusal of those is said once and changes nothing, record.2). Returns the commit."""
    unacts = unacted(act, subject)
    not unacts or fail(unacts)
    repo, ref = state_of(fleet, label)
    seen = {"eid": record.new_id()}
    CONTEXT.update(label=label)

    def make(tip):
        tip or fail(f"{repo} has no {ref} yet: crew state init {label}")
        w = Write(repo, label, tip, read(repo, ref, tip))
        in_step(w.plan)
        touched = change(w) or []
        base_drops(w)
        check(w.plan)
        if "requests.rec" in w.files:
            appended(w)
        seen.update(touched=touched, label=label, subject=f"{w.subject or subject} ({agent()})", held=w.held)
        own = dict(act=w.act or act, on=list(on) + w.on, frm=list(frm) + w.frm, why=why or w.why or record.subject(seen["subject"]),
                   **{**(fields or {}), **w.fields})
        seen["day"], seen["carried"] = carried(w, label, seen["eid"], own, by)
        seen["asked"] = w.asked
        files = {"plan.rec": w.plan.text(), **w.files}
        return files, message(seen["subject"], body, [eid for eid, _ in seen["carried"]])
    sha = land(repo, ref, None, make)
    print(f"{ref} {sha[:7]}: {seen['subject']}")
    for _, lines in seen["carried"]:
        record.append(label, seen["day"], lines)
    record.reach(label, said=True)
    asked(label, seen["asked"], seen["held"])
    return sha


def carried(w, label, eid, own, by=None):
    """The entries a write's commit carries (plan.2, read.5), composed at the tip it is applied to (state.1): its act's,
    by eid, from own (record.fields_of's act, on, frm, why and fields), then each ask's the change wrote (ask_lines) and
    each further act's (Write.also), each further act's Why its own or else the act's, and its id the one the change
    made or else one made here; each by this host, at this
    moment, naming no commit. They are added to this host's day file of that moment in the write's own files, as the
    change left it (Write.text), by record.with_entries. Returns the day and [(id, lines)], the act's first."""
    now = datetime.datetime.now(datetime.timezone.utc)
    entries = [(eid, record.fields_of(eid, now, by=by, **own))]
    for e, rec in w.asked:
        entries.append((e, record.fields_of(e, now, **record.ask_entry(f"{label}-{rec.get('Role')}", rec.get("What"), rec.get("Names"),
                                                                        rec.get("Words")))))
    for e, act, on, more in w.also:
        e = e or record.new_id()  # an id the change left to the write, made in the order of its acts
        rest = {k: v for k, v in more.items() if k not in ("why", "frm")}
        entries.append((e, record.fields_of(e, now, act, on, more.get("frm") or [], why=more.get("why") or own["why"], by=by, **rest)))
    lines = [(e, record.entry_text(f)) for e, f in entries]
    day = now.date().isoformat()
    path = f"runs/{crew.this_host()}/{day}.rec"
    w.replace(path, record.with_entries(w.text(path), dict(lines)))
    return day, lines


def base_drops(w):
    """A plan write's own ask again of each base place whose drop the runner refused, once no piece of its bolt is live
    (runner.base_drop_due; crew-lands-each-bolt-through-flumes-base-place, Decision 8), appended in the write's commit;
    nothing on a branch with no requests.rec, the runners read only where a bolt gone from the plan has a drop of its
    launch asked (runner.base_drop_asked), so a write that drops no bolt reads none, and nothing where its runners can't
    be read (read.1)."""
    if w.text("requests.rec") is None:
        return
    requests = requests_of(w).recs("Request")
    if not runner.base_drop_asked(w.plan, requests):
        return
    try:
        reads = w.runners()
    except Refusal:
        return
    for act, work, given in runner.base_drop_due(w.plan, requests, reads):
        request(w, act, work, **given)


def requests_of(w):
    """requests.rec of the drive as the write has it, its descriptor in step with crew's (runner.REQUESTS), or a new
    one when the branch has none yet (Decision 4 of teams-cross-to-flume-as-their-bolts-land)."""
    text = w.text("requests.rec")
    rq = Plan(text if text is not None else runner.REQUESTS)
    in_step(rq, runner.REQUESTS)
    return rq


def request(w, act, work, **given):
    """A request of the runners (act, launch, retry, drop, priority, preview or confirm, for work, with the fields given as
    runner.request_fields takes them) appended to requests.rec in the write's own commit, beside the plan write that
    occasions it and under its one Crew-Entry (state.1, plan.2): numbered the next, dated now and by the writer, and
    checked by crew's own rules (runner.request_refusal) before land checks the file by recfix with every other the
    commit holds. Returns its number."""
    rq = requests_of(w)
    have = rq.recs("Request")
    n = runner.next_request(have)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec = Rec("Request", runner.request_fields(n, act, work, given, now, agent()))
    why = runner.request_refusal(have, rec)
    why is None or fail(why)
    rq.insert(rec)
    w.replace("requests.rec", rq.text())
    return n


def appended(w):
    """A write that changes requests.rec only appends to it (runner.append_refusal): its requests at the tip the write
    is applied to stand unchanged, in order, ahead of those it adds, but for each rename the write makes (w.renaming),
    through which the tip's requests are read, so a request changes by its repository's name alone and only in a
    rename's write (Decision 6 of a-repository-is-renamed-by-one-explicit-command); refused otherwise."""
    why = appended_refusal(show(w.repo, w.tip, "requests.rec") or "", w.files["requests.rec"], w.renaming)
    why is None or fail(why)


def appended_refusal(was, now, renaming=()):
    """Why requests.rec's text now is no append to its text at the tip (was), or None (runner.append_refusal), was read
    through each rename of renaming, (old, new) in order, as the write's rename left it (rename_rec)."""
    for old, new in renaming:
        was = rename_rec(was, RENAMED_FIELDS["requests.rec"], old, new)[0]
    return runner.append_refusal([r.fields for r in Plan(was).recs("Request")], [r.fields for r in Plan(now).recs("Request")])


def either(rows):
    return rows[0] if len(rows) == 1 else ", ".join(rows[:-1]) + " or " + rows[-1]


def push_now(fleet, label):
    """crew events --push: each entry of the host's run record of the label that its branch lacks, which a push that
    was refused left in the host's file, pushed now, each as its own commit (record.reach); said when there is none."""
    ref, host = state_of(fleet, label)[1], crew.this_host()
    n = record.reach(label)
    print(f"{ref}: pushed {n} of {host}'s entries" if n else f"{ref}: nothing of {host}'s run record left to push")


# --------------------------------------------------------------------------------------------- crew state init

def state_init(fleet, a):
    """Create the drive's branch, adopting what the drive had: the first blueprints repo's plan/<label> is
    pushed as the branch, so the plan's history is the branch's, else the branch starts with an empty plan; each other
    blueprints repo's plan/<label> is joined in one commit naming where it came from; the plan's record descriptors are
    brought in step with crew's; then moves.rec, with the first blueprints repo's moves. Every step is its own push and first checks whether the branch already shows it, so a
    run that stopped partway is finished by running it again, and a finished branch is only reported. Returns what it
    did, {"repository", "branch", "tip", "outcome", "did"}: made where the branch was not there, finished where it
    stood and a step was taken, exists where none was; its caller says it (crew.state_said)."""
    p = crew.drive_of(fleet, a.label)
    label = p["label"]
    repo, ref = state_of(fleet, label)
    CONTEXT["label"] = label
    # What the drive had, read whole before anything is pushed.
    old = []
    for bp in p["blueprints"]:
        t = tip_of(bp, f"plan/{label}")
        if t:
            old.append((bp, t, read(bp, f"plan/{label}", t)))
    shared = shared_name(label, [(bp, plan) for bp, _, plan in old])
    shared is None or fail(shared)
    first = old[0] if old and old[0][0] == p["blueprints"][0] else None
    joins = [o for o in old if o is not first]
    did = []
    tip = tip_of(repo, ref)
    absent = tip is None
    if tip is None:
        if first:
            bp, t, _ = first
            r = git(bp, "push", "--quiet", url(repo), f"{t}:refs/heads/{ref}", check=False)
            r.returncode == 0 or fail(f"could not push plan/{label} of {bp} to {repo} as {ref}: {r.stderr.strip()}")
            tip = tip_of(repo, ref, fresh=True)
            did.append(f"adopted plan/{label} of {bp} at {t[:7]}, with its history")
            record.emit(label, "state.init", [f"plan/{label}"], commit=[f"{repo}@{tip}"], why=f"state({label}): adopt plan/{label} of {bp}")
        else:
            tip = init_step(repo, ref, label, f"state({label}): start the drive's plan",
                            lambda w_tip, files: files.update({"plan.rec": HEADER}) if w_tip is None else fail(f"{repo} has {ref} since {w_tip[:7]}"))
            did.append("started an empty plan")
    for bp, t, plan in joins:
        mark = f"join plan/{label} of {bp} at {t[:7]}"
        if git(repo, "log", "--format=%h", "-F", f"--grep={mark}", tip):
            continue

        def join(w_tip, files, bp=bp, plan=plan):
            have = read(repo, ref, w_tip)
            joined_into(have, plan, bp, f"{ref} of {repo}", label)
            files["plan.rec"] = have.text()
        tip = init_step(repo, ref, label, f"state({label}): {mark}", join)
        did.append(f"joined plan/{label} of {bp} at {t[:7]}")
    if in_step(read(repo, ref, tip)):
        def step(w_tip, files):
            have = read(repo, ref, w_tip)
            in_step(have)
            files["plan.rec"] = have.text()
        tip = init_step(repo, ref, label, f"state({label}): the plan's record descriptors in step with crew's", step)
        did.append("brought the plan's record descriptors in step with crew's")
    if show(repo, tip, "moves.rec") is None:
        src = p["blueprints"][0]
        st = tip_of(src, "main")
        moves = show(src, st, "signals/moves.rec") if st else None
        recs = Plan(moves).recs("Move") if moves else []
        at = f" at {st[:7]}" if moves else ""

        def start_moves(w_tip, files):
            show(repo, w_tip, "moves.rec") is None or fail(f"{ref} of {repo} has moves.rec since {w_tip[:7]}")
            files["moves.rec"] = moves_file(recs)
            if show(repo, w_tip, "proposals.rec") is None:
                files["proposals.rec"] = PROPOSALS
        tip = init_step(repo, ref, label, f"state({label}): moves.rec, with the {len(recs)} moves of {src}'s signals/moves.rec{at}", start_moves)
        did.append(f"added moves.rec with {len(recs)} moves of {src}{at}")
    return {"repository": repo, "branch": ref, "tip": tip, "outcome": "made" if absent else "finished" if did else "exists", "did": did}


def state_init_cmd(fleet, a):
    """crew state init <label>: the drive's branch made or finished (state_init), and what was done said."""
    print(crew.state_said(state_init(fleet, a)))


# ------------------------------------------------------------------------------------------- crew drive set

def drive_set(a):
    """crew drive set <label> (drive-setup; design of crew-makes-a-new-drives-state, Decision 6): the drive its flags
    give (crew.drive_given), how each of its roles runs by --runs and its batch setting by --review, named in this
    host's teams file and its state made, run on the host it is invoked on and
    never forwarded (Decision 11), before any teams file is loaded. The flags are checked first; then <label>/main of
    the state repository is fetched, refused naming the repository where crew cannot fetch from it, nothing written
    (read.1); then, under a lock on the file's folder, the file is read, decided on (crew.teams_step) and written by a
    new file renamed over it (teams.9), a file crew cannot read at all linked to its aside first, which a taken aside
    refuses, and a file at crew's own version never moved aside: the set mends what it replaces there, the file written
    wherever the file it would write passes every check, and refused with nothing written where a check still fails or
    a part of it is of a shape the set cannot keep (record 0065, point 8; crew.teams_step). Once the file names the
    drive as given, where a key of it changed, one drive.set entry naming each by its path is appended to this host's
    run record at once, without a push of its own, since a new drive has no branch yet to take it (Decision 10;
    a-drive-set-loses-no-drive-and-no-record, Decision 3); then crew loads the file afresh and the state is made by
    crew state init's own steps (state_init), whose first write pushes every entry the branch lacks, the set's first,
    a refusal from here on the state's, in crew.state_unmade's words (Decision 4); and last, every entry of this
    host's record of the drive the branch still lacks is pushed, a refused push said once and changing nothing of the
    answer (Decision 5). So a run again after a state not made finishes it and puts the first run's entry on the
    branch. Its answer is crew.drive_said's."""
    here = crew.this_host()
    given = crew.drive_given(a, here)
    label, teams = a.label, crew.TEAMS
    CONTEXT["label"] = label
    tip_of(given["drive"]["state"], f"{label}/main")
    aside = crew.aside_of(teams)
    teams.parent.mkdir(parents=True, exist_ok=True)
    with open(teams.parent / ".teams.lock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        linked = teams.is_symlink()
        step = crew.teams_step({"linked": linked, "target": os.readlink(teams) if linked else None,
                                "text": teams.read_bytes() if teams.exists() else None, "aside_taken": os.path.lexists(aside),
                                "given": given, "here": here})
        if step["step"] in ("write", "aside"):
            new = teams.with_name(f"{teams.name}.{os.getpid()}.new")
            new.write_text(step["text"])
            if step["step"] == "aside":
                try:
                    os.link(teams, aside)
                except FileExistsError:
                    new.unlink()
                    fail(f"{aside}, where crew drive set moves a teams file it cannot read at all once, is taken: {teams} and it are "
                         "left as they are, and nothing was written")
            os.replace(new, teams)
    crew.load.cache_clear()
    CONTEXT["teams_done"] = True
    changed = step.get("changed") or []
    eid = record.emit(label, "drive.set", [f"drive/{label}"], why="set " + ", ".join(changed), push=False) if changed else None
    try:
        st = state_init(crew.load(), a)
    except Refusal as e:
        fail(crew.state_unmade(label, str(e)))
    record.reach(label, eid, said=True)
    outcome = {"write": "written", "aside": "written", "unchanged": "unchanged", "linked": "linked"}[step["step"]]
    done = {"label": label, "state": st,
            "teams": {"file": str(teams), "outcome": outcome, "aside": str(aside) if step["step"] == "aside" else None,
                      "reason": step.get("reason"), "target": step.get("target"), "changed": changed}}
    print(crew.drive_said(done, a.json))


def drive_set_refused(a, e):
    """A refused crew drive set, in the drive's run record where the teams file loads and names the drive, as any
    refused command's is; elsewhere said alone, there being no drive's record to hold it (Decision 10). Once the teams
    step is done, the file naming the drive as given, the refusal is the state's: a refused state.init on
    plan/<label>, the act crew state init's steps record, beside the set's own entry, which records the set done
    (record.1; a-drive-set-loses-no-drive-and-no-record, Decision 4)."""
    if CONTEXT.get("teams_done"):
        record.emit(a.label, "state.init", [f"plan/{a.label}"], refused=str(e))
        return
    try:
        fleet = crew.load()
    except Refusal:
        return
    if a.label in fleet["drives"]:
        refused(fleet, a, ("drive", "set"), e)


def shared_name(label, plans):
    """Why the drive's plans can't be adopted together, or None: two of them, [(blueprints repo, plan)], hold a
    bolt, or a unit or chore, by the same name."""
    owner = {}
    for bp, plan in plans:
        for r in plan.bolts() + plan.work():
            other = owner.setdefault((r.kind, r.name()), bp)
            if other != bp:
                return (f"plan/{label} of {other} and plan/{label} of {bp} both hold {r.kind.lower()} {r.name()}: "
                        "rename one in its plan first; nothing was written")
    return None


def joined_into(have, plan, bp, where, label):
    """Another blueprints repo's plan joined into the branch's (have): each bolt and unit added, a Source naming no repo
    made to name bp, refused when the branch (where) already holds one by that name; then crew's own rules checked."""
    for r in plan.bolts() + plan.work():
        (have.bolt if r.kind == "Bolt" else have.item)(r.name()) is None or fail(
            f"{where} already holds {r.kind.lower()} {r.name()}, which plan/{label} of {bp} also holds; nothing was joined")
        have.insert(Rec(r.kind, [(n, v if n != "Source" or ":" in v else f"{bp}:{v}") for n, v in r.fields]))
    check(have)


def moves_file(recs):
    """A new moves.rec: crew's descriptor, then each move it starts with."""
    return MOVES + "".join("\n" + "\n".join(r.lines()) + "\n" for r in recs)


def init_step(repo, ref, label, subject, make_files):
    """One step of crew state init: make_files(tip, files) fills the commit's files at the tip (None when the branch
    is not there yet), pushed without force and replayed on a moved tip. The step's commit carries its state.init
    entry, naming no commit, as a plan write carries its act's (write, carried): added to this host's day file at the
    tip, made again on each replay, appended to the host's own file once the push is accepted, and the host's kept
    entries pushed after it. An adoption of another branch's history, which pushes commits crew did not make, records
    its entry as a commit of its own instead (state_init)."""
    eid = record.new_id()
    seen = {}

    def make(tip):
        files = {}
        make_files(tip, files)
        now = datetime.datetime.now(datetime.timezone.utc)
        lines = record.entry_text(record.fields_of(eid, now, "state.init", [f"plan/{label}"], why=subject))
        path = f"runs/{crew.this_host()}/{now.date().isoformat()}.rec"
        files[path] = record.with_entries(files[path] if path in files else show(repo, tip, path) if tip else None, {eid: lines})
        seen.update(day=now.date().isoformat(), lines=lines)
        return files, message(f"{subject} ({agent()})", "", eid)
    sha = land(repo, ref, None, make)
    record.append(label, seen["day"], seen["lines"])
    record.reach(label, said=True)
    return sha


# ------------------------------------------------------------------------------------------ the kits, per host

GATHER = (LIB / "gather.py").read_text()
LATER = ("code", "verify", "merged", "landed")


def gathered(fleet, host, req):
    """gather.py's answer to a request on a host, and None; or None and the last line of why it failed. On this host
    it is read in this process, as the same JSON, sparing a Python start each read; on another it is piped to that
    host's python3, since its crew may be older (code.1)."""
    if host == crew.this_host():
        if os.environ.get("CREW_TEST_READS"):  # crew's tests count a command's reads of the kits, a piped one by its python3
            with open(os.environ["CREW_TEST_READS"], "a") as f:
                f.write(f"{host} {'stamp' if req.get('stamp') else 'gather'}\n")
        try:
            running = gather.routes() if req.get("sites") and not req.get("stamp") else None
            return json.loads(json.dumps(gather.read(req, running))), None
        except Exception as e:
            import traceback
            return None, traceback.format_exception_only(e)[-1].strip()
    r = crew.on_machine(fleet, host, ["python3", "-", json.dumps(req)], input=GATHER)
    if r.returncode:
        return None, ((r.stderr or "").strip().splitlines() or [f"exit {r.returncode}"])[-1]
    return json.loads(r.stdout), None


def stamped(fleet, host, kits, labels=(), routes=False):
    """Each kit's stamp on a host (gather.stamp) and the stamp of its card readings folders of the drives named
    (gather.readings_stamp), {"kits": {main: stamp}, "readings": stamp}, a stamp None when it can't be read, and None;
    or None and why the host did not answer: in this process on this host, which starts nothing, and in one ssh to
    another, the follower's check that nothing moved there (plan.12). At the follower's clock's tick, with routes, it
    also asks the host's portless routes, {"routes": routes}: one portless here, and the same ssh there. It asks no
    sluice."""
    return gathered(fleet, host, {"kits": kits, "stamp": True, "labels": sorted(labels), **({"routes": True} if routes else {})})


def survey(fleet, held, sites=False, board=False, fetch=False):
    """Read the kits of every host holding active bolts, one call per host. held is [(where, bolt)], where a bolt's work
    runs as the runner that took it reported (bolt_at, its host and the kit's folder there), bolt None for the kit
    alone. The answer is per host: its kits by folder, or why it did not answer. With sites, each worktree's devurl
    names and the host's running portless routes too; board implies sites and adds the explorations on each kit's main,
    for the board. With fetch, each kit's GitHub is fetched on its host before it is read, for a read a decision of the moment
    rests on (plan.18, plan.19), and a fetch that fails reads that kit unread with git's words; a kit in the runner's
    clone, which crew fetches nothing in, is read as the runner last fetched it (crew.fetches_in). A kit the command has
    already read for every bolt asked of it is not asked again, but by a survey that fetches, which must read after its
    own fetch; what a host answers is kept for the command's later steps; a sites survey is neither served nor kept,
    but in the host's follower's board survey, which serves each kit whose stamp and request have not moved from what it kept
    (Kept.served) and asks each host only for the rest, its answers stamped."""
    sites = sites or board
    hosts = {}
    for t, bolt in held:
        kt = t["kit"]
        # a kit in the runner's clone is read as the runner last fetched it, with no fetch (crew.fetches_in)
        asked = {"fetch": crew.fetches_in(fleet, t["machine"], kt["main"])} if fetch else {}
        k = hosts.setdefault(t["machine"], {}).setdefault(kt["main"], {"main": kt["main"], "dir": kt["dir"], "bolts": [], **asked})
        if bolt and bolt not in k["bolts"]:
            k["bolts"].append(bolt)
    out, kept = {}, READ.follower if board and not fetch else None  # the follower's read is the board's survey
    for host, kits in sorted(hosts.items()):
        # a kit already read serves only a read of the bolts it was read for: one asked for another bolt is read again
        have = {} if sites or fetch else {m: k for m, k in READ.kits(host).items()
                                          if m in kits and all(b in (k.get("bolts") or {}) for b in kits[m]["bolts"])}
        if kept is not None:
            have.update({m: a for m, k in kits.items() if (a := kept.served(host, m, k)) is not None})
            for m in have:
                kept.use(host, m, kits[m], have[m])
        ask = [k for m, k in kits.items() if m not in have]
        if ask:
            req = {"kits": list(ask), "sites": sites,
                   **({"board": True} if board else {}), **({"stamped": True} if kept is not None else {})}
            got, error = gathered(fleet, host, req)
            for k in ask if kept is not None else ():
                kept.use(host, k["main"], k, None if error else got.get(k["main"]))
            if error:
                out[host] = {"ok": False, "error": error}
                continue
            if not sites:
                READ.keep_kits(host, {m: k for m, k in got.items() if k.get("ok")})
            have.update(got)
        out[host] = {"ok": True, "kits": have}
    return out


def amended(mark):
    """Whether a unit's Amended mark waits for construct to be run again: proposal/<n> or intent. Any other mark is
    the head of unit/<unit> when construct started again."""
    return mark == "intent" or (mark or "").startswith("proposal/")


# The stages at which a unit has finished construct: its change is committed, and a unit after it may be constructed.
CONSTRUCTED = ("planned", "code", "verify", "merged", "landed")


# The stages at which a chore has something committed to build on: its code has delivered its commits (plan.11).
CODED = ("verify", "merged", "landed")


def built_on(kind, stage):
    """Whether a unit or chore it comes after has something committed for the dependent to build on (plan.13): a unit
    its change, once construct has finished; a chore its code, once its commits are in its place."""
    return stage in (CODED if kind == "chore" else CONSTRUCTED)


def after_met(deps):
    """Whether a unit's or chore's After is met, from each one it names as (its kind, its stage): each has something
    committed to build on (built_on), never waiting on a merge (plan.13), whichever kind the dependent is. None while
    one's stage is unknown (read.1)."""
    if any(s == "unknown" for _, s in deps):
        return None
    return all(built_on(k, s) for k, s in deps)


def chore_stage(name, bolt, k, pl):
    """A chore's stage in a bolt its team holds, read from the kit as gathered (k) and its place (pl, None when it has
    none), or None when it has no place and its stage is ready or waiting (state.2, plan.11): landed once main's history
    holds its trailer, merged once the bolt's does; verify once its place holds a commit beyond the bolt, code while it
    holds none; unknown when its place tracks no bolt crew can read. Returns (stage, why)."""
    if name in k.get("chores", []):
        return "landed", None
    if name in k["bolts"].get(bolt, {}).get("chores", []):
        return "merged", None
    if not pl:
        return None, None
    if pl.get("ahead") is None:
        return "unknown", f"chore {name}'s place {pl['path']} tracks no bolt crew can read"
    return ("verify" if pl["ahead"] else "code"), None


class Stages:
    """Each unit's and chore's stage. Work with no bolt is queued; work of a bolt not started is ready or waiting by
    whether its After is met (after_met); and a unit or chore of a started bolt (Path: flume, started) reads its stage
    from the runner's records alone, never from a place in the kit, landed once main holds it, and unknown where the
    runner that took it can't be read or told (crossed; Decision 8 of teams-cross-to-flume-as-their-bolts-land), the
    plan's drive's (label) requests and runners read once for the command beside its plan (runs, {label: (requests,
    readings)} as runner_facts reads them, read when first needed where not given; plan.12), and its kit read where
    the runner that took its work reported it (at, bolt_at)."""

    def __init__(self, fleet, plan, survey, runs=None, label=None):
        self.fleet, self.plan, self.survey, self.memo, self.runs, self.label = fleet, plan, survey, {}, dict(runs or {}), label

    def runner(self, label):
        """The drive's requests and its runners as read (runner_facts), or why they could not be read."""
        if label not in self.runs:
            try:
                self.runs[label] = runner_facts(self.fleet, label)
            except Refusal as e:
                self.runs[label] = str(e)
        return self.runs[label]

    def crossed(self, name, u, bolt, res):
        """A started piece's stage (runner.stage_of) from its newest launch not dropped, the answer of the runner that
        took it and its place's record there (runner.piece_stage): unknown where its drive's runners can't be read,
        or it has no launch, as stage_of says; merged once its place has landed on its bolt, and landed once main holds
        it, a unit's change archived there or a chore's trailer, as today's do. It has no worktree in the kit, flume
        holds the whole of stage_of's answer, which the views show (runner.piece_said), and carried when the runner
        carried its place's status, which a batch reads it at (crossed_changes). Its end is the runner's report alone,
        the record Flume holds for the runner after it tidies the place among them, and no landing commit on its bolt is
        read for it (bolt-plan "A tidied place reads as the record Flume holds of it for the runner"; crew record 0056 point 4)."""
        run, work = self.runner(self.label), runner.work_of(u)
        if isinstance(run, str):
            s = runner.stage_of(work, None, None, None, f"crew can't read {self.label}'s requests or runners: {run}")
        else:
            requests, reads = run
            launch = runner.launch_of(requests, work)
            s = runner.piece_stage(requests, reads, launch) if launch is not None else runner.stage_of(work, None, None, None, True)
            n = runner.number(launch.get("Request")) if launch is not None else None
            reading = runner.taken(reads, n)[0] if launch is not None else None
            place = reading["places"].get(n) if reading else None
            res["carried"] = place["at"] if place else None  # when the runner carried its place's status
        k, _ = self.kit(bolt) if not isinstance(run, str) else (None, None)
        if s["stage"] == "merged":
            if k and name in (k.get("chores", []) if is_chore(u) else k["main"]):
                s = dict(s, stage="landed")
        res.update(stage=s["stage"], tasks=s.get("tasks"), flume=s, **({"why": s["why"]} if s.get("why") else {}))
        return res

    def base(self, bolt):
        """A started bolt's base place's stage (runner.stage_of of bolt/<bolt>; crew-lands-each-bolt-through-flumes-base-place,
        Decisions 3 and 9), from its newest launch not dropped as the runner that took it answers it (runner.piece_stage):
        unlaunched with the runner's words while it is not launched; legacy, with runner.legacy_said's words, for a bolt
        with no launch of its own, started before bolts were base places; unknown where its drive's runners can't be
        read; None for a bolt not started."""
        if not started(bolt):
            return None
        run = self.runner(self.label)
        if isinstance(run, str):
            return {"stage": "unknown", "why": f"crew can't read {self.label}'s requests or runners: {run}"}
        requests, reads = run
        launch = runner.launch_of(requests, f"bolt/{bolt.name()}")
        if launch is None:
            return {"stage": "legacy", "words": runner.legacy_said(bolt.name())}
        return runner.piece_stage(requests, reads, launch)

    def landing(self, bolt):
        """A started bolt's landing as the runner reports it (runner.landing_of; crew-lands-each-bolt-through-flumes-base-
        place, Decisions 6 and 10), from its base place's launch and its lands: {outcome, ...}; {outcome: legacy, words}
        for a bolt started before bolts were base places (runner.legacy_said); unknown where the drive's runners
        can't be read; None for a bolt not started."""
        if not started(bolt):
            return None
        run = self.runner(self.label)
        if isinstance(run, str):
            return {"outcome": "unknown", "why": f"crew can't read {self.label}'s requests or runners: {run}"}
        requests, reads = run
        launch = runner.launch_of(requests, f"bolt/{bolt.name()}")
        if launch is None:
            return {"outcome": "legacy", "words": runner.legacy_said(bolt.name())}
        return runner.landing_of(launch, runner.lands_of(requests, launch), reads)

    def fixes(self, bolt):
        """Each fix standing on a started bolt, in requests.rec's order, as (its work, fix/<bolt>/<name>, its launch, its
        stage as stage_of gives it), read from the runner's records alone as its units and chores are, merged once the
        runner reports its place landed on the bolt, a record Flume holds for the runner among them (runner.fixes_on;
        bolt-plan "A fix the runner reports merged holds nothing"); none where the drive's runners can't be read,
        which unread names."""
        run = self.runner(self.label)
        if isinstance(run, str):
            return []
        return [(l.get("Work"), l, s) for l, s in runner.fixes_on(*run, f"bolt/{bolt.name()}")]

    def pieces(self, bolt):
        """A started bolt's units, chores and fixes as runner.verification takes them, [(work, its stage)], its units and
        chores in build order with their stages as crossed reads them, then its fixes as fixes reads them."""
        work = [(runner.work_of(u), self.of(u.name()).get("flume") or {"stage": self.of(u.name())["stage"]})
                for u in self.plan.work_of(bolt.name())]
        return work + [(w, s) for w, _, s in self.fixes(bolt)]

    def verification(self, bolt, head, landing=None):
        """A started bolt's verification at head, as read where it lives: whether that head is the landing of its work,
        as the runner reports it, or a landing sluice made on the bolt that passed, as its commit's trailers name it
        (landing, gather.head_landing of that head) (runner.verification over pieces; crew record 0056 points 1 and 4;
        record 0062 as amended 2026-11-10), as (state, words)."""
        return runner.verification(head, self.pieces(bolt), landing)

    def unread(self, bolt):
        """Why the runners a started bolt is read from can't be read, as (what, why), or None: its drive's requests,
        or, while crew can't tell where its work runs, a runner's branch of the drive missing or refused (read.1,
        read.3)."""
        run = self.runner(self.label)
        if isinstance(run, str):
            return f"the requests and runners of {self.label}", run
        if not run[1]:
            return f"{self.label}'s runners", (f"no runner answers for {self.label}: its state repository holds no "
                                               f"{self.label}/runner/<host>")
        if self.at(bolt)[0]:
            return None
        bad = [(f"{h}'s runner", r["why"]) for h, r in sorted(run[1].items()) if r["why"]]
        return bad[0] if bad else None

    def at(self, bolt):
        """Where a started bolt's work runs, as the runner that took it reported (bolt_at), or None, and why crew can't
        tell."""
        run = self.runner(self.label)
        if isinstance(run, str):
            return None, f"crew can't read {self.label}'s requests or runners: {run}"
        try:
            return bolt_at(self.fleet, self.label, bolt, run), None
        except Refusal as e:
            return None, str(e)

    def host(self, bolt):
        """The host a started bolt's work runs on, as its head line says it: where it runs (at), or, while the kit's
        folder there can't be told, the host of the runner that took the newest of its launches taken
        (runner.newest_taker), whose report or places crew reads it by; None where no runner has taken it or crew can't
        tell which did (read.1)."""
        t, _ = self.at(bolt)
        if t:
            return t["machine"]
        run = self.runner(self.label)
        if isinstance(run, str) or not started(bolt):
            return None
        took, _ = runner.newest_taker(run[1], bolt_launches(run[0], bolt.name()), f"bolt {bolt.name()}")
        return took["host"] if took else None

    def kit(self, b):
        """The bolt's kit as read where its work runs (at), with that place (at) and its host, or why it can't be."""
        t, why = self.at(b)
        if not t:
            return None, why or f"bolt {b.name()} is not started"
        h = self.survey.get(t["machine"])
        if not h or not h["ok"]:
            return None, f"{t['machine']} did not answer" + (f" ({h['error']})" if h else "")
        k = h["kits"].get(t["kit"]["main"])
        if not k or not k.get("ok"):
            return None, f"{t['machine']}: " + (k.get("error") if k else "the kit was not read")
        return dict(k, at=t, host=t["machine"]), None

    def of(self, name):
        if name in self.memo:
            return self.memo[name]
        u = self.plan.item(name)
        self.memo[name] = res = {"stage": "unknown", "tasks": None, "worktree": None, "open": [], "kind": kind_of(u)}
        b = u.get("Bolt")
        if not b:
            res["stage"] = "queued"
            return res
        bolt = self.plan.bolt(b)
        if started(bolt):
            return self.crossed(name, u, bolt, res)
        met = after_met([(self.of(a)["kind"], self.of(a)["stage"]) for a in u.all("After")])
        res["stage"] = "unknown" if met is None else "ready" if met else "waiting"
        return res

    def bolt_state(self, b):
        """A bolt's state: planned while it is not started (started); unknown when its kit can't be read; landed once every unit
        and chore has landed; else unknown when crew can't tell where the bolt is read (gather.bolt_read); waits, to
        land, once every one has merged and its head is the landing of its work, as the runner reports it (verification;
        teams.16); else active."""
        if not started(b):
            return "planned"
        k, _ = self.kit(b)
        if not k:
            return "unknown"
        units = self.plan.work_of(b.name())
        stages = [self.of(u.name())["stage"] for u in units]
        if units and all(x == "landed" for x in stages):
            return "landed"
        facts = k["bolts"].get(b.name(), {})
        if facts.get("error"):
            return "unknown"
        if units and all(x in ("merged", "landed") for x in stages) and self.verification(b, facts.get("head"), facts.get("head_landing"))[0] == "green":
            return "waits"
        return "active"


def stages_for(fleet, label, plan, bolts, fetch=False):
    """Stages for the units of the given bolts of a drive's plan, reading its runners once and only the hosts their
    work runs on (bolt_at), each kit's GitHub fetched first with fetch (survey); each piece's end is the runner's report,
    and nothing of a bolt's landing is sought."""
    try:
        run = runner_facts(fleet, label)
    except Refusal as e:
        return Stages(fleet, plan, {}, {label: str(e)}, label)
    held = [(t, b.name()) for b in bolts if started(b) for t in [known_at(fleet, label, b, run)] if t]
    return Stages(fleet, plan, survey(fleet, held, fetch=fetch), {label: run}, label)


# ------------------------------------------------------------------------------------------- finding the plans

def default_label(fleet, a):
    """The drive a command means: --label, else the agent's own (CREW_LABEL, or its run's: crew.caller_label),
    else none."""
    label = getattr(a, "label", None) or crew.caller_label(fleet)
    if label:
        crew.drive_of(fleet, label)
        CONTEXT.setdefault("label", label)
    return label


def plans(fleet, labels, errors=None):
    """(label, repo, tip, plan) for each drive's one plan, on its branch of its state repository, with tip and
    plan None where the branch is not started. A plan that can't be read is left out and its reason put in errors
    when that is given, else refused."""
    out = []
    for l in labels:
        repo = None
        try:
            repo, ref = state_of(fleet, l)
            tip = tip_of(repo, ref)
            out.append((l, repo, tip, read(repo, ref, tip) if tip else None))
        except Refusal as e:
            if errors is None:
                raise
            errors[f"{ref} of {repo}" if repo else f"the plan of {l}"] = str(e)
    return out


def locate(fleet, kind, name, label, word=None):
    """The one plan holding a bolt, or a record of the Unit set, a unit or a chore (said as word), by name."""
    labels, errors, word = [label] if label else list(fleet["drives"]), {}, word or kind.lower()
    hits = [h for h in plans(fleet, labels, errors) if h[3] and (h[3].bolt(name) if kind == "Bolt" else h[3].item(name))]
    hits or fail(f"no {word} {name} in the plans of " + ", ".join(labels)
                 + "".join(f"; {k} could not be read: {v}" for k, v in errors.items()))
    len(hits) == 1 or fail(f"{word} {name} is in more than one plan: " + ", ".join(f"{h[0]}/main of {h[1]}" for h in hits) + "; add --label")
    CONTEXT["label"] = hits[0][0]
    return hits[0]


def kit_labels(fleet, kit):
    """The drives whose kits (drive_kits, the repositories their plans and landings name) name a kit, by its
    name or forge address (kit_in), sorted; each branch read once for the command, and refused naming one that can't
    be read (read.1), since crew can't tell then whether it names the kit."""
    return [l for l in sorted(fleet["drives"]) if kit_in(kit, kits_read(fleet, l))]


def main_kit(fleet, label, kit):
    """Where crew acts on a kit before any runner has taken the work in hand (the user's ruling of 2026-11-01; Decision 4
    of the-team-machinery-leaves): the checkout the drive's main-level host keeps of it, as the teams file keeps it
    there (crew.kit_kept), in the shape bolt_at gives a bolt's, {"label", "machine", "stream" None, "kit"}; None where the
    host keeps none. A start's branch and checks, a new unit's name, a bolt never started landed, the design agent's
    records, a proposal's records and the board's explorations are read and acted on there."""
    host = crew.drive_of(fleet, label)["machine"]
    k = crew.kit_kept(fleet, host, kit)
    return {"label": label, "machine": host, "stream": None, "kit": k} if k else None


def main_kit_read(fleet, label, kit):
    """A kit's checkout on its drive's main-level host (main_kit) for a view, None where crew can't tell it, its
    teams file keeping none or two by the kit's name there: the board shows no explorations of it then."""
    try:
        return main_kit(fleet, label, kit)
    except Refusal:
        return None


def main_kit_said(fleet, label, kit, what):
    """Why crew can't act on a kit on its drive's main-level host (main_kit): that host keeps no checkout of it,
    and, since a kit renamed on its host is kept there by its new name alone, the way on when it was (Decision 2 of
    a-kit-renamed-on-its-host-is-renamed-across-the-plan)."""
    host = crew.drive_of(fleet, label)["machine"]
    return (f"{label}'s main level runs on {host}, and the teams file keeps no {kit} there, so crew can't {what}; if it was "
            f"renamed on its host, crew kit rename {kit} <new> names it so in the plan")


def kit_in(kit, kits):
    """Whether kits (drive_kits) name a kit, by its name or its forge address, <owner>/<name>, either way round."""
    return kit.split("/")[-1] in {k.split("/")[-1] for k in kits}


def renamed_kit(value, old, new):
    """A field's repository after a rename of old to new (Decision 1 of a-repository-is-renamed-by-one-explicit-command):
    new where the value names old, by its name or forge address (kit_in), kept in its form, a forge address by its owner
    and the new name unless new is an address itself, so a reader matching by address keeps the owner; the value as it
    is otherwise."""
    if not value or not kit_in(value, [old]):
        return value
    if "/" in new or "/" not in value:
        return new
    return f"{value.rsplit('/', 1)[0]}/{new}"


# The objects built on a repository's name that a reader matches it by (record.py's typed names, cards.row_object's keys):
# kit/<repo>, land/<repo>, queue/<repo>, record/<repo>/<number> and fix/main/<repo>/<name>.
KIT_OBJECT = re.compile(r"^(kit|land|queue)/([^/]+)$|^(record)/([^/]+)/(\d+)$|^(fix/main)/([^/]+)/(.+)$")


def renamed_object(obj, old, new):
    """An object built on a repository's name after a rename of old to new (Decision 1 of
    a-repository-is-renamed-by-one-explicit-command; KIT_OBJECT): its repository part new's name where it names old, by
    name (kit_in); any other object as it is."""
    m = KIT_OBJECT.match(obj or "")
    if not m:
        return obj
    name = new.split("/")[-1]
    if m.group(1) and kit_in(m.group(2), [old]):
        return f"{m.group(1)}/{name}"
    if m.group(3) and kit_in(m.group(4), [old]):
        return f"{m.group(3)}/{name}/{m.group(5)}"
    if m.group(6) and kit_in(m.group(7), [old]):
        return f"{m.group(6)}/{name}/{m.group(8)}"
    return obj


def renamed_source(source, old, new):
    """A Source line after a rename of old to new (Decision 1 of a-repository-is-renamed-by-one-explicit-command): each
    decision-record reference whose repository names old, <owner>/<old> before docs/adr/<n> (RECORD_REF), naming it by
    the new name in its form (renamed_kit); the rest of the line, its words, as written."""
    def one(m):
        repo = m.group(1)
        if not repo or not kit_in(repo, [old]):
            return m.group(0)
        return renamed_kit(repo, old, new) + m.group(0)[len(repo):]
    return RECORD_REF.sub(one, source or "")


def renamed_field(field, value, old, new):
    """One field of a record after a rename of old to new (Decision 1 of a-repository-is-renamed-by-one-explicit-command):
    a Repo by its repository (renamed_kit), a Source by its record references (renamed_source), and an On, From or Work
    by its object (renamed_object); any other field, a card's Key among them, as it is."""
    if field == "Repo":
        return renamed_kit(value, old, new)
    if field == "Source":
        return renamed_source(value, old, new)
    if field in ("On", "From", "Work"):
        return renamed_object(value, old, new)
    return value


# The fields a rename renames in each file of a drive's branch that a reader matches a repository by (Decision 1 of
# a-repository-is-renamed-by-one-explicit-command): the plan's decision-record sources, a request's repository and a fix
# of its main's work, and a run-record entry's repository and the objects it names. An entry's Key is the key Pending You
# held its card under, left as it was posted.
RENAMED_FIELDS = {"plan.rec": ("Source",), "requests.rec": ("Repo", "Work"), "runs/": ("Repo", "On", "From")}


def rename_rec(text, fields, old, new):
    """A recutils file's text after a rename of old to new (Decision 1 of a-repository-is-renamed-by-one-explicit-command),
    record by record: each field of fields renamed (renamed_field), every kit.rename entry whole, since it records an
    earlier act, and every other line, the descriptor, comments and the order of records and fields, byte for byte.
    Returns (text, how many records it renamed)."""
    blocks, n = re.split(r"(\n\s*\n)", text), 0
    for i in range(0, len(blocks), 2):
        lines = blocks[i].split("\n")
        if any(l.startswith(("%", "#")) for l in lines if l.strip()):
            continue
        if any(re.match(r"^Act: ?kit\.rename\s*$", l) for l in lines):
            continue
        out = []
        for l in lines:
            m = re.match(r"^([A-Za-z][A-Za-z0-9_]*):( ?)(.*)$", l)
            if m and m.group(1) in fields:
                v = renamed_field(m.group(1), m.group(3), old, new)
                l = f"{m.group(1)}:{m.group(2)}{v}" if v != m.group(3) else l
            out.append(l)
        if out != lines:
            blocks[i], n = "\n".join(out), n + 1
    return "".join(blocks), n


def rename_branch(w, old, new):
    """The drive's branch as a rename of old to new leaves it, in the write (Decision 1 of
    a-repository-is-renamed-by-one-explicit-command; plan.22, record.4): the plan's records by their decision-record
    sources, requests.rec, and every file of the run record under runs/ at the tip, each by its fields (RENAMED_FIELDS,
    rename_rec), a file replaced only where a record of it changed; no Bolt or Unit Repo, since none names old when the
    rename runs (rename_standing), and no other file. The rename is recorded on the write (w.renaming), through which
    appended reads requests.rec. Returns how many records it renamed, together, the entry's Count."""
    n = 0
    for r in w.plan.bolts() + w.plan.work():
        was = list(r.fields)
        r.fields[:] = [(f, renamed_field(f, v, old, new) if f in RENAMED_FIELDS["plan.rec"] else v) for f, v in r.fields]
        n += r.fields != was
    paths = ["requests.rec"] + [p for p in w.paths("runs/") if p.endswith(".rec")]
    for path, text in zip(paths, w.texts(paths)):
        if text is None:
            continue
        renamed, k = rename_rec(text, RENAMED_FIELDS.get(path) or RENAMED_FIELDS["runs/"], old, new)
        if k:
            w.replace(path, renamed)
            n += k
    if n:
        w.renaming.append((old, new))
    return n


def proposal_names(do, old):
    """Whether a proposal's Do line names a repository, old (Decision 2 of a-repository-is-renamed-by-one-explicit-command):
    any of its words, after the command's own, that holds the repository's name or forge address (kit_in), an object
    built on it (renamed_object) or a decision record's source in its repository (renamed_source), as a rename would find
    it in a record; a quoted goal or intent is one word, so a name inside its prose names nothing. Read by its words, so
    a line crew's parser would refuse still counts, and a rename of old held by another open proposal names it too."""
    try:
        words = shlex.split(do or "")
    except ValueError:
        words = (do or "").split()
    words = words[1:] if words[:1] == ["crew"] else words
    return any(kit_in(w, [old]) or renamed_object(w, old, "-") != w or renamed_source(w, old, "-") != w for w in words[2:])


def rename_standing(old, plan, requests, reads, entries, proposals, own):
    """What of a repository's work stands, so crew kit rename <old> <new> waits for it (Decision 2 of
    a-repository-is-renamed-by-one-explicit-command; plan.22), from plain facts (code.7): the plan as the write holds it;
    requests.rec's records; the drive's runners as the write read them ({host: runner.host_read's reading}); the
    run record's entries at the tip, each once, oldest first; proposals.rec's records; and own, the number of the
    proposal applying the rename, None for a direct run. old matches by name or forge address (kit_in) throughout. What
    stands: each bolt of old, which has not landed, since a landed or dropped bolt has left the plan (state.2), and each
    unit or chore of its queue; a fix of its main or a role's work in it, launched and standing (runner.standing), whose
    stage (runner.piece_stage) is not landed, dropped or refused; a place a runner carries of a launch in old whose
    phase in Flume's status is live or making, a unit's place still live after its unit's drop among them; the newest
    card under land/<old> or record/<old>/<n>[/<commit>] while it is open, or lost to its owner, which the rail raises
    again (cards.posted_cards); a batch neither closed (batch_closed) nor settled (batch_settled) that holds a unit of
    old, by the plan's unit or by a landing of old naming it; and an open proposal, but own, a Do of which names old
    (proposal_names). Returns (what stands, what crew could not read), each as words: a stage crew can't tell, a
    runner it can't read, and a place whose status it can't read (read.1)."""
    of = lambda r: bool(r.get("Repo")) and kit_in(r.get("Repo"), [old])
    stands, unread = [], []
    stands += [f"bolt {b.name()} has not landed" for b in renamed_in(plan, old)[0]]
    stands += [f"{kind_of(u)} {u.name()} waits in {old}'s queue" for u in plan.queue() if of(u)]
    for l in runner.standing(requests):
        work = l.get("Work") or ""
        if not work.startswith(("fix/main/", "role/")) or not of(l):
            continue
        st = runner.piece_stage(requests, reads, l)
        if st["stage"] == "unknown":
            unread.append(f"crew can't tell how far {work} (request {l.get('Request')}) has got: {st['why']}")
        elif st["stage"] not in ("landed", "dropped", "refused"):
            stands.append(f"{work} (request {l.get('Request')}) is {runner.stage_said(st)}")
    launches = {runner.number(r.get("Request")): r for r in requests if r.get("Act") == "launch"}
    for host in sorted(reads):
        reading = reads[host]
        if reading.get("why"):
            unread.append(reading["why"])
            continue
        for n, p in sorted((reading.get("places") or {}).items()):
            l = launches.get(n)
            if l is None or not of(l) or (l.get("Work") or "").startswith(("fix/main/", "role/")):
                continue
            if p.get("why"):
                unread.append(p["why"])
                continue
            f = runner.flume_facts(p.get("status"), p.get("place"))
            if f is None:
                unread.append(f"Flume's status of the place of request {n}, as {host}'s runner carried it, holds no place {p.get('place')}")
            elif f["phase"] in ("live", "making"):
                stands.append(f"place {p.get('place')} of request {n} ({l.get('Work')}) is {f['phase']} on {host}")
    newest = {}
    for c in cards.posted_cards(entries):
        newest[c["key"]] = c
    for key, c in newest.items():
        parts = key.split("/")
        mine = len(parts) >= 2 and kit_in(parts[1], [old]) and (
            (parts[0] == "land" and len(parts) == 2) or (parts[0] == "record" and len(parts) in (3, 4) and parts[2].isdigit()))
        if mine and c["state"] is None:
            stands.append(f"{c['by']}'s card {key} is open")
        elif mine and c["state"] == "lost":
            stands.append(f"{c['by']}'s card {key} was lost to its owner, and the rail raises it again")
    olds = {u.name() for u in plan.work() if of(u)} | {o[5:] for e in entries if e.get("Act") == "bolt.land" and not e.get("Refused")
                                                       and of(e) for o in e.get("On") or [] if o.startswith("unit/")}
    closed, settled, posts, held = batch_closed(entries), batch_settled(entries), batch_posts(entries), []
    for n, _, units in batches(entries):
        for key, part in batch_cards(n, units, posts):
            mine = [u for u, *_ in part if u in olds]
            if mine and key not in closed and key not in settled and n not in held:
                held.append(n)
                stands.append(f"batch {n} is unanswered and holds {cards.joined(list(dict.fromkeys(mine)))}")
    for p in proposals:
        if p.get("State") == "open" and p.get("Proposal") != own and any(proposal_names(d, old) for d in p.all("Do")):
            stands.append(f"proposal {p.get('Proposal')} is open and names {old}")
    return stands, list(dict.fromkeys(unread))


def rename_kept(old, hosts):
    """Which hosts still keep a repository, so crew kit rename <old> <new> waits for its removal (Decision 3 of
    a-repository-is-renamed-by-one-explicit-command; plan.22), from plain facts (code.7): hosts, {host: (report,
    filed)} for each host with a runner branch of the drive and its main-level host, report the repositories its
    runner's repositories.rec names, None for a runner that reports none or a host with no runner branch, or why its
    runner can't be read, and filed the repositories the teams file keeps there (crew.kept, record 0064), None for a
    host that is neither the one the file is written on nor a drive's machine, whose keeping the file does not give. A
    host's keeping is its runner's report where it gives one, else the teams file's; a host keeps old where a repository
    it keeps has old's name, or is old's address when old is given as one, each such repository named. Reads only
    whether a host still keeps the name, to refuse, never where a kit's work runs (roles.9). No host needs to keep the
    new name: the repository is added back under it after the rename. Returns (what keeps old, what crew could not read),
    each as words (read.1)."""
    names = (lambda r: r == old) if "/" in old else (lambda r: r.split("/")[-1] == old)
    kept, unread = [], []
    for host in sorted(hosts):
        report, filed = hosts[host]
        if isinstance(report, str):
            unread.append(report)
        elif report is not None:
            kept += [f"{host}'s runner keeps {r}" for r in sorted(report) if names(r)]
        elif filed is None:
            unread.append(f"{host}'s runner reports no repositories, and {host} is neither the host the teams file is "
                          f"written on nor one a drive runs on, so crew can't read whether it keeps {old}")
        else:
            kept += [f"{host}'s teams file keeps {r}" for r in sorted(set(filed)) if names(r)]
    return kept, unread


# A kit as a command names it (code.4): its name, lowercase words with dashes, or its forge address, <owner>/<name>, as
# the teams file lists it, the owner as GitHub has it.
KIT = re.compile(r"^(?:[A-Za-z0-9][A-Za-z0-9_.-]*/)?[a-z0-9][a-z0-9-]*$")


def kit_name(text):
    """A kit's name as crew's parser takes it (KIT), refused otherwise, as the parser refuses any argument it can't
    read."""
    if not KIT.match(text):
        raise argparse.ArgumentTypeError(f"a kit is named by its name, lowercase words with dashes, or <owner>/<name>, not {text}")
    return text


def rename_refusal(label, old, new, bolts, stands, unread, kept, unkept, count):
    """Why crew kit rename <old> <new> is refused, or None (Decision 4 of a-repository-is-renamed-by-one-explicit-command;
    plan.22), from plain facts (code.7): the drive's bolts' names; what of old's work stands and what crew could not
    read of it (rename_standing); which hosts keep old and whose keeping crew could not read (rename_kept); and count,
    the records rename_branch renamed, None before it has run. Refused, in this order: for two names of one repository;
    for a new name a bolt of the drive holds, since land/<new> would name the bolt; while any of old's work stands or
    crew can't read whether it does, every one named in one message; while any host keeps old or crew can't read whether
    one does, since the repository is removed from the runner, Flume and sluice first; and for a name no record of the
    drive holds, once rename_branch has run."""
    name = new.split("/")[-1]
    if old.split("/")[-1] == name:
        return f"{old} and {new} name one repository: a rename gives it another name"
    if name in bolts:
        return (f"{name} is the name of bolt {name} of {label}, so land/{name} would name the bolt and not the repository: "
                "a repository and a bolt of one drive take different names")
    if stands or unread:
        said = f"crew can't rename {old} while its work stands: " + "; ".join(stands) + "; its work lands or is dropped first" \
            if stands else f"crew can't rename {old}: it can't read whether its work stands"
        return said + ((", and crew can't read whether more of it stands: " if stands else ": ") + "; ".join(unread) if unread else "")
    if kept or unkept:
        said = f"crew can't rename {old} while a host keeps it: " + "; ".join(kept) if kept else \
            f"crew can't rename {old}: it can't read whether a host keeps it"
        said += (", and crew can't read whether another keeps it: " if kept else ": ") + "; ".join(unkept) if unkept else ""
        return said + f"; {old} is removed from the runner, Flume and sluice before crew renames its records"
    if count == 0:
        return f"no record of {label}'s names {old}: neither its plan's sources, its requests nor its run record"
    return None


def renamed_in(plan, old):
    """The plan's records whose Repo names a repository, old, by its name or forge address (kit_in): its bolts and its
    units and chores, as (bolts, work), each in the plan's order; work that stands, so a rename of old waits for it
    (rename_standing), and what a proposal holding the rename names."""
    of = lambda r: bool(r.get("Repo")) and kit_in(r.get("Repo"), [old])
    return [b for b in plan.bolts() if of(b)], [u for u in plan.work() if of(u)]


def plan_for(fleet, kit, label):
    """The plan a kit's work goes in, (label, state repository) (Decision 3 of the-team-machinery-leaves): the drive
    the command runs as (label, --label or the agent's own: default_label), a kit entering a drive with its first
    bolt or unit; else the one drive whose plan or landings already name the kit (kit_labels), refused when none
    or several do."""
    if not label:
        labels = kit_labels(fleet, kit)
        labels or fail(f"no drive's plan or landings name {kit}, so crew can't tell which plan its work goes in; add --label")
        len(labels) == 1 or fail(f"{kit}'s work could go in the plan of " + ", ".join(labels) + "; add --label")
        label = labels[0]
    CONTEXT["label"] = label
    return label, state_of(fleet, label)[0]


def name_free(fleet, label, kit, names):
    """A unit's name is its OpenSpec change's, and a name is taken once in a kit, by a unit or a chore (plan.7, plan.11):
    refused when the kit's main already has that change, open or archived, or holds a chore by it, read in the checkout
    the drive's main-level host keeps of the kit (main_kit), and refused where it keeps none."""
    t = main_kit(fleet, label, kit) or fail(main_kit_said(fleet, label, kit, f"check {kit}'s changes"))
    sv = survey(fleet, [(t, None)])[t["machine"]]
    sv["ok"] or fail(f"cannot check {kit}'s changes: {t['machine']} did not answer ({sv['error']})")
    k = sv["kits"][t["kit"]["main"]]
    k.get("ok") or fail(f"cannot check {kit}'s changes on {t['machine']}: {k.get('error')}")
    for n in names:
        why = name_taken(kit, n, k["main"], k.get("chores"))
        not why or fail(why)


# Which of Flume's branches stand in a repository, read in its folder ($1) as Flume's place profile reads a branch
# before it makes one (flume 3, 78: `git worktree add -b` refuses a branch that exists): each ref named after it,
# refs/heads/<branch>, with its commit, and nothing for one that does not stand (runner.refs_standing).
BRANCHES = r"""cd "$1" || exit 3
shift
git for-each-ref --format='%(objectname) %(refname)' "$@"
"""


def branches_in(fleet, host, folder, branches):
    """{branch: commit} of the branches that stand in the repository at folder on host (BRANCHES,
    runner.refs_standing); refused naming the folder and host when git there can't be read, or the host did not answer
    (read.1)."""
    r = crew.on_machine(fleet, host, ["bash", "-c", BRANCHES, "crew", folder, *[f"refs/heads/{b}" for b in branches]])
    if r.returncode == 255:
        fail(f"cannot read whether {', '.join(branches)} stands in {folder}: {host} did not answer")
    r.returncode == 0 or fail(f"cannot read whether {', '.join(branches)} stands in {folder} on {host}: "
                              + ((r.stderr or r.stdout).strip() or f"git exited {r.returncode}"))
    return runner.refs_standing(r.stdout, branches)


def branch_free(fleet, label, kit, names, kind):
    """A unit or chore (kind) is planned under a name only while no launch of it would be refused because Flume's
    branch for its place stands (runner.branch_refusal; flume 3, 67): Flume keeps a dropped place's branch while it holds
    work, so a name dropped and added again would pass the plan and fail at its launch. Read in every repository a
    launch of the kit's work would be made in (runner.launch_repositories), from the drive's requests and runners as
    this command read them (runner_facts), and in each with git as Flume reads it (branches_in), never from crew's own
    record of a drop; refused when crew can't tell where (read.1); nothing read while no runner has taken any of the
    kit's work and none reports keeping it."""
    requests, reads = runner_facts(fleet, label)
    repos, why = runner.launch_repositories(reads, runner.kit_launches(requests, kit), kit)
    not why or fail(f"cannot check whether Flume's branch for {kind} {', '.join(names)} stands: {why}")
    branches = [runner.place_branch(f"{kind}/{n}") for n in names]
    found = [dict(r, refs=branches_in(fleet, r["host"], r["dir"], branches)) for r in repos]
    why = runner.branch_refusal(kit, kind, names, found)
    not why or fail(why)


def name_taken(kit, name, changes, chores):
    """Why a new unit's or chore's name is not free in its kit, or None: not a name crew mints, the name of a change the
    kit's main holds (changes), or of a chore main's history holds (chores, None when the kit was read by a crew that
    reads none, so nothing is refused for it)."""
    if not crew.NAME.match(name):
        return f"a unit's or chore's name is lowercase words with dashes, not {name}"
    if name in changes:
        return f"{kit}'s main already has a change named {name}, open or archived; pick another name"
    if name in (chores or ()):
        return f"{kit}'s main already holds a chore named {name}; pick another name"
    return None


def host_run(fleet, host, script, *args):
    """Run a bash script on a host, with its arguments; refused with its own words when it fails."""
    r = crew.on_machine(fleet, host, ["bash", "-c", script, "crew", *args])
    r.returncode == 0 or fail(f"on {host}: " + ((r.stderr or r.stdout).strip() or f"exit {r.returncode}"))
    return r.stdout.strip()


# Where a bolt's branch lives, for kit.bolt_lives (plan.19), read in a checkout of its kit with $bolt and $file set:
# LOCAL and TRACKED, the commit of the host's own bolt/<bolt> and of origin's tracking ref of it, as this host last
# fetched it, or -; AT_LOCAL and AT_TRACKED, the policy ($file) at each, base64, or - when it holds none, read from the
# commit as sluice reads a branch's policy. Its two reads, ref and pol, are REFS.
REFS = r"""ref() { git rev-parse --verify -q "$1^{commit}" || echo -; }
pol() { if [ "$1" != - ] && text=$(git show "$1:$file" 2>/dev/null); then printf '%s\n' "$text" | base64 | tr -d '\n'; else printf -; fi; }
"""
BOLT_AT = REFS + r"""l=$(ref "refs/heads/bolt/$bolt") o=$(ref "refs/remotes/origin/bolt/$bolt")
echo "LOCAL=$l"; echo "TRACKED=$o"; echo "AT_LOCAL=$(pol "$l")"; echo "AT_TRACKED=$(pol "$o")"
"""


# A script that fetches from origin in a kit's checkout is told so on its first line where crew may not fetch there
# (fetch_told, crew.fetches_in): fetch=no in a repository the host's teams file names, the runner's clone, which the
# runner alone fetches (agentplot/boomdrive core.14), where the script reads origin's tracking refs as the runner last
# fetched them; a script told nothing fetches as before. FETCH is that fetch, origin_fetch, made unless told fetch=no, and
# refused with nothing fetched, in its own words on standard error, for a word that is neither (read.1).
#
# The fetch is one try to the family's limit on the host where its git runs (weir 69, C.3), by bounded, gather.tried's
# twin in bash, since the host's crew may be older and no crew module is on its disk: bounded <call> <remote> <command...>
# runs the command in a process group of its own (job control on for its start), its output to temporary files it
# removes once read, and waits, a look every tenth of a second, until its leader has exited and no process of its group
# is left, or to try_for_ms, when it asks the group to end, gives it grace_ms, then kills it and reaps the leader; the
# looks count the time slept, and $SECONDS, whole seconds of the wall clock, bounds a host so loaded that the sleeps run
# long, so a try ends at most two seconds past its limit there and never before it. A try
# that ends gives its output, its standard error and its exit as they were; a stopped one prints none of its output,
# says gather.stopped's words on standard error and returns 124. try_for_ms and grace_ms are filled from gather.TRY_FOR
# and gather.GRACE here, one line each, and read from nothing else. It runs on bash 3.2, a Mac's /bin/bash, as on 5.
FETCH = f"""try_for_ms={round(gather.TRY_FOR * 1000)}
grace_ms={round(gather.GRACE * 1000)}
""" + r"""bounded() {
  local call=$1 remote=$2 out err pid code= waited=0 began=$SECONDS stopped= last limit
  shift 2
  out=$(mktemp "${TMPDIR:-/tmp}/crew-try.XXXXXX") || return 2
  err=$(mktemp "${TMPDIR:-/tmp}/crew-try.XXXXXX") || { rm -f "$out"; return 2; }
  # The shell's own words on the job, bash 3.2's "Terminated" among them, are no part of the try's: its standard
  # error goes to $err, and the shell's here to /dev/null.
  {
    set -m
    "$@" </dev/null >"$out" 2>"$err" &
    pid=$!
    set +m
    while :; do
      if [ -z "$code" ] && ! kill -0 "$pid"; then wait "$pid"; code=$?; fi
      if [ -n "$code" ] && ! kill -0 -- "-$pid"; then break; fi
      if [ "$waited" -ge "$try_for_ms" ] || [ $(( (SECONDS - began - 1) * 1000 )) -ge "$try_for_ms" ]; then stopped=yes; break; fi
      sleep 0.1
      waited=$((waited + 100))
    done
    if [ -n "$stopped" ]; then
      kill -TERM -- "-$pid"
      waited=0
      while [ "$waited" -lt "$grace_ms" ]; do
        if [ -z "$code" ] && ! kill -0 "$pid"; then wait "$pid"; code=$?; fi
        kill -0 -- "-$pid" || break
        sleep 0.1
        waited=$((waited + 100))
      done
      if kill -0 -- "-$pid"; then
        kill -KILL -- "-$pid"
        waited=0
        while [ "$waited" -lt 5000 ] && kill -0 -- "-$pid"; do sleep 0.1; waited=$((waited + 100)); done
      fi
      [ -n "$code" ] || wait "$pid"
    fi
  } 2>/dev/null
  if [ -n "$stopped" ]; then
    last=$(awk 'NF { l = $0 } END { sub(/^[ \t\r]+/, "", l); sub(/[ \t\r]+$/, "", l); print l }' "$err")
    if [ "$try_for_ms" -ge 1000 ] && [ $((try_for_ms % 1000)) -eq 0 ]; then limit="$((try_for_ms / 1000))s"; else limit="$try_for_ms"ms; fi
    rm -f "$out" "$err"
    echo "${last:+$last; }$call with $remote was still going after $limit, the most a try may take, and was stopped" >&2
    return 124
  fi
  cat "$out"
  cat "$err" >&2
  rm -f "$out" "$err"
  return "$code"
}
origin_fetch() {
  case ${fetch-yes} in
    yes) bounded "git fetch" origin git fetch -q origin "$@" ;;
    no) ;;
    *) echo "crew told this script fetch=${fetch}, which is neither yes nor no, so it fetches nothing" >&2; return 2 ;;
  esac
}
"""

# A kit's GitHub fetched in its folder, $1, on the host its work runs on, as one try (FETCH): run through fetch_told and
# host_run by origin_fetched and landing_opened, so a kit is fetched only by gather or origin_fetch.
ORIGIN_FETCH = FETCH + r"""cd "$1" || exit 1
origin_fetch
"""


def fetch_told(fleet, host, main, script):
    """A script that fetches from origin in a kit's checkout (main) on a host (FETCH), told fetch=no on its first line
    in the runner's clone, which crew fetches nothing in (crew.fetches_in); elsewhere as it is, fetching as before."""
    return script if crew.fetches_in(fleet, host, main) else "fetch=no\n" + script


# What a kit's main checkout holds of its mains, on its host, for kit.main_now to decide which is main now (plan.18,
# code.7): ORIGIN, whether it has an origin remote, which it then fetches, once for the command, and FETCHED, ok or the
# fetch's error, or runner where it is the runner's clone, which crew fetches nothing in (FETCH), its origin/main as the
# runner last fetched it; GITHUB and OWN, the commits origin/main and its own main are at, or -.
MAINS = FETCH + r"""if git remote get-url origin >/dev/null 2>&1; then
  echo ORIGIN=yes
  if [ "${fetch-yes}" = no ]; then echo FETCHED=runner
  elif err=$(origin_fetch 2>&1); then echo FETCHED=ok; else echo "FETCHED=$(printf '%s' "$err" | tr '\n' ' ')"; fi
else echo ORIGIN=no; fi
echo "GITHUB=$(git rev-parse --verify -q 'refs/remotes/origin/main^{commit}' || echo -)"
echo "OWN=$(git rev-parse --verify -q 'refs/heads/main^{commit}' || echo -)"
"""

# What a kit's main checkout holds of its mains, on its host (MAINS), for the commit its main is at now, which a
# landing records (plan.14), and the number of sluice's submission each main's head landed, SUBMISSION_GITHUB and
# SUBMISSION_OWN, its Sluice-Submission trailer, empty for a head sluice did not make.
MAIN = r"""main=$1
cd "$main" || exit 1
""" + MAINS + r"""n() { git log -1 --format='%(trailers:key=Sluice-Submission,valueonly,separator=%x20)' "$1" 2>/dev/null; }
echo "SUBMISSION_GITHUB=$(n refs/remotes/origin/main)"
echo "SUBMISSION_OWN=$(n refs/heads/main)"
"""


COMMIT = re.compile(r"^[0-9a-f]{7,64}$")


def main_held(name, machine, said):
    """The commit a kit's main holds now, from what MAIN read on its host (kit.main_now): (sha, None), or (None, why).
    A host's own main lagging GitHub's refuses nothing: sluice forms every landing on GitHub's main and pushes it with a
    lease (plan.8), and main now is GitHub's for a kit with an origin."""
    _, sha, why = kit.main_now(said, name, machine)
    return sha, why


def sweep_on(fleet, t, what, landed=None, units=()):
    """The kit's read after a landing or a drop of one of its bolts (kit_read, code.3), on the host its work runs on and
    in the kit's folder there (t, bolt_at): run in this process when that is this host, else crew _sweep there as the
    one asking, saying what it did: each landing of the kit's bolts nothing recorded read, but after a landing
    (reap_landings, plan.21, kit_read); the tidy's naming of any landing or legacy worktree it finds (tidy); after a
    landing, the bolt's landing card closed there with the words (landing_cards_closed), landed being (bolt, the
    outcome recorded); after it, what the bolt's units (units) recorded as made, kept there, removed (made_drop). crew deletes no
    branch (crew-lands-each-bolt-through-flumes-base-place, Decision 8). A host that does not answer, or whose read
    fails, leaves that to the kit's next read, and the write stands."""
    bolt, outcome = landed or (None, None)
    kit_name = t["kit"]["name"]
    if t["machine"] == crew.this_host():
        try:
            kit_read(fleet, t, bolt, outcome, units)
        except Refusal as e:
            print(f"{kit_name}'s read after {what} failed ({e}): its next read sweeps what is over")
        return
    more = ["--landed", bolt, "--outcome", outcome] if landed else []
    more += ["--units", *units] if units else []
    r = crew.on_machine(fleet, t["machine"], crew.crew_argv(fleet, t["machine"], "_sweep", t["label"], kit_name, "--dir",
                                                            t["kit"]["dir"], *more))
    READ.drop_kit(t["machine"], t["kit"]["main"])
    if r.returncode:
        why = "did not answer" if r.returncode == 255 else "failed (" + ((r.stderr or r.stdout).strip().splitlines() or [f"exit {r.returncode}"])[-1] + ")"
        print(f"{kit_name}'s host {t['machine']} {why}, so what crew made for {what} is not swept yet: the kit's next read sweeps it")
    elif (r.stdout + r.stderr).strip():
        print((r.stdout + r.stderr).strip())


# --------------------------------------------------------------------------------------------------- bolts

def launched_said(repo, bolt, launched, base=None):
    """What a start says once the plan starts the bolt (Decision 5; crew-lands-each-bolt-through-flumes-base-place,
    Decision 3): its base place asked of the runner by its request (base), each piece of work launched by its request,
    for the runner whose configuration names the bolt's repository to take in the stream its host maps it to (the user's
    ruling of 2026-11-01), and that no agent starts and no branch is made, crew bolts showing the places."""
    work = ", ".join(f"{w} (request {n})" for n, w in launched) or "nothing, the bolt holding no unit or chore yet"
    place = (f"{bolt}'s base place, bolt/{bolt}, is asked of the runner (request {base}), which has sluice make its branch "
             "from main; " if base else "")
    return (f"{place}no agent starts: {work} is launched in {repo}, for a runner whose configuration names it to take, in "
            "the stream its host maps it to, and crew bolts shows their places")


def crossed_bolt(plan, bolt):
    """Whether a bolt of the plan was given through Flume, marked Path: flume (Decision 2)."""
    b = plan.bolt(bolt) if bolt else None
    return b is not None and b.get("Path") == "flume"


def reach_places(fleet, w, bolt, again=()):
    """A plan write's own act on a started bolt (Decisions 5 to 7 of teams-cross-to-flume-as-their-bolts-land): the
    requests runner.reach decides, its launches, drops and launches anew, each in the bolt's repository for the runner
    whose configuration names it to take (the user's ruling of 2026-11-01), appended in the write's own commit
    (request), then the priorities the plan's order changed (reprioritise); again the work launched anew. Returns each
    launch appended, as (its number, its work)."""
    b = w.plan.bolt(bolt)
    b is None or started(b) or fail(f"bolt {bolt} is not started, so nothing of its work is launched")
    launched = []
    for act, work, given in runner.reach(w.plan, requests_of(w).recs("Request"), bolt, w.label, again):
        n = request(w, act, work, **given)
        if act == "launch":
            launched.append((n, work))
    reprioritise(w)
    return launched


def reprioritise(w):
    """Decision 6: a priority request appended for each launch standing on a bolt given through Flume whose priority
    the plan's order changed (runner.priorities), in the write's own commit; nothing when the branch holds no
    requests."""
    if w.text("requests.rec") is None:
        return
    for launch, p in runner.priorities(w.plan, requests_of(w).recs("Request")):
        request(w, "priority", launch.get("Work"), Of=launch.get("Request"), Priority=p)


def runner_facts(fleet, label):
    """What a crossed piece's stage is read from in a drive (runner.piece_stage; Decision 8 of teams-cross-to-flume-
    as-their-bolts-land): requests.rec's records at the tip of its branch this command reads (tip_of), as written, none
    where the branch is not started, and each host's runner read beside it (runners)."""
    repo, ref = state_of(fleet, label)
    tip = tip_of(repo, ref)
    requests = Plan(show(repo, tip, "requests.rec") or runner.REQUESTS).recs("Request") if tip else []
    return requests, runners(repo, label)


def launch_label(fleet, work, label):
    """The drive whose requests.rec holds a launch standing for the work a command names (runner.named_launch):
    label when given, else the one drive that holds it; refused naming each drive when none does, or when
    more than one does, which --label settles."""
    labels, errors, hits, why = [label] if label else sorted(fleet["drives"]), {}, [], None
    for l in labels:
        try:
            repo, ref = state_of(fleet, l)
            tip = tip_of(repo, ref)
        except Refusal as e:
            errors[l] = str(e)
            continue
        launch, why = runner.named_launch(Plan(show(repo, tip, "requests.rec") or runner.REQUESTS).recs("Request") if tip else [], work)
        if launch is not None:
            hits.append(l)
    if len(hits) == 1:
        return hits[0]
    hits or fail((why if len(labels) == 1 else f"no launch of {work} stands in the requests of " + ", ".join(labels))
                 + "".join(f"; {l}/main could not be read: {e}" for l, e in errors.items()))
    fail(f"{work} has a launch standing in the requests of {' and '.join(hits)}: add --label")


def answer(fleet, a):
    """crew answer <work> "<words>" [--label L]: a retry of the stage the place of a started bolt's work stopped short on,
    or waits on its caller for, carrying the words, the planner's, the design agent's or main-level ops's answer
    (Decision 9 of teams-cross-to-flume-as-their-bolts-land, runner.answer_retry); its submission again where that is
    what waits, unheld. Appended to requests.rec in one plan write, the work's stage read again from the runner's
    records at the tip it is applied to (plan.1), and recorded as stage.answer, which holds none of the words
    (record.3). Refused, naming the place's stage, when the place neither stopped short nor waits on its caller; naming
    what crew could not read when it can't tell, as while the runner holds the launch or has carried no status of the
    place (read.1); and when no launch of the work stands. A stop-short whose agent Flume keeps open is answered as any
    other, the retry naming its stage reaching that session (flume 49)."""
    label = launch_label(fleet, a.work, default_label(fleet, a))
    CONTEXT["label"], seen = label, {}

    def change(w):
        seen.update(answer_place(w, a.work, a.words))
        return []
    write(fleet, label, change, "plan: answer a place", act="stage.answer")
    print(f"{seen['work']}'s place {seen['place']} is asked to run {seen['what']} again with the answer (request {seen['n']}): "
          f"the runner on {seen['host']} retries it")


def answer_place(w, named, words):
    """crew answer's change to a write (answer): the retry runner.answer_retry decides for the place of the work named,
    its stage read from the runner's records as the write reads them, appended to requests.rec with the words, the
    write's subject and objects set. Returns what it asked, {n, work, host, place, what}: the request's number, the work
    as requests name it, the host whose runner took it and retries it, its place, and the stage, or the submission,
    run again."""
    requests = requests_of(w).recs("Request")
    launch, why = runner.named_launch(requests, named)
    not why or fail(why)
    work = launch.get("Work")
    CONTEXT["work"] = work
    s = runner.piece_stage(requests, w.runners(), launch)
    n = runner.number(launch.get("Request"))
    reading = runner.taken(w.runners(), n)[0]
    carried = (reading["host"], reading["places"][n]["at"]) if reading and n in reading["places"] else None
    how, stage = runner.answer_retry(work, s, carried)
    how or fail(stage)
    host = w.taker(launch)
    n = request(w, "retry", work, Of=launch.get("Request"), Stage=stage, Submission=how == "submission", Words=words)
    what = stage or "submission"
    w.subject = f"plan({(launch.get('Intent') or '').split('/', 1)[-1]}): answer {work}'s {what}"
    w.on += [work] + ([launch.get("Base")] if (launch.get("Base") or "").startswith("bolt/") else [])
    return dict(n=n, work=work, host=host, place=s.get("place") or launch.get("Name"), what=what)


def land_refusal(bolt, units, stage_of, outside, label, held=None, kit_name=None):
    """Why a bolt does not land, or None (plan.16): a unit or chore (units, by name) crew cannot read, or one that has
    not landed on main, or units whose latest change no batch has held yet (outside); a chore is in no batch. A bolt
    given through Flume, held given for it alone ({commit: whether kit_name's main now holds it}, main_holds), reads
    each merged from the runner's records and lands once main holds the commit each place landed at on the bolt, a
    chore asked for no trailer (runner.unlanded; Decision 12 of teams-cross-to-flume-as-their-bolts-land)."""
    if held is not None:
        why = runner.unlanded(bolt, kit_name, [(u, stage_of(u).get("kind", "unit"), stage_of(u).get("flume") or stage_of(u))
                                               for u in units], held)
        if why:
            return why
    for u in units if held is None else ():
        s = stage_of(u)
        k = s.get("kind", "unit")
        if s["stage"] == "unknown":
            return f"cannot tell whether {k} {u} has landed: {s.get('why')}"
        if s["stage"] != "landed":
            return f"{k} {u} has not landed on main: it is {s['stage']}"
    if outside:
        return (f"bolt {bolt} lands only once every unit's latest change has been in a batch, and {either(outside)} "
                + ("has" if len(outside) == 1 else "have") + f" not: a batch is due for them (crew review {label})")
    return None


def drive_kits(plan, landings):
    """A drive's kits (Decision 3 of the-team-machinery-leaves): the repositories its plan's Bolt and Unit records
    name, with those its run record's landings name, each bolt.land entry not refused (landings, as record.acts_in
    finds them), by Repo as written, sorted and each once (plan.22). There is no registry of repositories in crew: a kit enters
    a drive with its first bolt, and a kit whose last bolt has landed stays one by its landings. plan None, a
    branch not started, names none."""
    named = [r.get("Repo") for r in (plan.bolts() + plan.work() if plan is not None else [])]
    named += [e.get("Repo") for e in landings if e.get("Act") == "bolt.land" and not e.get("Refused")]
    return sorted({r for r in named if r})


def runs_at(repo, tip):
    """What crew reads of the run record by its acts at a tip of a drive's branch, in one pass over its files under
    runs/, read once for the command by the tip (plan.12): every bolt.land entry, found by its act (record.acts_in),
    {"landings"}; a kit.rename entry among them renames nothing crew reads (plan.22)."""
    name = f"runs-{tip}"
    held = READ.held(name)
    if held is not None:
        return held
    paths = [p for p in paths_at(repo, tip, "runs/") if p.endswith(".rec")]
    texts = [show(repo, tip, p) for p in paths] if kept_listing(repo, tip) is not None else cat_file(repo, [f"{tip}:{p}" for p in paths])
    out = {"landings": [e for t in texts for e in record.acts_in(t or "", "bolt.land")]}
    READ.keep(name, out)
    return out


def landings_at(repo, tip):
    """Every bolt.land entry the run record holds at a tip of a drive's branch (runs_at)."""
    return runs_at(repo, tip)["landings"]


def kits_at(repo, tip, pl):
    """A drive's kits (drive_kits) as its branch holds them at a tip: the plan read there (pl) and the landings
    its run record holds; none for a branch not started (tip None)."""
    return drive_kits(pl, landings_at(repo, tip) if tip else [])


def kits_read(fleet, label, fresh=True):
    """A drive's kits (drive_kits) read from its branch, fetched once for the command, or, not fresh, as crew's
    cache holds it now with no fetch (tip_here, plan.12), as a standing agent's due restart reads its kit folders
    (crew.kits_on); none for a branch not started, or not yet fetched into the cache. Refused naming the branch when it
    can't be read (read.1)."""
    repo, ref = state_of(fleet, label)
    if fresh:
        tip = tip_of(repo, ref)
    else:
        tip = tip_here(repo, ref)
        tip is not None or fail(f"crew's cache of {repo} can't be read for {ref}")
    return kits_at(repo, tip, read(repo, ref, tip) if tip else None)


def land_key(key, kits):
    """What a land/ card key names (rail-cards, record 0031 as amended 2026-10-23), from the drive's kits
    (drive_kits, the repositories its plan and its landings name): ("kit", <kit>) for land/<kit>, the kit's
    landings card, main-level ops's; ("bolt", <bolt>) for any other land/<x>, a bolt's reading and preview, and an old
    landing card of the bolt's own, land/<bolt> or land/<bolt>/<head> as a conductor posted one before; None for a key
    that is no landing's."""
    m = re.fullmatch(r"land/([a-z0-9][a-z0-9-]*)(/[0-9a-f]{7})?", key or "")
    if not m:
        return None
    return ("kit", m.group(1)) if m.group(1) in kits and not m.group(2) else ("bolt", m.group(1))


def kit_named(bolt, kits, label):
    """Why a bolt may not be added under its name, or None (rail-cards "A bolt's own landing card gives way to its
    kit's"): it is the name of one of the drive's kits (drive_kits, the repositories its plan and its landings
    name), whose landings card is land/<kit>, so land/<bolt> would name the kit's card and not the bolt."""
    if bolt in kits:
        return (f"a bolt of {label} may not be named {bolt}: that is the name of a kit {label}'s plan or landings name, "
                f"whose landings card is land/{bolt}")
    return None


def unheld_stages(k, why, other, chores=()):
    """Each unit's and chore's stage for the landing of a bolt no team holds: landed when main holds it on its kit as
    read there (k), a unit's change open or archived and a chore's trailer (chores, the bolt's chores' names), unknown
    with why when the kit could not be read, else its stage in the plan (other(name))."""
    def of(name):
        kind = "chore" if name in chores else "unit"
        if k is None:
            return {"stage": "unknown", "why": why, "kind": kind}
        return {"stage": "landed", "kind": kind} if name in (k.get("chores", []) if kind == "chore" else k["main"]) else dict(other(name), kind=kind)
    return of


def unheld_refusal(fleet, bolt, units, kit, t, label):
    """Why a bolt never started can't land, or None: it holds units or chores, since a bolt with none has nothing on
    main, and the drive's main-level host keeps a checkout of its kit (t, main_kit), whose main is read."""
    if not units:
        return f"bolt {bolt} was never started and holds no units or chores, so nothing of it has landed"
    if t is None:
        return f"bolt {bolt} was never started, and {main_kit_said(fleet, label, kit, 'read its main')}"
    return None


def landed_words(head, submission):
    """What a bolt's landing card closes with at crew bolt land (plan.16, record 0032 §3): where GitHub's main holds the
    landing, with sluice's submission number when its head carries one, and that every host's folder follows by the
    fleet's timer, since nothing waits on a host."""
    n = f" (#{submission.strip()})" if re.fullmatch(r"\d+", (submission or "").strip()) else ""
    return f"landed on GitHub's main at {head[:7]}{n}; every host's folder follows by swancloud's timer within minutes"


def landing_card_keys(entries, bolt, owner):
    """The keys under which owner holds an open landing card of the bolt's own, from its host's run record:
    land/<bolt>, as crew raised it (record 0031), and land/<bolt>/<head>, as a conductor posted one before."""
    keys = sorted({e.get("Key") for e in entries if e.get("Act") == "card.post" and e.get("By") == owner
                   and re.fullmatch(rf"land/{re.escape(bolt)}(/[0-9a-f]{{7}})?", e.get("Key") or "")})
    return [k for k in keys if cards.card_under(entries, k, owner)]


def landing_act(event, head=None, words=None):
    """Which act a bolt's landing card takes at its event (record 0031 §1, plan.16), from facts alone: ("change", note)
    once the bolt reads proven, at the merge's end or the rail's read, which row_card_change posts when no card is held,
    changes in place, its head moved, while the user has not answered it, and once they have leaves as it is, or
    follows with a new card when the head moved since their answer;
    ("close", None, reason) when a fix starts on the bolt, withdrawn as held for the fix, in its words; ("close",
    outcome, None) when it lands, the outcome landed_words'."""
    if event == "proven":
        return ("change", f"Its head is now {head[:7]}")
    if event == "fix":
        return ("close", None, f"held for a fix: {words}")
    if event == "preview":
        return ("change", words)
    return ("close", words, None)


def landing_unready(work, verified, fixes):
    """Why a bolt does not yet read proven (record 0031 §1, record 0025), or None: work is each of its units and chores
    as (name, kind, stage); verified, its verification as (state, words), whether its head is the landing of its work
    as the runner reports it (Stages.verification); fixes, the fixes of the bolt in flight. It reads proven once every
    unit and chore has merged, not every one has landed, its verification is green, and no fix is in flight on it,
    since a fix started on the bolt holds its landing until the fix merges or is dropped."""
    if not work:
        return "it holds no units or chores"
    for name, kind, stage in work:
        if stage not in ("merged", "landed"):
            return f"{kind} {name} has not merged: it is {stage}"
    if all(stage == "landed" for *_, stage in work):
        return "every unit and chore of it has landed"
    state, said = verified
    if state != "green":
        return f"its verification is not green: {said}"
    return f"{either(sorted(fixes))} is in flight on it" if fixes else None


def landing_facts(bolt, kit_name, work, head, at, due, unanswered, read_in, moved, pr):
    """The landing card's facts as cards.landing_card takes them, once the bolt reads proven by its kit (landing_unready):
    the bolt, its kit, its units and chores, the batch each unit was last read in (read_in), its head and when sluice
    landed it there (at), how many landings main has had since the bolt last met it (moved), and sluice's pull request
    at the head (pr) or None. None while a unit's latest change waits for a batch (due), or has been in one whose
    card the user has not answered (unanswered, awaiting_answer), since a bolt lands only once each has been in a batch
    the user has answered (briefs.12); a chore is in no batch."""
    units = [n for n, kind, _ in work if kind == "unit"]
    if any(u in due or u in unanswered for u in units):
        return None
    return dict(bolt=bolt, kit=kit_name, units=units, chores=[n for n, kind, _ in work if kind == "chore"],
                batches={u: read_in[u] for u in units if u in read_in}, head=head, at=at, moved=moved, pr=pr)


def pull_of(sluice_from, repo):
    """sluice's pull request for the submission at a head, from its Sluice-From trailer, `<agent> (pull/<n>)` when the
    submission went through one: {number, url} on the kit's GitHub, or None for a submission from a branch."""
    m = re.search(r"\(pull/(\d+)\)\s*$", sluice_from or "")
    return dict(number=int(m.group(1)), url=f"https://github.com/{repo}/pull/{m.group(1)}") if m else None


def last_submits(entries):
    """Each bolt's last bolt.submit entry, from the run record's entries, oldest first: {bolt: entry}. One marked
    Outcome queued is a landing in flight (submit_queued): no landing, no refusal and no stop."""
    last = {}
    for e in entries:
        if e.get("Act") != "bolt.submit":
            continue
        for o in e.get("On") or []:
            if o.startswith("bolt/"):
                last[o[5:]] = e
    return last


def sent_back(entries):
    """Each bolt whose landing Flume's verdict sent back for the bolt's own content, a failed check or a conflict, as
    crew recorded it from the runner's report (landing_entry), and whose refusal still stands (rail-cards "A bolt
    whose landing Flume refused is held at that head with no box", bolt-teams "No land is posted again until a fix moves the head sent back"), from the run
    record's entries, oldest first: {bolt: {head, words, n}}, from its last bolt.submit refused naming a head: the head
    its land carried, the words it was refused with (runner.landing_said), and the merge queue's entry Flume named,
    None when the entry names none. It stands through every bolt.submit after it that landed nothing at its head, since
    crew posts no land at a head sent back: a refusal naming no head, and a stop naming no entry of the merge queue's
    at that head, as an older crew recorded of a submit that submitted nothing (the Willdan box's 22:28Z stop of
    2026-11-06, signal 2026-11-06-wldn-ops-ea539623/01). Any other entry lifts it: a land asked or submitted, a
    landing, a stop naming an entry of its own, or one at another head. A decision of facts alone (code.7)."""
    out = {}
    for e in entries:
        if e.get("Act") != "bolt.submit":
            continue
        for b in [o[5:] for o in e.get("On") or [] if o.startswith("bolt/")]:
            if e.get("Refused") and e.get("Head"):
                out[b] = dict(head=e["Head"], words=e["Refused"], n=e.get("Submission") or None)
            elif b in out and (e.get("Refused") or e.get("Outcome") == "stopped" and not e.get("Submission")
                               and at_head(out[b]["head"], e.get("Head"))):
                continue
            else:
                out.pop(b, None)
    return out


def refusals(entries):
    """Each bolt whose landing Flume's verdict refused for the bolt's own content and still stands so (sent_back), from
    the run record's entries, oldest first: {bolt: (head, words)}, the head its land carried and the words it was
    refused with; a bolt whose landing since landed, was asked again or was stopped with an entry of its own, or that
    has none, is not in it."""
    return {b: (r["head"], r["words"]) for b, r in sent_back(entries).items()}


def stops(entries):
    """Each bolt whose last landing the runner or Flume stopped, nothing of the bolt's (rail-cards "A landing the runner
    or Flume stopped keeps its box", landing_entry), from the run record's entries, oldest first: {bolt: (head,
    words)}, the head its land carried and the runner's or Flume's words for what stopped it, from each bolt's last
    bolt.submit entry when it is marked Outcome stopped and names its Head; a bolt whose last one landed or was
    refused, or that has none, is not in it, nor one whose stop names no head, which no land of the bolt carried, nor
    one whose refusal Flume's verdict sent back still stands (sent_back), which a stop that landed nothing at its head
    leaves the bolt's fix."""
    held = sent_back(entries)
    return {b: (e["Head"], e.get("Why") or "") for b, e in last_submits(entries).items()
            if e.get("Outcome") == "stopped" and e.get("Head") and not e.get("Refused") and b not in held}


def stopped_at(stopped, bolt, head):
    """What stopped the bolt's last landing, in the words it was recorded with, when it was stopped at head, from the
    stops already read ({bolt: (head, words)}, stops), or None: one stopped at another head says nothing, the bolt's
    head having moved since, as a refusal at another head holds nothing (held_at)."""
    return held_at(stopped, bolt, head)


def held_at(refused, bolt, head):
    """refused_at from the refusals already read ({bolt: (head, words)}, refusals)."""
    at, words = refused.get(bolt, (None, None))
    return words if at and head and (at.startswith(head) or head.startswith(at)) else None


def send_stands(sent, head, work):
    """Whether the user's send on a kit's landings card still stands for a bolt they ticked at sent, now at head
    (rail-cards "A ticked bolt's approval stands while its own work is unchanged", record 0031 as amended 2026-10-24):
    the heads one by prefix, or the bolt's own work, its non-merge commits main lacks, read between them (work,
    bolt_work's {head, gained, lost, why}) with nothing gained and nothing lost. Work not read, or read with why, holds
    no send at another head (read.1). A decision of facts alone (code.7), runner.send_stood's, by which the lands a send
    makes due are judged too (runner.lands_due)."""
    return runner.send_stood(sent, head, work)


SAID_COMMITS = 5  # the subjects a bolt asked again names of each list, before how many more


def work_said(bolt, sent, head, work):
    """The words for a bolt the user ticked at sent and asked for again at head, whose send does not stand
    (send_stands, rail-cards "A ticked bolt whose own work changed is asked again, saying what changed"): its head now,
    then the subjects of its own commits it gained since the send and those it no longer holds, SAID_COMMITS of each
    at most and how many more; or why crew could not tell, in git's words (read.1)."""
    work, now = work or {"why": "crew read none of its work"}, f"{bolt}'s head is now {head[:7]}" if head else None

    def listed(commits):
        more = len(commits) - SAID_COMMITS
        return "; ".join([s for _, s in commits[:SAID_COMMITS]] + ([f"and {more} more"] if more > 0 else []))
    if work.get("why"):
        return ", but ".join(([now] if now else []) + [
            f"crew could not tell whether {bolt}'s own work changed since your send at {sent[:7]}: {work['why']}"])
    gained, lost = list(work.get("gained") or []), list(work.get("lost") or [])
    said = [now or f"{bolt}'s head has moved"]
    if gained:
        said.append(f"with work of its own since your send at {sent[:7]}: {listed(gained)}")
    if lost:
        said.append(f"and no longer holding: {listed(lost)}" if gained else
                    f"no longer holding work of its own your send at {sent[:7]} held: {listed(lost)}")
    return ", ".join(said)


# The words a take-main fix starts with (the landing read's, and main-level ops's for a landing that conflicts): a fix in
# flight with them holds its bolt's row as taking main first (rail-cards "A take-main fix holds its row as taking main
# first").
TAKE_MAIN = "Take main into the bolt"


def carries_said(carries, error=None):
    """What holds a bolt's landing while it carries another bolt's work (plan.8, gather.carried_bolts), as one clause, or
    None while it carries none: each bolt whose work it carries, with that bolt's landings it holds, which main lacks,
    and that it lands once main holds them, by that bolt's own landing; or, when what it carries can't be read
    (error), that crew can't tell, with why, which holds it too (read.1). The same words on its row, the rail's land
    line and crew bolts. A decision of facts alone (code.7)."""
    if error:
        return f"crew can't tell whether it carries another bolt's work, so it does not land: {error}"
    if not carries:
        return None
    return (f"carries {carried_named(carries)}, which main lacks; a bolt never carries another bolt's work to main, so "
            f"it lands once main holds that work, by the landing of {joined([f'bolt {b}' for b in sorted(carries)])}")


def carried_named(carries):
    """Each bolt whose work a branch carries, with that bolt's landings it holds by their short shas, as words:
    `bolt <b>'s work, its landing <sha>` (carries, {bolt: [commits]}, gather.carried_bolts)."""
    return joined([f"bolt {b}'s work, its " + ("landing " if len(cs) == 1 else "landings ") + ", ".join(c[:7] for c in cs)
                   for b, cs in sorted(carries.items())])


def landing_rows(order, rows, held, stopped=None, takes_main=None, left=()):
    """The rows of a kit's landings card (rail-cards, record 0031 as amended 2026-10-23), from facts alone: order, the
    plan's bolts of the kit by name, in its order; rows, {bolt: facts} for each that reads proven as a fix in flight on
    it leaves it (land_row), its facts carrying its head and its fixes in flight, {fix: the words it started with or
    None}; held, each bolt's last landing Flume's verdict refused for its own content, {bolt: (head, words)}
    (refusals); stopped, each bolt's last landing the runner or Flume stopped, nothing of the bolt's, the same (stops);
    takes_main, each bolt forecast to conflict with what main holds at its present head, {bolt: (main's short sha,
    [paths])}, by the card's forecast or the run record's (main_conflict). In the plan's order, each {bolt, box: True,
    facts}, a row the user ticks, its facts carrying stopped, (head, words), when its last landing was stopped at its
    present head (stopped_at), which holds nothing (rail-cards "A landing the runner or Flume stopped keeps its box");
    or {bolt, box: False, why, facts}, held with no box: while its facts say it carries another bolt's work main lacks,
    or that what it carries can't be read (carries, carries_error; carries_said), whatever else holds it, so no landing
    card is raised for it nor its row marked able to land (plan.8); for a fix in flight on it, in the fix's words, or
    for Flume's refusal of its landing at its present head, in Flume's words, the row saying the landing was rejected
    and the bolt is open for work, until a fix on the bolt moves the head (rail-cards "A refused row says whether it waits
    for a fix or takes main first"); or, marked takes_main, taking main first,
    forecast to conflict with main, or with only take-main fixes in flight (TAKE_MAIN), each named with its words; but a
    bolt the user left (left, left_now) marked takes_main keeps its box, its facts marked would_main, (main's short
    sha, [paths]), for its row to say it would take main first once ticked (rail-cards "A row the user left keeps
    its box and says whether it would take main first"). A bolt not in rows is no row."""
    out, stopped, takes_main = [], stopped or {}, takes_main or {}
    for b in [b for b in order if b in rows]:
        f = rows[b]
        fixes = f.get("fixes") or {}
        at, words = held.get(b, (None, None))
        main_first = bool(fixes) and all((note or "").startswith(TAKE_MAIN) for note in fixes.values())
        carry = carries_said(f.get("carries"), f.get("carries_error"))
        if f.get("legacy"):  # started before bolts were base places: no land is posted for it (Decision 9)
            why, main_first = f["legacy"], False
        elif carry:  # another bolt's work it carries holds it as a conflict does, whatever else holds it (plan.8)
            why, main_first = f"held: {carry}", False
        elif fixes:
            why = "; ".join(f'takes main first: {fix.rsplit("/", 1)[-1]} taking main in: "{note}"' if (note or "").startswith(TAKE_MAIN)
                            else f"held for a fix: {note} ({fix})" if note else f"held for {fix} until it merges or is dropped"
                            for fix, note in sorted(fixes.items()))
        elif at and (at.startswith(f["head"]) or f["head"].startswith(at)):
            why = f"landing rejected at {f['head'][:7]}, open for work: it waits for a fix on the bolt: {words}"
        elif b in takes_main and b not in left:
            main, paths = takes_main[b]
            why, main_first = (f"takes main first: forecast to conflict with main on {joined(list(paths))} at {main[:7]}, "
                               "until a fix taking main in moves its head"), True
        else:
            stop = stopped_at(stopped, b, f["head"])
            marks = dict(**({"stopped": (stopped[b][0], stop)} if stop else {}),
                         **({"would_main": (takes_main[b][0][:7], list(takes_main[b][1]))} if b in takes_main else {}))
            out.append(dict(bolt=b, box=True, facts=dict(f, **marks) if marks else f))
            continue
        out.append(dict(bolt=b, box=False, why=why, facts=f, **({"takes_main": True} if main_first else {})))
    return out


def card_rows(rows):
    """The rows a kit's landings card shows (rail-cards "A row taking main first stays on the card"), from its rows as
    landing_rows gives them, less those an earlier send still lands (rows_unsent): while any row can land, each that can
    and each held only to take main first beside it (landing_rows' takes_main), but one an earlier send lands (sent),
    in the plan's order; none while no row can land, since no card is raised then (plan.8). A row taking main first
    shown so keeps its place as its bolt takes main in and comes back, so its coming and going keeps the card's form
    (cards.landings_form) and changes the card in place, where its leaving the card would follow it. A decision of
    facts alone (code.7)."""
    if not any(r["box"] for r in rows):
        return []
    return [r for r in rows if r["box"] or r.get("takes_main") and not r.get("sent")]


def card_heads(text):
    """A kit's landings card's rows as its post or change recorded them (built_fields): [(bolt, head, left)] in the
    card's order, left whether the user cleared it on their last send; [] for none recorded. A row the card showed
    taking main first, marked :main, is among them, never left (heads_taking)."""
    out = []
    for w in (text or "").split():
        m = re.fullmatch(r"([a-z0-9][a-z0-9-]*)@([0-9a-f]{7,40})(:left|:main)?", w)
        if m:
            out.append((m.group(1), m.group(2), m.group(3) == ":left"))
    return out


def heads_taking(text):
    """The rows a kit's landings card's post or change recorded as taking main first, marked :main (cards.landings_card,
    rail-cards "A row taking main first stays on the card"): their bolts."""
    return {m.group(1) for w in (text or "").split() for m in [re.fullmatch(r"([a-z0-9][a-z0-9-]*)@[0-9a-f]{7,40}:main", w)] if m}


def at_head(head, now):
    """Whether a head recorded short or whole (head) is the bolt's head now (now), either a prefix of the other."""
    return bool(head and now) and (now.startswith(head) or head.startswith(now))


def left_marks(entries, key):
    """What the run record holds of the bolts the user left on a kit's landings card (rail-cards "A bolt the user left
    stays left until they tick it"), from the entries, oldest first: the last set a raise of the card under key recorded
    (a landing.left not refused with that Key, its Heads <bolt>@<head7> each), {bolt: head7}, and each stop main-level
    ops recorded after it on the user's words in its pane (bolt.leave, its Head), [(bolt, head)]. No word in a pane
    lands a bolt (record 0056 point 5), so only the user's tick lifts a stop (left_now). The bolts of every kit are
    among the stops, which the kit's heads sort out (left_now, left_of)."""
    recorded, stops = {}, []
    for e in entries:
        act = e.get("Act")
        if e.get("Refused") or act not in ("landing.left", "bolt.leave"):
            continue
        bolt = next((o[5:] for o in e.get("On") or [] if o.startswith("bolt/")), None)
        if act == "landing.left" and e.get("Key") == key:
            recorded, stops = {b: h for b, h, _ in card_heads(e.get("Heads"))}, []
        elif act == "bolt.leave" and bolt and e.get("Head"):
            stops.append((bolt, e["Head"]))
    return recorded, stops


def left_now(card, ticked, heads, recorded, stops):
    """The bolts of a kit's landings card the user left, at a raise of it (rail-cards "A bolt the user left stays left
    until they tick it", "A bolt stopped in ops's pane is shown as left"), from facts alone (code.7): card, the card ops
    holds as kit_card_state reads it, {status, heads}, or None; ticked, the bolts the user ticked on it once answered;
    heads, {bolt: its head now} of each row of the kit read now; recorded and stops, as left_marks gives them. A bolt at
    its head now is left when it is marked left on the card held while it waits, the card held is answered and the user
    did not tick its row, or the record names it left or stopped and the card held has not ticked it; one the user
    ticked, one at another head, one that is no row and one the card showed taking main first, unticked by crew's own
    hand (card's taking), are not. {bolt: head7}."""
    status = (card or {}).get("status")
    ticks = set(ticked or []) if status == "answered" else set()
    taking = set((card or {}).get("taking") or ())
    out = {}
    for b, h, marked in (card or {}).get("heads") or []:
        if b in taking:
            continue
        if at_head(h, heads.get(b)) and (marked if status == "waiting" else status == "answered" and b not in ticks):
            out[b] = heads[b][:7]
    for b, h in list(recorded.items()) + list(stops):
        if b not in ticks and at_head(h, heads.get(b)):
            out.setdefault(b, heads[b][:7])
    return out


def left_of(entries, key, heads):
    """The bolts of a kit's landings card the user left, as the run record holds them (left_marks): the last set its
    raise recorded and each stop recorded since, kept only at the bolt's head now (heads, {bolt: head}); a tick on a
    send, read by the raise that recorded the set, a moved head or a landing on the user's words ending one. Which the
    rail reads, not seeing the card. {bolt: head7}."""
    recorded, stops = left_marks(entries, key)
    return {b: heads[b][:7] for b, h in list(recorded.items()) + stops if at_head(h, heads.get(b))}


def landings_sent(entries, key, owner):
    """The bolts the user's send on a kit's landings card still landed when a new card followed it (landings_step's
    follow), from the run record's entries, oldest first: {bolt: the head they ticked}, from the Heads of each close of
    a card under key in owner's name that carries them, the last for each bolt; {} for none."""
    out = {}
    for e in entries:
        if e.get("Act") == "card.close" and not e.get("Refused") and e.get("Key") == key and e.get("By") == owner:
            out.update({b: h for b, h, _ in card_heads(e.get("Heads"))})
    return out


def rows_unsent(rows, sent, work=None):
    """A kit's landings card's rows (landing_rows) less each that can land on an earlier send that still stands for it
    (landings_sent, send_stands), at the head sent or at a head whose own work is the same (work, bolt_work's for each
    bolt whose head moved), which is no row of a card that follows that send's, nor of any after it; those bolts; and
    each that can land whose send does not stand, a row again, with the words that say what changed (work_said):
    (rows, [bolt], [(bolt, words)]). A row taking main first whose earlier send stands stays held with no box, marked
    sent, since that send lands it once it reads proven (card_rows). A decision of facts alone (code.7)."""
    work, out, landing, asked = work or {}, [], [], []
    for r in rows:
        b, head = r["bolt"], r["facts"]["head"]
        at = sent.get(b)
        if r["box"] and at and send_stands(at, head, work.get(b)):
            landing.append(b)
            continue
        if not r["box"] and r.get("takes_main") and at and send_stands(at, head, work.get(b)):
            out.append(dict(r, sent=True))
            continue
        out.append(r)
        if r["box"] and at:
            asked.append((b, work_said(b, at, head, work.get(b))))
    return out, landing, asked


def sent_left(sent, now, in_plan, refused, work=None):
    """The bolts an earlier send on a kit's landings card still lands (landings_sent's sent, {bolt: the head they
    ticked}), in the order sent, which crew card read land/<kit> prints with or without a card open, so the send is read
    though its card closed before ops read it: each the plan still holds (in_plan) whose head now is read (now, {bolt:
    its head or None}), whose send stands there (send_stands, work bolt_work's between the two), and that sluice did not
    refuse at its head now (refused, refusals), a refusal at the head sent holding nothing once a fix on it moved it;
    and beside them each it can't tell of, its head now unread or its work not compared, with why (read.1): (bolts,
    [(bolt, why)]). A decision of facts alone (code.7)."""
    work, out, unknown = work or {}, [], []
    for b, h in sent.items():
        if b not in in_plan:
            continue
        w = work.get(b) or {}
        if not now.get(b):
            unknown.append((b, w.get("why") or f"crew read no head of bolt/{b}"))
        elif send_stands(h, now[b], work.get(b)):
            if not held_at(refused, b, now[b]):
                out.append(b)
        elif w.get("why"):
            unknown.append((b, w["why"]))
    return out, unknown


def ticked_of(got, heads):
    """The bolts the user ticked on a kit's landings card, in the card's order (heads, card_heads), from get_request's
    answer on their turn: the one row of an approval they approved, none of one they declined; each box of a list,
    land:<bolt>, from its choiceIds, or each question's of lists. None while they have not answered."""
    answer = got.get("answer") if isinstance(got, dict) and got.get("status") == "answered" else None
    if not isinstance(answer, dict):
        return None
    if isinstance(answer.get("approved"), bool):
        return [heads[0][0]] if answer["approved"] and heads else []
    picked = [c for c in answer.get("choiceIds") or [] if isinstance(c, str)]
    for a in (answer.get("answers") or {}).values() if isinstance(answer.get("answers"), dict) else []:
        picked += [c for c in (a.get("choiceIds") or [] if isinstance(a, dict) else []) if isinstance(c, str)]
    return [b for b, _, _ in heads if f"land:{b}" in picked]


def landings_step(rows, card, ticked, in_plan, landed=None, note=None, work=None):
    """What the raise of a kit's landings card does with it (rail-cards, record 0031 as amended 2026-10-23), from facts
    alone (code.7): rows, its rows as landing_rows gives them; card, None when ops holds none, else {status, heads},
    status "waiting" or "answered" and heads its rows as its last post or change recorded them (card_heads); ticked,
    the bolts the user ticked on it once answered (ticked_of); in_plan, the kit's bolts the plan still holds; landed,
    {bolt: the commit GitHub's main holds} for each that landed (the bolt.land entries); note, the event's own change
    note; work, each ticked bolt's own work between the head the card showed and its head now, for those whose head
    moved (bolt_work), by which the user's send still stands for a bolt that only took main in (send_stands, record
    0031 as amended 2026-10-24). Each act with the bolts the user cleared on their last send (left), which its card
    shows unticked:
    ("none",) when no row can land and no card is held;
    ("withdraw", why) when no row can land and a waiting card is held, each row held or none proven;
    ("post", left) when rows can land and no card is held, following the kit's last card only when that one was
    answered and closed with rows left (cards.follows_of);
    ("change", note, kind_changed, left) when a waiting card is held and its rows (card_rows, a row taking main first
    among them, marked so on the card, card's taking), their heads, whether each takes main first, or the event changed
    it, its form changed or not (cards.landings_form), followed then rather than changed; ("leave",) when nothing did;
    ("leave",) when an answered card is held while any bolt the user ticked is still to land on their send, in the
    plan, not held, or held only taking main first (landing_rows' takes_main), and its send standing at its head now,
    which stands while it takes main in, one landed and not yet closed among them, and no row reads proven since but at
    a head their send still stands at;
    ("follow", outcome, left, landing) when one does, a bolt on no row of the card or at a head the card did not show
    whose send does not stand, which is never added to the card they answered: it is closed saying what landed, what
    their send still lands, each whose last landing at its head sluice or its host stopped with what stopped it (its
    row's stopped, landing_rows), which holds nothing, what takes main in first, what was held and what was left, a
    row the card showed taking main first and left unticked being no bolt they left, and what changed of a ticked bolt
    asked again (work_said), and a new card follows it with every row that can land but
    those their send still lands (landing, each (bolt, the head they ticked), a held one whose send stands among them);
    ("close", outcome, then, standing) once none is still to land, the outcome saying what landed and where GitHub's
    main holds it, what was held and why, what was left and what reads proven since, then the bolts left when rows can
    land, for a new card that follows it, else None, then each ticked bolt held whose send still stands, (bolt, the
    head they ticked), which the close keeps, saying so, for it to land on that send once a fix on it has only taken
    main in; a send ticking none closes it at once, landing nothing. A bolt left on the last send is shown
    unticked on the card that follows only while its head stands."""
    boxed = [r for r in rows if r["box"]]
    now = [(r["bolt"], r["facts"]["head"][:7]) for r in boxed]
    held = {r["bolt"]: r["why"] for r in rows if not r["box"]}
    if card is None:
        return ("post", []) if boxed else ("none",)
    heads = card.get("heads") or []
    if card["status"] != "answered":
        if not boxed:
            return ("withdraw", "every bolt waiting to land is held: "
                    + "; ".join(f"{b}, {w}" for b, w in held.items()) if held else "no bolt waits to land on its main")
        shows = card_rows(rows)
        shown = [(r["bolt"], r["facts"]["head"][:7]) for r in shows]
        taking, took = {r["bolt"] for r in shows if not r["box"]}, set(card.get("taking") or ())
        was = {b: (h, left) for b, h, left in heads}
        left = [b for b, h in now if b in was and was[b][1] and was[b][0] == h]
        said = [f"{b} joins the card and {held[b]}" if b in taking else f"{b} reads proven and joins the card"
                for b, _ in shown if b not in was]
        said += [f"{b}'s head is now {h}" for b, h in shown if b in was and was[b][0] != h]
        said += [f"{b} {held[b]}" for b, _ in shown if b in was and b in taking and b not in took]
        said += [f"{b} can land again" for b, _ in shown if b in was and b not in taking and b in took]
        said += [(f"{b} {held[b]}" if held[b].startswith("takes main first") else f"{b}'s {held[b]}" if held[b].startswith("landing ")
                  else f"{b} is {held[b]}") if b in held
                 else f"{b} no longer waits to land" for b, _, _ in heads if b not in dict(shown)]
        said = ([note] if note else []) + said
        if not said:
            return ("leave",)
        return ("change", "; ".join(said), cards.landings_form(len(heads)) != cards.landings_form(len(shown)), left)
    ticked, work = list(ticked or []), work or {}
    was, took = {b: h for b, h, _ in heads}, set(card.get("taking") or ())
    at = {r["bolt"]: r["facts"]["head"] for r in rows}

    def stands(b):  # the user's send still stands for a bolt they ticked, at its head now
        return b in ticked and b in was and send_stands(was[b], at[b], work.get(b))
    # proven since the send: on no row of the card, at a new head their send does not stand at, or shown taking main
    # first and left unticked by crew
    anew = [(b, h) for b, h in now if (was.get(b) != h or b in took) and not stands(b)]
    moved = {b for b, _ in anew}
    main_first = {r["bolt"] for r in rows if not r["box"] and r.get("takes_main")}  # its send stands while it takes main in
    # a ticked bolt whose land on this send the runner or Flume stopped: the send is spent, so the card closes naming it
    # and the card that follows asks for it again (crew-lands-each-bolt-through-flumes-base-place, Decision 7)
    spent = {r["bolt"] for r in rows if r["box"] and r["facts"].get("stopped")}
    landing = [b for b in ticked if b in in_plan and (b not in held or b in main_first and stands(b)) and b not in moved
               and b not in spent]  # in flight or not yet submitted
    standing = [b for b in ticked if b in in_plan and b in held and b not in landing and stands(b)]
    if landing and not anew:
        return ("leave",)
    on = [b for b, _, _ in heads]
    gone = [b for b in ticked if b not in in_plan]
    said = ([f"Landed on GitHub's main: " + joined([f"{b} at {landed[b][:7]}" if b in (landed or {}) else b for b in gone])
             + "; every host's folder follows by swancloud's timer within minutes."]
            if gone and all(b in (landed or {}) for b in gone) else
            [f"Landed or left the plan: {joined(gone)}."] if gone else [])
    lands = [b for b in landing if b not in main_first]
    said += [f"Asked of the runner as you ticked: {joined(lands)}."] if lands else []
    stopped = {r["bolt"]: r["facts"]["stopped"] for r in boxed if r["facts"].get("stopped")}
    said += [f"{b}'s landing at {stopped[b][0][:7]} was stopped, nothing of the bolt's: {stopped[b][1].rstrip('.')}; your send of "
             "it is spent, and the card that follows asks for it again." for b in ticked if b in spent]
    said += [f"Taking main in first, your send standing for it: {joined([b for b in landing if b in main_first])}."] if len(lands) < len(landing) else []
    said += [f"Held: {b}, {held[b]}; your send stands for it: it lands once a fix on it has only taken main in and "
             "it reads proven at its new head, with nothing asked." if b in standing else
             f"Held: {b}, {held[b]}; {work_said(b, was[b], at[b], work.get(b))}, so a card asks for it again once it reads "
             "proven." for b in ticked if b in held and b not in landing]
    cleared = [b for b in on if b not in ticked and b not in took]  # crew unticked a row taking main first, not they
    said += [f"Left: {joined(cleared)}."] if cleared else []
    said += ["Since your send, " + "; ".join(work_said(b, was[b], at[b], work.get(b)) if b in was and b in ticked else
                                             f"{b}'s head is now {h}" if b in was and was[b] != h else f"{b} reads proven"
                                             for b, h in anew)
             + f", and the card that follows asks for {'it' if len(anew) == 1 else 'them'}."] if anew else []
    if not ticked:
        said = ["Sent with no bolt ticked, so nothing lands."] + said
    left = [b for b in cleared if b in dict(now) and b not in moved]
    if landing:
        return ("follow", " ".join(said), left, [(b, was[b]) for b in ticked if b in landing or b in standing])
    return ("close", " ".join(said), left if boxed else None, [(b, was[b]) for b in standing])


def landings_since(earlier, rows):
    """What changed since the user's send on a kit's last landings card, which a new card raised after it, following it
    (cards.follows_of), says first (rail-cards "A follow-on card says what changed in the words its event gives"), from facts
    alone (code.7): earlier, that card's rows as its last post or change recorded them (card_heads); rows, the rows
    that can land now (landing_rows, with a box). Each bolt that joins the card, each head that moved, and each bolt
    still waiting at the head the card showed, which the user's send left; sentences."""
    was = {b: h for b, h, _ in earlier}
    joins = [r["bolt"] for r in rows if r["bolt"] not in was]
    moved = [(r["bolt"], r["facts"]["head"][:7]) for r in rows if r["bolt"] in was
             and not (r["facts"]["head"].startswith(was[r["bolt"]]) or was[r["bolt"]].startswith(r["facts"]["head"]))]
    waits = [r["bolt"] for r in rows if r["bolt"] in was and r["bolt"] not in dict(moved)]
    return ([f"{joined(joins)} {'reads' if len(joins) == 1 else 'read'} proven and {'joins' if len(joins) == 1 else 'join'} the card."]
            if joins else []) + [f"{b}'s head is now {h}." for b, h in moved] + (left_waits(waits) if waits else [])


def left_waits(left):
    """The sentence a kit's landings card that follows the user's send says of the bolts that send left, shown again."""
    return [f"{joined(left)}, which you left, {'waits' if len(left) == 1 else 'wait'} on this card."]


def row_forecasts(order, pairs, held=()):
    """Each row's forecast conflicts (rail-cards "Each landings row carries its forecast conflicts, or why none could be made"), from facts alone
    (code.7): order, the bolts of the card's rows that can land, in its order; pairs(ours, theirs), the paths git
    forecasts in conflict when the bolt ours is merged onto theirs, "main" or a bolt above it on the card, from their
    merge base: [] for none, None when git can't tell; held, the bolts the run record holds taking main first
    (main_conflict). {bolt: [(with, paths)]}, main first, then each bolt above it in the card's order, a pair with no
    conflict left out and one git could not tell kept with paths None, a forecast not made, which holds nothing; an
    empty list, no conflict forecast. Every bolt is forecast against main first, and one forecast to conflict with it,
    or held, takes main first (landing_rows), so it is forecast against main alone and no row is forecast against it:
    the rest are forecast among themselves, pairwise, as units are (teams.12)."""
    mains = {b: pairs(b, "main") for b in order}
    rest = [b for b in order if not mains[b] and b not in held]
    return {b: [(w, p) for w, p in [("main", mains[b])] + ([(w, pairs(b, w)) for w in rest[:rest.index(b)]] if b in rest else [])
                if p is None or p] for b in order}


def tree_paths(rc, out):
    """The paths `git merge-tree --write-tree --name-only --no-messages` names in conflict, from its exit and output:
    [] for a clean merge (0), the paths after the tree's id (1), each once; None for any other exit."""
    if rc == 0:
        return []
    if rc != 1:
        return None
    return list(dict.fromkeys(l for l in out.split("\n")[1:] if l))


def forecast_rows(fleet, label, kit, bolts, held=()):
    """The forecasts of a kit's landings card's rows (row_forecasts, held the bolts it is handed as taking main first by
    the run record), made in the kit's folder where its work runs (kit_at): GitHub's main fetched there, a kit with no
    origin reading its own; each bolt read
    where it lives (gather.bolt_at, plan.19), GitHub's copy when the policy in it names a remote for the bolt, else the
    host's, a bolt made before gives went through sluice; and git merge-tree of each onto main and onto each bolt above
    it. Returns ({bolt: [(with, paths)]}, {bolt: why}, at),
    why for each bolt whose forecast crew could not make, or that has one not made against another it could not read:
    a branch on no ref it can read, a fetch or a git that failed, or crew not telling where the kit's work runs, said
    and holding nothing (read.1); at, the revision of main forecast against, {"main": <sha>}, the commit origin/main
    names after the fetch or main for a kit with no origin, or None when the fetch or the read of it failed."""
    try:
        t = kit_at(fleet, label, kit)
        main, host = t["kit"]["main"], t["machine"]
        origin = origin_fetched(fleet, t, main)
        name = "refs/remotes/origin/main" if origin else "refs/heads/main"
        rc, sha = kit_git(fleet, t, main, "rev-parse", "--verify", "-q", f"{name}^{{commit}}", ok=(0, 1))
        rc == 0 and sha or fail(f"{main} on {host} has no {'origin/main' if origin else 'branch main'} to forecast against")
    except Refusal as e:
        return {b: [("main", None)] for b in bolts}, {b: str(e) for b in bolts}, None
    at, why = bolts_where(fleet, t, main, origin, bolts)
    refs = {"main": sha, **at}

    def pairs(ours, theirs):
        if ours in why or theirs in why:
            return None
        try:
            return tree_paths(*kit_git(fleet, t, main, "merge-tree", "--write-tree", "--name-only", "--no-messages",
                                       refs[theirs], refs[ours], ok=(0, 1)))
        except Refusal:
            return None
    got = row_forecasts(bolts, pairs, held)
    for b, fs in got.items():
        for w, paths in fs:
            if paths is None and b not in why:
                why[b] = why.get(w) or f"git merge-tree could not tell in {main} on {host}"
    return got, why, {"main": sha}


def origin_fetched(fleet, t, main):
    """Whether the kit's folder on the host its work runs on (t) has an origin, GitHub, fetched there when it has, as one
    try to the family's limit on that host (ORIGIN_FETCH through fetch_told and host_run; weir 69, C.3); refused naming
    the host with git's words or the stopped try's when the fetch fails (plan.18). In the runner's clone nothing is
    fetched, and origin's tracking refs are read as the runner last fetched them (crew.fetches_in)."""
    origin = kit_git(fleet, t, main, "remote", "get-url", "origin", ok=(0, 2))[0] == 0
    if origin and crew.fetches_in(fleet, t["machine"], main):
        host_run(fleet, t["machine"], fetch_told(fleet, t["machine"], main, ORIGIN_FETCH), main)
    return origin


def bolts_where(fleet, t, main, origin, bolts):
    """Each bolt's head where it lives (gather.bolt_at, plan.19), read in the kit's folder on its host (t)
    once fetched (origin_fetched): GitHub's copy when the policy in it names a remote for the bolt, else the host's.
    Returns ({bolt: commit}, {bolt: why}), why for each on no ref crew can read there, or whose policy or git failed."""
    host, refs, why = t["machine"], {}, {}
    for b in bolts:
        github, own, at = f"refs/remotes/origin/bolt/{b}", f"refs/heads/bolt/{b}", {}
        try:
            for ref in ([github] if origin else []) + [own]:
                rc, out = kit_git(fleet, t, main, "rev-parse", "--verify", "-q", f"{ref}^{{commit}}", ok=(0, 1))
                if rc == 0 and out:
                    at[ref] = out
            rc, text = kit_git(fleet, t, main, "show", f"{github}:{gather.POLICY}", ok=(0, 128)) if github in at else (1, None)
            ref = gather.bolt_at(b, github in at, own in at, gather.policy_remote(text if rc == 0 else None, f"bolt/{b}"))
        except Refusal as e:
            why[b] = str(e)
            continue
        except ValueError as e:
            why[b] = f"{gather.POLICY} at origin/bolt/{b} is not TOML, so crew can't read bolt {b}: {e}"
            continue
        if ref:
            refs[b] = at[ref]
        else:
            why[b] = f"bolt/{b} is on no branch crew can read in {main} on {host}, GitHub's or the host's"
    return refs, why


def commits_listed(out):
    """git log --format='%h %s''s lines as [(sha, subject)], newest first."""
    return [tuple(l.split(" ", 1)) if " " in l else (l, "") for l in out.splitlines() if l.strip()]


def bolt_work(fleet, label, kit, moves):
    """Each bolt's own work between the head the user sent and its head now (rail-cards "A ticked bolt's approval
    stands while its own work is unchanged", Decision 1), read where the kit's forecasts are made (forecast_rows), in
    the kit's folder where its work runs (kit_at), GitHub's main fetched there once: a bolt's own work at a head being
    its non-merge commits main lacks, what it gained is `git log --no-merges <now> ^<sent> ^<main>` and what it lost
    `<sent> ^<now> ^<main>`, main GitHub's, or a kit's own with no origin. moves, {bolt: (sent, head)}, head None for
    one read where the bolt lives (bolts_where). Returns {bolt: {head, gained, lost, why}}, gained and lost
    [(sha, subject)], why set when crew could not tell, the fetch, the head sent or now, or git having failed, or where
    the kit's work runs (read.1)."""
    def told(head, why):
        return dict(head=head, gained=[], lost=[], why=why)
    try:
        t = kit_at(fleet, label, kit)
        main, host = t["kit"]["main"], t["machine"]
        origin = origin_fetched(fleet, t, main)
    except Refusal as e:
        return {b: told(h, str(e)) for b, (_, h) in moves.items()}
    mains = "refs/remotes/origin/main" if origin else "refs/heads/main"
    at, unread = bolts_where(fleet, t, main, origin, [b for b, (_, h) in moves.items() if not h])
    out = {}
    for b, (sent, head) in moves.items():
        head = head or at.get(b)
        if not head:
            out[b] = told(None, unread.get(b) or f"bolt/{b} is on no branch crew can read in {main} on {host}")
            continue
        try:
            for what, rev in (("your send's head", sent), ("its head now", head)):
                rc, _ = kit_git(fleet, t, main, "rev-parse", "--verify", "-q", f"{rev}^{{commit}}", ok=(0, 1, 128))
                rc == 0 or fail(f"{what}, {rev[:7]}, names no one commit in {main} on {host}")
            gained = commits_listed(kit_git(fleet, t, main, "log", "--no-merges", "--format=%h %s", head, f"^{sent}", f"^{mains}")[1])
            lost = commits_listed(kit_git(fleet, t, main, "log", "--no-merges", "--format=%h %s", sent, f"^{head}", f"^{mains}")[1])
        except Refusal as e:
            out[b] = told(head, str(e))
            continue
        out[b] = dict(head=head, gained=gained, lost=lost, why=None)
    return out


def batch_waits(units, due, unanswered):
    """Why a bolt that otherwise reads proven has no landing card yet (briefs.12), as landing_facts holds it: the units
    whose latest change no batch has held (due), then the batches holding a unit's latest change whose card the user
    has not answered (unanswered, {unit: batch}); None when neither holds it."""
    late = [u for u in units if u in due]
    held = sorted({unanswered[u] for u in units if u in unanswered and u not in due})
    said = ([f"{either(late)} {'has' if len(late) == 1 else 'have'} not been in a batch, which is due"] if late else []) + (
        [f"the user has not answered batch{'' if len(held) == 1 else 'es'} {joined([str(n) for n in held])}"] if held else [])
    return "; ".join(said) or None


def land_held(fleet, label, bolt):
    """The drive's plan, the bolt and where its work runs (bolt_at), as a landing reads them: the bolt None when
    the plan holds none by that name, where None when it is not started. Refused when the plan can't be read, or crew
    can't tell where its work runs (read.1)."""
    plan = plan_of(fleet, label) or fail(f"{label}/main could not be read, so whether bolt {bolt} reads proven can't be told")
    b = plan.bolt(bolt)
    return plan, b, bolt_at(fleet, label, b) if b else None


def land_facts(fleet, label, plan, b, t, fixes_hold=True):
    """A started bolt's landing facts, read on the host its work runs on (t, bolt_at), so its row on its kit's landings
    card (land_row) and its reading (crew card session) read the same bolt: (facts, None) once it reads proven
    (landing_unready, landing_facts), the row's facts as cards.landings_card takes them with what the reading's writer
    needs beside them, its host, the kit's folder there (main), its repository as the plan names it (repo, for where its
    diff is read whole) and where the bolt last met main (base); (None, why) while it does not. With
    fixes_hold False, a fix in flight on it does not keep it from reading proven, and the facts hold each such fix with
    the words it started with ({fix: its launch's brief}, runner.fixes_in_flight over Stages.fixes, so a fix read
    merged from its bolt's landing holds nothing), the bolt's last landing sluice
    refused ((head, words),
    refusals) or None, for landing_rows to hold its row by, and its last one sluice or its host stopped ((head, words),
    stops) or None, for its row to say, and, for a bolt started before bolts were base places, legacy, the words that
    say it lands under the crew that started it (runner.legacy_said), for landing_rows to give it no box. Refused when
    its kit can't be read (read.1)."""
    bolt = b.name()
    st = stages_for(fleet, label, plan, [b])
    k, why = st.kit(b)
    not why or fail(f"bolt {bolt}'s kit could not be read: {why}")
    of = {u.name(): st.of(u.name()) for u in plan.work_of(bolt)}
    work = [(n, s.get("kind", "unit"), s["stage"]) for n, s in of.items()]
    facts = k["bolts"].get(bolt, {})
    # A started bolt holds its fixes as Flume places, read as crew bolts reads them (Stages.fixes): from their launches,
    # the runner's records and the bolt's landings, each with its brief for its words, and the live landing fix of its
    # base place (Decision 10 of teams-cross-to-flume-as-their-bolts-land; plan.12; crews-bolt-kind-names-its-landing-fix,
    # Decision 5).
    run = runner_facts(fleet, label) if crossed_bolt(plan, bolt) else None
    flume = runner.fixes_in_flight(st.fixes(b), bolt, *run) if run else {}
    # a bolt started before bolts were base places lands under the crew that started it, and has no box (Decision 9)
    legacy = runner.legacy_said(bolt) if run and runner.launch_of(run[0], f"bolt/{bolt}") is None else None
    fixes = sorted(flume)
    why = landing_unready(work, st.verification(b, facts.get("head"), facts.get("head_landing")), fixes if fixes_hold else [])
    if why:
        return None, why
    entries = drive_entries(fleet, label)
    read_in = {}
    for n, _, us in batches(entries):
        for u, _, _ in us:
            read_in[u] = n
    main, head = t["kit"]["main"], facts["head"]
    now = gather.now_ref(gather.has_origin(main))  # the kit's main now, as its stages read it (plan.18)
    _, base = kit_git(fleet, t, main, "merge-base", facts["at"], now)  # the bolt where it is read (gather.bolt_read)
    _, moved = kit_git(fleet, t, main, "rev-list", "--count", "--first-parent", f"{base}..{now}")
    _, came = kit_git(fleet, t, main, "log", "-1", "--format=%(trailers:key=Sluice-From,valueonly)", head)
    crossed = crossed_changes(plan, st)  # a crossed unit's change, once landed on its bolt (Decision 13)
    due, unanswered = {u for u, *_ in due_changes(plan, entries, crossed)}, awaiting_answer(entries, crossed)
    came = came.strip()
    card = landing_facts(bolt, t["kit"]["name"], work, head, facts.get("head_at"), due, unanswered, read_in, int(moved),
                         pull_of(came, forge(fleet, t)) if pull_of(came, "") else None)
    if not card:
        return None, batch_waits([n for n, kind, _ in work if kind == "unit"], due, unanswered)
    held = {} if fixes_hold else dict(fixes={f: flume[f] for f in fixes}, refusal=refusals(entries).get(bolt),
                                      stop=stops(entries).get(bolt))
    # Another bolt's work it carries, or why that can't be read (gather.carried_bolts), for landing_rows to hold it by (plan.8).
    carry = {x: facts[x] for x in ("carries", "carries_error") if facts.get(x)}
    return dict(card, host=t["machine"], main=t["kit"]["main"], repo=t["kit"]["repo"], base=base, **held, **carry,
                **({"legacy": legacy} if legacy else {})), None


def landing_retry(why, fresh, fresh_why):
    """What follows a first refusal of a landing's reading at a raise (card-sessions "A landing's row tries its
    reading once more on the bolt's host"), from that refusal (why), the landing read afresh once the kit's main was
    fetched, as land_facts gives it (fresh, (facts, why it does not read proven)), or why that read was refused
    (fresh_why, fresh None): ("again", facts) to open the reading once more with the fresh facts, the card's from then;
    ("none", None) when the bolt no longer reads proven, so the raise posts and changes nothing; ("stand", why) when
    the fresh read was refused, the first facts and the first reason standing (read.1)."""
    if fresh_why:
        return "stand", why
    facts, unproven = fresh
    return ("none", None) if unproven else ("again", facts)


def landing_opened(fleet, label, plan, b, t, card, acts):
    """A landings row's facts with its reading opened by its read (land_row), before the card is built: its link,
    or on a refusal one more try as crew card session land/<bolt> makes it, the kit's main fetched on the team's host,
    this one, as one try to the family's limit (ORIGIN_FETCH), a fetch that failed or stopped said and the try going on
    (plan.18), nothing fetched in the runner's clone, where
    the kit's main is read as the runner last fetched it (crew.fetches_in), the landing read afresh (land_facts) and its
    reading opened again with those facts (landing_retry). The facts the card is built from, carrying the reading's
    link or why it could not be opened (unread, the second try's reason, or the first's when the fresh read was
    refused); None when, read afresh, the bolt no longer reads proven, so the raise posts and changes nothing."""
    key, main = f"land/{card['bolt']}", t["kit"]["main"]
    try:
        return dict(card, link=acts.reading(label, key, card)[0])
    except Refusal as e:
        why = str(e)
    fetch = crew.fetches_in(fleet, t["machine"], main)
    name = t["kit"]["name"]
    print(f"card {key}: its reading could not be opened on the tailnet: {why}; crew "
          + (f"fetches {name}'s main" if fetch else f"reads {name}'s main as its runner last fetched it")
          + " and tries once more", file=sys.stderr)
    try:
        if fetch and gather.has_origin(main):
            host_run(fleet, t["machine"], fetch_told(fleet, t["machine"], main, ORIGIN_FETCH), main)
    except Refusal as e:
        print(f"card {key}: {e}; the reading is tried again all the same", file=sys.stderr)
    fresh, fresh_why = None, None
    try:
        with READ.fresh():
            fresh = land_facts(fleet, label, plan, b, t)
    except Refusal as e:
        fresh_why = str(e)
    step, got = landing_retry(why, fresh, fresh_why)
    if step == "none":
        return None
    if step == "stand":
        why = got
    else:
        try:
            return dict(got, link=acts.reading(label, key, got)[0])
        except Refusal as e:
            card, why = got, str(e)
    print(f"card {key}: its reading could not be opened on the tailnet: {why}; crew card session {key} starts it", file=sys.stderr)
    return dict(card, unread=why)


def land_read(fleet, label, plan, b, t):
    """A started bolt's row on its kit's landings card, read on its host (t) as land_facts reads it, a fix in flight
    on it holding its row rather than keeping it off the card: (row, None), the row as landing_rows gives it, a box,
    or held for a fix or for sluice's refusal of its landing at its present head (rail-cards, Decision 7), a box saying
    what stopped its last landing at that head; (None, why) while it is no row. Refused when its kit can't be read
    (read.1)."""
    facts, why = land_facts(fleet, label, plan, b, t, fixes_hold=False)
    if why:
        return None, why
    return landing_rows([b.name()], {b.name(): facts}, {b.name(): facts["refusal"]} if facts.get("refusal") else {},
                        {b.name(): facts["stop"]} if facts.get("stop") else {})[0], None


def land_row(fleet, label, bolt, acts=None):
    """crew _land-row <label> <bolt>: a bolt's row on its kit's landings card, on the host its work runs on (bolt_at),
    where its reading runs (Decision 2): read as land_read reads it; a row that can land with its reading opened, or
    given again while it serves, twice if it must be, the second time on the landing read afresh (landing_opened); a
    held row, and a bolt that is no row, with its reading ended, as a card's close ends it (row_card_close). Its preview
    is no part of it: the raise on the drive's main machine reads it from the runner's report (landings_previews;
    Decision 7 of a-cards-preview-is-asked-of-the-runner). Returns the row, {bolt, box, why, facts}, its facts carrying
    its reading's link or why it could not be opened; or {bolt, why} while it is no row. Refused on any host but the
    bolt's, naming it, and when what it reads can't be read (read.1)."""
    acts = acts or CardActs(fleet)
    plan, b, t = land_held(fleet, label, bolt)
    if not b:
        return dict(bolt=bolt, why=f"{label}'s plan holds no bolt {bolt}")
    if not t:
        return dict(bolt=bolt, why=f"bolt {bolt} is not started")
    t["machine"] == acts.host() or fail(f"bolt {bolt}'s row is read on {t['machine']}, where the runner that took its work runs")
    row, why = land_read(fleet, label, plan, b, t)
    if row and row["box"]:
        facts = landing_opened(fleet, label, plan, b, t, row["facts"], acts)
        if facts:
            return dict(row, facts=facts)
        row, why = None, "read afresh, it no longer reads proven"
    said = acts.end(label, f"land/{bolt}")
    if said:
        print(said)
    return row or dict(bolt=bolt, why=why)


def land_row_cmd(fleet, a):
    """crew _land-row <label> <bolt> [--json]: land_row, what it does said on standard error, and the row printed, as
    JSON with --json, the one line on standard output, which the raise of the kit's card reads (CardActs.land_row)."""
    with contextlib.redirect_stdout(sys.stderr):
        row = land_row(fleet, a.label, a.bolt)
    print(json.dumps(row) if a.json else f"{a.bolt}: " + ("can land" if row.get("box") else row["why"]))


class Unposted(Exception):
    """A send's lands applied to a tip that already holds them (lands_change): the write writes nothing."""


def lands_posted(entries):
    """The lands crew recorded posting on the user's sends (crew-lands-each-bolt-through-flumes-base-place, Decision 4),
    from the run record's entries, oldest first: each bolt.submit or fix.merge marked Outcome asked with the land's
    Request, not refused, as {work, card, head, request}, its work the bolt's or the fix of main's it is On."""
    out = []
    for e in entries:
        if e.get("Act") not in ("bolt.submit", "fix.merge") or e.get("Refused") or not e.get("Request"):
            continue
        work = next((o for o in e.get("On") or [] if o.startswith(("bolt/", "fix/main/"))), None)
        if work:
            out.append(dict(work=work, card=e.get("Card"), head=e.get("Head"), request=e["Request"]))
    return out


def lands_sent(entries, key, owner, card=None, shown=(), ticked=()):
    """The sends that stand on a kit's landings card's rows (Decision 4), {a row's work: (the card whose send ticked it,
    the head it ticked)}: each bolt or fix an earlier card's close kept as its Heads (landings_sent), under the card
    closed, and each the answered card held now ticked (card, its rows as shown, card_heads, and the rows ticked),
    under that card; a fix of main's row named main--<name> is its fix/main/<kit>/<name>."""
    kit = key.split("/", 1)[-1]

    def work(b):
        return f"fix/main/{kit}/{b[len('main--'):]}" if b.startswith("main--") else f"bolt/{b}"
    out = {}
    for e in entries:
        if e.get("Act") == "card.close" and not e.get("Refused") and e.get("Key") == key and e.get("By") == owner:
            out.update({work(b): (e.get("Card"), h) for b, h, _ in card_heads(e.get("Heads"))})
    if card:
        out.update({work(b): (card, h) for b, h, _ in shown if b in (ticked or [])})
    return out


def lands_change(w, kit, rows, sent, reads, work=None):
    """The plan write that posts the lands a send makes due (crew-lands-each-bolt-through-flumes-base-place, Decision 4;
    rail-cards "The user's send on a kit's landings card posts one land for each row it lands"), applied to w at its tip:
    the lands due there (runner.lands_due over requests.rec and the run record as the tip holds them, so a replay finds
    those a concurrent raise posted), each a land request of its row's launch in the card's order, the fixes of main
    first, and an entry for each row, bolt.submit on bolt/<bolt> or fix.merge on fix/main/<kit>/<name>, naming the card
    whose send it carries, the head it ticked and the land's request, marked Outcome asked, the first the write's own act
    and the rest written with it (Write.also). Raises Unposted where none is due at the tip. Returns [(work, request,
    head)]."""
    due = runner.lands_due(rows, sent, requests_of(w).recs("Request"), reads, lands_posted(w.entries()), work)
    if not due:
        raise Unposted()
    heads = {r.get("work") or f"bolt/{r['bolt']}": (r.get("facts") or {}).get("head") or "" for r in rows}
    out = []
    for i, (wk, n) in enumerate(due):
        m = request(w, "land", wk, Of=n)
        act = "fix.merge" if wk.startswith("fix/main/") else "bolt.submit"
        fields = dict(Card=sent[wk][0], Head=heads[wk], Request=str(m), Outcome="asked")
        if i == 0:
            w.act, w.fields = act, dict(w.fields, **fields)
            w.on.append(wk)
        else:
            w.also.append((record.new_id(), act, [wk], fields))
        out.append((wk, m, heads[wk]))
    w.subject = f"plan({kit}): land {joined([row_name(wk) for wk, _, _ in out])} on the user's send"
    return out


def lands_post(fleet, label, kit, owner, rows, sent, reads, work=None):
    """The lands a send on a kit's landings card makes due, posted by one plan write in main-level ops's name, the
    card's owner (lands_change): [(work, request, head)] posted, [] where none is due, nothing written."""
    posted = []

    def change(w):
        posted[:] = lands_change(w, kit, rows, sent, reads, work)
        return []
    try:
        write(fleet, label, change, f"plan({kit}): land on the user's send", act="bolt.submit", by=owner)
    except Unposted:
        return []
    return posted


def fix_row(kit, f):
    """A fix of a kit's main as a row of its landings card (crew-lands-each-bolt-through-flumes-base-place, Decision 5;
    crew-rail "A delivered fix of main is a line of its kit's landings row, sent as a bolt's is"), from runner.main_fixes_waiting's f: its row's name
    main--<name> and its work fix/main/<kit>/<name>, a box while Flume's status names the head its place delivered,
    else held saying crew can't tell it (read.1), its facts as a landings row's, with the first line of its brief."""
    name, head = f"main--{f['name']}", f.get("head")
    facts = dict(bolt=name, kit=kit, fix=True, units=[], chores=[], batches={}, head=head or "", at=f.get("carried"), moved=0,
                 pr=None, preview=None, brief=(f["brief"].strip().splitlines() or [""])[0], host=f["host"], sent=f.get("sent"))
    work = f"fix/main/{kit}/{f['name']}"
    if not head:
        return dict(bolt=name, work=work, box=False, facts=facts,
                    why=f"crew can't tell its head: Flume's status of its place, as the runner on {f['host']} carried it, names none")
    return dict(bolt=name, work=work, box=True, facts=facts)


def kit_card_state(acts, label, key, owner, card, entries):
    """The kit's landings card ops holds (card), as landings_step reads it, with the bolts the user ticked on it:
    ({status, heads, taking}, ticked), status "answered" once the user answered it, else "waiting", heads its rows as
    its last post or change recorded them (card_heads), taking those it showed taking main first (heads_taking); (None,
    why) when Pending You could not be read or no longer finds it, so the raise changes nothing (read.1), but a lost
    card, recorded lost, reads as none held, for a new one to be posted, and so does one Pending You has ended by
    another hand (cards.ended), recorded closed as ended there with what the user answered and their send (close_kept),
    so the card posted after it has no row for a bolt that send still lands. A card read answered has the user's answer
    recorded, once, with the bolts they ticked at the heads it showed (answer_seen)."""
    try:
        with acts.bridge(owner, "Its landings card is not changed.") as py:
            got, words = py.answer("get_request", {"requestId": card, "name": owner})
    except Refusal as e:
        return None, str(e)
    if words is not None:
        if cards.lost(words, owner):
            card_lost(acts, label, owner, key, card, words)
            return {"status": None}, None
        return None, f"Pending You refused get_request: {words}"
    recorded = shown_heads(entries, card)
    heads, taking = card_heads(recorded), heads_taking(recorded)
    state = ended_close(acts, label, owner, key, card, got, entries)
    if state:  # ended in Pending You by another hand: recorded so, its answer and send kept, and none held (Decision 4)
        print(f"card {key}: {card} was {state} in Pending You already, and the raise posts as the bolts stand")
        return {"status": None}, None
    if got.get("status") == "answered":  # the user's answer recorded the first time crew reads it (Decision 1)
        answer_seen(acts, label, owner, key, card, got, entries, heads, offered_boxes(recorded))
    return {"status": "answered" if got.get("status") == "answered" else "waiting", "heads": heads,
            "taking": taking, "ticked": ticked_of(got, heads)}, None


def said_heads(entries, left=()):
    """The Heads of the forecasts and amendments the run record holds said (entries), which a landings card's raise
    says once each, one a conductor's wait said before counting as said: a forecast said while its bolt was left
    (Reached: left) counts only while the
    bolt is still left (left, its name among them), so the raise records it held once the user ticks it (main_told)."""
    return {e["Heads"] for e in entries if e.get("Act") in ("forecast", "amendment") and not e.get("Refused") and e.get("Heads")
            and (e.get("Reached") != "left" or next((o[5:] for o in e.get("On") or [] if o.startswith("bolt/")), None) in left)}


def left_said(bolt, main, paths):
    """The sentence a kit's landings card's change note says of a bolt the user left that a forecast first finds in
    conflict with main (rail-cards "A left row's first conflict with main changes the card in place once")."""
    return f"{bolt}, which you left, would take main first: forecast to conflict with main on {joined(list(paths))} at {main[:7]}"


def main_told(acts, label, rows, found, at, entries, left=()):
    """Each bolt the landings card's forecast found newly in conflict with main held on its row (rail-cards "A row
    forecast to conflict with main takes main first, recorded once and telling no one"): rows, {bolt: facts} of each whose forecast against main names
    files (found, {bolt: paths}), at main's revision (at); recorded on bolt/<bolt> with its Heads and Paths, once for
    the same bolt head and revision of main, whichever raise recorded it first, read from the drive's run record
    and this host's (entries, said_heads), as found while held (Reached: held), so its row takes main first at every
    raise at that head (main_conflict). Nobody is told and nothing is started: a fix taking main in is launched when
    sluice refuses the bolt's landing for the conflict (take_main_launch), or by hand. A bolt the user left (left) is
    recorded once as found while it is left (Reached: left), and said in the sentence returned for the card's change
    note (left_said); those sentences."""
    done, said = said_heads(entries, left), []
    for b, f in rows.items():
        heads = f"bolt/{b}@{f['head'][:7]} main@{at['main'][:7]}"
        if heads in done:
            continue
        acts.emit(label, "forecast", [f"bolt/{b}"], why=f"bolt({b}): forecast to conflict with main", Heads=heads,
                  Paths=" ".join(found[b]), Reached="left" if b in left else "held")
        done.add(heads)
        if b in left:
            said.append(left_said(b, at["main"], found[b]))
    return said


def raise_landings(fleet, label, kit, acts=None, note=None, dead=False):
    """crew _land-card <label> <kit>: a kit's landings card raised, changed, followed or closed (rail-cards, record 0031
    as amended 2026-10-23, Decisions 2 and 8), on the drive's main machine in main-level ops's name, refused
    elsewhere naming it: each of the plan's bolts of the kit a team holds asked for its row on its team's host
    (acts.land_row, land_row), a host that does not answer named and its rows left off, the rest raised (read.3); the
    card ops holds read first, its state in Pending You and the bolts the user ticked on it; the rows in the plan's
    order, but each that an earlier send still lands (landings_sent, rows_unsent), at the head sent or at one whose own
    work is the same (record 0031 as amended 2026-10-24), read once for every bolt sent or ticked whose head moved
    (acts.work, bolt_work), one whose work changed a row again; each that can land forecast against main and the rows
    above it (acts.forecast, forecast_rows); the bolts the user left (left_now) recorded as landing.left when they
    change, shown unticked on every card the raise posts, changes or follows with, each keeping its box though it
    conflicts with main and said once in the change note when a forecast finds it so (main_told, rail-cards "A bolt
    the user left stays left until they tick it"), each other found so recorded held, telling no one (main_told); each
    row taking main first beside one that can land kept on the card unticked, saying why (card_rows, rail-cards "A row
    taking main first stays on the card"), so its bolt taking main in and coming back changes the card in place; then
    what the card makes of them (landings_step):
    posted, changed in place with what changed, or the event's note first, followed when its form changed, left,
    withdrawn saying why, or closed with what landed, was held and was left, with how many rows can still land, a new
    card following it while any can,
    each card that asks for a bolt again saying first what changed of its work (work_said): in its opening when it
    follows the user's send (below), else ahead of its summary (built_saying); an answered
    card whose send still lands bolts while another reads proven since is closed saying so, the bolts it still lands
    kept as its close's Heads, and a new card follows it with the rest; one closed with a ticked bolt held whose send
    stands keeps it as its Heads, for it to land on that send. A card that follows the user's send says first what they sent and what changed since: what landed, was held and was
    left, the outcome, and that each bolt they left waits on it; or, posted after the kit's last card, what changed of
    each bolt asked again and the bolts that joined, moved or still wait since (landings_since). With
    dead, an older copy this host's sign-in can't reach standing, as the rail's sweep hands it, the card is posted
    saying first that it was lost (built_again). One raise of a kit's card at a time, under its lock (CardActs.raising),
    every read made in it, so two bolts closing at once close their card once, the second reading the first's close.
    The card's id, or None."""
    acts = acts or CardActs(fleet)
    machine = crew.drive_of(fleet, label)["machine"]
    machine == acts.host() or fail(f"{kit}'s landings card is raised on {machine}, where {label}-ops's cards are")
    acts.read_landings(label, kit)  # each outcome the runner reports recorded and acted on first, out of the card's lock
    with acts.raising(label, kit):
        return landings_raised(fleet, label, kit, acts, note, dead)


LANDINGS_READ = set()  # the kits whose landings this process is reading at a raise, so a close inside it raises no read again


def kit_landings_read(fleet, label, kit):
    """The landings of a kit's started bolts read at a raise of its landings card (landing_read), before the card's lock
    is taken (raise_landings), each bolt one crew posted a land of: an outcome the runner reports recorded and acted on,
    a landed bolt closed leaving its card to this raise (card False), so the card that follows reads it gone. A read
    refused said; a raise inside it reads none again."""
    if (label, kit) in LANDINGS_READ:
        return
    LANDINGS_READ.add((label, kit))
    try:
        plan = plan_of(fleet, label)
        if plan is not None:
            reap_judged(fleet, label, [dict(bolt=b.name()) for b in plan.bolts() if b.get("Repo") == kit and started(b)])
    except Refusal as e:
        print(f"crew read none of {kit}'s landings: {e}", file=sys.stderr)
    finally:
        LANDINGS_READ.discard((label, kit))


def landings_raised(fleet, label, kit, acts, note, dead):
    """raise_landings' reads and acts, made under the kit's card's lock."""
    plan = plan_of(fleet, label) or fail(f"{label}/main could not be read, so {kit}'s landings card is not raised")
    owner, key = f"{label}-ops", f"land/{kit}"
    got, unread, hosts = {}, set(), {}
    run = runner_facts(fleet, label)
    for b in plan.bolts():
        if b.get("Repo") != kit or not started(b):
            continue
        t, why = bolt_taken(fleet, label, b, run)
        if why:
            print(f"card {key}: crew can't tell where bolt {b.name()} runs ({why}), so its row is left off", file=sys.stderr)
            unread.add(b.name())
        if not t:  # a bolt no runner has taken work of yet has nothing merged to land
            continue
        hosts[b.name()] = t["machine"]
        row, why = acts.land_row(label, b.name(), t["machine"])
        if row is None:
            print(f"card {key}: {t['machine']} did not answer for bolt {b.name()} ({why}), so its row is left off", file=sys.stderr)
            unread.add(b.name())
        elif "box" in row:
            got[b.name()] = row
    # each fix of the kit's main whose code delivered and whose submission waits held is a row of the card, ahead of the
    # bolts, ticked and sent as a bolt's is (crew-lands-each-bolt-through-flumes-base-place, Decision 5)
    fixes = [fix_row(kit, f) for f in runner.main_fixes_waiting(*run) if f["kit"] == kit]
    entries, whole = acts.entries(label), acts.drive(label)
    card = cards.card_under(entries, key, owner)
    state, ticked = None, None
    if card:
        state, why = kit_card_state(acts, label, key, owner, card, entries)
        if state is None:
            print(f"card {key}: {card} is not changed, since where it stands can't be read: {why}", file=sys.stderr)
            return None
        if state["status"] is None:  # lost to its owner, or ended in Pending You, and recorded so: posted again
            card, state, entries = None, None, acts.entries(label)
        else:
            ticked = state.pop("ticked")
    rows = fixes + [got[b.name()] for b in plan.bolts() if b.name() in got]
    every = {r["bolt"]: r for r in rows}  # each row as read, those an earlier send lands among them (rows_unsent)
    shown = (state or {}).get("heads") or []
    # a bolt on a row of the card held is that card's to ask for; the rest an earlier send ticked are judged by it
    sent = {b: h for b, h in landings_sent(entries, key, owner).items() if b not in {s for s, _, _ in shown}}
    ticked_at = {b: h for b, h, _ in shown if b in (ticked or [])}
    at = {r["bolt"]: r["facts"]["head"] for r in rows}
    # The bolts the user left (left_now), recorded when they change: a row whose host did not answer is left as recorded
    # (read.1). This host's entries the branch does not hold yet come after the branch's.
    ids = {e["Id"] for e in whole if e.get("Id")}
    was, stops = left_marks(whole + [e for e in entries if not e.get("Id") or e["Id"] not in ids], key)
    left = dict(left_now(state, ticked, at, was, stops), **{b: h for b, h in was.items() if b in unread})
    if left != was:
        acts.emit(label, "landing.left", [cards.row_object(key, acts.kits(label))], by=owner, Key=key,
                  Heads=" ".join(f"{b.name()}@{left[b.name()]}" for b in plan.bolts() if b.name() in left))
    moves = {b: (h, at[b]) for b, h in list(sent.items()) + list(ticked_at.items())
             if b in at and not b.startswith("main--") and not (at[b].startswith(h) or h.startswith(at[b]))}
    work = acts.work(label, kit, moves) if moves else {}
    rows, landing, asked = rows_unsent(rows, sent, work)
    for b in landing:
        print(f"card {key}: {b} lands on the user's send of an earlier card, so it is no row of this one")
    for b, words in asked:
        print(f"card {key}: {words}; the user's send of an earlier card does not stand for it, so it is a row again")
    # Every row that can land is forecast against main first, and each forecast to conflict with it, by this forecast or
    # the run record's at its present head, takes main first; the rest are forecast among themselves (row_forecasts).
    recorded = {r["bolt"]: c for r in rows if r["box"] and not r.get("work") for c in [main_conflict(whole, r["bolt"], r["facts"]["head"])] if c}
    boxed = [r["bolt"] for r in rows if r["box"] and not r.get("work")]  # a fix of main is forecast against nothing
    forecast, unmade, onto = acts.forecast(label, kit, boxed, list(recorded)) if boxed else ({}, {}, None)
    if onto:
        acts.keep_main(label, kit, onto["main"])
    found = {b: p for b, fs in forecast.items() for w, p in fs if w == "main" and p}
    takes = dict(recorded, **{b: (onto["main"][:7], p) for b, p in found.items()})
    rows = [landing_rows([r["bolt"]], {r["bolt"]: r["facts"]}, {}, takes_main=takes, left=left)[0] if r["box"] and not r.get("work") else r
            for r in rows]
    # each conflict found is recorded once, telling no one, and a bolt the user left is said in the card's change note
    lefts = main_told(acts, label, {r["bolt"]: r["facts"] for r in rows if r["bolt"] in found}, found, onto, whole + entries, left)
    note = "; ".join(([note] if note else []) + lefts) or None
    boxed = [r["bolt"] for r in rows if r["box"]]
    for r in rows:
        if r["box"] and not r.get("work"):
            r["facts"] = dict(r["facts"], forecast=forecast.get(r["bolt"], []), forecast_why=unmade.get(r["bolt"]))
    # The user's send carried to the runner: one land of each row it lands at its head now, posted by one plan write
    # before the card is acted on, and said (lands_post; crew-lands-each-bolt-through-flumes-base-place, Decision 4).
    standing = lands_sent(entries, key, owner, card if (state or {}).get("status") == "answered" else None, shown, ticked)
    for wk, n, h in acts.post_lands(label, kit, owner, rows + [every[b] for b in landing if b in every], standing, run[1], work):
        print(f"card {key}: {row_name(wk)} is asked of the runner to land at "
              f"{h[:7]} (request {n}), on the user's send")
    landed = {next((o[5:] for o in e.get("On") or [] if o.startswith("bolt/")), None): e.get("Head") or ""
              for e in whole if e.get("Act") == "bolt.land" and not e.get("Refused")}
    in_plan = {b.name() for b in plan.bolts() if b.get("Repo") == kit} | {r["bolt"] for r in fixes}
    told = landings_previews(fleet, label, kit, rows, hosts, unread, run)
    step = landings_step(rows, state, ticked, in_plan, landed, note, work)
    try:
        t = kit_at(fleet, label, kit)
    except Refusal:
        t = None
    where = card_where(card_kit(fleet, t, kit, {"main": str(pathlib.Path.home()), "repo": kit}))
    # the card's rows: each that can land, and each taking main first beside them, which says why (card_rows)
    shows = card_rows(rows)
    on = {r["bolt"] for r in shows}
    facts = dict(kit=kit, rows=[r["facts"] if r["box"] else dict(r["facts"], taking=r["why"]) for r in shows],
                 held=[dict(bolt=r["bolt"], why=r["why"]) for r in rows if r["bolt"] not in on], ops=owner)
    # the rows its answer ticked or left; one it showed taking main first, unticked by crew, is none they left
    offered = [f"land:{b}" for b, _, _ in (state or {}).get("heads") or [] if b not in (state or {}).get("taking", set())]

    def unticked(cleared):  # the rows a card shows unticked: those the step names cleared, and every bolt the user left
        return [r["bolt"] for r in rows if r["box"] and (r["bolt"] in cleared or r["bolt"] in left)]
    said = [w for _, w in asked]  # what changed of each bolt an earlier send ticked that is a row again, said first
    if step[0] == "none":
        return None
    if step[0] == "leave":
        print(f"card {key}: {card} is left as it is" + (", the user having answered it" if state and state["status"] == "answered" else ""))
        return card
    if step[0] == "withdraw":
        return row_card_close(fleet, label, owner, key, reason=step[1], acts=acts, Rows="0")
    if step[0] == "post":
        facts.update(left=unticked(step[1]), follows=cards.follows_of("land", {"kit": kit}, entries, owner))
        earlier = card_heads(next((e.get("Heads") for e in reversed(entries) if e.get("Card") == facts["follows"] and not e.get("Refused")
                                   and e.get("Act") in ("card.post", "card.update") and e.get("Heads")), None)) if facts["follows"] else []
        # following the user's send, what changed of a bolt asked again opens the card with the rest (card_posted)
        build = cards.landings_card if facts["follows"] else built_saying(cards.landings_card, said)
        since = [f"{w}." for w in said] + landings_since(earlier, [r for r in rows if r["box"] and r["bolt"] not in dict(asked)])
        return told_kept(label, key, told, row_card_change(fleet, label, owner, built_again(build) if dead else build, facts,
                                                           "; ".join(said + [note or "Raised as the bolts stand"]), where, acts,
                                                           since=since if facts["follows"] else None))
    if step[0] == "change":
        _, change, kind_changed, cleared = step
        return told_kept(label, key, told, row_card_change(fleet, label, owner, cards.landings_card, dict(facts, left=unticked(cleared)),
                                                           "; ".join(said + [change]), where, acts, kind_changed))
    outcome = " ".join([f"{w}." for w in said] + [step[1]])
    if step[0] == "follow":  # closed with the bolts the send still lands as its Heads (landings_sent), the rest following
        _, _, cleared, landing = step
        rest, waits = [f for f in facts["rows"] if f["bolt"] not in dict(landing)], unticked(cleared)
        closed = row_card_close(fleet, label, owner, key, outcome=outcome, acts=acts, offered=offered, Rows=str(len(rest)),
                                Heads=" ".join(f"{b}@{h}" for b, h in landing))
        # the outcome, what changed of each bolt asked again among it (landings_step), opens the card that follows
        return closed and told_kept(label, key, told, row_card_change(
            fleet, label, owner, cards.landings_card, dict(facts, rows=rest, left=waits, follows=closed), outcome, where, acts,
            since=[outcome] + (left_waits(waits) if waits else [])))
    _, _, then, standing = step  # the bolts held whose send stands kept as its close's Heads (landings_sent)
    closed = row_card_close(fleet, label, owner, key, outcome=outcome, acts=acts, offered=offered, Rows=str(len(boxed)),
                            Heads=" ".join(f"{b}@{h}" for b, h in standing))  # its own, none when nothing stands (close_kept)
    if then is None or not boxed or not closed:  # a close refused leaves the card open, and nothing follows it yet
        return closed
    waits = unticked(then)
    return told_kept(label, key, told, row_card_change(
        fleet, label, owner, cards.landings_card,
        dict(facts, rows=[f for f in facts["rows"] if f["bolt"] not in dict(standing)], left=waits, follows=closed),
        outcome, where, acts, since=[outcome] + (left_waits(waits) if waits else [])))


def raise_landings_row(fleet, row, acts=None):
    """The rail's raise of a kit's landing row, land/<kit>, whose card is missing or lost (sweep_cards), or whose card
    this host's sign-in can't reach, handed that older copy as the row's dead: raise_landings of its kit; a row of a
    bolt's key, the form before a kit's card, is raised by none."""
    kind = land_key(row.get("key"), kits_read(fleet, row["label"]))
    return raise_landings(fleet, row["label"], kind[1], acts, dead=bool(row.get("dead"))) if kind and kind[0] == "kit" else None


def land_hand(fleet, label, kit, note=None):
    """The raise of a kit's landings card handed to the drive's main machine, where main-level ops's cards are
    (Decision 2, code.3): raise_landings there, as crew _land-card <label> <kit>, through crew.on_machine as the one
    asking, or in this process when this is that machine, note the event's change note; what it said passed on, and its
    failure said, refusing nothing of the event that handed it."""
    machine = crew.drive_of(fleet, label)["machine"]
    if machine == crew.this_host():
        try:
            raise_landings(fleet, label, kit, note=note)
        except Refusal as e:
            print(f"{kit}'s landings card is not raised: {e}", file=sys.stderr)
        return
    r = crew.on_machine(fleet, machine, crew.crew_argv(fleet, machine, "_land-card", label, kit, *(["--note", note] if note else [])))
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode:
        said = ((r.stderr or r.stdout).strip().splitlines() or [f"exit {r.returncode}"])[-1]
        print(f"{kit}'s landings card is not raised on {machine}: {said}", file=sys.stderr)


def land_card_cmd(fleet, a):
    """crew _land-card <label> <kit> [--note <words>]: raise_landings on the drive's main machine, handed there by
    the event that changed a bolt's row (land_hand). An older crew's --pane, a landing on the user's words in ops's
    pane, is taken and read as nothing, since no word in a pane lands a bolt (record 0056 point 5)."""
    raise_landings(fleet, a.label, a.kit, note=a.note)


def land_end(fleet, label, bolt):
    """A bolt's reading ended on this, its team's, host, with its row on its kit's landings card, held or gone, which no
    close of a card of the bolt's own ends (row_card_close): what it said, printed. Its preview is put away by the raise
    of its kit's landings card that follows (landings_previews)."""
    said = CardActs(fleet).end(label, f"land/{bolt}")
    if said:
        print(said)


def landings_previews(fleet, label, kit, rows, hosts, unread, run):
    """Each row of a kit's landings card that can land given its preview, from the runner's report alone (Decisions 5
    and 7 of a-cards-preview-is-asked-of-the-runner; rail-cards "A landing row carries what brings its bolt's preview
    up"), no file of the kit's read: first, in one plan write, the done of each standing ask of a bolt of the kit that no
    row that can land carries at its host and head (runner.previews_put_away), so a row held for a fix, gone, landed or
    dropped, or at a moved head, has its ask put away, a bolt whose row crew could not read (unread) keeping its own
    (read.1), and a write refused said, the next raise trying again; then each row that can land carries crew's ask of
    its head on its host as the runner reports it (runner.preview_report), or what brings it up, {branch: bolt/<bolt>,
    head, state: "ask"}, with released where that write put an ask of its bolt at another head away. rows, as the raise
    holds them, each given its preview in its facts; hosts, {bolt: the host whose runner took its work}; run, the
    drive's requests and runners (runner_facts). Returns what each row was told, {request: word}, for the raise
    to keep once it posts or changes the card (told_kept)."""
    requests, reads = run
    key = f"land/{kit}"
    standing = runner.previews_standing(requests, reads)
    asks = {k: r for k, r in standing.items() if (r.get("Work") or "").startswith("bolt/") and r.get("Repo") == kit}
    carried = {(hosts.get(r["bolt"]), kit, r["facts"]["head"]) for r in rows if r["box"]}
    gone = runner.previews_put_away(asks, carried, {f"bolt/{b}" for b in unread})
    released = {}
    if gone:
        things = joined(sorted({r.get("Work")[len("bolt/"):] for r in gone}))
        try:
            preview_written(fleet, label, key, things, gone, done=True, made=[], by=f"{label}-ops")
            released = {r.get("Work")[len("bolt/"):]: r.get("Revision") for r in gone}
            print(f"card {key}: put away " + "; ".join(f"{r.get('Work')[len('bolt/'):]}'s preview of {r.get('Revision')[:7]} on "
                                                       f"{r.get('Host')}" for r in gone))
        except Refusal as e:
            print(f"card {key}: the previews of {things} are not put away yet, the next raise trying again: {e}", file=sys.stderr)
    asked = runner.previews_asked(requests)
    gone_ids = {r.get("Request") for r in gone} if released else set()
    told = {}
    for r in rows:
        if not r["box"] or r.get("work"):  # a fix of main's row carries no preview: its facts' preview stays None (fix_row)
            continue
        head = r["facts"]["head"]
        ask = asked.get((hosts.get(r["bolt"]), kit, head))
        if ask is not None and ask.get("Request") not in gone_ids:
            p = runner.preview_report(reads, ask)
            told[ask.get("Request")] = runner.preview_word(p)
        else:
            was = released.get(r["bolt"])
            p = dict({"branch": f"bolt/{r['bolt']}", "head": head, "state": "ask"}, **({"released": was} if was and was != head else {}))
        r["facts"] = dict(r["facts"], preview=p)
    return told


def told_path(label):
    """Where the drive's main machine keeps what each card was last told of each preview it carries (Decision 8
    of a-cards-preview-is-asked-of-the-runner): beside the card folders and in none, as landings_main keeps a card's
    main, so no card's close or sweep removes it."""
    return CARDS / label / "previews.json"


def told_read(label):
    """What each card was last told of each preview it carries, {key: {request: word}}, kept on this host (told_path);
    a cache of what crew read (state.4), so one lost or unreadable reads as {}, which costs one more change of each
    card."""
    try:
        got = json.loads(told_path(label).read_text())
    except (OSError, ValueError):
        return {}
    return {k: {str(n): w for n, w in v.items() if isinstance(w, str)} for k, v in got.items() if isinstance(v, dict)} \
        if isinstance(got, dict) else {}


def told_keep(label, key, words):
    """What a card under key was told of each preview it carries, {request: word}, kept on this host for the next rail
    read to compare (previews_changed), written whole and atomically, as landing_word_keep writes, and only when it
    changes; a card that carries none has its entry removed. What can't be written is said, and costs one more
    change."""
    have = told_read(label)
    now = {str(n): w for n, w in words.items()}
    if have.get(key, {}) == now:
        return
    if now:
        have[key] = now
    else:
        have.pop(key, None)
    p = told_path(label)
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_name(f".{p.name}.{os.getpid()}")
        tmp.write_text(json.dumps(have, sort_keys=True))
        tmp.replace(p)
    except OSError as e:
        print(f"card {key}: crew could not keep what it told the card of its previews: {e.strerror or e}; the next rail "
              "read changes it once more", file=sys.stderr)


def told_kept(label, key, words, card):
    """A card's post or change (card, its id, None when none was made) passed back, with what it was told of each
    preview it carries kept once it was made (told_keep)."""
    if card:
        told_keep(label, key, words)
    return card


def landing_cards_closed(fleet, t, bolt, outcome):
    """At a bolt's close, on the host its work runs on, once the drive's plan no longer holds the bolt (plan.16):
    any landing card of the bolt's own main-level ops still holds closed with outcome, its reading ended (land_end);
    then the kit's landings card raised on the drive's main machine (land_hand), which closes it once every bolt
    the user ticked has landed or been held, naming where GitHub's main holds each, and puts away the bolt's preview
    (landings_previews). A plan that can't be read closes none, saying so (read.1)."""
    pl = plan_of(fleet, t["label"])
    if pl is None or pl.bolt(bolt):
        print(f"no landing card of bolt {bolt} is closed: " + (f"{t['label']}/main could not be read" if pl is None else
                                                                f"{t['label']}/main still holds the bolt"))
        return
    owner, (_, outcome, reason) = reading_owner(t["label"], f"land/{bolt}"), landing_act("landed", words=outcome)
    for key in landing_card_keys(cards.host_entries(record, t["label"], crew.this_host()), bolt, owner):
        row_card_close(fleet, t["label"], owner, key, outcome=outcome, reason=reason)
    land_end(fleet, t["label"], bolt)
    land_hand(fleet, t["label"], t["kit"]["name"])


def bolt_land(fleet, a, by=None, close_why=None, card=True):
    """crew bolt land <bolt>: a bolt out of the plan with its units and chores, its bolt.land recording the commit its
    kit's main holds for it (plan.14, plan.16). A started bolt closes only once its landing reads landed from the
    runner's report (runner.landing_of; crew-lands-each-bolt-through-flumes-base-place, Decision 7), at the commit
    Flume names, with its Age and Split from the run record (landing_spent), crew deleting no branch and removing no
    worktree, Flume tidying the base place and sluice ending bolt/<bolt>; refused, recording nothing, naming its landing's
    outcome while it reads otherwise, and for a bolt started before bolts were base places, which lands under the crew
    that started it (Decision 9). Its kit's landings card is then raised to close naming the commit and the fleet's
    timer (land_hand), and its readings and previews ended on the bolt's host (sweep_on), but with card False, as a
    raise's own read of the landing closes it (landing_read), leaving the card to that raise. A bolt never started, built
    outside crew, is read on the host and main checkout the drive's main-level host keeps of its kit, and lands the
    same way once main holds each of its units' changes and chores, on the user's word (roles.2), nothing merged. A read
    of its landing closes it with this code (landing_close), its bolt.land in the name of by, with close_why as its
    Why."""
    label, repo, tip, plan = locate(fleet, "Bolt", a.bolt, default_label(fleet, a))
    b = plan.bolt(a.bolt)
    units = [u.name() for u in plan.work_of(a.bolt)]
    if started(b):
        return started_land(fleet, label, plan, b, units, by, close_why, card)
    t = main_kit(fleet, label, b.get("Repo"))
    why = unheld_refusal(fleet, a.bolt, units, b.get("Repo"), t, label)
    not why or fail(why)
    # What main holds now, GitHub's after the command's one fetch (plan.18), read before which units landed; the
    # landing records it (plan.14).
    said = host_run(fleet, t["machine"], fetch_told(fleet, t["machine"], t["kit"]["main"], MAIN), t["kit"]["main"])
    ref, head, why = kit.main_now(said, t["kit"]["name"], t["machine"])
    not why or fail(why)
    h = survey(fleet, [(t, None)]).get(t["machine"]) or {"ok": False, "error": "it was not asked"}
    k = h["kits"].get(t["kit"]["main"]) if h["ok"] else None
    k = k if k and k.get("ok") else None
    stage_of = unheld_stages(k, h.get("error") or f"{t['machine']} did not read {t['kit']['main']}", Stages(fleet, plan, {}, label=label).of,
                             [u.name() for u in plan.work_of(a.bolt) if is_chore(u)])
    landed = land_refusal(a.bolt, units, stage_of, [], label, None, t["kit"]["name"]) is None
    entries = drive_entries(fleet, label) if landed else []
    outside = [u for u, *_ in due_changes(plan, entries, None) if u in units] if landed else []
    why = land_refusal(a.bolt, units, stage_of, outside, label, None, t["kit"]["name"])
    not why or fail(why)

    def change(w):
        land_pieces(w, fleet, label, a.bolt, units, f"bolt {a.bolt} landed on {t['kit']['name']}'s main at {head[:7]}")
        return [a.bolt]
    write(fleet, label, change, f"plan({a.bolt}): land the bolt", act="bolt.land", on=[f"bolt/{a.bolt}"],
          fields=dict(Repo=t["kit"]["name"], Head=head), by=by, why=close_why)
    print(f"{a.bolt} has landed at {t['kit']['name']}'s {head[:7]}; it was never started")


def land_pieces(w, fleet, label, bolt, units, words):
    """A landing's change to a write: the bolt and each of its units and chores out of the plan, refused when work was
    added since it was checked, and its landing asked of the roles that run as their kinds (landed_asks)."""
    w.bolt(bolt)
    late = [u for u in w.plan.work_of(bolt) if u.name() not in units]
    not late or fail(f"{kind_of(late[0])} {late[0].name()} was added to {bolt} since it was checked; it has not landed")
    for u in w.plan.work_of(bolt):
        w.plan.remove(u)
        w.on.append(f"{kind_of(u)}/{u.name()}")
    w.plan.remove(w.plan.bolt(bolt))
    landed_asks(w, fleet, label, bolt, words)


def landing_refused_said(bolt, l):
    """Why crew bolt land closes nothing of a started bolt whose landing does not read landed (Decision 7), naming its
    outcome as the runner's report gives it."""
    o = l.get("outcome")
    said = runner.landing_said(l) or {
        "none": "no land of it has been asked of the runner: it lands on the user's send of its row on its kit's landings card",
        "unlaunched": "its base place is not launched" + (f": {l['words']}" if l.get("words") else ""),
        "dropped": "its base place was dropped"}.get(o, o)
    return f"bolt {bolt} has not landed, so crew bolt land closes nothing of it: {said}"


def started_land(fleet, label, plan, b, units, by, close_why, card):
    """crew bolt land of a started bolt (bolt_land): its landing read from the runner's report alone, closed at Flume's
    commit once it reads landed, its bolt.submit outcome recorded in the same commit where no read has recorded it
    (landing_entry at the tip), the record Flume holds for the runner after it tidies the base place among them, read
    as any status (runner.landing_of, flume_facts); refused naming its outcome otherwise, recording nothing, and a bolt
    started before bolts were base places refused in runner.legacy_said's words, closed only by the crew that started
    it (bolt-teams "crew bolt land closes a started bolt only once its base place reads landed", "A bolt with no launch of its own lands under
    the crew that started it"). No landing commit on its kit's main is read for it (crew record 0056 point 4)."""
    bolt = b.name()
    requests, reads = runner_facts(fleet, label)
    launch = runner.launch_of(requests, f"bolt/{bolt}")
    launch is not None or fail(f"{runner.legacy_said(bolt)}, so crew bolt land closes nothing of it here")
    l = runner.landing_of(launch, runner.lands_of(requests, launch), reads)
    l["outcome"] == "landed" or fail(landing_refused_said(bolt, l))
    head, kit_name = l["commit"], (b.get("Repo") or launch.get("Repo") or "").split("/")[-1]
    entries = drive_entries(fleet, label)
    spent = landing_spent(entries, plan, b, label, kit_name, datetime.datetime.now(datetime.timezone.utc))

    def change(w):
        land_pieces(w, fleet, label, bolt, units, f"bolt {bolt} landed on {kit_name}'s main at {head[:7]}")
        fields = landing_entry(w.entries(), bolt, l)  # its outcome, where no read recorded it yet, in the same commit
        if fields:
            w.also.append((record.new_id(), "bolt.submit", [f"bolt/{bolt}"], outcome_fields(fields)))
        return [bolt]
    write(fleet, label, change, f"plan({bolt}): land the bolt", act="bolt.land", on=[f"bolt/{bolt}"],
          fields=dict(Repo=kit_name, Head=head, **spent), by=by, why=close_why)
    print(f"{bolt} has landed at {kit_name}'s {head[:7]}, as the runner reports it")
    if not card:
        return
    try:
        t = launched_at(fleet, label, bolt, b.get("Repo") or kit_name, (requests, reads))
    except Refusal as e:
        print(f"bolt {bolt}'s readings and previews are not ended: {e}", file=sys.stderr)
        t = None
    if t:
        sweep_on(fleet, t, f"bolt {bolt}", (bolt, landed_words(head, l.get("entry"))), units=units)
    else:
        land_hand(fleet, label, kit_name)


def landing_spent(entries, plan_, b, label, kit_name, now):
    """A started bolt's Age and Split for its bolt.land (plan.20), from the run record alone, as the views' bolt_time
    gives them (crew-lands-each-bolt-through-flumes-base-place, Decision 7): from its newest bolt.start, or an older
    crew's bolt.give, to now, no sluice history being read; {} when crew can't tell them, the landing going on."""
    tm = time_at(bolt_facts(entries, plan_, b.name(), label, None, kit_name), now)
    if "unknown" in tm:
        return {}
    return {"Age": str(tm["age"]), "Split": ", ".join(f"{h.replace('_', '-')} {tm['shares'][h]}" for h in HOLDERS)}

def pane_words(acts, words, refusal):
    """The transcript record the user's words in the caller's pane were read from, as the run record names it
    (session/<id>/<its uuid, or line-<its hash>>), read in the caller's own session transcript on this host (acts.heard);
    refused in refusal's words, given crew's verdict on them (submit_word_refusal, leave_word_refusal), when crew does
    not read them as the user's (signals.5, briefs.12)."""
    v, sid = acts.heard(words)
    why = refusal(v)
    not why or fail(why)
    return f"session/{sid}/{v.uuid or f'line-{v.line_hash()[:16]}'}"


def leave_word_refusal(bolt, v):
    """Why crew bolt leave records no stop of the bolt (main-level "A stop said in ops's pane is read as the user's
    words", "A stop crew cannot read as the user's words is refused"), or None, judging the words as words_refusal
    judges every word said in a pane, holding none of them (record.3). A decision of facts alone (code.7)."""
    return words_refusal(f"crew records no stop of bolt {bolt}", v, "stop a landing",
                         "the user stops a landing on its kit's landings card or in main-level ops's pane")


# What a bolt's tip carries of other bolts' work (plan.8, plan.19), for kit.carries_of and gather.carried_bolts, read in
# its kit's main checkout with one fetch of main and every bolt from origin, pruning nothing, since a bolt's branch
# GitHub deleted was in main and its line beyond main is empty: $3 the tip judged, $4 a branch it is judged beyond, or
# empty for the bolt's own landing, which is all crew judges on this line, since Flume merges a place into its bolt.
# READ with git's words when a fetch or a listing fails; else LANDING, yes for a landing; HOLDS, the commits the tip
# holds beyond main now (and beyond $4); OWN, the tip's first-parent commits beyond main; and a LINE for each bolt, its
# name and its first-parent commits beyond main, every bolt GitHub holds read there, and a bolt the host keeps with no
# copy on GitHub read in the host's refs, a ref another command removed while it was read left out, as gone. Read from
# the branches alone, never a commit's words. In the runner's clone crew fetches nothing (FETCH), and the branches are
# read as the runner last fetched them.
CARRIES = FETCH + r"""main=$1 bolt=$2 tip=$3 into=${4:-}
cd "$main" || exit 1
now=refs/heads/main
if git remote get-url origin >/dev/null 2>&1; then
  if ! err=$(origin_fetch '+refs/heads/main:refs/remotes/origin/main' '+refs/heads/bolt/*:refs/remotes/origin/bolt/*' 2>&1); then
    echo "READ=$(printf '%s' "$err" | tr '\n' ' ')"; exit 0
  fi
  now=refs/remotes/origin/main
fi
read_out() { echo "READ=git could not list $1: $(printf '%s' "$2" | tr '\n' ' ')"; exit 0; }
if [ -n "$into" ]; then h=$(git rev-list "$tip" "^$now" "^$into" 2>&1) || read_out "what $tip holds beyond $into" "$h"; echo LANDING=no
else h=$(git rev-list "$tip" "^$now" 2>&1) || read_out "what $tip holds" "$h"; echo LANDING=yes; fi
o=$(git rev-list --first-parent "$tip" "^$now" 2>&1) || read_out "$tip's own commits" "$o"
echo "HOLDS=$(printf '%s' "$h" | tr '\n' ' ')"; echo "OWN=$(printf '%s' "$o" | tr '\n' ' ')"
seen=" "
for r in $(git for-each-ref --format='%(refname)' refs/remotes/origin/bolt/) $(git for-each-ref --format='%(refname)' refs/heads/bolt/); do
  b=${r#refs/remotes/origin/bolt/}; b=${b#refs/heads/bolt/}
  case "$seen" in *" $b "*) continue ;; esac
  seen="$seen$b "
  if ! l=$(git rev-list --first-parent "$r" "^$now" 2>&1); then
    git rev-parse -q --verify "$r" >/dev/null || continue
    read_out "bolt/$b's own commits" "$l"
  fi
  echo "LINE $b $(printf '%s' "$l" | tr '\n' ' ')"
done
"""


def bolts_carried(fleet, t, bolt, tip, into=""):
    """What a bolt's tip carries of other bolts' work (gather.carried_bolts), read on the bolt's host after one fetch
    (CARRIES, kit.carries_of): {bolt: [its landings the tip holds]} beyond main that are not on the tip's own
    first-parent line, and beyond into when given. Refused, naming what could not be read, when git could not fetch or
    list it (read.1)."""
    holds, lines, why = kit.carries_of(host_run(fleet, t["machine"], fetch_told(fleet, t["machine"], t["kit"]["main"], CARRIES),
                                                 t["kit"]["main"], bolt, tip, into), bolt)
    not why or fail(f"crew can't tell whether {tip} carries another bolt's work: {why}")
    return gather.carried_bolts(holds, lines, bolt)


def take_main_launch(fleet, label, t, bolt, conflict):
    """A crossed bolt's landing that Flume refused for a conflict with main (conflict: main's revision, Flume's words and
    the land's request, landing_of) takes main in by the act that read the refusal (landing_read; Decision 10 of
    teams-cross-to-flume-as-their-bolts-land, plan.8, plan.21; crew-lands-each-bolt-through-flumes-base-place,
    Decision 7): one plan write appending the
    launch of its take-main fix (runner.take_main), recorded as fix.start, unless a fix of that name already stands, so
    a refusal read twice launches it once; nothing for a bolt given on today's path, whose conductor takes main in. What
    crew could not write is said on standard error, and the landing's outcome stands."""
    plan = plan_of(fleet, label)
    if plan is None or not crossed_bolt(plan, bolt):
        return
    name = runner.take_main_name(*conflict[:1], *conflict[2:3])
    on, seen = [f"fix/{bolt}/{name}", f"bolt/{bolt}"], {}
    if runner.launch_of(runner_facts(fleet, label)[0], on[0]) is not None:
        print(f"bolt {bolt} takes main first: {on[0]} stands already, taking main in")
        return

    def change(w):
        crossed_bolt(w.plan, bolt) or fail(f"bolt {bolt} is no longer given through Flume")
        launched = runner.take_main(w.plan, requests_of(w).recs("Request"), bolt, label, *conflict)
        launched or fail(f"{on[0]} stands already, taking main in")
        act, work, given = launched
        seen.update(n=request(w, act, work, **given), repo=given["Repo"])
        w.subject = f"plan({bolt}): fix {name}"
        return []
    try:
        write(fleet, label, change, f"plan({bolt}): fix {name}", act="fix.start", on=on)
    except Refusal as e:
        print(f"crew launched no take-main fix for bolt {bolt}: {e}", file=sys.stderr)
        return
    print(f"bolt {bolt} takes main first: fix {bolt}--{name} is launched in {seen['repo']} (request {seen['n']}) for the runner "
          "that keeps it, taking origin/main into the bolt, and the user's send standing for it, crew asks the runner to land "
          "it again once it reads proven at its new head")


def landing_pending(entries, bolt):
    """The bolt's landing a read is to record (Decision 2), from the run record's entries, oldest first: its last
    bolt.submit marked Outcome asked, a land crew posted on the user's send, unless an entry after it records that
    request's outcome; or, as an older crew wrote them, marked Outcome queued, unless an entry after it records that
    submission's outcome, a bolt.submit naming the same Submission with another Outcome, a stop an older crew recorded
    with no Submission leaving it to a later read (record.4); else None. A decision of facts alone (code.7)."""
    mine = [e for e in entries if e.get("Act") == "bolt.submit" and f"bolt/{bolt}" in (e.get("On") or [])]
    i = next((i for i in range(len(mine) - 1, -1, -1) if mine[i].get("Outcome") in ("queued", "asked")), None)
    if i is None:
        return None
    if mine[i].get("Outcome") == "asked":  # a land crew posted on the user's send, until the runner's report decides it
        n = mine[i].get("Request")
        return None if not n or any(e.get("Request") == n and e.get("Outcome") != "asked" for e in mine[i + 1:]) else mine[i]
    if not mine[i].get("Submission"):
        return None
    n = mine[i]["Submission"]
    return None if any(e.get("Submission") == n and e.get("Outcome") != "queued" for e in mine[i + 1:]) else mine[i]


def since_start(entries, bolt):
    """The run record's entries since the bolt's newest start, a bolt.start or the bolt.give an older crew wrote, oldest
    first, else all of them, a bolt's name being free again once it lands. A decision of facts alone (code.7)."""
    on = lambda e: f"bolt/{bolt}" in (e.get("On") or [])
    i = max((i for i, e in enumerate(entries) if e.get("Act") in ("bolt.start", "bolt.give") and on(e)), default=-1)
    return entries[i + 1:]


def landing_head(entries, bolt):
    """The newest head a landing of the bolt carried (bolt-teams "A bolt whose work is on its kit's main reads landed"),
    from the run record's entries since its newest start (since_start): {head, submission, request}, the head the
    newest bolt.submit of the bolt naming one carried, whatever its outcome, an older crew's queued or stopped and a
    land crew asked among them, with the Submission and Request of the landing still pending over the same entries
    (landing_pending), each None where none stands; None where no bolt.submit of it names a head. A decision of facts
    alone (code.7)."""
    mine = since_start(entries, bolt)
    last = next((e for e in reversed(mine) if e.get("Act") == "bolt.submit" and f"bolt/{bolt}" in (e.get("On") or [])
                 and e.get("Head")), None)
    if last is None:
        return None
    q = landing_pending(mine, bolt) or {}
    return {"head": last["Head"], "submission": q.get("Submission") or None, "request": q.get("Request") or None}


def landing_phase(entries, bolt):
    """Where the bolt's landing stands in the run record (plan.8; bolt-teams "A bolt's landing reads queued, rejected or landing again from the run record"),
    from the drive's entries, oldest first, each state its own: asked, {state, n, head}, a land crew posted on the
    user's send whose outcome is not recorded (landing_pending), n its request, with rejected, (the merge queue's entry
    or None, its head), where an earlier land of the bolt was refused; queued, {state, n, head}, while a submission an
    older crew recorded queued has no outcome recorded and no earlier one of it was refused, and again, the same with
    rejected as asked has it; rejected, {state, n, head, words}, once Flume's verdict refused its newest landing for the
    bolt's own content, a conflict or a failed check, as crew recorded it from the runner's report with the head its
    land carried (landing_entry), until a land is asked again, n the merge queue's entry or None where Flume named
    none, standing through a later entry that landed nothing at its head (sent_back); stopped, {state, n, head, words},
    once its last landing was recorded stopped at a head by the runner or Flume, nothing of the bolt's (stops); else
    None: never asked, landed, or refused naming no head. asked, queued and again hold the bolt's work
    (landing_hold); rejected and stopped hold none. A decision of facts alone (code.7)."""
    mine = [e for e in entries if e.get("Act") == "bolt.submit" and f"bolt/{bolt}" in (e.get("On") or [])]
    rejected = lambda e: bool(e.get("Refused") and e.get("Head"))
    q = landing_pending(entries, bolt)
    if q is not None and q.get("Outcome") == "asked":  # crew's land on the user's send, its outcome not read yet
        i = next(i for i, e in enumerate(mine) if e is q)
        before = next((e for e in reversed(mine[:i]) if rejected(e)), None)
        out = dict(state="asked", n=q["Request"], head=q.get("Head") or "")
        return dict(out, rejected=(before.get("Submission"), before["Head"])) if before else out
    if q is not None:
        i = next(i for i, e in enumerate(mine) if e is q)
        before = next((e for e in reversed(mine[:i]) if rejected(e)), None)
        out = dict(state="again" if before else "queued", n=q["Submission"], head=q.get("Head") or "")
        return dict(out, rejected=(before.get("Submission"), before["Head"])) if before else out
    back = sent_back(entries).get(bolt)  # standing through a submit at its head that submitted nothing
    if back:
        return dict(state="rejected", n=back["n"], head=back["head"], words=back["words"])
    stop = stops(entries).get(bolt)  # stopped at that head, nothing of the bolt's: its send spent, holding nothing
    if stop:
        return dict(state="stopped", n=None, head=stop[0], words=stop[1])
    return None


def landing_phases(entries):
    """Each bolt's landing as the run record holds it (landing_phase), for every bolt a bolt.submit names, from the
    drive's entries, oldest first: {bolt: phase} for those whose landing is queued, again or rejected."""
    named = {o[5:] for e in entries if e.get("Act") == "bolt.submit" for o in e.get("On") or [] if o.startswith("bolt/")}
    return {b: p for b in sorted(named) for p in [landing_phase(entries, b)] if p}


def rejected_said(n, head):
    """A landing sluice rejected, as a line names it: by its number, else by the head it was submitted at."""
    return f"#{n}" if n else f"its landing at {(head or '')[:7]}"


def phase_said(phase, head):
    """What a bolt's line says of its landing as the run record holds it (landing_phase), each state in words of its own
    (bolt-teams "The views say a queued landing and leave it out of the bolts that can land"), the number always named, since no view reads sluice's queue
    (crew record 0056 points 1 and 4): queued, `landing queued as #<n>`; again, `landing again as #<n>, after #<m> was
    rejected`; rejected, while the bolt's head now (head) is the one rejected, `landing #<m> rejected at <head>, open
    for work: <words>`, and nothing once a fix has moved it, the rejection holding nothing (held_at); else None. A
    decision of facts alone (code.7)."""
    if not phase:
        return None
    if phase["state"] == "asked":
        return f"landing asked, request {phase['n']}"
    if phase["state"] == "queued":
        return f"landing queued as #{phase['n']}"
    if phase["state"] == "again":
        return f"landing again as #{phase['n']}, after {rejected_said(*phase['rejected'])} was rejected"
    if phase["state"] == "stopped":
        return (f"landing stopped at {phase['head'][:7]}, nothing of the bolt's: {phase['words']}" if at_head(phase["head"], head)
                else None)
    if at_head(phase["head"], head):
        return (f"landing {'#' + str(phase['n']) + ' ' if phase['n'] else ''}rejected at {phase['head'][:7]}, open for work: "
                f"{phase['words']}")
    return None


def landing_line(landing, phase, head, bolt=None):
    """What a started bolt's head line says of its landing (crew-lands-each-bolt-through-flumes-base-place, Decision
    10), from the runner's report (landing, Stages.landing) and the run record (phase, landing_phase): asked with its
    request, nothing of a refusal before it (crew-board "Landing again"); submitted with the merge queue's entry, and
    after an earlier land was refused, that it lands again, naming both (bolt-teams "Landing again"); landed at its
    commit; refused, at the head its land was posted at, while that is the bolt's head now, in Flume's words with what
    comes next, the bolt open for work and ops's fix for a failed check, or that it takes main first for a conflict
    (runner.landing_said, given the bolt), whether or not the run record holds it yet, and nothing once a fix has moved
    the head, the refusal holding nothing; stopped at that head, in its words; unknown, why; a bolt started before bolts
    were base places, that it lands under the crew that started it; else the run record's words (phase_said); None for
    nothing to say. A decision of facts alone (code.7)."""
    o = (landing or {}).get("outcome")
    at = (phase or {}).get("head") or ""
    if o == "legacy":
        return landing["words"]
    if o == "submitted" and phase and phase.get("rejected") and landing.get("entry"):
        state = runner.landing_said(landing).split(f"#{landing['entry']} ", 1)[-1]
        return f"landing again as #{landing['entry']}, {state}, after {rejected_said(*phase['rejected'])} was refused"
    if o in ("asked", "submitted", "landed", "unknown"):
        return runner.landing_said(landing)
    if o == "stopped":
        return runner.landing_said(landing, head=at or head)
    if o == "refused":
        if at and head and not at_head(at, head):
            return None  # a fix has moved its head since: the refusal holds nothing (held_at)
        return runner.landing_said(landing, bolt or "<bolt>", at or head)
    # a landing fix live with nothing else to say, as a forecast's is (runner.fix_clause; crews-bolt-kind-names-its-landing-fix, Decision 6)
    return phase_said(phase, head) or (runner.fix_clause(landing) if landing else "") or None


def phase_at(w, bolt):
    """The bolt's landing as the run record holds it at the tip the write is applied to (landing_phase), with the merge
    queue's entry Flume names for a land asked, as the runners the write read report it (runner.landing_of), where they
    can be read, so a refusal of work joining it names that entry (bolt-teams "A fix while the landing is queued")."""
    phase = landing_phase(w.entries(), bolt)
    if phase and phase["state"] == "asked":
        try:
            requests = requests_of(w).recs("Request")
            launch = runner.launch_of(requests, f"bolt/{bolt}")
            l = runner.landing_of(launch, runner.lands_of(requests, launch), w.runners()) if launch is not None else {}
        except Refusal:
            l = {}
        if l.get("entry"):
            phase = dict(phase, entry=l["entry"])
    return phase


def landing_hold(phase, bolt, what):
    """Why work may not join a bolt whose landing is queued (plan.8; bolt-teams "Work into a bolt whose landing is queued is refused"),
    from the run record's state of its landing (landing_phase), or None: while it is queued or landing again, what
    would join it (what, `unit <u>`, `chore <c>` or `fix <bolt>--<f>`) is refused naming the landing, since sluice
    lands the head it was given and work merged into the bolt meanwhile would be left out of main's landing; once
    sluice has rejected it, or with no landing in flight, nothing is refused. A land asked names its request, and once
    Flume names the merge queue's entry (phase's entry, Reads.landing) that too, and the refusal before it where one was
    (bolt-teams "A fix while the landing is queued" and "Landing again"). A decision of facts alone (code.7)."""
    if not phase or phase["state"] not in ("queued", "again", "asked"):
        return None
    if phase["state"] == "asked":  # crew-lands-each-bolt-through-flumes-base-place, Decision 7
        landing = (f"is landing again as #{phase['entry']} (request {phase['n']})" if phase.get("entry") and phase.get("rejected")
                   else f"is landing again (request {phase['n']})" if phase.get("rejected")
                   else f"has its landing #{phase['entry']} in the merge queue (request {phase['n']})" if phase.get("entry")
                   else f"has its landing asked of the runner (request {phase['n']})")
        before = f", after {rejected_said(*phase['rejected'])} was refused" if phase.get("rejected") else ""
        return (f"bolt {bolt} {landing}{before}, so {what} does not join it until its outcome is read: Flume lands the "
                "bolt's branch as it stands, and work merged into it meanwhile would be left out of main; put it on another "
                "bolt, or into this one once its landing has been refused")
    landing = (f"is landing again as #{phase['n']}, after {rejected_said(*phase['rejected'])} was rejected"
               if phase["state"] == "again" else f"has its landing queued on main as #{phase['n']}")
    return (f"bolt {bolt} {landing}, so {what} does not join it until sluice decides: sluice lands the head it was given, "
            "and work merged into the bolt meanwhile would be left out of main; put it on another bolt, or into this one "
            "once sluice has rejected the landing")


def landing_entry(entries, bolt, l):
    """The bolt.submit entry crew records of a bolt's landing once the runner's report decides it (plan.21;
    crew-lands-each-bolt-through-flumes-base-place, Decision 6), from plain facts (code.7): entries, the drive's run
    record, oldest first; l, the landing as runner.landing_of reads it. For an outcome decided, landed, refused or
    stopped, its fields: Outcome landed or stopped, or the refusal's words as Refused, the land's Request and the Head
    its land carried, from the newest land crew posted of the bolt (lands_posted), the merge queue's entry as Submission
    where Flume names one, and the words of a stop as Why; None for one undecided, unknown or unlaunched, and for one
    the run record already holds at that request, so a read twice records once."""
    if l.get("outcome") not in ("landed", "refused", "stopped"):
        return None
    asked = next((p for p in reversed(lands_posted(entries)) if p["work"] == f"bolt/{bolt}"), None)
    n = str(l.get("request") or (asked or {}).get("request") or "")
    mine = [e for e in entries if e.get("Act") == "bolt.submit" and f"bolt/{bolt}" in (e.get("On") or [])
            and (e.get("Request") or "") == n and (e.get("Outcome") in ("landed", "stopped") or e.get("Refused"))]
    if mine:
        return None
    fields = dict(Request=n or None, Head=(asked or {}).get("head") or None, Submission=l.get("entry"))
    if l["outcome"] == "landed":
        return dict(fields, Outcome="landed", Why=f"bolt({bolt}): landed on main at {(l.get('commit') or '')[:7]}, as the runner reports it")
    if l["outcome"] == "stopped":
        return dict(fields, Outcome="stopped", Why=l.get("words") or "stopped, nothing of the bolt's")
    return dict(fields, Refused=runner.landing_said(l))


def landing_read(fleet, label, bolt, run=None, entries=None, card=True):
    """A started bolt's landing read from the runner's report (plan.21; crew-lands-each-bolt-through-flumes-base-place,
    Decisions 6 and 7), by whichever act of crew's reads the bolt first, on any host, the runners' branches being the
    drive's state (read.5): its base place's landing (runner.landing_of) from the drive's requests and runners
    (run, as runner_facts reads them, read when not given), and once it is decided, recorded once in main-level ops's
    name and acted on, each outcome by a write of its own (landing_record). A landing then closes the bolt
    (landing_close), with card False leaving its kit's card to the raise that read it. The read that records a refusal
    or a stop asks main-level ops where it runs as its kind, keyed by the land's
    request (unlanded_ask); a conflict launches the take-main fix on the bolt, once however often it is read
    (take_main_launch). Where the bolt's base place names a landing fix (runner.landing_way;
    crews-bolt-kind-names-its-landing-fix, Decision 4), a refusal whose way on is Flume's, its landing fix live, landed
    or due, launches nothing and asks nothing, and one whose way on is its caller's, past the bound or its fix dropped
    or not launched, asks ops in Flume's words (runner.caller_said) and launches nothing. Each record is decided at the tip its write is applied to, so two reads at once record once.
    Nothing is recorded for a landing undecided or one crew can't tell (read.1). (whether it reads landed, what is said
    of it), said too."""
    requests, reads = run or runner_facts(fleet, label)
    launch = runner.launch_of(requests, f"bolt/{bolt}")
    if launch is None:
        said = runner.legacy_said(bolt)
        print(said)
        return False, said
    l = runner.landing_of(launch, runner.lands_of(requests, launch), reads)
    entries = drive_entries(fleet, label) if entries is None else entries
    said = runner.landing_said(l) or runner.base_said(dict(l, stage=l["outcome"])) or f"bolt {bolt}'s landing is not asked yet"
    ops, kit_name = f"{label}-ops", (launch.get("Repo") or "").split("/")[-1]
    print(f"bolt/{bolt}: {said}", file=sys.stdout if l["outcome"] != "unknown" else sys.stderr)
    if l["outcome"] == "landed":
        pl = plan_of(fleet, label)
        if pl is not None and pl.bolt(bolt):
            landing_record(fleet, label, bolt, l, said, ops)
            landing_close(fleet, label, bolt, l, entries, card)
        return True, said
    by = (l.get("fix") or {}).get("by", "crew")  # whose a refusal's way on is (runner.landing_way)
    if l["outcome"] in ("refused", "stopped") and landing_record(fleet, label, bolt, l, said, ops) and (
            l["outcome"] == "stopped" or by in ("crew", "caller")):
        unlanded_ask(fleet, label, bolt, kit_name, landing_request(entries, bolt, l),
                     runner.caller_said(l, bolt) if l["outcome"] == "refused" and by == "caller" else said)
    if l["outcome"] == "refused" and l.get("why") == "conflict" and by == "crew":
        take_main_launch(fleet, label, None, bolt, (l.get("main") or "", l.get("words") or "", l.get("request")))
    return False, said


def landing_request(entries, bolt, l):
    """The request of the land a bolt's landing answers: the runner's report's, else the newest land crew posted of
    it (lands_posted), else None."""
    asked = next((p for p in reversed(lands_posted(entries)) if p["work"] == f"bolt/{bolt}"), None)
    return str(l.get("request") or (asked or {}).get("request") or "") or None


def outcome_fields(fields):
    """landing_entry's fields as a write records them: Refused as the entry's refusal and Why as its Why, each empty
    field left out."""
    out = {k: v for k, v in fields.items() if v and k not in ("Refused", "Why")}
    if fields.get("Refused"):
        out["refused"] = fields["Refused"]
    if fields.get("Why"):
        out["why"] = fields["Why"]
    return out


def landing_record(fleet, label, bolt, l, said, by):
    """A bolt's landing outcome recorded by one plan write in main-level ops's name (by), its bolt.submit entry
    decided at the tip the write is applied to (landing_entry over the run record there), so a read replayed on a
    tip holding it, or two reads at once, record it once (bolt-teams "Two reads at once"). Whether this write recorded
    it; one crew could not write is said, recording nothing (read.1)."""
    def change(w):
        fields = landing_entry(w.entries(), bolt, l)
        if not fields:
            raise Unposted()
        got = outcome_fields(fields)
        w.why = got.pop("why", None) or f"bolt({bolt}): {said}"
        refused = got.pop("refused", None)
        w.fields = dict(w.fields, **got, **({"refused": refused} if refused else {}))
        w.subject = f"plan({bolt}): its landing {'refused' if refused else got.get('Outcome')}, as the runner reports it"
        return []
    try:
        write(fleet, label, change, f"plan({bolt}): its landing, as the runner reports it", act="bolt.submit",
              on=[f"bolt/{bolt}"], by=by)
    except Unposted:
        return False
    except Refusal as e:
        print(f"crew could not record bolt {bolt}'s landing: {e}", file=sys.stderr)
        return False
    return True


def close_refused_new(entries, bolt, words):
    """Whether a close of the landed bolt crew refused in words is recorded (Decision 4, bolt-teams "Each read tries
    a refused close again and records only new words"), from the run record's entries,
    oldest first: when no bolt.land on the bolt refused since its last bolt.submit carries those words, the last
    carrying others or none being there. A decision of facts alone (code.7)."""
    on = lambda e: f"bolt/{bolt}" in (e.get("On") or [])
    i = max((i for i, e in enumerate(entries) if e.get("Act") == "bolt.submit" and on(e)), default=-1)
    last = next((e for e in reversed(entries[i + 1:]) if e.get("Act") == "bolt.land" and on(e) and e.get("Refused")), None)
    return not last or last["Refused"] != words


def closed_already(entries, bolt):
    """Whether the run record holds the bolt closed since its newest start: a bolt.land not refused after its newest
    bolt.start, or an older crew's bolt.give, so a close another read made is no refusal of this one's (bolt-teams "Two
    reads at once"). A decision of facts alone (code.7)."""
    on = lambda e: f"bolt/{bolt}" in (e.get("On") or []) and not e.get("Refused")
    i = max((i for i, e in enumerate(entries) if e.get("Act") in ("bolt.start", "bolt.give") and on(e)), default=-1)
    return any(e.get("Act") == "bolt.land" and on(e) for e in entries[i + 1:])


def landing_close(fleet, label, bolt, l, entries, card=True):
    """A landed bolt closed by a read of its landing (plan.21; Decision 7): crew bolt land's own code, with no word asked
    of whoever ran the act, since the user's word to land was their send and the read records the runner's report, its
    bolt.land in main-level ops's name at Flume's commit (l, landing_of's), its Why naming who read it; card False
    leaving its kit's landings card to the raise that read it. A close crew refuses is said on standard error every
    time, and recorded as a refused bolt.land in main-level ops's name only when its words are new since the landing
    (close_refused_new). Whether it closed."""
    ops = f"{label}-ops"
    closing = argparse.Namespace(cmd="bolt", sub="land", bolt=bolt, label=label)
    try:
        bolt_land(fleet, closing, by=ops, card=card,
                  close_why=f"plan({bolt}): land the bolt, landed at {(l.get('commit') or '')[:7]} as the runner reports it, read by {record.who()}")
        return True
    except Refusal as e:
        words = str(e)
        try:
            now = drive_entries(fleet, label)
        except Refusal:
            now = entries
        if closed_already(now, bolt):  # another read closed it meanwhile (bolt-teams "Two reads at once")
            print(f"bolt/{bolt} landed and is closed already")
            return True
        print(f"bolt/{bolt} landed and was not closed: {words}; crew's next read of the bolt closes it once that is mended",
              file=sys.stderr)
        if close_refused_new(now, bolt, words):
            record.emit(label, "bolt.land", [f"bolt/{bolt}"], refused=words, by=ops)
        return False


# What crew bolt submit and crew main fix --send say, refusing at once (crew-lands-each-bolt-through-flumes-base-place,
# Decisions 1 and 5): a landing is the user's send of its row on its kit's landings card, which crew carries to the
# runner as a land by its own act, so no command of an agent's lands anything.
def submit_refused(bolts=()):
    """What crew bolt submit says, refusing at once (bolt-teams "crew bolt submit lands nothing"), naming each bolt it
    was given, else a bolt: it lands on the user's send of its row on its kit's landings card, carried to the runner."""
    who = joined(list(bolts)) if bolts else "a bolt"
    return (f"crew bolt submit lands nothing: {who} {'land' if len(bolts) > 1 else 'lands'} on the user's send of "
            f"{'their rows' if len(bolts) > 1 else 'its row'} on {'their' if len(bolts) > 1 else 'its'} kit's landings card, "
            "which crew carries to the runner as a land")


def send_refused(kit, name):
    """What crew main fix <kit> <name> --send says, refusing at once (main-level "A fix of main sent by hand is
    refused, and nothing else submits it"): the fix lands on the user's send of its row, main--<name>, on its kit's landings card, land/<kit>."""
    return (f"crew main fix --send lands nothing: fix {name} of {kit}'s main lands on the user's send of its row, "
            f"main--{name}, on {kit}'s landings card, land/{kit}, which crew carries to the runner as a land")


SUBMIT_REFUSED = submit_refused()


def bolt_submit(fleet, a):
    """crew bolt submit [<bolt>...] [--excerpt "<words>"] [--label L]: kept as a word, so an agent whose brief predates
    crew's landing through the runner is told the way (crew-lands-each-bolt-through-flumes-base-place, Decision 1): run
    with any arguments, refused at once, before it reads anything, naming the bolts it was given (submit_refused); its
    usage still answers --help (code.11)."""
    fail(submit_refused(a.bolt or ()))


def bolt_leave(fleet, a):
    """crew bolt leave <bolt>... --excerpt "<the user's words>" [--label L]: main-level ops's record of the user's own
    words in its pane stopping the landing of bolts waiting on a kit's landings card (main-level "A stop said in ops's
    pane is read as the user's words", "A stop crew cannot read as the user's words is refused", "A stop is recorded
    holding none of the user's words", rail-cards "A bolt stopped in ops's pane is shown as left"): the words read first
    in the caller's own session transcript on this host (acts.heard), and
    nothing recorded unless crew reads them as the user's (pane_words, leave_word_refusal); refused too, recording
    nothing, for a bolt the plan does not hold, one not started and one that does not read proven (land_read), which
    have no landing to stop. Each bolt's stop recorded as a bolt.leave naming its head as its row reads it, the
    transcript record the words were read from and their length, none of the words (record.3); then each kit's landings
    card raised on the drive's main machine (land_hand), saying the bolts were stopped on the user's words, which
    shows them unticked as left until the user ticks them on a send or their head moves (left_now)."""
    bolts = list(a.bolt)
    label, _, _, plan = locate(fleet, "Bolt", bolts[0], default_label(fleet, a))
    CONTEXT["label"] = label
    held = {b: plan.bolt(b) or fail(f"{label}'s plan holds no bolt {b}, so it has no landing to stop") for b in bolts}
    teams = {b: bolt_at(fleet, label, held[b]) or fail(f"bolt {b} is not started, so it has no landing to stop") for b in bolts}
    words = a.excerpt or ""
    words.strip() or fail("crew bolt leave needs the user's words: --excerpt \"<their words, as they wrote them>\"")
    frm = [pane_words(CardActs(fleet), words, lambda v: leave_word_refusal(", ".join(bolts), v))]
    heads = {}
    for b in bolts:
        row, why = land_read(fleet, label, plan, held[b], teams[b])
        row or fail(f"bolt {b} does not read proven, so it has no landing to stop: {why}")
        heads[b] = row["facts"]["head"]
    kits = {}
    for b in bolts:
        record.emit(label, "bolt.leave", [f"bolt/{b}"], frm=frm, why=f"bolt({b}): stopped on the user's words in {record.who()}'s pane",
                    Head=heads[b], Chars=len(words))
        kits.setdefault(held[b].get("Repo") or teams[b]["kit"]["name"], []).append(b)
        print(f"bolt {b} is left at {heads[b][:7]} on the user's words in {record.who()}'s pane: no take-main fix starts for it "
              "until they tick it on its kit's landings card or you land it on their words")
    for kit_name, stopped in kits.items():
        land_hand(fleet, label, kit_name, note=f"{joined(stopped)} {'was' if len(stopped) == 1 else 'were'} stopped on your words "
                                               f"in {record.who()}'s pane")

# ---------------------------------------------------------------------------------------------------- units

def group_of(u):
    """Where a unit is, as an object: its bolt, or its kit's queue."""
    return f"bolt/{u.get('Bolt')}" if u.get("Bolt") else f"queue/{u.get('Repo')}"


def unit_stage(fleet, label, plan, name):
    u = plan.item(name)
    b = plan.bolt(u.get("Bolt")) if u.get("Bolt") else None
    return (stages_for(fleet, label, plan, [b]) if b else Stages(fleet, plan, {}, label=label)).of(name)


# Where a bolt lives, read in its kit's main checkout (BOLT_AT).
BOLT_LIVES = r"""cd "$1" || exit 1
bolt=$2 file=$3
""" + BOLT_AT


# Where a bolt lives (BOLT_LIVES), and AT_MAIN, the policy at the kit's main now as this host last fetched it, with no
# fetch (plan.18): origin/main for a kit with an origin, else its own main, base64, or - when it holds none.
BOLT_HOME = BOLT_LIVES + r"""now=refs/heads/main; if git remote get-url origin >/dev/null 2>&1; then now=refs/remotes/origin/main; fi
echo "AT_MAIN=$(pol "$(ref "$now")")"
"""


def bolt_local_said(bolt, lives, main_remote):
    """What a team's read says, once, of a bolt the team holds (plan.19, record 0032's amendment): that it is local
    until it lands, when it lives on its host only (lives None, kit.bolt_lives) while the policy at the kit's main now
    names a remote for its bolt branches (main_remote); else None, a bolt on GitHub, or every bolt local while main's
    policy names none. Nothing is run for it: sluice has no command that puts a local branch's tip on GitHub, and its
    landing's pull request puts it there."""
    if lives is None and main_remote:
        return (f"bolt/{bolt} is local until it lands: it was made before bolts were on GitHub, so its places are cut "
                "from the local branch, and its landing puts it on GitHub")
    return None


def bolts_local_said(fleet, t, plan):
    """The line a kit's read says of each bolt whose work runs on its host (t, bolts_on) that is local until it lands
    (bolt_local_said), read there in each bolt's kit (BOLT_HOME); a bolt whose home crew can't read says nothing."""
    out = []
    for b in bolts_on(fleet, t["label"], plan, t["machine"]):
        k = known_at(fleet, t["label"], b)
        if k is None:
            continue
        r = crew.on_machine(fleet, k["machine"], ["bash", "-c", BOLT_HOME, "crew", k["kit"]["main"], b.name(), kit.DECLARATION])
        try:
            lives, main_remote = kit.bolt_home(r.stdout, b.name()) if r.returncode == 0 else (None, None)
        except Refusal:
            continue
        said = bolt_local_said(b.name(), lives, main_remote)
        if said:
            out.append(said)
    return out


# ------------------------------------------------------------------------------------------ who writes what

# The commands that write the plan directly, and the one role each agent crew started may use them in.
PLAN_WRITES = {("bolt", "new"), ("bolt", "start"), ("bolt", "order"), ("bolt", "drop"), ("bolt", "land"), ("unit", "add"),
               ("unit", "split"), ("unit", "amend"), ("unit", "order"), ("unit", "after"), ("unit", "move"), ("unit", "drop"),
               ("chore", "add"), ("chore", "order"), ("chore", "after"), ("chore", "move"), ("chore", "drop"), ("kit", "rename")}


def role(fleet, name):
    """What an agent crew started is, from its name alone: (kind, its drive's label), or ("user", None) for no agent
    at all, or for the user's <user>@<host>, which a command run again on another host carries."""
    if not name or "@" in name:
        return "user", None
    for label in fleet["drives"]:
        for kind, n in (("planner", f"{label}-planner"), ("design", f"{label}-design"), ("main-ops", f"{label}-ops")):
            if name == n:
                return kind, label
        if name == f"{label}-operator" or name.startswith(f"{label}-operator-"):  # the latter, a host's before record 0035
            return "operator", label
    return "other", None


def planner_of(fleet, kind, of):
    return f"{of}-planner" if of in fleet["drives"] else "the drive's planner"


def may_write(fleet, key, a):
    """Who writes the plan directly. The user writes everything. The planner changes it only by a proposal; the design
    agent queues; the main level's ops lands bolts (roles.1). A chore's commands are written by the same hands as the unit's of the
    same name (plan.11). Any other plan write by an agent crew started is refused, naming the planner. A command that
    writes a request for a runner, crew answer and crew main fix, is its own row of the table (may_request), as crew
    fix is once it finds its bolt given through Flume (flume_fix). A role's run writes as its role (crew.caller)."""
    name = crew.caller(fleet)
    kind, of = role(fleet, name)
    if " ".join(k for k in key if k) in REQUESTERS:
        return may_request(fleet, " ".join(k for k in key if k))
    if key not in PLAN_WRITES or kind == "user":
        return
    cmd, as_unit = " ".join(key), ("unit", key[1]) if key[0] == "chore" else key
    if kind == "planner":
        fail(f"the planner changes the plan through a proposal: crew plan propose, not crew {cmd}")
    if key == ("bolt", "start"):  # the user's choice of what runs (Decision 14 of the-team-machinery-leaves)
        fail(f"{name} does not start a bolt: the user starts it, or approves {planner_of(fleet, kind, of)}'s proposal holding "
             f"crew bolt start; tell {planner_of(fleet, kind, of)}, who proposes it")
    if (kind == "design" and as_unit == ("unit", "add") and not a.bolt) or (kind == "main-ops" and key == ("bolt", "land")):
        return
    fail(f"{name} does not write the plan with crew {cmd}" + (" --bolt" if as_unit == ("unit", "add") and a.bolt else "")
         + f": tell {planner_of(fleet, kind, of)}, who proposes it")


# The commands that write a request for a runner beyond the plan writes the role table already lets their callers run
# (Decision 16 of teams-cross-to-flume-as-their-bolts-land, roles.1), each with the roles besides the user who may run
# it, the first the one to tell: crew answer, crew fix of a bolt given through Flume, crew main fix, its --send
# among it, which ops runs only on the user's word (roles.2), and crew card preview, a card's owner's on the user's
# words on the card (Decision 6 of a-cards-preview-is-asked-of-the-runner). crew role land is a role's run's alone, told by its place
# and never by a name a standing agent carries too (role_land, run_named; Decision 10 of roles-run-as-flume-kinds).
REQUESTERS = {"answer": ("planner", "design", "main-ops"), "fix": ("planner", "main-ops"), "main fix": ("main-ops",),
              "card preview": ("main-ops", "planner")}
ROLE_SAID = {"planner": "the planner", "design": "the design agent", "main-ops": "main-level ops"}


def may_request(fleet, what):
    """Who writes a request crew <what> appends (REQUESTERS; Decision 16 of teams-cross-to-flume-as-their-bolts-land):
    the user, and the roles the table names for it; any other agent crew started is refused, naming who runs it and
    the one of them to tell. A request's By names who ran it (plan.request). A role's run requests as its role
    (crew.caller)."""
    name = crew.caller(fleet)
    kind, of = role(fleet, name)
    if kind == "user" or kind in REQUESTERS[what]:
        return
    label, first = of, REQUESTERS[what][0]
    to = f"{label}-{'ops' if first == 'main-ops' else first}" if label in fleet["drives"] else f"the drive's {ROLE_SAID[first].removeprefix('the ')}"
    fail(f"{name} does not run crew {what}: " + ", ".join(ROLE_SAID[r] for r in REQUESTERS[what]) + f" and the user do; tell {to}")


# ----------------------------------------------------------------------------------- plan commands, as ops

class Op:
    """One plan command, split so a proposal can check it without writing and an approval can apply several in one
    commit. It is built against a plan, and building it runs its checks, those that read the kits included. It holds
    its change to a Write (which checks again on each replay and returns the bolts whose conductors hear the write),
    the subject and run-record entry of its write, what to prepare before the push with its undo (a unit's rebase),
    and what follows the push."""

    def __init__(self, label, change, subject, act, on=(), frm=(), body="", prepare=None, after=None, fields=None):
        self.label, self.change, self.subject, self.act, self.body = label, change, subject, act, body
        self.on, self.frm = list(on), list(frm)
        self.prepare, self.after = prepare, after
        self.added_on, self.added_frm = [], []
        self.fields = fields if fields is not None else {}  # its entry's own fields, which its change may fill at the tip it is applied to
        self.also_at = None  # inside an approval, where its entry goes among the write's further acts (apply_all)


class Reads:
    """How a plan command reads the kits: its units' stages, whether a change's name is free on a kit's main, and the
    first unit of a held bolt not yet merged. A command run directly or inside a proposal reads them; a proposal's
    card reads none (Drawn)."""
    w = None  # the write a command inside a proposal is applied to; a command run directly reads the branch's tip

    def stages(self, label, plan, bolts):
        return stages_for(self.fleet, label, plan, bolts)

    def stage(self, label, plan, name):
        return unit_stage(self.fleet, label, plan, name)

    def free(self, label, kit, names, kind="unit"):
        """Each name is free for a unit or chore (kind) of the kit: no change or chore its main holds by it (name_free),
        and no branch of Flume's standing where a launch of it would be made (branch_free)."""
        name_free(self.fleet, label, kit, names)
        branch_free(self.fleet, label, kit, names, kind)

    def first_open(self, label, plan, bolt):
        return first_open(self.fleet, label, plan, bolt)

    def landing(self, w, bolt):
        """The bolt's landing as the run record holds it at the tip the write is applied to (landing_phase), which work
        joining it is checked against (landing_hold), with the merge queue's entry Flume names for a land asked, as the
        runners the write read report it (runner.landing_of), where they can be read."""
        return phase_at(w, bolt)


class Direct(Reads):
    """What a command run directly sees: the plans of every drive, or of --label (or the agent's own)."""
    direct = True

    def __init__(self, fleet, a):
        self.fleet, self.label = fleet, default_label(fleet, a)

    def locate(self, kind, name, word=None):
        label, _, _, plan = locate(self.fleet, kind, name, self.label, word)
        return label, plan

    def kit(self, kit):
        return plan_for(self.fleet, kit, self.label)[0]

    def kits(self, label):
        """The drive's kits (drive_kits) as its branch holds them now."""
        return kits_read(self.fleet, label)


class Proposed(Reads):
    """What a command inside a proposal sees: the proposal's drive and number, in the plan as the commands before
    it in the proposal have left it."""
    direct = False

    def __init__(self, fleet, label, w, n):
        self.fleet, self.label, self.w, self.n = fleet, label, w, n

    def locate(self, kind, name, word=None):
        (self.w.plan.bolt(name) if kind == "Bolt" else self.w.plan.item(name)) or self.w.gone(kind, name, word)
        return self.label, self.w.plan

    def kit(self, kit):
        return plan_for(self.fleet, kit, self.label)[0]

    def kits(self, label):
        """The drive's kits (drive_kits) in the plan as the commands before this one leave it, with the landings
        its branch holds at the write's tip."""
        return kits_at(self.w.repo, self.w.tip, self.w.plan)


class Drawn(Proposed):
    """What a command inside a proposal sees when the proposal's card is drawn: the plan as the commands before it have
    left it, and no kit (plan.12). No stage is known, so nothing is refused for one; a change's name is checked only
    for its form; and work a held bolt needs goes ahead of the bolt's first unit, merged or not. The approval reads the
    kits and checks them all."""
    UNREAD = {"stage": "unread", "worktree": None}

    def stages(self, label, plan, bolts):
        return self

    def of(self, name):
        return dict(self.UNREAD)

    def stage(self, label, plan, name):
        return dict(self.UNREAD)

    def free(self, label, kit, names, kind="unit"):
        for n in names:
            crew.NAME.match(n) or fail(f"a unit's or chore's name is lowercase words with dashes, not {n}")

    def first_open(self, label, plan, bolt):
        return next((u.name() for u in plan.work_of(bolt)), None)

    def landing(self, w, bolt):
        return None


def first_open(fleet, label, plan, bolt):
    """The first unit or chore of a held bolt that has not merged into it: where work the bolt needs to land goes, ahead
    of what waits on it. None when every one has merged, or the bolt has none."""
    b = plan.bolt(bolt)
    st = stages_for(fleet, label, plan, [b])
    return next((u.name() for u in plan.work_of(bolt) if st.of(u.name())["stage"] not in ("merged", "landed")), None)


def unblocking(ctx, plan, label, a, into):
    """--unblocks <bolt>: the unit or chore is work a bolt a team holds needs before it can be proven or land. It goes
    into that bolt, ahead of what waits on it, never into the queue or another bolt. Returns what it goes ahead of."""
    into == a.unblocks or fail(f"{a.unit} unblocks bolt {a.unblocks}, so it goes into that bolt, ahead of what waits on it, "
                               f"not into {f'bolt {into}' if into else 'the queue'}")
    started(plan.bolt(a.unblocks)) or fail(f"{a.unit} unblocks bolt {a.unblocks}, which is not started, so nothing waits on "
                                           "it: --unblocks names a bolt in flight")
    return ctx.first_open(label, plan, a.unblocks)


def kind_refusal(kind, cmd, sub, name):
    """Why a unit or chore command may not act on a record of the plan's Unit set (plan.11), or None: a unit command
    names a chore, or a chore command a unit, said with its kind and the command that takes it; and a chore is never
    split or amended, its words changing by a proposal that drops it and adds it again."""
    if kind == cmd:
        return None
    if kind == "chore" and sub in ("split", "amend"):
        return (f"{name} is a chore, which is never " + ("split" if sub == "split" else "amended")
                + ": a chore's words change by a proposal that drops it and adds it again (crew chore drop, crew chore add)")
    return f"{name} is a {kind}, not a {cmd}: crew {kind} {sub} acts on it"


def the_work(ctx, a):
    """The plan holding the unit or chore a command names (a.unit), as (label, plan), refused when it is of the other
    kind than the command (kind_refusal)."""
    label, plan = ctx.locate("Unit", a.unit, a.cmd)
    why = kind_refusal(kind_of(plan.item(a.unit)), a.cmd, a.sub, a.unit)
    not why or fail(why)
    return label, plan


def called(a):
    """How a write's subject names the unit or chore a command acts on: a unit by its name, a chore as `chore <name>`."""
    return f"chore {a.unit}" if a.cmd == "chore" else a.unit


def op_bolt_new(ctx, a):
    label = ctx.kit(a.repo)
    crew.NAME.match(a.bolt) or fail(f"a bolt's name is lowercase words with dashes, not {a.bolt}")
    why = kit_named(a.bolt, ctx.kits(label), label)
    not why or fail(why)

    def change(w):
        w.plan.bolt(a.bolt) is None or fail(f"{label}/main already has bolt {a.bolt}")
        r = Rec("Bolt", [("Bolt", a.bolt), ("Repo", a.repo), ("Goal", a.goal)] + [("Source", x) for x in a.source])
        w.plan.insert(r, before=w.bolt(a.before) if a.before else None)
        return [a.bolt]
    return Op(label, change, f"plan({a.bolt}): add the bolt", "bolt.new", on=[f"bolt/{a.bolt}"])


def op_bolt_start(ctx, a):
    """crew bolt start <bolt>: the bolt's work started through Flume with no team (Decision 14 of
    the-team-machinery-leaves; crew-lands-each-bolt-through-flumes-base-place, Decision 3): in one plan write, the bolt
    marked Path: flume, the launch of its base place, of crew's kind crew/bolt on main (runner.bolt_launch), and then a
    launch of each of its units and chores on bolt/<bolt> (reach_places), each in its repository for the runner whose
    configuration names it to take, starting no agent, making no branch and reading no host (record 0056 point 2). A
    proposal may hold it, and the user runs it directly (roles.1, may_write). Refused, with the plan unchanged and
    nothing requested, while no runner answers for the drive (runner.runnerless), and for a bolt started already,
    but one whose own launch the runner refused, which it launches anew (runner.restart)."""
    label, plan = ctx.locate("Bolt", a.bolt)
    fleet, b = ctx.fleet, plan.bolt(a.bolt)
    seen = {}

    def change(w):
        s = w.bolt(a.bolt)
        why = runner.runnerless(w.label, list(w.runners()))
        not why or fail(why)
        if started(s):
            asked, why = runner.restart(w.plan, requests_of(w).recs("Request"), w.runners(), a.bolt, w.label)
            not why or fail(why)
        else:
            s.set("Path", "flume")
            asked = [runner.bolt_launch(w.plan, a.bolt, w.label)]
        for act, work, given in asked:
            n = request(w, act, work, **given)
            if act == "launch":
                seen["bolt"] = n
        seen["launched"] = reach_places(fleet, w, a.bolt)
        return [a.bolt]

    def after(repo, sha):
        print(launched_said(b.get("Repo"), a.bolt, seen.get("launched") or [], seen.get("bolt")))
    return Op(label, change, f"plan({a.bolt}): start the bolt", "bolt.start", on=[f"bolt/{a.bolt}"], after=after)


def op_bolt_order(ctx, a):
    label, _ = ctx.locate("Bolt", a.bolt)

    def change(w):
        b, bolts = w.bolt(a.bolt), w.plan.bolts()
        if a.first:
            w.plan.insert(b, before=bolts[0]) if bolts[0] is not b else None
        elif a.last:
            w.plan.insert(b, after=bolts[-1]) if bolts[-1] is not b else None
        else:
            o = w.bolt(a.before)
            o is not b or fail("a bolt can't go before itself")
            w.plan.insert(b, before=o)
        reprioritise(w)
        return [a.bolt]
    where = "first" if a.first else "last" if a.last else f"before {a.before}"
    return Op(label, change, f"plan({a.bolt}): order the bolt {where}", "bolt.order", on=[f"bolt/{a.bolt}"])


def op_bolt_drop(ctx, a):
    """crew bolt drop <bolt> <reason> [--requeue]: the bolt out of the plan with its units and chores, or with them
    queued (bolt-plan "A bolt is created and dropped through crew"); for a started bolt, the drop's own commit drops
    each launch of its work still standing and then its base place's (crew-lands-each-bolt-through-flumes-base-place,
    Decision 8). It asks nothing of any host: Flume tidies the base place and sluice ends its branch, and what its units
    recorded as made on this host is removed here (made_drop). A bolt started before bolts were base places has no base
    place to drop, and the drop says its branch stays, the user's (Decision 9)."""
    label, plan = ctx.locate("Bolt", a.bolt)
    seen = {}

    def change(w):
        b = w.bolt(a.bolt)
        through = crossed_bolt(w.plan, a.bolt)
        for u in w.plan.work_of(a.bolt):
            if a.requeue:
                u.drop("Bolt")
                u.drop("After")
                w.plan.place_last(u)
            else:
                w.plan.remove(u)
                w.on.append(f"{kind_of(u)}/{u.name()}")
        w.plan.remove(b)
        if through:  # every place it launched is dropped (Decision 7), its base place's last (Decision 8)
            reach_places(ctx.fleet, w, a.bolt)
            base = runner.launch_of(requests_of(w).recs("Request"), f"bolt/{a.bolt}")
            if base is not None:
                request(w, "drop", f"bolt/{a.bolt}", Of=base.get("Request"))
            seen["legacy"] = not any(r.get("Act") == "launch" and r.get("Work") == f"bolt/{a.bolt}"
                                     for r in requests_of(w).recs("Request"))
        return [a.bolt]

    gone = [] if a.requeue else [u.name() for u in plan.work_of(a.bolt)]

    def after(repo, sha):  # asks nothing of any host (bolt-plan "The drop's host does not answer"; Decision 8)
        dropped = made_drop(label, gone)
        if dropped:
            print(dropped)
        if seen.get("legacy"):
            print(legacy_drop_said(a.bolt))
    return Op(label, change, f"plan({a.bolt}): drop the bolt" + (", its units queued" if a.requeue else ""), "bolt.drop",
              on=[f"bolt/{a.bolt}"], body=a.reason, after=after)


def legacy_drop_said(bolt):
    """What the drop of a bolt started before bolts were base places says of its branch (bolt-teams "A drop of
    a bolt started before bolts were base places leaves its branch to the user", Decision 9)."""
    return (f"bolt/{bolt} stays: {bolt} was started before bolts were base places, so it has no base place and crew asks "
            "nothing for its branch, which is the user's to keep or delete")


def op_unit_add(ctx, a):
    """crew unit add, and crew chore add (a.cmd), whose record is marked Kind: chore (plan.11): the same flags, the same
    refusals and the same hands. Work added to a bolt whose landing the run record has queued, or landing again, with no
    outcome is refused naming the landing, as a move into it is (landing_hold, plan.8)."""
    k = a.cmd
    label = ctx.label
    if a.bolt:
        label, plan = ctx.locate("Bolt", a.bolt)
        kit = plan.bolt(a.bolt).get("Repo")
        a.repo in (None, kit) or fail(f"bolt {a.bolt} is in {kit}, not {a.repo}")
    else:
        a.repo or fail(f"a {k} goes in a bolt (--bolt) or in a repo's queue (--repo)")
        label = ctx.kit(a.repo)
        kit, plan = a.repo, None
    ahead = unblocking(ctx, plan, label, a, a.bolt) if getattr(a, "unblocks", None) else None
    ctx.free(label, kit, [a.unit], k)
    sources = list(a.source)
    if a.signal:
        a.signal = signal_id(ctx.fleet, label, a.signal, ctx.w)  # a short id is routed, and sourced, by its full one
        sources.insert(0, f"signals/{a.signal}")

    def change(w):
        had = w.plan.item(a.unit)
        had is None or fail(f"{label}/main already has {kind_of(had)} {a.unit}")
        if a.bolt:
            w.bolt(a.bolt)
            why = landing_hold(ctx.landing(w, a.bolt), a.bolt, f"{k} {a.unit}")
            not why or fail(why)
        if a.signal:  # its one move, route, in the same commit, checked again on each replay, its entry carried there
            move(ctx.fleet, label, w, a.signal, route_move(a.signal, f"{k}/{a.unit}"))
            w.also.append((None, "signal.move", [f"signals/{a.signal}", f"{k}/{a.unit}"],
                           {"why": f"signals({a.signal}): route to {k}/{a.unit}"}))
        repo = w.bolt(a.bolt).get("Repo") if a.bolt else a.repo
        r = Rec("Unit", [("Unit", a.unit), ("Repo", repo)] + ([("Bolt", a.bolt)] if a.bolt else []) + ([("Kind", "chore")] if k == "chore" else [])
                + [("Intent", a.intent)] + [("After", x) for x in a.after] + [("Source", x) for x in sources])
        before = a.before or ahead
        o = w.plan.item(before) if before else None
        if a.before:
            o = w.item(a.before)
            o.get("Bolt") == a.bolt and o.get("Repo") == repo or fail(f"{kind_of(o)} {a.before} is not in {a.bolt or 'the queue of ' + repo}")
        if o is not None:
            w.plan.insert(r, before=o)
        else:
            w.plan.place_last(r)
        if crossed_bolt(w.plan, a.bolt):  # launched as the give launches it (Decision 7)
            reach_places(ctx.fleet, w, a.bolt)
        return [a.bolt] if a.bolt else []

    def after(repo, sha):
        if a.signal:
            print(f"signal {a.signal} routed to {k}/{a.unit}, in the same commit")
    return Op(label, change, f"plan({a.bolt or 'queue'}): add {called(a)}", f"{k}.add",
              on=[f"{k}/{a.unit}", f"bolt/{a.bolt}" if a.bolt else f"queue/{kit}"], frm=[f"signals/{a.signal}"] if a.signal else [], after=after)


def op_unit_split(ctx, a):
    label, plan = the_work(ctx, a)
    s = ctx.stage(label, plan, a.unit)
    s["stage"] not in LATER or fail(f"unit {a.unit} is in {s['stage']}, so it is no longer split; add the remainder as a new unit instead (crew unit add)")
    s["stage"] != "unknown" or fail(f"cannot tell unit {a.unit}'s stage: {s.get('why')}")
    ctx.free(label, plan.unit(a.unit).get("Repo"), [n for n, _ in a.into])
    bolt = plan.unit(a.unit).get("Bolt")

    def change(w):
        u = w.of(a)
        if crossed_bolt(w.plan, u.get("Bolt")):
            why = runner.launched_refusal(requests_of(w).recs("Request"), runner.work_of(u), "split")
            not why or fail(why)
        u.set("Intent", a.intent)
        prev = u
        for n, intent in a.into:
            had = w.plan.item(n)
            had is None or fail(f"{label}/main already has {kind_of(had)} {n}")
            r = Rec("Unit", [("Unit", n), ("Repo", u.get("Repo"))] + ([("Bolt", u.get("Bolt"))] if u.get("Bolt") else [])
                    + [("Intent", intent)] + [("Source", x) for x in u.all("Source")])
            w.plan.insert(r, after=prev)
            prev = r
        if crossed_bolt(w.plan, u.get("Bolt")):  # a unit not launched yet, and what it was split into, launched
            reach_places(ctx.fleet, w, u.get("Bolt"))
        return [u.get("Bolt")] if u.get("Bolt") else []
    return Op(label, change, f"plan({bolt or 'queue'}): split {a.unit} into " + ", ".join(n for n, _ in a.into), "unit.split",
              on=[f"unit/{a.unit}"] + [f"unit/{n}" for n, _ in a.into], frm=[f"unit/{a.unit}"])


def op_unit_amend(ctx, a):
    """A unit's intent replaced. One of a started bolt reaches its place by the write's own requests (amend_place):
    one whose place is launched has a change written for the old intent, so its construct is run again with the
    amendment's words and it is marked amended, proposal/<n> inside an approval and intent when the user runs it
    (bolt-plan "A unit's intent is amended through crew, its construct run again"); one whose launch is held or
    unanswered has no place yet, and is launched anew carrying the amendment, unmarked. Merged work is not amended, and
    a chore never is (plan.11)."""
    label, plan = the_work(ctx, a)
    s = ctx.stage(label, plan, a.unit)
    s["stage"] not in ("merged", "landed") or fail(
        f"unit {a.unit} has " + ("merged into its bolt" if s["stage"] == "merged" else "landed on main")
        + ", so it is not amended: a defect in it is a fix, and new work is a new unit")
    s["stage"] != "unknown" or fail(f"cannot tell unit {a.unit}'s stage: {s.get('why')}")
    bolt = plan.unit(a.unit).get("Bolt")
    mark = f"proposal/{ctx.n}" if not ctx.direct else "intent"

    def change(w):
        u = w.of(a)
        u.set("Intent", a.intent)
        if crossed_bolt(w.plan, u.get("Bolt")) and amend_place(ctx.fleet, w, u, mark) == "retry":
            u.set("Amended", mark)
        return [bolt] if bolt else []
    return Op(label, change, f"plan({bolt or 'queue'}): amend {a.unit}", "unit.amend", on=[f"unit/{a.unit}"])


def amend_place(fleet, w, u, by):
    """An approved amendment of a unit of a bolt given through Flume, reaching its place as the write's own act
    (Decision 7 of teams-cross-to-flume-as-their-bolts-land, runner.amending), u already holding its new intent: once
    its place is launched, a retry of its construct with the amendment's words, as a construct run again on today's
    path is prompted (again_words), by the user or by proposal <n> with the planner's case; while its launch is held or
    unanswered, that launch dropped and the unit launched anew carrying the amendment (reach_places). Returns which,
    "retry" or "again". Refused when the runner's records can't tell which, or its place has merged."""
    requests, work = requests_of(w).recs("Request"), runner.work_of(u)
    launch = runner.launch_of(requests, work)
    n = runner.number(launch.get("Request")) if launch is not None else None
    reading, unread = runner.taken(w.runners(), n) if launch is not None else (None, None)
    answer, place = (reading["answers"].get(n), reading["places"].get(n)) if reading else (None, None)
    how, why = runner.amending(work, launch, answer, place, unread or True)
    not why or fail(why)
    if how == "again":
        reach_places(fleet, w, u.get("Bolt"), again={work})
        return how
    case = next((p.get("Case") for p in Plan(w.text("proposals.rec") or "").recs("Proposal")
                 if by == f"proposal/{p.get('Proposal')}"), None) if by.startswith("proposal/") else None
    request(w, "retry", work, Of=launch.get("Request"), Stage="construct", Words=runner.brief(u) + again_words(by, case))
    return "retry"


def op_unit_order(ctx, a):
    label, plan = the_work(ctx, a)
    u0, k = plan.item(a.unit), a.cmd

    def change(w):
        u = w.of(a)
        g = w.plan.group(u)
        if a.first:
            w.plan.insert(u, before=g[0]) if g[0] is not u else None
        elif a.last:
            w.plan.insert(u, after=g[-1]) if g[-1] is not u else None
        else:
            o = w.item(a.before)
            o is not u or fail(f"a {k} can't go before itself")
            o in g or fail(f"{kind_of(o)} {a.before} is not in {u.get('Bolt') or 'the queue'} with {a.unit}")
            w.plan.insert(u, before=o)
        return [u.get("Bolt")] if u.get("Bolt") else []
    where = "first" if a.first else "last" if a.last else f"before {a.before}"
    return Op(label, change, f"plan({u0.get('Bolt') or 'queue'}): order {called(a)} {where}", f"{k}.order",
              on=[f"{k}/{a.unit}", group_of(u0)])


def op_unit_after(ctx, a):
    label, plan = the_work(ctx, a)
    a.none or a.deps or fail("name the units or chores it comes after, or --none")
    u0, k = plan.item(a.unit), a.cmd

    def change(w):
        u = w.of(a)
        had = sorted(u.all("After"))
        if a.none:
            u.drop("After")
        for d in a.deps:
            w.item(d)
            d != a.unit or fail(f"a {k} can't come after itself")
            if d not in u.all("After"):
                u.add("After", d, after="Intent")
        if crossed_bolt(w.plan, u.get("Bolt")) and sorted(u.all("After")) != had:
            why = runner.launched_refusal(requests_of(w).recs("Request"), runner.work_of(u), f"put {what}")
            not why or fail(why)
            reach_places(ctx.fleet, w, u.get("Bolt"))
        return [u.get("Bolt")] if u.get("Bolt") else []
    what = "after nothing" if a.none else "after " + ", ".join(a.deps)
    return Op(label, change, f"plan({u0.get('Bolt') or 'queue'}): {called(a)} {what}", f"{k}.after",
              on=[f"{k}/{a.unit}", group_of(u0)])


def op_unit_move(ctx, a):
    label, plan = the_work(ctx, a)
    u, k = plan.item(a.unit), a.cmd
    src, to = u.get("Bolt"), None if a.bolt == "queue" else a.bolt
    to != src or fail(f"{k} {a.unit} is already in {src or 'the queue'}")
    if to:
        tb = plan.bolt(to) or fail(f"no bolt {to} in {label}/main of {state_of(ctx.fleet, label)[0]}")
        tb.get("Repo") == u.get("Repo") or fail(f"bolt {to} is in {tb.get('Repo')}; a {k} moves only between bolts of its own repo, {u.get('Repo')}")
    ahead = unblocking(ctx, plan, label, a, to) if getattr(a, "unblocks", None) else None
    s = ctx.stage(label, plan, a.unit)
    s["stage"] not in ("merged", "landed") or fail(f"{k} {a.unit} has merged into {src}, so it can't move")
    s["stage"] != "unknown" or s.get("place_unread") or fail(f"cannot tell {k} {a.unit}'s stage: {s.get('why')}")
    def change(w):
        u = w.of(a)
        u.get("Bolt") == src or fail(f"{k} {a.unit} moved to {u.get('Bolt') or 'the queue'} meanwhile")
        if crossed_bolt(w.plan, src):
            why = runner.launched_refusal(requests_of(w).recs("Request"), runner.work_of(u), f"moved to {to or 'the queue'}")
            not why or fail(why)
        u.drop("After")
        if to:
            w.bolt(to)
            why = landing_hold(ctx.landing(w, to), to, f"{k} {a.unit}")
            not why or fail(why)
            u.set("Bolt", to, after="Repo")
        else:
            u.drop("Bolt")
        o = w.plan.item(ahead) if ahead else None
        if o is not None and o is not u and o.get("Bolt") == to:
            w.plan.insert(u, before=o)
        else:
            w.plan.place_last(u)
        if crossed_bolt(w.plan, to):  # launched as the give launches it (Decision 7)
            reach_places(ctx.fleet, w, to)
        return [b for b in (src, to) if b]
    kit = u.get("Repo")
    return Op(label, change, f"plan({to or 'queue'}): move {called(a)} from {src or 'the queue'}", f"{k}.move",
              on=[f"{k}/{a.unit}", f"bolt/{to}" if to else f"queue/{kit}"], frm=[f"bolt/{src}" if src else f"queue/{kit}"])


def op_unit_drop(ctx, a):
    """A unit or chore removed from the plan, and from each After naming it. One of a started bolt has its place dropped
    by the write's own request (reach_places); Flume removes no branch holding work (flume 67), so a drop whose launch
    stood says, as it prints and on its entry (Note), that Flume keeps the place's branch and the name stays taken while
    it stands (runner.drop_kept_said), which a later add under the name is refused for (branch_free). crew removes no
    branch and no unit's place."""
    label, plan = the_work(ctx, a)
    k = a.cmd
    s = ctx.stage(label, plan, a.unit)
    s["stage"] not in ("merged", "landed") or fail(f"{k} {a.unit} has merged into its bolt, so it can't be dropped")
    # A stage unknown only for its place is not merged: the drop goes, and crew removes no place of it.
    s["stage"] != "unknown" or s.get("place_unread") or fail(f"cannot tell {k} {a.unit}'s stage: {s.get('why')}")
    u0 = plan.item(a.unit)
    bolt = u0.get("Bolt")
    fields = {}

    def change(w):
        u = w.of(a)
        for o in w.plan.group(u):
            if a.unit in o.all("After"):
                o.fields = [(n, v) for n, v in o.fields if not (n == "After" and v == a.unit)]
        w.plan.remove(u)
        fields.pop("Note", None)
        if crossed_bolt(w.plan, u.get("Bolt")):  # its place dropped, and each dependent's held launch made again without it
            if runner.launch_of(requests_of(w).recs("Request"), runner.work_of(u)) is not None:
                fields["Note"] = runner.drop_kept_said(k, a.unit, f"bolt/{u.get('Bolt')}")
            reach_places(ctx.fleet, w, u.get("Bolt"))
        return [bolt] if bolt else []

    def after(repo, sha):  # the kit's read where the bolt runs, which closes it once landed (plan.21); crew removes no unit's place
        t = known_at(ctx.fleet, label, plan.bolt(bolt)) if bolt else None
        if t:
            sweep_on(ctx.fleet, t, f"{k} {a.unit}")
        if s["worktree"]:
            print(f"its worktree stays at {s['worktree']}, on {k}/{a.unit}")
        if fields.get("Note"):
            print(fields["Note"])
    return Op(label, change, f"plan({bolt or 'queue'}): drop {called(a)}", f"{k}.drop", on=[f"{k}/{a.unit}", group_of(u0)],
              body=a.reason, after=after, fields=fields)


def op_kit_rename(ctx, a):
    """crew kit rename <old> <new> (a-repository-is-renamed-by-one-explicit-command; record 0060, plan.22): old renamed
    new, by its name or forge address, in one commit wherever a reader matches the repository on the drive's branch
    (rename_branch): the plan's decision-record sources, requests.rec and the run record's entries, and nothing else, no
    record moved, no request appended, nothing launched, retried or dropped. Its entry, kit.rename, names the repository
    by its new name (On: kit/<name>) and the one it had (From: kit/<old>), with Repo the new and Count every record
    renamed. Before the write reads the branch, the entries this host kept unpushed are pushed (record.reach), so they
    are renamed with the rest, a refused push refusing the rename. Refused, with nothing written, by rename_refusal at
    the tip it is applied to (plan.1): while old's work stands (rename_standing), the proposal applying it excepted, or
    any host still keeps old (rename_kept), each host with a runner branch of the drive read with its main-level
    host, by its runner's report or else what the teams file keeps there; and for a name no record holds. Run again, it
    renames what an earlier rename left. A proposal may hold it, and the user runs it directly (roles.1, may_write)."""
    label, fleet = ctx.kit(a.old), ctx.fleet
    host = crew.drive_of(fleet, label)["machine"]
    own = None if ctx.direct else str(ctx.n)
    fields = {}

    def prepare():  # returns no undo: a push of this host's own entries takes nothing back
        record.reach(label)

    def change(w):
        paths = [p for p in w.paths("runs/") if p.endswith(".rec")]
        seen = {}
        for text in w.texts(paths):
            for e in record.parse(text or ""):
                seen.setdefault(e["Id"], e)
        entries = sorted(seen.values(), key=lambda e: (e["At"], e["Id"]))
        reads = w.runners()
        stands, unread = rename_standing(a.old, w.plan, requests_of(w).recs("Request"), reads, entries,
                                         proposals(w).recs("Proposal"), own)
        # What the teams file keeps on a host (record 0064): read for the host it is written on and each a drive
        # runs on, and for no other, whose keeping the file does not give.
        here, machines = crew.this_host(), {p["machine"] for p in fleet["drives"].values()}
        filed = lambda h: [k["repo"] for k in crew.kept(fleet, h)] if h == here or h in machines else None
        hosts = {h: ((reads[h].get("why") or reads[h].get("repositories")) if h in reads else None, filed(h))
                 for h in sorted({host, *reads})}
        kept, unkept = rename_kept(a.old, hosts)
        bolts = [b.name() for b in w.plan.bolts()]
        why = rename_refusal(label, a.old, a.new, bolts, stands, unread, kept, unkept, None)
        not why or fail(why)
        n = rename_branch(w, a.old, a.new)
        why = rename_refusal(label, a.old, a.new, bolts, [], [], [], [], n)
        not why or fail(why)
        fields.update(Repo=a.new, Count=str(n))
        return []

    def after(repo, sha):
        print(f"{a.old} is {a.new} in {label}'s records: {cards.plural(int(fields.get('Count') or 0), 'record')} renamed")
    return Op(label, change, f"plan(kit): rename {a.old} {a.new}", "kit.rename", on=[f"kit/{a.new.split('/')[-1]}"],
              frm=[f"kit/{a.old}"], prepare=prepare, after=after, fields=fields)


# The commands a proposal may hold, each built the same way whether run directly or inside a proposal. A chore's five are
# a unit's, the kind read from the command (plan.11).
OPS = {
    ("bolt", "new"): op_bolt_new, ("bolt", "start"): op_bolt_start, ("bolt", "order"): op_bolt_order, ("bolt", "drop"): op_bolt_drop,
    ("unit", "add"): op_unit_add, ("unit", "split"): op_unit_split, ("unit", "amend"): op_unit_amend, ("unit", "order"): op_unit_order,
    ("unit", "after"): op_unit_after, ("unit", "move"): op_unit_move, ("unit", "drop"): op_unit_drop,
    ("chore", "add"): op_unit_add, ("chore", "order"): op_unit_order, ("chore", "after"): op_unit_after, ("chore", "move"): op_unit_move,
    ("chore", "drop"): op_unit_drop, ("kit", "rename"): op_kit_rename,
}


def direct(key):
    """A plan command run directly: built (its checks), prepared, written, and what follows done, as one write."""
    def run(fleet, a):
        op = OPS[key](Direct(fleet, a), a)
        undo = op.prepare() if op.prepare else None
        try:
            sha = write(fleet, op.label, op.change, op.subject, op.body, act=op.act, on=op.on, frm=op.frm, fields=op.fields)
        except Refusal:
            if undo:
                undo()
            raise
        if op.after:
            op.after(state_of(fleet, op.label)[0], sha)
    return run


# -------------------------------------------------------------------------------------------------- asks

ASKS = """\
# The asks of the drive's main-level roles that run as their kinds, and the turns their runs took them in
# (record 0047 move 6). An ask names a role, whose next run takes it at its start, crew role start, and answers it at
# its end, crew role end. Written only through crew. An ask is never removed, and its number is never reused.

%rec: Ask
%doc: One ask of a role: who or what asks (From), what kind of ask it is (What), the record it names (Names), the key it is written once by (Key), its words and when.
%key: Id
%type: Id int
%type: Role enum design planner reviewer ops operator
%type: What enum tell send capture landed card open batch delivered
%type: At date
%mandatory: Id Role From What At
%allowed: Id Role From What Names Key Words At
%unique: Role From What Names Key Words At

%rec: Turn
%doc: A run of a role taking what was pending for it (Took: ask/<id>, place/<request>@<since>, landed/<request>), from its start (Began) to its end (Ended, with what it Said it did), or Superseded by the turn that took its asks again.
%key: Turn
%type: Turn,Superseded int
%type: Role enum design planner reviewer ops operator
%type: Began,Ended date
%mandatory: Turn Role Run Place Host Began
%allowed: Turn Role Run Place Host Took Began Ended Said Superseded
%unique: Role Run Place Host Began Ended Said Superseded
"""
ROLES = """\
# The runs of the drive's main-level roles that run as their kinds: one record for each, the launch the host's
# runner makes while anything is pending for the role (asks.rec). Written only through crew, to match the teams file,
# at crew main up and with an ask whose role's record is missing or differs.

%rec: Role
%doc: A role's run: the place <Kind>--<Name> in Repository on Host, launched from crew's kinds in Stream at Priority for Intent, with Model and Effort.
%key: Role
%type: Role enum design planner reviewer ops operator
%type: Priority int
%type: Effort enum low medium high xhigh max
%mandatory: Role Address Run Host Repository Kinds Kind Name Stream Priority Intent Model Effort
%allowed: Role Address Run Host Repository Kinds Kind Name Stream Priority Intent Model Effort
%unique: Role Address Run Host Repository Kinds Kind Name Stream Priority Intent Model Effort
"""


class AskHeld(Exception):
    """An ask written alone whose key asks.rec holds at the tip the write was applied to: nothing is committed."""


def rec_file(w, path, header):
    """One of crew's recutils files on the drive as the write has it, its record descriptors in step with crew's
    (in_step), or a new one when the branch has none yet."""
    pl = Plan(w.text(path) or header)
    in_step(pl, header)
    return pl


def ask_rec(w, fleet, label, role, what, frm, names=None, key=None, words=None):
    """An ask of the drive's role appended to asks.rec in the write w (design Decision 4), and the role's record
    written to roles.rec where it is missing or differs (roles_lines), so it stands before the runner can want the
    role: the ask's record, or None when asks.rec at the tip the write is applied to holds an ask with its key, which
    writes nothing (role-runs "An ask with a key is written once"), on the tip first tried and on any a refused push is
    applied again to (plan.1, state.1). frm, an agent's name, <user>@<host> or crew; names, the record it names."""
    pl = rec_file(w, "asks.rec", ASKS)
    held, _ = asks.parse(pl.text())
    if asks.keyed(held, key, role):
        return None
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec = Rec("Ask", [("Id", str(asks.next_id(held))), ("Role", role), ("From", frm), ("What", what)]
              + [(f, v) for f, v in (("Names", names), ("Key", key), ("Words", words)) if v] + [("At", at)])
    pl.insert(rec)
    w.replace("asks.rec", pl.text())
    roles_lines(w, fleet, label, [role])
    return rec


def ask_lines(w, fleet, label, role, what, frm, names=None, key=None, words=None):
    """An ask written in the commit of the act that makes it, the write w (role-runs "An ask is written with the act that
    makes it"): ask_rec, its run-record entry's id made ahead, so write names it in the commit beside the act's own and
    emits it once pushed (plan.2). Returns the ask's record, or None when its key was held, which write says."""
    rec = ask_rec(w, fleet, label, role, what, frm, names, key, words)
    if rec is None:
        w.held.append((f"{label}-{role}", key))
        return None
    w.asked.append((record.new_id(), rec))
    return rec


def ask_write(fleet, label, role, what, frm, names=None, key=None, words=None):
    """An ask of the role in a commit of its own, where the act that makes it writes nothing to the drive's branch:
    its own write, its entry the ask's; or nothing, said, when asks.rec holds an ask with its key at the tip the write is
    applied to (ask_rec). Returns the commit, or None when nothing was written."""
    run, e = f"{label}-{role}", record.ask_entry(f"{label}-{role}", what, names, words)

    def change(w):
        if ask_rec(w, fleet, label, role, what, frm, names, key, words) is None:
            raise AskHeld()
        return []
    try:
        return write(fleet, label, change, f"ask({run}): {what} from {frm}", act=e["act"], on=e["on"], why=e["why"], fields={"Chars": e["Chars"]})
    except AskHeld:
        print(f"{label}/main: {run} is already asked by {key}; nothing written")
        return None


def capture_asks(w, fleet, label, ids):
    """A capture landed through crew, crew signal's or crew signal land's, asks the drive's design agent where it
    runs as its kind (design Decision 5, role-runs "A capture and a bolt's landing are asks"): one `capture` ask per signal, ids,
    from whoever recorded it, naming the signal and keyed by its id, in the capture's commit, the write w. A design
    agent that stands is asked nothing: its curation runs at its start and on the user's word, as today (signals.7)."""
    if crew.role_runs(fleet, label, "design") == crew.RUNS_STANDING:
        return
    for sig in ids:
        ask_lines(w, fleet, label, "design", "capture", agent(), names=f"signals/{sig}", key=f"signal/{sig}")


def landed_asks(w, fleet, label, bolt, words):
    """A bolt's landing, as crew's read of it records it (bolt_land, whichever act closes it), asks the drive's
    planner and design agent where each runs as its kind (design Decisions 5 and 12, role-runs "A capture and a bolt's
    landing are asks"): a `landed` ask from crew naming the bolt, keyed landed/<bolt>, the landing in words, in the landing's
    own commit, the write w. A role that stands is asked nothing."""
    for role in ("planner", "design"):
        if crew.role_runs(fleet, label, role) == crew.RUNS_ON_DEMAND:
            ask_lines(w, fleet, label, role, "landed", "crew", names=f"bolt/{bolt}", key=f"landed/{bolt}", words=words)


def unlanded_ask(fleet, label, bolt, kit_name, n, words):
    """A landing the runner's report has refused or stopped, recorded by the read that found it (landing_read,
    landing_record), asks the drive's main-level ops where it runs as its kind, in a commit of its own (role-runs
    "A land the runner refused"; crew-lands-each-bolt-through-flumes-base-place, Decision 6): a `landed` ask from crew
    naming the bolt with Flume's or the runner's words, keyed by the land's request, request/<kit>/<n>, so its outcome
    read twice asks once; one with no request crew can name is keyed by nothing. An ask crew could not write is said,
    the read going on (read.1)."""
    if crew.role_runs(fleet, label, "ops") == crew.RUNS_STANDING:
        return
    try:
        ask_write(fleet, label, "ops", "landed", "crew", names=f"bolt/{bolt}", key=f"request/{kit_name}/{n}" if n else None, words=words)
    except Refusal as e:
        print(f"could not ask {label}-ops that bolt/{bolt} did not land: {e}", file=sys.stderr)


# A card's request id and version as Pending You's notice gives them, `pendingyou watch`'s PENDINGYOU_REQUEST_ID and
# PENDINGYOU_VERSION (pendingyou 0.39.0, dist/watch.js, read 2026-10-31), and what each of its events says of the card,
# PENDINGYOU_EVENT (watch.js eventOf), as a card ask's words.
REQUEST = re.compile(r"req_[A-Za-z0-9-]+")
CARD_EVENTS = {"answer_ready": "the user answered it", "message_ready": "a message came on it",
               "fallback_due": "its fallback came due", "delegated_ready": "another of the user's assistants handed it on"}


def card_ask(fleet, name, request, version, event):
    """The ask a change on a card makes, as Pending You's notice names it to the host's follower (design Decision 5,
    role-runs "A card's answer, an opening and a batch are asks"): a `card` ask of the role whose run the card's asker,
    name, is, naming card/<request>, keyed card/<request>/<version> so the change is asked once and a later one again,
    its words what the notice's event says; None for a card in any other name, a standing agent's, a unit's or the
    user's own, which stays the wake mod's. Nothing else of the card is read: the run reads it in its own name at its
    start (Decision 7). A request id or version not of Pending You's form is refused (read.2). A decision of plain
    facts (code.7)."""
    REQUEST.fullmatch(request or "") or fail(f"Pending You's notice named no card crew can read: request {request!r}")
    (version or "").isdigit() or fail(f"Pending You's notice named card {request} at no version crew can read: {version!r}")
    run = crew.kind_role_of(fleet, name) if isinstance(name, str) else None
    if run is None:
        return None
    label, role = run
    return dict(label=label, role=role, names=f"card/{request}", key=f"card/{request}/{version}",
                words=CARD_EVENTS.get(event) or f"Pending You's notice named it {event or 'with no event'}")


def card_answered(fleet, a):
    """crew _answered: what Pending You's notice, `pendingyou watch -- crew _answered`, which the host's follower runs
    while a role here runs as its kind (board.answers_watched), runs for each change on a card of the host's sign-in:
    the card's request id, version and event from its environment and its asker's name, sessionLabel, from the card on
    standard input, and nothing else of it; a change on a card in a run's name is a `card` ask of the role, written
    alone from crew (card_ask, ask_write), and any other writes nothing. A notice crew can't read is refused, so the
    watch hands it again; one naming no asker writes nothing, said."""
    request, version = os.environ.get("PENDINGYOU_REQUEST_ID"), os.environ.get("PENDINGYOU_VERSION")
    request or fail("crew _answered runs from Pending You's notice, `pendingyou watch -- crew _answered`, which names the card "
                    "in PENDINGYOU_REQUEST_ID and PENDINGYOU_VERSION; neither is set")
    try:
        card = json.loads(sys.stdin.read() or "null")
    except ValueError:
        card = None
    name = card.get("sessionLabel") if isinstance(card, dict) else None
    if not isinstance(name, str) or not name:
        print(f"card {request}: Pending You's notice names no asker, so no role is asked")
        return
    ask = card_ask(fleet, name, request, version, os.environ.get("PENDINGYOU_EVENT"))
    if ask is not None:
        ask_write(fleet, ask["label"], ask["role"], "card", "crew", names=ask["names"], key=ask["key"], words=ask["words"])


def asked(label, made, held):
    """Once a write that made asks in its commit is pushed (write), whose commit carries each ask's entry (carried):
    each ask said, and each key found held."""
    for _, rec in made:
        run = f"{label}-{rec.get('Role')}"
        print(f"asked {run}: {rec.get('What')}" + (f" on {rec.get('Names')}" if rec.get("Names") else ""))
    for run, key in held:
        print(f"{label}/main: {run} is already asked by {key}; nothing more asked")


def roles_lines(w, fleet, label, only=None):
    """roles.rec in the write w brought to match the teams file (asks.roles_due; role-runs "Role records follow the teams
    file"), for the roles in only, or for every one: each record missing or differing written, and each of a role the
    drive's `runs` no longer names on demand removed. A branch with no roles.rec and nothing due is left with none.
    Returns whether anything changed."""
    p = crew.drive_of(fleet, label)
    metas = {r: crew.definition(asks.definition_of(r))[0] for r in crew.KIND_ROLES if crew.on_demand(p, r)}
    pl = rec_file(w, "roles.rec", ROLES)
    due, gone = asks.roles_due(asks.parse_roles(pl.text()), p, metas)
    due, gone = [d for d in due if only is None or d["Role"] in only], [g for g in gone if only is None or g in only]
    if not (due or gone):
        return False
    have = {r.get("Role"): r for r in pl.recs("Role")}
    for d in due:
        if d["Role"] in have:
            have[d["Role"]].fields = list(d.items())
        else:
            pl.insert(Rec("Role", list(d.items())))
    for g in gone:
        pl.remove(have[g])
    w.replace("roles.rec", pl.text())
    return True


# A role's run is its role's only in its own place, crew-<role>--<label> (design Decision 8): what a start or an end
# outside one says.
NOT_A_RUN = ("{cmd} runs only in a run of a crew role, in the place Flume made for it, crew-<role>--<label>, for a role its "
             "drive runs as its kind; this is none, and nothing is written")


class NothingPending(Exception):
    """A run's start that found nothing pending for its role at the tip: no turn is recorded."""


def run_named(fleet, cmd):
    """The role's run a command runs in, (label, role, its name), read from its place alone (crew.run_here), never from
    CREW_AGENT, which a standing agent carries too; refused anywhere else, naming where it runs."""
    run = crew.run_here(fleet) or fail(NOT_A_RUN.format(cmd=cmd))
    CONTEXT["label"] = run[0]
    return run[0], run[1], f"{run[0]}-{run[1]}"


def request_dicts(requests):
    """requests.rec's records as asks takes them: each a dict of its fields, a field held more than once by its first
    value, but a confirm's Delivery, the list of its keys."""
    return [dict(dict((f, v) for f, v in reversed(q.fields)), **({"Delivery": q.all("Delivery")} if q.get("Delivery") else {}))
            for q in requests]


def run_reads(fleet, label, role):
    """What a role's run's start reads of the runners, in one read (runner_facts, plan.12; design Decision 8 of
    crews-role-runs-confirm-what-they-collect): requests.rec at the tip this command fetched and each host's runner
    beside it, as (the places that wait on the role, asks.waits_on, design Decision 5 of roles-run-as-flume-kinds; every
    end Flume owes the role's address of a place crew launched, asks.ends_owed; the requests, as asks takes them; the
    words of each host whose runner can't be read). What waits on such a host, and what Flume owes there, is not taken,
    so it stays pending for the role's next run (read.3)."""
    requests, reads = runner_facts(fleet, label)
    places, unread = [], []
    for h, r in sorted(reads.items()):
        if r.get("why"):
            unread.append(r["why"])
            continue
        places += [{"Request": str(n), "Place": p["place"], "Status": p["status"]} for n, p in sorted(r["places"].items()) if not p["why"]]
    reqs = request_dicts(requests)
    address = f"{label}/{role}"
    return asks.waits_on(address, reqs, places), asks.ends_owed(address, reqs, places), reqs, unread


def turn_file(label, role):
    """Where a run's start writes its role's brief on the host (design Decision 9)."""
    return record.ROOT / label / "turns" / f"{role}.md"


def run_cards_said(fleet, label, run):
    """The role's answered cards as its run's start prints them, read in the run's own Pending You name (design Decision
    7, briefs.16): list_pending under it, then get_request of each on the agent's turn (cards.run_cards), each named by
    the key its card ask holds, card/<request>/<version>, its title and what the user answered (cards.answer_lines),
    with what closes it: crew at the act its answer asks for when crew raised it in the run's name (cards.posted_keys),
    else the run's own ack_answer at that version. Pending You read as no card answered prints nothing; Pending You not
    read says so, naming list_pending for the run to call itself, since its turn is already recorded."""
    try:
        with cards.Bridge(run, f"Call list_pending as {run} yourself, and act on what the user answered.") as py:
            listed = cards.run_cards(py.call("list_pending", {"name": run}))
            got = [(c, title, py.call("get_request", {"requestId": c, "name": run})) for c, title in listed]
    except Refusal as e:
        return [f"Your cards could not be read in Pending You as {run}: {e}"]
    if not got:
        return []
    crews = cards.posted_keys(cards.host_entries(record, label, crew.this_host()), run)
    out = [f"The cards the user answered, read in Pending You as {run}:"]
    for c, title, g in got:
        g = g if isinstance(g, dict) else {}
        v = g["version"] if isinstance(g.get("version"), int) and not isinstance(g.get("version"), bool) else None
        key = f"card/{c}/{v}" if v is not None else f"card/{c}"
        out.append(f"card {key}" + (f" ({crews[c]})" if c in crews else "") + (f": {title}" if title else ""))
        out += cards.answer_lines(crews.get(c, key), c, g)[1:]
        out.append(f"  crew closes it at the act its answer asks for, as your brief says for {crews[c]}" if c in crews else
                   f"  once you have acted on it, ack_answer (requestId {c}, expectedVersion {v}, name {run}) with a one-line outcome"
                   if v is not None else f"  Pending You gave no version for it: read it again with get_request as {run} before you ack it")
    return out


def role_start(fleet, a):
    """crew role start, a role's run's first act and the one collector of what is pending for it (design Decision 7,
    roles.7; role-runs "A run's start takes everything pending" and "A run's start prints its brief's path, then what it took in order"): in
    one commit, the turn that takes every ask of the role and every place that waits on it that no ended turn took,
    each turn of the run still open, a lost or retried run's, marked superseded by it, its asks taken again; then the
    role's brief written to the host's file for it (turn_file) and its path printed to read whole first, then each ask
    taken, oldest first, each place, the ends Flume holds for the role it took, and the role's answered cards
    (run_cards_said). The turn takes, beside what is pending, each end Flume owes the role's address that no confirm of
    the address names in requests.rec at the tip the write is applied to, so a confirm written meanwhile is seen (plan.1;
    asks.taken_ends, design Decisions 1, 2 and 5 of crews-role-runs-confirm-what-they-collect); its end asks for their
    confirmation. The ends make no role wanted: with nothing pending, no turn is recorded and no end taken, and it says
    so; its entry counts the asks and waiting places alone. Refused anywhere but a role's run (run_named)."""
    label, role, run = run_named(fleet, "crew role start")
    repo, ref = state_of(fleet, label)
    waits, owed, _, unread = run_reads(fleet, label, role)
    taken = {}

    def change(w):
        pl = rec_file(w, "asks.rec", ASKS)
        held, turns = asks.parse(pl.text())
        mine, places = asks.pending(held, waits, turns, role)
        if not (mine or places):
            raise NothingPending()
        ends = asks.taken_ends(owed, request_dicts(requests_of(w).recs("Request")), f"{label}/{role}")
        n = asks.next_turn(turns)
        old = {t["Turn"] for t in asks.superseded(turns, run)}
        for t in pl.recs("Turn"):
            if t.get("Turn") in old:
                t.set("Superseded", str(n))
        took = asks.took(mine, places, ends)
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        pl.insert(Rec("Turn", [("Turn", str(n)), ("Role", role), ("Run", run), ("Place", f"crew-{role}--{label}"),
                               ("Host", crew.this_host())] + [("Took", t) for t in took] + [("Began", now)]))
        w.replace("asks.rec", pl.text())
        k = len(mine) + len(places)
        e = record.turn_begin_entry(run, n, k)
        w.subject, w.why, w.fields = f"turn({run}): {n} takes {k}" + (f" and {len(ends)} {'end' if len(ends) == 1 else 'ends'}" if ends else "") \
            + (f", superseding {', '.join(sorted(old, key=int))}" if old else ""), e["why"], {"Took": e["Took"]}
        taken.update(n=n, asks=mine, places=places, ends=ends, old=sorted(old, key=int))
        return []
    try:
        write(fleet, label, change, f"turn({run})", act="turn.begin", on=[f"agent/{run}"])
    except NothingPending:
        print(f"Nothing waits for {run}: no turn is taken and nothing is recorded. End your turn now with crew role end.")
        for why in unread:
            print(f"{why}: what waits on {run} there is left for its next run")
        return
    brief = turn_file(label, role)
    brief.parent.mkdir(parents=True, exist_ok=True)
    brief.write_text(crew.brief(fleet, label, asks.definition_of(role), run))
    print(f"Read {brief} whole first: it is your brief as {run}, filled for {label}.")
    if taken["old"]:
        print(f"Turn {taken['n']} takes again what turn {', '.join(taken['old'])} took, whose run ended before its end: that turn answers nothing.")
    for x in taken["asks"]:
        print("\n".join(asks.ask_said(x)))
    for x in taken["places"]:
        print("\n".join(asks.wait_said(x)))
    for line in asks.ends_said(taken["ends"]):
        print(line)
    for why in unread:
        print(f"{why}: what waits on {run} there is left for its next run")
    for line in run_cards_said(fleet, label, run):
        print(line)


def role_end(fleet, a):
    """crew role end --report <path> "<what was done>", a role's run's last act (design Decision 7; role-runs "A run's end
    answers what it took"): the run's open turn recorded ended with the words, in one commit, and the report written at
    the path, the stage's deliverable, naming the turn, what it took and what was done. In that commit, one confirm is
    appended to requests.rec for each launch whose place's ends the turn took, oldest first, naming the launch, the
    role's address and each end's delivery key in the order taken, for the runner that holds the launch to confirm to
    Flume as the role (asks.turn_confirms; design Decisions 3, 4 and 6 of crews-role-runs-confirm-what-they-collect),
    read at the tip the write is applied to for each launch's work (plan.1); a turn that took no end appends none. With
    no open turn, a run that found nothing pending, the report says no turn was taken and nothing is recorded, so every
    run delivers its stage, and no confirm is asked. Refused anywhere but a role's run (run_named)."""
    label, role, run = run_named(fleet, "crew role end")
    report = pathlib.Path(a.report).expanduser()
    ended = {}

    def change(w):
        pl = rec_file(w, "asks.rec", ASKS)
        held, turns = asks.parse(pl.text())
        t = asks.open_turn(turns, run)
        if t is None:
            raise NothingPending()
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rec = next(r for r in pl.recs("Turn") if r.get("Turn") == t["Turn"])
        rec.set("Ended", now, after="Began")
        rec.set("Said", a.words, after="Ended")
        w.replace("asks.rec", pl.text())
        confirms = asks.turn_confirms(t["Took"], request_dicts(requests_of(w).recs("Request")))
        asked = [request(w, "confirm", work, Of=n, Recipient=f"{label}/{role}", Delivery=keys) for n, work, keys in confirms]
        m = sum(len(keys) for _, _, keys in confirms)
        e = record.turn_end_entry(run, t["Turn"])
        w.subject, w.why = f"turn({run}): {t['Turn']} ends" + (
            f", asking {len(asked)} {'confirm' if len(asked) == 1 else 'confirms'} of {m} {'end' if m == 1 else 'ends'}" if asked else ""), e["why"]
        ended.update(turn=t, held=held, at=now, asked=asked, ends=m)
        return []
    try:
        write(fleet, label, change, f"turn({run})", act="turn.end", on=[f"agent/{run}"])
    except NothingPending:
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(asks.no_turn_report(run, a.words, now))
        print(f"{run} took no turn, so nothing is recorded; the report {report} says so.")
        return
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(asks.report(ended["turn"], ended["held"], a.words, ended["at"]))
    print(f"turn {ended['turn']['Turn']} of {run} is ended, and its report is {report}.")
    if ended["asked"]:
        n = len(ended["asked"])
        print(f"The {ended['ends']} {'end' if ended['ends'] == 1 else 'ends'} it took {'is' if ended['ends'] == 1 else 'are'} confirmed to "
              f"Flume as {label}/{role} once the runners carry {'request' if n == 1 else 'requests'} {asks.listed([str(x) for x in ended['asked']])}.")


def role_open(fleet, a):
    """crew role open <role> [--label L], the user opening a role that runs as its kind to talk with its run (design
    Decision 13; role-runs "The user opens a role to talk"): an `open` ask of the role from whoever runs it, in a commit
    of its own (ask_write), saying its run opens as the place crew-<role>--<label> on the main level's host once the
    runner there makes it, with the runner's words where its last launch of the run was refused. Where the runner's
    records on that host show a run of the role live (runner.role_run), nothing is written and that run's place is named
    to talk to now; where they can't be read, it refuses naming what it could not read, writing nothing (read.1), as it
    does for a role the drive runs as a standing agent."""
    label = default_label(fleet, a) or fail(f"which drive's {a.role}? add --label " + "|".join(fleet["drives"]))
    run, host, place = f"{label}-{a.role}", crew.drive_of(fleet, label)["machine"], f"crew-{a.role}--{label}"
    if crew.role_runs(fleet, label, a.role) == crew.RUNS_STANDING:
        fail(f"{label} runs its {a.role} as a standing agent, {run}, in its tab of crew main up {label}: crew role open opens "
             "only a role its drive runs as its kind; nothing is written")
    _, reads = runner_facts(fleet, label)
    r = runner.role_run(runner.of_host(reads, label, host), f"{label}/{a.role}")
    if r["why"]:
        fail(f"crew can't tell whether a run of {run} is live: {r['why']}; nothing is written")
    if r["live"]:
        print(f"{run}'s run is live on {host}, the place {r['place']}: talk to it there now, as {place} in herdr; nothing is written")
        return
    ask_write(fleet, label, a.role, "open", record.who())
    print(f"asked {run} to open: its run opens as the place {place} in herdr on {host} once the runner there makes it, "
          "and greets you in its pane")
    if r["words"]:
        print(f"the runner on {host} could not launch {run}'s last run: {r['words']}")


def land_named(fleet, label, kits):
    """The repositories a role's work may land in (runner.role_launch), as owner/name: every drive's blueprints
    repositories, which the teams file names, and the drive's kits (kits, drive_kits), a kit its plan names by
    its name alone as the drive's main-level host keeps it (crew.kits_kept), where the role's work is launched. Not
    a state repository, whose branches crew's own commands alone write (state.1)."""
    named = {b for p in fleet["drives"].values() for b in p["blueprints"]}
    host = crew.drive_of(fleet, label)["machine"]
    named |= {k["repo"] for k in crew.kits_kept(fleet, host, [k for k in kits if "/" not in k])}
    return named | {k for k in kits if "/" in k}


def role_land(fleet, a):
    """crew role land <repo> <name> --brief-file <file>, a role's run's work that lands (design Decision 10; role-runs "A
    role's work that lands is a place it launches"; roles.7 part 3): in a commit of its own, a launch of Flume's chore
    kind named <name> in the repository on its default branch, on the main level's host in the drive's own stream, named
    by its label (Decision 2 of a-roles-way-of-running-says-what-it-means), the file's text whole its brief and the run's address its recipient, for the runner there to launch (runner.role_launch),
    read again at the tip it is applied to (plan.1). Recorded as role.land on role/<role>/<name> and the run, done or
    refused; none of the brief's words (record.3). The run commits on no branch, submits nothing and leaves no worktree:
    Flume builds the chore, submits it through sluice and tidies its place, and its landing, or a wait on its caller,
    reaches the role's next run. Refused anywhere but a role's run (run_named), which is who writes it, never by its
    name (Decision 16 of teams-cross-to-flume-as-their-bolts-land, may_request)."""
    label, role, run = run_named(fleet, "crew role land")
    on, seen = [f"role/{role}/{a.name}", f"agent/{run}"], {}
    host, stream = crew.drive_of(fleet, label)["machine"], label
    try:
        crew.NAME.match(a.name) or fail(f"work that lands is named with lowercase words and dashes, not {a.name}")
        path = pathlib.Path(a.brief_file).expanduser()
        try:
            brief = path.read_text().rstrip("\n")  # the text whole, less the file's last line end
        except (OSError, UnicodeDecodeError) as e:
            fail(f"the brief {path} can't be read: {e.strerror or e}")

        def change(w):
            launched, why = runner.role_launch(requests_of(w).recs("Request"), land_named(fleet, label, kits_at(w.repo, w.tip, w.plan)),
                                               label, role, host, stream,
                                               a.repo, a.name, brief)
            not why or fail(why)
            act, work, given = launched
            seen.update(n=request(w, act, work, **given))
            return []
        write(fleet, label, change, f"land({run}): {a.name} in {a.repo}", act="role.land", on=on, fields={"Repo": a.repo})
    except Refusal as e:
        record.emit(label, "role.land", on, refused=str(e), Repo=a.repo)
        raise
    print(f"the runner on {host} launches chore {a.name} in {a.repo} on {runner.ROLE_BASE} (request {seen['n']}) in stream {stream}, "
          f"your brief its brief whole and {label}/{role} its recipient: Flume builds it and submits it through sluice, and its "
          f"landing, or a wait on you, reaches {run}'s next run")


# --------------------------------------------------------------------------------------------- proposals

PROPOSALS = """\
# The planner's proposals: each change it would make to the plan, waiting for the user's approval. Written only
# through crew plan. A proposal is never removed, its commands never change, and its number is never reused.

%rec: Proposal
%doc: A case, and the plan commands it would run in order (Do), as typed without the leading crew.
%key: Proposal
%type: Proposal,Replaces int
%type: State enum open approved dropped
%type: Opened,Closed date
%mandatory: Proposal Case Do State Opened By
%allowed: Proposal Case Do State Opened By Closed Reason Replaces Cleared
"""
# The commands a proposal may hold.
PROPOSABLE = tuple(OPS)


class Strict(argparse.ArgumentParser):
    """crew's own parser, refusing instead of exiting: a proposal's Do is read by the same grammar as the command line."""

    def error(self, message):
        fail(message)


def refuse(said, recorded):
    """A refusal that quotes typed text: said whole, and in the run record as crew's own words without it (record.3)."""
    e = Refusal(said)
    e.recorded = recorded
    raise e


def do_named(a):
    """A proposal's command as the run record holds it: the command and what it acts on, never its intent or reason."""
    return f"{a.cmd} {a.sub} " + (a.bolt if a.cmd == "bolt" else f"{a.old} {a.new}" if a.cmd == "kit" else a.unit)


def do_args(label, do):
    """A proposal's Do as crew's parser reads it: one of the ten plan commands, in the proposal's drive."""
    try:
        argv = shlex.split(do)
    except ValueError as e:
        refuse(f"`{do}`: {e}", f"a Do line does not parse: {e}")
    argv = argv[1:] if argv[:1] == ["crew"] else argv
    held = "a proposal holds only the plan's commands (" + ", ".join(" ".join(k) for k in PROPOSABLE) + ")"
    tuple(argv[:2]) in PROPOSABLE or refuse(f"{held}, not `{do}`", held)
    try:
        a = parser(Strict).parse_args(argv)
    except Refusal as e:
        refuse(f"`{do}`: {e}", f"`{' '.join(argv[:2])}` does not parse as crew's parser reads it")
    getattr(a, "label", None) in (None, label) or refuse(f"`{do}` names drive {a.label}, and the proposal is {label}'s",
                                                         f"`{do_named(a)}` names drive {a.label}, and the proposal is {label}'s")
    a.label, a.do = label, do
    return a


def proposals(w):
    """proposals.rec of the drive as the write has it, or a new one when the branch has none yet."""
    text = w.text("proposals.rec")
    return Plan(text if text is not None else PROPOSALS)


def proposal(pl, n, label):
    return next((p for p in pl.recs("Proposal") if p.get("Proposal") == str(n)), None) or fail(
        f"no proposal {n} in {label}/main")


def objects(argvs):
    """Every bolt, unit and chore a proposal's commands name, as run-record objects, in order and once each."""
    out = []
    for a in argvs:
        if a.cmd == "bolt":
            out.append(f"bolt/{a.bolt}")
        elif a.cmd == "kit":
            out += [f"kit/{a.new.split('/')[-1]}", f"kit/{a.old}"]
        else:
            out.append(f"{a.cmd}/{a.unit}")
            out += [f"unit/{n}" for n, _ in getattr(a, "into", None) or []]
            if a.sub == "add" and a.bolt:
                out.append(f"bolt/{a.bolt}")
            if a.sub == "move" and a.bolt != "queue":
                out.append(f"bolt/{a.bolt}")
    return list(dict.fromkeys(out))


def summary(argvs):
    """A proposal's changes in a few words that name things and quote nothing anyone typed, for its subjects."""
    words = {("bolt", "new"): lambda a: f"new bolt {a.bolt}", ("bolt", "start"): lambda a: f"start bolt {a.bolt}",
             ("bolt", "order"): lambda a: f"order bolt {a.bolt}",
             ("bolt", "drop"): lambda a: f"drop bolt {a.bolt}",
             ("unit", "add"): lambda a: f"add {a.unit} to " + (a.bolt or f"the {a.repo} queue"),
             ("unit", "split"): lambda a: f"split {a.unit}", ("unit", "amend"): lambda a: f"amend {a.unit}",
             ("unit", "order"): lambda a: f"order {a.unit}",
             ("unit", "after"): lambda a: f"set what {a.unit} comes after",
             ("unit", "move"): lambda a: f"move {a.unit} to " + ("the queue" if a.bolt == "queue" else a.bolt),
             ("unit", "drop"): lambda a: f"drop {a.unit}", ("kit", "rename"): lambda a: f"rename kit {a.old} {a.new}"}
    # A chore's command is said as the unit's, its name as `chore <name>`.
    return ", ".join(words[("unit", a.sub)](argparse.Namespace(**dict(vars(a), unit=called(a)))) if a.cmd == "chore"
                     else words[(a.cmd, a.sub)](a) for a in argvs)


def touched_by(plan, argvs):
    """The bolts each of a proposal's commands touches, read from the plan and the commands alone (no kit is read): a
    unit's or chore's add's bolt; the bolt a unit or chore leaves and the one it joins; the bolt of a unit split, or of
    a unit or chore ordered, given what it comes after, amended or dropped; the bolt of a bolt start, order or drop. A
    bolt new touches none."""
    where = {u.name(): u.get("Bolt") for u in plan.work()}
    out = []
    for a in argvs:
        key, t = ("unit" if a.cmd == "chore" else a.cmd, a.sub), []
        if key in (("bolt", "start"), ("bolt", "order"), ("bolt", "drop")):
            t = [a.bolt]
            for u in [u for u, b in where.items() if b == a.bolt]:
                if a.sub == "drop":
                    where[u] = None
        elif key == ("unit", "add"):
            t, where[a.unit] = [a.bolt], a.bolt
        elif key == ("kit", "rename"):
            t = [b.name() for b in renamed_in(plan, a.old)[0]]
        elif key == ("unit", "move"):
            to = None if a.bolt == "queue" else a.bolt
            t, where[a.unit] = [where.get(a.unit), to], to
        elif key[0] == "unit":
            t = [where.get(a.unit)]
            for n, _ in getattr(a, "into", None) or []:
                where[n] = where.get(a.unit)
            if a.sub == "drop":
                where.pop(a.unit, None)
        out.append([b for b in t if b])
    return out


def flat(lists):
    return list(dict.fromkeys(x for l in lists for x in l))


def apply_all(fleet, label, w, argvs, n):
    """Proposal n's commands built and applied in order to the write's plan, each checked against the plan as the ones
    before it left it. Returns the ops, each with the objects its change added and where its entry goes among the
    write's further acts (Op.also_at), and the bolts whose conductors hear the write."""
    ctx, ops, told = Proposed(fleet, label, w, n), [], []
    for a in argvs:
        try:
            op = OPS[(a.cmd, a.sub)](ctx, a)
            op.also_at = len(w.also)  # its entry goes ahead of those its change adds (Write.also)
            n_on, n_frm = len(w.on), len(w.frm)
            told += op.change(w) or []
        except Refusal as e:
            refuse(*command_refused(a, e))
        op.added_on, op.added_frm = w.on[n_on:], w.frm[n_frm:]
        ops.append(op)
    return ops, list(dict.fromkeys(told))


def command_refused(a, e):
    """A proposal's command refused, as said, its line as typed, and as recorded, its command and the names it acts on
    with no intent or reason typed in it (record.3)."""
    return f"`{a.do}`: {e}", f"`{do_named(a)}`: {getattr(e, 'recorded', None) or e}"


def check_ops(fleet, label, w, argvs, n, seen=Proposed):
    """Proposal n's commands applied in order to a copy of the plan and of the files they change: every refusal and
    rule each has when run directly, the schema's and crew's own rules included. Returns the copy, which a proposal's
    card draws (seen=Drawn, which reads no kit) and nothing writes."""
    scratch = Write(w.repo, label, w.tip, Plan(w.plan.text()))
    scratch.files = dict(w.files)
    scratch.runners = w.runners  # the runners as the write read them, so a start's check reads them no other way
    for a in argvs:
        try:
            OPS[(a.cmd, a.sub)](seen(fleet, label, scratch, n), a).change(scratch)
        except Refusal as e:
            refuse(*command_refused(a, e))
    try:
        check(scratch.plan)
        checked({"plan.rec": scratch.plan.text(), **scratch.files})
    except Refusal as e:
        fail(f"the proposal as a whole: {e}")
    return scratch


def read_proposal_file(path):
    """The planner's proposal file: one record of a Case and its Do lines, and nothing else."""
    try:
        text = pathlib.Path(path).read_text()
    except OSError as e:
        fail(f"cannot read {path}: {e.strerror}")
    recs = [p for p in Plan(text).paras if isinstance(p, Rec)]
    len(recs) == 1 or fail(f"{path} holds {len(recs)} records: a proposal file is one record of a Case and its Do lines")
    r = recs[0]
    other = sorted({n for n, _ in r.fields if n not in ("Case", "Do", "#")})
    not other or fail(f"{path} has fields a proposal file doesn't: " + ", ".join(other) + "; only Case and Do")
    len(r.all("Case")) == 1 and r.get("Case").strip() or fail(f"{path} needs one Case: why these changes")
    r.all("Do") or fail(f"{path} has no Do: the plan commands the proposal would run, in order")
    return r.get("Case").strip(), r.all("Do")


def proposal_label(fleet, a, n=None):
    """The drive a proposal command means: --label, the agent's own, the only drive, or, for a numbered
    proposal, the one drive whose branch has that number."""
    label = default_label(fleet, a)
    if label:
        return label
    if len(fleet["drives"]) == 1:
        return next(iter(fleet["drives"]))
    n is not None or fail("which drive's proposals? add --label " + "|".join(fleet["drives"]))
    hits = []
    for l in fleet["drives"]:
        repo, ref = state_of(fleet, l)
        tip = tip_of(repo, ref)
        text = show(repo, tip, "proposals.rec") if tip else None
        if text and any(p.get("Proposal") == str(n) for p in Plan(text).recs("Proposal")):
            hits.append(l)
    len(hits) == 1 or fail(f"proposal {n} is in " + (", ".join(hits) or "no drive's proposals") + ": add --label")
    CONTEXT["label"] = hits[0]
    return hits[0]


def at_tip(fleet, label, n):
    """The drive's branch at its tip, with proposal n: (repo, tip, plan, proposals, the proposal, its commands)."""
    repo, ref = state_of(fleet, label)
    tip = tip_of(repo, ref) or fail(f"{repo} has no {ref} yet: crew state init {label}")
    w = Write(repo, label, tip, read(repo, ref, tip))
    pl = proposals(w)
    p = proposal(pl, n, label)
    return w, pl, p, [do_args(label, d) for d in p.all("Do")]


def tell_planner(fleet, label, text):
    planner = f"{label}-planner"
    if agent() != planner:
        crew.tell(fleet, planner, text)


# A decision record a source names by its path (plan-proposals): docs/adr/ and its four digits, the repository's when
# <owner>/<name> and a colon or a space come right before it. The lookbehinds keep a path's tail from reading as a
# repository, and other/docs/adr/ from reading as a record.
RECORD_REF = re.compile(r"(?:(?<![\w./-])([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)[:\s])?(?<![\w./-])docs/adr/(\d{4})(?!\d)")
UNACCEPTED = "crew refuses the proposal: it rests on records the user has not accepted."
UNACCEPTED_AFTER = "Propose it once each record is accepted on its kit's main."


def record_refs(source, kit_repo):
    """The decision records a source names, [(repo, number)] in the order they appear and each once: each by its path
    (RECORD_REF), of the repository written before it, else of kit_repo, the repository of the kit whose work names it.
    A record named only in words ("record 0026") is no record here, since nothing in the words says whose it is."""
    return list(dict.fromkeys((m.group(1) or kit_repo, int(m.group(2))) for m in RECORD_REF.finditer(source)))


def record_items(fleet, label, plan, argvs):
    """The records a proposal's new work names (plan-proposals, briefs.15): for each bolt its `bolt new`s create, then
    each unit or chore it makes new to a bolt or the queue (new_units), as the plan its commands leave holds them, each
    record its sources name (record_refs), as (kind, name, kit, repo, number): kit the record's kit as a refusal names
    it, the work's kit by its name, or <owner>/<name> when the record is another repository's, and repo the repository
    it is read in, the work's kit as the drive's main-level host keeps it (main_kit; the user's ruling of
    2026-11-01). A source's repository is read as written. Work whose sources name a record and whose kit that host
    keeps no checkout of is refused, since crew can't tell whose records they are (read.1)."""
    work = [("bolt", a.bolt, plan.bolt(a.bolt)) for a in argvs if (a.cmd, a.sub) == ("bolt", "new")]
    work += [(kind_of(plan.item(u)) if plan.item(u) else "unit", u, plan.item(u)) for u in new_units(argvs)]
    out = []
    for kind, name, r in work:
        sources = [s for s in (r.all("Source") if r else []) if RECORD_REF.search(s)]
        if not sources:
            continue
        kit = r.get("Repo")
        t = main_kit(fleet, label, kit)
        t or fail(f"{kind} {name} names a decision record, and " + main_kit_said(fleet, label, kit, "tell whose it is"))
        k = t["kit"]
        for s in sources:
            for repo, n in record_refs(s, k["repo"]):
                own = repo == k["repo"]
                out.append((kind, name, k["name"], k["repo"], n) if own else (kind, name, repo, repo, n))
    return list(dict.fromkeys(out))


def unaccepted(items, held):
    """Why a proposal can't be written because its new work rests on records the user has not accepted, or None when
    every one is (plan-proposals, roles.3 on briefs.15): one line for each item, (kind, name, kit, repo, number) as
    record_items gives them, whose record its main does not hold accepted, saying what it holds, read from held, which
    maps (repo, number) to the files main holds by that number with the one file's status and whether an amendment is
    marked proposed ({"files", "status", "marked"}), or to why it could not be read ({"why"}, read.1)."""
    lines = []
    for kind, name, kit, repo, number in items:
        h, n = held[(repo, number)], f"{number:04d}"
        if "why" in h:
            says = h["why"]
        elif not h["files"]:
            says = f"{kit}'s main holds no record {n} in docs/adr/"
        elif len(h["files"]) > 1:
            says = f"{kit}'s main holds {len(h['files'])} records numbered {n}: {', '.join(h['files'])}"
        elif record_accepted(h["status"], h["marked"]):
            continue
        else:
            says = f"{kit}'s main holds it " + ("" if h["status"] else "with ") + record_says(h["status"], h["marked"])
        lines.append(f"  {kind} {name} names record {n} of {kit}: {says}")
    return "\n".join([UNACCEPTED, *lines, UNACCEPTED_AFTER]) if lines else None


def proposal_records(fleet, label, scratch, argvs):
    """The records a proposal's new work names, read on each repository's main as GitHub holds it now (plan.18): the
    items record_items finds in the plan its commands leave (scratch), and what each repository's main holds by each
    number, for unaccepted. Each repository is fetched once into crew's cache, held for the command (plan.12), its
    docs/adr/ listed at that tip and the one file by a number read; a main that can't be fetched, or a file that can't
    be read as text, gives why, naming it (read.1, read.2). Returns (items, held)."""
    items, held = record_items(fleet, label, scratch.plan, argvs), {}
    for repo in dict.fromkeys(i[3] for i in items):
        numbers = sorted({i[4] for i in items if i[3] == repo})
        try:
            tip = tip_of(repo, "main")
            listed = git(repo, "ls-tree", "--name-only", tip, "docs/adr/").splitlines() if tip else []
        except Refusal as e:
            held.update({(repo, n): {"why": str(e)} for n in numbers})
            continue
        for n in numbers:
            if not tip:
                held[(repo, n)] = {"why": f"{repo} has no main on GitHub"}
                continue
            files = [f for f in listed if re.fullmatch(rf"docs/adr/{n:04d}-[^/]*\.md", f)]
            held[(repo, n)] = {"files": files, "status": "", "marked": False}
            if len(files) != 1:
                continue
            try:
                text = show(repo, tip, files[0])
            except UnicodeDecodeError:
                text = None
            if text is None:
                held[(repo, n)] = {"why": f"crew can't read {files[0]} on {repo}'s main at {tip[:7]} as text"}
                continue
            status, marked = record_status_held(text)
            held[(repo, n)].update(status=status, marked=bool(marked))
    return items, held


def plan_propose(fleet, a):
    """crew plan propose <file> [--replaces <n>]: the planner's proposal, checked against the plan at the tip, written
    open with the next number, waiting on the user alone. Refused, with nothing written,
    when a bolt it creates, or a unit or chore it adds or moves into a bolt, names a decision record its main on GitHub
    does not hold accepted (proposal_records, unaccepted). Once it is written, crew raises its card in the planner's
    name, or, for a rewrite, changes its chain's card in place (raise_proposal_at)."""
    kind, of = role(fleet, crew.caller(fleet))
    kind in ("planner", "user") or fail(proposer_refusal(fleet, crew.caller(fleet), kind, of))
    label = of if kind == "planner" else proposal_label(fleet, a)
    a.label in (None, label) or fail(f"{label}-planner proposes for {label}, not {a.label}")
    CONTEXT["label"] = label
    case, dos = read_proposal_file(a.file)
    argvs = [do_args(label, d) for d in dos]
    seen = {}

    def change(w):
        pl = proposals(w)
        n = next_proposal(pl)
        scratch = check_ops(fleet, label, w, argvs, n)
        said = unaccepted(*proposal_records(fleet, label, scratch, argvs))
        not said or fail(said)
        seen["old_by"] = open_proposal(pl, n, case, dos, agent(), datetime.date.today().isoformat(), a.replaces, label)
        w.replace("proposals.rec", pl.text())
        w.subject = f"plan(proposal {n}): propose: {summary(argvs)}"
        w.on += [f"proposal/{n}"] + objects(argvs) + ([f"proposal/{a.replaces}"] if a.replaces else [])
        seen.update(n=n, w=w)
        return []
    write(fleet, label, change, "plan: propose", act="plan.propose")
    n = seen["n"]
    if a.replaces:
        print(f"proposal {a.replaces} is dropped, replaced by proposal {n}")
    print(f"proposal {n} is open, waiting on the user: crew plan proposed {n} --label {label}")
    if kind != "planner" and a.replaces and seen.get("old_by") == f"{label}-planner":
        tell_planner(fleet, label, f"Proposal {a.replaces} was replaced by proposal {n}, by {agent()}.")
    raise_proposal_at(fleet, label, seen["w"], n, "replace" if a.replaces else "propose")


def proposer_refusal(fleet, name, kind, of):
    """Why an agent may not propose (roles.1): only the planner and the user write proposals."""
    return f"{name} does not write proposals: tell {planner_of(fleet, kind, of)}, who proposes changes to the plan"


def next_proposal(pl):
    """The number a new proposal takes: one past the highest, never reused (plan.4)."""
    return 1 + max([int(p.get("Proposal")) for p in pl.recs("Proposal")] or [0])


def open_proposal(pl, n, case, dos, by, today, replaces=None, label=None):
    """Proposal n written open in proposals.rec (pl), its case and commands as given (plan.4); one it replaces, which
    must be open, is dropped with the reason that it was replaced. Returns who wrote the
    one replaced."""
    old_by = None
    if replaces:
        old = proposal(pl, replaces, label)
        old.get("State") == "open" or fail(f"proposal {replaces} is {old.get('State')}, so nothing replaces it")
        old_by = old.get("By")
        old.set("State", "dropped")
        old.set("Closed", today, after="By")
        old.set("Reason", f"replaced by proposal {n}", after="Closed")
    pl.insert(Rec("Proposal", [("Proposal", str(n)), ("Case", case)] + [("Do", d) for d in dos]
                  + [("State", "open"), ("Opened", today), ("By", by)] + ([("Replaces", str(replaces))] if replaces else [])))
    return old_by


def proposal_chain(pl, n):
    """Proposal n's chain in proposals.rec (pl), its first to n: each proposal it replaces, followed back by Replaces.
    The chain is one card, keyed by its first, proposal/<first> (record 0031 §1)."""
    out = [n]
    while True:
        p = next((p for p in pl.recs("Proposal") if p.get("Proposal") == str(out[0])), None)
        back = int(p.get("Replaces")) if p is not None and (p.get("Replaces") or "").isdigit() else None
        if back is None or back in out:
            return out
        out.insert(0, back)


def closed_refusal(p, n):
    """Why proposal n can't be approved because it is closed, said with its reason and recorded without it (record.3),
    or None while it is open."""
    if p.get("State") == "open":
        return None
    state = f"proposal {n} is {p.get('State')}"
    return state + (f": {p.get('Reason')}" if p.get("Reason") else ""), state


def close(p, state, today, reason=None, cleared=()):
    """A proposal closed: approved, with each new unit the user left out of the change as Cleared, or dropped with its
    reason; one that is not open is refused, saying what it is (plan.4)."""
    p.get("State") == "open" or fail(f"proposal {p.get('Proposal')} is {p.get('State')}, so it can't be " + (
        "dropped" if state == "dropped" else "approved"))
    p.set("State", state)
    p.set("Closed", today, after="By")
    if reason:
        p.set("Reason", reason, after="Closed")
    for u in cleared:
        p.add("Cleared", u, after="Closed")


def plan_approve(fleet, a):
    """crew plan approve <n> [--clear <unit>...]: the proposal's commands applied in order to the plan at the tip, and
    the proposal closed as approved, in one commit, which carries and names the plan.approve entry and each applied
    command's, from proposal/<n> (Write.also, carried); refused, with nothing changed, when a command no longer applies: it
    waits on the user alone. A rebase it prepares is undone if the approval is refused. With
    --clear, the commands that concern only the units the user left out are not applied, a command left in that names
    one refuses the whole, and the proposal records each as Cleared (plan.3). Then crew closes the proposal's card with
    what was applied, and the planner is told it when someone else approved (raise_proposal_at)."""
    label = proposal_label(fleet, a, a.n)
    CONTEXT["label"] = label
    w0, _, p0, argvs = at_tip(fleet, label, a.n)
    repo = w0.repo
    cleared = list(dict.fromkeys(getattr(a, "clear", None) or []))

    def opened(p):
        why = closed_refusal(p, a.n)
        not why or refuse(*why)
    opened(p0)
    applied = kept(argvs, cleared, a.n)
    ops0 = apply_all(fleet, label, w0, applied, a.n)[0]  # checked at the tip, to know what to prepare
    undos, seen = [], {}
    try:
        for op in ops0:
            if op.prepare:
                undos.append(op.prepare())

        def change(w):
            pl = proposals(w)
            p = proposal(pl, a.n, label)
            opened(p)
            ops, told = apply_all(fleet, label, w, applied, a.n)
            for op in reversed(ops):  # each applied command's entry, carried and named in the approval's one commit
                w.also.insert(op.also_at, (None, op.act, op.on + op.added_on, dict(op.fields, why=record.subject(op.subject),
                                                                                    frm=op.frm + op.added_frm + [f"proposal/{a.n}"])))
            if cleared:  # a branch's proposals.rec keeps the descriptor it was made with, from before Cleared
                in_step(pl, PROPOSALS)
            close(p, "approved", datetime.date.today().isoformat(), cleared=cleared)
            w.replace("proposals.rec", pl.text())
            w.subject = f"plan(proposal {a.n}): approve: {summary(applied) or 'nothing applied'}"
            w.on += [f"proposal/{a.n}"] + objects(argvs)
            seen.update(ops=ops, w=w)
            return told
        body = f"Left out: {', '.join(cleared)}" if cleared else ""
        sha = write(fleet, label, change, "plan: approve", body, act="plan.approve")
    except Refusal:
        for undo in reversed([u for u in undos if u]):
            undo()
        raise
    for op in seen["ops"]:
        if op.after:
            op.after(repo, sha)
    print(f"proposal {a.n} is approved and applied" + (f", without {joined(cleared)}" if cleared else ""))
    words = approved_words(applied, cleared)
    if p0.get("By") == f"{label}-planner":
        tell_planner(fleet, label, f"Proposal {a.n} was approved by {agent()}. {words}")
    raise_proposal_at(fleet, label, seen["w"], a.n, "approve", outcome=words)


def plan_drop(fleet, a):
    """crew plan drop <n> "<reason>": an open proposal closed unapplied, with the reason kept whole on its record; the
    planner is told when someone else dropped it, and crew withdraws its card with the reason, or acks it, once the
    user answered it, as dropped on their note (raise_proposal_at, DROPPED)."""
    label = proposal_label(fleet, a, a.n)
    CONTEXT["label"] = label

    def change(w):
        pl = proposals(w)
        p = proposal(pl, a.n, label)
        argvs = [do_args(label, d) for d in p.all("Do")]
        close(p, "dropped", datetime.date.today().isoformat(), a.reason)
        w.replace("proposals.rec", pl.text())
        w.subject = f"plan(proposal {a.n}): drop"
        w.on += [f"proposal/{a.n}"] + objects(argvs)
        seen["w"] = w
        return []
    seen = {}
    write(fleet, label, change, "plan: drop", a.reason, act="plan.drop")
    said = f"Proposal {a.n} was dropped by {agent()}: {a.reason.strip()}"
    tell_planner(fleet, label, said + ("" if said[-1:] in ".!?" else "."))
    raise_proposal_at(fleet, label, seen["w"], a.n, "drop", reason=a.reason.strip())


def signal_text(fleet, label, sig):
    """A signal's assertion, its excerpt and the excerpt's grade where its capture has one, from whichever home holds
    it, for a proposal's page."""
    try:
        hit = signal_at(fleet, label, sig)
    except Refusal:
        return None, None, None
    if not hit:
        return None, None, None
    _, repo, tip, text, sig = hit
    return (*asserted(text), field(show(repo, tip, capture_of(sig)) or "", "excerpt"))


def asserted(text):
    """A signal's assertion and its quoted excerpt, the first paragraph of its body that is not a quote and the first
    that is, or None for either it lacks."""
    body = text.split("---", 2)[2] if text.startswith("---") and text.count("---") >= 2 else text
    paras = [p.strip() for p in body.strip().split("\n\n") if p.strip()]
    return next((p for p in paras if not p.startswith(">")), None), next((p for p in paras if p.startswith(">")), None)


def amendment(fleet, label, plan, a, alone=False):
    """A unit amend as the user reads it: the unit's bolt, team and stage, its intent as it stands and as it would be,
    and what approval sets in motion. The stage is read from the unit's kit; alone, nothing is read but the plan, and
    only its first line is said."""
    return amendment_lines(plan, a, None if alone or plan.unit(a.unit) is None else unit_stage(fleet, label, plan, a.unit))


def amendment_lines(plan, a, s):
    """What a proposal's page says of a unit amend: the unit's bolt and team, and, given its stage (s, None when the page
    is drawn alone), its intent as it stands and as proposed and what approval sets in motion: for a unit of a bolt given
    through Flume, its construct retried with the new intent, or its launch not yet started dropped and launched anew
    (reach_places), as the approval's own write does."""
    u = plan.unit(a.unit)
    if u is None:
        return [f"**Amend unit `{a.unit}`**, new in this proposal", f"Intent, as proposed:  {a.intent}"]
    b = u.get("Bolt")
    where = (f"bolt `{b}`" + (" (started)" if started(plan.bolt(b)) else "")) if b else f"the queue of {u.get('Repo')}"
    if s is None:
        return [f"**Amend unit `{a.unit}`** in {where}"]
    st = s["stage"]
    now = ("" if st == "queued" else f", its stage unknown ({s.get('why')})" if st == "unknown" else
           f", now in {st}" if st in ("construct", "planned", "code", "verify") else f", now {st}")
    flume = s.get("flume")
    then = ("On approval: its launch, which Flume has not started, is dropped and launched again carrying the new intent."
            if flume and flume.get("stage") in ("launching", "waiting") else
            "On approval: Flume runs its construct again with the new intent, and the unit goes on from its tasks with no "
            "approval asked, its revised change due for the next batch." if flume and st != "unknown" else
            "On approval: its intent is replaced; it has no change written yet, so nothing else changes.")
    return [f"**Amend unit `{a.unit}`** in {where}{now}", f"Intent, as it stands: {u.get('Intent')}", f"Intent, as proposed:  {a.intent}", then]


def describe(fleet, label, plan, p, alone=False, signal_of=None):
    """A proposal as the user reads it: each change in plain words, with what the user is comparing beside it (a unit's
    intent and sources, the goal of the bolt it would join and whether it is started, an amended unit's intent before
    and after). alone, it reads nothing but the plan and the proposal: no kit for an amended unit's stage and
    no signal, as a proposal's card is drawn (plan.12). signal_of(id) gives a unit's signal as signal_text reads it."""
    signal_of = signal_of or (lambda sig: signal_text(fleet, label, sig))
    argvs = [do_args(label, d) for d in p.all("Do")]
    per = touched_by(plan, argvs)
    new_bolts, changes = {}, []

    def bolt_line(b):
        if b in new_bolts:
            return f"bolt `{b}` (new in this proposal)"
        r = plan.bolt(b)
        return f"bolt `{b}`" + (", started" if started(r) else "")

    def goal_of(b):
        return new_bolts.get(b) or (plan.bolt(b).get("Goal") if plan.bolt(b) else None)

    def intent_of(u):
        r = plan.item(u)
        return r.get("Intent") if r else None
    for i, a in enumerate(argvs):
        # A chore's command reads as the unit's of the same name, said of a chore and its words (plan.11).
        key, lines = ("unit" if a.cmd == "chore" else a.cmd, a.sub), []
        noun, says = ("chore", "Chore") if a.cmd == "chore" else ("unit", "Intent")
        if key == ("bolt", "new"):
            new_bolts[a.bolt] = a.goal
            lines = [f"**New bolt `{a.bolt}`** in {a.repo}", f"Goal: {a.goal}"] + [f"Source: {s}" for s in a.source]
        elif key == ("bolt", "start"):
            lines = [f"**Start bolt `{a.bolt}`**: its work launched through Flume", f"Goal: {goal_of(a.bolt)}"]
        elif key == ("bolt", "order"):
            where = "first" if a.first else "last" if a.last else f"before `{a.before}`"
            lines = [f"**Order bolt `{a.bolt}`** {where}", f"Goal: {goal_of(a.bolt)}"]
        elif key == ("bolt", "drop"):
            lines = [f"**Drop bolt `{a.bolt}`**" + (", its units back to the queue" if a.requeue else ", with its units"),
                     f"Goal: {goal_of(a.bolt)}", f"Reason: {a.reason}"]
        elif key == ("unit", "add"):
            where = bolt_line(a.bolt) if a.bolt else f"the queue of {a.repo}"
            lines = [f"**New {noun} `{a.unit}`** in {where}", f"{says}: {a.intent}"]
            if a.bolt and goal_of(a.bolt):
                lines.append(f"Bolt's goal: {goal_of(a.bolt)}")
            if getattr(a, "unblocks", None):
                lines.append(f"Unblocks: bolt `{a.unblocks}`, which can't be proven or land without it")
            if a.signal and not alone:
                assertion, excerpt, grade = signal_of(a.signal)
                lines.append(f"From: signals/{a.signal}" + (f": \"{assertion}\"" if assertion else ""))
                if excerpt:
                    lines.append(f"Excerpt" + (f" ({grade})" if grade else "") + f": {excerpt}")
            lines += [f"Source: {s}" for s in a.source]
        elif key == ("unit", "move"):
            src = next((b for b in per[i] if b != a.bolt), None)
            to = None if a.bolt == "queue" else a.bolt
            lines = [f"**Move {noun} `{a.unit}`** from {bolt_line(src) if src else 'the queue'} to {bolt_line(to) if to else 'the queue'}",
                     f"{says}: {intent_of(a.unit)}"]
            if to and goal_of(to):
                lines.append(f"Bolt's goal: {goal_of(to)}")
            if getattr(a, "unblocks", None):
                lines.append(f"Unblocks: bolt `{a.unblocks}`, which can't be proven or land without it")
        elif key == ("unit", "split"):
            lines = [f"**Split unit `{a.unit}`**", f"Narrowed intent: {a.intent}"] + [f"New unit `{n}`: {i}" for n, i in a.into]
        elif key == ("unit", "amend"):
            lines = amendment(fleet, label, plan, a, alone)
        elif key == ("unit", "order"):
            where = "first" if a.first else "last" if a.last else f"before `{a.before}`"
            lines = [f"**Order {noun} `{a.unit}`** {where}", f"{says}: {intent_of(a.unit)}"]
        elif key == ("unit", "after"):
            lines = [f"**{noun.capitalize()} `{a.unit}` comes after** " + ("nothing" if a.none else ", ".join(f"`{d}`" for d in a.deps))]
        elif key == ("unit", "drop"):
            lines = [f"**Drop {noun} `{a.unit}`**", f"{says}: {intent_of(a.unit)}", f"Reason: {a.reason}"]
        elif key == ("kit", "rename"):
            bolts, work = renamed_in(plan, a.old)
            lines = [f"**Rename kit `{a.old}`** to `{a.new}`, as its host renamed it",
                     "Bolts: " + (", ".join(f"`{b.name()}`" + (" (started)" if started(b) else "") for b in bolts) or "none"),
                     "Units and chores: " + (", ".join(f"`{u.name()}`" for u in work) or "none"),
                     "On approval: each names the kit by its new name; nothing is dropped, added or launched again."]
        changes.append({"do": a.do, "lines": lines, "bolts": per[i]})
    return {"proposal": int(p.get("Proposal")), "state": p.get("State"), "by": p.get("By"), "opened": p.get("Opened"),
            "closed": p.get("Closed"), "reason": p.get("Reason"), "replaces": p.get("Replaces"), "case": p.get("Case"),
            "changes": changes, "waits": ["the user"] if p.get("State") == "open" else []}


def code_span(text):
    """text as a markdown code span: fenced one backtick longer than its longest run of backticks, with a space inside
    each end when it starts or ends with one (CommonMark's rule)."""
    fence = "`" * (max((len(r) for r in re.findall(r"`+", text)), default=0) + 1)
    pad = " " if text[:1] == "`" or text[-1:] == "`" else ""
    return f"{fence}{pad}{text}{pad}{fence}"


def page(d, label):
    """The markdown of one proposal: each change in plain words with the command approval runs for it, and, while it is
    open, who it waits on, in words."""
    out = [f"# Proposal {d['proposal']} — {d['state']}, by {d['by']}, {d['opened']}", ""]
    if d["replaces"]:
        out += [f"Replaces proposal {d['replaces']}.", ""]
    out += [d["case"], "", "## Changes", ""]
    for i, c in enumerate(d["changes"], 1):
        first, *rest = c["lines"]
        out.append(f"{i}. {first}")
        out += [f"   {l}" for l in rest]
        out.append(f"   Runs: {code_span(c['do'] if c['do'].startswith('crew ') else 'crew ' + c['do'])}")
        out.append("")
    if d["state"] != "open":
        out += [f"Closed {d['closed']}" + (f": {d['reason']}" if d["reason"] else "") + "."]
        return "\n".join(out).rstrip() + "\n"
    out += ["## Waiting on", ""]
    out.append("- the user, to approve it or say what to change")
    return "\n".join(out) + "\n"


def open_proposals(fleet, labels, found=None):
    """Each open proposal of the labels' drives, as describe() gives it, with its label and its chain's first
    (proposal_chain), whose key its card is under. found, when given, is the plans already read, as plans() gives
    them: their tips are used, and a label it lacks is skipped."""
    rows = []
    for l in labels:
        repo, ref = state_of(fleet, l)
        if found is None:
            tip, plan = tip_of(repo, ref), None
        else:
            tip, plan = next(((t, p) for x, _, t, p in found if x == l), (None, None))
        text = show(repo, tip, "proposals.rec") if tip else None
        if not text:
            continue
        plan, pl = plan or read(repo, ref, tip), Plan(text)
        for p in pl.recs("Proposal"):
            if p.get("State") == "open":
                rows.append(dict(describe(fleet, l, plan, p), label=l, first=proposal_chain(pl, int(p.get("Proposal")))[0]))
    return rows


def plan_proposed(fleet, a):
    """crew plan proposed [<n>] [--label L] [--json] [--open]: the open proposals, or one as the user would read it.
    Reads the drives' branches only, so any host can answer. With --open, one proposal's page is written to
    ~/.local/state/crew/proposals/<label>-<n>.md on this host, replacing any earlier copy, and opened in plannotator:
    beside the caller in herdr, inline in the terminal otherwise. The file is a copy for reading; nothing reads it back."""
    why = open_refusal(a.n, a.open, a.json)
    not why or fail(why)
    label = default_label(fleet, a)
    if a.n is not None:
        label = label or proposal_label(fleet, a, a.n)
        w, _, p, _ = at_tip(fleet, label, a.n)
        d = describe(fleet, label, w.plan, p)
        if a.open:
            f = pathlib.Path.home() / ".local/state/crew/proposals" / f"{label}-{a.n}.md"
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(page(d, label))
            argv = ["plannotator-tui", "herdr", "open", str(f)] if os.environ.get("HERDR_ENV") == "1" else ["plannotator-tui", str(f)]
            try:
                sys.exit(subprocess.run(argv).returncode)
            except FileNotFoundError:
                fail(f"plannotator-tui is not on this host's path; the proposal is written to {f}")
        print(json.dumps(d, indent=1) if a.json else page(d, label), end="" if not a.json else "\n")
        return
    rows = [dict(d, waits=["the user"])
            for d in open_proposals(fleet, [label] if label else list(fleet["drives"]))]
    if a.json:
        print(json.dumps(rows, indent=1))
        return
    if not rows:
        print("no proposal is open" + (f" in {label}" if label else ""))
        return
    for r in rows:
        print(f"{r['label']} {r['proposal']:<3} {r['by']:<24} {r['opened']}  {r['case'].splitlines()[0][:70]}  waiting on "
              + ", then ".join(r["waits"]))


def open_refusal(n, open_, as_json):
    """Why crew plan proposed refuses --open: it opens one proposal, by its number, and prints no JSON beside it."""
    if open_ and n is None:
        return "--open needs a proposal's number: crew plan proposed <n> --open"
    if open_ and as_json:
        return "--open shows the proposal in plannotator and --json prints it: use one"
    return None


# ------------------------------------------------------------------------------------------- a proposal's card

def concerns(a):
    """The unit a proposal's command concerns, its subject, or None for a bolt's or a kit's command."""
    return None if a.cmd in ("bolt", "kit") else a.unit


def names_units(a):
    """Every unit a proposal's command names: its subject and each unit it refers to."""
    if a.cmd in ("bolt", "kit"):
        return []
    out = [a.unit] + list(getattr(a, "after", None) or []) + ([a.before] if getattr(a, "before", None) else [])
    out += [n for n, _ in getattr(a, "into", None) or []] + list(getattr(a, "deps", None) or [])
    return list(dict.fromkeys(out))


def kept(argvs, cleared, n):
    """Proposal n's commands the user kept, the cleared units left out (plan.3): each cleared unit must be one the
    proposal makes new to a bolt; every command that concerns only a cleared unit is left out; a command left in that
    names one refuses the whole, so the planner writes the proposal again without it."""
    new = new_units(argvs)
    wrong = [u for u in cleared if u not in new]
    not wrong or fail(f"proposal {n} neither adds nor moves into a bolt {either(wrong)}, so the user can't leave "
                      + ("it" if len(wrong) == 1 else "them") + " out: "
                      + (f"the units it may leave out are {either(new)}" if new else "it makes no unit new to a bolt"))
    out = []
    for a in argvs:
        if concerns(a) in cleared:
            continue
        hit = [u for u in names_units(a) if u in cleared]
        if hit:
            refuse(f"`{a.do}` names {either(hit)}, which the user left out: write the proposal again without "
                   + ("it" if len(hit) == 1 else "them"), f"`{do_named(a)}` names {either(hit)}, which the user left out")
        out.append(a)
    return out


def approved_words(applied, cleared):
    """What an approval did, as the proposal's card is closed with it and the planner told (record 0031 §1): what was
    added, dropped and amended, with a count of the rest, then the new units the user left out."""
    def units(subs, xs):
        return [a.unit for a in xs if a.cmd in ("unit", "chore") and a.sub in subs]
    added, dropped, amended = new_units(applied), units(("drop",), applied), units(("amend",), applied)
    rows = [a for a in applied if a.cmd in ("unit", "chore") and (a.sub in ("drop", "amend") or a.sub in ("add", "move") and a.unit in added)]
    rest = len(applied) - len(rows)
    did = ([f"added {joined(added)}"] if added else []) + ([f"dropped {joined(dropped)}"] if dropped else []) \
        + ([f"amended {joined(amended)}"] if amended else []) + ([cards.plural(rest, "other change")] if rest else [])
    said = [("Applied: " + "; ".join(did) + ".") if did else "Nothing applied."]
    said += [f"Left out on your word: {joined(cleared)}."] if cleared else []
    return " ".join(said)


def answers_file(label, n):
    return CARDS / label / "proposal" / str(n) / "answers.json"


def held_answers(f):
    """The answers gathered for a proposal's card, {} when none; refused when crew can't read them (read.1)."""
    try:
        held = json.loads(f.read_text())
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        fail(f"crew can't read the answers it gathered, {f}: {e}")
    return held if isinstance(held, dict) else fail(f"{f} holds no answers crew gathered")


def plan_answer(fleet, a):
    """crew plan answer <n> <question> <answer>... [--note "<text>"] [--label L]: one question of open proposal n's card
    answered, as the planner reads it from the card: rows-<k> and the ids of the boxes the user left ticked (none when
    every one is cleared; rows-1 for a card of one list, and for a lone new unit the side the user picked), or, for a
    hold-to-approve, plan approve or decline. It is checked against the card crew builds for the proposal now
    (proposal_facts, cards.proposal_card), and kept on this host, the planner's, beside the card's session files: a
    card's working state, never the plan's (state.2). Once it holds every question's answer, the change is applied with
    the boxes as they stand, as crew plan approve applies it, and the answers go: a new unit unticked left out; a note
    beside it is then printed as the user's word for the planner's next proposal. A decline applies nothing, and its
    answers go. Refused for a question the card does not ask, a box its question does not hold, an answer that differs
    from the one held, and a closed proposal, recording nothing."""
    label = proposal_label(fleet, a, a.n)
    CONTEXT["label"] = label
    w, _, p, _ = at_tip(fleet, label, a.n)
    b = cards.proposal_card(proposal_facts(fleet, label, w, a.n))
    asks = card_asks(b["card"])
    answer = card_answer(asks, b["card"].get("kind") == "choice", a.n, a.question, a.answer)
    f = answers_file(label, a.n)
    f.parent.mkdir(parents=True, exist_ok=True)
    with open(f.parent / ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        held = with_answer(held_answers(f), a.n, a.question, answer, a.note)
        tmp = f.parent / ".answers.json"
        tmp.write_text(json.dumps(held, indent=1) + "\n")
        tmp.replace(f)
        note = held.get("note")
        if held.get("plan") == "decline":
            f.unlink()
            print(f"proposal {a.n} is declined: nothing is applied, and the answers crew gathered are gone. The decline"
                  + (f", and the user's note beside it, \"{note}\"," if note else "") + " is the user's word for you to act on: "
                  f"write the proposal again with crew plan propose <file> --replaces {a.n}, or drop it with "
                  f"crew plan drop {a.n} \"<the user's reason>\".")
            return
        waits, cleared = answered(asks, held, b["boxes"])
        if waits:
            print(f"proposal {a.n} waits on {either(waits)}: nothing is applied")
            return
        approval = argparse.Namespace(cmd="plan", sub="approve", n=a.n, label=label, clear=cleared)
        try:
            plan_approve(fleet, approval)
        except Refusal as e:
            refused(fleet, approval, ("plan", "approve"), e)
            raise
        f.unlink()
    if note:
        print(f"The user's note beside the approval of proposal {a.n}: \"{note}\". Propose what it asks as a new proposal.")


def card_asks(card):
    """The questions a proposal's card crew built asks, as crew plan answer takes their answers, each with the ids of
    its boxes: plan, approve or decline, for a hold-to-approve; else rows-<k> for each list of boxes, rows-1 for a card
    of one list or a lone new unit's choice of its two sides."""
    if card.get("kind") == "approve":
        return {"plan": None}
    if card.get("questions"):
        return {q["id"]: [o["id"] for o in q["options"]] for q in card["questions"]}
    return {"rows-1": [o["id"] for o in card["options"]]}


def card_answer(asks, lone, n, question, given):
    """One question of proposal n's card answered, checked against the questions the card asks now (asks, each
    question's box ids): plan, approve or decline; a lone new unit's, the one side the user picked; rows-<k>, the boxes
    the user left ticked of those it holds. Returns the answer as kept."""
    question in asks or fail(f"proposal {n}'s card asks {either(list(asks))}, not {question}")
    given, boxes = list(dict.fromkeys(given)), asks[question]
    if question == "plan":
        len(given) == 1 and given[0] in ("approve", "decline") or fail("plan is answered approve or decline")
        return given[0]
    if lone:
        len(given) == 1 and given[0] in boxes or fail(f"{question} is answered {either(boxes)}")
        return given
    bad = [x for x in given if x not in boxes]
    not bad or fail(f"{question} holds {either(boxes)}, not {either(bad)}")
    return given


def with_answer(held, n, question, answer, note=None):
    """The answers held for proposal n's card with one more: the same answer again is fine, a different one refused,
    and a note joins the notes held, once."""
    if question in held:
        was = held[question]
        same = was == answer if question == "plan" else sorted(was) == sorted(answer)
        words = was if isinstance(was, str) else " ".join(was) or "nothing ticked"
        same or fail(f"crew already holds {question} {words} for proposal {n}: the user answered it once")
    held = dict(held)
    held.setdefault(question, answer)
    if note and note.strip() and note.strip() not in held.get("note", ""):
        held["note"] = (held.get("note", "") + "\n\n" + note.strip()).strip()
    return held


def answered(asks, held, boxes):
    """What the answers held say once a card's questions are read (record 0031 §5): the questions still unanswered,
    and, once none is, the new units the user cleared, each one's box left unticked. A hold-to-approve leaves none out,
    the boxes of one that links its reading session standing as proposed."""
    waits = [q for q in asks if q not in held]
    if waits or "plan" in asks:
        return waits, []
    picked = {x for q in asks for x in held[q]}
    return [], [b["unit"] for b in boxes if b["id"] not in picked]


def proposal_facts(fleet, label, w, n):
    """What proposal n's card is built from (record 0031 §5), as card_model reads it, from the write w as it left the
    branch and no kit (plan.12): the plan at the tip and as the proposal's commands leave it, applied to a copy as
    check_ops applies them; the proposal's number, state, case and commands, parsed; its chain's first, whose key the
    card is under; and no reading session. A closed proposal's facts hold
    no plan after it, and the builder refuses them."""
    pl = proposals(w)
    p = proposal(pl, n, label)
    argvs = [do_args(label, d) for d in p.all("Do")]
    after = check_ops(fleet, label, w, argvs, n, Drawn).plan if p.get("State") == "open" else w.plan
    return dict(n=n, first=proposal_chain(pl, n)[0], state=p.get("State"), case=p.get("Case"), before=w.plan,
                after=after, argvs=argvs, session=None)


def named_kit(plan, argvs):
    """The kit of the first bolt or unit a proposal's commands name, in whose area its card is filed (briefs.11): a new
    bolt's, or a unit's added to the queue, as the command gives it, a kit's rename's new name, else the plan's for the
    bolt or unit it names; None when the plan names none of them."""
    for a in argvs:
        if a.cmd == "bolt":
            b = plan.bolt(a.bolt)
            repo = a.repo if a.sub == "new" else b.get("Repo") if b else None
        elif a.cmd == "kit":
            repo = a.new
        elif a.sub == "add":
            repo = a.repo or (plan.bolt(a.bolt).get("Repo") if a.bolt and plan.bolt(a.bolt) else None)
        else:
            repo = plan.item(a.unit).get("Repo") if plan.item(a.unit) else None
        if repo:
            return repo
    return None


def chain_open(pl, first):
    """The open proposal of the chain whose card is keyed proposal/<first>, in proposals.rec (pl): its number, or None
    when the chain has none open, its last one approved or dropped."""
    return next((int(p.get("Proposal")) for p in pl.recs("Proposal") if p.get("State") == "open"
                 and proposal_chain(pl, int(p.get("Proposal")))[0] == first), None)


SWEPT = "Raised again as the plan stands"  # the change note of a proposal's card the rail's sweep raises
# The outcome a dropped proposal's card is acked with once the user answered it: their note, the drop's reason, may ask
# them something, which Pending You refuses as an outcome (proposal 161's drop on 2026-10-19: "Your outcome asks your
# person something; put it on a new card with follows instead."), so the reason stays on the proposal's record.
DROPPED = "Dropped on your note, nothing of it applied"


def proposal_act(event, n, mine, was_mine=False, held=True, home=True, outcome=None, reason=None, by=None):
    """Which act proposal n's card takes at its event (record 0031 §1), from facts alone: ("post",) when it is
    accepted, ("change", note) when it is rewritten (replace), the rail's sweep finds its card
    missing or lost (sweep), or its reading opens after the card was raised without it (relink, reading_again),
    ("close", outcome, reason) when it is approved, or dropped, its card acked with DROPPED
    once the user answered it and withdrawn with the reason while it waits, or None when it has no card of
    crew's. mine, whether the planner wrote it, the card's owner, whose proposals alone crew raises a card for;
    was_mine, at a rewrite, whether the planner wrote the one it replaces, whose card a rewrite of anyone else's
    withdraws. A change is made only where its card was posted, held on this host, or on the planner's own (home),
    where it is posted when none is held: elsewhere it is ("skip",), since a card is reached only from the host that
    posted it. The sweep runs only on the planner's host."""
    if event == "replace" and not mine:
        return ("close", None, f"Rewritten by {by} as proposal {n}, which has no card") if was_mine else None
    if not mine:
        return None
    if event == "propose":
        return ("post",)
    if event == "sweep":
        return ("change", SWEPT)
    if event == "relink":
        return ("change", RELINKED)
    if event == "replace":
        if not held and not home:
            return ("skip",)
        return ("change", f"Rewritten as proposal {n} after your note")
    return ("close", outcome, None) if event == "approve" else ("close", DROPPED, reason)


def chain_closed(pl, first):
    """How the chain keyed proposal/<first> stands closed in proposals.rec (pl), in row_gone's words, as its card is
    closed once the plan shows it so (raise_proposal): (outcome, None) when its last proposal was approved, its card
    closed as applied; (None, reason) when it was dropped, its card withdrawn; None while a proposal of it is open, and
    for a chain pl holds no proposal of."""
    chain = [p for p in pl.recs("Proposal") if proposal_chain(pl, int(p.get("Proposal")))[0] == first]
    if not chain or any(p.get("State") == "open" for p in chain):
        return None
    last = max(chain, key=lambda p: int(p.get("Proposal")))
    return ("its proposal was applied", None) if last.get("State") == "approved" else (None, "its proposal was dropped")


def tip_write(fleet, label, fresh=False):
    """The drive's branch at its tip, as a write; with fresh, the tip fetched anew, the plan as it stands and not
    as this command first read it (fetch). None when the branch has no tip."""
    repo, ref = state_of(fleet, label)
    tip = tip_of(repo, ref, fresh)
    return Write(repo, label, tip, read(repo, ref, tip)) if tip else None


def chain_read(fleet, label, first):
    """The open proposal of the chain keyed proposal/<first>, read at the branch's tip: (w, n), the write as the tip
    holds it and the proposal's number; None when the branch has no tip or the chain has no proposal open."""
    w = tip_write(fleet, label)
    n = chain_open(proposals(w), first) if w else None
    return (w, n) if n is not None else None


def raise_proposal(fleet, row, acts=None, event="sweep"):
    """The rail's sweep's raise of a proposal row's card (record 0031 §1), for a row whose card is missing or lost:
    the open proposal of the chain its key names, read at the branch's tip from the row's label and key, fetched anew
    at the sweep (tip_write), raised through row_card_change, which posts it when none is held and posts it again, its
    summary saying the older copy is dead, when Pending You no longer finds it, and when the sweep hands it the older
    copy this host can't reach as the row's dead; or, with event relink, its card changed to carry its reading's link
    (reading_again). The rail's read of the plan can be older than an approval or a drop its run record already holds
    (wldn's proposal 538 on 2026-10-23, approved at 9b8c8c1 and its card closed, then posted again by the sweep 15 s
    after on the read's tip, signal 2026-10-23-swancloud-planner-727dc1ea/01), so the sweep's raise fetches the tip
    again, the one fetch of the state branch past a command's first (plan.12), made only for a card about to be posted:
    a chain the plan as it stands shows approved or dropped raises none, and a card the planner still holds open under
    its key on this host is closed as one whose row is gone (chain_closed), so the user is not asked what was answered.
    None, raising nothing, when the key is no proposal chain's or the chain has no proposal open. The card's id, or
    None."""
    label, m = row["label"], re.fullmatch(r"proposal/(\d+)", row.get("key") or "")
    w = tip_write(fleet, label, fresh=event == "sweep") if m else None
    pl = proposals(w) if w else None
    n = chain_open(pl, int(m.group(1))) if pl else None
    if n is not None:
        return raise_proposal_at(fleet, label, w, n, event, acts, dead=bool(row.get("dead")))
    closed = chain_closed(pl, int(m.group(1))) if pl and event == "sweep" else None
    if closed:
        acts, owner = acts or CardActs(fleet), f"{label}-planner"
        print(f"card {row['key']} not raised: {closed[0] or closed[1]}, as the plan stands")
        if cards.card_under(acts.entries(label), row["key"], owner):
            row_card_close(fleet, label, owner, row["key"], *closed, acts=acts)
    return None


def raise_proposal_at(fleet, label, w, n, event, acts=None, outcome=None, reason=None, dead=False):
    """Proposal n's card at its event (record 0031 §1, briefs.11), once the event's write is made (code.9), from the
    write w as it left the branch: the act proposal_act decides; the card built by the proposal's builder from
    proposal_facts, and posted, changed or closed by the act in the planner's name under its chain's key,
    proposal/<first>, filed in the area of the kit of the first bolt or unit its commands name. A rewrite whose card
    takes another form than the replaced proposal's (cards.proposal_form: a hold-to-approve, a choice, one list or
    lists), which update_request never changes, has the card followed as a card whose kind changed; a rewrite asks
    anew, and follows a card the user answered, where the sweep's raise leaves it as it is, its answer
    going on to the approval (row_card_change); the card that follows says what the rewrite changed against the
    proposal it replaces (cards.proposal_since), and one that changes neither its commands nor its case is withheld,
    the user's answer standing (card_posted). With dead, an older copy this host can't reach standing, the card is
    built saying first that it was lost (built_again). A card crew cannot build, or Pending You refuses, refuses
    nothing of the proposal: it is said, and the rail shows the row with no card. The card's id, or None."""
    acts = acts or CardActs(fleet)
    owner, part = f"{label}-planner", crew.drive_of(fleet, label)
    pl = proposals(w)
    p = proposal(pl, n, label)
    replaced = proposal(pl, int(p.get("Replaces")), label) if (p.get("Replaces") or "").isdigit() else None
    was = replaced.get("By") if replaced else None
    key = f"proposal/{proposal_chain(pl, n)[0]}"
    near = event == "replace"
    act = proposal_act(event, n, p.get("By") == owner, was == owner,
                       held=near and cards.card_under(acts.entries(label), key, owner) is not None,
                       home=acts.host() == part["machine"], outcome=outcome, reason=reason, by=p.get("By"))
    if act is None:
        return None
    if act[0] == "skip":
        print(f"card {key} not changed here: {owner} holds it on {part['machine']}, and {acts.host()} holds none")
        return None
    try:
        if act[0] == "close":
            return row_card_close(fleet, label, owner, key, outcome=act[1], reason=act[2], acts=acts)
        facts = proposal_facts(fleet, label, w, n)
        kit_ = named_kit(w.plan, facts["argvs"])
        try:  # where the kit's work runs, from the runners and requests the write read at its tip
            t = kit_at(fleet, label, kit_, (Plan(w.text("requests.rec") or runner.REQUESTS).recs("Request"),
                                            w.runners())) if kit_ else None
        except Refusal:
            t = None
        where = card_where(card_kit(fleet, t, kit_, {"main": part["checkout"], "repo": part["blueprints"][0]}))
        build = built_again(cards.proposal_card) if dead else cards.proposal_card
        if act[0] == "post":
            return row_card_post(fleet, label, owner, build, facts, where, acts)
        old = [do_args(label, d) for d in replaced.all("Do")] if event == "replace" and replaced is not None else None
        moved = old is not None and cards.proposal_form(old) != cards.proposal_form(facts["argvs"])
        since = cards.proposal_since(old, replaced.get("Case"), facts["argvs"], facts["case"]) if old is not None else None
        return row_card_change(fleet, label, owner, build, facts, act[1], where, acts, kind_changed=moved,
                               anew={} if event == "replace" else None,
                               since=[f"The planner rewrote it as proposal {n}."] + since if since else since)
    except Refusal as e:
        print(f"card {key} not raised: {e}", file=sys.stderr)
        return None


# -------------------------------------------------------------------------------------------------- signals

SHORT_ID = re.compile(r"^[^/]+/[0-9]{2}$")  # a signal's short id, <capture>/<NN>: its full id without the slug


def signal_at(fleet, label, sig, w=None):
    """Where a signal is: signals/<id>.md on the drive's branch (as the write w has it, else at the branch's tip),
    else on main of the drive's first blueprints repo, where the daily pass writes meetings' and channels'. sig is
    its full id, <capture>/<NN>-<slug>, or its short form, <capture>/<NN>, which names the one signal of that capture
    numbered NN. (where, repo, tip, the signal's text, its full id), or None when it is in neither."""
    if w is not None:
        repo, ref, tip = w.repo, f"{label}/main", w.tip
    else:
        repo, ref = state_of(fleet, label)
        tip = tip_of(repo, ref)
    hit = signal_in(repo, tip, sig, w) if tip or w is not None else None
    if hit:
        return ref, repo, tip, *hit
    srepo = crew.drive_of(fleet, label)["blueprints"][0]
    tip = tip_of(srepo, "main")
    hit = signal_in(srepo, tip, sig) if tip else None
    return ("main", srepo, tip, *hit) if hit else None


def signal_in(repo, tip, sig, w=None):
    """A signal's (text, full id) in the repo at tip, as the write w has it when given; None when it is not there. A
    short id is looked for among the files of its capture's folder."""
    if SHORT_ID.match(sig):
        cap = sig.split("/")[0]
        listed = git(repo, "ls-tree", "--name-only", f"{tip}:signals/{cap}", check=False) if tip else None
        names = (listed.stdout.split() if listed and listed.returncode == 0 else []) + [
            p.rsplit("/", 1)[1] for p in (w.files if w is not None else ()) if p.startswith(f"signals/{cap}/")]
        sig = signal_named(sig, names)
        if sig is None:
            return None
    path = f"signals/{sig}.md"
    text = w.text(path) if w is not None else show(repo, tip, path)
    return (text, sig) if text is not None else None


def signal_named(sig, names):
    """The full id a short id, <capture>/<NN>, names, from the file names in its capture's folder: the one signal
    numbered NN, <capture>/<NN>-<slug>. None when the capture has none; refused when it has more than one, since
    nothing says which (read.1)."""
    cap, n = sig.split("/")
    hits = sorted({f"{cap}/{x[:-3]}" for x in names if SIGNAL_FILE.match(x) and x.startswith(f"{n}-")})
    len(hits) < 2 or fail(f"signal {sig} names {len(hits)} signals: {', '.join(hits)}; give the full id of one")
    return hits[0] if hits else None


def signal_id(fleet, label, sig, w=None):
    """A signal's full id: a full id as it is, a short one as signal_at finds it (in the write w, when given), refused
    when it is in neither home."""
    return sig if not SHORT_ID.match(sig) else (signal_at(fleet, label, sig, w) or no_signal(fleet, label, sig))[4]


def no_signal(fleet, label, sig):
    cap, _, n = sig.rpartition("/")
    fail(f"no signal {sig} on {label}/main of {state_of(fleet, label)[0]} or on main of "
         f"{crew.drive_of(fleet, label)['blueprints'][0]}: "
         + (f"signals/{cap}/ holds no {n}-<slug>.md in either" if SHORT_ID.match(sig) else f"signals/{sig}.md is in neither"))


def frontmatter(text):
    """The fields of a markdown file's frontmatter, [(name, value)] in order; none when it has none."""
    m = re.match(r"^---\n(.*?)\n---\n", text or "", re.S)
    return [tuple(l.split(": ", 1)) if ": " in l else (l.rstrip(":"), "") for l in m.group(1).splitlines() if l.strip()] if m else []


def field(text, name):
    return next((v for k, v in frontmatter(text) if k == name), None)


def capture_of(sig):
    """A signal's capture, signals/<capture>/capture.md, from its id <capture>/<NN>-<slug>."""
    return f"signals/{sig.rsplit('/', 1)[0]}/capture.md"


def move(fleet, label, w, sig, rec):
    """A signal's one move, appended to the drive's moves.rec in the write w: refused when the signal is in
    neither of its homes, or already has its move. recfix checks the file before the commit, so a move the file's
    schema refuses writes nothing."""
    signal_at(fleet, label, sig, w) or no_signal(fleet, label, sig)
    moves = w.text("moves.rec")
    moves is not None or fail(f"{label}/main of {w.repo} has no moves.rec: crew state init {label}")
    unmoved(moves, sig)
    w.replace("moves.rec", moves.rstrip("\n") + "\n\n" + "\n".join(rec.lines()) + "\n")


def unmoved(text, sig):
    moved = [m for m in Plan(text).recs("Move") if m.get("Signal") == sig]
    not moved or fail(f"signal {sig} already has its move: {moved[0].get('Move')}")


def route_move(sig, target):
    """A signal's route move to the work that takes it, its target that work's object, unit/<unit> or chore/<chore>."""
    return Rec("Move", [("Signal", sig), ("Move", "route"), ("Target", target if "/" in target else f"unit/{target}"),
                        ("Date", datetime.date.today().isoformat()), ("By", agent())])


CURATION = ("attach", "challenge", "new-territory", "answered", "drop")
KINDS = ("constraint", "ask", "question", "commitment", "reaction")


def signal_move(fleet, a):
    """Curation's five moves, each written through crew the way the route is: one move per signal, appended to
    moves.rec on the drive's branch of its state repository, never merged. A short id is moved by its full one."""
    label = default_label(fleet, a) or fail("which drive's signals? add --label " + "|".join(fleet["drives"]))
    a.signal = signal_id(fleet, label, a.signal)
    rec, on = curation_move(a.signal, a.move, a.target, a.reason, datetime.date.today().isoformat(), agent())
    write(fleet, label, lambda w: move(fleet, label, w, a.signal, rec), f"signals({a.signal}): {a.move}", act="signal.move", on=on)


def curation_move(sig, kind, target, reason, today, by):
    """A curation move's record, and the objects its run-record entry names: the signal, and its target when that is a
    pointer, a typed name such as unit/<unit> or a path, never words that could be typed text. Refused when an attach,
    a challenge or an answered names no target, or a drop gives no reason."""
    kind not in ("attach", "challenge", "answered") or target or fail(
        f"a {kind} move names its target (--target): the intent, claim or record it " + {"attach": "lands on", "challenge": "argues with", "answered": "was settled by"}[kind])
    kind != "drop" or reason or fail("a drop gives its reason (--reason)")
    rec = Rec("Move", [("Signal", sig), ("Move", kind)] + ([("Target", target)] if target else [])
              + ([("Reason", reason)] if reason else []) + [("Date", today), ("By", by)])
    return rec, [f"signals/{sig}"] + ([target] if target and re.fullmatch(r"[a-z]+/[^\s]+", target) else [])


class Already(Exception):
    """The signal is recorded already, in its capture: nothing is written, and its id is said."""


def dashed(s):
    """A name as a directory's part: lowercase, any other characters a dash."""
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def sha16(text):
    import hashlib
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def quoted(excerpt, position):
    """The excerpt as a signal quotes it: a blockquote of the words, verbatim, then its position."""
    return "\n".join(f"> {l}" if l else ">" for l in f'"{excerpt}" — {position}'.split("\n"))


def where_of(fleet, name, plan):
    """Where an agent was working, read without asking it: the main level for a main-level role; None for an agent crew
    has no role for."""
    kind, _ = role(fleet, name)
    return "main level" if kind in ("planner", "design", "main-ops", "operator") else None


def bank(path, line):
    """The source record appended to the host's raw file for its capture, outside git, unless it is there already."""
    try:
        if path.exists() and line in path.read_bytes().split(b"\n"):
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "ab") as f:
            f.write(line + b"\n")
    except OSError as e:
        fail(f"the source record could not be banked at {path}: {e.strerror or e}")


def signal(fleet, a):
    """A finding, as a capture and its signal under signals/ on the drive's branch, in the shape the blueprints'
    signals/README.md gives. An agent quotes the words that show it, which are looked for in its own Claude transcript
    and graded (transcript.py), and a paraphrase is refused. Its capture is the one record that holds the excerpt,
    copied to this host's raw/ outside git; a second signal from that record joins the capture, and the same signal
    again writes nothing. The user's note at a shell is its own excerpt. One write, one commit."""
    label = default_label(fleet, a) or fail("which drive's signals? add --label " + "|".join(fleet["drives"]))
    signal_refusal(a.slug, a.asserts) and fail(signal_refusal(a.slug, a.asserts))
    name, host = crew.caller(fleet), crew.this_host()
    now = datetime.datetime.now(datetime.timezone.utc)
    excerpt = a.excerpt
    if a.excerpt_file:
        try:
            excerpt = pathlib.Path(a.excerpt_file).read_text()
        except (OSError, UnicodeDecodeError) as e:
            fail(f"cannot read the excerpt from {a.excerpt_file}: {getattr(e, 'strerror', None) or e}")
    v = sid = user = None
    if name:
        excerpt = (excerpt or "").strip()
        excerpt or fail('a signal quotes the words that show it: add --excerpt "<the exact words the user said or the '
                        'tool printed>", or --excerpt-file <path>')
        v, sid = check_excerpt(fleet, name, a, excerpt, host)
        excerpt_refusal(v) and fail(excerpt_refusal(v))
    else:
        import getpass
        excerpt, user = (excerpt or a.asserts).strip(), getpass.getuser()
    by = agent()
    key, cap, date, who, position, kind = capture_named(name, v, sid, excerpt, now, a.kind, user, host, by)
    # An id is unique across both homes, so it is looked up in either without asking which.
    srepo = crew.drive_of(fleet, label)["blueprints"][0]
    btip = tip_of(srepo, "main")
    not (btip and git(srepo, "ls-tree", "--name-only", btip, f"signals/{cap}")) or fail(
        f"{srepo} has signals/{cap} already, so a capture can't take that name")
    raw = None
    if v and v.grade != "unverified":
        bank(record.ROOT / label / "raw" / f"{cap}.jsonl", v.raw)
        raw = f"{host}:~/.local/state/crew/{label}/raw/{cap}.jsonl"
    quote = quoted(excerpt, position)
    seen = {}

    def change(w):
        cpath = f"signals/{cap}/capture.md"
        have = w.text(cpath)
        names = []
        if have is not None:
            listed = git(w.repo, "ls-tree", "--name-only", f"{w.tip}:signals/{cap}", check=False)
            names = listed.stdout.split() if listed.returncode == 0 else []
        nn, count = signal_number(have, key, cap, label, names, a.slug, quote, lambda n: w.text(f"signals/{cap}/{n}"))
        sig = f"{cap}/{nn:02d}-{a.slug}"
        if have is None:
            have = capture_text(fleet, name, host, v, sid, key, cap, date, now, raw, w.plan, by)
        w.replace(cpath, re.sub(r"(?m)^signals: [0-9]+$", f"signals: {count}", have, count=1))
        w.replace(f"signals/{sig}.md", signal_md(sig, kind, who, a.subject, a.asserts, quote))
        w.subject = f"signals({sig}): {a.slug}"
        w.on.append(f"signals/{sig}")
        capture_asks(w, fleet, label, [sig])
        seen["id"] = sig
        return []
    try:
        write(fleet, label, change, f"signals: {a.slug}", act="capture")
    except Already as e:
        print(f"signal {e} is recorded already; nothing was written")
        return
    print(signal_said(seen["id"], v))


def signal_refusal(slug, asserts):
    """Why crew signal refuses a signal before reading anything, or None: its slug is a name and not a subcommand's,
    and it says what it asserts."""
    if not crew.NAME.match(slug):
        return f"a signal's slug is lowercase words with dashes, not {slug}"
    if slug in ("move", "show", "land"):
        return f"a signal's slug can't be '{slug}'"
    if not asserts.strip():
        return "a signal says what it asserts, in a sentence"
    return None


def excerpt_refusal(v):
    """Why crew signal refuses an agent's excerpt on its verdict v, or None: the words are not in the session's
    transcript, reworded or a background task's output the agent has not read yet (signals.2)."""
    if v.grade != "refused":
        return None
    return ("the excerpt is not in your session's transcript: quote the words as you received them, from the user or "
            "from a tool's output. A background task's output reaches your transcript only once you read the output file "
            "its task notification names: read that file, then record the signal again")


def capture_named(name, v, sid, excerpt, now, kind=None, user=None, host=None, by=None):
    """The capture a signal goes in, and how it quotes its excerpt: (key, capture name, date, who asserted it, the
    quote's position, kind). An agent's (name) by the verdict v on its excerpt in session sid: a received record by its
    uuid, any other line by its hash, an unchecked excerpt by its own, dated by the record's time where it has one,
    asserted by whom the verdict says, the agent itself for a tool's output; kind constraint unless given. The user's
    note at a shell (no name), by user, at host, recorded by by: its own excerpt, by its hash, kind ask unless given."""
    if not name:
        h = sha16(excerpt)
        date = now.date().isoformat()
        return f"operator/{by}/{h}", f"{date}-{dashed(user)}-{dashed(host)}-{h[:8]}", date, "user", now.strftime("%H:%M:%SZ"), kind or "ask"
    when = transcript.stamp(v.at) if v.grade == "verified" else None
    date = (transcript.stamp(v.at) or now).date().isoformat()
    rid = re.sub(r"[^a-z0-9]", "", (v.uuid or "").lower()) if v.grade == "verified" else ""
    if v.grade == "unverified":
        h = sha16(excerpt)
        key, part = f"unverified/{name}/{h}", h[:8]
    elif rid:
        key, part = f"session/{sid}/{v.uuid}", rid[:8]
    else:
        h = v.line_hash()[:16]
        key, part = f"session/{sid}/line-{h}", h[:8]
    who = {"user": "user", "crew": "crew"}.get(v.asserted_by) or (v.asserted_by[6:] if v.asserted_by.startswith("agent:") else name)
    position = "unverified" if v.grade == "unverified" else when.strftime("%H:%M:%SZ") if when else f"line {v.n}"
    return key, f"{date}-{dashed(name)}-{part}", date, who, position, kind or "constraint"


def signal_number(have, key, cap, label, names, slug, quote, text_of):
    """The number a signal takes in its capture, and how many signals the capture then holds: 1 and 1 in a capture
    not yet written (have is None); else one past the highest of the capture's signals (names, the files in its
    folder), refused when the capture there is another's (its key), and Already when one of them is this signal, by
    its slug and its quote (text_of(name), read only then)."""
    if have is None:
        return 1, 1
    field(have, "key") == key or fail(f"signals/{cap} on {label}/main is another capture ({field(have, 'key')}), not {key}")
    names = [n for n in names if re.match(r"^[0-9]{2}-.*\.md$", n)]
    for n in names:
        if n[3:-3] == slug and quote in (text_of(n) or ""):
            raise Already(f"{cap}/{n[:-3]}")
    return 1 + max([int(n[:2]) for n in names] or [0]), len(names) + 1


def signal_md(sig, kind, who, subject, asserts, quote):
    """A signal's file: its frontmatter, what it asserts, and its quote; subject, as typed, a comma-separated list."""
    subject = "[" + ", ".join(x.strip() for x in subject.split(",") if x.strip()) + "]" if subject else None
    return ("---\n" + f"signal: {sig}\nkind: {kind}\nwho: {who}\n" + (f"subject: {subject}\n" if subject else "")
            + "---\n\n" + asserts.strip() + "\n\n" + quote + "\n")


def signal_said(sig, v):
    """What crew signal says once the signal is written: its id and its excerpt's grade, own for the user's note,
    with who asserted a verified one and why one is unverified."""
    grade = "own" if v is None else v.grade
    return (f"signal {sig}: excerpt {grade}" + (f", asserted by {v.asserted_by}" if v and v.grade == "verified" else "")
            + (f" ({v.reason})" if v and v.grade == "unverified" else ""))


def check_excerpt(fleet, name, a, excerpt, host):
    """The agent's excerpt checked against its own Claude session's transcript, which is on this host: crew signal
    is never run on another. The session is the one a forwarded command carries, else herdr's for the agent. Returns
    the verdict and the session id."""
    sid, elsewhere = session_here(record.session(), host)
    if elsewhere:
        return transcript.unverified(elsewhere), sid
    skip = [a.excerpt_file, str(pathlib.Path(a.excerpt_file).resolve())] if a.excerpt_file else []
    return transcript.check(sid, excerpt, skip), sid


def session_here(sess, host):
    """The session a signal's excerpt is checked in, from the caller's <host>:<id>, and why it can't be read on this
    host, or None: a session on another host is not."""
    shost, sid = sess.split(":", 1) if sess and ":" in sess else (host, sess)
    return sid, (f"session {sid} is on {shost}, not {host}" if sid and shost != host else None)


def capture_text(fleet, name, host, v, sid, key, cap, date, now, raw, plan, by=None):
    """A new capture.md: where its excerpt came from and how well crew could check it, with the count of its signals,
    which each signal that joins it rewrites. The user's note (v None) is captured by by, the user at this host."""
    today = now.date().isoformat()
    if v is None:
        fields = [("capture", cap), ("source", "operator"), ("key", key), ("captured_by", by), ("host", host),
                  ("excerpt", "own"), ("asserted_by", "user")]
        title, body = f"{by}, {date}", "The user's own note, recorded with crew signal at a shell."
    else:
        when = transcript.stamp(v.at) if v.grade != "unverified" else None
        record_name = None if v.grade == "unverified" else v.uuid or f"line {v.n}"
        fields = [("capture", cap), ("source", "crew-session"), ("key", key), ("captured_by", name), ("host", host),
                  ("session", sid), ("record", record_name), ("at", when.strftime("%Y-%m-%dT%H:%M:%SZ") if when else None),
                  ("excerpt", v.grade), ("unverified", v.reason), ("asserted_by", v.asserted_by),
                  ("where", where_of(fleet, name, plan)), ("raw", raw)]
        title = f"{name}, {date}" + (f" {when.strftime('%H:%M')}Z" if when else "")
        body = (f"Words {name} quoted, captured with crew signal; crew could not check them against its session."
                if v.grade == "unverified" else f"One record of {name}'s session, captured with crew signal.")
    fields += [("event_date", date), ("imported", today), ("status", "read"), ("signals", "1")]
    return "---\n" + "".join(f"{k}: {x}\n" for k, x in fields if x not in (None, "")) + f"---\n\n# {title}\n\n{body}\n"


SIGNAL_FILE = re.compile(r"^[0-9]{2}-[a-z0-9][a-z0-9-]*\.md$")
SIGNAL_LIMIT = 8 * 1024  # a signal's file larger than this copies its source; a program cuts its excerpt to fit (signals.3)


def raw_of(cap_text):
    """Where a capture's raw record is, from its raw field, <host>:<path>: (host, path), or None when it names none."""
    raw = field(cap_text, "raw")
    return tuple(raw.split(":", 1)) if raw and ":" in raw else None


def capture_refusal(cap, files, here, banked):
    """Why a program's capture does not land on the drive's branch (signals.6), or None. cap is its folder's name,
    files the folder's files ({name: text}, None for anything that is not a readable file), here this host and banked
    whether the raw record its capture.md names is there on it. A capture is a name crew takes (code.4) holding
    capture.md and its signals, NN-<slug>.md, and nothing else, since raw material stays on its host (signals.3);
    capture.md names itself, the program as its source, who captured it, its event's date, its raw record banked on
    this host, the host that ran the program, and is read, with as many signals as it holds, at least one; each signal
    names itself in its capture, its kind and who asserted it, says what it asserts, quotes its excerpt and is no
    larger than crew lands. The first refusal found is said, naming the file."""
    if not crew.NAME.match(cap):
        return f"{cap} is no capture's name crew takes: lowercase words, digits and dashes (code.4)"
    if files.get("capture.md") is None:
        return f"{cap} has no capture.md"
    for n in sorted(files):
        if n != "capture.md" and (not SIGNAL_FILE.match(n) or files[n] is None):
            return f"{cap}/{n} is no signal's file, NN-<slug>.md: a capture's raw material stays on its host, outside git (signals.3)"
    c = files["capture.md"]
    sigs = sorted(n for n in files if n != "capture.md")
    if field(c, "capture") != cap:
        return f"{cap}/capture.md names the capture {field(c, 'capture')}, not {cap}"
    for f, what in (("source", "the program that recorded it"), ("captured_by", "who recorded it"), ("event_date", "its event's date")):
        if not field(c, f):
            return f"{cap}/capture.md names no {f}, {what}"
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", field(c, "event_date")):
        return f"{cap}/capture.md: event_date is a date, 2026-10-12, not {field(c, 'event_date')}"
    raw = raw_of(c)
    if not raw:
        return f"{cap}/capture.md names no raw record, <host>:<path>, banked on the host that ran the program (signals.3)"
    if raw[0] != here:
        return f"{cap}/capture.md's raw record is on {raw[0]}, and a program's capture lands from the host that banked it, not {here}"
    if not banked:
        return f"{cap}/capture.md's raw record, {raw[1]}, is not on {here}"
    if field(c, "status") != "read" or not sigs:
        return f"{cap} lands read, with its signals: a program's capture is its own excerpt, and its one signal is made with it (signals.6)"
    if field(c, "signals") != str(len(sigs)):
        return f"{cap}/capture.md counts {field(c, 'signals')} signals, and {cap} holds {len(sigs)}"
    for n in sigs:
        t, what = files[n], f"{cap}/{n}"
        if len(t.encode()) > SIGNAL_LIMIT:
            return f"{what} is larger than {SIGNAL_LIMIT // 1024} KiB, so it copies its source: cut its excerpt and keep the whole in the raw record"
        if field(t, "signal") != f"{cap}/{n[:-3]}":
            return f"{what} names the signal {field(t, 'signal')}, not {cap}/{n[:-3]}"
        if field(t, "kind") not in KINDS:
            return f"{what}: kind is one of {', '.join(KINDS)}, not {field(t, 'kind')}"
        if not field(t, "who"):
            return f"{what} names no who, who asserted it"
        body = [l for l in re.sub(r"^---\n.*?\n---\n", "", t, count=1, flags=re.S).splitlines() if l.strip()]
        if not any(not l.startswith(">") for l in body):
            return f"{what} says nothing it asserts"
        if not any(l.startswith(">") for l in body):
            return f"{what} quotes no excerpt"
    return None


def capture_landing(cap, files, have, label):
    """What a capture's landing writes on the drive's branch, {path: text}, from the folder's files and what the
    branch holds at each of their paths (have, {name: text or None}): each file the branch lacks; one it holds the same
    is passed over; one it holds otherwise refuses the landing, since captures and signals are never changed (signals.4).
    Already when there is nothing to write."""
    out = {}
    for n in sorted(files):
        if have.get(n) is None:
            out[f"signals/{cap}/{n}"] = files[n]
        elif have[n] != files[n]:
            fail(f"signals/{cap}/{n} on {label}/main is not the one landed now, and a capture or signal is never changed (signals.4)")
    if not out:
        raise Already(cap)
    return out


def signal_land(fleet, a):
    """crew signal land <capture-dir>: a program's capture, a release adapter's or a deployer's, landed on the
    branch of the drive named, as recorded on this host and never forwarded (signals.2, signals.6): the
    folder checked whole (capture_refusal), then its capture and signals written in one commit, the files the branch holds
    already passed over, and nothing written when it holds them all. Its raw record stays where the program banked it."""
    label = default_label(fleet, a) or fail("which drive? add --label " + "|".join(fleet["drives"]))
    d = pathlib.Path(a.dir)
    d.is_dir() or fail(f"{a.dir} is no capture's folder")
    cap = d.resolve().name
    files = {}
    for f in sorted(d.iterdir()):
        try:
            files[f.name] = f.read_text() if f.is_file() and not f.is_symlink() else None
        except (OSError, UnicodeDecodeError):
            files[f.name] = None
    raw = raw_of(files.get("capture.md"))
    why = capture_refusal(cap, files, crew.this_host(), bool(raw) and pathlib.Path(raw[1]).expanduser().exists())
    not why or fail(why)
    srepo = crew.drive_of(fleet, label)["blueprints"][0]
    btip = tip_of(srepo, "main")
    not (btip and git(srepo, "ls-tree", "--name-only", btip, f"signals/{cap}")) or fail(
        f"{srepo} has signals/{cap} already, so a capture can't take that name (signals.1)")
    seen = {}

    def change(w):
        out = capture_landing(cap, files, {n: w.text(f"signals/{cap}/{n}") for n in files}, label)
        for path, text in out.items():
            w.replace(path, text)
        seen["ids"] = [p[8:-3] for p in out if not p.endswith("/capture.md")]
        w.on += [f"signals/{i}" for i in seen["ids"]]
        capture_asks(w, fleet, label, seen["ids"])
        w.subject = f"signals({cap}): land " + (f"{len(seen['ids'])} signal" + ("" if len(seen["ids"]) == 1 else "s") if seen["ids"] else "the capture")
        return []
    try:
        write(fleet, label, change, f"signals({cap}): land", act="capture")
    except Already:
        print(f"{cap} is already landed on {label}/main; nothing was written")
        return
    print(f"landed {cap} on {label}/main: " + (", ".join(seen["ids"]) or "its capture"))


def signal_show(fleet, a):
    """crew signal show <id>: the signal, by its full id or its short one, its capture's provenance in plain lines (the
    excerpt's grade among them), and its move in each drive that reads it. Reads only the branches, so any host can
    answer."""
    label = default_label(fleet, a)
    labels, errors, hit = [label] if label else list(fleet["drives"]), {}, None
    for l in labels:
        try:
            h = signal_at(fleet, l, a.signal)
        except Refusal as e:
            if label:
                raise
            errors[l] = str(e)  # with no drive named, one that can't be read is passed over, and named below
            continue
        if h:
            hit = (l, h)
            break
    hit or fail(f"no signal {a.signal} on the branches of " + ", ".join(f"{l}/main" for l in labels)
                + " or on main of their first blueprints repos" + "".join(f"; {l} could not be read: {e}" for l, e in errors.items()))
    found_in, (where, repo, tip, text, sig) = hit
    # A signal in the state is its drive's alone; one in a blueprints repo is read by each drive it is first for.
    readers = [found_in] if where != "main" else [l for l in labels if crew.drive_of(fleet, l)["blueprints"][0] == repo]
    moves = []
    for l in readers:
        srepo, ref = state_of(fleet, l)
        stip = tip_of(srepo, ref)
        recs = show(srepo, stip, "moves.rec") if stip else None
        moves.append((l, next((m for m in Plan(recs).recs("Move") if m.get("Signal") == sig), None) if recs else None))
    print(shown_signal(sig, where, repo, text, show(repo, tip, capture_of(sig)), moves))


def shown_signal(sig, where, repo, text, cap, moves):
    """crew signal show: where the signal is, its text, its capture's fields in plain lines (cap, its capture.md, None
    when it has none), and its move in each drive that reads it (moves, [(label, its Move record or None)])."""
    out = [f"signals/{sig}, on {where} of {repo}", "", text.rstrip(), ""]
    if cap is None:
        out.append(f"No capture.md beside it in {repo}.")
    else:
        out.append(f"Its capture, {capture_of(sig)}:")
        out += [f"  {k}: {x}" for k, x in frontmatter(cap)]
    out.append("")
    for l, m in moves:
        out.append(f"No move yet in {l}." if not m else f"Its move in {l}: {m.get('Move')}" + (f" {m.get('Target')}" if m.get("Target") else "")
                   + f", by {m.get('By')} on {m.get('Date')}" + (f": {m.get('Reason')}" if m.get("Reason") else ""))
    return "\n".join(out)


# ---------------------------------------------------------------------- a team's state and this host's run record

def local_entries(label, days=30):
    """This host's run record of the label, from days back, oldest first."""
    runs = record.ROOT / label / "runs" / crew.this_host()
    since = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=days)).isoformat()
    out = []
    for f in sorted(runs.glob("*.rec")) if runs.is_dir() else []:
        if f.stem >= since:
            out += record.parse(f.read_text())
    return sorted(out, key=lambda e: (e["At"], e["Id"]))


# ---------------------------------------------------- a bolt's landing, its fixes and the tidy, on its host


def again_words(mark, case=None):
    """What construct run again on an amended intent adds to its prompt, from the unit's mark: the user's amendment, or
    an approved proposal's, with the planner's case as the user approved it; nothing for any other mark."""
    if mark == "intent":
        return " This unit's intent was amended by the user; revise the existing change to it."
    if amended(mark):
        return (f" This unit's intent was amended by proposal {mark.split('/', 1)[1]}; revise the existing change to it. "
                f"The planner's case, as the user approved it: {' '.join((case or '').split())}")
    return ""


def started(b):
    """Whether a bolt's work is started, by crew bolt start or a crossed team's give before it: marked Path: flume
    (Decision 14 of the-team-machinery-leaves); a bolt in flight is a started one."""
    return b is not None and b.get("Path") == "flume"


def bolt_launches(requests, bolt):
    """Every launch of a bolt's work, its base place's and each on its branch, dropped or not, in requests.rec's order:
    what the runners that took them report where the bolt's work runs by (runner.where)."""
    return [r for r in requests if r.get("Act") == "launch" and (r.get("Base") == f"bolt/{bolt}" or r.get("Work") == f"bolt/{bolt}")]


def kit_of(repo, folder):
    """A kit as crew reads and acts in it on its host (bolt_at): its name, its repository as the plan names it (repo),
    and its folder there (folder), where git runs and crew's landing place goes, <folder>/places/land-<bolt>, as the
    repositories.rec of the runner that took its work reports it, or Flume's status of a place that runner carries
    names it where it reports no repositories (runner.where)."""
    return {"name": repo.split("/")[-1], "repo": repo, "main": folder, "dir": folder}


def bolt_at(fleet, label, b, run=None):
    """Where a started bolt's work runs, read and landed, as the runner that took it reported (the user's ruling of
    2026-11-01; Decision 4 of the-team-machinery-leaves; runner.where): {"label", "machine", "stream", "kit" (kit_of)},
    the host whose runner took the newest of its launches taken, the kit's folder there as that runner's
    repositories.rec reports it, or, where it reports no repositories, as Flume's status of its newest place of the
    kit's work names it (launched_at), and the stream as Flume's status of its places names it; None for a bolt not
    started (started) or naming no kit. crew looks up no kit's host. Refused when no runner has reported taking its work
    yet, crew can't tell which did, the runner that did reports its repositories and none by the kit's name, or it
    reports none and carries no place of the kit's work naming its folder (read.1). run, the drive's requests and
    runners as runner_facts reads them, read when not given."""
    if not started(b) or not b.get("Repo"):
        return None
    return launched_at(fleet, label, b.name(), b.get("Repo"), run)


def bolt_taken(fleet, label, b, run=None):
    """Where a started bolt's work runs (bolt_at), as (where, None); (None, None) while no runner has taken any of its
    own work and every runner was read, so nothing of it has merged through Flume to land; or (None, why) when crew
    can't tell (read.1)."""
    requests, reads = run or runner_facts(fleet, label)
    if runner.where(reads, bolt_launches(requests, b.name()), f"bolt {b.name()}", b.get("Repo") or "") == (None, None):
        return None, None
    try:
        return bolt_at(fleet, label, b, (requests, reads)), None
    except Refusal as e:
        return None, str(e)


def launched_at(fleet, label, bolt, repo, run=None):
    """Where a bolt's work ran, as bolt_at gives it, from its launches, which requests.rec keeps once the bolt has left
    the plan, its kit (repo) as the plan or its landing named it (a landing read after the bolt's close, landing_at); and,
    while no runner has taken any of the bolt's own work, where the runner that took its kit's work reported the kit
    (kit_at), since the bolt is read and landed in the kit's folder there; and where the runner that took the bolt's
    work reports no repositories and carries no place of it naming the folder, every launch refused, as one for a change
    the bolt already holds is, or its places no longer carried, the kit's folder on that runner's host as its places of
    the kit's other work name it (kit_at), never another host's; refused naming the host where neither names it
    (drive-state "A runner that reports no repositories"; read.1)."""
    requests, reads = run or runner_facts(fleet, label)
    at, why = runner.where(reads, bolt_launches(requests, bolt), f"bolt {bolt}", repo)
    not why or fail(why)
    if at is None:
        return kit_at(fleet, label, repo, (requests, reads))
    if not at["dir"]:
        try:
            k = kit_at(fleet, label, repo, (requests, reads))
        except Refusal:
            k = None
        if k and k["machine"] == at["host"]:
            return dict(k, stream=at["stream"] or k["stream"])
    at["dir"] or fail(f"the runner on {at['host']} took bolt {bolt}'s work, reports no repositories it keeps and carries no "
                      f"place of {repo}'s work naming its folder, so crew can't tell where it keeps {repo} there")
    return {"label": label, "machine": at["host"], "stream": at["stream"], "kit": kit_of(repo, at["dir"])}


def known_at(fleet, label, b, run=None):
    """Where a started bolt's work runs (bolt_at), or None for one not started, or whose host crew can't tell, which its
    stages' reads name (Stages.kit)."""
    try:
        return bolt_at(fleet, label, b, run)
    except Refusal:
        return None


def bolt_host(fleet, label, b, runs):
    """The host a started bolt's work runs on (known_at) from the drive's runners as a read holds them (runs, {label:
    (requests, readings)}, rail_runs), None for one not started, one whose drive the read holds no runners of, or
    one whose host crew can't tell; reading nothing (code.7)."""
    return (known_at(fleet, label, b, runs[label]) or {}).get("machine") if started(b) and label in (runs or {}) else None


def bolts_on(fleet, label, plan, host, run=None):
    """The started bolts of a drive's plan whose work runs on a host (known_at), in the plan's order: what that host
    reads and lands of the drive's bolts."""
    run = run or runner_facts(fleet, label)
    return [b for b in plan.bolts() if (known_at(fleet, label, b, run) or {}).get("machine") == host]


def kit_at(fleet, label, kit, run=None):
    """Where a kit's work runs, as the runner that took it reported (the user's ruling of 2026-11-01; runner.where): of
    every launch of the drive's work in the kit's repository, by its name or forge address (kit_in), the host whose
    runner took the newest taken, and the kit's folder there, as bolt_at gives a bolt's; where its landings card's rows
    are forecast and read. Refused when no runner has reported taking any of the kit's work, crew can't tell which did,
    or where it keeps the kit (read.1)."""
    requests, reads = run or runner_facts(fleet, label)
    at, why = runner.where(reads, runner.kit_launches(requests, kit), kit, kit)
    not why or fail(why)
    at or fail(f"no runner has reported taking {kit}'s work yet, so crew can't tell where it runs")
    at["dir"] or fail(f"the runner on {at['host']} took {kit}'s work, reports no repositories it keeps and carries no place "
                      f"of it naming its folder, so crew can't tell where it keeps {kit} there")
    return {"label": label, "machine": at["host"], "stream": at["stream"], "kit": kit_of(kit, at["dir"])}


def card_kit(fleet, t, kit, home):
    """The kit a card of it is asked from and filed under (card_where): its folder where its work runs (t, kit_at), with
    its forge address (forge); home, the kit as the card names it when crew can't tell where its work runs or its forge
    address, t None."""
    if t is None:
        return home
    try:
        return dict(t["kit"], repo=forge(fleet, t))
    except Refusal:
        return dict(t["kit"], repo=home["repo"])


def unit_at(fleet, label, unit):
    """Where a unit's work ran, as its bolt's (bolt_at), read from the plan. Refused when the plan can't be read, holds
    no such unit, or its bolt is not started or crew can't tell where its work runs."""
    plan = plan_of(fleet, label) or fail(f"{label}/main could not be read, so where {unit} was built can't be told")
    u = plan.item(unit) or fail(f"{label}/main holds no unit {unit}")
    b = plan.bolt(u.get("Bolt")) if u.get("Bolt") else None
    b or fail(f"{unit} is in no bolt of {label}/main, so where it was built can't be told")
    return bolt_at(fleet, label, b) or fail(f"bolt {b.name()} is not started, so {unit} was built nowhere crew can read")


def batch_unit_at(fleet, label, bolt, unit, run=None):
    """Where a batch's unit was built (review-batches; the user's ruling of 2026-11-01): where the bolt its entry names
    (<unit>:<bolt>@<commit>) ran its work, as the runner that took it reported, the kit from its launches (launched_at),
    so a bolt that has left the plan is still read; and, for an entry written before a batch named its bolt, whose
    middle name is a team's, where the plan's bolt of the unit runs (unit_at). Refused when crew can't tell."""
    requests, reads = run or runner_facts(fleet, label)
    mine = bolt_launches(requests, bolt)
    if mine:
        return launched_at(fleet, label, bolt, mine[-1].get("Repo"), (requests, reads))
    return unit_at(fleet, label, unit)


def forge(fleet, t):
    """A kit's forge address, <owner>/<name>, for GitHub's pull requests: the plan's Repo where it names one, else read
    from the origin remote of its folder on its host (t, bolt_at), refused when that names no GitHub repository (read.1)."""
    repo = t["kit"]["repo"]
    if "/" in repo:
        return repo
    _, url = kit_git(fleet, t, t["kit"]["main"], "config", "--get", "remote.origin.url")  # as configured, before any insteadOf
    m = re.search(r"github\.com[:/]([^/\s]+/[^/\s]+?)(?:\.git)?/?$", url)
    m or fail(f"{t['kit']['name']}'s origin in {t['kit']['main']} on {t['machine']} is {url}, which names no GitHub repository")
    return m.group(1)


def kit_git(fleet, t, where, *args, ok=(0,)):
    """git in a checkout of the team's kit, on the team's host: (exit status, output); refused in git's words when it
    exits with a status outside ok."""
    r = crew.on_machine(fleet, t["machine"], ["git", "-C", where, *args])
    r.returncode in ok or fail(f"git {args[0]} in {where} on {t['machine']} failed: "
                               + ((r.stderr or r.stdout).strip() or f"exit {r.returncode}"))
    return r.returncode, r.stdout.strip()


def plan_of(fleet, label):
    """The label's plan, or None when it can't be read, so a team's slots are still read from the kit."""
    try:
        repo, ref = state_of(fleet, label)
        tip = tip_of(repo, ref)
        return read(repo, ref, tip) if tip else None
    except Refusal:
        return None


def tidy(fleet, t, landed=None):
    """The tidy of a kit's checkout on this host (plan.9 as crew-lands-each-bolt-through-flumes-base-place, Decision 8,
    departs from it): crew makes no worktree on a bolt's branch now, so it removes none and runs no sluice: each
    worktree of crew's own from before, a landing's place, <kit>/places/land-<bolt> on bolt/<bolt>, or a bolt's
    worktree from before record 0026, <kit>/bolts/<bolt>, is named with the commands that remove it, sluice's release
    and then the kit's own wt remove, as the user's to run; no bolt branch is deleted and no mark of crew's kept or
    read, a bolt's branch being Flume's tidy's and sluice's. Every other worktree, a place of Flume's among them, is
    left alone. landed is kept for its callers and changes nothing. Returns the paths removed, none."""
    main, kdir = os.path.realpath(t["kit"]["main"]), os.path.realpath(t["kit"]["dir"])
    for w in gather.worktrees(main):
        path, branch = w["path"], w.get("branch") or ""
        said = leftover_said(path, branch, kdir)
        if said:
            print(said)
    return []


def leftover_said(path, branch, kdir):
    """What the tidy says of a worktree crew made before bolts were base places (Decision 8), or None for any other: a
    landing's place, <kit>/places/land-<bolt> on bolt/<bolt>, or a legacy bolt worktree, <kit>/bolts/<bolt>, named with
    the commands that remove it, sluice's release of it and then the kit's own wt remove, the user's to run, since crew
    calls neither. A decision of facts alone (code.7)."""
    folder, parent = os.path.basename(path), os.path.basename(os.path.dirname(path))
    land = parent == "places" and os.path.dirname(os.path.dirname(path)) == kdir and branch.startswith("bolt/") and folder == f"land-{branch[5:]}"
    legacy = parent == "bolts" and os.path.dirname(os.path.dirname(path)) == kdir
    if not (land or legacy):
        return None
    what = f"a landing's place of bolt {branch[5:]}" if land else f"bolt {folder}'s worktree from before bolts lived on GitHub"
    return (f"{path} is {what}, which crew makes no more and removes no more: it is yours to remove, with "
            f"sluice release --worktree {path} and then wt -C {os.path.join(kdir, 'main')} remove {path}")


# ------------------------------------------------ a kit's read after a landing or a drop, and a bolt's conflict with main


def kit_sweep(fleet, a):
    """crew _sweep <label> <kit> --dir <folder> [--landed <bolt> --outcome <words>] [--units <unit>...], on the host a
    bolt's work runs on, which a landing hands it to with the kit's folder there (sweep_on, bolt_at, code.3): the kit's
    read there (kit_read), reading no landing after a landing (--landed). An older crew's --said and --here, a landing
    on the user's words in ops's pane, are taken and read as nothing, since no word in a pane lands a bolt (record 0056
    point 5)."""
    here = crew.this_host()
    arrived(fleet, here)
    kit_read(fleet, {"label": a.label, "machine": here, "stream": None, "kit": kit_of(a.kit, a.dir)}, a.landed, a.outcome,
             a.units)


def kit_read(fleet, t, landed=None, outcome=None, units=()):
    """A kit's read on the host a bolt's work runs on, in the kit's folder there (t, bolt_at), which a landing or a drop
    asks for there (sweep_on): the landing of each started bolt of the kit
    that may have an outcome or a close nothing recorded read (reap_landings), but by the read a landing's close asks
    for (landed, the bolt), which reads none: crew bolt land waits on that read, and a landing read's close of a bolt
    runs under the bolt's landing lock (landing_read), so a landing read there would wait on a lock its own caller
    holds, its bolt's when the plan is read below the close, its bolt.land entry not yet on the branch (read.5), or
    another bolt's whose read waits on its own close in turn; that bolt was read by the act that closed it, and the
    kit's next read reads the rest (plan.21); then the tidy, which names any landing or legacy bolt worktree an older
    crew left and removes nothing (tidy); then each bolt of it that is local until it lands said, once
    (bolts_local_said, plan.19); what the units of a bolt that landed or was dropped (units) recorded as made, kept here
    for its batch's card, removed (made_drop); and after a landing, the bolt's card closed here with the outcome
    (landing_cards_closed). What any of them refuses is said on standard error."""
    if not landed:  # a landing's read reads no landing: its caller may hold a landing's lock (landing_read)
        reap_landings(fleet, t["label"])
    try:
        tidy(fleet, t, landed)
    except Refusal as e:
        print(e, file=sys.stderr)
    try:
        plan = plan_of(fleet, t["label"])
        for line in bolts_local_said(fleet, t, plan) if plan else []:
            print(line)
    except Refusal as e:
        print(e, file=sys.stderr)
    dropped = made_drop(t["label"], list(units))
    if dropped:
        print(dropped)
    if landed:
        landing_cards_closed(fleet, t, landed, outcome or "")


def main_conflict(entries, bolt, head):
    """The conflict with what main has landed the run record holds for a bolt at its present head (rail-cards "A row
    forecast to conflict with main takes main first, recorded once and telling no one", teams.21), from the entries, oldest first: the latest forecast,
    not refused, on bolt/<bolt> alone, at the head (its Heads beginning bolt/<bolt>@<head7> main@), meeting no submission
    queued on main (no #<n> in its Heads) and naming its Paths, a landings card's raise's or a conductor's wait's from
    before: (main's short sha, [paths]); None for none, one at a head the bolt has moved from, one met only queued, and
    the form a wait recorded when sluice could not forecast, which names no paths."""
    if not head:
        return None
    at = f"bolt/{bolt}@{head[:7]} main@"
    for e in reversed(entries):
        words = (e.get("Heads") or "").split()
        if (e.get("Act") == "forecast" and not e.get("Refused") and e.get("On") == [f"bolt/{bolt}"] and len(words) == 2
                and (e.get("Heads") or "").startswith(at) and (e.get("Paths") or "").split()):
            return words[1][len("main@"):], e["Paths"].split()
    return None


# ------------------------------------------------------------------------------------------------- the wait

POLL = 10  # seconds between a wait's reads
ENDED_WITH = "the session that started this wait has ended, so the wait ends with it"


def wait_session():
    """The Claude Code session a wait runs in on this host, by the process id Claude Code gives every command its Bash
    tool runs, a background one's included, in CLAUDE_PID (read against Claude Code 2.1.308 on deneb, 2026-10-28);
    None for a wait no session of this host started: a person's at a terminal, or one forwarded from another host,
    since ssh carries no CLAUDE_PID (code.3)."""
    pid = os.environ.get("CLAUDE_PID", "")
    return int(pid) if pid.isdigit() and int(pid) > 1 else None


def session_ended(pid):
    """Whether the session a wait runs in (wait_session) has ended, its process gone, so the wait ends with it rather
    than outliving its caller (teams.24); never for a wait no session started."""
    if pid is None:
        return False
    try:
        os.kill(pid, 0)
    except PermissionError:  # alive, as another user's
        return False
    except OSError:
        return True
    return False


def background(info):
    """What an agent's own session says it still waits on: (the background tasks it started and has not been told are
    over, when its transcript last wrote, None), or (None, None, what crew could not read)."""
    sess = info.get("agent_session")
    sid = sess.get("value") if isinstance(sess, dict) else None
    if not isinstance(sid, str) or not sid:
        return None, None, "herdr names no session for it"
    path = transcript.find(sid)
    if path is None:
        return None, None, f"no transcript for its session {sid}"
    pending = transcript.pending(path)
    if pending is None:
        return None, None, f"its transcript {path} can't be read"
    return pending, transcript.last_at(path), None


# ------------------------------------------------------------------------------ a team's commands, one process each

def sh(**pairs):
    return "\n".join(f"{k}={__import__('shlex').quote(str(v))}" for k, v in pairs.items())


def forwarded(fleet, machine):
    """A team's or a main level's command runs on the host its agents run on (code.3). On another host this process says
    on descriptor 3 where that is and how crew is run there, as shell assignments (teams.9), for bash crew to run the same
    command there as the one asking, and stops, having touched nothing."""
    if machine == crew.this_host():
        return
    said = sh(MACHINE=machine, SSH_TARGET=crew.ssh_of(fleet, machine), **crew.reach(fleet, machine))
    try:
        os.write(3, (said + "\n").encode())
    except OSError:
        fail(f"this runs on {machine}: run it there with crew")
    raise Stopped(0)


def arrived(fleet, machine):
    """A command where it runs: forwarded there when this is not that host (forwarded); what killed commands left of
    their readings swept; and the asker's Claude session read while herdr's listing is the one the command starts with
    (record.session)."""
    forwarded(fleet, machine)
    READ.sweep()
    record.session()


def not_held(label=None, act=None, on=()):
    """A command that would start an agent refused while this host is held (teams.19): said, and for an act that moves
    work recorded refused (stopped); nothing when it is not held."""
    h = crew.held()
    if not h:
        return
    said = crew.held_said(crew.this_host(), h)
    if label and act:
        stopped(label, act, list(on), said)
    fail(said)


def stopped(label, act, on, said):
    """A team's command refused: said on standard error, recorded as the act refused (record.1), and stopped."""
    print(said, file=sys.stderr)
    record.emit(label, act, on, refused=said)
    raise Stopped(1)


def landings_judged(fleet, label, plan, sv, runs):
    """The landings each host's card sweep reads (reap_judged), from the rail's read and reading nothing (code.7):
    {host: [{bolt, kit, dir, stages}]}, each started bolt of the drive whose landing the runner's report has decided,
    landed, refused or stopped (Stages.landing), under the host its work runs on as the read holds it (known_at), with
    its kit's folder there and the stage of each unit and chore the plan holds in it (Stages), so a sweep reads no plan
    or kit of its own (plan.12), and one with no landing decided reads nothing for it; none where the read holds no
    runners of the drive."""
    if label not in (runs or {}):
        return {}
    st, out = Stages(fleet, plan, sv, runs, label), {}
    of = st.of
    for b in plan.bolts():
        decided = started(b) and (st.landing(b) or {}).get("outcome") in ("landed", "refused", "stopped")
        t = known_at(fleet, label, b, runs[label]) if decided else None
        if t:
            out.setdefault(t["machine"], []).append(dict(bolt=b.name(), kit=t["kit"]["name"], dir=t["kit"]["dir"],
                                                         stages=[of(u.name())["stage"] for u in plan.work_of(b.name())]))
    return out


def reap_landings(fleet, label):
    """A kit's read of the drive's landings on this host after a landing or a drop (kit_read): each started bolt
    whose work runs here (bolts_on), read by reap_judged. A plan or runners that can't be read read none."""
    pl = plan_of(fleet, label)
    try:
        run = runner_facts(fleet, label)
    except Refusal:
        return
    bolts = bolts_on(fleet, label, pl, crew.this_host(), run) if pl else []
    reap_judged(fleet, label, [dict(bolt=b.name()) for b in bolts], run)


def reap_judged(fleet, label, landings, run=None):
    """The read of a drive's landings (plan.21; crew-lands-each-bolt-through-flumes-base-place, Decision 6), which
    the rail's sweep (card_sweep, from the rail's read, landings_judged) and a kit's read (reap_landings) run: of each
    bolt given, {bolt, ...}, one crew posted a land of on the user's send (lands_posted), its landing read from the
    runner's report and recorded and acted on once decided (landing_read), so a refused close is tried again at each
    sweep until it is lifted; one with no land posted reads nothing, so an idle sweep's read is unchanged (plan.12). A
    read refused said and raised no further; requests, runners or a run record that can't be read read none."""
    if not landings:
        return
    try:
        run = run or runner_facts(fleet, label)
        entries = drive_entries(fleet, label)
    except Refusal as e:
        print(f"crew reads none of {label}'s landings: {e}", file=sys.stderr)
        return
    asked = {p["work"] for p in lands_posted(entries)}
    for g in landings:
        if f"bolt/{g['bolt']}" not in asked:
            continue
        try:
            landing_read(fleet, label, g["bolt"], run, entries, card=not LANDINGS_READ)
        except Refusal as e:
            print(e, file=sys.stderr)


def fix(fleet, a):
    """crew fix <bolt> <name> "<what is wrong>" | --drop [--label L]: a fix of a started bolt as a Flume place of the fix
    kind on its branch (Decision 15 of the-team-machinery-leaves, record 0049 part 4), the planner's or main-level
    ops's (may_request), a plan write on the asking host that starts nothing there: a new fix a launch on the bolt's
    branch in its repository, for a runner whose configuration names it to take, in the stream its host maps it to (the user's
    ruling of 2026-11-01; runner.fix_launch), the bolt's landing held while it is in
    flight (land_hand, land_facts), and refused while the run record has the bolt's landing queued or landing again
    with no outcome, naming it, open again once sluice has rejected it (landing_hold); --drop a drop of its launch
    (runner.fix_drop_refusal), refused for a fix the runner reports merged. Flume submits the place and
    tells its end itself, so crew fix has no merge and no wait. Recorded as fix.start or fix.drop, done or refused
    (teams.3)."""
    crew.NAME.match(a.name) or fail("a fix is named with lowercase words and dashes")
    mode = "drop" if a.drop else "start"
    (a.words is not None) != a.drop or fail('crew fix takes the fix\'s words or --drop: crew fix <bolt> <name> "<words>" | --drop')
    label, repo, tip, plan = locate(fleet, "Bolt", a.bolt, default_label(fleet, a))
    on, act, seen = [f"fix/{a.bolt}/{a.name}", f"bolt/{a.bolt}"], f"fix.{mode}", {}
    try:
        may_request(fleet, "fix")
        mode == "drop" or (a.words or "").strip() or fail(f'crew fix needs what is wrong: crew fix {a.bolt} {a.name} "<words>"')
        def change(w):
            seen.update(fix_flume(fleet, w, a.bolt, mode, a.name, a.words))
            return []
        write(fleet, label, change, f"plan({a.bolt}): fix {a.name}", act=act, on=on)
    except Refusal as e:
        record.emit(label, act, on, refused=str(e))
        raise
    if mode == "drop":
        print(f"fix/{a.bolt}/{a.name} is dropped (request {seen['n']}): {took(seen['host'])} drops its place")
        return
    print(f"fix {a.bolt}--{a.name} is launched on bolt/{a.bolt} in {seen['repo']} (request {seen['n']}) for a runner whose "
          f"configuration names it to take, and crew bolts shows its place; {a.bolt}'s landing waits until it has merged or been dropped")
    land_hand(fleet, label, plan.bolt(a.bolt).get("Repo"), f"{a.bolt} is held for a fix: {a.words}")


def took(host):
    """The runner a request's words name: the one on its host where crew read which took the launch (Write.taker),
    else the runner that took it."""
    return f"the runner on {host}" if host else "the runner that took it"


def fix_flume(fleet, w, bolt, mode, name, words):
    """crew fix's change to a write (fix), each fact read again at the tip it is applied to (plan.1): the bolt started,
    marked Path: flume; then a new fix's launch appended in the bolt's repository (runner.fix_launch), refused while the
    run record at that tip has the bolt's landing asked, queued or landing again (phase_at, landing_hold), or for --drop
    its launch's drop (runner.fix_drop_refusal), its stage read from the runner that took it alone, as the write reads
    them: a fix the runner reports merged, a record Flume holds for the runner among them, has its drop refused as a
    merged fix's is (bolt-plan "A fix the runner reports merged holds nothing").
    Returns what it asked, {n, host, repo}: host, the runner's that took the launch dropped, where crew can tell."""
    crossed_bolt(w.plan, bolt) or fail(f"bolt {bolt} has not been started, so a fix of it has no Flume place to run in")
    requests, work = requests_of(w).recs("Request"), f"fix/{bolt}/{name}"
    if mode == "drop":
        launch = runner.launch_of(requests, work)
        s = runner.piece_stage(requests, w.runners(), launch) if launch is not None else None
        why = runner.fix_drop_refusal(f"bolt {bolt}", work, launch, s)
        not why or fail(why)
        w.subject = f"plan({bolt}): drop fix {name}"
        return dict(n=request(w, "drop", work, Of=launch.get("Request")), host=w.taker(launch), repo=launch.get("Repo"))
    why = landing_hold(phase_at(w, bolt), bolt, f"fix {bolt}--{name}")
    not why or fail(why)
    launched, why = runner.fix_launch(w.plan, requests, bolt, w.label, name, words)
    not why or fail(why)
    act, work, given = launched
    w.subject = f"plan({bolt}): fix {name}"
    return dict(n=request(w, act, work, **given), host=None, repo=given["Repo"])


def main_fix(fleet, a):
    """crew main fix <kit> <name> "<the failure's words>" | --drop [--label L]: a fix of a kit's red main as a Flume place on main (Decision 11 of teams-cross-to-flume-as-their-bolts-land,
    Decision 15 of the-team-machinery-leaves, state.3), main-level ops's or the user's on reading main's checks red
    after a landing (may_request), a plan write on the asking host that starts nothing there: a launch of Flume's fix
    kind on main, its submission held for the user's send and main-level ops its recipient, in the kit's repository for
    a runner whose configuration names it to take in the stream its host maps it to (the user's ruling of 2026-11-01;
    runner.main_fix_launch), refused naming state.3's way, a bolt of one chore proposed first among the planned, where
    no runner answers for the drive; --drop a drop of its launch (runner.fix_drop_refusal). --send, with or without
    --excerpt, is refused at once, before anything is read (send_refused): the fix lands on the user's send of its row
    on its kit's landings card, which crew carries to the runner as a land (lands_change; crew-lands-each-bolt-through-
    flumes-base-place, Decision 5). The kit's drive is the one whose plan or landings name it (drive_kits),
    --label choosing. Recorded as fix.start or fix.drop on fix/main/<kit>/<name>, done or refused."""
    not (a.send or a.excerpt is not None) or fail(send_refused(a.kit, a.name))  # before anything is read (Decision 5)
    mode = "drop" if a.drop else "start"
    (a.words is not None) + a.drop == 1 or fail(
        'crew main fix takes the failure\'s words or --drop: crew main fix <kit> <name> "<words>" | --drop')
    crew.NAME.match(a.name) or fail("a fix is named with lowercase words and dashes")
    label = default_label(fleet, a)
    labels = [l for l in ([label] if label else sorted(fleet["drives"])) if kit_in(a.kit, kits_read(fleet, l))]
    labels or fail((f"{label} plans no work of {a.kit} and records no landing of it" if label else
                    f"no drive plans work of {a.kit} or records a landing of it") + ", so crew has no main of it to fix")
    len(labels) == 1 or fail(f"{a.kit} is planned in {' and '.join(labels)}: add --label")
    CONTEXT["label"] = label = labels[0]
    kit_name = a.kit.split("/")[-1]
    repo = next(k for k in kits_read(fleet, label) if kit_in(a.kit, [k]))
    on, act, seen = [f"fix/main/{kit_name}/{a.name}"], {"start": "fix.start", "drop": "fix.drop"}[mode], {}
    frm, fields = [], {}
    try:
        (a.words or "").strip() or mode != "start" or fail(f"crew main fix needs the failure's words: crew main fix {kit_name} {a.name} \"<words>\"")

        def change(w):
            seen.update(main_fix_change(fleet, w, repo, a.name, mode, a.words))
            return []
        write(fleet, label, change, f"plan(main): fix {a.name} of {kit_name}", act=act, on=on, frm=frm, fields=fields)
    except Refusal as e:
        record.emit(label, act, on, frm, refused=str(e))
        raise
    if mode == "drop":
        print(f"fix main--{a.name} of {kit_name}'s main is dropped (request {seen['n']}): {took(seen['host'])} drops its place")
        return
    print(f"fix main--{a.name} is launched on {kit_name}'s main in {repo} (request {seen['n']}) for a runner whose configuration "
          f"names it to take, its submission held for the user's send: once its code has delivered, {kit_name}'s landings row carries it")


def main_fix_change(fleet, w, repo, name, mode, words):
    """crew main fix's change to a write (main_fix), each fact read again at the tip it is applied to (plan.1): for a
    new fix, a runner answering for the drive and the launch appended in the kit's repository (repo, as the
    drive's kits name it; runner.main_fix_launch); for --drop, its launch's drop (runner.fix_drop_refusal), its
    stage read from the runner that took it as the write reads them; the user's send of it is its kit's landings card's
    (lands_change). Returns what it asked, {n, host}: host, the runner's that took the launch, where crew can tell."""
    kit = repo.split("/")[-1]
    requests = requests_of(w).recs("Request")
    work = f"fix/main/{kit}/{name}"
    if mode == "drop":
        launch = runner.launch_of(requests, work)
        s = runner.piece_stage(requests, w.runners(), launch) if launch is not None else None
        why = runner.fix_drop_refusal(kit, work, launch, s)
        not why or fail(why)
        w.subject = f"plan(main): drop fix {name} of {kit}"
        return dict(n=request(w, "drop", work, Of=launch.get("Request")), host=w.taker(launch))
    launched, why = runner.main_fix_launch(w.plan, requests, w.label, repo, name, words, bool(w.runners()))
    not why or fail(why)
    act, work, given = launched
    w.subject = f"plan(main): fix {name} of {kit}"
    return dict(n=request(w, act, work, **given), host=None)


def greeting(fleet, agents, roles):
    """Each agent of a main level that a command started or brought back is greeted (teams.7), side by side, so one
    waiting on a question holds back no other; a greeting that can't be sent fails nothing. Returns the greetings, for
    the command to wait on before it ends (greeted)."""
    import threading

    def greet(name):
        try:
            crew.greet_standing(fleet, name)
        except Refusal as e:
            print(e, file=sys.stderr)
    out = [threading.Thread(target=greet, args=(agents.agent_of(r),)) for r in roles]
    for th in out:
        th.start()
    return out


def greeted(greetings):
    """Once every greeting has been sent, or given up on."""
    for th in greetings:
        th.join()


def moved_role(fleet, label, ms):
    """What refuses a main level's up while one of its roles' agents still runs in a session the role no longer stands
    in, its pane recorded there, so up would start it a second time in its own: None when none does."""
    p = crew.drive_of(fleet, label)
    for m in ms:
        for role, *_ in m.lines("panes"):
            if role in crew.MAIN_STANDING and not crew.on_demand(p, role) and role not in m.standing and m.status(role):
                return (f"{label}-{role} still runs in session {m.session} ({m.pane(role)}), and its drive names it another session "
                        f"now: crew main down {label} ends it, then crew main up {label} starts it there")
    return None


def kinds_up(fleet, label, ms):
    """What crew main up does for the roles its drive's `runs` names on demand (crew.on_demand), which run as their
    kind and none of which it starts or greets (design
    Decision 14, main-level "A role that runs as its kind gets no tab, no start and no revive"): roles.rec on the drive's branch written to
    match the teams file where anything is due (asks.roles_due), in a commit of its own, the record of a role that
    stands again removed though none runs as its kind now (role-runs "The planner stands again"); and a standing agent
    of such a role still up ended and its tab closed, or, while it works, left and said so. With none running as its
    kind, a branch not there yet holds no record, and one crew can't read keeps what it holds, said, and up goes on
    (read.1), as it did before any role ran as its kind (roles.8)."""
    p = crew.drive_of(fleet, label)
    kinds = [r for r in crew.MAIN_STANDING + ("reviewer",) if crew.on_demand(p, r)]
    repo, ref = state_of(fleet, label)
    if kinds:
        tip = tip_of(repo, ref) or fail(f"{repo} has no {ref} yet: crew state init {label}")
    else:
        try:
            tip = tip_of(repo, ref)
        except Refusal as e:
            print(f"{e}: crew can't tell whether {label}'s roles.rec holds a role that stands again, and removes nothing",
                  file=sys.stderr)
            return
        if not tip:
            return
    metas = {r: crew.definition(asks.definition_of(r))[0] for r in kinds}
    due, gone = asks.roles_due(asks.parse_roles(show(repo, tip, "roles.rec")), p, metas)
    def change(w):
        roles_lines(w, fleet, label)
        return []
    if due or gone:
        write(fleet, label, change, f"roles({label}): to match the teams file",
              act="main.up", on=[f"agent/{label}-{r}" for r in [d["Role"] for d in due] + gone],
              why=f"main({label}): roles.rec to match the teams file")
    for role in kinds:
        m = next((m for m in ms if m.session == crew.role_session(p, role)), None)
        if not m or not m.status(role):
            continue
        why = m.stop(role)
        if why:
            print(f"{why}: {label}'s {role} runs as its kind, so it is ended once it is not working")
            continue
        m.close_pane(role)
        m.record("main.down", f"main({label}): end {label}-{role}, which runs as its kind", [role])
        print(f"{label}-{role}'s standing agent is ended: {label}'s {role} runs as its kind")


def kind_said(stream, waiting, run, now):
    """What crew main status says of a role its drive's `runs` names on demand (main-level "A role that runs as its
    kind is not started by crew-role"), from facts: the stream it runs in, its drive's own, named by its label
    (Decision 2 of a-roles-way-of-running-says-what-it-means), the asks of it that wait, oldest first (asks.pending),
    its latest run as the runner's records show it (runner.role_run) and the time now. That it is on-demand, the
    file's own word (crew.RUNS_ON_DEMAND; Decision 4 of a-roles-way-of-running-is-said-in-the-files-words), in that
    stream; whether a run of it stands, naming its place, with the runner's words where it could launch none, or that
    crew can't tell, naming why (read.1); and how many asks wait, with the oldest's age."""
    if run["why"]:
        ran = f"crew can't tell whether a run stands: {run['why']}"
    elif run["live"]:
        ran = f"a run stands, the place {run['place']}"
    else:
        ran = "no run stands" + (f" (the runner could not launch its last: {run['words']})" if run["words"] else "")
    n = len(waiting)
    waits = (f"{n} ask{'' if n == 1 else 's'} wait{'s' if n == 1 else ''}, the oldest asked {age(utc(waiting[0]['At']), now)} ago"
             if waiting else "no ask waits")
    return f"{crew.RUNS_ON_DEMAND} in stream {stream}; {ran}; {waits}"


def kinds_said(fleet, label):
    """What crew main status says of each role the drive's `runs` names on demand, {role: words} (kind_said), its stream
    the drive's label: read from
    asks.rec on the drive's branch (asks.pending) and the runner's records on the main level's host
    (runner_facts, runner.role_run), a host whose runner can't be read named for each role and the rest still said
    (read.3)."""
    p = crew.drive_of(fleet, label)
    kinds = [r for r in crew.KIND_ROLES if crew.on_demand(p, r)]
    if not kinds:
        return {}
    repo, ref = state_of(fleet, label)
    tip = tip_of(repo, ref)
    held, turns = asks.parse(show(repo, tip, "asks.rec") if tip else None)
    reading = runner.of_host(runner_facts(fleet, label)[1], label, p["machine"])
    now = datetime.datetime.now(datetime.timezone.utc)
    return {role: kind_said(label, asks.pending(held, [], turns, role)[0],
                            runner.role_run(reading, f"{label}/{role}"), now) for role in kinds}


def main_cmd(fleet, a):
    """crew main up|down|status <label>, on the main level's host: its standing roles, of its design agent, planner, ops
    and operator, one tab each in the <label> workspace of the session each runs in (record 0035), started and greeted,
    ended, or listed, and nothing else; no dispatcher is started anywhere. Up refuses while a role's agent still runs in
    a session it no longer stands in (moved_role), which down ends."""
    p = crew.drive_of(fleet, a.label)
    arrived(fleet, p["machine"])
    ms = crew.mains(fleet, a.label, a.force)
    for m in ms:
        m.ensure()
    label = p["label"]
    if a.act == "up":
        not_held()
        moved = moved_role(fleet, label, ms)
        not moved or fail(moved)
        kinds_up(fleet, label, ms)
        started_in = []
        for m in ms:
            m.mark(down=False)
            m.panes()
            started = m.start_standing()
            m.record("main.up", f"main({label}): up", started)
            started_in.append((m, started))
        greetings = []
        for m, started in started_in:
            greetings += greeting(fleet, m, started)
        greeted(greetings)
    elif a.act == "down":
        for m in ms:
            # Every agent its panes file names, a role that stood here before its drive named it a session apart
            # among them, so down ends what up would refuse over.
            for role in [r for r, *_ in m.lines("panes") if r in crew.MAIN_STANDING]:
                why = m.stop(role)
                if why:
                    print(why, file=sys.stderr)
            m.mark(down=True)
            m.record("main.down", f"main({label}): down", m.ended)
        print(f"{label}'s main level is down; its panes are still there.")
    else:
        # Each role's line says the word its drive's `runs` names it by (main-level "Main status says a standing role
        # is standing"): a standing role's before its agent's status, an on-demand role's from kind_said.
        for m in ms:
            for role in m.standing:
                print("%-34s %-8s %-14s %s; %s" % (m.agent_of(role), m.pane(role), m.session, crew.RUNS_STANDING,
                                                   m.status(role) or "not up"))
        for role, said in kinds_said(fleet, label).items():
            print("%-34s %-8s %-14s %s" % (f"{label}-{role}", "-", "-", said))


def review_cmd(fleet, a):
    """crew review <label> [--wait [--timeout <ms>]], on the main level's host: the drive's reviewer started fresh
    for the batch of changes due, in a review tab of the main level's workspace beside the planner, and sent its batch as
    its prompt, the start recorded; with --wait, the wait for its summary, which records the batch, and then its agent
    ended and its tab closed. Refused while a reviewer still reviews, or the main level is not up. A drive that
    runs its reviewer as its kind is asked the batch instead (review_asked).

    The batch is sent taken or sent again (teams.15, crew.send_taken): one the reviewer did not take at the second
    sending leaves nothing typed, its start recorded refused and the command refused; one crew can't tell it took is
    recorded started, saying so. A reviewer up but idle that took no batch, with no summary written since its last
    start, is ended, the end recorded (review.end) and said, and the batch's reviewer started afresh; one at work, at a
    question or that took its batch is refused, since crew review takes no --force and a working agent is ended only
    with one (teams.2); and --wait on a reviewer that took no batch refuses, naming crew review (reviewer_up_said)."""
    p = crew.drive_of(fleet, a.label)
    arrived(fleet, p["machine"])
    if crew.role_runs(fleet, p["label"], "reviewer") == crew.RUNS_ON_DEMAND:
        return review_asked(fleet, p["label"], a)
    m = crew.main_holding(fleet, a.label, "reviewer")
    m.ensure()
    label, agent = p["label"], m.agent_of("reviewer")
    if a.wait:
        up = reviewer_up(fleet, label, m)
        if up and up[0] == "afresh":
            fail(f"{agent} took no batch, so no summary is coming: crew review {label} ends it and starts the batch's "
                 "reviewer afresh")
        summary = review_wait(fleet, argparse.Namespace(label=label, timeout=a.timeout))
        why = m.stop("reviewer")
        if why:
            print(why, file=sys.stderr)
        m.close_pane("reviewer")
        tab = m.get("layout", "tab:review")
        if tab:
            m.herdr.run("tab", "close", tab)
            m.drop("layout", "tab:review")
        print(f"batch summary: {summary}")
        return
    not_held()
    up = reviewer_up(fleet, label, m)
    not up or up[0] == "afresh" or fail(up[1])
    m.get("layout", crew.ws_key(label)) or fail(f"{label}'s main level is not up in session {m.session}: crew main up {label}")
    b = review_start(fleet, argparse.Namespace(label=label))
    if up:
        why = m.stop("reviewer")
        not why or fail(f"{why}: crew starts no reviewer over it")
        m.record("review.end", f"review({label}): end {agent}, which took no batch", ["reviewer"])
        print(up[1])
    if not m.herdr.live(m.pane("reviewer")):  # the tab is kept in the layout, so the batch's end closes it
        made = m.tab(label, "review", m.cwd, "reviewer")
        m.put("layout", "tab:review", made["tab"]["tab_id"])
    if not m.start("reviewer"):
        raise Stopped(1)
    n, on = b["N"], [f"batch/{b['N']}", f"agent/{agent}"] + [f"unit/{u}" for u in b["NAMES"].split()]
    how, why = crew.send_taken(fleet, agent, b["PROMPT"])
    afresh = f"crew review {label} ends it and starts the batch's reviewer afresh"
    if how == "never":
        said = crew.untaken_said(agent, f"batch {n}", how, why)
        record.emit(label, "review.start", on, why=f"batch({n}): start review", refused=said, Batch=n, Units=b["UNITS"])
        fail(f"{said}; once it is idle, {afresh}")
    record.emit(label, "review.start", on, why=f"batch({n}): start review", Batch=n, Units=b["UNITS"])
    if how == "unread":
        print(f"{crew.untaken_said(agent, f'batch {n}', how, why)}; crew review {label} --wait waits for its summary, and "
              f"should {agent} sit idle having taken none, {afresh}", file=sys.stderr)
        print(f"batch {n} of {label} is recorded started, into {b['FILE']}: crew review {label} --wait waits for it")
        return
    print(f"{agent} is reviewing batch {n} of {label}, into {b['FILE']}: crew review {label} --wait waits for it")


def reviewer_up_said(label, agent, status, asking, took, written):
    """What crew review does with its drive's reviewer when herdr reads it up (teams.2, teams.15), from facts alone
    (code.7): herdr's status of it, whether it waits on a question in its pane, whether its session received a batch
    (True, False, or what crew could not read of that) and whether a summary was written since its last start.
    ("afresh", words): it sits idle or done, at no question, having received no batch and written no summary, so
    nothing of a batch is lost by ending it, and crew ends it and starts the batch's reviewer afresh. ("refuse",
    words) otherwise: one at work, or that took its batch or wrote a summary, is still reviewing, ended by the wait at
    its summary; one at a question waits on the user; and one crew can't read is never ended on a guess (read.1)."""
    still = f"{agent} is still reviewing a batch: crew review {label} --wait waits for its summary"
    if status == "blocked" or (asking and status in ("idle", "done")):
        return "refuse", f"{agent} is waiting on a question in its pane: answer it there; crew ends no reviewer at a question"
    if status not in ("idle", "done") or took is True or written:
        return "refuse", still
    if took is not False:
        return "refuse", f"crew can't tell whether {agent} took a batch: {took}; it is left as it is"
    return "afresh", f"{agent} sat {status} having taken no batch and written no summary: crew ends it and starts the batch's reviewer afresh"


# How every batch a standing reviewer is sent opens (review_prompt), which its transcript holds once it took one.
REVIEW_OPENS = "Review batch"


def reviewer_up(fleet, label, m):
    """reviewer_up_said's (how, words) for the drive's reviewer, m's, when herdr reads it up, else None: read from
    herdr's reading of it and its session's transcript, where it took a batch once it holds REVIEW_OPENS (crew.Pane, as
    send_taken reads it), and whether a summary was written since its last start on this host, taken or not."""
    if not m.status("reviewer"):
        return None
    agent = m.agent_of("reviewer")
    pane = crew.Pane(fleet, agent)
    status, asking, sid, unread = pane.reading()
    got = unread or (pane.received(sid, 0, REVIEW_OPENS) if sid else "crew found no session for it")
    took = got if isinstance(got, str) else got.get("received") if isinstance(got.get("received"), bool) else (
        f"crew's reading of its transcript on {pane.host} gave no answer crew reads")
    start = next((e for e in reversed(local_entries(label, BATCH_DAYS))
                  if e.get("Act") == "review.start" and (e.get("Batch") or "").isdigit()), None)
    try:
        mtime = batch_file(label, start["Batch"]).stat().st_mtime if start else None
    except OSError:
        mtime = None
    return reviewer_up_said(label, agent, status, asking, took, batch_written(start, mtime))


CONSOLE_TABS = ("shell", "flow", "rail", "board")


def console_asked(words):
    """The tabs crew console up names after its label: flow, rail and board, each at most once, in any order; any other
    word refused, naming the three."""
    for w in words:
        w in CONSOLE_TABS[1:] or fail(f"crew console up opens the tabs flow, rail and board; there is no tab {w}")
        words.count(w) == 1 or fail(f"crew console up names the {w} tab twice")
    return set(words)


def console_tabs(asked, recorded, follower):
    """Which of the console's tabs crew console up opens, keeps and forgets (code.7), from the tabs asked, each tab the
    console's panes file records with whether herdr still has its pane, and who follows on the host (board.follower_of).
    Wanted are the shell tab always, each tab asked, and the rail tab while no host job follows, since the rail tab is
    then the host's follower, a follower crew can't read taken as no job so a host is never left with none (read.1).
    open is each wanted tab with no live pane, in the order shell, flow, rail, board; keep each recorded tab whose pane
    is live, which every later up keeps, named or not; forget each recorded tab whose pane is gone and that is not
    wanted, since the user closed it."""
    wanted = {"shell"} | set(asked) | (set() if follower == "job" else {"rail"})
    live = {t for t, up in recorded.items() if up}
    return ([t for t in CONSOLE_TABS if t in wanted and t not in live], [t for t in CONSOLE_TABS if t in live],
            [t for t in CONSOLE_TABS if t in recorded and t not in live and t not in wanted])


def console_cmd(fleet, a):
    """crew console up|down <label> [flow] [rail] [board]: the drive's console on this host, in the `console`
    workspace of this host's `<label>` session, its tabs in the folder this host's teams file's `consoles` gives the
    drive and refused, with nothing opened, where it names none (crew.operator_session; record 0064), starting no agent
    (record 0035): a shell tab with the crew the host has
    installed on its path (crew.crew_command), the crew every tab runs, and the tabs named after the label: flow,
    following the run record; rail, the rail the host's follower writes above and a shell below; and board, drawn from
    the same read. The rail tab opens of itself too while no host job
    follows (board.follower_here), since its loop is then the host's follower (console_tabs). Up keeps each tab already
    open, named or not, and a tab whose pane holds its shell alone, as herdr brings each pane back after a restart, runs
    its command there again, while one running anything else is left and said (crew.tab_holds, read.4); a tab the
    user closed is forgotten and opened again only when named. swancloud's timer runs it every five minutes. An operator
    agent this host's console held before the operator was a main-level role is ended and its workspace closed once it
    is not working (retire_operator). Down closes the console's tabs."""
    import board  # board imports this module
    c = crew.standing(fleet, "console", a.label)
    c.ensure()
    installed = crew.crew_command()
    label, crew_cmd = a.label, shlex.quote(installed)
    if a.act == "down":
        not a.tabs or fail(f"crew console down {label} closes every tab of the console, and names none")
        c.teardown()
        print(f"{label}'s console on {crew.this_host()} is closed")
        return
    asked = console_asked(a.tabs)
    retire_operator(fleet, label)
    words = {"flow": ["events", "--follow", "--label", label], "rail": ["_rail", label], "board": ["_board", label]}
    path = f"export PATH={shlex.quote(os.path.dirname(installed))}:$PATH"
    opens, keeps, forgets = console_tabs(asked, {t: c.herdr.live(c.pane(t)) for t in CONSOLE_TABS if c.pane(t)}, board.follower_here())

    def shell_below():
        if not c.herdr.live(c.pane("rail-shell")):
            c.put("panes", "rail-shell", c.split(c.pane("rail"), "down", c.cwd))
            c.herdr.run("pane", "run", c.pane("rail-shell"), path)

    def keep(tab):
        run, pane = f"bash {crew_cmd} {shlex.join(words[tab])}", c.pane(tab)
        held, what = crew.tab_holds(c.herdr.process_info(pane), words[tab])
        if held == "shell":
            c.herdr.run("pane", "run", pane, run)
            print(f"{label}'s {tab} tab ({pane}) held its shell alone; its {tab} runs there again")
        elif held == "other":
            print(f"{label}'s {tab} tab ({pane}) runs {what}, not crew's {tab}; crew left it", file=sys.stderr)
        elif held is None:
            print(f"{label}'s {tab} tab ({pane}): {what}; crew left it", file=sys.stderr)
    for tab in CONSOLE_TABS:
        if tab in forgets:
            c.drop("panes", tab)
            if tab == "rail":
                c.drop("panes", "rail-shell")
        elif tab in opens:
            c.opened("console", tab, c.cwd, tab)
            c.herdr.run("pane", "run", c.pane(tab), path if tab == "shell" else f"bash {crew_cmd} {shlex.join(words[tab])}")
        elif tab in keeps and tab != "shell":
            keep(tab)
        if tab == "rail" and tab in opens + keeps:
            shell_below()


def retire_operator(fleet, label):
    """The operator agent this host ran in its operator session before record 0035, `<label>-operator-<host>`, ended,
    and the panes crew recorded in its `operator` workspace closed, once it is not working; one working, or one that
    did not exit, is left and said, and its console opens beside it. Nothing to do once it is gone."""
    state = pathlib.Path.home() / f".local/state/crew/{label}-operator"
    if not (state / "panes").exists():
        return
    host = crew.this_host()
    old = crew.Agents(fleet, "retired", label, label, label, state, ("operator",), str(state), host, host)
    old.agent_of = lambda role: f"{label}-operator-{host}"
    if old.status("operator") == "working":
        print(f"{label}-operator-{host} is working; it is no longer started (the operator is {label}-operator, at the main level), "
              f"and once it is not working the console ends it", file=sys.stderr)
        return
    why = old.stop("operator")
    if why:
        print(why, file=sys.stderr)
        return
    # Only the panes crew recorded there: a tab the user opened in that workspace stays, and the workspace goes with
    # its last pane.
    for _, pane, *_ in old.lines("panes"):
        if old.herdr.live(pane):
            old.herdr.run("pane", "close", pane)
    os.replace(state, state.with_name(f"{label}-operator.retired-{int(time.time())}"))
    print(f"{label}-operator-{host} is ended and its operator tabs closed: the operator is {label}-operator, at {label}'s main level")


def revive_cmd(fleet, a):
    """crew revive, after a restart: on this host, each main level's standing role, in each of its sessions, whose pane
    came back with no agent in it, or dead, closed and opened again in its layout first (crew.revived, teams.2), picked
    up from its last conversation and greeted; one taken down with crew main down stays down. What can't be revived is
    said, and the rest still are. Nothing is revived while this host is held (teams.19): crew go revives it."""
    not_held()
    greetings = []
    for label in crew.here(fleet):
        for agents in crew.mains(fleet, label):
            greetings += revive_main(fleet, label, agents)
    greeted(greetings)


def revive_main(fleet, label, agents):
    """One session of a main level revived (revive_cmd): the greetings it set going."""
    try:
        if not agents.lines("panes"):
            return []
        if agents.down():
            print(f"{label} was taken down; it stays down")
            return []
        back, ways = [], {r: crew.revived(agents.herdr.item(agents.pane(r)), agents.status(r)) for r in agents.standing}
        if "dead" in ways.values():
            agents.panes()
        for role in agents.standing:
            if not ways[role]:
                continue
            if ways[role] == "empty":
                crew.nap(10)
                if agents.status(role, fresh=True):  # herdr may still be resuming it
                    continue
            if not agents.start(role, "resume"):
                continue
            agents.record("agent.resume", f"main({label}): resume {agents.agent_of(role)}", [role])
            back.append(role)
        return greeting(fleet, agents, back)
    except Refusal as e:
        print(e, file=sys.stderr)
        return []


# ----------------------------------------------------------------------------------------------- crew bolts

def bolts_view(fleet, a):
    label = default_label(fleet, a)
    labels = [label] if label else list(fleet["drives"])
    errors = {}
    found = plans(fleet, labels, errors)
    runs = rail_runs(found)
    held = [(t, b.name()) for l, _, _, p in found if p and l in runs
            for b in p.bolts() if started(b) and a.bolt in (None, b.name()) for t in [known_at(fleet, l, b, runs[l])] if t]
    logs = {}  # each drive's run record, its bolts' landings read from it (landing_phase), or why it can't be read
    for l, _, _, p in found:
        if p:
            try:
                logs[l] = drive_entries(fleet, l)
            except Refusal as e:
                logs[l] = str(e)
    # Each kit's GitHub fetched once on its host before it is read: what has merged into a bolt is on GitHub (plan.19).
    data = bolts_data(fleet, labels, found, survey(fleet, held, fetch=True), errors, a.bolt, runs, logs)
    if a.bolt and not any(b for p in data["drives"] for pl in p["plans"] for b in pl["bolts"]):
        fail(f"no bolt {a.bolt} in the plans of " + ", ".join(labels))
    if a.json:
        print(json.dumps(data, indent=1))
        sys.exit(1 if errors else 0)
    print(bolts_text(data))
    if errors:
        sys.exit("\n".join(errors.values()))


def bolts_data(fleet, labels, found, sv, errors, bolt=None, runs=None, logs=None):
    """What crew bolts shows, from the plans read (found) and the survey of the hosts holding their bolts (sv): each
    drive's plans, each bolt with the host its work runs on as the runner that took it reported (bolt_at), state, verification (whether its head is the landing of its
    work, as the runner reports it, Stages.verification, for a bolt whose kit was read), units and chores in build order with their kinds and
    stages read from the kits, and fixes, each piece's submission said by its stage as the runner carries it
    (runner.piece_said) and nothing of sluice's queue read (crew record 0056 points 1 and 4); and the queue; the hosts that did not answer and the plans that could not be read. Each started bolt says
    the Flume stream its work runs in, as Flume's status of its places names it (stream), and a bolt given through Flume its units' and chores' stages and its fixes' from the
    runner's records (Stages.crossed, Stages.fixes), each with stage_of's answer (flume), no worktree and no submission
    of crew's, and the runners that could not be read, which hide that work alone (runners_unread; Decisions 8 and 14
    of teams-cross-to-flume-as-their-bolts-land), read once for the command (runs, as Stages takes them, read when
    first needed where not given). Each started bolt carries its head and its landing as its drive's run record
    holds it (logs, {label: entries, or why they can't be read}; landing_phase), queued, again or rejected, each its
    own state (landing_record), and a drive whose record can't be read says why (record_error). With bolt, that
    bolt alone."""
    data = {"drives": [], "unreachable": {h: v["error"] for h, v in sv.items() if not v["ok"]}, "unread": errors, "runners_unread": {}}
    for l in labels:
        log = (logs or {}).get(l)
        part = {"label": l, "plans": [], **({"record_error": log} if isinstance(log, str) else {})}
        for pl, repo, tip, plan in found:
            if pl != l:
                continue
            if not plan:
                part["plans"].append({"repo": repo, "plan": None, "bolts": [], "queue": []})
                continue
            st = Stages(fleet, plan, sv, runs, pl)
            bolts = []
            for b in plan.bolts():
                if bolt not in (None, b.name()):
                    continue
                t = st.at(b)[0] if started(b) else None
                k, _ = st.kit(b) if t else (None, None)
                units = [dict(unit=u.name(), kind=kind_of(u), after=u.all("After"), sources=u.all("Source"), **{
                    x: st.of(u.name())[x] for x in ("stage", "tasks", "worktree")}, flume=st.of(u.name()).get("flume"))
                    for u in plan.work_of(b.name())]
                crossed = started(b)
                fixes = [dict(fix=w, worktree=None, merged=s["stage"] in ("merged", "landed"), flume=s) for w, _, s in st.fixes(b)] if crossed else []
                silent = st.unread(b) if crossed else None
                if silent:
                    data["runners_unread"][silent[0]] = silent[1]
                bk = (k or {}).get("bolts", {}).get(b.name()) or {}
                verified = dict(zip(("state", "said"), st.verification(b, bk.get("head"), bk.get("head_landing")))) if k and bk.get("exists") else None
                bolts.append(dict(bolt=b.name(), repo=b.get("Repo"), goal=b.get("Goal"), sources=b.all("Source"),
                                  host=st.host(b) if crossed else None, state=st.bolt_state(b), base=st.base(b), landing=st.landing(b), verification=verified, units=units, fixes=fixes,
                                  given=b.get("Path"), stream=t["stream"] if t else None,
                                  head=bk.get("head"), landing_record=landing_phase(log, b.name()) if crossed and isinstance(log, list) else None,
                                  carries=bk.get("carries") or {}, carries_error=bk.get("carries_error")))
            queue = [] if bolt else [dict(unit=u.name(), kind=kind_of(u), repo=u.get("Repo"), stage="queued", sources=u.all("Source"))
                                     for u in plan.queue()]
            part["plans"].append({"repo": repo, "plan": tip, "bolts": bolts, "queue": queue})
        data["drives"].append(part)
    return data


def bolts_text(data):
    """crew bolts as text: each plan's branch and tip, each bolt with its repo, host and state, its verification when
    its kit was read, and each unit with its stage, tasks and place, each chore among them with `chore` before its
    stage, each fix with its stage, the
    queue by repo with each unit's and chore's sources, and each host that did not answer. A started bolt's host and
    stream are on its head line (runner.stream_said), with its landing as the run record holds it, queued, again or
    rejected, each in words of its own (phase_said), and a crossed piece's line says its stage as the runner's records give it, its
    Flume place in its place's stead and what goes with its stage after (runner.piece_said); each runner that could not
    be read is named, the stages of the work it runs unknown (Decision 14 of teams-cross-to-flume-as-their-bolts-land)."""
    lines = []
    for p in data["drives"]:
        for pl in p["plans"]:
            if not pl["plan"]:
                lines.append(f"{p['label']}/main  {pl['repo']}  not started: crew state init {p['label']}")
                continue
            lines.append(f"{p['label']}/main {pl['plan'][:7]}  {pl['repo']}")
            for b in pl["bolts"]:
                who = (f"@ {b['host']}" if b["host"] else "not started" if not b.get("given") else "where it runs can't be told") + (
                    f", {runner.stream_said(b['stream'])}" if b.get("stream") else "")
                record_said = landing_line(b.get("landing"), b.get("landing_record"), b.get("head"), b.get("bolt"))
                lines.append(f"{b['bolt']}  {b['repo']}  {who}  {b['state']}" + (f"  {record_said}" if record_said else ""))
                base = runner.base_said(b.get("base") or {})
                if base:
                    lines.append(f"  {base}")
                carry = carries_said(b.get("carries"), b.get("carries_error"))
                if carry:
                    lines.append(f"  landing: held: {carry}")
                if b.get("verification"):
                    lines.append(f"  verification: {b['verification']['state']}, {b['verification']['said']}")
                for u in b["units"]:
                    if u.get("flume"):
                        stage, detail = runner.piece_said(u["flume"])
                        stage = ("chore " if u.get("kind") == "chore" else "") + stage
                        lines.append(f"  {u['unit']:<40} {stage:<12} {flume_place(u['flume'])}  {detail}".rstrip())
                        continue
                    stage = ("chore " if u.get("kind") == "chore" else "") + u["stage"] + (
                        f" {u['tasks'][0]}/{u['tasks'][1]}" if u["stage"] in ("code", "verify") and u["tasks"] else "")
                    where = "places/" + os.path.basename(u["worktree"]) if u["worktree"] else ""
                    lines.append(f"  {u['unit']:<40} {stage:<12} {where}".rstrip())
                for f in b["fixes"]:
                    if f.get("flume"):
                        stage, detail = runner.piece_said(f["flume"])
                        lines.append(f"  {f['fix']:<40} {'fix ' + stage:<12} {flume_place(f['flume'])}  {detail}".rstrip())
                        continue
                    fixed = "fix merged" if f["merged"] else "fix"
                    lines.append(f"  {f['fix']:<40} {fixed:<12} places/{os.path.basename(f['worktree'])}")
            repos = sorted({u["repo"] for u in pl["queue"]})
            for r in repos:
                lines.append(f"queue  {r}")
                for u in (x for x in pl["queue"] if x["repo"] == r):
                    queued = "chore queued" if u.get("kind") == "chore" else "queued"
                    lines.append(f"  {u['unit']:<40} {queued:<12} {', '.join(u['sources'])}".rstrip())
        if p.get("record_error"):
            lines.append(f"{p['label']}'s run record can't be read ({p['record_error']}): no bolt's landing is said from it")
    for h, why in data["unreachable"].items():
        lines.append(f"{h} did not answer ({why}): the stages of its bolts are unknown")
    for what, why in data.get("runners_unread", {}).items():
        lines.append(f"{what} can't be read ({why}): the stages of the work crossed to Flume there are unknown")
    return "\n".join(lines)


def flume_place(s):
    """A crossed piece's Flume place as its line names it, flume/<the place's folder>, a tidied place's time left off;
    nothing before the runner has launched it."""
    return f"flume/{os.path.basename(s['place']).split('@')[0]}" if s.get("place") else ""


# ------------------------------------------------------------------------------------------------- a bolt's time

HOLDERS = ("team", "kit", "team_or_kit", "user", "hold", "nobody")
HOLDER_SAID = {"team_or_kit": "team or kit"}  # a holder as its line names it, where its key is not its words
UNSPLIT = "team or kit: sluice keeps no start of its checks"  # why minutes are the team's or the kit's, said once


def bolt_time(start, end, stages, submissions, cards, holds):
    """Where a started bolt's time went (plan.20, record 0044), a decision of facts alone (code.7): from its newest start
    (start) to end, the time now or its landing, cut at every start and end the facts hold, each piece going to the
    first holder that applies: the team while a stage of its work runs other than a merge; the kit while one of its
    submissions is under test, from the start of its checks to its decision; the team or the kit, unsplit
    (team_or_kit), while one of its submissions is in sluice with no start of its checks crew holds, from its submit to
    its decision, or to end while it stands testing, and for the whole run of a merge stage that ended when crew holds no
    submit of its work within it, so no minute crew can't split goes to the team under its merge stage, nor to the kit;
    the team while a merge stage runs, one of its submissions stands in sluice not under test, or a decided one stood
    from its submit to the start of its checks; the user while a card of the bolt's is open; a hold while one is
    recorded on it; else nobody. A team at work is not idle whatever else happens, a gate's checks are the gate's while
    the merge agent waits on them, and waiting on people counts only while nothing moves, so the shares sum to the age.
    stages are [{start, end, merge, what, work}], work the branch of a unit, chore or fix the stage is of; submissions
    [{submitted, started, decided, state, what, worktree}], worktree the branch it came from, one with no submit, a
    decision alone, placing no minute; cards [{at, until, key}] and holds [{at, until, what}], every time aware and an
    end of None running to end (the design's Decision 3). Returns {age, shares: {holder: minutes}, now: {holder, what,
    since}} in whole minutes, since the time the holder at end began to hold the bolt."""
    facts = []

    def put(a, b, rank, holder, what):
        a, b = max(a, start), min(b or end, end)
        if a < b:
            facts.append((rank, a, b, holder, what))
    for s in stages:
        if not s.get("merge"):
            put(s["start"], s.get("end"), 1, "team", s.get("what"))
        elif s.get("end") and not any(x.get("submitted") and x.get("worktree") is not None and x.get("worktree") == s.get("work")
                                      and s["start"] <= x["submitted"] <= s["end"] for x in submissions):
            put(s["start"], s["end"], 3, "team_or_kit", s.get("what"))
        else:
            put(s["start"], s.get("end"), 4, "team", s.get("what"))
    for s in submissions:
        if not s.get("submitted"):
            continue
        if s.get("started"):
            put(s["started"], s.get("decided"), 2, "kit", s.get("what"))
            put(s["submitted"], s["started"], 4, "team", s.get("what"))
        elif s.get("decided") or s.get("state") == "testing":
            put(s["submitted"], s.get("decided"), 3, "team_or_kit", s.get("what"))
        else:
            put(s["submitted"], None, 4, "team", s.get("what"))
    for c in cards:
        put(c["at"], c.get("until"), 5, "user", c.get("key"))
    for h in holds:
        put(h["at"], h.get("until"), 6, "hold", h.get("what"))
    facts.sort(key=lambda f: (f[0], f[1]))
    cuts = sorted({start, end} | {t for f in facts for t in f[1:3]})
    secs, pieces = dict.fromkeys(HOLDERS, 0.0), []
    for a, b in zip(cuts, cuts[1:]):
        top = next((f for f in facts if f[1] <= a and f[2] >= b), None)
        holder, what = (top[3], top[4]) if top else ("nobody", None)
        secs[holder] += (b - a).total_seconds()
        pieces.append((a, holder, what))
    age = int(max(0.0, (end - start).total_seconds()) // 60)
    shares = {h: int(secs[h] // 60) for h in HOLDERS}
    for h in sorted(HOLDERS, key=lambda h: -(secs[h] / 60 - shares[h]))[:age - sum(shares.values())]:
        shares[h] += 1  # the minutes the floors left, to the largest parts left over, so the shares sum to the age
    holder, what, since = (pieces[-1][1], pieces[-1][2], pieces[-1][0]) if pieces else ("nobody", None, start)
    for a, h, _ in reversed(pieces):
        if h != holder:
            break
        since = a
    return {"age": age, "shares": shares, "now": {"holder": holder, "what": what, "since": since}}


def bolt_facts(entries, plan, bolt, label, host, kit_name, unread=None):
    """What a started bolt's time is split from (bolt_time), read from what crew already keeps, a decision of facts alone
    (code.7): the drive's run record (entries, oldest first, read from its branch, read.5), and no submission of
    sluice's, since the runner's report carries no time of one (crew record 0056 points 1 and 4; plan.20 as
    crew-calls-no-tool-but-its-runner's Decision 5 and crew-lands-each-bolt-through-flumes-base-place's Decision 7 read
    it), so no minute is placed by a submission, a landing's among them. The start is the run record's newest entry not
    refused that made the bolt's branch, bolt.start or an older crew's bolt.give (the-team-machinery-leaves Decision
    11). Its stages are each stage.start of a unit or chore of the bolt's, and each fix.start and fix.merge of a fix of
    it, fix/<bolt>/<f>, not refused, to the next stage.end naming the same stage and agent, or running yet, a merge told
    by its stage/<u>/merge or by fix.merge, each with its work, the unit's, chore's or fix's branch. Its cards are each
    card posted and neither answered nor closed yet, a card lost to its owner and posted again under its key counting
    as one, each from its post to the user's answer on it (card.answer) or its close, whichever comes first, that is
    the bolt's: under land/<bolt>; a batch's holding a unit of it; a proposal's whose plan.propose names the bolt or its
    work, or one of its chain does; its kit's landings card, land/<kit>, while its last post or change names the bolt
    among its rows, from the later of that entry and the end of its last merge (landings_spans); or one whose post
    names the bolt or its work, a question among them, and no question that names neither (design Decision 8). Its
    holds are those of the host its work runs on, each host.hold to its host.go, what for being who held the host (the
    one hold crew records, the design's Decision 4). Returns {start, stages, submissions, cards, holds} as bolt_time
    takes them, submissions always none, or {unknown: why} when the start or the run record can't be read, so no share
    is guessed (read.1)."""
    if unread:
        return {"unknown": "its age can't be told: " + "; ".join(f"{k} could not be read ({v})" for k, v in unread.items())}
    give = next((e for e in reversed(entries) if e.get("Act") in ("bolt.start", "bolt.give") and not e.get("Refused")
                 and f"bolt/{bolt}" in (e.get("On") or [])), None)
    if give is None:
        return {"unknown": f"its age can't be told: the run record of the last {BATCH_DAYS} days holds no start of it"}
    start = utc(give["At"])
    work = {f"{kind_of(u)}/{u.name()}" for u in plan.work_of(bolt)}
    units, fixes = {o.split("/", 1)[1] for o in work}, f"fix/{bolt}/"

    def ours(on):
        return any(o in work or o == f"bolt/{bolt}" or o.startswith(fixes) for o in on)

    def agent_of(on):
        return next((o for o in on if o.startswith("agent/")), None)
    ends = {}
    for i, e in enumerate(entries):
        if e.get("Act") == "stage.end" and not e.get("Refused"):
            for o in e.get("On") or []:
                if o.startswith(("stage/", fixes)):
                    ends.setdefault((o, agent_of(e["On"])), []).append(i)
    stages = []
    for i, e in enumerate(entries):
        act, on = e.get("Act"), e.get("On") or []
        if e.get("Refused") or act not in ("stage.start", "fix.start", "fix.merge"):
            continue
        if act == "stage.start":
            obj = next((o for o in on if o.startswith("stage/")), None) if any(o in work for o in on) else None
            if not obj:
                continue
            _, name, stage = obj.split("/", 2)
            merge, what = stage == "merge", f"{stage} on " + ("chore " if f"chore/{name}" in on else "") + name
            branch = next((o for o in on if o in work), None)
        else:
            obj = next((o for o in on if o.startswith(fixes)), None)
            if not obj:
                continue
            merge = act == "fix.merge"
            what, branch = f"merge of {obj}" if merge else f"fix {obj}", obj
        later = ends.get((obj, agent_of(on)), [])
        j = bisect.bisect_right(later, i)
        stages.append({"start": utc(e["At"]), "end": utc(entries[later[j]]["At"]) if j < len(later) else None, "merge": merge, "what": what,
                       "work": branch})
    last_merge = max((s["end"] for s in stages if s["merge"] and s["end"]), default=None)

    chain, named = {}, set()

    def first(p):
        while chain.get(p, p) != p:
            p = chain[p]
        return p
    for e in entries:
        if e.get("Act") == "plan.propose" and not e.get("Refused"):
            ps = [first(o) for o in e.get("On") or [] if o.startswith("proposal/")]
            for p in ps[1:]:
                chain[p] = ps[0]
            if ps and ours(e["On"]):
                named.add(ps[0])
    named = {first(p) for p in named}
    held_units = {f"batch/{n}": [u for u, *_ in us] for n, _, us in batches(entries)}
    open_, lost, spans, key_of, shows = {}, {}, [], {}, {}
    for e in entries:
        act, card = e.get("Act"), e.get("Card")
        if act in ("card.post", "card.update") and card and not e.get("Refused"):  # the rows each post or change showed
            shows.setdefault(card, []).append((utc(e["At"]), e.get("Heads")))
        if act == "card.post" and card and not e.get("Refused"):
            k = e.get("Key") or card
            key_of[card] = k
            if k not in open_:
                open_[k] = dict(lost.pop(k), cards=set(), answered=None) if k in lost else {  # an answer to a lost copy reached nobody
                    "at": utc(e["At"]), "key": e.get("Key"), "by": e.get("By"), "on": e.get("On") or [], "cards": set(), "all": set(),
                    "answered": None}
            open_[k]["cards"].add(card)
            open_[k]["all"].add(card)
        elif act == "card.answer" and card and not e.get("Refused"):  # the user's answer ends the card's wait on them
            c = open_.get(key_of.get(card))
            if c is not None and card in c["cards"] and c["answered"] is None:
                c["answered"] = utc(e["At"])
        elif act == "card.close" and card and not e.get("Refused"):
            k = key_of.get(card) or e.get("Key") or card
            c = open_.get(k)
            if c is None:
                continue
            c["cards"].discard(card)
            if not c["cards"]:  # a card lost to its owner waits for its copy posted again under its key
                del open_[k]
                c["until"] = utc(e["At"])
                if e.get("State") == "lost":
                    lost[k] = c
                else:
                    spans.append(c)
    cards_ = []
    for c in spans + list(lost.values()) + [dict(c, until=None) for c in open_.values()]:
        key, at = c["key"] or "", c["at"]
        until = min((u for u in (c["until"], c["answered"]) if u is not None), default=None)  # its answer or its close
        if key == f"land/{kit_name}" and kit_name != bolt:  # the bolt's only while its rows name it, from its last merge
            cards_ += [{"at": a, "until": u, "key": c["key"]} for a, u in landings_spans(
                sorted(x for card in c["all"] for x in shows.get(card, [])), bolt, last_merge, until)]
            continue
        if key.startswith("batch/"):
            mine = any(u in units for u in card_part(key, held_units.get(key.partition("-")[0], [])))
        elif key.startswith("proposal/"):
            mine = first(key) in named
        else:
            mine = key == f"land/{bolt}" or key.startswith(f"land/{bolt}/") or ours(c["on"])
        if mine and (until is None or until > at):
            cards_.append({"at": at, "until": until, "key": c["key"]})

    holds, held = [], None
    for e in entries:
        if f"host/{host}" in (e.get("On") or []) and not e.get("Refused"):
            if e.get("Act") == "host.hold" and held is None:
                held = {"at": utc(e["At"]), "what": f"its host {host} is held by {e.get('By')}"}
            elif e.get("Act") == "host.go" and held is not None:
                holds.append(dict(held, until=utc(e["At"])))
                held = None
    return {"start": start, "stages": stages, "submissions": [], "cards": cards_,
            "holds": holds + ([dict(held, until=None)] if held else [])}


def landings_spans(shown, bolt, last_merge, until):
    """The spans a kit's landings card holds a bolt for the user (crew-board "A card under the bolt's key, a batch's,
    a proposal's or its landings card is the bolt's", design Decision 8), from facts alone (code.7): shown, each post or change of the card's (copies posted
    again under its key among them), (when, its Heads or None), oldest first; the bolt; the end of its last merge,
    None while none has ended; and the card's end, its answer or its close, None while it waits. From each post or
    change whose rows name the bolt, one recorded with no Heads naming every bolt as before crew recorded heads, from
    the later of it and the last merge, to the next that does not name it or the card's end; none before the bolt's
    last merge has ended. [(at, until)]."""
    if last_merge is None:
        return []
    out, since = [], None
    for when, heads in shown:
        names = heads is None or bolt in {b for b, _, _ in card_heads(heads)}
        if names and since is None:
            since = when
        elif not names and since is not None:
            out.append((since, when))
            since = None
    if since is not None:
        out.append((since, until))
    out = [(max(a, last_merge), u) for a, u in out]
    return [(a, u if until is None or u is None else min(u, until)) for a, u in out
            if (u is None or u > a) and (until is None or until > a)]


def span(m):
    """Minutes in their two largest units, as age says a time ago: <1m, 14m, 3h 05m, 2d 04h."""
    if m < 1:
        return "<1m"
    if m < 60:
        return f"{m}m"
    h, m = divmod(m, 60)
    if h < 24:
        return f"{h}h {m:02d}m"
    d, h = divmod(h, 24)
    return f"{d}d {h:02d}h"


def time_said(tm, now):
    """A started bolt's time as its head line on the board and its land line on the rail end with it (the design's
    Decision 5 of a-bolts-row-shows-its-age-and-who-holds-it): its age, each holder's minutes in HOLDERS' order but a
    holder that held none, and who holds it now and since when, the card's key for the user, the submission for the
    kit, the stage for the team, what the hold is for, or nobody, with no word of a stall (teams.23 retires with
    the-team-machinery-leaves), `3h 05m: team 2h 10m, kit 12m, user 40m; user since 14:02, batch/12`; minutes crew can't split named `team or kit`,
    and why, once (UNSPLIT); or why it can't be told, after its age once that is known (time_at)."""
    if "unknown" in tm:
        return (f"{span(tm['age'])}; " if "age" in tm else "") + tm["unknown"]
    shares = ", ".join(f"{HOLDER_SAID.get(h, h)} {span(tm['shares'][h])}" for h in HOLDERS if tm["shares"][h])
    n = tm["now"]
    since = utc(n["since"]) if isinstance(n["since"], str) else n["since"]
    at = f"{since.astimezone():%H:%M}" if since.astimezone().date() == now.astimezone().date() else f"{since.astimezone():%Y-%m-%d %H:%M}"
    who = (f"held since {at}: {n['what']}" if n["holder"] == "hold" else
           f"nobody since {at}" if n["holder"] == "nobody" else f"{HOLDER_SAID.get(n['holder'], n['holder'])} since {at}, {n['what'] or 'a question'}")
    return span(tm["age"]) + (f": {shares}" if shares else "") + f"; {who}" + (f"; {UNSPLIT}" if tm["shares"]["team_or_kit"] else "")


def held_time(fleet, entries, unread, plan_, b, k, now):
    """A started bolt's time to now, as its rows carry it (plan.20): bolt_time's split of bolt_facts' facts, read from the
    drive's run record (entries, oldest first, and unread, its branches that could not be read) and its kit as the
    gather or the host's follower last read it (k, Stages.kit's), for where its work runs and its name; no minute is
    placed by a submission, since the runner's report carries no time of one (bolt_facts); since as ISO 8601, so the board's JSON carries it, and the words its lines end with (time_said). The board and the rail each call it at the time they draw, from the same read, so
    the two never differ for one bolt and a redraw from a kept read ages it reading nothing."""
    t = (k or {}).get("at") or {}  # where its work runs (Stages.kit)
    facts = bolt_facts(entries, plan_, b.name(), t.get("label"), t.get("machine"), b.get("Repo") or ((k or {}).get("kit") or {}).get("name"),
                       unread)
    tm = time_at(facts, now)
    if "now" in tm:
        tm = dict(tm, now=dict(tm["now"], since=tm["now"]["since"].astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")))
    return dict(tm, said=time_said(tm, now))


def time_at(facts, end):
    """A started bolt's time to end, from its facts (bolt_facts): bolt_time's split, or, when the facts can't be told,
    {unknown: why}, with its age in minutes once its start was read."""
    if "unknown" in facts:
        return {"unknown": facts["unknown"], **({"age": int(max(0.0, (end - facts["start"]).total_seconds()) // 60)} if facts.get("start") else {})}
    return bolt_time(facts["start"], end, facts["stages"], facts["submissions"], facts["cards"], facts["holds"])


# ------------------------------------------------------------------------------------------------- batches

BATCH_DAYS = 60  # how far back the run record is read for constructs and batches
UNIT_AT = re.compile(r"^([a-z0-9][a-z0-9-]*):([a-z0-9][a-z0-9-]*)@([0-9a-f]{4,40})$")


def reviews(label):
    """The drive's reviews folder on its main level's host, where each batch's summary is written."""
    return pathlib.Path.home() / f".local/state/crew/{label}-main/reports"


def batch_file(label, n):
    return reviews(label) / f"batch-{label}-{n}.md"


def units_of_batch(e):
    """A review entry's units, in order, as (unit, the name between, commit): the unit's bolt, or in an entry written
    before a batch named its bolt, the team its work ran with, read as written (Decision 8 of the-team-machinery-leaves)."""
    return [m.groups() for m in (UNIT_AT.match(w) for w in (e.get("Units") or "").split()) if m]


def drive_entries(fleet, label, days=BATCH_DAYS):
    """The drive's run record from days back, read from its branch alone, no host asked for it (read.5); refused
    naming the branch when it cannot be read (read.1), since what is due can't be told without it."""
    since = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=days)).isoformat()
    entries, missing = record.gather(fleet, [label], since)
    return entries if not missing else fail(unread_batches(state_of(fleet, label)[0], missing))


def unread_batches(repo, missing):
    """Why crew can't tell what a batch holds or is due, the branch named that could not be read, {<label>/main: why}."""
    return "crew can't tell which changes have been in a batch: " + "; ".join(f"{k} of {repo} could not be read ({v})" for k, v in missing.items())


def batches(entries):
    """The drive's review batches, oldest first: (number, when, [(unit, its bolt or old team, commit)])."""
    return [(int(e["Batch"]), e["At"], units_of_batch(e)) for e in entries
            if e.get("Act") == "review.batch" and not e.get("Refused") and (e.get("Batch") or "").isdigit()]


def batch_posts(entries):
    """The batch card keys the run record holds a card.post under."""
    return {e["Key"] for e in entries if e.get("Act") == "card.post" and (e.get("Key") or "").startswith("batch/")}


def card_part(key, units):
    """The units of a batch that its card under key holds: every one for batch/<n>, and for batch/<n>-<k>, a card of a
    batch posted as cards of five before a batch was one card, the k-th five."""
    _, _, k = key.split("/")[1].partition("-")
    return units[(int(k) - 1) * 5:int(k) * 5] if k else units


def batch_cards(n, units, posts):
    """Batch n's cards, as (key, the units it holds): one, batch/<n>, holding every unit, or, for a batch posted as
    cards of five before a batch was one card, each batch/<n>-<k> a card was posted under (posts, batch_posts), which
    is read as it was posted until it closes, and no batch/<n>."""
    old = sorted((int(m.group(1)), k) for k in posts for m in [re.fullmatch(rf"batch/{n}-(\d+)", k)] if m)
    return [(k, card_part(k, units)) for _, k in old] or [(f"batch/{n}", units)]


def latest_changes(entries, crossed=None):
    """Each unit's latest change, the commit its last delivered construct left, and when: {unit: (commit, when)}; a unit
    of a bolt given through Flume, whose construct crew does not run, by the commit its place landed at on its bolt
    (crossed, crossed_changes)."""
    latest = {}
    for e in entries:
        if e.get("Act") != "stage.end" or e.get("Ended") != "delivered" or e.get("Refused"):
            continue
        st = next((o for o in e["On"] if o.startswith("stage/") and o.endswith("/construct")), None)
        unit = st.split("/")[1] if st else None
        got = e.get("Delivered") or ""
        if unit and got.startswith(f"unit/{unit}@"):
            latest[unit] = (got.rpartition("@")[2], e["At"])
    latest.update(crossed or {})
    return latest


def crossed_changes(plan, st):
    """Each unit of a bolt given through Flume whose change a review batch reads (Decision 13 of teams-cross-to-flume-
    as-their-bolts-land; review-batches "A crossed team's unit is batched once its change has landed on its bolt"),
    {unit: (commit, when)}: a Flume place's commits live in the runner's clone, which crew does not read, so a unit is
    read once its stage reads merged by the runner's records (st, Stages) and its bolt as the kit was read holds its
    change archived, at the commit its place landed at on the bolt, when the runner carried that; a unit whose
    construct has delivered and whose place is still in code is not yet read."""
    out = {}
    for b in plan.bolts():
        if not started(b):
            continue
        k, _ = st.kit(b)
        archived = ((k or {}).get("bolts", {}).get(b.name()) or {}).get("archived", [])
        for u in plan.units_of(b.name()):
            s = st.of(u.name())
            commit = (s.get("flume") or {}).get("commit")
            if s["stage"] in ("merged", "landed") and commit and u.name() in archived and s.get("carried"):
                out[u.name()] = (commit, s["carried"])
    return out


def batch_closed(entries):
    """The batch card keys the run record holds closed, entries oldest first: those whose last act under the key is a
    card.close, not refused and not lost to its owner, once the user sent the card back with a tap or sent its reading
    session, or closed it in Pending You, or crew's own close of the batch, a batch.close not refused, card or none,
    once the user sent its reading session and no card of it was closed (batch_read_close), or the sweep found it
    waits on nothing. A card posted under the key after it, one followed or raised again, opens the key again, and a
    close as lost leaves it open for its card posted again; a refused post or close changes nothing, since neither
    Pending You nor crew did it. A batch the user answered in a main-level pane (pane_answered) has every key of it
    closed for good, whatever card is posted under one after, in whichever order the hosts' entries came."""
    closed = set()
    for e in entries:
        key, act = e.get("Key") or "", e.get("Act")
        if not key.startswith("batch/") or e.get("Refused") or (act != "batch.close" and not e.get("Card")):
            continue
        if act == "card.post" or (act == "card.close" and e.get("State") == "lost"):
            closed.discard(key)
        elif act in ("card.close", "batch.close"):
            closed.add(key)
    return closed | set(pane_answered(entries))


def pane_answered(entries):
    """Each batch card key of a batch the user answered in their own words in a main-level pane, a batch.answer not
    refused (crew card answer), as {key: (who recorded it, when)}: batch/<n>, and every batch/<n>-<k> any entry is
    under, a card of a batch posted as cards of five before. The first answer of a batch is its answer."""
    answered = {}
    for e in entries:
        if e.get("Act") == "batch.answer" and not e.get("Refused") and (e.get("Batch") or "").isdigit():
            answered.setdefault(int(e["Batch"]), (e.get("By"), e.get("At")))
    keys = {e.get("Key") for e in entries if (e.get("Key") or "").startswith("batch/")}
    out = {f"batch/{n}": by for n, by in answered.items()}
    for k in keys:
        m = re.fullmatch(r"batch/(\d+)-\d+", k)
        if m and int(m.group(1)) in answered:
            out[k] = answered[int(m.group(1))]
    return out


def pane_said(by, at):
    """Where and when a batch was answered in a pane, as pane_answered gives it: "answered in <agent>'s pane at
    <HH:MM>Z"."""
    return f"answered in {by}'s pane at {(at or '')[11:16]}Z"


def batch_settled(entries):
    """The batch card keys whose batch waits on nothing (briefs.12), from the run record's entries, oldest first, as
    {key: why}: each batch/<n>, or for a batch posted as cards of five before, each batch/<n>-<k> (batch_cards), every
    unit of which has landed, a bolt.land not refused naming it, or was dropped since the batch was made, a unit.drop or
    bolt.drop not refused naming it later in the entries' order than the batch's review.batch, since a drop from before
    says nothing of a unit added again under its name, or is held by a later batch not refused, at any commit, since a
    later batch held the unit's latest change when it was made. Landings, drops and batches are only ever added, so a
    key once settled stays so. Whether a card of it closed is not read: batch_closed is what the user's answer closed.
    Each unit is counted once, the first of landed, dropped, held later true of it. The words name the units in the
    batch's order: those landed, those dropped, then, oldest first, each later batch with the units it is the newest to
    hold."""
    landed = {o[5:] for e in entries if e.get("Act") == "bolt.land" and not e.get("Refused") for o in e.get("On") or [] if o.startswith("unit/")}
    made_at, dropped_at = {}, {}
    for i, e in enumerate(entries):
        if e.get("Refused"):
            continue
        if e.get("Act") == "review.batch" and (e.get("Batch") or "").isdigit():
            made_at[int(e["Batch"])] = i
        elif e.get("Act") in ("unit.drop", "bolt.drop"):
            dropped_at.update({o[5:]: i for o in e.get("On") or [] if o.startswith("unit/")})
    made, posts, out = batches(entries), batch_posts(entries), {}
    for n, _, units in made:
        for key, part in batch_cards(n, units, posts):
            names = list(dict.fromkeys(u for u, *_ in part))
            here = [u for u in names if u in landed]
            gone = [u for u in names if u not in landed and dropped_at.get(u, -1) > made_at[n]]
            later = {u: max((m for m, _, us in made if m > n and any(v == u for v, *_ in us)), default=None)
                     for u in names if u not in here + gone}
            if not names or not all(later.values()):
                continue
            why = ([f"{joined(here)} {'has' if len(here) == 1 else 'have'} landed"] if here else []) + (
                [f"{joined(gone)} {'was' if len(gone) == 1 else 'were'} dropped"] if gone else []) + [
                f"batch {m} holds " + ("a newer change of " if len(us) == 1 else "newer changes of ") + joined(us)
                for m in sorted(set(later.values())) for us in [[u for u in later if later[u] == m]]]
            out[key] = "its batch waits on nothing: " + "; ".join(why)
    return out


def awaiting_answer(entries, crossed=None):
    """Each unit whose latest change has been in a batch whose card the user has not answered (briefs.12), as {unit: the
    batch}: no card of a batch holding the change at its commit (batch_cards) is closed (batch_closed), so its row
    still waits on the rail. A unit whose latest change no batch has held is due_changes', and a chore is in no batch.
    crossed, as due_changes takes it."""
    latest, closed, posts, held = latest_changes(entries, crossed), batch_closed(entries), batch_posts(entries), {}
    for n, _, units in batches(entries):
        for key, part in batch_cards(n, units, posts):
            for u, _, sha in part:
                if u in latest and latest[u][0] == sha:
                    held.setdefault(u, []).append((n, key in closed))
    return {u: max(n for n, _ in ns) for u, ns in held.items() if not any(answered for _, answered in ns)}


def due_changes(plan, entries, crossed=None):
    """Each change due for the user's review, in the plan's order: a unit of a started bolt (started) whose latest
    change, its place's landing on its bolt (crossed, crossed_changes) or a construct an older crew ran, left a commit
    no batch has held it at, as (unit, its bolt, commit, when) (review-batches "A unit is batched once its change has
    landed on its bolt")."""
    latest = latest_changes(entries, crossed)
    held = {(u, sha) for _, _, us in batches(entries) for u, _, sha in us}
    out = []
    for u in plan.units():
        b = plan.bolt(u.get("Bolt")) if u.get("Bolt") else None
        if started(b) and u.name() in latest and (u.name(), latest[u.name()][0]) not in held:
            out.append((u.name(), b.name(), *latest[u.name()]))
    return out


def told_since_last_batch(entries):
    """Whether the planner was told a batch is due since the last batch was delivered (a `batch.due` entry after it)."""
    done = [e["At"] for e in entries if e.get("Act") == "review.batch"]
    last = max(done) if done else None
    return any(e.get("Act") == "batch.due" and (last is None or e["At"] > last) for e in entries)


def batch_due(due, entries, setting, now, bolts):
    """Why a batch of the due changes is due now (briefs.12): at the drive's setting, `review`, once `after_changes`
    changes are due or `after_hours` hours have passed since the last batch, or since the first due change was
    constructed when there has been none (record 0064 as amended 2026-11-09), or at once for a bolt
    with every unit merged whose units' latest changes are due. bolts are the team's held bolts as (name, every unit
    merged, its units due). [] when none is, or when the planner was told of a batch since the last one was delivered."""
    if not due or told_since_last_batch(entries):
        return []
    done = [e["At"] for e in entries if e.get("Act") == "review.batch"]
    last = max(done) if done else None
    clock = utc(last) if last else min(utc(at) for *_, at in due)
    why = []
    if len(due) >= setting["after_changes"]:
        why.append(f"{len(due)} changes are due, and a batch is due after {setting['after_changes']}")
    if now - clock >= datetime.timedelta(hours=setting["after_hours"]):
        why.append(f"{setting['after_hours']} hours have passed since " + ("the last batch" if last else "the first of them was constructed"))
    for name, merged, waiting in bolts:
        if merged and waiting:
            why.append(f"bolt {name} has every unit merged, and lands only once {either(waiting)} "
                       + ("has" if len(waiting) == 1 else "have") + " been in a batch the user has answered")
    return why


def batch_reckoners(fleet, found, here):
    """The drives the rail's sweep on this host (here) reckons a batch for (briefs.12; review-batches "A batch is
    reckoned at the rail's sweep on the main level's host" of the-team-machinery-leaves): each whose plan was read and
    whose main level runs here, in the order found, so each is reckoned once, on one host. A batch due by the drive's
    clock, or at once for a bolt whose units have all merged, so reaches the planner with no agent waiting on anything
    (2026-10-19: two bolts merged two hours with no batch begun)."""
    return [label for label, _, _, pl in found if pl and fleet["drives"][label]["machine"] == here]


def reckon_batches(fleet, found, read=None, skip=()):
    """The rail's sweep reckons each drive's batch on its main level's host, this one (batch_reckoners, batch_check),
    once, since a batch is told once; what crew can't read is said on standard error and the rail read stands. With read, the rail read's, the plan, the run record and the stages are taken from it and
    nothing is read again, as the host's follower reckons at every refresh, its read kept; a drive in skip, one the
    follower told at its read's tip already (batch_told), is not reckoned. Returns each drive a batch was due for,
    with whether its planner was told, {label: told}."""
    told = {}
    for label in batch_reckoners(fleet, found, crew.this_host()):
        if label in skip:
            continue
        try:
            said = batch_check(fleet, label, read)
        except Refusal as e:
            print(f"no batch reckoned for {label}: {e}", file=sys.stderr)
            continue
        if said is not None:
            told[label] = said
    return told


def batch_told(told, found, tick):
    """The drives the host's follower reckons no batch for at a refresh (Decision 8 of
    a-rail-refresh-after-no-change-reads-nothing), from what it told at which tip, {label: (tip, whether the tell went
    through)}: one told at the tip its read still holds, until the read takes in the batch.due entry that tell wrote,
    which moves the tip; and one whose tell did not go through, its planner not up, until the clock's next tick (tick),
    so it is tried again once a minute and not at every refresh. A decision on plain facts (code.7)."""
    return {label for label, _, tip, _ in found if tip and label in told and told[label][0] == tip and (told[label][1] or not tick)}


def batch_check(fleet, label, read=None):
    """On the rail's sweep on the drive's main level's host (reckon_batches): the changes due across the drive,
    counted from the run record, make a batch due at the drive's setting, `review`, `after_changes` of them or
    `after_hours` hours since its last batch with at least one due, or at once when a started bolt has every unit merged and some unit's latest change has
    been in no batch. crew then tells the drive's planner once, `batch.due` in the run record, until the next batch
    is delivered (briefs.12). With read, a rail read, the plan, the run record and the stages are its, read nothing
    again (the host's follower's, every refresh, Decision 8 of a-rail-refresh-after-no-change-reads-nothing). Returns
    whether it told the planner, None when no batch is due; refused when crew can't read the run record (read.1)."""
    setting = fleet["drives"][label]["review"]
    if read is not None:
        plan = next((p for l, _, _, p in read["found"] if l == label), None)
        if plan is None:
            return
        if (read.get("unread") or {}).get(label):
            fail(unread_batches(state_of(fleet, label)[0], read["unread"][label]))
        entries = read["logs"].get(label, [])
    else:
        plan = plan_of(fleet, label)
        if plan is None:
            return
        entries = drive_entries(fleet, label)
    # A started unit's change is read once it has landed on its bolt, from the runner's records and its kit (Decision 13
    # of teams-cross-to-flume-as-their-bolts-land).
    crossing = [b for b in plan.bolts() if started(b)]
    st = (Stages(fleet, plan, read["sv"], read.get("runs"), label) if read is not None else
          stages_for(fleet, label, plan, crossing)) if crossing else None
    due = due_changes(plan, entries, crossed_changes(plan, st) if crossing else None)
    if not due or told_since_last_batch(entries):
        return
    bolts = [(b.name(), bool(plan.work_of(b.name())) and all(st.of(u.name())["stage"] in ("merged", "landed") for u in plan.work_of(b.name())),
              [u for u, *_ in due if plan.unit(u).get("Bolt") == b.name()]) for b in crossing]
    why = batch_due(due, entries, setting, datetime.datetime.now(datetime.timezone.utc), bolts)
    if not why:
        return
    planner = f"{label}-planner"
    text = batch_due_said(label, due, why)
    if crew.tell(fleet, planner, text):
        record.emit(label, "batch.due", [f"agent/{planner}"] + [f"unit/{u}" for u, *_ in due], why=f"batch: due, {len(due)} changes",
                    Count=len(due))
        return True
    return False


def batch_due_said(label, due, why):
    """What the planner is told when a batch is due (briefs.12): the changes due, by unit and bolt, why, and how to start
    and wait for its reviewer, whose summary raises the batch's card."""
    return (f"A batch of {label}'s changes is due: " + ", ".join(f"{u} ({bolt})" for u, bolt, *_ in due) + "; " + "; ".join(why)
            + f". Start its reviewer with crew review {label}, and wait for the summary with crew review {label} --wait, which "
            "raises the batch's card and its reading session in your name.")


def reading_command(fleet, label, bolt, sha, unit, archived=False):
    """How the reviewer, on the main level's host, reads a unit's change at a commit in its kit where its bolt's work
    ran (batch_unit_at); a started unit's change archived at the commit of its bolt that holds it (archived; Decision 13
    of teams-cross-to-flume-as-their-bolts-land), its folder found under the archive first."""
    t, here = batch_unit_at(fleet, label, bolt, unit), fleet["drives"][label]["machine"]
    pre = "" if t["machine"] == here else f"ssh -o BatchMode=yes {crew.ssh_of(fleet, t['machine'])} "
    folder = f"openspec/changes/{unit}/"
    if archived:
        folder = "<folder>/"
        found = (f"its change is archived at that commit: find its folder with `{pre}git -C {t['kit']['main']} ls-tree -d --name-only "
                 f"{sha} openspec/changes/archive/`, the one named <date>-{unit}, then ")
    return ((found if archived else "") + f"list its files with `{pre}git -C {t['kit']['main']} ls-tree -r --name-only {sha} {folder}` "
            f"and read each with `{pre}git -C {t['kit']['main']} show {sha}:<path>`")


def review_start(fleet, a):
    """The batch the drive's reviewer is started for: its number (N), the file it writes (FILE), its units as
    <unit>:<bolt>@<commit> (UNITS) and by name (NAMES), and its prompt (PROMPT), naming each change, its bolt, its kit
    and host, and how to read it at its commit. Refused when no change is due."""
    p = crew.drive_of(fleet, a.label)
    label = p["label"]
    CONTEXT["label"] = label
    repo, ref = state_of(fleet, label)
    tip = tip_of(repo, ref) or fail(f"{repo} has no {ref} yet: crew state init {label}")
    plan = read(repo, ref, tip)
    entries = drive_entries(fleet, label)
    # A crossed unit's change is read on GitHub's bolt after a fetch, at the commit holding it archived (Decision 13).
    crossing = [b for b in plan.bolts() if started(b)]
    crossed = crossed_changes(plan, stages_for(fleet, label, plan, crossing, fetch=True)) if crossing else {}
    due = due_changes(plan, entries, crossed)
    due or fail(f"no change of {label} is due for a batch: every unit's latest change has been in one")
    # A start refused for its batch not taken is no batch (review_cmd), so the next start takes its number.
    n = 1 + max([int(e["Batch"]) for e in entries if e.get("Act") in ("review.start", "review.batch") and not e.get("Refused")
                 and (e.get("Batch") or "").isdigit()] or [0])
    f = batch_file(label, n)
    prompt = review_prompt(fleet, label, n, f, due, crossed)
    return dict(N=n, FILE=f, UNITS=" ".join(f"{u}:{bolt}@{sha}" for u, bolt, sha, _ in due), NAMES=" ".join(u for u, *_ in due),
                PROMPT=prompt)


def review_prompt(fleet, label, n, f, due, crossed=()):
    """What batch n's reviewer is sent: the changes due, each with its bolt, kit, host and commit and how to read it
    there, a started unit's archived at that commit (crossed, by name), and the file its summary goes to."""
    at = {u: batch_unit_at(fleet, label, bolt, u) for u, bolt, *_ in due}
    return (f"{REVIEW_OPENS} {n} of {label}, {len(due)} change{'' if len(due) == 1 else 's'}, and write its summary to {f}. "
            + " ".join(f"{u} ({bolt}, {at[u]['kit']['name']} on {at[u]['machine']}, at {sha}): "
                       f"{reading_command(fleet, label, bolt, sha, u, u in crossed)}." for u, bolt, sha, _ in due))


def review_wait(fleet, a):
    """Wait, on the main level's host, for the summary of the batch the reviewer was last started for, written since it
    started: once it is, the batch is recorded (`review.batch`, its number and each unit at the commit its change was
    read at), its card raised with its reading session in the planner's name (raise_batch), and the file's path
    returned. A batch already recorded is returned at once, its card raised if the planner holds none on this host,
    so a batch's card is never changed in place. Stopped with exit 3 when the
    timeout passes first or the session that started the wait has ended (session_ended), refused when the reviewer is
    gone with no summary written."""
    label = crew.drive_of(fleet, a.label)["label"]
    CONTEXT["label"] = label
    entries = local_entries(label, BATCH_DAYS)
    tried = [e for e in entries if e.get("Act") == "review.start" and (e.get("Batch") or "").isdigit()]
    tried or fail(f"no batch of {label} has been started: crew review {label} starts one")
    s = tried[-1]
    not s.get("Refused") or fail(f"batch {s['Batch']} of {label} was not started: {s['Refused']}; crew review {label} starts it again")
    n, f = int(s["Batch"]), batch_file(label, s["Batch"])
    if any(e.get("Act") == "review.batch" and e.get("Batch") == s["Batch"] for e in entries):
        if not cards.card_under(cards.host_entries(record, label, crew.this_host()), f"batch/{n}", f"{label}-planner"):
            raise_batch(fleet, {"label": label, "key": f"batch/{n}"})
        return f
    begun, deadline, session = utc(s["At"]), time.monotonic() + a.timeout / 1000, wait_session()
    while True:
        try:
            written = f.stat().st_mtime >= begun.timestamp()
        except OSError:
            written = False
        if written:
            record.emit(label, "review.batch", [f"batch/{n}"] + [f"unit/{u}" for u, *_ in units_of_batch(s)],
                        why=f"batch({n}): reviewed", Batch=n, Units=s.get("Units"))
            raise_batch(fleet, {"label": label, "key": f"batch/{n}"})
            return f
        if crew.agent_status(fleet, f"{label}-reviewer") is None:
            fail(f"{label}-reviewer is no longer running, and batch {n}'s summary {f} was not written")
        if session_ended(session):
            print(f"{ENDED_WITH}: batch {n}'s review is still running; nothing is recorded yet", file=sys.stderr)
            raise Stopped(3)
        if time.monotonic() >= deadline:
            print(f"batch {n}'s review is still running after the wait's {a.timeout} ms: nothing is recorded yet", file=sys.stderr)
            raise Stopped(3)
        time.sleep(POLL)


def review_asked(fleet, label, a):
    """crew review <label> for a drive that runs its reviewer as its kind (design Decision 11, review-batches "A
    reviewer its drive runs as its kind gets its batch as an ask"), on the main level's host, where the reviewer's run writes the summary:
    the batch of changes due asked of the reviewer, a `batch` ask naming batch/<n>, keyed by it, its words what a
    standing reviewer is sent first (review_start), and the batch's start recorded as today, with no tab opened and no
    agent started; the reviewer's run hands it back with crew review delivered, which asks the planner. --wait refuses,
    since nothing waits on the batch: its delivery reaches the planner as an ask."""
    not a.wait or fail(f"{label} runs its reviewer as its kind, so crew review --wait waits on nothing: the batch's "
                       f"delivery reaches {label}-planner as an ask")
    b = review_start(fleet, argparse.Namespace(label=label))
    ask_write(fleet, label, "reviewer", "batch", agent(), names=f"batch/{b['N']}", key=f"batch/{b['N']}", words=b["PROMPT"])
    record.emit(label, "review.start", [f"batch/{b['N']}", f"agent/{label}-reviewer"] + [f"unit/{u}" for u in b["NAMES"].split()],
                why=f"batch({b['N']}): start review", Batch=b["N"], Units=b["UNITS"])
    print(f"{label}-reviewer is asked batch {b['N']} of {label}, into {b['FILE']}: its run hands it back with crew review "
          f"delivered, which asks {label}-planner")


def batches_taken(turn, held):
    """The batches a reviewer's turn took (design Decision 11), from the turn and the asks on the branch (asks.parse):
    the number of each `batch` ask it took that names batch/<n>, in the order taken. A decision of facts alone (code.7)."""
    by = {asks.took_of(x): x for x in held}
    out = []
    for took in turn["Took"]:
        x = by.get(took)
        m = re.fullmatch(r"batch/(\d+)", (x or {}).get("Names") or "") if x and x.get("What") == "batch" else None
        if m and int(m.group(1)) not in out:
            out.append(int(m.group(1)))
    return out


def batch_written(start, mtime):
    """Whether a batch's summary is written for its start (review_wait's reading): its file's time, mtime, None when
    there is none, at or after the batch's start, its review.start entry, None when this host recorded none."""
    return bool(start) and mtime is not None and mtime >= utc(start["At"]).timestamp()


def review_delivered(fleet, a):
    """crew review delivered [--label L], in a run of a drive's reviewer on its main level's host (design Decision
    11, review-batches "A reviewer's run hands its batch back"): each batch the run's open turn took (batches_taken)
    whose summary is written since its start, delivered as the planner's wait delivered it (review_wait): recorded
    (review.batch) unless it is already, and its card raised with its reading session in the planner's name
    (raise_batch) unless the planner holds it on this host already; then, for a planner that runs as its kind, a
    `delivered` ask of the planner naming batch/<n>, keyed delivered/<n>, with the line that adopts its card, which a
    planner that stands is told as today. A batch whose summary is not written is refused by name once the others are
    delivered. Refused anywhere but the reviewer's run, with no open turn, or a turn that took no batch."""
    run = crew.run_here(fleet)
    run and run[1] == "reviewer" or fail("crew review delivered runs in a run of a drive's reviewer, in its place "
                                         "crew-reviewer--<label>, which hands back the batches its turn took")
    label = run[0]
    a.label in (None, label) or fail(f"{label}-reviewer hands back {label}'s batches, not {a.label}'s")
    CONTEXT["label"] = label
    machine = crew.drive_of(fleet, label)["machine"]
    machine == crew.this_host() or fail(f"{label}'s batches are written on {machine}, where its main level runs, not {crew.this_host()}")
    repo, ref = state_of(fleet, label)
    tip = tip_of(repo, ref) or fail(f"{repo} has no {ref} yet: crew state init {label}")
    held, turns = asks.parse(show(repo, tip, "asks.rec"))
    turn = asks.open_turn(turns, f"{label}-reviewer") or fail(
        f"{label}-reviewer has no open turn: crew role start takes the batches asked of it first")
    taken = batches_taken(turn, held) or fail(f"{label}-reviewer's turn {turn['Turn']} took no batch, so it has none to hand back")
    planner = f"{label}-planner"
    kind = crew.role_runs(fleet, label, "planner") == crew.RUNS_ON_DEMAND
    entries, unwritten = local_entries(label, BATCH_DAYS), []
    for n in taken:
        start = next((e for e in reversed(entries) if e.get("Act") == "review.start" and not e.get("Refused") and e.get("Batch") == str(n)), None)
        f = batch_file(label, n)
        try:
            mtime = f.stat().st_mtime
        except OSError:
            mtime = None
        if not batch_written(start, mtime):
            unwritten.append((n, f))
            continue
        recorded = any(e.get("Act") == "review.batch" and e.get("Batch") == str(n) for e in entries)
        if not recorded:
            record.emit(label, "review.batch", [f"batch/{n}"] + [f"unit/{u}" for u, *_ in units_of_batch(start)],
                        why=f"batch({n}): reviewed", Batch=n, Units=start.get("Units"))
        acts = Heard(fleet, planner if kind else None)
        if not (recorded and cards.card_under(cards.host_entries(record, label, crew.this_host()), f"batch/{n}", planner)):
            raise_batch(fleet, {"label": label, "key": f"batch/{n}"}, acts=acts)
        if kind:
            line = acts.heard or f"Its card is not raised here; crew rail --label {label} raises it."
            ask_write(fleet, label, "planner", "delivered", f"{label}-reviewer", names=f"batch/{n}", key=f"delivered/{n}",
                      words=f"Batch {n} of {label} is reviewed, its summary {f}. {line}")
        print(f"batch {n} of {label} is delivered: {f}")
    not unwritten or fail("; ".join(f"batch {n}'s summary {f} is not written since its start, so it is not delivered" for n, f in unwritten))


# A heading in a batch's summary: a Markdown heading, or a line that opens in bold and says little after it.
HEADING = re.compile(r"^\s*(?:#{1,6}\s+(.+?)[\s#]*|\*\*([^*]+)\*\*(.{0,60}))$")


def summary_paragraph(summary, unit):
    """The paragraph the reviewer opened a unit's section of a batch's summary with, as its brief has it write one
    section per unit headed by the unit's name and its bolt: the first paragraph under the first heading that names the
    unit, a Markdown heading or a short line in bold; None when no heading names it, or a heading follows it at once."""
    named = re.compile(rf"(?<![a-z0-9-]){re.escape(unit)}(?![a-z0-9-])")
    out, found = [], False
    for line in summary.splitlines():
        head = HEADING.match(line)
        if not found:
            found = bool(head and named.search("".join(g or "" for g in head.groups())))
        elif head:
            break
        elif line.strip():
            out.append(line.strip())
        elif out:
            break
    return "\n".join(out) or None


def subject(goal):
    """A bolt's goal as a batch card's title names what a unit is about: its own words, with no closing stop, the first
    letter small but for a word in capitals."""
    s = (goal or "").strip().rstrip(".")
    return s[0].lower() + s[1:] if len(s) > 1 and not s[1].isupper() else s


def batch_subjects(plan):
    """What each unit of the plan is about, as a batch card's title says it: its bolt's goal (subject), by unit. Empty
    when the plan could not be read, and a unit no bolt holds left out: its card names it by its name instead."""
    out = {}
    for u in plan.units() if plan else []:
        b = plan.bolt(u.get("Bolt")) if u.get("Bolt") else None
        if b and b.get("Goal"):
            out[u.name()] = subject(b.get("Goal"))
    return out


def batch_facts(n, entries, summary, subjects):
    """Batch n's card's facts, as cards.batch_card takes them (record 0031 §5), from the run record's entries on the main
    level's host, oldest first, and the reviewer's summary: n, the batch before it, and each unit in the batch's order
    with its bolt (units_of_batch, an older entry's team read as written), the commit the batch read it at, what it is about (subjects, else its name in words) and the
    paragraph the reviewer opened its section with, or a line saying the summary has none. None while the batch's point
    has not come or has passed: the run record holds no batch n, its summary is not there (None), its key is closed
    (batch_closed), the last card act under it a close, but as lost to its owner, or the batch waits on nothing
    (batch_settled), so crew review --wait raises no card for it. A card of it the owner holds open is no reason: the
    act changes it, or posts it again once lost."""
    key = f"batch/{n}"
    held = [e for e in entries if e.get("Act") == "review.batch" and not e.get("Refused") and e.get("Batch") == str(n)]
    if not held or summary is None:
        return None
    if key in batch_closed(entries) or key in batch_settled(entries):
        return None
    previous = max((m for m, _, _ in batches(entries) if m < n), default=None)
    units = [dict(unit=u, bolt=bolt, commit=sha, subject=subjects.get(u) or u.replace("-", " "),
                  paragraph=summary_paragraph(summary, u) or f"The reviewer's summary has no section for {u}.")
             for u, bolt, sha in units_of_batch(held[-1])]
    return dict(n=n, previous=previous, units=units, link=None)


def batch_read(fleet, label, n, acts):
    """Batch n's card's facts as its raise reads them, on the main level's host: from this host's run record, the
    reviewer's summary and the plan's goals (batch_facts), each unit with what its stages recorded as made and the
    runner's report of each preview of it crew asked for (batch_made), and what each line is told (told); None while
    its point has not come or has passed. A summary crew can't read is refused, naming it."""
    f = batch_file(label, n)
    try:
        summary = f.read_text()
    except FileNotFoundError:
        summary = None
    except OSError as e:
        fail(f"crew can't read batch {n}'s summary {f}: {e.strerror or e}")
    facts = batch_facts(n, acts.entries(label), summary, batch_subjects(plan_of(fleet, label)))
    if facts:
        facts["told"] = batch_made(fleet, label, facts, acts)
    return facts


def batch_made(fleet, label, facts, acts):
    """Each unit of a batch's card given what its stages recorded as made (made), read from the copies kept on the host
    its bolt's work ran on (batch_unit_at), through acts.made, one read a host (crew _made, code.3; design Decision 4);
    and, for each made thing that must run, crew's ask of its preview on that host as the runner reports it (up, by
    the thing's name; Decision 7 of a-cards-preview-is-asked-of-the-runner), the ask of its unit's repository and
    revision there (previews_asked) and refused ones among them, so the line says why. A host that does not answer,
    and a unit whose host crew can't tell, is said on standard error, its units carrying none this raise (read.3);
    the runner crew can't read is said the same way, its lines carrying no preview; nothing is refused, since the batch
    stands, and a host is read only for its own kits' places' facts (read.5). Returns what each line was told,
    {request: word}, for the raise to keep once it posts or changes the card (told_kept)."""
    n, by = facts["n"], {}
    for u in facts["units"]:
        try:
            by.setdefault(batch_unit_at(fleet, label, u["bolt"], u["unit"])["machine"], []).append(u["unit"])
        except Refusal as e:
            print(f"batch {n}'s card carries nothing {u['unit']} made: {e}", file=sys.stderr)
    try:
        requests, reads = acts.runner(label)
    except Refusal as e:
        print(f"batch {n}'s card carries no preview this raise: {e}", file=sys.stderr)
        requests, reads = [], {}
    asked, told = runner.previews_asked(requests), {}
    for host, names in sorted(by.items()):
        try:
            got = acts.made(label, host, names)
        except Refusal as e:
            print(f"batch {n}'s card carries nothing {joined(names)} made this raise: {host} did not answer ({e})", file=sys.stderr)
            continue
        for u in facts["units"]:
            if u["unit"] not in names:
                continue
            u["made"], u["up"] = got["made"].get(u["unit"]) or [], {}
            repo = unit_repo(requests, u["bolt"])
            for _, lines in u["made"]:
                for m in map(cards.made_line, lines):
                    ask = asked.get((host, repo, m.get("revision"))) if "branch" in m and "revision" in m and "address" not in m else None
                    if ask is not None:
                        u["up"][m["name"]] = runner.preview_report(reads, ask)
                        told[ask.get("Request")] = runner.preview_word(u["up"][m["name"]])
    return told


def unit_repo(requests, bolt):
    """The repository a batch's unit was built in, as its bolt's newest launch names it (Decision 6 of
    a-cards-preview-is-asked-of-the-runner), which a preview of its line names; None when requests.rec holds none."""
    launches = [r for r in requests if r.get("Act") == "launch" and r.get("Base") == f"bolt/{bolt}"]
    return launches[-1].get("Repo") if launches else None


def raise_batch(fleet, row, acts=None, note=None):
    """A batch's raise (record 0031 §1, briefs.12), for its rail row, of which it reads the label and the key: once the
    reviewer's summary is there, its one card, asked in the planner's name, filed in the kit of its first unit whose bolt crew can place (batch_unit_at),
    its reading session started by the act, and posted through row_card_change, so a card the planner holds that
    Pending You no longer finds is recorded lost and posted again saying its older copy is dead, and one it holds is
    changed with note, by default that crew could not find its earlier copy, RELINKED when its reading opened after it
    was raised (reading_again); nothing while batch_facts finds its point not come or passed, and nothing for a key not
    batch/<n>, an old batch card's among them. crew review --wait calls it once the batch is recorded, and the rail's
    sweep for a row whose card is missing or lost, and for one whose card this host can't reach, handed that older copy
    as the row's dead, when the card is posted saying first that an older copy was lost and to dismiss it in the app
    (cards.posted_again). Run on the main level's host, where the batch and its card are recorded and its summary
    written. What crew can't read is said and refuses nothing, since the batch stands. What each line was told of its
    preview is kept once the card is posted or changed (told_kept; Decision 8 of a-cards-preview-is-asked-of-the-runner).
    The card's id, or None."""
    m = re.fullmatch(r"batch/(\d+)", row["key"] or "")
    if not m:
        return None
    acts, label, n = acts or CardActs(fleet), row["label"], int(m.group(1))
    owner = f"{label}-planner"
    try:
        facts = batch_read(fleet, label, n, acts)
    except Refusal as e:
        print(f"batch {n}'s card is not raised: {e}", file=sys.stderr)
        return None
    if not facts:
        return None
    told = facts.pop("told", {})
    t, whys = None, []
    for u in facts["units"]:
        try:
            t = batch_unit_at(fleet, label, u["bolt"], u["unit"])
            break
        except Refusal as e:
            whys.append(str(e))
    if not t:
        print(f"batch {n}'s card is not raised: crew can't tell where any of its units was built, so it has no kit to be filed "
              f"in: {'; '.join(whys)}", file=sys.stderr)
        return None
    build = built_again(cards.batch_card) if row.get("dead") else cards.batch_card
    return told_kept(label, row["key"], told, row_card_change(fleet, label, owner, build, facts,
                                                              note or "Raised again: crew could not find its earlier copy",
                                                              card_where(card_kit(fleet, t, t["kit"]["name"], t["kit"])), acts))


def built_saying(build, said):
    """A builder whose kit's landings card says first, ahead of its summary, what changed of each bolt it asks for
    again since the user's send that ticked it (said, work_said's words), so the card that asks again says so
    (rail-cards "A ticked bolt whose own work changed is asked again, saying what changed"); build itself with none."""
    if not said:
        return build

    def saying(facts):
        b = build(facts)
        return dict(b, card=dict(b["card"], summary=cards.prose(" ".join(f"{w}." for w in said) + f"\n\n{b['card']['summary']}")))
    return saying


def built_again(build):
    """A builder whose card, posted again under its key once an older copy was lost to its owner, says so first
    (built_copy)."""
    return lambda facts: built_copy(build(facts))


def built_copy(b):
    """A built card posted again under its key once an older copy was lost to its owner: its summary saying so first
    (cards.posted_again), and marked again, since it is the row's card the user can no longer reach and never a
    follow-on with nothing changed, so its post is never withheld (card_posted, row_card_change)."""
    return dict(b, card=cards.posted_again(b["card"]), again=True)


# ------------------------------------------------------------------------------------------------ crew rail

RAIL = ("proposals", "batches", "land", "operations")


def utc(iso):
    """An ISO 8601 time, as git and the run record write it, as an aware datetime."""
    return datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")) if iso else None


def age(at, now):
    """How long ago, in its two largest units: <1m, 14m, 3h 05m, 2d 04h."""
    m = int((now - at).total_seconds()) // 60
    if m < 1:
        return "<1m"
    if m < 60:
        return f"{m}m"
    h, m = divmod(m, 60)
    if h < 24:
        return f"{h}h {m:02d}m"
    d, h = divmod(h, 24)
    return f"{d}d {h:02d}h"


def opener(fleet, host, here, path):
    """The command that opens a file or folder on a host in plannotator: beside the rail when the host is the one it
    runs on, else inline over ssh by the name the teams file's `hosts` gives the host (crew.ssh_of), quoted again for
    the shell on the other end; a path relative to the home ssh starts in there opens the file under that home."""
    if host == here:
        return f"plannotator-tui herdr open {shlex.quote(path)}"
    return f"ssh -t {crew.ssh_of(fleet, host)} plannotator-tui {shlex.quote(shlex.quote(path))}"


# How far back the rail reads the run record for the cards still open.
CARD_DAYS = 14


def rail_record(fleet, found, props, crossed=None):
    """What the rail reads of the run record, in one read of each drive whose plan was read: from 60 days back, for
    the batches and the constructs they hold, or from the day before its oldest open proposal's Opened when that is
    earlier, since Opened is the writing host's date and the record's files are named by the UTC day. Returns when each
    open proposal was proposed, {(label, proposal/<n>): time}, from the earliest plan.propose entry naming it (a
    proposal whose entry isn't found is left out); the cards open, each {label, card, key, on, by, host, at}, from each
    card.post of the last 14 days with a Card that no later card.close of that Card closes, and that no later card.post
    by the same agent under the same Key names another Card for: within one Pending You sign-in a key gives its card
    back, so a second card under it from its owner means the first was lost to it, and the newer is the row's; the
    branch whose record could not be read, {label: {<label>/main: why}}, no host being asked for it (read.5); the landings, each {label, bolt, units, at, by, host}, from each
    bolt.land entry not refused, oldest first; the team each bolt was given to, {(label, bolt): team}, from the newest
    bolt.give entry naming it that was not refused; what the batches hold, {label: {"batches": [(n, at, units)],
    "closed": card keys closed, "posts": batch card keys posted, "due": units whose latest change no batch has held,
    "unanswered": {unit: the batch} whose card the user has not answered that holds its latest change}}, the last two
    None for a drive whose branch could not be read, since then they can't be told; the rail's rows for the
    operations; the entries the operations are read from, {label: entries}, the ops entries of the main level's host
    and the landings, oldest first, which the board's Operation lane reads (ops.environments); and
    every entry read,
    {label: entries}, oldest first, which the sweep (sweep_cards) and the board's design band read. crossed, each
    drive's crossed units' changes, {label: crossed_changes'}, which its due and unanswered units count."""
    times, cards, unread, landings, held, deploys, opses, logs = {}, [], {}, [], {}, [], {}, {}
    today = datetime.datetime.now(datetime.timezone.utc).date()
    fresh = utc(f"{today - datetime.timedelta(days=CARD_DAYS)}T00:00:00Z")
    for l, _, _, plan in [f for f in found if f[3]]:
        since = today - datetime.timedelta(days=BATCH_DAYS)
        opened = [d["opened"] for d in props if d["label"] == l]
        if opened:
            since = min(since, datetime.date.fromisoformat(min(opened)) - datetime.timedelta(days=1))
        entries, missing = record.gather(fleet, [l], since.isoformat())
        unread[l], logs[l] = missing, entries
        r = record_reading(l, entries, plan, fresh, missing, (crossed or {}).get(l))
        times.update(r["times"])
        cards += r["cards"]
        landings += r["landings"]
        held[l] = r["held"]
        import ops  # ops.py imports nothing of this module
        mine = [e for e in entries if (e.get("Act") or "").startswith("ops.") and e.get("Host") == fleet["drives"][l]["machine"]]
        deploys += [dict(r, at=utc(r["at"]), doc=None) for r in ops.rows(fleet, l, mine)]
        opses[l] = sorted(mine + [e for e in entries if e.get("Act") == "bolt.land"], key=lambda e: (e["At"], e["Id"]))
    return times, cards, unread, landings, held, deploys, opses, logs


def record_reading(l, entries, plan, fresh, missing=None, crossed=None):
    """What the rail reads of one drive's run record entries, as rail_record gives it: when each proposal was
    proposed, the cards open (posted since fresh and not closed, the same owner's newer card under a key replacing its
    older, lost to it), the landings, and what the batches hold, the due units
    None while its branch could not be read (missing), as are the units whose latest change waits on the user's
    answer to its batch's card (awaiting_answer). A close refused leaves its card open; a card's close as lost to its
    owner ends that card but not its row, whose card is posted again under its key; and a batch's key is closed while
    its last card act is a close (batch_closed), so a batch card posted again after a close keeps its row, or once its
    batch waits on nothing (batch_settled), whose words are held as settled. crossed, as due_changes takes it. An open
    card the user answered carries answered, {at, answer, heads}, from its first card.answer (design Decision 3 of
    a-wait-on-the-user-is-one-open-card-the-rail-agrees-with); one not answered carries none. The held facts keep, for
    each bolt's land line (card_stand), each land/ key's open card in main-level ops's name, its rows as its last post
    or change showed them and its answer (land_cards), and the sends kept on that key's closed cards (sends,
    landings_sent)."""
    times, posted, closed, landings = {}, {}, set(), []
    for e in entries:
        act = e.get("Act")
        if act == "plan.propose" and not e.get("Refused"):
            for o in e["On"]:
                if o.startswith("proposal/"):
                    times.setdefault((l, o), utc(e["At"]))
        elif act == "card.post" and e.get("Card") and not e.get("Refused") and utc(e["At"]) >= fresh:
            if e.get("Key"):  # the same owner's card under the same key, but another, is the older copy, lost to it
                for c in [c for c, d in posted.items() if (d["key"], d["by"]) == (e["Key"], e.get("By")) and c != e["Card"]]:
                    del posted[c]
            posted.setdefault(e["Card"], dict(label=l, card=e["Card"], key=e.get("Key"), on=(e["On"] or [None])[0],
                                              by=e.get("By"), host=e.get("Host"), at=utc(e["At"])))
        elif act == "card.close" and e.get("Card") and not e.get("Refused"):  # a refused close leaves the card open
            posted.pop(e["Card"], None)
            if e.get("Key") and e.get("State") != "lost":  # a lost card's row still waits, for its card posted again
                closed.add(e["Key"])
        elif act == "card.answer" and e.get("Card") in posted and not e.get("Refused") and "answered" not in posted[e["Card"]]:
            posted[e["Card"]]["answered"] = dict(at=utc(e["At"]), answer=e.get("Answer"), heads=e.get("Heads"))
        elif act == "bolt.land" and not e.get("Refused"):
            bolt = next((o[5:] for o in e["On"] if o.startswith("bolt/")), None)
            if bolt:
                landings.append(dict(label=l, bolt=bolt, units=[o.split("/", 1)[1] for o in e["On"] if o.startswith(("unit/", "chore/"))], at=utc(e["At"]),
                                     by=e.get("By"), host=e.get("Host")))
    settled = batch_settled(entries)
    closed = {k for k in closed if not k.startswith("batch/")} | batch_closed(entries) | set(settled)  # a batch card posted again reopens its row
    # each landings key's open card in ops's name, as its last post or change showed it, and the sends kept on its
    # closed cards (landings_sent), which say how each bolt's card stands (card_stand)
    ops_cards = sorted((c for c in posted.values() if (c["key"] or "").startswith("land/") and c["by"] == f"{l}-ops"), key=lambda c: c["at"])
    land_cards = {c["key"]: dict(card=c["card"], heads=card_heads(shown_heads(entries, c["card"])),
                                 taking=heads_taking(shown_heads(entries, c["card"])), answered=c.get("answered")) for c in ops_cards}
    sends = {k: landings_sent(entries, k, f"{l}-ops") for k in dict.fromkeys(
        e["Key"] for e in entries if e.get("Act") == "card.close" and (e.get("Key") or "").startswith("land/") and e.get("Heads"))}
    held = dict(batches=batches(entries), closed=closed, settled=settled, posts=batch_posts(entries),
                due=None if missing else {u for u, *_ in due_changes(plan, entries, crossed)},
                unanswered=None if missing else awaiting_answer(entries, crossed), refused=refusals(entries), stopped=stops(entries),
                phases=landing_phases(entries),
                forecasts=[e for e in entries if e.get("Act") == "forecast"],
                left=[e for e in entries if e.get("Act") in ("landing.left", "bolt.leave")],
                land_cards=land_cards, sends=sends)
    return dict(times=times, cards=list(posted.values()), landings=landings, held=held)


def rail_rows(fleet, found, sv, props, times, held=None, runs=None):
    """What waits on the user in the plans read, from the open proposals and when each was proposed, the batches the run
    record holds (held, as rail_record reads it), and the kits as surveyed: each row's group, its drive, its card
    key, the time it began to wait (shown as a date alone when that is all that is known), what it is, its commands, and
    the document its card asks the user to read: ("page", label, n) for a proposal, ("batch", label, n) for a batch
    card, whose units and the commits the batch read them at the row holds too, each unit named with its bolt, None for
    a landing. A
    proposal's row is keyed by its chain's card, proposal/<first>, the first proposal it was rewritten from. A
    verify report is no row: its findings are fixed in one round with no card (teams.17). A batch is one row, keyed
    batch/<n>, holding every unit, until its card closes or it waits on nothing (batch_settled); a batch posted as cards
    of five before a batch was one card is a row for each card posted, keyed batch/<n>-<k>, until it closes or the units
    it holds wait on nothing. Each kit with a started bolt whose every unit has merged is one landing row, keyed
    land/<kit>, main-level ops's (record 0031 as amended 2026-10-23), naming each such bolt in the plan's order with
    the host its work runs on and what it waits on (bolts, each {bolt, host, at, can, line}): a bolt can land only once
    its verification is green, its head the landing of its work as the runner reports it (Stages.verification,
    record 0025), every unit's latest
    change has been in a batch whose card the user has answered, no fix is in flight on it, sluice did not refuse its
    landing at its head (refusals, held's refused) and the run record holds no conflict with main forecast at its head
    (main_conflict, held's forecasts); until then its line says which units no batch has held, which batches wait on the
    user's answer, the fix, that its landing was rejected and the bolt is open for work, in sluice's words, or that it
    takes main first (briefs.12); a bolt whose landing the run record has queued, or landing again, with no outcome
    (held's phases, landing_phase) says so and that no work joins it until sluice decides, and is no bolt that can land
    (bolt-teams "The views say a queued landing and leave it out of the bolts that can land"), or for a bolt the user left on the
    kit's landings card (left_of, held's left), that it takes main first once ticked (crew-rail "A left bolt's land line
    says it would take main first once ticked"); and, once the drive's run record was read, how the kit's card
    stands for it, carried, held by the user's send or following (card_stand, stand_said). A bolt given through Flume is a row's on the same terms, its pieces' stages
    and its fixes in flight read from the runner's records (Stages, runner.fixes_on), and each bolt's line says its
    team's stream after its host (runner.stream_said; Decision 14 of teams-cross-to-flume-as-their-bolts-land), its team's
    Flume stream where another's says nothing of slots. A kit's row carries too, ahead of its bolts, each fix of its main whose
    code has delivered and whose submission waits held (runner.main_fixes_waiting, from each drive's requests and
    runners, runs, {label: (requests, readings)}, as rail_runs reads them; Decision 11 of
    teams-cross-to-flume-as-their-bolts-land), a row of its own where no bolt of the kit waits, each line naming ops's
    command for the user's send of it (main_fix_line, fixes, each {fix, host, can, send}). The row's answer tells ops
    to land those that can, in order, and offers nothing while none can."""
    rows, here, held = [], crew.this_host(), held or {}
    for d in props:
        l, n = d["label"], d["proposal"]
        what = [f"proposal {n} ({l}), by {d['by']}: {d['case'].splitlines()[0][:70]}"]
        at = times.get((l, f"proposal/{n}"))
        rows.append(dict(group="proposals", label=l, key=f"proposal/{d.get('first') or n}", at=at or utc(f"{d['opened']}T00:00:00Z"),
                         date=None if at else d["opened"], what=what, doc=("page", l, n),
                         cmds=[("read", f"crew plan proposed {n} --label {l}"), ("open", f"crew plan proposed {n} --label {l} --open"),
                               ("answer", f"crew plan approve {n} --label {l}")]))
    for l, h in held.items():
        main = fleet["drives"][l]["machine"]
        for n, at, units in h["batches"]:
            for key, part in batch_cards(n, units, h.get("posts", set())):
                if key in h["closed"]:
                    continue
                # On another host, the report by its path under the home ssh starts in there (record 0064, Decision 7),
                # for a host the teams file's `hosts` names, opened over its ssh name (opener).
                f = (str(batch_file(l, n)) if main == here else
                     f".local/state/crew/{l}-main/reports/batch-{l}-{n}.md" if main in fleet["hosts"] else None)
                k = key.partition("-")[2]
                card = f", card {k} of {-(-len(units) // 5)}" if k else ""
                rows.append(dict(group="batches", label=l, key=key, at=utc(at), doc=("batch", l, n),
                                 units=[u for u, *_ in part], commits={u: sha for u, _, sha in part},
                                 what=[f"batch {n} ({l}){card}: " + ", ".join(f"{u} ({bolt})" for u, bolt, _ in part)],
                                 cmds=([("open", opener(fleet, main, here, f))] if f else [])
                                 + [("answer", f'crew tell {l}-planner "On batch {n}: "')]))
    for l, _, _, plan in found:
        if not plan:
            continue
        st, kits = Stages(fleet, plan, sv, runs, l), {}
        for b in plan.bolts():
            if not started(b):
                continue
            k, _ = st.kit(b)
            if not k:
                continue
            host = k["host"]
            path = runner.stream_said(k["at"]["stream"])
            units = plan.work_of(b.name())
            stages = [st.of(u.name())["stage"] for u in units]
            at, head = k["bolts"].get(b.name(), {}).get("head_at"), k["bolts"].get(b.name(), {}).get("head")
            if not (stages and at and head and all(x in ("merged", "landed") for x in stages) and not all(x == "landed" for x in stages)):
                continue
            due, waits = held.get(l, {}).get("due"), held.get(l, {}).get("unanswered") or {}
            outside = [u.name() for u in units if due is not None and u.name() in due]
            unread = sorted({waits[u.name()] for u in units if u.name() in waits})
            bk = k["bolts"].get(b.name(), {})
            state, verdict = st.verification(b, head, bk.get("head_landing"))
            if state != "green":  # a bolt's proof is its verification (record 0025, tests.5)
                lands = [f"lands once its verification is green; now {verdict}"]
            elif due is None and l in held:
                lands = [f"whether every unit's latest change has been in a batch can't be told: {l}/main could not be read"]
            else:  # in a batch whose card the user has answered (briefs.12)
                lands = ([f"lands once {either(outside)} " + ("has" if len(outside) == 1 else "have") + " been in a batch, which is due for them"]
                         if outside else []) + ([f"lands once you have answered batch{'' if len(unread) == 1 else 'es'} "
                                                 f"{joined([str(n) for n in unread])}"] if unread else [])
            # A started bolt holds its fixes as Flume places, read from the runner's records (Decision 10).
            fixes = sorted(w for w, _, s in st.fixes(b) if s["stage"] not in ("merged", "landed", "dropped")) if b.get("Path") == "flume" else []
            refused = held_at(held.get(l, {}).get("refused") or {}, b.name(), head)
            stop = stopped_at(held.get(l, {}).get("stopped") or {}, b.name(), head)
            conflict = main_conflict(held.get(l, {}).get("forecasts") or [], b.name(), head)
            phase = (held.get(l, {}).get("phases") or {}).get(b.name())
            kit_name = b.get("Repo") or k["kit"]["name"]
            bk = k["bolts"].get(b.name(), {})
            carry = carries_said(bk.get("carries"), bk.get("carries_error"))
            landing = st.landing(b)
            o = (landing or {}).get("outcome")
            here = not (phase or {}).get("head") or at_head(phase["head"], head)  # the head its last land was posted at
            if o == "stopped" and here and not stop:  # the runner's or Flume's stop, before a read records it
                stop = (landing.get("words") or "").strip().splitlines()[0] if (landing.get("words") or "").strip() else "stopped"
            if o == "legacy":  # it lands under the crew that started it (Decision 9)
                lands = [landing["words"]]
            elif o == "refused" and here:  # Flume refused it at this head, recorded or not: held in Flume's words (rail-cards)
                lands = [landing_line(landing, phase, head, b.name())]
            elif o == "unknown":  # crew can't tell it from the runner's report: said, and why (read.1)
                lands = [landing_line(landing, phase, head, b.name()) + (": no unit, chore or fix joins it until its outcome is read"
                                                                         if phase and phase["state"] in ("queued", "again", "asked") else "")]
            elif o in ("asked", "submitted") or o != "stopped" and phase and phase["state"] in ("queued", "again", "asked"):
                lands = [f"{landing_line(landing, phase, head, b.name())}: no unit, chore or fix joins it until its outcome is read"]
            elif not lands and carry:  # another bolt's work it carries holds it as a conflict does (plan.8)
                lands = [f"held: {carry}"]
            elif not lands and fixes:  # a fix started on the bolt holds its landing
                lands = [f"lands once {either(sorted(fixes))} has merged or been dropped"]
            elif not lands and refused:  # sluice rejected its landing at this head (refused_at), the bolt open for work
                lands = [f"landing rejected at {head[:7]}, open for work: it lands again once a fix moves its head: {refused}"]
            elif not lands and conflict and left_of(held.get(l, {}).get("left") or [], f"land/{kit_name}", {b.name(): head}):
                lands = [f"left by the user: takes main first once ticked, forecast to conflict with main on {joined(conflict[1])}"]
            elif not lands and conflict:  # forecast at this head to conflict with what main holds (main_conflict)
                lands = [f"takes main first: forecast to conflict with main on {joined(conflict[1])}, until a fix "
                         "taking main in moves its head"]
            can = [f"can land on your send of land/{kit_name}"] + (
                [f"its last landing at {head[:7]} was stopped, nothing of the bolt's: {stop.rstrip('.')}; it lands on your next send"]
                if stop else [])  # stopped_at, holding nothing
            # how the kit's card stands for the bolt, once the run record was read (card_stand, design Decision 8)
            stand = card_stand(b.name(), head, not lands, (held[l].get("land_cards") or {}).get(f"land/{kit_name}"),
                               (held[l].get("sends") or {}).get(f"land/{kit_name}") or {}) if l in held else None
            kits.setdefault(kit_name, []).append(
                dict(bolt=b.name(), host=host, at=at, can=not lands, line=f"{b.name()}, on {host}"
                     + (f", {path}" if path else "") + ": " + "; ".join((lands or can) + ([stand_said(stand, kit_name, l, head)] if stand else []))))
        waiting = {}
        for f in runner.main_fixes_waiting(*(runs or {}).get(l, ([], {}))):
            waiting.setdefault(f["kit"], []).append(f)
        for kit_name in list(kits) + [k_ for k_ in waiting if k_ not in kits]:
            bolts, fixes = kits.get(kit_name, []), [main_fix_line(l, kit_name, f) for f in waiting.get(kit_name, [])]
            can = [f"fix {f['fix']}" for f in fixes if f["can"]] + [x["bolt"] for x in bolts if x["can"]]
            items = ([plural_of(len(fixes), "fix of main", "fixes of main")] if fixes else []) + ([plural_of(len(bolts), "bolt", "bolts")] if bolts else [])
            what = [f"{kit_name} ({l}): {' and '.join(items)} {'waits' if len(fixes) + len(bolts) == 1 else 'wait'} to land on its main"
                    + (", in the plan's order" if bolts else "") + f"; each lands on your send of land/{kit_name}"] + [f["line"] for f in fixes] + [x["line"] for x in bolts]
            # no command for main-level ops: the user's send on the kit's card is the one word, which crew carries to the
            # runner itself (crew-lands-each-bolt-through-flumes-base-place, Decision 4)
            rows.append(dict(group="land", label=l, key=f"land/{kit_name}", at=min([utc(x["at"]) for x in bolts] + [f["at"] for f in fixes]),
                             doc=None, what=what, cmds=[],
                             bolts=[{k_: x[k_] for k_ in ("bolt", "host", "can")} for x in bolts],
                             fixes=[{k_: f[k_] for k_ in ("fix", "host", "can", "send")} for f in fixes]))
    return rows


def card_stand(bolt, head, can, card, sends):
    """How a kit's landings card stands for one bolt of its land row (crew-rail "Each bolt's land line says whether its
    card carries, holds or follows it", design Decision 8), from facts alone (code.7): the bolt, its head now and
    whether it can land; card, the open card under land/<kit> in main-level ops's name as record_reading keeps it, None
    or {card, heads: [(bolt, head7, left)], taking, answered: {heads} or None}; sends, the sends kept on that key's
    closed cards, landings_sent's {bolt: head}. ("carries", the head the card shows, or None when it shows the head now)
    while the card waits on the user and shows the bolt as a row; ("holds",) when the card is answered and its answer
    ticked the bolt, or a kept send names the bolt and no open card shows it, since a raise leaves out exactly the bolts
    whose send stands (rows_unsent), so no git read is needed to agree with it; ("follows", whether the card that carries
    it follows an answered one) when the bolt can land and neither holds; None for a bolt that can't land and is no row
    of the card."""
    shown = {b: h for b, h, _ in (card or {}).get("heads") or []}
    answered = (card or {}).get("answered")
    if card and not answered and bolt in shown:
        return ("carries", None if at_head(shown[bolt], head) else shown[bolt])
    if answered and bolt in {b for b, _, _ in card_heads(answered.get("heads"))}:
        return ("holds",)
    if bolt in sends and bolt not in shown:
        return ("holds",)
    return ("follows", bool(answered)) if can else None


def stand_said(stand, kit, label, head):
    """A bolt's card stand (card_stand) in the words its land line ends with, before its time."""
    if stand[0] == "carries":
        return (f"carried by land/{kit} at {stand[1]}, its head now {head[:7]}, waiting on you" if stand[1] else
                f"carried by land/{kit}, waiting on you")
    if stand[0] == "holds":
        return f"held by your send on land/{kit}: crew asks the runner to land it on that send"
    return (f"follows: the card after land/{kit}'s answered one carries it" if stand[1] else
            f"follows: the next card under land/{kit} carries it")


def main_fix_line(label, kit, f):
    """A fix of main's line on its kit's landings row (Decision 11 of teams-cross-to-flume-as-their-bolts-land; crew-rail
    "A delivered fix of main is a line of its kit's landings row, sent as a bolt's is"), from runner.main_fixes_waiting's f: fix main--<name> on its host
    with the first line of its brief, the failure's words, and that it lands on the user's send of its kit's landings
    card, naming no command (crew-lands-each-bolt-through-flumes-base-place, Decision 5), or that the send was carried
    to the runner by its land's request and the runner acts on it; the time it began to wait, Flume's since, else when
    the runner carried the status that shows it waiting. {fix, host, can, send, line, at}, send the card's key."""
    send = f"land/{kit}"
    first = (f["brief"].strip().splitlines() or [""])[0]
    then = (f"can land on your send of {send}" if f["sent"] is None else
            f"sent on the user's word (request {f['sent']}): the runner on {f['host']} submits it")
    at = datetime.datetime.fromtimestamp(f["since"], datetime.timezone.utc) if f["since"] is not None else utc(f["carried"])
    return dict(fix=f"main--{f['name']}", host=f["host"], can=f["sent"] is None, send=send, at=at,
                line=f"fix main--{f['name']} on {f['host']}: {first}; {then}")


def plural_of(n, one, more):
    """n with the words for one or for more."""
    return f"{n} {one if n == 1 else more}"


def card_kind(key):
    """What an open card is, from its key: a row's ("row"), under a key crew raises a row's card under, as record
    0031 keys them or as they were keyed before it (crews_key); a decision record's ("record"), which is no row's; or
    an agent's question ("question"), under a key of its asker's own or none (briefs.11)."""
    kind = crews_key(key or "")
    return "record" if kind == "record" else "row" if kind else "question"


def unjudged(unread, c):
    """Whether it can't be told that an open card is still open: its drive's run record could not be read from its
    branch, so its close may not have been read (read.1). A host that does not answer hides no card's close, which is
    on the branch whatever host recorded it (read.5)."""
    return bool(unread.get(c["label"]))


def record_cards(cards, unread):
    """The open cards under a decision record's key the user has not answered, oldest first: no row's, so never among
    the cards with no row; one they answered waits on its asker (answered_cards). A card is left out while its
    drive's record could not be read, as stray_cards leaves one out, since its close may not have been read."""
    return sorted((c for c in cards if card_kind(c["key"]) == "record" and not c.get("answered") and not unjudged(unread, c)),
                  key=lambda c: (c["at"], c["card"]))


def question_cards(cards, unread):
    """The open questions the four asking roles posted in their own name the user has not answered, oldest first
    (briefs.11), but one whose drive's record could not be read, as record_cards leaves one out; one they answered
    waits on its asker (answered_cards)."""
    return sorted((c for c in cards if card_kind(c["key"]) == "question" and not c.get("answered") and not unjudged(unread, c)),
                  key=lambda c: (c["at"], c["card"]))


def answered_cards(cards, unread, rows, logs):
    """The open cards the user has answered that wait on their askers, no row's (crew-rail "An answered question or
    record card no longer waits on the user", design Decision 3), oldest first: each answered question, each answered
    decision record's card, and each kit's landings card whose row is gone while a bolt the user's send ticked waits to
    land (send_waits, the sweep leaving it); none whose drive's record could not be read. A decision of facts
    alone (code.7)."""
    rowed = {(r["label"], r["key"]) for r in rows}
    return sorted((c for c in cards if c.get("answered") and not unjudged(unread, c) and (
        card_kind(c["key"]) in ("question", "record") or (
            (c["label"], c["key"]) not in rowed and re.fullmatch(r"land/[a-z0-9][a-z0-9-]*", c["key"] or "")
            and send_waits(logs.get(c["label"], []), c["card"])))), key=lambda c: (c["at"], c["card"]))


def answered_waits(c, entries):
    """Whose act a card the user answered now waits on, in crew's words (crew-rail "A row whose card the user answered
    says whose act it waits on", design Decision 3), by its key's kind, from the card (its owner, by, and its answer,
    answered) and the drive's entries: a kit's landings card, ops's landing of the bolts the send ticked; a
    proposal, the planner's apply once approved or ticked, else its act on it; a batch, the planner's handing on its
    notes; a deploy, ops's record of the word, or, once the word stands (ops.word_stands), the deploy's end; a step,
    ops's record of it; anything else, its owner's act on it. A decision of facts alone (code.7)."""
    import ops  # its decision of a deploy's word alone
    by, a = c["by"], c.get("answered") or {}
    kind = (c["key"] or "").split("/")[0]
    if kind == "land":
        bolts = [b for b, _, _ in card_heads(a.get("heads"))]
        return f"waits on the runner to land {joined(bolts)}" if bolts else f"sent with no bolt ticked: waits on {by} to close it"
    if kind == "proposal":
        said = a.get("answer") or ""
        yes = re.search(r"\bapproved\b", said) or re.search(r"\bticked (?!none)", said)
        return f"waits on {by} to apply it" if yes else f"waits on {by} to act on it"
    if kind == "batch":
        return f"waits on {by} to hand on its notes"
    if kind == "deploy":
        return "your word stands: the deploy's end closes it" if ops.word_stands(c["key"], entries) else f"waits on {by} to record your word"
    if kind == "op":
        return f"waits on {by} to record it"
    return f"waits on {by} to act on it"


def answered_said(c, now):
    """When and what the user answered on a card, as the rail says it: answered <HH:MM> (<age> ago): <answer>."""
    a = c["answered"]
    return f"answered {a['at'].astimezone():%H:%M} ({age(a['at'], now)} ago): {a.get('answer') or 'answered'}"


# What the sweep says first of a kit's landings card it leaves open as the user answered it, waiting on its owner to
# land what they ticked (sweep_cards, send_waits): no act of the sweep's that did not go through (board.card_left).
WAITS_ON_OWNER = "answered: "


def send_waits(entries, card):
    """The bolts the user's send on a kit's landings card still waits to land (rail-cards "The sweep leaves an answered
    landings card while a bolt it ticked waits to land", design Decision 5): each its card.answer's Heads name, the
    first recorded, with no bolt.land or bolt.drop of it since, none refused; [] when the run record (entries) holds no
    answer of the card, or one ticking none. A decision of facts alone (code.7)."""
    answer = next((e for e in entries if e.get("Act") == "card.answer" and e.get("Card") == card and not e.get("Refused")), None)
    if answer is None:
        return []
    since = answer.get("At") or ""
    ended = {o[5:] for e in entries if e.get("Act") in ("bolt.land", "bolt.drop") and not e.get("Refused") and (e.get("At") or "") >= since
             for o in e.get("On") or [] if o.startswith("bolt/")}
    return [b for b, _, _ in card_heads(answer.get("Heads")) if b not in ended]


def stray_cards(fleet, found, sv, rows, cards, unread, logs=None, runs=None):
    """The open cards under a row's key that match no row, oldest first: never a decision record's (record_cards) nor
    a question (question_cards), nor a deploy's whose word stands, from each drive's entries (logs), which the
    deploy's end closes (ops.word_stands), nor a kit's landings card the user answered while a bolt their send ticked
    waits to land (send_waits), which waits on its owner and is listed with the answered cards. A card is left out when whether it has a row can't be known: its drive's
    record could not be read from its branch, so its close may not have been read, or it is a land card of a bolt whose
    host did not answer (runs, the read's runners, rail_runs). A verify report's card, posted before its row went (teams.17), matches none."""
    import ops  # its decision of a deploy's card alone
    plans_, rowed, out = {l: p for l, _, _, p in found if p}, {(r["label"], r["key"]) for r in rows}, []
    for c in cards:
        if (c["label"], c["key"]) in rowed or card_kind(c["key"]) != "row" or unjudged(unread, c):
            continue
        if ops.word_stands(c["key"], (logs or {}).get(c["label"], [])):
            continue
        if re.fullmatch(r"land/[a-z0-9][a-z0-9-]*", c["key"] or "") and send_waits((logs or {}).get(c["label"], []), c["card"]):
            continue
        if c["key"] and blind_land(fleet, c["label"], plans_[c["label"]], sv, c["key"], runs):
            continue
        out.append(c)
    return sorted(out, key=lambda c: (c["at"], c["card"]))


def blind_land(fleet, label, plan, sv, key, runs=None):
    """Whether a card's key is a landing's whose row can't be told, since the host its bolt's work runs on (bolt_host),
    or for a kit's landings card, land/<kit>, a bolt of the kit's, did not answer."""
    m = re.match(r"land/([a-z0-9][a-z0-9-]*)", key)
    if not m:
        return False
    down = lambda b: (lambda h: bool(h) and h in sv and not sv[h]["ok"])(bolt_host(fleet, label, b, runs))
    if plan.bolt(m.group(1)):
        return down(plan.bolt(m.group(1)))
    return any(down(b) for b in plan.bolts() if b.get("Repo") == m.group(1) and started(b))


# How long crew leaves a card, or a row's card, whose last post or close Pending You refused before the sweep tries it
# again, so a refusal that stands is not tried again at the rail tab's pace, every thirty seconds, each try an entry.
CARD_RETRY = 600


def row_gone(key, entries, kits=(), kit_of=None):
    """Why a row's card has no row now, from the run record's entries, oldest first: (outcome, None) when the event
    that ends its row was recorded, so its card is closed with what was done, a proposal applied, a bolt landed or a
    batch answered in a main-level pane, in whose and when (pane_answered); else (None, reason), its card withdrawn
    with why, a proposal or a bolt dropped among them, and a batch that waits on nothing with the words of crew's close
    (batch_settled). A kit's landings card, land/<kit> (kits, the drive's kits' names), that nothing waits to land
    on its main; and a landing card of a bolt's own, from before a kit's card, whose bolt its kit's landing row names (kit_of, {bolt: its kit}), that it is now a row of its kit's landings card (rail-cards
    "A bolt's own landing card gives way to its kit's")."""
    kind, _, rest = (key or "").partition("/")
    thing, _, head = rest.partition("/")
    if kind == "land" and not head and thing in kits:
        return None, f"nothing waits to land on {thing}'s main"

    def last(on, *acts):
        return next((e["Act"] for e in reversed(entries) if e.get("Act") in acts and not e.get("Refused") and on in (e.get("On") or [])), None)
    if kind == "proposal":
        act = last(f"proposal/{thing}", "plan.approve", "plan.drop")
        return (("its proposal was applied", None) if act == "plan.approve" else
                (None, "its proposal was dropped" if act == "plan.drop" else "its proposal is closed"))
    if kind == "land":
        act = last(f"bolt/{thing}", "bolt.land", "bolt.drop")
        return (("its bolt landed", None) if act == "bolt.land" else
                (None, "its bolt was dropped" if act == "bolt.drop" else
                 f"{thing} is now a row of {(kit_of or {})[thing]}'s landings card" if (kit_of or {}).get(thing) else
                 "its bolt no longer waits to land" + (f" at {head}" if head else "")))
    answered = pane_answered(entries) if kind == "batch" else {}
    if key in answered:
        said = pane_said(*answered[key])
        return said[0].upper() + said[1:], None
    settled = batch_settled(entries) if kind == "batch" else {}
    if key in settled:
        return None, settled[key]
    return None, {"batch": "its batch no longer waits to be read", "deploy": "its deploy no longer waits on your word",
                  "op": "its step no longer waits on you",
                  "verify": "a verify report has no card, its findings fixed in one round"}.get(kind, "its row is gone")


def record_settled(key, entries, kits=()):
    """The outcome a decision record's card closes with, under its key in either form (cards.row_object, kits as it
    takes them), its kit as the key names it, from the run record's entries, oldest first: the record's last status
    crew record recorded, "Accepted at <commit>" or "Rejected at <commit>" as crew record closes it, the commit left out
    when the entry names none; None while it is proposed, or none is recorded."""
    obj = cards.row_object(key or "", kits)
    last = next((e for e in reversed(entries) if obj and e.get("Act") in ("record.proposed", "record.accepted", "record.rejected")
                 and not e.get("Refused") and obj in (e.get("On") or [])), None)
    if not last or last["Act"] == "record.proposed":
        return None
    commit = next((c.rsplit("@", 1)[-1][:7] for c in last.get("Commit") or [] if "@" in c), None)
    return last["Act"].split(".")[1].capitalize() + (f" at {commit}" if commit else "")


def record_proposed(key, entries):
    """A decision record's last record.proposed entry, done, under its key in either form (cards.row_object), its kit
    as the key names it, from the run record's entries, oldest first: its State says whether the user settled it in
    the pane, its Form whether its card offered alternatives; None when crew record recorded it proposed nowhere."""
    obj = cards.row_object(key or "")
    return next((e for e in reversed(entries) if obj and e.get("Act") == "record.proposed" and not e.get("Refused")
                 and obj in (e.get("On") or [])), None)


def refused_lately(entries, now, key=None, card=None):
    """Whether crew's last post under a row's key, or its last close of a card, was refused under CARD_RETRY seconds
    before now, so the sweep leaves it for a later read."""
    last = None
    for e in entries:
        if (card and e.get("Act") == "card.close" and e.get("Card") == card) or (key and e.get("Act") == "card.post" and e.get("Key") == key):
            last = e
    return bool(last and last.get("Refused") and (now - utc(last["At"])).total_seconds() < CARD_RETRY)


def reading_unread(entries, key, card, now=None):
    """Whether a batch's, a long proposal's or a landing's card stands without its reading, from this host's run
    record, oldest first (card-sessions "Each rail read tries the reading of a waiting card on this host that stands without it"): a done post or
    change of the card with Unread, or a refused try of the key's reading (card.reading), marks it so from that entry's
    time; a done post or change of the card without Unread clears it; a refused post or change, and a done try, change
    nothing. With now, whether it stands so and its last such entry is CARD_RETRY seconds old or more, so the rail's
    sweep tries it again no sooner than it posts a refused card again."""
    last = None
    for e in entries:
        if e.get("Act") in ("card.post", "card.update") and card and e.get("Card") == card and not e.get("Refused"):
            last = e if e.get("Unread") else None
        elif e.get("Act") == "card.reading" and e.get("Key") == key and e.get("Refused"):
            last = e
    if not last or now is None:
        return bool(last)
    return (now - utc(last["At"])).total_seconds() >= CARD_RETRY


def stood(entries, key, owner):
    """Whether the owner's newest post under a row's key was a follow-on crew withheld, nothing having changed since the
    user answered the card before it (rail-cards "A follow-on with nothing changed is not posted"), from the run
    record's entries, oldest first: the rail's sweep raises no card for that row, and records nothing more."""
    last = None
    for e in entries:
        if e.get("Act") == "card.post" and e.get("Key") == key and e.get("By") == owner:
            last = e
    return bool(last and last.get("State") == cards.STANDS)


def last_refusal(entries, key):
    """The words of the last post under a row's key when it was refused, as the row's card line gives them; None when
    it was not, or there was none."""
    said = None
    for e in entries:
        if e.get("Act") == "card.post" and e.get("Key") == key:
            said = e.get("Refused") or None
    return said


def row_owner(fleet, plan, row):
    """Whose a rail row's card is and the host it runs on, where its card is posted under that host's sign-in: the
    planner's a proposal's and a batch's, and main-level ops's an operation's and a kit's landings card's, land/<kit>,
    on the drive's main machine (rail-cards, record 0031 as amended 2026-10-23)."""
    return row_owner_name(row), fleet["drives"][row["label"]]["machine"]


def row_owner_name(row):
    """Whose a rail row's card is (row_owner), by its group alone: <label>-planner or <label>-ops."""
    return f"{row['label']}-{'planner' if row['group'] in ('proposals', 'batches') else 'ops'}"


def row_cards(cards_, row):
    """A rail row's card and the other cards open under its key (rail-cards "A row's card is the one open in its owner's name, others named apart", design
    Decision 7): the newest open in the row owner's name (row_owner_name), or None, and each other, oldest first, a copy
    in another name or an older one in the owner's, which is not the row's card. A decision of facts alone (code.7)."""
    under = sorted((c for c in cards_ if (c["label"], c["key"]) == (row["label"], row["key"])), key=lambda c: (c["at"], c["card"]))
    own = [c for c in under if c["by"] == row_owner_name(row)]
    return (own[-1] if own else None), [c for c in under if not own or c is not own[-1]]


def last_close_refusal(entries, card):
    """The words of a card's last close when Pending You or crew refused it, as the rail says of an open card whose row
    is gone (rail-cards "The rail names an open card whose row is gone"); None when its last close went through, or
    there was none."""
    said = None
    for e in entries:
        if e.get("Act") == "card.close" and e.get("Card") == card:
            said = e.get("Refused") or None
    return said


def older_than_card(key, proposed):
    """Whether the plan the rail read is older than a proposal's card under key (record 0031 §1, briefs.11): it holds
    no proposal by the number the key names, proposed being the numbers its proposals.rec holds, open or closed, or
    None when they were not read. A proposal is numbered once and never removed (plan.4), and its card is raised at the
    commit that proposed it or past it, so a read that holds the proposal is at or past that commit, and one that does
    not is older than the card: a fresh proposal's row missing from it says nothing of whether the proposal stands.
    False for a key that is no proposal's."""
    m = re.fullmatch(r"proposal/(\d+)", key or "")
    return bool(m) and (proposed is None or int(m.group(1)) not in proposed)


def proposals_held(found):
    """The numbers of the proposals each plan read holds, open or closed, {label: {n}}, from proposals.rec at the tip
    it was read at (found, as plans() gives it), an empty set where the branch holds none; a label whose plan was not
    read is left out, so its proposals' cards are judged against no read (older_than_card)."""
    return {l: {int(p.get("Proposal")) for p in Plan(show(repo, tip, "proposals.rec") or "").recs("Proposal")}
            for l, repo, tip, pl in found if pl}


def sweep_judged(here, rows, cards_, entries, owners, blind, proposed, now, planner=(None, None), design=(None, None), kits=(),
                 kit_of=None, labels=None):
    """What the rail's read does with one drive's cards, of those posted on this host (here), the only ones its
    sign-in reaches: each row's card whose row is gone, to close with why (row_gone), but a land card whose row can't
    be told (blind, the bolts whose team's host did not answer) and a proposal's card on a plan read older than it
    (older_than_card, proposed the numbers of the proposals the read holds), which is left for a later read, its
    proposal maybe still open; each question, whose asker herdr is asked for; and
    each row's card with its row, which Pending You is asked whether it still finds; a deploy's card whose word stands
    left for the deploy's end to close (ops.word_stands); and each decision record's card, under either key form,
    whose record crew record has recorded accepted or rejected since, to close with its status (record_settled), a
    card key's kit read as the key names it. Then each row in record 0031's
    form with no card open on any host, whose owner runs here (owners, {row key: (owner, host)}), to post through its
    kind's raise; but each row whose owner runs here and whose owner's newest card under its key this host's sign-in
    can't reach, one posted from another host and not closed, or one lost to its owner on any host (cards.stranded,
    over the whole record read), to post again through its kind's raise, the older copy named, and not as a row with no
    card; nor a row whose owner's newest post under its key was a follow-on crew withheld, its earlier card's answer
    standing (stood), until an event raises it with something changed. And, where the drive's design agent runs
    (design, its <label>-design and host), each decision record's
    key in record 0031's form under which the design agent posted a card, whose record crew record last recorded
    proposed (record_proposed) and not settled in the pane, and whose card this host's sign-in can't reach so, to post
    again through the record's raise as a row of the group records, with whether its card offered alternatives (the
    Form its last record.proposed records). A card or a row whose last close or post was refused under CARD_RETRY
    seconds ago is left for a later read. And, where the drive's batches' owner runs (planner, (owner, host), row_owner's for a
    batch), each batch card key whose batch waits on nothing (batch_settled), to record crew's close of, with why,
    once: none is under its key yet, and the user's answer has not closed it (batch_closed). And each row's card of a
    batch, batch/<n>, a proposal, proposal/<n>, or a kit's landings, land/<kit>, that the run record shows standing
    without its reading, or a row's of it, last posted, changed or tried CARD_RETRY seconds ago or more
    (reading_unread), to try its reading again. Before all of it, each card of crew's six (cards.row_object names its
    key) whose owner left the fleet, a drive role's name whose label is none of the teams file's labels now
    (cards.role_left), to withdraw in its owner's name with the words that say so (cards.left_said), and none judged
    so with no labels handed; such a card cards no row, so its row is posted in its owner's name as a row with none.
    And each decision record's card still open, its record not settled, whose answer the sweep reads in its owner's
    name (records, cards_owned). A kit's landings card whose row is gone is not judged gone while the user's answer on
    it holds a bolt that has neither landed nor been dropped since (send_waits): its row's absence is one read, a kit not
    read or a head not yet read, and taking the wait as ended from it is a guess (read.1); it is left waiting on its
    owner to land those bolts (waiting_on_owner, design Decision 5).
    Returns {gone: [(card, outcome, reason)], questions: [card], held: [(card, row)], none: [row], again: [(row, older
    card)], settled: [(key, why)], unread: [(card, row)], left_fleet: [(card, words)], records: [card],
    waiting_on_owner: [(card, bolts)]}."""
    import ops  # its decision of a deploy's card alone
    rowed = {r["key"]: r for r in rows}
    out = {"gone": [], "questions": [], "held": [], "none": [], "again": [], "settled": [], "unread": [], "left_fleet": [],
           "records": [], "waiting_on_owner": []}

    def left(c):  # a card of crew's own whose owner left the fleet (cards.role_left)
        return labels is not None and bool(cards.row_object(c["key"] or "")) and cards.role_left(c["by"], labels)
    for c in cards_:
        kind = card_kind(c["key"])
        if c["host"] != here:
            continue
        if left(c):
            if not refused_lately(entries, now, card=c["card"]):
                out["left_fleet"].append((c, cards.left_said(c["by"], c["key"], ops.word_stands(c["key"], entries))))
        elif kind == "record":
            settled = record_settled(c["key"], entries)
            if settled and not refused_lately(entries, now, card=c["card"]):
                out["gone"].append((c, settled, None))
            elif not settled:
                out["records"].append(c)
        elif kind == "question":
            out["questions"].append(c)
        elif c["key"] in rowed:
            out["held"].append((c, rowed[c["key"]]))
            if re.fullmatch(r"(batch|proposal)/\d+|land/[a-z0-9][a-z0-9-]*", c["key"]) and reading_unread(entries, c["key"], c["card"], now):
                out["unread"].append((c, rowed[c["key"]]))
        elif (land_key(c["key"], kits) or (None,))[0] == "kit" and send_waits(entries, c["card"]):
            out["waiting_on_owner"].append((c, send_waits(entries, c["card"])))
        elif (not (c["key"].startswith("land/") and c["key"].split("/")[1] in blind) and not refused_lately(entries, now, card=c["card"])
              and not ops.word_stands(c["key"], entries) and not older_than_card(c["key"], proposed)):
            out["gone"].append((c, *row_gone(c["key"], entries, kits, kit_of)))
    carded = {c["key"] for c in cards_ if not left(c)}  # a card in a name that left the fleet cards no row
    mine = [r for r in rows if cards.row_object(r["key"]) and (owners.get(r["key"]) or (None, None))[1] == here
            and not refused_lately(entries, now, key=r["key"])]
    for r in mine:
        older = cards.stranded(entries, r["key"], owners[r["key"]][0], here)
        if older:
            out["again"].append((r, older))
    again = {r["key"] for r, _ in out["again"]}
    out["none"] = [r for r in mine if r["key"] not in carded | again and not stood(entries, r["key"], owners[r["key"]][0])]
    if design[1] == here:
        posted = (e.get("Key") for e in entries if e.get("Act") == "card.post" and e.get("By") == design[0])
        for key in dict.fromkeys(k for k in posted if re.fullmatch(r"record/[a-z0-9][a-z0-9-]*/\d{4}", k or "")):
            last = record_proposed(key, entries)
            if (not last or record_settled(key, entries) or last.get("State") == "settled in the pane"
                    or refused_lately(entries, now, key=key)):
                continue
            older = cards.stranded(entries, key, design[0], here)
            if older:
                out["again"].append((dict(label=design[0].removesuffix("-design"), key=key, group="records",
                                          alternatives=last.get("Form") == "alternatives"), older))
    if planner[1] == here:
        done = {e.get("Key") for e in entries if e.get("Act") == "batch.close" and not e.get("Refused")} | batch_closed(entries)
        out["settled"] = [(k, why) for k, why in batch_settled(entries).items() if k not in done]
    return out


def stranded_said(entries, card, owner, new):
    """What the sweep says of a row's card this host could not reach once its raise posted it again as new
    (cards.stranded), from the run record's entries, oldest first: lost to its owner when its last close says so, else
    held on the host its post names, which this host's sign-in does not reach."""
    state, host = None, None
    for e in entries:
        if e.get("Card") != card or e.get("Refused"):
            continue
        if e.get("Act") == "card.post":
            host = e.get("Host")
        elif e.get("Act") == "card.close":
            state = e.get("State")
    return (f"lost to {owner}" if state == "lost" else f"held on {host}, which this host's sign-in does not reach") + f": posted again as {new}"


def sweep_sessions(fleet, found, sv, rows, cards, unread, batched, only=None, runs=None):
    """End the card sessions crew started whose card is closed or whose row is gone, and read the landings nothing
    recorded, on every host of each drive whose plan was read, its main
    machine and each its runners answer on as the read read them (runs, hosts_of): one crew card sweep --label <label>
    on each (code.3), handed
    as live every row key less each the record holds as closed with no card open under it (batched, what the batches
    hold as rail_record reads it, {label: {batches, closed, due}}), and as blind the key prefixes it can't judge, batch/
    while the record could not be read from its branch, when no key is taken out for being closed either (read.1). A host the survey
    found not answering is not asked again. Returns what the sweeps did, each {label, host, key, unit, why, said, sent},
    why "its row is gone" or "its card is closed", or, for a reading the user sent that the sweep told its owner of or
    recorded read (sent), "its reading was sent", and the hosts not checked, each {label, host, why} (read.3). only,
    when given, {label: hosts}, asks those hosts alone: the follower's refresh after nothing moved, on the hosts its
    last could not check (sessions_unchecked)."""
    ended, unchecked = [], []
    for l, _, _, plan in found:
        if not plan or (only is not None and not only.get(l)):
            continue
        readings = {f"land/{b['bolt']}" for r in rows if r["label"] == l and r["group"] == "land" for b in r.get("bolts", []) if b["can"]}
        rowed = {r["key"] for r in rows if r["label"] == l} | readings  # each row's, and each landing row's reading
        judgment, landings = sweep_judgment(l, rowed, cards, unread.get(l), batched.get(l, {}), readings), landings_judged(fleet, l, plan, sv, runs)
        for h in hosts_of(fleet, l, runs):
            judged = json.dumps(dict(judgment, landings=landings[h]) if landings.get(h) else judgment)
            if only is not None and h not in only[l]:
                continue
            if h in sv and not sv[h]["ok"]:
                unchecked.append(dict(label=l, host=h, why=f"did not answer ({sv[h]['error']})"))
                continue
            try:
                r = crew.on_machine(fleet, h, crew.crew_argv(fleet, h, "card", "sweep", "--label", l), input=judged)
            except Refusal as e:
                unchecked.append(dict(label=l, host=h, why=str(e)))
                continue
            if r.returncode:
                said = ((r.stderr or "").strip().splitlines() or [f"exit {r.returncode}"])[-1]
                unchecked.append(dict(label=l, host=h, why=f"did not answer ({said})" if r.returncode == 255 else f"its sweep failed ({said})"))
                continue
            try:
                got = json.loads(r.stdout)
            except ValueError:
                got = None
            if not (isinstance(got, list) and all(isinstance(x, dict) and isinstance(x.get("key"), str) and isinstance(x.get("said"), str)
                                                  and (x.get("unit") is None or isinstance(x["unit"], str)) for x in got)):
                unchecked.append(dict(label=l, host=h, why="its sweep printed no list of sessions crew reads"))
                continue
            ended += [dict(label=l, host=h, key=x["key"], unit=x.get("unit"), said=x["said"], sent=x.get("sent") is True,
                           why="its reading was sent" if x.get("sent") is True else "its card is closed" if x["key"] in rowed
                           else "its row is gone") for x in got]
    return ended, unchecked


def sessions_unchecked(unchecked):
    """The hosts a refresh after nothing moved asks to end their card sessions, {label: hosts}: those the last refresh
    could not check (sweep_sessions), and no other, since every other host was judged on the same facts (the
    card-sessions spec, A host the last sweep missed)."""
    out = {}
    for u in unchecked or []:
        out.setdefault(u["label"], set()).add(u["host"])
    return out


def sweep_judgment(label, rowed, cards, unread, batched, readings=()):
    """The rail's judgment a card sweep acts on (read.1): live, every row key of the drive less each the run record
    holds as closed with no card open under it, and every reading of a bolt that is a row of its kit's landings card,
    land/<bolt> (readings), whatever card of the bolt's own was closed under that key before, which is no word on the
    row; blind, the key prefixes it can't judge, batch/ while the record could not be read from its branch, when no key
    is taken out for being closed either."""
    closed = set() if unread else batched.get("closed", set()) - {c["key"] for c in cards if c["label"] == label}
    blind = ["batch/"] if unread else []
    return {"live": sorted((rowed - closed) | set(readings)), "blind": sorted(blind)}


def rail_runs(found):
    """What the rail reads of each drive's runners, once for its read, for the stages of its crossed work (Stages)
    and the fixes of main its landings rows carry (rail_rows, runner.main_fixes_waiting): {label: (requests.rec's
    records at the tip the read found, as written, its runners as read beside it, runners)}, for each drive whose plan holds a bolt given through Flume or whose requests hold a fix of
    main standing; a drive with neither reads no runner."""
    out = {}
    for l, repo, tip, p in found:
        rq = Plan(show(repo, tip, "requests.rec") or runner.REQUESTS).recs("Request") if p and tip else []
        if any((r.get("Work") or "").startswith("fix/main/") for r in runner.standing(rq)) or (
                p and any(b.get("Path") == "flume" for b in p.bolts())):
            out[l] = (rq, runners(repo, l))
    return out


def landings_moved(cards_, mains, kept):
    """Which kits' landings cards main moved under (rail-cards "Main moves under an open card", "Main has not moved"),
    from facts alone (code.7): cards_, each open landings card as (label, kit); mains, the revision of main the survey
    read each kit at in its builder's main checkout, {(label, kit): main_at}, as last fetched (gather.kit, plan.18);
    kept, the revision its rows were last forecast against, {(label, kit): sha}, none when none is kept. Returns (due,
    unread): the cards due a raise, whose kit's main is at another revision than the kept one, or with none kept; and
    those whose kit's read names no revision, an older gather's or a read that failed, which are not judged moved
    (read.2)."""
    due, unread = [], []
    for c in dict.fromkeys(cards_):
        now, was = mains.get(c), kept.get(c)
        if not now:
            unread.append(c)
        elif not was or not (now.startswith(was) or was.startswith(now)):
            due.append(c)
    return due, unread


def rail_read(fleet, labels, board=False, sweep=False):
    """Everything the rail is made from, in one read of the labels' plans, proposals, kits and run record: the plans
    found and the errors of those that could not be read, the survey, the open proposals, the cards, the branches whose
    record could not be read, the landings and gives, the operations' entries, every entry read, each drive's kits
    (kits_at, the repositories its plan and its landings name), and the rows. The survey is of each host where a
    started bolt's work runs, as the runner that took it reported (known_at); with board, of each kit's checkout on its
    drive's main-level host too (main_kit), and the explorations on each kit's main there, for the board
    (board.py), from which the rail's text is made as well.
    With sweep, once the rows are made, the cards on this host are swept under its sign-in (sweep_cards), against the
    proposals the plans read hold (proposals_held), the cards read then being those open once it acted, each kit's
    landings card main moved under is raised again (sweep_moved), the done of each preview crew asked for whose card or
    row is gone is written and each card whose preview the runner reports anew is changed in place, on the drive's
    main machine (sweep_previews, previews_changed), and the card sessions whose card is closed or whose row is gone are
    ended on every host of the labels read; what the sweeps did, and which hosts were not checked, are in the read
    (sweep_sessions). No state is written but by those sweeps' acts. Each drive's runners are read once beside its
    plan (runs, rail_runs), for the stages of its crossed work and the changes its batches count (crossed_changes)."""
    errors = {}
    found = plans(fleet, labels, errors)
    runs = rail_runs(found)  # each drive's runners, read once beside its plan for its crossed work (plan.12)
    held = [(t, b.name()) for l, _, _, p in found if p and l in runs
            for b in p.bolts() if started(b) for t in [known_at(fleet, l, b, runs[l])] if t]
    kits = {l: kits_at(repo, tip, p) for l, repo, tip, p in found}
    if board:  # the explorations on each kit's main, read in the checkout its drive's main-level host keeps of it
        held += [(t, None) for l, ks in kits.items() for k in ks for t in [main_kit_read(fleet, l, k)] if t]
    sv = survey(fleet, held, board=board)
    props = open_proposals(fleet, [l for l, _, _, p in found if p], found)
    crossed = {l: crossed_changes(p, Stages(fleet, p, sv, runs, l)) for l, _, _, p in found if p and l in runs}
    times, cards_, unread, landings, batched, deploys, opses, logs = rail_record(fleet, found, props, crossed)
    read = dict(found=found, errors=errors, sv=sv, props=props, times=times, cards=cards_, unread=unread, landings=landings,
                ops=opses, logs=logs, batched=batched, runs=runs, kits=kits,
                rows=rail_rows(fleet, found, sv, props, times, batched, runs) + deploys)
    if sweep:
        read["proposed"] = proposals_held(found)
        k = READ.follower
        if k is not None and k.cards is None:  # the follower's tick with no read kept to ask from: its one ask, made here
            now = datetime.datetime.now(datetime.timezone.utc)
            k.cards = cards_fetched(fleet, cards_asked(fleet, read, crew.this_host(), now),
                                    owned=owners_asked(fleet, read, crew.this_host(), now) or None)
            k.listed = askers_listed(fleet, askers_asked(fleet, read, crew.this_host(), now))
        read["swept"] = sweep_cards(fleet, read, answers=k.cards if k is not None else None, listed=k.listed if k is not None else None)
        read["cards"] = swept_cards(read["cards"], read["swept"], crew.this_host(), datetime.datetime.now(datetime.timezone.utc),
                                    read["kits"])
        read["moved"] = sweep_moved(fleet, read)
        read["previews"] = sweep_previews(fleet, read)
        read["previewed"] = previews_changed(fleet, read)
        read["ended"], read["unchecked"] = sweep_sessions(fleet, found, sv, read["rows"], read["cards"], unread, batched, runs=runs)
        read["told"] = reckon_batches(fleet, found, read)
    return read


def swept_cards(cards_, swept, here, now, kits=()):
    """The open cards once the sweep acted (sweep_cards): each it closed, withdrew or recorded lost gone, each whose
    answer it recorded carrying it (answered), and each it posted, again or anew, there, posted on this host (here) at
    now under its row's key in its owner's name, on its row's object (cards.row_object, the kits of its drive,
    {label: names}, as it takes them)."""
    gone = {d["card"] for d in swept["done"] if d["did"] in ("closed", "withdrawn", "lost") and d["card"]}
    answers = swept.get("answered") or {}
    cards_ = [dict(c, answered=answers[c["card"]]) if c["card"] in answers and not c.get("answered") else c for c in cards_]
    return [c for c in cards_ if c["card"] not in gone] + [
        dict(label=d["label"], card=d["new"], key=d["key"], on=cards.row_object(d["key"], kits.get(d["label"], ()) if kits else ()), by=d["by"], host=here, at=now)
        for d in swept["done"] if d.get("new")]


def rail_text(fleet, labels, read, now):
    """The rail as crew rail prints it, from a read rail_read made: its groups in order, each row with when it began to
    wait, how long ago that was, what it is, each bolt's line of a kit's landing row ending with the bolt's age and who
    held its time (land_times), the commands that answer it, and its card key with whether a card is open for it,
    whose and its id, by which its owner asks Pending You for it, or, with none open, the words of the refusal of its
    last post, oldest first; then the questions the asking roles put to the user, each with its key, which names it,
    its asker and its age, since no entry holds a card's words (record.3), a row's card being the one open in its
    owner's name and each other card open under its key named apart as not the row's (row_cards), and a card the user
    answered saying when, what, and whose act it now waits on (answered_said, answered_waits), the questions and
    records they answered listed apart, after the records, as answered cards waiting on their askers, with each kit's
    landings card left waiting on ops to land what was ticked (answered_cards); then each card act of an agent's whose reply
    crew could not read (unread_card_acts); then the decision records waiting on the user, each the design
    agent's open card for one, with when it was asked and by whom, and no command, since the card is where it is
    answered; then any open card whose row is gone that the sweep did not close, with the words of its last close's
    refusal where its last close was refused (last_close_refusal), else the host whose rail read closes it; then, from
    a read that swept, each card the sweep closed, withdrew, recorded lost or posted, and each batch it
    closed or left with no card, named so, each drive it changed nothing for and why, each landings card raised
    again as main moved under it and each whose kit's revision of main can't be read (sweep_moved), each card session ended,
    with its host and why, each reading the user sent whose owner it told or that it recorded read, and each host whose
    sessions were not checked. A host is named as not answering only when it holds a bolt of the plans read, so a read
    that surveyed more (the board's) gives the same text. Of a read of several drives, labels may name some: the
    rail of those alone, as a read of them alone would give it (the host's follower's, which reads every drive on
    the host at once)."""
    read = labels_of(read, labels)
    found, rows, cards_, here = read["found"], read["rows"], read["cards"], crew.this_host()
    holding = {h for l, _, _, p in found if p for b in p.bolts() for h in [bolt_host(fleet, l, b, read.get("runs"))] if h}
    sv = {h: v for h, v in read["sv"].items() if h in holding}
    swept = read.get("swept") or {"done": [], "unswept": []}
    logs = read.get("logs") or {}
    lines = [f"What waits on you ({', '.join(labels)}), as of {now.astimezone():%H:%M:%S}"]

    def when(c):
        return f"  {c['at'].astimezone():%Y-%m-%d %H:%M}  {age(c['at'], now):<7}  "
    for g in RAIL:
        lines += ["", g]
        mine = sorted((r for r in rows if r["group"] == g), key=lambda r: (r["at"] is None, r["at"] or now, r["what"][0]))
        if not mine:
            lines.append("  none")
        for r in mine:
            at = r.get("date") or (f"{r['at'].astimezone():%Y-%m-%d %H:%M}" if r["at"] else "-")
            first, *rest = r["what"]
            if g == "land":  # each bolt's line, after the fixes of main ahead of them, ends with its time, drawn now as the board draws it (land_times)
                k = len(r.get("fixes", []))
                rest = rest[:k] + [f"{w}; {t}" for w, t in zip(rest[k:], land_times(fleet, read, r, now))]
            lines.append(f"  {at:<16}  {age(r['at'], now) if r['at'] else '-':<7}  {first}")
            lines += [" " * 29 + w for w in rest]
            lines += [f"    {c + ':':<8}{cmd}" for c, cmd in r["cmds"]]
            refused = last_refusal(logs.get(r["label"], []), r["key"])
            own, others = row_cards(cards_, r)  # the row's one card, its owner's, and any other open under its key apart
            lines += [f"    {'card:':<8}{r['key']}, {answered_said(own, now)}; {answered_waits(own, logs.get(r['label'], []))} ({own['card']})"
                      if own and own.get("answered") else
                      f"    {'card:':<8}{r['key']}, open, asked by {own['by']} ({own['card']})" if own else
                      f"    {'card:':<8}{r['key']}, none open" + (f"; its last post was refused: {refused}" if refused else "")]
            lines += [f"    {'also:':<8}{c['card']}, {c['by']}'s, open under {r['key']}, not the row's card" for c in others]
    questions = question_cards(cards_, read["unread"])
    if questions:
        lines += ["", "questions waiting on you:"]
    for c in questions:
        lines.append(when(c) + f"{c['key'] or 'a question'} ({c['label']}), asked by {c['by']} on {c['host']} ({c['card']})")
    unread_acts = unread_card_acts(logs, now)
    if unread_acts:
        lines += ["", "card acts crew could not read:"]
    for label, e in unread_acts:
        lines.append(f"  {utc(e['At']).astimezone():%Y-%m-%d %H:%M}  {age(utc(e['At']), now):<7}  {e['Act']} by {e.get('By')} "
                     f"on {e.get('Host')} ({label})" + (f", under {e['Key']}" if e.get("Key") else "")
                     + ": Pending You's reply named no card")
    records = record_cards(cards_, read["unread"])
    if records:
        lines += ["", "decision records waiting on you:"]
    for c in records:
        lines.append(when(c) + f"{c['key']} ({c['label']}), asked by {c['by']} on {c['host']}")
    answered = answered_cards(cards_, read["unread"], rows, logs)
    if answered:
        lines += ["", "answered, waiting on their askers:"]
    for c in answered:
        a = c["answered"]
        lines.append(when(c) + f"{c['key'] or 'a question'} ({c['label']}), asked by {c['by']} on {c['host']}, answered "
                     f"{a['at'].astimezone():%H:%M}: {a.get('answer') or 'answered'}; {answered_waits(c, logs.get(c['label'], []))}")
    stray = stray_cards(fleet, found, sv, rows, cards_, read["unread"], logs, read.get("runs"))
    if stray:
        lines += ["", "open cards whose row is gone:"]
    for c in stray:
        lines.append(when(c) + f"{c['key']} ({c['label']}), asked by {c['by']} on {c['host']}")
        refused = last_close_refusal(logs.get(c["label"], []), c["card"])
        lines.append(f"    {'left:':<8}" + (f"its last close was refused: {refused}" if refused else
                                            f"a rail read on {c['host']} closes it, under that host's sign-in" if c["host"] != here
                                            else "a later rail read here closes it"))
    done = [f"  {d['key'] or 'a question'} ({d['label']}), {d['by']}" + (f"'s {d['card'] or d['new']}" if d["card"] or d["new"] else ", no card")
            + f": {d['did']}: {d['words']}" for d in swept["done"]]
    lines += (["", "cards swept:"] + done if done else []) + (
        ["", "cards not swept:"] + [f"  {u['label']}: {u['why']}" for u in swept["unswept"]] if swept["unswept"] else [])
    moved = read.get("moved") or {"raised": [], "unread": []}
    shifted, sent_ = [m for m in moved["raised"] if not m.get("sent")], [m for m in moved["raised"] if m.get("sent")]
    lines += (["", "landings cards forecast again, main having moved:"] + [
        f"  land/{m['kit']} ({m['label']}): main is at {m['now'][:7]}, its rows forecast at "
        + (m["was"][:7] if m["was"] else "no revision crew kept") + ": "
        + (f"its raise refused: {m['said']}" if m["said"] else f"raised again ({m['card']})" if m["card"] else "raised again, no card left open")
        for m in shifted] if shifted else []) + (["", "landings cards raised on the user's send, its lands posted:"] + [
        f"  land/{m['kit']} ({m['label']}): " + (f"its raise refused: {m['said']}" if m["said"] else "raised")
        for m in sent_] if sent_ else []) + (
        ["", "landings cards whose main can't be read:"] + [
            f"  land/{u['kit']} ({u['label']}): whether main moved under it can't be told: {u['why']}" for u in moved["unread"]]
        if moved["unread"] else [])
    gone = [f"  {x['work']} at {x['revision'][:7]} ({x['label']}): {x['said']}" for x in read.get("previews") or []]
    told = [f"  {x['key']} ({x['label']}): {x['note']}" + (f"; {x['said']}" if x.get("said") else "") for x in read.get("previewed") or []]
    lines += (["", "previews put away, their card or row gone:"] + gone if gone else []) + (
        ["", "cards changed as the runner reported their previews:"] + told if told else [])
    said = [(e.get("sent"), f"  {e['key']}{' ' + e['unit'] if e['unit'] else ''} ({e['label']}) on {e['host']}: {e['why']}; {e['said']}")
            for e in read.get("ended") or []]
    ended, sent = [w for s, w in said if not s], [w for s, w in said if s]
    unended = [f"  {u['host']} ({u['label']}): {u['why']}" for u in read.get("unchecked") or []]
    lines += [""] if ended or sent or unended else []
    lines += (["card sessions ended:"] + ended if ended else []) + (["readings sent:"] + sent if sent else []) + (
        ["card sessions not checked:"] + unended if unended else [])
    for h, v in sv.items():
        if not v["ok"]:
            lines.append(f"\n{h} did not answer ({v['error']}): its units and bolts may also wait on you")
    return "\n".join(lines)


def land_times(fleet, read, r, now):
    """The time of each bolt a kit's landing row names, in its order, as its land line ends with it (crew-rail "A bolt's
    land line shows its age and who held its time", plan.20): held_time's words at now, from the read's run record and
    the bolt's kit as the read surveyed it, the very read and rule the board's head line is drawn from, so the rail and
    the board never differ for one bolt."""
    plan_ = next((p for l, _, _, p in read["found"] if l == r["label"] and p), None)
    if plan_ is None:
        return []
    st, out = Stages(fleet, plan_, read["sv"], read.get("runs"), r["label"]), []
    for x in r.get("bolts", []):
        b = plan_.bolt(x["bolt"])
        out.append(held_time(fleet, (read.get("logs") or {}).get(r["label"], []), read["unread"].get(r["label"], {}), plan_, b,
                             st.kit(b)[0], now)["said"] if b else "")
    return out


def labels_of(read, labels):
    """A rail read narrowed to some of the drives it read: its plans, rows, cards, what its sweeps did and the hosts
    they could not check, each of those labels'; the survey stays whole, since a host serves every drive."""
    labels = set(labels)
    swept = read.get("swept")
    moved = read.get("moved")
    return dict(read, found=[f for f in read["found"] if f[0] in labels], rows=[r for r in read["rows"] if r["label"] in labels],
                cards=[c for c in read["cards"] if c["label"] in labels], unread={l: v for l, v in read["unread"].items() if l in labels},
                logs={l: v for l, v in (read.get("logs") or {}).items() if l in labels},
                swept=swept and {"done": [d for d in swept["done"] if d["label"] in labels], "unswept": [u for u in swept["unswept"] if u["label"] in labels]},
                moved=moved and {k: [x for x in v if x["label"] in labels] for k, v in moved.items()},
                ended=[e for e in read.get("ended") or [] if e["label"] in labels],
                previews=[x for x in read.get("previews") or [] if x["label"] in labels],
                previewed=[x for x in read.get("previewed") or [] if x["label"] in labels],
                unchecked=[u for u in read.get("unchecked") or [] if u["label"] in labels])


def unread_card_acts(logs, now):
    """Each card act a crew agent made through Pending You's tools whose reply named no card, recorded unread by the card
    hook, in the last CARD_DAYS days, oldest first: (label, entry), from each drive's entries (logs)."""
    since = now - datetime.timedelta(days=CARD_DAYS)
    return [(l, e) for l, es in sorted(logs.items()) for e in es
            if (e.get("Act") or "").startswith("card.") and e.get("State") == "unread" and utc(e["At"]) >= since]


def rail_view(fleet, a):
    """crew rail [--label L]: what waits on the user, as rail_text gives it, read from the plans, the proposals, the
    kits and the run record. It sweeps the cards on this host under its sign-in (sweep_cards) and ends the card
    sessions whose card is closed or whose row is gone, on every host of the drives read, and says what each did;
    it writes nothing else. It prints everything it could read, then exits non-zero naming each plan it could not."""
    label = default_label(fleet, a)
    labels = [label] if label else list(fleet["drives"])
    read = rail_read(fleet, labels, sweep=True)
    print(rail_text(fleet, labels, read, datetime.datetime.now(datetime.timezone.utc)))
    if read["errors"]:
        sys.exit("\n".join(read["errors"].values()))


# ------------------------------------------------------------------------------------------------ crew card

# A card's plannotator session, by its card key, in ~/.local/state/crew/cards/<label>/<key>/ on the owner's host, the
# key's slashes as folders, an old batch card's per unit under <key>/<unit>/: session.json (pid, document, url,
# started, its document the files plannotator was given joined by ", "), and plannotator's result.json once the user
# decides.
CARDS = pathlib.Path.home() / ".local/state/crew/cards"


def landings_main(label, kit):
    """Where the main level's host keeps the revision of main a kit's landings card's rows were last forecast against
    (CardActs.keep_main), beside the card's state: no session's, so no card's close or sweep removes it."""
    return CARDS / label / "land" / kit / "main"


def landings_lock(label, kit):
    """The lock a raise of a kit's landings card holds on the main level's host (CardActs.raising): beside the card
    folders of land/<kit> and land/<bolt>, not in one, so ending a card's session, which empties its folder, never
    removes it from under a raise that holds it."""
    return CARDS / label / "land" / f".{kit}.lock"
# The rail rows' card keys, the thing's and not its version's (record 0031): a card crew keys them by, which its
# commands name. A card under an older form, land/<bolt>/<head> or a verify report's verify/<unit>/<stamp>, is still
# crew's (crews_key), closed by the rail's read as one whose row is gone, and none is posted.
CARD_KEYS = (r"proposal/\d+", r"batch/\d+", r"batch/\d+-\d+", r"land/[a-z0-9][a-z0-9-]*", r"deploy/[a-z0-9][a-z0-9-]*",
             r"op/[a-z0-9][a-z0-9-]*/\d+")
# A verify report's key, verify/<unit>/<stamp>, whose card and session from before teams.17 a sweep still ends, and
# whose answered card its asker closes (card_refusal).
VERIFY_KEY = r"verify/[a-z0-9][a-z0-9-]*/\d{8}-\d{4}"
# A decision record's card key, the design agent's: the kit and the record's four digits, one card per record however
# often it is revised (briefs.15, record 0031 §1), raised by crew record. It is no rail row's: the rail lists its open
# cards apart. A card the design agent posted before record 0031, under the key with the commit after it,
# record/<kit>/<number>/<commit>, is the record's too (cards.row_object), closed at the record's status as one under
# this key is.
RECORD_KEY = r"record/([a-z0-9][a-z0-9-]*)/(\d{4})"
CARD_START = 10  # seconds a start waits for plannotator to list its session
# The ports a card's session takes the first free one of when its environment names no range: swancloud's agents'
# range, set in its lib/agent-config.nix (session_env).
CARD_PORTS = "19432-19451"
CARD_GRACE = 120  # seconds a session is left alone after it starts, since the rail's read may not have seen its row


# The roles that ask the user a question of their own on a card, by the kind role() gives them (record 0031, briefs.11).
ASKERS = ("planner", "main-ops", "design")
# The first part of every key crew raises a card under: a rail row's, a decision record's, and a verify report's,
# which no row has had since teams.17. No agent's question takes one (crews_key).
CREWS = {"proposal": "a proposal's card is crew's, raised by crew plan propose and closed at its approval or drop",
         "batch": "a batch's card is crew's, raised with its reading session once the reviewer's summary is delivered",
         "land": "a kit's landings card is crew's, raised in main-level ops's name when a bolt of the kit reads proven, "
                 "and closed when nothing waits to land on the kit's main",
         "deploy": "a deploy's card is crew's, raised by crew ops offer and closed at the deploy's end",
         "op": "a step's card is crew's, raised by crew ops step and closed with the step's state",
         "record": "a record's card is crew's, raised by crew record and closed at the record's status",
         "verify": "a verify report has no card: its findings are fixed in one round"}


def crews_key(key):
    """The kind of crew's own card a key names, by its first part (CREWS), whatever follows, the drive's label
    crew qualifies a key with as it sends it, its revision and its fill of a short one (cards.post_key) and a key of an
    older form among it; None for any other key, an agent's question's."""
    kind = key.split("/", 1)[0] if isinstance(key, str) and "/" in key else None
    return kind if kind in CREWS else None


def card_refusal(fleet, name, label, tool, key, kits=()):
    """Whether a crew agent's Pending You call may go through (briefs.11, record 0031): None to let it, else the
    refusal's words. The user's own name is never checked. A card's post, change or close is a question's, the agent's
    own, only from the planner, main-level ops or the design agent (ASKERS), and never under crew's own
    key (crews_key). A post's key is its idempotencyKey, judged by its form alone, with or without the drive's
    @<label>, :<n> or the fill of a short key (cards.post_key), and no plan read. A change or a close carries a request id and no key, so its key is
    the one this host's run record holds the card under, crew's raises and the agents' own posts alike, read locally
    with no state-branch fetch, None when it holds none; the hook refuses the call when that record can't be read. The planner's close of a card under
    batch/<n>-<k>, which it posted itself before a batch was one card and crew never raises, passes, a departure from
    briefs.11 that goes once no such card is open; its post or change there is refused. So does an asker's ack of an
    answered card under a verify report's key, verify/<unit>/<stamp>, a row form crew no longer raises (teams.17),
    which a conductor posted before it and no event of crew's closes, the same departure: its post, change or
    withdrawal there is refused (signal 2026-10-19-crw-2-conductor-2bec975e/01). An area is made only under
    create-area:<owner>/<kit> for one of the asker's drive's kits (kits, drive_kits, the repositories its plan
    and its landings name, by name or forge address: a kit named in the plan by name alone takes any owner, since crew
    keeps no registry of repositories). Everything else passes: a question's form, and its key but crew's, are its
    asker's. A decision of the role, the call, the key and the drive's kits alone (code.7)."""
    kind, of = role(fleet, name)
    if kind == "user":
        return None
    what = "an area" if tool == "create_area" else "a card"
    if kind not in ASKERS:
        left = ("The user is in your pane: ask them there." if kind == "operator" else
                "Tell the drive's operator what you wait on, as your brief says.")
        return (f"crew refuses {what} from {name}: only the planner, main-level ops and the design agent ask the user on a "
                f"card. {left}")
    if tool == "create_area":
        m = re.fullmatch(r"create-area:([^/\s]+)/([^/\s]+)", key or "")
        if m and (m.group(0).split(":", 1)[1] in kits or m.group(2) in kits):
            return None
        mine = [f"create-area:{k}" if "/" in k else f"create-area:<owner>/{k}" for k in sorted(kits)]
        return (f"crew refuses an area under {key}: " + (f"{name} makes a kit's area only under {either(mine)}." if mine
                else f"no kit's area is {name}'s to make: {label}'s plan and landings name no kit."))
    crews = crews_key(key)
    old = (kind == "planner" and tool in ("cancel_request", "ack_answer") and old_batch(key)
           or tool == "ack_answer" and old_verify(key))
    if crews and not old:
        verb = {"post_request": "post", "update_request": "change"}.get(tool, "close")
        return (f"crew refuses {name}'s {verb} of the card under {key}: {CREWS[crews]}. Ask a question of your own under "
                f"a key of your own, ask/{name}/<what it is about>.")
    return None


def old_batch(key):
    """Whether a card key is a batch's posted as cards of five before a batch was one card, batch/<n>-<k>, whose
    sessions are its units'."""
    return bool(re.fullmatch(r"batch/\d+-\d+", key or ""))


def old_verify(key):
    """Whether a card key is a verify report's, verify/<unit>/<stamp>, posted by a conductor before teams.17."""
    return bool(re.fullmatch(VERIFY_KEY, key or ""))


def card_of(fleet, a, unit_needed=True):
    """The drive a card command runs as and the key's folder, an old batch card's per unit: refused with no
    drive, a key that is not one of the rail's, a batch/<n> key with a unit, since a batch has one session on the
    whole batch, a batch/<n>-<k> key with no unit where one is needed, and a unit with any other key."""
    label = default_label(fleet, a) or fail("crew card runs as the card's drive: run it as a crew agent, or add --label")
    any(re.fullmatch(k, a.key) for k in CARD_KEYS) or fail(
        f"{a.key} is not a card key: proposal/<n>, batch/<n>, land/<kit> or land/<bolt>")
    old = old_batch(a.key)
    if old:
        a.unit or not unit_needed or fail(f"a batch card posted as cards of five has a session for each of its units: "
                                          f"crew card {a.sub} {a.key} <unit>")
    elif a.key.startswith("batch/"):
        not a.unit or fail(f"a batch has one reading session, on the whole batch: crew card {a.sub} {a.key}")
    else:
        not a.unit or fail(f"only an old batch card's key, batch/<n>-<k>, takes a unit, and {a.key} is not one")
    if a.unit:
        crew.NAME.match(a.unit) or fail(f"a unit's name is lowercase words with dashes, not {a.unit}")
    return label, CARDS / label / a.key / a.unit if old and a.unit else CARDS / label / a.key


def session_refusal(key, label, main, here, host=None, kits=()):
    """Why a card key's session is not started or waited on here, before its row is read: a batch card's one session
    runs on the drive's main level's host (main), where its summary is written and its card raised; a bolt's
    reading, land/<bolt>, on the host its work runs on (host, bolt_at), where the runner that took it keeps its kit; a
    kit's landings card, land/<kit> (kits, the drive's kits' names, land_key), has no reading of its own, each of
    its rows having its bolt's."""
    kind = land_key(key, kits)
    if kind and kind[0] == "kit":
        return (f"{key} is {kind[1]}'s landings card, {label}-ops's, which has no reading of its own: each of its rows "
                f"has its bolt's, land/<bolt>, on the host its work runs on")
    if key.startswith("land/") and host != here:
        return (f"{key}'s reading session runs on {host}, the host its bolt's work runs on, where the runner that took it "
                f"keeps its kit: run crew card session {key} there")
    if key.startswith("batch/") and not old_batch(key) and main != here:
        return (f"{key}'s reading session runs on {main}, where {label}'s main level writes the batch's summary: run crew card "
                f"session {key} there")
    return None


def no_row(label, key, down):
    """What a card command says of a key no row of the rail has: its row is gone, or whether one would can't be known,
    naming each host that did not answer (read.1)."""
    return (f"no row of {label}'s rail has the card key {key}"
            + (", and whether one would can't be known: " + "; ".join(down) if down else ": its row is gone, so its card has nothing to read"))


def plannotator_sessions():
    """The plannotator sessions running on this host, ({pid: session}, None), as `plannotator sessions --json` lists
    them, each with the pid, target and url it lists; (None, why) when the list can't be read."""
    try:
        r = subprocess.run(["plannotator", "sessions", "--json"], capture_output=True, text=True, timeout=8)
    except FileNotFoundError:
        return None, "plannotator is not on this host's path"
    except subprocess.TimeoutExpired:
        return None, "plannotator sessions did not answer in 8 seconds"
    if r.returncode:
        return None, "plannotator sessions: " + ((r.stderr or r.stdout).strip().splitlines() or [f"exit {r.returncode}"])[-1]
    try:
        got = json.loads(r.stdout)
    except ValueError:
        got = None
    if not isinstance(got, list):
        return None, "plannotator sessions --json printed no list"
    return {s["pid"]: s for s in got if isinstance(s, dict) and isinstance(s.get("pid"), int) and isinstance(s.get("target"), str)
            and isinstance(s.get("url"), str)}, None


def card_recorded(d):
    """The session crew started for a key, as session.json records it, or None when none is recorded. A record crew
    can't read is refused, so nothing is done to a process it names."""
    f = d / "session.json"
    try:
        s = json.loads(f.read_text())
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as e:
        fail(f"crew can't read {f}: {e}")
    ok = (isinstance(s, dict) and isinstance(s.get("pid"), int) and s["pid"] > 1
          and all(isinstance(s.get(k), str) for k in ("document", "url", "started")))
    return s if ok else fail(f"{f} is not a session crew recorded: it lacks a pid, document, url or started")


def serving(listed, s):
    """Whether plannotator lists the recorded session's pid as serving its document, path by path: a session of
    several files is listed with their paths joined by ", ", as crew records its document, and a folder's target, as
    a session started before crew gave plannotator files, without its last slash."""
    got = listed.get(s["pid"])
    return bool(got) and [os.path.realpath(p) for p in got["target"].split(", ")] == s["document"].split(", ")


def card_result(d):
    """The user's decision in a key's session, as plannotator wrote it to result.json: (decision, feedback, how many
    annotations), feedback None when it gave none and the count None when it gave none; None while there is no result."""
    f = d / "result.json"
    try:
        r = json.loads(f.read_text())
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as e:
        fail(f"crew can't read plannotator's result {f}: {e}")
    if not isinstance(r, dict) or r.get("decision") not in ("approved", "annotated", "dismissed"):
        fail(f"plannotator's result {f} holds no decision crew knows: approved, annotated or dismissed")
    fb, k = r.get("feedback"), r.get("annotationCount")
    return (r["decision"], fb if isinstance(fb, str) and fb.strip() else None,
            k if isinstance(k, int) and not isinstance(k, bool) and k >= 0 else None)


def card_row(fleet, label, key):
    """The rail row of one drive with that card key, read as crew rail reads its rows: only the proposals for a
    proposal's key, and only the run record's batches for a batch card's."""
    found = plans(fleet, [label])
    plan = found[0][3]
    kind = key.split("/")[0]
    sv = survey(fleet, [])
    props = open_proposals(fleet, [label], found) if kind == "proposal" and plan else []
    batched = {}
    if kind == "batch" and plan:
        _, _, unread, _, batched, *_ = rail_record(fleet, found, [])
        not unread.get(label) or fail(f"crew can't tell whether {key}'s card is still open: "
                                      + "; ".join(f"{h} did not answer" for h in sorted(unread[label])))
    row = next((r for r in rail_rows(fleet, found, sv, props, {}, batched) if r["key"] == key), None)
    if row:
        return row, props
    fail(no_row(label, key, [f"{h} did not answer ({v['error']})" for h, v in sv.items() if not v["ok"]]))


def card_stop(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def card_session(fleet, a, acts=None):
    """crew card session <key> [<unit>] [--label L]: the plannotator session of a card that has one, on what the rail
    row with that card key asks the user to read, started on this host with an Approve button and no browser if none
    runs, and its link printed (session_open). A batch card's, batch/<n>, is one session on the whole batch, started on
    the drive's main level's host and refused elsewhere, naming it: crew writes the batch's folder (batch_folder)
    and gives plannotator its files as one review. A proposal's is on its page, for a proposal whose card links one
    (proposal_reads), and refused for any other, whose card holds it whole. Either is opened by reading_again, so a
    start anew is recorded and the planner's card, while it waits on the user, changed to carry the link, and a card
    the user has answered left as it is. An old batch card's, batch/<n>-<k>, is one
    session for each unit it holds, on that unit's whole change as its Markdown files, started on the host its work ran
    on (batch_at, code.3) and refused for a unit the card does not hold. A landing's, land/<bolt>, is one session on
    what the bolt brings to main, on the host its work runs on (land_session). Refused for a key
    with no row, a document crew can't read whole, and a link that would open only on this host."""
    label, d = card_of(fleet, a)
    if a.key.startswith("land/"):
        return land_session(fleet, label, a.key, acts)
    here = crew.this_host()
    why = session_refusal(a.key, label, fleet["drives"][label]["machine"], here)
    not why or fail(why)
    row, props = card_row(fleet, label, a.key)
    row["doc"] or fail(f"{a.key}'s card has no document to read, so it has no session")
    name = f"{a.key}'s session"

    def said(url, decided):
        print(url)
        if decided:
            print(f"the user decided in {name} before it ended: crew card read {a.key} gives the decision", file=sys.stderr)
    if not old_batch(a.key):
        if row["doc"][0] == "page":
            p = next(x for x in props if x["proposal"] == row["doc"][2])
            proposal_reads([do_args(label, c["do"]) for c in p["changes"]]) or fail(
                f"{a.key}'s card has nothing to read: it holds the proposal whole, and only a proposal of more than "
                f"{cards.CARD_NEW} new units has a reading session")
        reading_again(fleet, label, a.key, acts, said)
        return
    a.unit in row["units"] or fail(f"{a.key} holds {either(row['units'])}, not {a.unit}: its sessions are its units'")
    t = batch_at(fleet, label, a.key, a.unit)
    if t["machine"] != here:
        return forward_card(fleet, t, a, label)
    # A crossed unit's change is read archived at the commit of its bolt the batch read it at (Decision 13).
    p = plan_of(fleet, label)
    u = p.item(a.unit) if p else None
    at = (row.get("commits") or {}).get(a.unit) if u is not None and crossed_bolt(p, u.get("Bolt")) else None
    folder, name = change_folder(fleet, t, a.unit, d / "change", at), f"{a.key}'s session of {a.unit}"
    said(*session_open(d, name, lambda: change_files(folder) or fail(
        f"{a.unit}'s change {folder} on {here} holds no Markdown file to read"))[:2])


# The change note of a card changed to carry its reading's new link, a kit's landings card a row's (card-sessions).
RELINKED = "Its reading is open again at a new link"


def relinks(due, got):
    """Whether crew changes a card to carry its reading's new link (card-sessions "Starting a batch's or a proposal's
    reading changes its card"): only when it is due, the session started anew or the card standing without its
    reading, and the card, as get_request gives it (got, None when none is held or it could not be read), still waits on
    the user; a card the user has answered is left as it is, since a new card following it would ask again."""
    return bool(due) and card_waiting(got)


def card_waiting(got):
    """Whether a card, as get_request gives it (got, None when none is held or it could not be read), still waits on
    the user, so crew changes it in place; one the user answered is left as it is."""
    return isinstance(got, dict) and got.get("status") in OPEN


def land_session(fleet, label, key, acts=None, say=None):
    """crew card session land/<bolt>: the bolt's one reading session, on what it brings to main at its head, on the host
    its work runs on (bolt_at) and refused elsewhere, naming it, while it is a row of its kit's landings card that can land,
    read from the same facts as its row (land_read) and opened as its row's raise opens it (reading_open), its link
    printed, or said by say(link, decided) when given. The try, from the row's read on, is recorded as one card.reading
    entry on the bolt in main-level ops's name (reading_owner), done when the session started anew and refused with
    crew's message when the bolt is no row that can land or the reading could not open, a session given again
    recording nothing (record.1), nor a refusal before the try. When it started the session anew, none running, or the run record shows the kit's
    card standing without a row's reading (kit_unread), the kit's card is raised on the drive's main machine with
    the new link's note (land_hand), changed in place while it waits on the user and left as it is once they answered
    it (card-sessions "The session command puts a landing's link on its card while the card waits"). Refused for land/<kit>, which has no reading of
    its own, a bolt the plan does not hold, one not started, and one that is no row that can land, saying what it
    waits on or why it is held (card-sessions "A bolt that is no row"). As reading_open returns it: its link, whether
    the user decided in it, and whether it was started anew; a refusal of the try, recorded, is raised again."""
    acts = acts or CardActs(fleet)
    kits = kits_read(fleet, label)
    why = session_refusal(key, label, fleet["drives"][label]["machine"], acts.host(), None, kits)
    if why and land_key(key, kits)[0] == "kit":
        fail(why)
    bolt = key.split("/", 1)[1]
    plan, b, t = land_held(fleet, label, bolt)
    b or fail(f"{label}'s plan holds no bolt {bolt}, so {key} has no reading")
    t or fail(f"bolt {bolt} is not started, so it is no row of its kit's landings card, and it has no reading")
    why = session_refusal(key, label, fleet["drives"][label]["machine"], acts.host(), t["machine"], kits)
    not why or fail(why)
    owner, obj, kit = reading_owner(label, key), cards.row_object(key, kits), b.get("Repo") or t["kit"]["name"]
    try:
        row, why = land_read(fleet, label, plan, b, t)
        row or fail(f"{bolt} is no row of {kit}'s landings card, so it has no reading: {why}")
        row["box"] or fail(f"{bolt} is {row['why']} on {kit}'s landings card, so it has no reading until it can land again")
        url, decided, started = acts.reading(label, key, row["facts"])
    except Refusal as e:
        acts.emit(label, "card.reading", [obj], by=owner, refused=str(e), Key=key)
        raise
    if started:
        acts.emit(label, "card.reading", [obj], by=owner, Key=key)
    if say:
        say(url, decided)
    else:
        print(url)
        if decided:
            print(f"the user decided in {key}'s session before it ended: crew card read {key} gives the decision", file=sys.stderr)
    if started or kit_unread(acts, label, kit):
        land_hand(fleet, label, kit, f"{bolt}: {RELINKED}")
    return url, decided, started


def kit_unread(acts, label, kit):
    """Whether the kit's landings card, main-level ops's, stands without a row's reading (reading_unread), read from the
    drive's run record, where its posts and changes reach the branch from the main machine (read.5); False, said,
    when that record can't be read, so a session given again changes no card."""
    try:
        entries = acts.drive(label)
    except Refusal as e:
        print(f"card land/{kit}: whether it stands without a row's reading can't be read: {e}", file=sys.stderr)
        return False
    key = f"land/{kit}"
    return reading_unread(entries, key, cards.card_under(entries, key, f"{label}-ops"))


def relink(acts, label, key, owner, due, change):
    """The card owner holds under key on this host changed to carry its reading's link, when due (relinks): read in the
    owner's name, and changed in place by change(), the kind's change with RELINKED as its note, while it waits on the
    user; left as it is, said, once the user has answered it; not changed, said, when whether it waits can't be read.
    Nothing when none is held or it is not due."""
    card = cards.card_under(acts.entries(label), key, owner) if due else None
    if not card:
        return
    got = None
    try:
        with acts.bridge(owner, "The reading stands at its new link, and its card is not changed.") as py:
            got, words = py.answer("get_request", {"requestId": card, "name": owner})
    except Refusal as e:
        words = str(e)
    if relinks(due, got):
        change()
    elif got is not None:
        print(f"card {key}: {card} is left as it is: " + ("the user has answered it" if got.get("status") == "answered"
                                                          else f"Pending You shows it {got.get('status')}"))
    else:
        print(f"card {key}: {card} is not changed, since whether it waits on the user can't be read: {words}", file=sys.stderr)


def reading_facts(fleet, label, key, acts):
    """The facts a batch's or a long proposal's reading is opened on (reading_open), read as its raise reads them: a
    batch's card's from this host's run record and the reviewer's summary (batch_read); a proposal's number, the open
    one of its chain at the branch's tip (chain_read), whose page is its reading. Refused when its point has passed."""
    kind, n = key.split("/")[0], int(key.split("/")[1])
    if kind == "batch":
        facts = batch_read(fleet, label, n, acts) or fail(
            f"{key}'s card has nothing to read: this host's run record holds no batch {n} waiting on the user, or its "
            "summary is not there")
        facts.pop("told", None)
        return facts
    got = chain_read(fleet, label, n) or fail(f"{key}'s card has nothing to read: no proposal of its chain is open")
    return dict(n=got[1], first=n)


def reading_again(fleet, label, key, acts=None, say=None):
    """A batch's or a long proposal's reading, batch/<n> or proposal/<n>, opened after its card's raise
    (card-sessions "Starting a batch's or a proposal's reading changes its card"): its facts read as its raise reads
    them (reading_facts), and its reading opened as the raise opens it (reading_open), said by say(link, decided) when
    given; the try recorded as one card.reading entry on the row's object in the planner's name, with the card held
    under the key, done when the session started anew and refused with crew's message when it could not open, a
    session given again recording nothing (record.1); then the card the planner holds under the key changed in place
    to carry the link, while it waits on the user, when the session started anew or the run record shows the card
    standing without its reading (reading_unread), by the kind's raise with RELINKED as its note (relink). As
    reading_open returns it: its link, whether the user decided in it, and whether it was started anew; a refusal,
    recorded, is raised again."""
    acts = acts or CardActs(fleet)
    owner, obj = f"{label}-planner", cards.row_object(key)
    card = cards.card_under(acts.entries(label), key, owner)
    held = {"Card": card} if card else {}
    try:
        url, decided, started = acts.reading(label, key, reading_facts(fleet, label, key, acts))
    except Refusal as e:
        acts.emit(label, "card.reading", [obj], by=owner, refused=str(e), Key=key, **held)
        raise
    if started:
        acts.emit(label, "card.reading", [obj], by=owner, Key=key, **held)
    if say:
        say(url, decided)
    row = {"label": label, "key": key, "group": "proposals" if key.startswith("proposal/") else "batches"}
    relink(acts, label, key, owner, started or reading_unread(acts.entries(label), key, card),
           lambda: raise_proposal(fleet, row, acts, "relink") if key.startswith("proposal/") else raise_batch(fleet, row, acts, RELINKED))
    return url, decided, started


def proposal_reads(argvs):
    """Whether a proposal's card links a reading session, as cards.proposal_card decides it from the proposal's
    commands (briefs.9): more units and chores new to a bolt or the queue than its boxes take, whatever else it
    changes, since only those are boxes."""
    return len(new_units(argvs)) > cards.CARD_NEW


# What a card's session does not carry of the agent that starts it: herdr's reading of the agent's pane, which the
# Claude plannotator starts to answer the user would report its own session to, so herdr took it for a new session in
# the agent's pane and dropped the agent's name (swc-3-conductor on deneb, 2026-10-23: its landing card's session,
# started by `crew card wait`, gave herdr the session of the Claude that answered the user's question on the page, and
# crew read the conductor ended; signal 2026-10-23-swc-3-conductor-8556b697/01); and the identity crew-role gives
# the agent (teams.6), which would record that Claude's start as the agent's own (hooks/session-start), and the
# agent's Claude session a command carries to another host (record.session), so the session and what it starts act
# under no agent's name (briefs.17).
NOT_CARRIED = ("HERDR_ENV", "HERDR_PANE_ID", "HERDR_TAB_ID", "HERDR_WORKSPACE_ID", "HERDR_AGENT", "HERDR_SESSION",
               "HERDR_SOCKET_PATH", "CREW_AGENT", "CREW_LABEL", "CREW_ROLE", "CREW_LAUNCH", "CREW_SESSION", "SLUICE_AGENT",
               "SLUICE_BRANCH")


def session_env(environ):
    """The environment a card's session starts plannotator in, from the caller's environ, which is not changed:
    everything but what it does not carry of the agent (NOT_CARRIED), with no browser opened and its links for another
    host (session_open), and PLANNOTATOR_PORT kept when it names a range plannotator 0.28.26 reads (<a>-<b>,
    1 <= a <= b <= 65535), else crew's own, CARD_PORTS, so the session takes the first free port of a range wherever
    crew runs: unset, one port, which plannotator holds alone, and a value it can't read, which in remote mode it takes
    as the one port 19432."""
    env = {**{k: v for k, v in environ.items() if k not in NOT_CARRIED}, "PLANNOTATOR_SKIP_BROWSER_OPEN": "1", "PLANNOTATOR_REMOTE": "1"}
    m = re.fullmatch(r"([0-9]+)-([0-9]+)", env.get("PLANNOTATOR_PORT", ""))
    if not (m and 1 <= int(m[1]) <= int(m[2]) <= 65535):
        env["PLANNOTATOR_PORT"] = CARD_PORTS
    return env


def session_open(d, name, write):
    """The plannotator session of a card key on this host, kept in its folder d, called name in what is said: the one
    crew recorded given again while it serves its document, or kept for crew card read when the user decided in it
    before it ended; else started anew on the files write() writes and returns, as one review in their order, with an
    Approve button and no browser (plannotator 0.28.6), recorded once plannotator lists it. One the user closed
    undecided has its result moved aside, so a new one starts. Returns its link, whether the user decided in it before
    it ended, and whether it was started anew rather than given again. Refused, any session it started ended, when
    plannotator can't be listed, is not on this host, does not list it in time, ends first, or gives a link only this
    host could open (read.1)."""
    import shutil
    d.mkdir(parents=True, exist_ok=True)
    with open(d / ".lock", "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        s = card_recorded(d)
        if s:
            listed, why = plannotator_sessions()
            listed is not None or fail(f"crew can't tell whether {name} still runs: {why}")
            verdict = session_verdict(s, serving(listed, s), card_result(d))
            if verdict in ("serving", "decided"):
                return s["url"], verdict == "decided", False
            if verdict == "dismissed":
                (d / "result.json").rename(d / f"result.{re.sub(r'[-:]', '', s['started'])}.json")
            (d / "session.json").unlink()
        shutil.which("plannotator") or fail("plannotator is not on this host's path, and a card's session is a plannotator session")
        untold(d)  # a told mark is the last reading's, and this one is told of when the user sends it
        here = crew.this_host()
        files = [os.path.realpath(f) for f in write()]
        gone = [f for f in files if not os.path.isfile(f)]
        not gone or fail(f"{name}'s document {gone[0]} is not on {here}")
        doc = ", ".join(files)  # as plannotator lists a session of several files
        started = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        env = session_env(os.environ)
        with open(d / "out", "w") as out, open(d / "err", "w") as err:
            # Several files, each its own path, open as one review in that order with one decision (plannotator 0.28.6).
            # Its own session, so it outlives the command that started it, and the shell that ran that.
            proc = subprocess.Popen(["plannotator", "annotate", *files, "--gate", "--json", "--result-file", str(d / "result.json")],
                                    stdin=subprocess.DEVNULL, stdout=out, stderr=err, env=env, start_new_session=True)
        deadline = time.monotonic() + CARD_START
        while True:
            listed, why = plannotator_sessions()
            got = (listed or {}).get(proc.pid)
            if got:
                break
            if proc.poll() is not None:
                said = (d / "err").read_text().strip().splitlines()
                fail(f"plannotator ended before {name} was ready" + (f": {said[-1]}" if said else f", exit {proc.returncode}"))
            if time.monotonic() > deadline:
                card_stop(proc)
                fail(f"plannotator did not list {name} within {CARD_START} seconds" + (f" ({why})" if why else "")
                     + ", so crew ended it")
            time.sleep(0.2)
        if local_link(got["url"]):
            card_stop(proc)
            fail(f"plannotator gave {name} the link {got['url']}, which would open only on {here}, so crew ended it: "
                 "a card's session needs PLANNOTATOR_URL_HOST naming the host on the tailnet (swancloud sets it to auto)")
        tmp = d / ".session.json"
        tmp.write_text(json.dumps({"pid": proc.pid, "document": doc, "url": got["url"], "started": started}) + "\n")
        tmp.replace(d / "session.json")
    return got["url"], False, True


def reading_open(fleet, label, key, facts):
    """The reading session of a card crew raises with one (briefs.9), started on this host or given again while it
    serves (session_open): a batch's, batch/<n>, on its folder, the reviewer's summary and every unit's change at the
    commit the batch read it at (facts' units), and refused but on the drive's main level's host; a landing's,
    land/<bolt>, on what the bolt brings to main at its head (landing_write), in the head's own folder, and refused but
    on the host its work runs on (facts' host), a session of the key on another head ended first; a long
    proposal's on its page, as crew plan proposed <n> prints it, a session of the key serving an older page of its
    chain ended first. As session_open returns it: its link, whether the user decided in it before it ended, and
    whether it was started anew; a Refusal says why it could not open."""
    d = CARDS / label / key
    why = session_refusal(key, label, fleet["drives"][label]["machine"], crew.this_host(), facts.get("host"))
    not why or fail(why)
    if key.startswith("batch/"):
        units = [(u["unit"], u["bolt"], u["commit"]) for u in facts["units"]]
        return session_open(d, f"{key}'s session", lambda: batch_folder_write(fleet, label, facts["n"], units))
    if key.startswith("land/"):
        folder = d / facts["head"][:7]
        s = card_recorded(d) if d.is_dir() else None
        if s and not all(os.path.dirname(p) == os.path.realpath(folder) for p in s["document"].split(", ")):
            print(end_session(label, key)[0])
        return session_open(d, f"{key}'s session", lambda: landing_write(fleet, facts, folder))
    f = d / f"proposal-{facts['n']}.md"
    s = card_recorded(d) if d.is_dir() else None
    if s and s["document"] != os.path.realpath(f):
        print(end_session(label, key)[0])

    def write():
        p = next((x for x in open_proposals(fleet, [label]) if str(x["proposal"]) == str(facts["n"])), None) or fail(
            f"proposal {facts['n']} of {label} is not open, so it has no page to read")
        f.write_text(page(p, label))
        return [str(f)]
    return session_open(d, f"{key}'s session", write)


def session_verdict(s, serves, decided):
    """What crew card session does with the session it recorded for a key, s (plan's card-sessions): it still serves its
    document, so its link is given again ("serving"); the user approved or annotated before it ended, so it is kept for
    crew card read ("decided"); the user closed it undecided, so its result is moved aside and a new one starts
    ("dismissed"); else it ended, and a new one starts ("ended")."""
    if serves:
        return "serving"
    if decided and decided[0] != "dismissed":
        return "decided"
    return "dismissed" if decided else "ended"


def local_link(url):
    """Whether plannotator's link would open only on the host it runs on, so a card's session can't use it."""
    import urllib.parse
    host = urllib.parse.urlsplit(url).hostname or ""
    return host in ("localhost", "::1") or host.startswith("127.")


def change_folder(fleet, t, unit, into, at=None):
    """A unit's whole change on its team's host, this one: in its place while it has one, else on its bolt's worktree,
    else, for a unit of a bolt given through Flume, which has neither, at the commit of its bolt its batch read it at
    (at; Decision 13 of teams-cross-to-flume-as-their-bolts-land), else as the kit's main holds it now, open or
    archived, read by ref after a fetch (MAIN, plan.18), never from the main checkout's files, which the fleet's timer
    moves minutes behind: its Markdown written into the folder into (change_written)."""
    k = survey(fleet, [(t, None)]).get(t["machine"], {})
    kit = k.get("kits", {}).get(t["kit"]["main"], {}) if k.get("ok") else {}
    kit.get("ok") or fail(f"{t['kit']['main']} on {t['machine']} could not be read: {kit.get('error') or k.get('error')}")
    pl = kit["places"].get(unit)
    where = [f"{pl['path']}/openspec/changes/{unit}"] if pl else []
    where += [f"{w}/openspec/changes/{unit}" for w in (b["worktree"] for b in kit["bolts"].values()) if w]
    found = next((w for w in where if os.path.isdir(w)), None) or (change_written(t["kit"]["main"], at, unit, into) if at else None)
    if found:
        return found
    r = subprocess.run(["bash", "-c", fetch_told(fleet, crew.this_host(), t["kit"]["main"], MAIN), "crew", t["kit"]["main"]],
                       capture_output=True, text=True, env=gitenv())
    r.returncode == 0 or fail(f"on {t['machine']}: " + ((r.stderr or r.stdout).strip() or f"exit {r.returncode}"))
    head, why = main_held(t["kit"]["name"], t["machine"], r.stdout)
    not why or fail(why)
    return change_written(t["kit"]["main"], head, unit, into) or fail(
        f"unit {unit}'s change is in no checkout of {t['kit']['name']} on {t['machine']}, nor on its main at {head[:7]}")


def change_held(main, ref, unit):
    """A unit's change as a checkout of its kit holds it at ref, open, else archived (gather.DATED): its Markdown files,
    [(path under the change, content)] as git holds them, or None when ref holds no change by that name."""
    out = gather.run(["git", "ls-tree", "-d", "--name-only", ref, "openspec/changes/", "openspec/changes/archive/"], main) or ""
    archive = "openspec/changes/archive/"
    held = [l for l in out.splitlines() if l == f"openspec/changes/{unit}"] or sorted(
        l for l in out.splitlines() if l.startswith(archive) and l[len(archive) + 11:] == unit and gather.DATED.fullmatch(l[len(archive):][:11]))
    if not held:
        return None
    folder = held[-1]
    return [(f[len(folder) + 1:], gather.run(["git", "show", f"{ref}:{f}"], main) or "")
            for f in (gather.run(["git", "ls-tree", "-r", "--name-only", ref, "--", f"{folder}/"], main) or "").splitlines()
            if f.endswith(".md")]


def change_written(main, ref, unit, into):
    """A unit's change as a kit's main holds it at ref, open, else archived (change_held), its Markdown files written
    into the folder into, emptied first, as git holds them: the folder, or None when main holds no change by that
    name."""
    import shutil
    files = change_held(main, ref, unit)
    if files is None:
        return None
    shutil.rmtree(into, ignore_errors=True)
    for p, text in files:
        target = pathlib.Path(into, p)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
    return str(into)


def landing_write(fleet, f, folder):
    """Write a landing's reading afresh into folder, its head's, on the host the bolt's work runs on, in the kit's folder
    there, from the landing's facts (land_facts, its host and main): each unit's change as the kit holds it at the bolt's head, open or archived
    (change_held), and the bolt's diff against main from where it last met main (base) to its head, less
    openspec/changes/, whose Markdown the units' files show whole, named and ordered by landing_reading, the diff in as
    many files as plannotator's limit for one file asks (diff_parts), each written as the UTF-8 it was measured in.
    Every file is read before any is written: what crew can't read refuses, naming it, and nothing is written (read.1).
    Returns the files' paths, in order."""
    t = {"label": None, "machine": f["host"], "kit": kit_of(f.get("repo") or f["kit"], f["main"])}
    main, head = t["kit"]["main"], f["head"]
    changes = []
    for u in f["units"]:
        held = change_held(main, head, u)
        held is not None or fail(f"unit {u}'s change is not on bolt {f['bolt']} at {head[:7]}, open or archived, in {main} on {t['machine']}")
        held or fail(f"unit {u}'s change on bolt {f['bolt']} at {head[:7]} holds no Markdown file to read")
        changes.append((u, held))
    _, diff = kit_git(fleet, t, main, "diff", "--no-color", "--no-ext-diff", f["base"], head, "--", ".", ":(exclude)openspec/changes")
    whole = dict(repo=t["kit"]["repo"], base=f["base"], main=main, host=t["machine"])
    out = landing_reading(f["bolt"], f["kit"], head, f["units"], f.get("chores") or [], changes, diff + "\n" if diff else "", whole)
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.iterdir():
        if old.is_file():
            old.unlink()
    for name, text in out:
        (folder / name).write_text(text, encoding="utf-8")
    return [str(folder / name) for name, _ in out]


def change_order(path):
    """Where a file of a change, by its path under the change, comes in its reading: its proposal, design, specs in
    path order, tasks, then any other Markdown in path order."""
    return ({"proposal.md": 0, "design.md": 1, "tasks.md": 3}.get(path, 2 if path.startswith("specs/") else 4), path)


def change_files(folder):
    """A change's Markdown files in a folder on this host, each a path, in the order of its reading (change_order):
    what plannotator is given, never the folder, whose listed files the user would have to open one by one."""
    root = pathlib.Path(folder)
    found = [p.relative_to(root).as_posix() for p in root.rglob("*.md") if p.is_file()]
    return [str(root / p) for p in sorted(found, key=change_order)]


def batch_folder(label, n):
    """Batch n's own folder on the drive's main level's host, beside its summary: the files its one reading session
    opens."""
    return reviews(label) / f"batch-{label}-{n}"


# A change's Markdown files at a commit in a kit, run on the team's host: each file's path under the change, then its
# content as git holds it, each ended by NUL, which no Markdown file holds.
# A unit's change at a commit, open, else archived (as change_held finds it): a unit given through Flume is batched once
# its change is archived on its bolt (crossed_changes), at the commit that holds it so.
CHANGE_AT = r"""set -eo pipefail
main=$1 sha=$2 unit=$3
cd "$main"
git cat-file -e "$sha^{commit}" 2>/dev/null || { echo "$sha is not a commit of $main" >&2; exit 1; }
folder=openspec/changes/$unit
if [ -z "$(git ls-tree -d --name-only "$sha" "$folder")" ]; then
  folder=$(git ls-tree -d --name-only "$sha" openspec/changes/archive/ | grep -E "^openspec/changes/archive/[0-9]{4}-[0-9]{2}-[0-9]{2}-$unit\$" | sort | tail -n 1 || true)
fi
[ -n "$folder" ] || exit 0
git ls-tree -r -z --name-only "$sha" -- "$folder/" | while IFS= read -r -d '' p; do
  case $p in *.md) printf '%s\0' "${p#"$folder/"}"; git cat-file blob "$sha:$p"; printf '\0' ;; esac
done
"""


def change_at(fleet, t, unit, sha):
    """A unit's change as read at a commit in its kit's main checkout on its team's host, over ssh when that host is
    another (code.3), as the reviewer reads it (reading_command), open, else archived (CHANGE_AT): its Markdown files,
    [(path under the change, content)], in the order of its reading. Refused naming the unit, the host and what failed
    (read.1)."""
    r = crew.on_machine(fleet, t["machine"], ["bash", "-c", CHANGE_AT, "crew", t["kit"]["main"], sha, unit])
    why = unread_change(t, unit, sha, r.returncode, r.stderr)
    not why or fail(why)
    parts = r.stdout.split("\0")
    files = sorted(zip(parts[0:-1:2], parts[1::2]), key=lambda f: change_order(f[0]))
    return files or fail(f"{unit}'s change at {sha} in {t['kit']['main']} on {t['machine']} holds no Markdown file")


def unread_change(t, unit, sha, code, stderr):
    """Why a batch can't be read whole, from CHANGE_AT's exit on the unit's team's host (read.1): the host did not
    answer, naming it, or the change could not be read at its commit, naming the unit, the commit and the host."""
    said = ((stderr or "").strip().splitlines() or [f"exit {code}"])[-1]
    if code == 255:
        return f"crew can't read {unit}'s change: {t['machine']}, {t['name']}'s host, did not answer ({said})"
    return f"crew can't read {unit}'s change at {sha} in {t['kit']['main']} on {t['machine']}: {said}" if code else None


def batch_folder_write(fleet, label, n, units):
    """Write batch n's folder afresh, on the main level's host, from the batch the run record holds, its units in the
    batch's order as (unit, its bolt, the commit the batch read it at): 00-summary.md, the reviewer's summary as written,
    then for the k-th unit each Markdown file of its change at that commit, named <kk>-<unit>-<its path under the
    change, / as ->, so each file plannotator shows by its name alone names its unit. Every file is read before any is
    written: what crew can't read refuses, naming it, and nothing is written (read.1). Returns the files' paths, in that
    order."""
    f = batch_file(label, n)
    try:
        summary = f.read_text()
    except OSError as e:
        fail(f"crew can't read batch {n}'s summary {f}: {e.strerror or e}")
    out = [("00-summary.md", summary)]
    for k, (u, bolt, sha) in enumerate(units, 1):
        out += [(f"{k:02d}-{u}-{p.replace('/', '-')}", text) for p, text in change_at(fleet, batch_unit_at(fleet, label, bolt, u), u, sha)]
    folder = batch_folder(label, n)
    folder.mkdir(parents=True, exist_ok=True)
    for old in folder.iterdir():
        if old.is_file() and re.fullmatch(r"\d{2}-.+\.md", old.name):
            old.unlink()
    for name, text in out:
        (folder / name).write_text(text)
    return [str(folder / name) for name, _ in out]


def landing_reading(bolt, kit, head, units, chores, changes, diff, whole):
    """A landing's reading, the files its one session opens as one review, in order, each (name, text) (card-sessions,
    briefs.9): 00-<bolt>.md, a page naming the bolt, its kit and its head, the units and chores that land, one a line,
    and saying that the reading lands nothing, approving the card being the word to land, and that what the user sends
    from it reaches main-level ops as notes on the card, a note naming a defect holding the landing for a fix;
    then for the k-th unit each Markdown file of its change as the head holds it, named <kk>-<unit>-<its path under the
    change, / as ->, in a change's reading order (change_order), as a batch's folder names them; then the bolt's diff
    against main, numbered after the last unit, as text, which plannotator opens beside Markdown in one review where it
    refuses a .diff (plannotator 0.28.23): <nn>-<bolt>-diff.txt, or, when it passes the most plannotator opens in one
    file, its parts (diff_parts), <nn>-<bolt>-diff-<k>-of-<m>.txt, the page saying how many. A file whose own change
    passes that most is in no part: the page names each such file with its size, how many there are, and where to read
    them whole, GitHub's compare view of the bolt's base against its head and the git command on the kit's host
    (sluice core.43's shape for a request's commits past the forge's limit). changes: [(unit, [(path under the change,
    text)])] in the plan's order; diff: the diff's text; whole: where the diff is read whole, the kit's GitHub repo
    (owner/name), the commit the diff is from (base), and the kit's main checkout and host."""
    parts, past = diff_parts(diff) if diff.strip() else (["The bolt changes nothing against main outside its change folders.\n"], [])
    lines = [f"# Bolt {bolt}, landing on {kit}'s main", "", f"What lands, at its head {head[:7]}:", ""]
    lines += [f"- {u}" for u in units] + [f"- {c} (chore)" for c in chores]
    lines += ["", "This reading lands nothing: approving the landing card is the word to land, and its Approve here lands "
                  "nothing.", "",
              "What you send from it reaches main-level ops as notes on the landing card, and a note naming a defect "
              "holds the landing for a fix.", "",
              "After this page come each unit's change as the bolt holds it, then what the bolt changes against main, "
              "from where it last met main to its head, less its change folders, shown whole before it."]
    if len(parts) > 1:
        lines += ["", f"That diff comes in {len(parts)} files, each holding whole files' changes in git's order, since "
                      f"plannotator opens no file over {megabytes(PLANNOTATOR_MOST)}."]
    if past:
        url = f"https://github.com/{whole['repo']}/compare/{whole['base']}...{head}"
        lines += ["", f"Left out of this reading, {plural_of(len(past), 'file', 'files')} whose change alone passes the "
                      f"{megabytes(PLANNOTATOR_MOST)} plannotator opens in one file, each named in its place in the diff:", ""]
        lines += [f"- `{p}`, {megabytes(n)}" for p, n in past]
        lines += ["", f"Read {'it' if len(past) == 1 else 'them'} whole in GitHub's compare view of the bolt against main, "
                      f"{url}, or on {whole['host']} with `git -C {whole['main']} diff {whole['base']} {head} -- <path>`."]
    out = [(f"00-{bolt}.md", "\n".join(lines) + "\n")]
    for k, (u, files) in enumerate(changes, 1):
        out += [(f"{k:02d}-{u}-{p.replace('/', '-')}", text) for p, text in sorted(files, key=lambda f: change_order(f[0]))]
    n = len(changes) + 1
    if len(parts) == 1:
        return out + [(f"{n:02d}-{bolt}-diff.txt", parts[0])]
    return out + [(f"{n:02d}-{bolt}-diff-{k}-of-{len(parts)}.txt", text) for k, text in enumerate(parts, 1)]


# The most bytes plannotator opens in one file: a file one byte longer, by its size on disk, is refused with "File too
# large to annotate (max 2MB)", and with it the whole review that names it, while a review of several files has no cap
# on them together (plannotator 0.28.48, MAX_ANNOTATABLE_FILE_BYTES in resolveAnnotateBundleFiles; read 2026-11-05 on
# deneb, a file of exactly this many bytes opening, one of a byte more refused, and five of 7.8 MB together opening,
# each served whole).
PLANNOTATOR_MOST = 2 * 1024 * 1024


def megabytes(n):
    """A count of bytes in MB as plannotator counts them, 2**20 to one, rounded up to a tenth, so a size past its 2 MB
    never reads 2.0; a whole count with no tenth."""
    tenths = -(-n * 10 // 2**20)
    return f"{tenths // 10} MB" if tenths % 10 == 0 else f"{tenths / 10:.1f} MB"


def diff_path(section):
    """The file a section of git's diff is of, from its header, `diff --git a/<path> b/<path>`: the path when both
    sides name it alike, else the two sides as git wrote them, as for a rename or a path git quotes."""
    sides = section.split("\n", 1)[0].removeprefix("diff --git ")
    p = sides[2:2 + (len(sides) - 5) // 2]
    return p if sides == f"a/{p} b/{p}" else sides


def diff_parts(diff, most=PLANNOTATOR_MOST):
    """A bolt's diff as its landing's reading holds it, so plannotator opens every file of it: (parts, past). parts, the
    texts of its files, git's sections, one to a file changed, each whole and in git's order, as many to a part as keep
    it within most bytes as UTF-8, a new part begun where the next section would pass it. past, [(path, bytes)] in git's
    order, each file whose own section passes most, which no part can hold whole and none holds cut (sluice core.43: an
    item is never cut within itself to fit a limit): a line in its place says so, naming it and its size, and the
    reading's first page says where to read it whole (landing_reading)."""
    parts, past, part, size = [], [], [], 0
    for section in re.split(r"(?m)^(?=diff --git )", diff):
        if not section:
            continue
        n = len(section.encode())
        if n > most:
            path = diff_path(section)
            past.append((path, n))
            section = (f"{path}: its change, {megabytes(n)}, passes the {megabytes(most)} plannotator opens in one file, "
                       "so it is not in this reading; its first page says where to read it whole.\n")
            n = len(section.encode())
        if part and size + n > most:
            parts.append("".join(part))
            part, size = [], 0
        part.append(section)
        size += n
    if part:
        parts.append("".join(part))
    return parts, past


def forward_card(fleet, t, a, label):
    """An old batch card's command for one of its units, run on the host its work ran on (t, batch_at; code.3), as the
    one asking here; its output passed on, and its failure this command's."""
    r = crew.on_machine(fleet, t["machine"], crew.crew_argv(fleet, t["machine"], "card", a.sub, a.key, a.unit, "--label", label))
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode:
        sys.exit(r.returncode)


def batch_at(fleet, label, key, unit):
    """Where a unit a batch card holds was built (batch_unit_at), from the batch in the run record, whether or not the
    card is still open: every unit of the batch for batch/<n>, the k-th five for batch/<n>-<k>."""
    n = int(key.split("/")[1].split("-")[0])
    entries = drive_entries(fleet, label)
    for m, _, units in batches(entries):
        if m == n:
            part = card_part(key, units)
            names = [u for u, *_ in part]
            names or fail(f"batch {n} of {label} has no card {key.partition('-')[2]}")
            between = next((m for u, m, _ in part if u == unit), None) or fail(f"{key} holds {either(names)}, not {unit}")
            return batch_unit_at(fleet, label, between, unit)
    fail(f"{label}'s run record holds no batch {n}")


def card_wait(fleet, a):
    """crew card wait <key>: gone (card-sessions "A decision waits for the next read, and no process waits on a session",
    teams.24): crew keeps no process waiting on a card or its reading, so it is refused at once, with nothing read or
    started, naming crew card read <key>, which reads what the user sent. A card's answer wakes its owner by the fleet's
    wake mod, and the rail's refresh tells the owner once the user sends a reading (card_sweep)."""
    fail(f"crew card wait is gone: crew keeps no process waiting on a card or its reading. Run crew card read {a.key} "
         "when its card's answer wakes you or crew tells you its reading was sent")


OPEN = ("pending", "snoozed", "delegated")  # a card's statuses in Pending You while it still waits on the user


def batch_read_close(closed):
    """Whether a batch whose reading the user sent is recorded read by crew's own close of it (review-batches, briefs.12):
    when no card of it was closed, closed being what row_card_close gave, the card's id or None, or None when no card
    was held, so the user's word holds the batch's landings no longer whatever became of the card."""
    return closed is None


def batch_waited(key, decided, got):
    """What a wait on a batch's card and its session does once either has the user's word (review-batches): ("read",
    what it prints, the card's outcome) once the card is sent back, its note after it as the user wrote it, or the
    session sent, approved or annotated with every annotation as written, or both; ("closed", what it prints, the
    card's status) when Pending You shows the card closed outside crew; None while neither has, the session closed or
    ended undecided among them. decided is the session's result (card_result), got the card as get_request gives it,
    each None when there is none."""
    answer = got.get("answer") if isinstance(got, dict) and got.get("turn") == "agent" else None
    answer = answer if isinstance(answer, dict) else None
    status = got.get("status") if isinstance(got, dict) and isinstance(got.get("status"), str) else None
    sent = decided if decided and decided[0] in ("approved", "annotated") else None
    if answer is None and not sent:
        if status and status not in OPEN and status != "answered":
            return "closed", f"{key}: its card was closed outside crew; Pending You shows it {status}", status
        return None
    lines, notes = [], 0
    if answer is not None:
        note = cards.text_of(answer.get("note")) or cards.text_of(answer.get("text"))
        lines.append(f"{key}: sent back on its card" + (f", with a note:\n{note}" if note else ", with no note"))
        notes += 1 if note else 0
    if sent:
        lines.append(waited(key, sent, True))
        k = sent[2] if len(sent) > 2 else None
        notes = None if k is None and sent[1] else notes + (k if k is not None else 0)
    return "read", "\n".join(lines), read_outcome(notes)


def reading_read(key, got, decided, answered=None, held=False, recorded=True):
    """What crew card read gives of a key with a reading (card-sessions "A batch's or a long proposal's read
    gives its session's decision beside the card's answer", review-batches), a decision of facts alone (code.7): the card as get_request gives it (got,
    None when none is held, it was lost or it could not be read), whether a card of the key is held (held), the
    reading's result (decided, card_result's, None while there is none), whether a session of it is recorded on this
    host (recorded), and a batch's answer in a main-level pane (answered, (who, when) as pane_answered gives it). As
    {lines, close, record, closed, aside, end}: lines, what it prints; close, the outcome its card is closed with, None
    to close none; record, whether crew records the batch read by its own close when no card closed
    (batch_read_close); closed, the status of a card Pending You shows closed outside crew, recorded so; aside, whether
    the reading's decision is set aside so the next session starts anew (reading_decided); end, whether the reading's
    session ends. A batch's, batch/<n>: its pane answer said without the words, its card closed answered; else what the
    card and the reading sent together (batch_waited), the card closed with what was read and the batch recorded read,
    the session ending with the card or, none held, here; nothing sent, that the batch waits on the user. A landing's,
    land/<bolt>: the reading's decision alone, worded as land_waited words it, set aside, crew card session named to
    open it again; nothing sent, that it waits on the user, nothing forgotten or ended. A long proposal's,
    proposal/<n>: the reading's decision after the card's answer, a decided one set aside; nothing while it has none."""
    r = dict(lines=[], close=None, record=False, closed=None, aside=False, end=False)
    sent = bool(decided) and decided[0] in ("approved", "annotated")
    if key.startswith("batch/"):
        if answered:
            said = pane_said(*answered)
            return dict(r, lines=[f"{key}: {said}"], close=said[0].upper() + said[1:], end=True)
        done = batch_waited(key, decided, got)
        if done and done[0] == "read":
            return dict(r, lines=done[1].split("\n"), close=done[2], record=True, end=not held)
        if done:
            return dict(r, lines=[done[1]], closed=done[2], end=True)
        if decided:
            return dict(r, lines=[f"{waited(key, decided, True)}; the batch waits on the user's word on its card, and crew "
                                  f"card session {key} opens its reading again"])
        return dict(r, lines=[f"{key}: nothing sent yet: the batch waits on the user, on its card or its reading"])
    if key.startswith("land/"):
        if decided:
            return dict(r, lines=land_waited(key, decided, True).split("\n")
                        + [f"{key}: its card is left as it is; crew card session {key} opens its reading again"], aside=sent)
        if not recorded:
            return dict(r, lines=[f"{key}: no reading of it runs on this host: crew card session {key} starts it"])
        return dict(r, lines=[f"{key}: its reading waits on the user, who has sent nothing from it"])
    if not decided:
        return r
    said = waited(f"{key}'s reading", decided, True).split("\n")
    if not sent:
        said[0] += f", and its card is still the user's to answer; crew card session {key} opens its reading again"
    return dict(r, lines=said, aside=sent)


def read_outcome(notes):
    """A batch card's close once the user has read the batch (review-batches): with no notes, or the notes the planner
    hands on to their units' work (Decision 6 of the-team-machinery-leaves), counted when crew can count them (None when
    it cannot)."""
    if notes == 0:
        return "Read; no notes"
    if notes is None:
        return "Read; its notes for their units"
    return f"Read; {notes} note{'' if notes == 1 else 's'} for {'its unit' if notes == 1 else 'their units'}"


def waited(name, decided, recorded, gone=False):
    """What a wait on a key's session says once it ends: the user's decision, approved or annotated with their words
    after it as they are, or closed in plannotator with no decision; that crew ended the session (no longer recorded);
    or that it ended with no decision (gone: plannotator lists it serving nothing). None while it runs undecided."""
    if decided:
        said = {"approved": "approved", "annotated": "annotated", "dismissed": "closed in plannotator with no decision"}[decided[0]]
        return f"{name}: {said}" + (f"\n{decided[1].rstrip(chr(10))}" if decided[1] else "")
    if not recorded:
        return f"{name}: crew ended its session, as its card closed or crew card end was run"
    return f"{name}: the session ended with no decision" if gone else None


def land_waited(name, decided, recorded, gone=False):
    """What a wait on a landing's reading says once it ends (card-sessions, briefs.9): its annotations, with the user's
    words as plannotator gives them, as notes on the landing card; an approval, with any words after it, as landing
    nothing, the card's approval being the word to land; a reading crew ended (no longer recorded) as ended with its
    row or by crew card end, which no card's close does (row_card_close); anything else as waited says it. None while
    it runs undecided."""
    words = f"\n{decided[1].rstrip(chr(10))}" if decided and decided[1] else ""
    if decided and decided[0] == "annotated":
        return f"{name}: notes from its reading, as notes on the landing card:" + words
    if decided and decided[0] == "approved":
        return f"{name}: approved in its reading, which lands nothing: the card's approval is the word to land" + words
    if not decided and not recorded:
        return f"{name}: crew ended its reading, as its row was held or left its kit's landings card, or crew card end was run"
    return waited(name, decided, recorded, gone)


def reading_decided(d, decided):
    """A landing's or a long proposal's reading once crew card read printed the user's decision (card-sessions): an
    approval or annotations set aside, as result.<started>.json, and the session forgotten, plannotator having ended
    with the decision, so the next crew card session starts it anew and changes the card's link, and the rail's refresh
    tells nobody of it again (card_sweep). Anything else, and a session crew ended meanwhile, is left as it is."""
    if not decided or decided[0] not in ("approved", "annotated"):
        return
    try:
        lock = open(d / ".lock", "w")
    except FileNotFoundError:
        return  # crew ended the session, its card closed, while the wait printed
    with lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        s = card_recorded(d)
        if s and (d / "result.json").exists():
            (d / "result.json").rename(d / f"result.{re.sub(r'[-:]', '', s['started'])}.json")
            (d / "session.json").unlink()
            untold(d)


def untold(d):
    """A key's reading folder (d) cleared of the told mark the rail's refresh left (sweep_told), once the reading it
    marked is set aside or a new one starts, so the next reading the user sends is told of again."""
    try:
        (d / "told.json").unlink()
    except FileNotFoundError:
        pass


def end_session(label, key, unit=None):
    """End the plannotator session crew started for a card key on this host, an old batch card's (batch/<n>-<k>) for
    one of its units, and forget it: its folder goes first, so a wait on it hears crew ended it, then the recorded pid is sent SIGTERM only
    while plannotator lists it as serving the recorded document (read.4). When plannotator's list can't be read, nothing
    is ended and the session is kept as recorded, so a later rail read ends it (read.1). The answers crew plan answer
    gathered for a proposal's card stay, and with them their folder: they go only with the approval or the decline.
    Returns what it did, in words, and whether it sent SIGTERM. crew's card hook runs it when a crew agent closes or
    withdraws a keyed card, the act when crew closes or withdraws one of its own (row_card_close), and crew card sweep
    for each session the rail judges dead. A session that ended as the user sent it is forgotten, said so. A folder or
    file of the key's that another of these ends swept first, while this one read plannotator's list, is swept as
    empty, never raised, so a wait whose card's close ends the session returns."""
    any(re.fullmatch(k, key) for k in CARD_KEYS) or fail(f"{key} is not a card key")
    d = CARDS / label / key / unit if unit else CARDS / label / key
    key = f"{key} {unit}" if unit else key
    if not d.is_dir():
        return f"no session was running for {key}", False
    try:
        s = card_recorded(d)
    except Refusal:
        s = None
    try:
        decided = card_result(d)
    except Refusal:
        decided = None
    listed, why = plannotator_sessions() if s else (None, None)
    import shutil
    if s and listed is None:
        return end_said(key, s, None, why), False
    try:
        left = list(d.iterdir())
    except FileNotFoundError:
        left = []  # another end swept it first
    for f in left:
        if f.name != "answers.json":
            try:
                shutil.rmtree(f) if f.is_dir() and not f.is_symlink() else f.unlink()
            except FileNotFoundError:
                pass  # another end swept it first
    for p in [d, *d.parents]:
        if p == CARDS / label:
            break
        try:
            if any(p.iterdir()):
                break
            p.rmdir()
        except FileNotFoundError:
            continue  # another end swept it first: swept as empty
        except NotADirectoryError:
            break
    if s and decided and decided[0] != "dismissed" and not serving(listed, s):
        return f"{key}'s session had ended as the user sent it, and {key} is forgotten", False
    if not s or not serving(listed, s):
        return end_said(key, s, listed, why), False
    try:
        os.kill(s["pid"], SIGTERM)
    except ProcessLookupError:
        return f"{key}'s session had already ended, and {key} is forgotten", False
    return f"ended {key}'s session, plannotator pid {s['pid']}", True


def end_said(key, s, listed, why):
    """What crew card end says when it ends nothing (read.1, read.4): plannotator's list could not be read (listed
    None), so the session recorded (s) is kept; none was recorded, so only the key's folder goes; or plannotator lists
    the recorded pid on no session of the recorded document, so nothing is killed and the key is forgotten."""
    if s and listed is None:
        return f"crew can't read plannotator's sessions ({why}): it ended nothing, and keeps {key} to end later"
    if not s:
        return f"no session was recorded for {key}; its folder is removed"
    return f"plannotator lists no session of pid {s['pid']} on {s['document']}: crew ended nothing, and {key} is forgotten"


def card_end(fleet, a):
    """crew card end <key> [<unit>] [--label L]: end the session crew started for a card key on this host, and forget
    the key: a batch card's, batch/<n>, its one session; an old batch card's, batch/<n>-<k>, for one of its units on
    that unit's team's host, or with no unit for each of its units, as its close does."""
    label, _ = card_of(fleet, a, unit_needed=False)
    if not old_batch(a.key):
        print(end_session(label, a.key)[0])
        return
    names = [a.unit] if a.unit else card_units(fleet, label, a.key)
    for u in names:
        t = batch_at(fleet, label, a.key, u)
        if t["machine"] != crew.this_host():
            forward_card(fleet, t, argparse.Namespace(**dict(vars(a), unit=u)), label)
        else:
            print(end_session(label, a.key, u)[0])


def card_asker(fleet, a):
    """The drive and the asker of a crew card read (briefs.16): --label, else the agent's own; the asker the agent
    crew started, else the user at this host. An agent's label is its own."""
    agent, own = crew.caller(fleet), crew.caller_label(fleet)
    not (agent and own and a.label and a.label != own) or fail(
        f"{agent}'s cards are {own}'s: crew card {a.sub} runs as the agent's own drive")
    label = default_label(fleet, a) or fail(f"crew card {a.sub} runs as the card's drive: run it as a crew agent, or add --label")
    if agent:
        os.environ["CREW_LABEL"] = label
    return label, record.who()


def card_held(label, who, key):
    """The card `who` holds under a key on this host, read from its run record; refused when there is none."""
    import cards
    return cards.card_under(cards.host_entries(record, label, crew.this_host()), key, who) or fail(
        f"{who} holds no open card under {key} on {crew.this_host()}")


def row_name(work):
    """A landings row's name from its work: a bolt's own name, a fix of main's main--<name>."""
    return work[5:] if work.startswith("bolt/") else f"main--{work.split('/')[-1]}" if work.startswith("fix/main/") else work


def landing_lines(label, got, heads, earlier=(), unknown=(), stopped=None, main_first=(), gone=None, posted=None):
    """What crew card read land/<kit> prints beside the answer once the user sent the kit's landings card (rail-cards
    "The landings card's read prints the lands crew posted"): the rows they ticked in the card's order (ticked_of, heads
    its rows as card_heads gives them), each with the land crew posted for it on the send and its request (posted,
    {row: request}, lands_posted), or that none is posted yet, crew's next raise of the card posting it, and no command
    for any agent to run (crew-lands-each-bolt-through-flumes-base-place, Decision 10), or that none was ticked, so nothing lands;
    nothing while it waits on them, nor with no card open (got {}, heads []). The bolts an earlier send still lands
    (earlier, sent_left), its card closed, come first, said while this one waits too or with none open, crew's raise
    posting their lands before this card's; each sent bolt crew can't tell of (unknown, [(bolt, why)]) is said, and
    left out of it (rail-cards "The landings card's read prints the lands crew posted"). Each ticked bolt the run
    record holds forecast to conflict with main at the head the card showed (main_first, main_conflict) is left out of
    it too, said to take main first with the user's send standing for it (rail-cards "A ticked bolt taking main in lands
    on its send once it reads proven at a new head"). Each ticked bolt that landed since the card was posted or left the plan (gone, ticked_gone) is
    said so and left out of it, so a send some of whose bolts landed gives the rest alone (rail-cards "The landings
    card's read prints the lands crew posted"). Each bolt it lands whose last landing the runner or Flume stopped
    (stopped, {bolt: (head, words)}, stops) is said with what stopped it and the head it was at, and that it lands
    again only on the user's next send, with no land named for it, its last land being spent (rail-cards "A landing the
    runner or Flume stopped keeps its box")."""
    ticked, earlier, stopped, gone = ticked_of(got, heads), list(earlier), stopped or {}, gone or {}
    lands = [b for b in ticked or [] if b not in main_first and b not in gone]
    lines = [f"  can't tell whether the user's earlier send still lands {b}: {why}" for b, why in unknown]
    lines += [f"  to land on the user's send of an earlier card: {joined(earlier)}"] if earlier else []
    if ticked == []:
        lines += ["  no bolt ticked on this card: nothing of it lands" if earlier else "  no bolt ticked: nothing lands"]
    elif lands:
        lines += [f"  to land, in the card's order: {joined(lands)}"]
    lines += [f"  {b} takes main first until a fix taking main in moves its head, and the user's send stands for it"
              for b in ticked or [] if b in main_first and b not in gone]
    lines += [f"  {b} {gone[b]} since the card was posted, so it is no bolt to land" for b in ticked or [] if b in gone]
    both = earlier + lands
    lines += [f"  {b}'s last landing at {stopped[b][0][:7]} was stopped, nothing of the bolt's: {stopped[b][1].rstrip('.')}; "
              "it lands again only on the user's next send" for b in both if b in stopped]
    posted = posted or {}
    return lines + [f"  {b}: asked of the runner to land, request {posted[b]}" if b in posted else
                    f"  {b}: no land is posted for it yet: crew's next raise of the card posts it" for b in both if b not in stopped]


def send_entries(fleet, label, entries):
    """The run record a read of a kit's landings card's send judges its ticked bolts by: the drive's branch
    (read.5) and this host's entries (entries) it does not hold yet. A branch that can't be read is said, and this
    host's alone read."""
    try:
        whole = drive_entries(fleet, label)
    except Refusal as e:
        print(f"crew reads only this host's run record for what the user's send lands: {e}", file=sys.stderr)
        whole = []
    ids = {e["Id"] for e in whole if e.get("Id")}
    return whole + [e for e in entries if not e.get("Id") or e["Id"] not in ids]


def main_firsts(whole, heads, now=None):
    """The bolts of a kit's landings card the run record (whole, send_entries) holds forecast to conflict with main at
    the head the card showed (main_conflict), heads its rows as card_heads gives them. With now, {bolt: its head now
    where it lives, or None}, as bolt_work reads each such bolt where the kit's forecasts are made, one takes main
    first only while it still stands at that head or the record holds a conflict at the head it moved to: one whose
    take-main fix moved it since lands on the send that ticked it (rail-cards "A ticked bolt taking main in lands on
    its send once it reads proven at a new head"); one whose head now crew can't read still takes main first (read.1). A decision of facts alone (code.7)."""
    shown = {b: h for b, h, _ in heads if main_conflict(whole, b, h)}
    if now is None:
        return set(shown)
    return {b for b, h in shown.items() if not now.get(b) or at_head(h, now[b]) or main_conflict(whole, b, now[b])}


def firsts_now(fleet, label, kit, whole, heads, acts=None):
    """The bolts of a kit's landings card that still take main first at the card's read (main_firsts): each the run
    record holds forecast to conflict with main at the head the card showed, read where it lives now by one acts.work
    where the kit's forecasts are made (bolt_work)."""
    shown = main_firsts(whole, heads)
    if not shown:
        return shown
    worked = (acts or CardActs(fleet)).work(label, kit, {b: (h, None) for b, h, _ in heads if b in shown})
    return main_firsts(whole, heads, {b: (w or {}).get("head") for b, w in worked.items()})


def landed_since(entries, card):
    """The bolts the run record (entries) holds landed since a landings card was posted: each bolt/<bolt> of a
    bolt.submit that landed (Outcome landed) or a bolt.land, not refused, at or after the card's first entry, its post
    or a change; none when the record holds no entry of the card. A decision of facts alone (code.7)."""
    since = min((e["At"] for e in entries if e.get("Card") == card and e.get("At") and not e.get("Refused")), default=None)
    if since is None:
        return set()
    return {o[5:] for e in entries if not e.get("Refused") and (e.get("At") or "") >= since
            and (e.get("Act") == "bolt.land" or (e.get("Act") == "bolt.submit" and e.get("Outcome") == "landed"))
            for o in e.get("On") or [] if o.startswith("bolt/")}


def ticked_gone(ticked, in_plan, landed):
    """Of the bolts the user ticked on a kit's landings card (ticked, ticked_of), each that no longer lands on it, with
    why: landed since the card was posted (landed, landed_since), as the bolts of a group landing sluice took are while
    another it refused takes main in, or no longer in the plan (in_plan, the plan's bolts of the kit): {bolt: "landed"
    or "left the plan"}. A decision of facts alone (code.7)."""
    return {b: "landed" if b in landed else "left the plan" for b in ticked or [] if b in landed or b not in in_plan}


def landings_earlier(fleet, label, kit, key, who, entries, heads, acts=None):
    """The bolts an earlier send on a kit's landings card still lands beside the card who holds under key now, if any
    (heads its rows, [] for none), from this host's run record (entries), where ops's closes and submissions are
    (landings_sent, refusals), the drive's plan, read only when such a send stands, and each sent bolt's head now
    and its own work since the send, read by one acts.work where the kit's forecasts are made (bolt_work): (bolts,
    [(bolt, why)]) as sent_left gives them, a bolt on a row of the card read now being that card's to ask for. Refused
    naming the plan when it can't be read, since what the send still lands can't be told without it (read.1)."""
    on = {b for b, _, _ in heads}
    sent = {b: h for b, h in landings_sent(entries, key, who).items() if b not in on}
    if not sent:
        return [], []
    plan = plan_of(fleet, label) or fail(f"{label}/main could not be read, so what an earlier send on {key} still lands can't be told")
    in_plan = {b.name() for b in plan.bolts() if b.get("Repo") == kit}
    moves = {b: (h, None) for b, h in sent.items() if b in in_plan}
    work = (acts or CardActs(fleet)).work(label, kit, moves) if moves else {}
    return sent_left(sent, {b: (work.get(b) or {}).get("head") for b in moves}, in_plan, refusals(entries), work)


def landings_unopened(fleet, a, label, who, kit, entries, acts=None):
    """crew card read land/<kit> when who holds no landings card of the kit open (rail-cards "The landings card's read
    prints the lands crew posted", "A send's lands are posted by the first act that reads it"): that no card is open,
    then what an earlier send still lands at each bolt's head now and
    the land crew posted for it, and each bolt crew can't tell of, left out of it (landings_earlier,
    landing_lines); with --json, the same as {key, card: null, earlier, unknown}. Refuses nothing but what it can't read
    (read.1)."""
    earlier, unknown = landings_earlier(fleet, label, kit, a.key, who, entries, [], acts)
    if a.json:
        print(json.dumps(dict(key=a.key, card=None, earlier=earlier, unknown=dict(unknown)), indent=1, ensure_ascii=False))
        return
    posted = {row_name(p["work"]): p["request"] for p in lands_posted(entries)}
    print("\n".join([f"card {a.key}: no landings card of {kit} is open"] + landing_lines(label, {}, [], earlier, unknown,
                                                                                          stops(entries), posted=posted)))


def card_read(fleet, a, acts=None):
    """crew card read <key> [--label L] [--json]: where the card the asker holds under the key stands, read from
    Pending You: its status, whose turn it is, and on the asker's turn the user's answer and words; for a kit's
    landings card, land/<kit>, the bolts they ticked in the card's order and the land crew posted for each, no command,
    those an earlier send still lands, whose card closed as this one followed it, first (landings_earlier,
    landing_lines), each ticked bolt that landed since the card was posted or left the plan said so and left out of it
    (ticked_gone), the plan read for it, and refused naming it when it can't be (read.1), each whose last landing the runner or Flume stopped said with what stopped it (stops), and with no
    card of the kit open, those alone (landings_unopened). A kit's landings card the user sent is raised first, here on
    the drive's main machine (land_hand), what it says on standard error, so the send is acted on at once: a bolt
    ticked that was left and conflicts with main is held taking main first, recorded so and nobody told (main_told),
    and the bolts the read gives to land leave out each the run record holds so (main_firsts). An approval the user
    declined is then closed with their words, and the close recorded (record 0031 §1), with what they answered in
    crew's words (cards.answer_said); nothing else is. A key with a reading gives what the user sent in it too
    (reading_read), since nothing of crew's waits on it (teams.24): a batch's, batch/<n>, its card and its reading
    together, closing the card and recording the batch read (batch_card_read); a bolt's reading, land/<bolt>, its
    decision alone, to main-level ops (land_reading_read), unless the caller holds a card of the bolt's own under
    the key, as a conductor posted one before a kit had its landings card, which is read as any card; a long
    proposal's, its reading's decision after the card's answer, a decided one set aside. A card read answered has the
    user's answer recorded first, once, in crew's words, a kit's landings card's with the bolts they ticked at the
    heads it showed (answer_seen), before a declined approval is closed or the kit's card raised."""
    import cards
    acts = acts or CardActs(fleet)
    label, who = card_asker(fleet, a)
    kind = land_key(a.key, kits_read(fleet, label))
    if re.fullmatch(r"batch/\d+", a.key):
        return batch_card_read(fleet, label, a.key, who, a.json)
    if (kind and kind[0] == "bolt" and re.fullmatch(r"land/[a-z0-9][a-z0-9-]*", a.key)
            and not cards.card_under(cards.host_entries(record, label, crew.this_host()), a.key, who)):
        return land_reading_read(fleet, label, a.key, who, a.json)
    if kind and kind[0] == "kit":
        entries = cards.host_entries(record, label, crew.this_host())
        if not cards.card_under(entries, a.key, who):
            return landings_unopened(fleet, a, label, who, kind[1], entries)
    card = card_held(label, who, a.key)
    with cards.Bridge(who, "Read it again later.", (a.key, card)) as py:
        got = py.call("get_request", {"requestId": card, "name": who})
        if got.get("status") == "answered":  # the user's answer recorded first, the first time crew reads it (Decision 1)
            held = cards.host_entries(record, label, crew.this_host())
            shown = shown_heads(held, card) if kind and kind[0] == "kit" else None
            answer_seen(acts, label, who, a.key, card, got, held, card_heads(shown) if shown is not None else None,
                        offered_boxes(shown) if shown is not None else ())
        words = cards.declined(got)
        if words is not None:
            tool, args, _ = cards.close_call(got, card, who, cards.declined_outcome(words))
            py.call(tool, args)
    if kind and kind[0] == "kit" and words is None and got.get("status") == "answered":
        with contextlib.redirect_stdout(sys.stderr):  # the read's own output is the answer; a raise that fails is said
            land_hand(fleet, label, kind[1])
    if a.json:
        print(json.dumps(got, indent=1, ensure_ascii=False))
    else:
        entries = cards.host_entries(record, label, crew.this_host()) if kind and kind[0] == "kit" else []
        heads = card_heads(next((e.get("Heads") for e in reversed(entries) if e.get("Card") == card and e.get("Heads")
                                 and not e.get("Refused")), None))
        earlier, unknown = landings_earlier(fleet, label, kind[1], a.key, who, entries, heads) if kind and kind[0] == "kit" else ([], [])
        ticked = ticked_of(got, heads) if kind and kind[0] == "kit" else None
        first, gone, whole = set(), {}, entries
        if ticked:  # what the send still lands: no bolt taking main first, landed since or gone from the plan
            whole = send_entries(fleet, label, entries)
            plan = plan_of(fleet, label) or fail(f"{label}/main could not be read, so which bolts {a.key}'s send still lands can't be told")
            first = firsts_now(fleet, label, kind[1], whole, heads)
            gone = ticked_gone(ticked, {b.name() for b in plan.bolts() if b.get("Repo") == kind[1]}, landed_since(whole, card))
        d = CARDS / label / a.key
        reads = a.key.startswith("proposal/") and d.is_dir()
        decided = card_result(d) if reads else None
        r = reading_read(a.key, got, decided) if reads else dict(lines=[], aside=False)
        print("\n".join(cards.answer_lines(a.key, card, got)
                        + (landing_lines(label, got, heads, earlier, unknown, stops(entries), first, gone,
                                         {row_name(p["work"]): p["request"] for p in lands_posted(whole)})
                           if kind and kind[0] == "kit" else []) + r["lines"]))
        if r["aside"]:
            reading_decided(d, decided)
    if words is not None:
        record.emit(label, "card.close", [cards.row_object(a.key, kits_read(fleet, label)) or f"agent/{who}"], Card=card,
                    Key=a.key, State="declined", Outcome=cards.declined_outcome(words), Answer=cards.answer_said(got))
        print(f"card {a.key}: {card} closed, as the user declined it")


def reading_said(key, got, r, as_json):
    """What crew card read prints of a key with a reading, r as reading_read gives it: its lines, or with --json the
    key, the card as get_request gave it and the lines."""
    print(json.dumps(dict(key=key, card=got, said=r["lines"]), indent=1, ensure_ascii=False) if as_json else "\n".join(r["lines"]))


def batch_card_read(fleet, label, key, who, as_json=False, acts=None):
    """crew card read batch/<n>: the planner's read of a batch's card and its one reading together, on the main level's
    host, once the card's answer wakes it or crew tells it the reading was sent (review-batches, card-sessions), what
    reading_read gives: the batch answered in a main-level pane (pane_answered) said without the words, its card closed
    answered and the reading ended; else what the card and the reading sent, the card's note and every annotation as
    the user wrote them, the card closed with what was read, which ends the reading (row_card_close), and, when no card
    closed, none held, it was lost or Pending You refused its close, the batch recorded read by crew's own close,
    batch.close on batch/<n> in the planner's name (batch_read_close, briefs.12), the reading ended here when no card
    was held; a card closed outside crew recorded closed as Pending You shows it, the reading ended; nothing sent, that
    the batch waits on the user, nothing closed. A card Pending You no longer finds is recorded lost and the reading
    still read; one it can't read is said, and read past when the reading has the user's word. Refused off the main
    level's host, to any agent but the planner, and with neither a card nor a reading of the batch on this host."""
    acts = acts or CardActs(fleet)
    here, owner = acts.host(), f"{label}-planner"
    why = session_refusal(key, label, fleet["drives"][label]["machine"], here)
    not why or fail(why)
    "@" in who or who == owner or fail(f"{key}'s card and reading are {owner}'s to read, not {who}'s")
    entries, d = acts.entries(label), CARDS / label / key
    card, s, decided = cards.card_under(entries, key, owner), card_recorded(d), card_result(d)
    card or s or decided or fail(f"no card and no reading of {key} is open on {here}: crew raises both when the reviewer's "
                                 f"summary is delivered, with crew review {label} --wait")
    answered, got = pane_answered(entries).get(key), None
    if card and not answered:
        try:
            with acts.bridge(owner, "Read it again later.") as py:
                got, words = py.answer("get_request", {"requestId": card, "name": owner})
        except Refusal as e:
            words = str(e)
        if words is not None and cards.lost(words, owner):
            card_lost(acts, label, owner, key, card, words)
            card = None
        elif words is not None:
            got = None
            decided and decided[0] != "dismissed" or fail(f"crew can't read {key}'s card {card} now: {words}; read it again later")
            print(f"{key}: crew can't read its card {card} now: {words}", file=sys.stderr)
    r = reading_read(key, got, decided, answered, held=bool(card))
    reading_said(key, got, r, as_json)
    out = sys.stderr if as_json else sys.stdout
    with contextlib.redirect_stdout(out):
        closed = None  # the card a close closed, whose close ends the reading too
        if r["close"]:
            closed = row_card_close(fleet, label, owner, key, outcome=r["close"], acts=acts) if card else None
            if r["record"] and batch_read_close(closed):
                acts.emit(label, "batch.close", [cards.row_object(key) or key], by=owner,
                          why=f"batch({key.split('/', 1)[1]}): read in its session", Key=key, State="read", Outcome=r["close"])
                print(f"{key}: recorded read, {r['close']}")
        elif r["closed"]:
            acts.emit(label, "card.close", [cards.row_object(key)], by=owner, Card=card, Key=key, State=r["closed"],
                      Outcome="closed outside crew", Answer=cards.answer_said(got))
        if r["end"] and not closed:
            ended = acts.end(label, key)
            if ended:
                print(ended)


def land_reading_read(fleet, label, key, who, as_json=False, acts=None):
    """crew card read land/<bolt>: main-level ops's read of a bolt's landing's reading (reading_owner), on the host its
    work runs on (bolt_at), once crew tells it the user sent it (card-sessions "A landing's read gives its
    session's decision alone and leaves its card"), what reading_read gives: its annotations word for word as notes on the bolt's row of
    its kit's landings card, an approval as landing nothing, the card's approval being the word to land, the decision
    then set aside so the next crew card session starts the reading anew (reading_decided); nothing sent, that it
    waits on the user, nothing forgotten or ended. The kit's landings card, ops's own under land/<kit>, is left as it
    is. Refused for a bolt the plan does not hold or not started, off its host, and to any agent but ops."""
    acts = acts or CardActs(fleet)
    kits, bolt = kits_read(fleet, label), key.split("/", 1)[1]
    _, b, t = land_held(fleet, label, bolt)
    b or fail(f"{label}'s plan holds no bolt {bolt}, so {key} has no reading")
    t or fail(f"bolt {bolt} is not started, so it is no row of its kit's landings card, and it has no reading")
    why = session_refusal(key, label, fleet["drives"][label]["machine"], acts.host(), t["machine"], kits)
    not why or fail(why)
    owner = reading_owner(label, key)
    "@" in who or who == owner or fail(f"{key}'s reading is {owner}'s to read, not {who}'s")
    d = CARDS / label / key
    decided = card_result(d) if d.is_dir() else None
    r = reading_read(key, None, decided, recorded=bool(card_recorded(d)) if d.is_dir() else False)
    reading_said(key, None, r, as_json)
    if r["aside"]:
        reading_decided(d, decided)


# ------------------------------------------------------------------------------------- a batch answered in a pane

ANSWERERS = ("planner", "operator")  # the main-level roles in whose pane the user answers a batch (briefs.12)


def pane_answer_refusal(n, entries, v, kind):
    """Why crew card answer records no answer of batch n (review-batches, briefs.12), or None: the caller is not the
    drive's planner or operator, whose kind it is (role); the run record's entries, oldest first, hold no batch n;
    a card key of it is closed (batch_closed), by a tap, its reading session's send or a pane, naming in whose pane and
    when for a pane's (pane_answered); every card of it waits on nothing (batch_settled); or the verdict v on the words
    in the caller's own transcript (transcript.check, want="user") does not read them as the user's (signals.5), naming
    who said them. A decision of facts alone (code.7)."""
    head = f"crew records no answer of batch {n}"
    if kind not in ANSWERERS:
        return (f"{head}: only the planner and the operator record a batch the user answered in their pane, in the "
                "user's own words; the user answers a batch on its card or in one of those two panes")
    made = [units for m, _, units in batches(entries) if m == n]
    if not made:
        return f"{head}: the run record holds no batch {n}"
    keys = [k for k, _ in batch_cards(n, made[-1], batch_posts(entries))]
    closed, answered = batch_closed(entries), pane_answered(entries)
    done = [k for k in keys if k in closed]
    if done:
        how = pane_said(*answered[done[0]]) if done[0] in answered else "answered on its card or in its reading session"
        return f"{head}: batch {n} was {how} already"
    settled = batch_settled(entries)
    if all(k in settled for k in keys):
        return f"{head}: {settled[keys[0]]}"
    return words_refusal(head, v, "answer a batch", "the user answers a batch on its card or in your pane")


def words_refusal(head, v, what, advice):
    """Why crew takes no words the user said in the caller's pane to what, after head, or None: the verdict v on the
    words in the caller's own transcript (transcript.check, want="user") reads them as the user's (signals.5), and not
    only in a word from the board, which answers nothing (record 0038 §3, record 0010), so the caller is given advice;
    else why not, naming who said them, and for another agent's tell, telling the caller to tell that agent advice. A
    decision of facts alone (code.7)."""
    if v.grade == "verified" and v.asserted_by == "user" and v.board:
        return f"{head}: the words came from the board, which answers nothing; {advice}"
    if v.grade == "verified" and v.asserted_by == "user":
        return None
    if v.grade == "unverified":
        return f"{head}: crew can't read your session's transcript, so it can't tell the words are the user's: {v.reason}"
    if v.grade == "refused":
        return (f"{head}: the words are not in a record your session received; only the user's own words {what}, "
                "quoted as they wrote them in your pane, never your own")
    if v.grade == "found":
        return f"{head}: the words are in a record of your transcript crew can't read as anyone's, so it can't tell they are the user's"
    if v.asserted_by.startswith("agent:"):
        other = v.asserted_by[6:]
        return f"{head}: the words are {other}'s, passed on with crew tell, and not the user's; tell {other} that {advice}"
    return f"{head}: the words are " + ("crew's own message" if v.asserted_by == "crew" else "a tool's output") + ", not the user's"


def settled_refusal(n, kit, v):
    """Why crew record <kit> <n> --proposed --settled-in-pane records no record settled in the pane (briefs.15,
    signals.5), or None: the verdict v on the user's yes in the caller's own transcript (words_refusal) does not read
    the words as the user's. No caller is refused by who it is (roles.2): the record names who ran it and in which
    session. Each refusal sends the record to its card. A decision of facts alone (code.7)."""
    head = f"crew records record {n:04d} in {kit} as settled in no pane"
    why = words_refusal(head, v, "settle a record", "the user settles a record in your pane or on its card")
    return why and f"{why}; run crew record {kit} {n} --proposed without --settled-in-pane, and the user answers on its card"


def answer_said(n, by, words):
    """What crew card answer tells the planner when the operator recorded the answer (review-batches; Decision 6 of
    the-team-machinery-leaves, a batch's notes the planner's to hand on): the batch, whose pane, and the user's words
    whole, to hand on as a batch's notes."""
    return (f'Batch {n} was answered in {by}\'s pane: "{words}". Hand each unit\'s part on to its work, as you hand on a '
            "batch's notes.")


def batch_answer(fleet, a, acts=None):
    """crew card answer batch/<n> --excerpt "<words>" [--label L]: the user's answer to batch n in their own words in
    the caller's pane, the planner's or the operator's, recorded once crew reads the words in the caller's own session
    transcript on this host as the user's (pane_answer_refusal). Run on this host, never forwarded, since the
    transcript is here. One batch.answer entry on batch/<n>, naming the batch, the transcript record the words were
    read from and their length, never the words (record.3); then the planner's card of the batch held on this host
    closed answered with the words, its reading session ended with it (row_card_close), or, with none held here, the
    host the card was posted from named, whose rail's sweep closes it; and, when the operator ran it, the planner told
    the words, crew's tell, to send on as the batch's notes. Refused for any key but batch/<n>."""
    acts = acts or CardActs(fleet)
    m = re.fullmatch(r"batch/(\d+)", a.key or "") or fail(
        f"crew card answer records a batch's answer, under its key batch/<n>, not {a.key}")
    n, key, words = int(m.group(1)), a.key, a.excerpt
    words.strip() or fail("crew card answer needs the user's words: --excerpt \"<their words, as they wrote them>\"")
    who = acts.caller()
    kind, label = role(fleet, who)
    entries, v, sid = [], None, None
    if kind in ANSWERERS:
        a.label in (None, label) or fail(f"{who} answers {label}'s batches, not {a.label}'s")
        CONTEXT["label"] = label
        v, sid = acts.heard(words)
        entries = acts.drive(label)
    why = pane_answer_refusal(n, entries, v, kind)
    not why or fail(why)
    rid = v.uuid or f"line-{v.line_hash()[:16]}"
    acts.emit(label, "batch.answer", [key], frm=[f"session/{sid}/{rid}"], Key=key, Batch=str(n), Chars=len(words))
    print(f"batch {n} answered in {who}'s pane" + (f":\n{words}" if kind == "planner" else ""))
    owner, here = f"{label}-planner", acts.host()
    held = cards.card_under(acts.entries(label), key, owner)
    row_card_close(fleet, label, owner, key, outcome=f"Answered in {who}'s pane", said=f"Answered in {who}'s pane: {words}", acts=acts)
    if not held:
        posted = [e for e in entries if e.get("Act") == "card.post" and e.get("Key") == key and e.get("Card") and not e.get("Refused")]
        there = posted[-1].get("Host") if posted else None
        print(f"card {key}: its card was posted from {there}, whose rail's sweep closes it answered" if there and there != here
              else f"card {key}: no card of it is held on any host")
    if kind == "operator":
        if acts.tell(owner, answer_said(n, who, words)):
            print(f"{owner} was told the user's words, to hand each unit's part on to its work")
        else:
            print(f"crew could not tell {owner} the user's words, and batch {n} stands answered: tell {owner} them "
                  "yourself with crew tell, as the user wrote them")


# ---------------------------------------------------------------------------------------------- a card's preview

# A card's preview is asked of the runner on the host where the thing's work runs, by a request on the drive's branch,
# and read from that runner's report (Decisions 1 to 8 of a-cards-preview-is-asked-of-the-runner): crew keeps no
# record of a preview of its own, runs no sluice command for one, and reads no kit's policy for it.


def dashed(name):
    """A card's key or a thing as a file's name: each / written -."""
    return name.replace("/", "-")


# What a card's change note says of a preview, by its word (runner.preview_word; Decision 4 of
# a-cards-preview-is-asked-of-the-runner): "<thing>: Its preview of <h> " and one of these.
PREVIEW_NOTES = {"asked": "is asked of the runner on {host}", "held": "waits for room on {host}", "coming": "is coming up",
                 "up": "is up", "failed": "did not come up", "refused": "could not be brought up",
                 "unread": "could not be brought up", "unlisted": "is gone", "ask": "is put away"}


def asked_note(thing, p):
    """The change note of a card that carries a preview (rail-cards "Brought up", "A card is changed in place when the
    runner reports its preview anew"), from what the card now says of it (p, as cards.preview_said takes it): that the
    thing's preview is asked of the runner on its host, waits for room there, is coming up, is up, did not come up,
    could not be brought up, is gone, or, the card offering it again, is put away."""
    return f"{thing}: Its preview of {p['head'][:7]} " + PREVIEW_NOTES[runner.preview_word(p)].format(host=p.get("host"))


def preview_changed(fleet, label, key, note):
    """A preview's change said on the card it was asked from (rail-cards "A preview that fails is said on the card"):
    the card's raise handed to the drive's main machine with the note, a kit's landings card's (land_hand), where
    the row is read again, or a batch's (batch_hand); changed in place while it waits on the user, and left as it is
    once they answered it."""
    m = re.fullmatch(r"batch/(\d+)", key)
    if m:
        batch_hand(fleet, label, int(m.group(1)), note)
    else:
        land_hand(fleet, label, key.split("/", 1)[1], landing_act("preview", words=note)[1])


def preview_target(key, thing, carried, unread=None):
    """What brings a card's thing up (rail-cards "A thing the card does not carry"), from facts alone: carried, {thing:
    (branch, revision)}, each thing the card carries that must run, or None for one whose branch and revision are read
    where its work is; unread, {thing: why} for each whether it must run can't be told. Refused for a thing the card
    does not carry, naming those it does and those it can't tell of (read.1)."""
    thing in carried or fail(f"{key} carries no {thing} to bring up: " + (
        f"it carries {joined(sorted(carried))}" if carried else "it carries nothing that must run")
        + "".join(f"; whether {t} has a preview can't be told: {why}" for t, why in sorted((unread or {}).items())))
    return carried[thing]


def preview_owner(key, label, kits):
    """Whose card carries a thing crew card preview brings up: main-level ops's for a kit's landings card, land/<kit>,
    the planner's for a batch's, batch/<n>; refused for any other key, naming the two."""
    kind = land_key(key, kits)
    if kind and kind[0] == "kit":
        return f"{label}-ops"
    if re.fullmatch(r"batch/\d+", key):
        return f"{label}-planner"
    fail(f"{key} carries nothing crew brings up: crew card preview takes a kit's landings card, land/<kit>, or a batch's, batch/<n>")


def preview_caller(caller, owner, key):
    """Why the caller may not bring up or put away what a card carries (rail-cards "Asked by anyone but the owner"), or
    None: an agent other than the card's owner, who acts on the user's words on its own card; a person may."""
    if "@" in caller or caller == owner:
        return None
    return f"{key} is {owner}'s card: {owner} brings up what it carries, on the user's words on it"


def card_preview(fleet, a, acts=None):
    """crew card preview <key> <thing> [--done] [--label L]: run by a card's owner on the user's words on the card
    (rail-cards "The user asks for a preview by writing on the card", record 0043), main-level ops's for land/<kit>
    and the planner's for batch/<n> (preview_owner, preview_caller), on the drive's main machine, where the card
    is (code.3), asking the runner on the host where the thing's work runs and nothing of that host itself (Decision 6
    of a-cards-preview-is-asked-of-the-runner): the thing read from what the card carries (preview_thing); then one
    plan write of one request (state.1, plan.1), a bring-up where crew's ask of that revision on that host does not
    stand as the runner reports it (runner.ask_step), or, with --done, the done of each standing ask of it, its entry
    card.preview on the work with the card's key and asked or done (record.1); and the card changed in place with the
    note (preview_changed). An ask that stands is given back as the runner reports it, nothing written; a done with
    none standing is said, nothing written. It answers once the write is made, naming the request and what the card
    now says (code.9): the runner answers at its next pass, and the rail's read follows it (rail_read). Refused for any
    other key, caller or thing, writing nothing."""
    acts = acts or CardActs(fleet)
    label = default_label(fleet, a) or fail("crew card runs as the card's drive: run it as a crew agent, or add --label")
    owner = preview_owner(a.key, label, acts.kits(label))
    why = preview_caller(acts.caller(), owner, a.key)
    not why or fail(why)
    main = crew.drive_of(fleet, label)["machine"]
    if acts.host() != main:
        return acts.forward(main, ["card", "preview", a.key, a.thing, *(["--done"] if a.done else []), "--label", label])
    requests, reads = acts.runner(label)
    target = preview_thing(fleet, label, a.key, a.thing, owner, a.done, acts)
    CONTEXT.update(label=label, work=target["work"])  # a refusal's entry names it (named)
    standing = runner.previews_standing(requests, reads)
    if a.done:
        asks = [r for k, r in sorted(standing.items(), key=lambda kr: runner.number(kr[1].get("Request")) or 0)
                if (k == target["at"] if target.get("at") else r.get("Work") == target["work"] and r.get("Repo") == target["repo"])]
        if not asks:
            print(f"crew asked for no preview of {a.thing} that stands, from {a.key} or another card, so nothing is put away")
            return
        made = []
        preview_written(fleet, label, a.key, a.thing, asks, done=True, made=made)
        shown = {"branch": asks[-1].get("Branch"), "head": asks[-1].get("Revision"), "state": "ask", "released": asks[-1].get("Revision")}
        note = asked_note(a.thing, shown)
        print(f"request {', '.join(str(n) for n in made)}: {note}")
        preview_changed(fleet, label, a.key, note)
        return
    k = target["at"]
    ask = standing.get(k)
    report = runner.preview_report(reads, ask) if ask is not None else None
    if runner.ask_step(ask, report) == "keep":
        print(f"crew's ask of {a.thing}'s preview of {k[2][:7]} stands, as request {ask.get('Request')}, so none is written: "
              + preview_shown_said(a.thing, report))
        return
    made = []
    preview_written(fleet, label, a.key, a.thing, [dict(Work=target["work"], Host=k[0], Repo=k[1], Branch=target["branch"], Revision=k[2])],
                    done=False, made=made)
    note = asked_note(a.thing, {"head": k[2], "host": k[0], "state": "asked"})
    print(f"request {made[0]}: {note}")
    preview_changed(fleet, label, a.key, note)


def preview_shown_said(thing, p):
    """What a card says of a thing's preview, in a line: its change note, with the addresses listed or why it is not
    there."""
    return asked_note(thing, p) + (": " + ", ".join(f"{k} {v}" for k, v in p["addresses"].items()) if p.get("addresses") else
                                   f": {p['words']}" if p.get("state") == "refused" and p.get("words") else
                                   f": {p['why']}" if p.get("why") else "")


def preview_written(fleet, label, key, thing, asks, done, made, by=None):
    """One plan write of a card's preview requests (Decision 6 of a-cards-preview-is-asked-of-the-runner; state.1,
    plan.1): for each of asks, a bring-up, or with done its done, naming its host, work, repository, branch and
    revision (runner.preview_fields); the facts read again at the tip it is applied to, so a bring-up whose ask now
    stands there, or a done whose ask stands no more, is refused, writing nothing. Its entry is card.preview on each
    work, the card's key and asked or done (record.1), holding no words (record.3), in the name of by, the card's
    owner, for a done crew writes of its own as a row or card ends. Each request's number appended to made."""
    state = "done" if done else "asked"

    def change(w):
        have = requests_of(w).recs("Request")
        standing = runner.previews_standing(have, w.runners())
        for r in asks:
            k, h = (r.get("Host"), r.get("Repo"), r.get("Revision")), (r.get("Revision") or "")[:7]
            ask = standing.get(k)
            if done and (ask is None or ask.get("Request") != r.get("Request")):
                fail(f"crew's ask of {thing}'s preview of {h} on {k[0]} stands no more at {label}/main's tip, so its done is not written")
            if not done and runner.ask_step(ask, runner.preview_report(w.runners(), ask) if ask is not None else None) == "keep":
                fail(f"crew's ask of {thing}'s preview of {h} on {k[0]} stands at {label}/main's tip, as request "
                     f"{ask.get('Request')}, so none is written")
            made.append(request(w, "preview", r.get("Work"), **runner.preview_fields(k[0], k[1], r.get("Branch"), k[2], done)))
        return []
    how = "put away" if done else "asked"
    write(fleet, label, change, f"plan(card): preview of {thing} {how} from {key}", act="card.preview",
          on=sorted({r.get("Work") for r in asks}), fields={"Key": key, "State": state}, by=by)


def preview_thing(fleet, label, key, thing, owner, done, acts):
    """What a card's thing names for its preview (Decision 6 of a-cards-preview-is-asked-of-the-runner), read on the
    drive's main machine, nothing run on the work's host: {work, repo, branch, at: (host, repo, revision)}. A
    landings row's bolt among the card's last recorded rows (card_heads), bolt/<bolt> on the host whose runner took its
    work (land_held, bolt_at), its repository as the plan names it, at its row's full head read afresh as the raise
    reads it (CardActs.land_row), refused while the row can't land, naming why; with done, the row is not read, its
    work and repository naming its standing asks. A batch line's <unit>/<name> of a unit of the batch, unit/<unit> on
    the host its unit was built on (batch_unit_at), its repository its bolt's newest launch's, at the branch and
    revision its made lines hold (CardActs.made). Refused for a thing the card does not carry (preview_target), or
    whose host or row crew can't read (read.1)."""
    entries = acts.entries(label)
    if key.startswith("land/"):
        card = cards.card_under(entries, key, owner)
        rows = card_heads(next((e.get("Heads") for e in reversed(entries) if e.get("Card") == card and e.get("Heads")
                                and not e.get("Refused")), None)) if card else []
        preview_target(key, thing, {b: None for b, _, _ in rows})
        kit = key.split("/", 1)[1]
        if done:
            return {"work": f"bolt/{thing}", "repo": kit}
        _, b, t = land_held(fleet, label, thing)
        b or fail(f"{label}'s plan holds no bolt {thing}, so its preview is not asked")
        t or fail(f"bolt {thing} is not started, so its preview is not asked")
        row, why = acts.land_row(label, thing, t["machine"])
        row is not None or fail(f"{key}'s row {thing} can't be read, so its preview is not asked: {why}")
        row.get("box") or fail(f"{key}'s row {thing} can't land now, so its preview is not asked: {row.get('why')}")
        head = row["facts"]["head"]
        return {"work": f"bolt/{thing}", "repo": b.get("Repo"), "branch": f"bolt/{thing}", "at": (t["machine"], b.get("Repo"), head)}
    n = int(key.split("/")[1])
    units = next((us for m, _, us in batches(entries) if m == n), None)
    units is not None or fail(f"{label}'s run record on this host holds no batch {n}")
    unit, _, name = thing.partition("/")
    name or fail(f"a batch's line is named <unit>/<name>, as its card names it, not {thing}")
    preview_target(key, unit, {u: None for u, _, _ in units})
    between = next(m for u, m, _ in units if u == unit)
    host = batch_unit_at(fleet, label, between, unit)["machine"]
    lines = (acts.made(label, host, [unit]).get("made") or {}).get(unit) or []
    carried = {f"{unit}/{m['name']}": (m["branch"], m["revision"]) for _, ls in lines for m in map(cards.made_line, ls)
               if not m.get("unread") and "address" not in m and "branch" in m and "revision" in m}
    branch, revision = preview_target(key, thing, carried)
    repo = unit_repo(acts.runner(label)[0], between) or fail(
        f"no launch of bolt {between}'s work is in requests.rec, so {unit}'s repository can't be told")
    return {"work": f"unit/{unit}", "repo": repo, "branch": branch, "at": (host, repo, revision)}


# -------------------------------------------------------------------------------------- what a stage made, kept

# What a unit's stages recorded as made (rail-cards "A batch's card carries what each unit's stages recorded as made"),
# as a conductor's wait kept it on the team's host, so the lines outlive the place's tidy: ~/.local/state/crew/made/
# <label>/<unit>/<stage>.jsonl, a line a thing, gone when the unit's bolt lands or is dropped. crew keeps no new lines,
# since it waits on no stage; what a Flume place made reaches crew once the runner reports it (record 0043).
MADE = pathlib.Path.home() / ".local/state/crew/made"
UNIT_STAGES = ("construct", "code", "verify", "settle", "merge")


def made_lines(text):
    """The lines of a made.jsonl as the run wrote them, in order, each without its newline, a blank one holding nothing
    left out."""
    return [l for l in (text or "").split("\n") if l.strip()]


def made_file(path):
    """A made.jsonl's lines (made_lines), [] when there is none; refused naming the file when it can't be read."""
    try:
        return made_lines(pathlib.Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (OSError, UnicodeDecodeError) as e:
        fail(f"{path} can't be read: {getattr(e, 'strerror', None) or e}")


def made_kept(label, unit):
    """The lines kept for a unit on this host, by stage, [(stage, [line])], in the order its stages run; refused
    naming a copy that can't be read."""
    d = MADE / label / unit
    stages = sorted((p.stem for p in d.glob("*.jsonl")) if d.is_dir() else [],
                    key=lambda s: (UNIT_STAGES.index(s) if s in UNIT_STAGES else len(UNIT_STAGES), s))
    return [(s, made_file(d / f"{s}.jsonl")) for s in stages]


def made_drop(label, units):
    """The copies of the units removed from this host, once their bolt has landed or been dropped: what it said."""
    import shutil
    gone = [u for u in units if crew.NAME.match(u) and (MADE / label / u).is_dir()]
    for u in gone:
        shutil.rmtree(MADE / label / u, ignore_errors=True)
    return f"removed what {joined(gone)} recorded as made, kept for {'its' if len(gone) == 1 else 'their'} batch's card" if gone else None


def made_cmd(fleet, a):
    """crew _made <label> <unit>... --json, on the units' team's host: what each unit's stages recorded as made, kept
    here (made_kept), {"made": {unit: [[stage, [line]]]}}; what a copy crew can't read is said on standard error, its
    unit carrying none. A preview of a made thing is read from the runner's report on the main machine (batch_made),
    nothing of it here."""
    made = {}
    for u in a.unit:
        crew.NAME.match(u) or fail(f"a unit's name is lowercase words with dashes, not {u}")
        try:
            made[u] = [[s, ls] for s, ls in made_kept(a.label, u) if ls]
        except Refusal as e:
            print(f"{u}: {e}", file=sys.stderr)
    print(json.dumps({"made": made}))


def made_listed(out):
    """crew _made's answer as another host printed it (made_cmd), its shape checked (read.2): {"made": {unit: [[stage,
    [line]]]}}, an older crew's "previews" beside it read as nothing; refused when it is not that."""
    try:
        got = json.loads(out)
    except ValueError:
        got = None
    ok = (isinstance(got, dict) and isinstance(got.get("made"), dict)
          and all(isinstance(v, list) and all(isinstance(s, list) and len(s) == 2 and isinstance(s[0], str) and isinstance(s[1], list)
                                              and all(isinstance(l, str) for l in s[1]) for s in v) for v in got["made"].values()))
    return {"made": got["made"]} if ok else fail(f"crew _made printed nothing crew reads: {cut((out or '').strip(), 200)}")


def batch_hand(fleet, label, n, note):
    """The raise of batch n's card handed to the drive's main machine, where the planner's cards are (code.3), as
    crew _batch-card <label> <n> --note <words>, or in this process when this is that machine: changed in place while
    it waits on the user, and left as it is once they answered it (raise_batch); what it said passed on, and its failure
    said, refusing nothing of the event that handed it."""
    machine = crew.drive_of(fleet, label)["machine"]
    if machine == crew.this_host():
        try:
            raise_batch(fleet, {"label": label, "key": f"batch/{n}"}, note=note)
        except Refusal as e:
            print(f"batch {n}'s card is not raised: {e}", file=sys.stderr)
        return
    r = crew.on_machine(fleet, machine, crew.crew_argv(fleet, machine, "_batch-card", label, str(n), "--note", note))
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    if r.returncode:
        said = ((r.stderr or r.stdout).strip().splitlines() or [f"exit {r.returncode}"])[-1]
        print(f"batch {n}'s card is not raised on {machine}: {said}", file=sys.stderr)


def batch_card_cmd(fleet, a):
    """crew _batch-card <label> <n> [--note <words>]: raise_batch on the drive's main machine, handed there by an
    event that changed what the card carries (batch_hand)."""
    raise_batch(fleet, {"label": a.label, "key": f"batch/{a.n}"}, note=a.note)


# ------------------------------------------------------------------------------- crew's own cards: the act

class CardActs:
    """What the act reaches beyond its facts: Pending You through the fleet's bridge, this host's run record, a tell,
    a picture's upload, a card's reading session started and ended, this host and who runs the command. A logic test
    hands the act a stand-in (code.7)."""

    def __init__(self, fleet):
        self.fleet = fleet

    def bridge(self, name, later, held=None):
        return cards.Bridge(name, later, held)

    def emit(self, label, act, on, **fields):
        return record.emit(label, act, on, **fields)

    def entries(self, label):
        return cards.host_entries(record, label, crew.this_host())

    def tell(self, name, text):
        return crew.tell(self.fleet, name, text)

    def put(self, url, data, kind):
        return cards.put(url, data, kind)

    def session(self, label, key, facts):
        """The link of the key's reading session, started or given again (reading_open)."""
        return self.reading(label, key, facts)[0]

    def reading(self, label, key, facts):
        """The key's reading session as reading_open gives it: its link, whether the user decided in it before it
        ended, and whether it was started anew."""
        return reading_open(self.fleet, label, key, facts)

    def end(self, label, key):
        """The key's session ended, in words; None when crew recorded none for it on this host."""
        return end_session(label, key)[0] if (CARDS / label / key / "session.json").exists() else None

    def forward(self, host, args):
        """A crew command run on host as the one asking here (code.3), its output passed on and its failure this
        command's."""
        r = crew.on_machine(self.fleet, host, crew.crew_argv(self.fleet, host, *args))
        sys.stdout.write(r.stdout)
        sys.stderr.write(r.stderr)
        if r.returncode:
            sys.exit(r.returncode)

    def runner(self, label):
        """The drive's requests and its runners as this command read them (runner_facts)."""
        return runner_facts(self.fleet, label)

    def made(self, label, host, units):
        """What the units recorded as made, kept on host, {"made": {unit: [[stage, [line]]]}} (made_cmd): read here when
        this is the host, else by crew _made there as the one asking (code.3); refused naming what could not be read."""
        if host == crew.this_host():
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                made_cmd(self.fleet, argparse.Namespace(label=label, unit=list(units), json=True))
            return json.loads(out.getvalue())
        r = crew.on_machine(self.fleet, host, crew.crew_argv(self.fleet, host, "_made", label, *units, "--json"))
        sys.stderr.write(r.stderr)
        r.returncode == 0 or fail(((r.stderr or r.stdout).strip().splitlines() or [f"exit {r.returncode}"])[-1])
        return made_listed(r.stdout)

    def host(self):
        return crew.this_host()

    def caller(self):
        return agent()

    def heard(self, words):
        """The verdict on the words in the caller's own Claude session's transcript on this host, preferring the
        user's record of them (transcript.check, want="user"), and the session's id."""
        sid, elsewhere = session_here(record.session(), crew.this_host())
        return (transcript.unverified(elsewhere) if elsewhere else transcript.check(sid, words, want="user")), sid

    def kits(self, label):
        """The names of the kits the drive's teams build, which tell a kit's landings card's key from a bolt's
        (cards.row_object)."""
        return kits_read(self.fleet, label)

    def drive(self, label):
        """The drive's run record from BATCH_DAYS back, read from its branch (drive_entries), refused naming
        the branch when it cannot be read (read.1)."""
        return drive_entries(self.fleet, label)

    def read_landings(self, label, kit):
        """The landings of the kit's started bolts read from the runner's report at a raise (kit_landings_read)."""
        kit_landings_read(self.fleet, label, kit)

    def post_lands(self, label, kit, owner, rows, sent, reads, work):
        """The lands the user's send makes due, posted by one plan write (lands_post): [(work, request, head)]."""
        return lands_post(self.fleet, label, kit, owner, rows, sent, reads, work)

    def forecast(self, label, kit, bolts, held=()):
        """The forecasts of a kit's landings card's rows (forecast_rows)."""
        return forecast_rows(self.fleet, label, kit, bolts, held)

    def keep_main(self, label, kit, sha):
        """The revision of main a kit's landings card's rows were forecast against kept on this host, the main level's,
        beside the card's state (landings_main), crew's own note of what it read and no entry of the run record
        (state.1); what can't be written is said, and the raise goes on."""
        f = landings_main(label, kit)
        try:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(sha + "\n")
        except OSError as e:
            print(f"card land/{kit}: crew could not keep the revision of main its rows were forecast against: {e.strerror or e}; "
                  "the next rail read raises the card again", file=sys.stderr)

    def kept_main(self, label, kit):
        """The revision of main keep_main kept for a kit's landings card, or None when none is kept or it can't be read,
        which costs one more raise."""
        try:
            return landings_main(label, kit).read_text().strip() or None
        except OSError:
            return None

    @contextlib.contextmanager
    def raising(self, label, kit):
        """A kit's landings card held for one raise at a time on this host, the main level's, under a lock beside the
        kits' card folders (landings_lock), and the plan fetched afresh under it, as a landing's read is (landing_read):
        two bolts landing at once each raise the card as they close, and the second reads the first's close of it
        rather than closing it again."""
        f = landings_lock(label, kit)
        f.parent.mkdir(parents=True, exist_ok=True)
        with open(f, "w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            tip_of(*state_of(self.fleet, label), fresh=True)  # what a raise before this one wrote, which it waited on
            yield

    def work(self, label, kit, moves):
        """Each moved bolt's own work between the head the user sent and its head now (bolt_work)."""
        return bolt_work(self.fleet, label, kit, moves)

    def land_row(self, label, bolt, host):
        """A bolt's row on its kit's landings card, read on its team's host (land_row): (row, None), in this process
        when that is this host, else by crew _land-row there as the one asking (code.3), what it said passed on; (None,
        why) when that host did not answer, the read refused, or it printed no row crew reads (read.2, read.3)."""
        if host == self.host():
            try:
                with contextlib.redirect_stdout(sys.stderr):
                    return land_row(self.fleet, label, bolt, self), None
            except Refusal as e:
                return None, str(e)
        r = crew.on_machine(self.fleet, host, crew.crew_argv(self.fleet, host, "_land-row", label, bolt, "--json"))
        if r.stderr.strip():
            print(r.stderr.rstrip(), file=sys.stderr)
        if r.returncode:
            return None, ((r.stderr or r.stdout).strip().splitlines() or [f"exit {r.returncode}"])[-1]
        try:
            row = json.loads(r.stdout.strip().splitlines()[-1])
        except (ValueError, IndexError):
            row = None
        ok = isinstance(row, dict) and row.get("bolt") == bolt and (isinstance(row.get("why"), str) or row.get("box") is True)
        return (row, None) if ok else (None, f"crew _land-row printed no row crew reads: {cut(r.stdout.strip(), 200)}")


class Heard(CardActs):
    """A card's acts with the adopting line told to the planner kept rather than told, when the planner runs as its
    kind: a reviewer's delivery asks it instead (review_delivered)."""

    def __init__(self, fleet, planner):
        super().__init__(fleet)
        self.planner, self.heard = planner, None

    def tell(self, name, text):
        if name != self.planner:
            return super().tell(name, text)
        self.heard = text
        return True


CARD_LATER = "The event stands, and its card is not posted."
# A card the user answered before its thing changed, as its close is recorded: its note, the user's to read, is on the
# card, and the run record holds crew's words alone (record.3).
REVISED = "answered, then changed: a new card follows it"
# A card whose kind changed while it waited, as its withdrawal is recorded: Pending You changes no card's kind.
RENEWED = "changed in kind: a new card follows it"
# A card built again with questions while it waited, as its withdrawal is recorded: Pending You changes no card's
# questions.
REASKED = "changed with its questions: a new card follows it"
# A card Pending You had ended already, by another hand than crew's close, as its close is recorded (cards.ended).
ENDED_ELSEWHERE = "ended in Pending You already"
# A card Pending You resolved as crew's post of a card following it went in, as its close is recorded (card_posted).
FOLLOWED = "picked up in Pending You by the card that follows it"


def card_where(kit):
    """Where a kit's card is asked from and filed, as the act takes it: the kit's checkout, the card's folder, and its
    git remote as Pending You files an area by it."""
    return kit["main"], cards.remote_of(f"github.com/{kit['repo']}")


def card_area(py, label, cwd, remote, name):
    """The area a card of the kit at remote is filed in: the one Pending You matches to it, else the kit's, made under
    create-area:<owner>/<kit> in the drive's group (briefs.11)."""
    matched = py.call("match_area", {"cwd": cwd, "remote": remote, "task": name})
    area = cards.area_of(matched)
    if area:
        return area
    make = cards.create_area_args(remote, label, matched)
    made = py.call("create_area", make)
    area = made.get("areaId")
    isinstance(area, str) and cards.AREA_ID.match(area) or fail(
        f"Pending You's answer to create_area names no area: crew can't tell where the card would go. {CARD_LATER}")
    note = made.get("groupNote")
    if isinstance(note, str) and note.strip():
        print(f"area {make['name']}: {note.strip()}")
    return area


def card_heard(acts, key, card, owner):
    """How the owner hears a card crew posted in no session (briefs.16): the line that adopts it, printed, and told
    to the owner when the command that raised it is not the owner's own (roles.4)."""
    line = cards.adopt_line(card, owner)
    print(line)
    to = cards.told_to(owner, acts.caller())
    if to and acts.tell(to, f"Your card {key} is up for the user: {line}, to hear their answer."):
        print(f"told {to}: {line}")


def card_uploaded(acts, key, b, got):
    """A built card's picture put to the upload URL its post or change was given, or said where it did not land."""
    if not b.get("picture"):
        return
    title = next(x["title"] for x in b["card"].get("artifacts") or [] if x.get("upload"))
    url = cards.upload_of(got, title)
    why = acts.put(url, b["picture"], "image/png") if url else "Pending You gave no upload URL for it"
    if why:
        print(f"card {key}: its picture did not reach the card: {why}", file=sys.stderr)


def built_fields(b):
    """A built card's post or change entry's own fields: Unread, why its reading could not open (unopened), crew's own
    message (record.3), left out when it opened or the card links none; and Heads, a kit's landings card's rows as
    <bolt>@<head>, :left after one the user cleared on their last send (cards.landings_card), which its next raise reads
    (landings_step); and Form, a deploy card's boxes (cards.deploy_form), which its next raise reads (cards.form_asked)."""
    return (({"Unread": b["unread"]} if b.get("unread") else {}) | ({"Heads": " ".join(b["heads"])} if b.get("heads") else {})
            | ({"Form": b["form"]} if b.get("form") else {}))


def asked_of(b):
    """A built card's post or change entry's Head: the head a landing's or a deploy's card asks about, so a card the
    user answered is asked again only once the head moved (cards.head_anew); nothing for any other card."""
    return {"Head": b["head"]} if b.get("head") else {}


def card_posted(acts, label, owner, b, where, entries=None, since=None):
    """A built card posted, recorded, printed and heard; or said and recorded refused, refusing nothing else. It is
    posted under the row's key qualified by the drive's label, or that key with its revision once a card of the
    owner's under it closed, either filled out to Pending You's eight characters when shorter (post_key, from entries,
    this host's run record of the drive unless given), and recorded under the row's key, with why its reading could not open when it did not (built_fields) and the head it
    asks about (asked_of). A post Pending
    You answers
    with the card this host's record holds open under the key already, another command's post of it recorded while
    this one was asked, as two rail reads at once ask (record 0031 §1: two readers of one event make one card), is
    that card, printed with the line that adopts it and recorded once, by the command that recorded it first. A post
    that follows a card of the owner's those entries still hold open reads that card once it is made, and records it
    closed when Pending You has ended it, as it picks up an answered card a new card follows (followed_closed); one
    given back as recorded already reads nothing, the command that recorded it having read it.

    A post that comes after a card the user answered, the card it follows closed or declined, or the card whose answer
    stands under the row's key (cards.answered_before, record 0031 as amended 2026-10-24), opens its summary and its
    details with what they answered, when, and what changed since, since being the event's sentences, and follows that
    card (cards.answered_opening, cards.opened); with nothing changed, since empty or not given, it is not posted: it is
    recorded as a post refused in crew's words, naming that card and saying its answer stands (cards.stands_said), with
    the card and the state stands, said, and None returned, refusing nothing of the event (roles.3). A card posted again
    once an older copy was lost (built_copy) is no follow-on but the row's card, and is posted whatever since says, as
    built when it gives nothing (rail-cards "A row's card lost to its owner is posted again")."""
    key, obj = b["key"], cards.row_object(b["key"], acts.kits(label)) or f"agent/{owner}"
    cwd, remote = where
    known = acts.entries(label) if entries is None else entries
    earlier = cards.answered_before(known, b["card"].get("follows"), key, owner)
    if earlier:
        opening = cards.answered_opening(earlier, since)
        if not opening and not b.get("again"):
            words = cards.stands_said(earlier)
            acts.emit(label, "card.post", [obj], by=owner, refused=words, Card=earlier["card"], Key=key, State=cards.STANDS)
            print(f"card {key}: {words}", file=sys.stderr)
            return None
        b = dict(b, card=cards.opened(b["card"], opening, earlier["card"])) if opening else b
    asked = cards.post_key(known, key, owner, label)
    follows = b["card"].get("follows")
    held = cards.followed_open(known, follows, owner) if follows else None
    try:
        with acts.bridge(owner, CARD_LATER) as py:
            area = card_area(py, label, cwd, remote, owner)
            got = py.call("post_request", cards.post_args(b["card"], asked, owner, acts.host(), cwd, area))
            card = cards.request_id(got, "post_request")
            card_uploaded(acts, key, b, got)
            again = cards.card_under(acts.entries(label), key, owner) == card
            read = followed_read(py, follows, owner) if held and not again else None
    except Refusal as e:
        acts.emit(label, "card.post", [obj], by=owner, refused=str(e), Key=key, **built_fields(b))
        print(f"card {key} not posted: {e}", file=sys.stderr)
        return None
    url = got.get("url")
    url = f" {url}" if isinstance(url, str) else ""
    if again:
        print(f"card {key}: {card}{url}, its post recorded already")
        print(cards.adopt_line(card, owner))
        return card
    acts.emit(label, "card.post", [obj], by=owner, Card=card, Key=key, **built_fields(b), **asked_of(b))
    print(f"card {key}: {card}{url}")
    card_heard(acts, key, card, owner)
    if held:
        followed_closed(acts, label, owner, held, follows, card, *read)
    return card


def followed_read(py, card, owner):
    """The card a post followed, read in the post's session once the post is made: (get_request's answer, None), or
    (None, why) when it could not be read, the session's failure caught here so the post stands."""
    try:
        got, words = py.answer("get_request", {"requestId": card, "name": owner})
    except Refusal as e:
        return None, str(e).removesuffix(f" {CARD_LATER}")
    return (None, f"Pending You refused get_request: {words}") if words is not None else (got, None)


def followed_closed(acts, label, owner, key, card, by, got, why):
    """The card a post followed, held open under key, once read: recorded closed when Pending You has ended it, picked
    up by the card by that follows it when it reports it resolved, with what the user answered on it when its reply
    still carries that (cards.answer_said); left as the run record holds it while it waits or is answered, for the
    event that ends it to close, and when the read failed, which is said."""
    if why:
        print(f"card {key}: whether {card} was picked up can't be read: {why}", file=sys.stderr)
        return
    state = cards.ended(got)
    if not state:
        return
    picked, answer = got.get("status") == "resolved", cards.answer_said(got)
    acts.emit(label, "card.close", [cards.row_object(key, acts.kits(label)) or f"agent/{owner}"], by=owner, Card=card, Key=key, State=state,
              Outcome=FOLLOWED if picked else ENDED_ELSEWHERE, **({"Answer": answer} if answer else {}))
    print(f"card {key}: {card} picked up in Pending You by {by}, which follows it" if picked else
          f"card {key}: {card} was {state} in Pending You already")


# The fact a builder takes a card's reading session's link as, by the kind of card that links one (briefs.9).
READING = {"batch": "link", "proposal": "session", "land": "link"}


def reading_of(b):
    """Whether a built card links a reading session, and of which kind: a batch's and a landing's always, a
    proposal's when its builder says it needs one, for more than fifteen new units; None for any other."""
    kind = b["key"].split("/")[0]
    if b.get("linked"):  # a kit's landings card, each of whose rows' readings its raise opened (landings_card)
        return None
    return kind if kind in ("batch", "land") or (kind == "proposal" and b.get("session")) else None


def unopened(b, why):
    """A built card whose reading session could not open, raised all the same (briefs.9): its summary saying so after
    its first paragraph, cut again to Pending You's budget, saying that crew tries it again when the rail is read
    (sweep_cards) and naming crew card session <key> as how its owner starts it, the card then carrying its link
    (briefs.13: the owner's act, nothing for the user to run), a landing's main-level ops, a batch's and a long
    proposal's the planner; its details opening with why, where the link would be; and why kept on the built card
    (unread), for its post's or change's entry in the run record."""
    key = b["key"]
    owner = "main-level ops" if key.startswith("land/") else "the planner"
    said = (f"Its reading could not be opened on the tailnet: crew tries it again when the rail is read, and {owner} "
            f"starts it with crew card session {key}; this card then carries its link.")
    first, _, rest = b["card"]["summary"].partition("\n\n")
    summary = cards.prose("\n\n".join(x for x in (first, said, rest) if x))
    context = dict(b["card"]["context"], background=f"The reading could not be opened on the tailnet: {why}\n\n"
                   + b["card"]["context"]["background"])
    return dict(b, card=dict(b["card"], summary=summary, context=context), unread=why)


def card_built(acts, label, build, facts):
    """A card of crew's own built from its facts, with its reading session's link among them when it links one: the
    session started, or given again while it serves, before the card is built (reading_of); a batch's or a long
    proposal's tried once more when it refuses, its refusal said, the files it reads written afresh at the second
    start (card-sessions "A batch's or a long proposal's raise tries its reading twice"); facts that carry the link
    already, or why it could not be opened (unread), as a landing's raise opens it, twice if it must (landing_opened),
    used as they are, nothing started; a session that could not open said, naming crew card session <key>, and the card
    built without it, saying so, with the last try's reason (unopened)."""
    b = build(facts)
    kind = reading_of(b)
    if not kind or facts.get(READING[kind]):
        return b
    key, why = b["key"], facts.get("unread")
    for again in range(0 if why else 1 if kind == "land" else 2):
        if again:
            print(f"card {key}: its reading could not be opened on the tailnet: {why}; crew tries once more", file=sys.stderr)
        try:
            with READ.fresh() if again else contextlib.nullcontext():
                url = acts.session(label, key, facts)
        except Refusal as e:
            why = str(e)
        else:
            return build(dict(facts, **{READING[kind]: url}))
    print(f"card {key}: its reading could not be opened on the tailnet: {why}; crew card session {key} starts it", file=sys.stderr)
    return unopened(b, why)


def row_card_post(fleet, label, owner, build, facts, where, acts=None, since=None):
    """The act that posts a card of crew's own (briefs.16, record 0031 §1): build(facts), one of cards.py's six
    builders, posted through the fleet's `pendingyou mcp` under the host's sign-in, asked in the name of owner, the
    role whose row it is, under the row's key, from where, the kit's (checkout, remote) as card_where gives it, and
    filed in the kit's area, its picture uploaded; recorded on the row's object with the card's id and key, and
    printed with the line that adopts it, told to the owner when the command is not the owner's. A batch's card, a
    landing's and a long proposal's have their reading session started first, its link handed to the builder
    (card_built). Pending
    You's refusal, a host not signed in, no answer within a minute or a reply naming no card is said and recorded as
    the post refused, and refuses nothing of the event it was raised for. A card that follows one the user answered
    says first what they answered and what changed since, since, or is not posted when nothing did (card_posted). The
    card's id, or None."""
    acts = acts or CardActs(fleet)
    return card_posted(acts, label, owner, card_built(acts, label, build, facts), where, since=since)


def answer_due(entries, card):
    """Whether the user's answer on a card is still to be recorded (rail-cards "crew records the user's answer the first
    time it reads it"): true unless a card.answer of card, not refused, is among the entries, since Pending You changes
    no answered card and one answer per card is final (record.1). A decision of facts alone (code.7)."""
    return not any(e.get("Act") == "card.answer" and e.get("Card") == card and not e.get("Refused") for e in entries)


def answer_fields(key, got, heads=None, offered=()):
    """A card.answer's fields but its Card, from get_request's reply on the agent's turn (got): its Key and its Answer
    in crew's words made from names alone (cards.answer_said, offered the boxes the card offered), and for a kit's
    landings card, land/<kit>, its rows as its last post or change recorded them given (heads, card_heads), Heads: the
    bolts the user ticked (ticked_of), each at the head the card showed, left out when they ticked none. None when the
    reply holds no answer, or the card waits on the user. A decision of facts alone (code.7)."""
    if not isinstance(got, dict) or got.get("status") != "answered":
        return None
    answer = cards.answer_said(got, offered)
    if answer is None:
        return None
    fields = {"Key": key, "Answer": answer}
    if heads is not None and (key or "").startswith("land/"):
        ticked = ticked_of(got, heads) or []
        if ticked:
            fields["Heads"] = " ".join(f"{b}@{h}" for b, h, _ in heads if b in ticked)
    return fields


def answer_seen(acts, label, owner, key, card, got, entries, heads=None, offered=()):
    """The user's answer on a card crew read answered (got, get_request's reply in the owner's name) recorded, the first
    time an act of crew's reads it (rail-cards "crew records the user's answer the first time it reads it", design
    Decision 1): one card.answer on the row's object, or agent/<owner> for a question, in the owner's name, with its
    Card and answer_fields', heads and offered as they take them, unless the run record (entries) holds the card's
    answer already (answer_due). Said on standard error. The fields recorded, or None when nothing was."""
    if not answer_due(entries, card):
        return None
    fields = answer_fields(key, got, heads, offered)
    if fields is None:
        return None
    acts.emit(label, "card.answer", [cards.row_object(key, acts.kits(label)) or f"agent/{owner}"], by=owner, Card=card, **fields)
    print(f"card {key}: {card} was answered, {fields['Answer']}, and crew recorded it", file=sys.stderr)
    return dict(fields, Card=card)


def card_lost(acts, label, owner, key, card, words):
    """A card Pending You no longer finds for its owner, or holds in another assistant's name (cards.lost), recorded
    closed as lost so it is held no longer, its words naming who holds it when they do."""
    acts.emit(label, "card.close", [cards.row_object(key, acts.kits(label)) or f"agent/{owner}"], by=owner, Card=card, Key=key, State="lost",
              Outcome=f"lost to its owner: {words}")
    print(f"card {key}: {card} is lost to {owner} (Pending You: \"{words}\")", file=sys.stderr)


def row_card_change(fleet, label, owner, build, facts, note, where, acts=None, kind_changed=False, anew=None, since=None):
    """The act that changes a card of crew's own when its thing changes (record 0031 §3): build(facts) sent as
    update_request takes it, with note as the change note the user sees, at the version Pending You reports, to the
    card the owner holds under the row's key on this host, while it waits on the user. Once they have answered it,
    which Pending You changes no longer, it is final for what it asked (cards.revision): left as it is, the act their
    answer calls for going on, unless what it asks changed since (anew, None while it has not; else the facts that say
    so, {} for none, a landing's head moved since their approval among them, cards.head_anew), or its kind; then acked
    with note as its outcome and closed, its close keeping what they answered (cards.answer_said), and build(facts and
    anew) posted as a new card that follows it, under the key with its revision (post_key), against the run record with
    that close in it, its state, time and answer. A card whose kind changed (kind_changed), or one built again that carries questions,
    a proposal's whose rows fill more than one list, neither of which update_request ever changes, is followed the same
    way, withdrawn with note while it waits. Posted instead when the owner holds none, and posted again, its summary
    saying the older copy is dead, when Pending You no longer finds it. A landing's card and a long proposal's are
    built with their reading session's link, as a post's is (card_built), a landing's session on a moved head started
    anew there, so the card changed carries the new link, and its entry why it could not open when it did not
    (built_fields), and a landing's or a deploy's the head it asks about (asked_of). A new card posted after one the user
    answered opens with what they answered and what changed since, since, the event's sentences, or note when the
    event gives none, and is not posted when since is given empty (card_posted); a card posted again, the older copy
    lost or one this host can't reach handed over as dead (built_copy), is the row's card and never withheld, opening
    with note when the event gives nothing changed. A refusal is said and recorded as the change refused, refusing
    nothing of the event. The card's id, the new card's when one was posted, or None."""
    acts = acts or CardActs(fleet)
    b = card_built(acts, label, build, facts)
    key, obj = b["key"], cards.row_object(b["key"], acts.kits(label)) or f"agent/{owner}"
    entries = acts.entries(label)
    card = cards.card_under(entries, key, owner)
    if not card:
        return card_posted(acts, label, owner, b, where, entries, (since or [note]) if b.get("again") else since)
    lost, how, state = None, "change", None
    why = "its kind having changed" if kind_changed else "its questions having to be asked anew"
    try:
        with acts.bridge(owner, CARD_LATER) as py:
            got, lost = py.answer("get_request", {"requestId": card, "name": owner})
            if lost is None:
                state = cards.ended(got)
                how = cards.revision(got, kind_changed, "questions" in b["card"], anew is not None)
            if lost is None and how == "follow":
                tool, args, state = cards.close_call(got, card, owner, outcome=cut(note, cards.NOTE))
                _, lost = py.answer(tool, args)
            elif lost is None and how == "change":
                change = dict(cards.change_args(b["card"], note), requestId=card, name=owner,
                              expectedVersion=cards.version_of(got, card))
                got, lost = py.answer("update_request", change)
            if lost is not None and not cards.lost(lost, owner):
                what = {"closed": "close of the card the user answered", "withdrawn": f"withdrawal of the card, {why}"}
                fail(f"Pending You refused the {what.get(state, 'change')}: {lost}")
            if lost is None and how == "change":
                card_uploaded(acts, key, b, got)
    except Refusal as e:
        acts.emit(label, "card.update", [obj], by=owner, refused=str(e), Card=card, Key=key, **built_fields(b))
        print(f"card {key} not changed: {e}", file=sys.stderr)
        return None
    if how == "leave":
        print(f"card {key}: {card} is left as it is: the user has answered it")
        return card
    answer = cards.answer_said(got) if lost is None else None
    answered = {"Answer": answer} if answer else {}
    at = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    closed = entries + [dict(Act="card.close", Card=card, Key=key, By=owner, State="lost" if lost is not None else state, At=at, **answered)]
    if lost is not None:
        card_lost(acts, label, owner, key, card, lost)
        return card_posted(acts, label, owner, built_copy(b), where, closed, since or [note])
    if state == "closed" and anew:  # what it asks changed since the user answered it, which the new card says
        b = card_built(acts, label, build, dict(facts, **anew))
    if how == "ended":
        acts.emit(label, "card.close", [obj], by=owner, Card=card, Key=key, State=state, Outcome=ENDED_ELSEWHERE, **answered)
        print(f"card {key}: {card} was {state} in Pending You already, and its new version follows it")
        follows = {"follows": card} if state == "closed" else {}
        return card_posted(acts, label, owner, dict(b, card=dict(b["card"], **follows)), where, closed, [note] if since is None else since)
    if how == "follow":
        acts.emit(label, "card.close", [obj], by=owner, Card=card, Key=key, State=state,
                  Outcome=REVISED if state == "closed" else RENEWED if kind_changed else REASKED, **answered)
        print(f"card {key}: {card} " + ("closed, the user having answered it" if state == "closed" else f"withdrawn, {why}")
              + ", and its new version follows it")
        return card_posted(acts, label, owner, dict(b, card=dict(b["card"], follows=card)), where, closed, [note] if since is None else since)
    acts.emit(label, "card.update", [obj], by=owner, Card=card, Key=key, **built_fields(b), **asked_of(b))
    v = got.get("version")
    print(f"card {key}: {card} changed" + (f", now version {v}" if isinstance(v, int) else ""))
    return card


def row_card_close(fleet, label, owner, key, outcome=None, reason=None, acts=None, said=None, here=False, offered=(), **more):
    """The act that closes a card of crew's own at the event that ends it (record 0031 §1): the card the owner holds
    under the row's key on this host, acked with the outcome once the user answered it, else withdrawn with the
    reason, or the outcome; recorded with how it closed. A card Pending You no longer finds is recorded lost, and a
    refusal said and recorded as the close refused, neither refusing the event. The key's reading session on this
    host ends with the card, closed, lost or held by nobody, and stays while a refused close leaves the card open
    (card-sessions). A land/ key ends nothing: a kit's landings card has no reading or preview of its own, and a closed
    card of a bolt's own, land/<bolt> or land/<bolt>/<head> as a conductor posted one before, is no word on the bolt's
    row, whose reading and preview end with the row (land_end). said, when given, is what Pending You is sent in place
    of the outcome, words the run record does not keep (record.3); here, that the user answered it in a conversation,
    so a card still waiting closes as answered there (cards.close_call). A card the user answered is closed with what
    they answered, as Answer (card_closed); offered, the ids of the boxes the card offered, a kit's landings card's
    rows as land:<bolt>, so the answer names those they left. more, fields the close's entry carries beside crew's own,
    a kit's landings card's Rows (landings_step). The card's id, or None when none was closed."""
    acts = acts or CardActs(fleet)
    card = card_closed(acts, label, owner, key, outcome, reason, said, here, more, offered)
    if card is not False and key.split("/")[0] in READING and not key.startswith("land/"):
        said = acts.end(label, key)
        if said:
            print(said)
    if card is not False and re.fullmatch(r"batch/\d+", key):  # what was asked from it goes with it (record 0043)
        batch_previews_put_away(fleet, label, owner, key, acts)
    return card or None


def batch_previews_put_away(fleet, label, owner, key, acts):
    """At a batch card's close, the done of each standing ask of a preview of its units' lines that no other open batch
    card holds, in one plan write (Decision 7 of a-cards-preview-is-asked-of-the-runner; rail-cards "A preview is
    put away when its batch's card closes or its card or row is gone"); what it put away said, and a runner or a write crew
    can't read or make said, the rail's read putting it away later (sweep_previews). Nothing is run on a unit's host."""
    entries = acts.entries(label)
    of = lambda k: int(k.split("/")[1].split("-")[0])
    units = {u for m, _, us in batches(entries) if m == of(key) for u, _, _ in us}
    others = {e.get("Key") for e in entries if e.get("Act") == "card.post" and e.get("Key") != key
              and re.fullmatch(r"batch/\d+(-\d+)?", e.get("Key") or "") and cards.card_under(entries, e.get("Key"), owner)}
    held = {f"unit/{u}" for m, _, us in batches(entries) if m in {of(k) for k in others} for u, _, _ in us}
    try:
        requests, reads = acts.runner(label)
        asks = {k: r for k, r in runner.previews_standing(requests, reads).items() if r.get("Work") in {f"unit/{u}" for u in units}}
        gone = runner.previews_put_away(asks, set(), held)
        if gone:
            preview_written(fleet, label, key, joined(sorted({r.get("Work")[len("unit/"):] for r in gone})), gone, done=True, made=[],
                            by=owner)
            print(f"card {key}: put away " + "; ".join(f"{r.get('Work')[len('unit/'):]}'s preview of {r.get('Revision')[:7]} on "
                                                       f"{r.get('Host')}" for r in gone))
    except Refusal as e:
        print(f"card {key}: its units' previews are not put away yet, the rail's read putting them away: {e}", file=sys.stderr)


def card_closed(acts, label, owner, key, outcome, reason, said=None, here=False, more=None, offered=()):
    """row_card_close's close in Pending You: the card's id once closed, None when none was held or it was lost, and
    False when the close was refused, so the card stays open. said is sent in place of the outcome, and the outcome
    recorded; here closes a card still waiting as answered in a conversation. The close's entry carries what the user
    answered, as Answer, in crew's words (cards.answer_said, offered the ids of the boxes the card offered), or that
    they answered it in the owner's pane when it closed as answered there; a card withdrawn while it waits, none. A
    kit's landings card the user answered keeps their send as Heads on every close, the ended-in-Pending-You one among
    them, unless more gives its own (close_kept)."""
    obj = cards.row_object(key, acts.kits(label)) or f"agent/{owner}"
    entries = acts.entries(label)
    card = cards.card_under(entries, key, owner)
    if not card:
        print(f"card {key}: {owner} holds none open on this host, so none is closed")
        return None
    lost = None
    try:
        with acts.bridge(owner, "The event stands, and its card stays open.") as py:
            got, lost = py.answer("get_request", {"requestId": card, "name": owner})
            state = cards.ended(got) if lost is None else None
            if state:
                outcome, reason = ENDED_ELSEWHERE, None
            elif lost is None:
                tool, args, state = cards.close_call(got, card, owner, outcome if said is None else said, reason, here)
                _, lost = py.answer(tool, args)
            if lost is not None and not cards.lost(lost, owner):
                fail(f"Pending You refused the close: {lost}")
    except Refusal as e:
        acts.emit(label, "card.close", [obj], by=owner, refused=str(e), Card=card, Key=key)
        print(f"card {key} not closed: {e}", file=sys.stderr)
        return False
    if lost is not None:
        card_lost(acts, label, owner, key, card, lost)
        return None
    kept = close_kept(got, entries, card, obj.startswith("kit/"), offered, more)
    answer = kept.pop("Answer", None) or (f"answered in {owner}'s pane" if here and state == "closed" else None)
    acts.emit(label, "card.close", [obj], by=owner, Card=card, Key=key, State=state, Outcome=cards.close_words(got, outcome, reason),
              **{k: v for k, v in (more or {}).items() if k != "Heads"}, **kept, **({"Answer": answer} if answer else {}))
    print(f"card {key}: {card} {state}")
    return card


def ended_close(acts, label, owner, key, card, got, entries):
    """A card Pending You has ended by another hand (cards.ended: resolved, closed, cancelled or expired) recorded so,
    sending Pending You nothing: closed as ended there with what the user answered and, for a kit's landings card,
    their send (close_kept), or withdrawn; on the row's object, or agent/<owner> for a question, in its owner's name.
    The close's state, or None when the reply is no ended card's."""
    state = cards.ended(got)
    if state:
        obj = cards.row_object(key, acts.kits(label)) or f"agent/{owner}"
        acts.emit(label, "card.close", [obj], by=owner, Card=card, Key=key, State=state, Outcome=ENDED_ELSEWHERE,
                  **close_kept(got, entries, card, obj.startswith("kit/")))
    return state


def close_kept(got, entries, card, kit, offered=(), more=None):
    """What a card's close keeps of the user's answer, from get_request's reply (got) and the run record's entries:
    Answer, in crew's words (cards.answer_said, offered the boxes the card offered, a kit's landings card's read from
    its last post or change when none are given, offered_boxes); and for a kit's landings card (kit), Heads, the bolts
    the user ticked at the heads it showed (ticked_of, shown_heads), so the card that follows reads their send
    (landings_sent) whichever act closes it, the raise, the sweep, crew bolt land or a read that finds it ended in
    Pending You (rail-cards "A kit's landings card's close keeps the user's send", Decision 4), unless the act gives
    its own, more's Heads, landings_step's, kept as given and left out when empty. A card still waiting keeps none."""
    out, shown = {}, shown_heads(entries, card) if kit else None
    answer = cards.answer_said(got, offered or (offered_boxes(shown) if kit else ()))
    if answer:
        out["Answer"] = answer
    if kit:
        heads = (more or {}).get("Heads") if "Heads" in (more or {}) else sent_heads(got, card_heads(shown))
        if heads:
            out["Heads"] = heads
    return out


def sent_heads(got, heads):
    """The user's send on a kit's landings card, from get_request's reply on their answer, picked up or acked since or
    not (cards.ENDED's resolved and closed): the bolts they ticked at the heads the card showed (heads, card_heads),
    <bolt>@<head> each in the card's order; None for a card they did not answer, or a send ticking none."""
    answered = isinstance(got, dict) and (got.get("status") == "answered" or cards.ended(got) == "closed")
    ticked = ticked_of(dict(got, status="answered"), heads) if answered else None
    return " ".join(f"{b}@{h}" for b, h, _ in heads if b in ticked) or None if ticked else None


# ------------------------------------------------------------------------------------------------ crew record

def record_split(md):
    """A decision record's Markdown as crew reads it: its frontmatter's fields, its body and the body's paragraphs."""
    m = re.match(r"---\n(.*?)\n---\n", md, re.S)
    fields = dict(l.split(":", 1) for l in m.group(1).splitlines() if re.match(r"[a-z][\w-]*:", l)) if m else {}
    body = (md[m.end():] if m else md).strip()
    return {k: v.strip().strip("'\"") for k, v in fields.items()}, body, [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


def record_status_held(md):
    """A decision record's status as its file holds it, the one reading crew record and a proposal's check share
    (briefs.15): its frontmatter's status, and the paragraphs that mark an amendment proposed ("Status: proposed" past
    the record's own status line)."""
    fields, _, paras = record_split(md)
    own = next((i for i, p in enumerate(paras) if p.startswith("Status:")), None)
    return fields.get("status", "").lower(), [p for i, p in enumerate(paras) if i != own and "Status: proposed" in p]


def record_says(status, marked):
    """What a record's file holds, in crew's words, from its status and the amendments marked proposed."""
    return "accepted, with an amendment still marked proposed" if marked and status == "accepted" else status or "no status in its frontmatter"


def record_accepted(status, marked):
    """Whether a record's file holds it accepted: its status accepted, with no amendment still marked proposed."""
    return status == "accepted" and not marked


def record_facts(kit, number, text, status, before=None, alternatives=None):
    """A decision record's facts as its card is built from them (cards.record_card), from its Markdown at a commit, and
    whether the file holds the status the design agent records (briefs.15): its title, its frontmatter's or else its
    heading's; its opening, the first paragraph of its body that is neither a heading nor a `Name:` line, or, for an
    amendment, the paragraph its proposed mark stands in; an amendment's own first words, which title its card in
    place of the record's (cards.first_words, record 0031 as amended 2026-10-24), else None; the user's words its
    deciders line quotes; its body whole; and the alternatives a rule of the user's decided between, from the Markdown
    --alternatives hands, whose frontmatter names the rules that decided (`rules:`, separated by commas), the other
    path (`other:`) and, when the user's own words point there, `recommended: loosen`, else accepting as ruled is. A
    file holds its frontmatter's status, but proposed while an amendment to an accepted record is still marked proposed
    ("Status: proposed" past the record's own status line), and accepted or rejected alike once the mark the text
    before (before, the record at the commit before) held is gone, the amendment taken in or out. Refused naming what
    the file holds when it holds no such status, and refused when what the card is built from can't be read (read.1)."""
    n = f"{number:04d}"
    fields, body, paras = record_split(text)
    now, marked = record_status_held(text)
    then, was = record_status_held(before) if before else ("", [])
    holds = ["proposed"] if now == "accepted" and marked else ["accepted", "rejected"] if now == "accepted" and then == "accepted" and was else [now]
    says = record_says(now, marked)
    status in holds or fail(f"crew refuses record {n} in {kit} as {status}: its file on main says {says}. Commit it {status} "
                            f"and land it on main, then run crew record again.")
    head = next((p for p in paras if p.startswith("# ")), "")
    title = fields.get("title") or re.sub(r"^#\s+(\d+\.\s+)?", "", head)
    amended = bool(marked) and now == "accepted"
    if amended:
        opening = re.sub(r"\s*Status: proposed\b.*?(?:\.(?=\s|$)|$)", "", marked[0], flags=re.S).strip()
    else:
        opening = next((p for p in paras if not p.startswith("#") and not re.match(r"[A-Z][\w -]*:\s", p)), "")
    amendment = cards.first_words(opening) if amended else None
    title and opening and amendment != "" or fail(
        f"crew can't read record {n} in {kit} for its card: it has no "
        + ("title" if not title else "opening paragraph" if not opening else "words of its amendment") + ". Nothing is raised.")
    deciders = next((p for p in paras if p.startswith("Deciders:")), "")
    quoted = [a or b for a, b in re.findall(r"“([^”]+)”|\"([^\"]+)\"", deciders)]
    alt = None
    if alternatives is not None:
        afields, abody, _ = record_split(alternatives)
        rules = [r.strip() for r in afields.get("rules", "").split(",") if r.strip()]
        other, rec = afields.get("other", ""), afields.get("recommended", "accept")
        why = ("their frontmatter names no rules that decided, as rules: <rule ids, separated by commas>" if not rules else
               "their frontmatter names no other path, as other: <the path the rules ruled out>" if not other else
               f"their frontmatter recommends {rec}, where it takes loosen or accept" if rec not in ("loosen", "accept") else
               "the file holds nothing under its frontmatter for the card" if not abody else None)
        not why or fail(f"crew refuses the alternatives for record {n} in {kit}: {why}. Nothing is raised.")
        alt = {"rules": rules, "other": other, "text": abody, "recommended": rec}
    return {"kit": kit, "number": number, "title": title, "opening": opening, "amendment": amendment, "quoted": quoted, "text": body,
            "alternatives": alt}


def raise_record(fleet, label, facts, where, note, acts=None, dead=False):
    """A decision record's card raised in its design agent's name (record 0031 §1, briefs.15), record/<kit>/<number>,
    from the record's facts (record_facts), from where, the kit's checkout on this host and its remote: posted the
    first time, and while the design agent holds it open, changed in place with note, naming the new commit, or once the
    user has answered it, closed with note and followed by a new card, since a revision asks anew (row_card_change),
    which opens saying what they answered and that the record was revised, note.
    With dead, an older copy this host can't reach standing, the card is built saying first that it was lost
    (built_again). A refusal is said and recorded and refuses nothing of the status, already recorded. The card's id,
    or None."""
    build = built_again(cards.record_card) if dead else cards.record_card
    return row_card_change(fleet, label, f"{label}-design", build, facts, note, where, acts, anew={}, since=[note])


def raise_record_again(fleet, row, acts=None):
    """The rail's sweep's raise of a decision record's card its design agent's host can't reach (sweep_judged's again,
    record 0031 §1), for its row of the group records, of which it reads the label, the key record/<kit>/<number> and
    whether its card offered alternatives: the record read with status proposed as crew record reads it on the kit's
    main (record_read), and its card posted in the design agent's name saying first that an older copy was lost
    (raise_record). A card that offered alternatives is refused, since crew keeps no copy of the file they were read
    from (read.1), naming the crew record command that raises it again; a record whose file no longer holds proposed,
    or that crew can't read, is refused in record_read's words. The card's id, or None."""
    m = re.fullmatch(r"record/([a-z0-9][a-z0-9-]*)/(\d{4})", row.get("key") or "")
    if not m:
        return None
    label, kit_, n = row["label"], m.group(1), int(m.group(2))
    not row.get("alternatives") or fail(
        f"crew keeps no copy of record {n:04d}'s alternatives, so {label}-design raises it again with "
        f"crew record {kit_} {n} --proposed --alternatives <file>")
    facts, where, sha, subject = record_read(fleet, label, kit_, n, "proposed")
    return raise_record(fleet, label, facts, where, f"Raised again at {sha[:7]}: {subject}", acts, dead=True)


def record_card_close(fleet, label, owner, obj, outcome, acts=None):
    """A decision record's cards closed at its accepted or rejected status with outcome: each the owner holds open on
    this host under the record's key, obj, in either form, record 0031's or the one with the commit after it
    (cards.record_keys), closed as row_card_close closes a row's, and said when it holds none. The ids closed."""
    acts = acts or CardActs(fleet)
    keys = cards.record_keys(acts.entries(label), obj, owner, acts.kits(label)) or [obj]
    return [c for c in (row_card_close(fleet, label, owner, k, outcome=outcome, acts=acts) for k in keys) if c]


def record_kit(fleet, label, name):
    """The kit a design agent's record is in, by name, as the drive's main-level host keeps it (main_kit; the user's
    ruling of 2026-11-01), where its design agent runs and its records are read, a kit's first records coming before
    its first bolt; refused where that host keeps none."""
    t = main_kit(fleet, label, name) or fail(main_kit_said(fleet, label, name, "read its records"))
    return t["kit"]


def record_read(fleet, label, kit_, number, status, alternatives=None):
    """A decision record as crew record reads it (briefs.15): the kit's docs/adr/<number>-*.md on its main now, GitHub's
    after a fetch for a kit with an origin (kit.main_now, plan.18), read in this host's checkout of the kit, at the
    last commit that changed it, and its facts with the status and alternatives text given (record_facts). (facts,
    where, the commit, its subject), where as card_where gives it for the checkout; refused when the checkout, main,
    the one file or the status it holds can't be read (read.1)."""
    here, k, n = crew.this_host(), record_kit(fleet, label, kit_), f"{number:04d}"
    checkout = k["main"]

    def git(*args):
        r = subprocess.run(["git", "-C", checkout, *args], capture_output=True, text=True)
        r.returncode == 0 or fail(f"git {args[0]} in {checkout} failed: {(r.stderr or r.stdout).strip() or f'exit {r.returncode}'}")
        return r.stdout
    # The record as the kit's main holds it now, GitHub's after a fetch for a kit with an origin (kit.main_now, plan.18).
    r = subprocess.run(["bash", "-c", fetch_told(fleet, here, checkout, MAIN), "crew", checkout], capture_output=True, text=True,
                       env=gitenv())
    r.returncode == 0 or fail(f"{checkout} could not be read: {(r.stderr or r.stdout).strip() or f'exit {r.returncode}'}")
    _, now, why = kit.main_now(r.stdout, kit_, here)
    not why or fail(why)
    files = [f for f in git("ls-tree", "--name-only", now, "docs/adr/").splitlines() if re.fullmatch(rf"docs/adr/{n}-[^/]*\.md", f)]
    len(files) == 1 or fail(f"{kit_}'s main holds " + (f"no record {n} in docs/adr/" if not files else
                                                         f"{len(files)} records numbered {n}: {', '.join(files)}") + ", so crew records nothing.")
    commits = [l.split("\t", 1) for l in git("log", "-2", "--format=%H\t%s", now, "--", files[0]).splitlines()]
    sha, subject = commits[0]
    facts = record_facts(kit_, number, git("show", f"{sha}:{files[0]}"), status,
                         git("show", f"{commits[1][0]}:{files[0]}") if len(commits) > 1 else None, alternatives)
    return facts, card_where(dict(k, main=checkout)), sha, subject


def record_status(fleet, a):
    """crew record <kit> <number> --proposed|--accepted|--rejected [--settled-in-pane --excerpt "<words>"]
    [--alternatives <file>] [--label L]: the design agent's record at each turn of its status (briefs.15, record 0031
    §1). The kit is one the drive's main-level host keeps (record_kit); the record is read as record_read reads
    it, in that checkout, where the drive's main level runs. A status its file does not hold there is refused,
    naming what it holds, and so is an alternatives file crew can't read, with nothing recorded. Else record.<status>
    is recorded on record/<kit>/<number> with that commit; then --proposed raises the record's card in the design
    agent's name, or changes the one it holds, naming the commit, unless --settled-in-pane says the user said yes in
    the pane, in the words --excerpt gives, which crew reads in the caller's own transcript on this host as the user's
    before it reads the kit (settled_refusal), whoever the caller is (roles.2), and records naming the transcript
    record and the words' length, never the words (record.3), raising nothing; --alternatives makes the card the
    choice a rule decided, recorded as the proposed status's Form, none of the file's words (record.3); and --accepted
    or --rejected closes the card with the commit, under either key form (record_card_close). A card the design agent
    holds where this host's sign-in can't reach it, posted from another host or lost to it (record_stranded), is
    posted again saying first that the older copy was lost."""
    label = default_label(fleet, a) or fail("crew record runs as the record's drive: run it as the design agent, or add --label")
    p = crew.drive_of(fleet, label)
    k = record_kit(fleet, label, a.kit)
    0 < a.number < 10000 or fail(f"a record's number is its one to four digits, not {a.number}")
    a.status == "proposed" or not (a.settled_in_pane or a.alternatives) or fail(
        f"--settled-in-pane and --alternatives go with --proposed: a record {a.status} closes its card")
    not (a.settled_in_pane and a.alternatives) or fail(
        "a record settled in the pane raises no card, so it takes no alternatives: give --settled-in-pane or --alternatives")
    not a.settled_in_pane or (a.excerpt or "").strip() or fail(
        "--settled-in-pane needs --excerpt \"<the user's yes, as they wrote it in your pane>\": crew reads it in your transcript")
    a.excerpt is None or a.settled_in_pane or fail(
        "--excerpt goes with --settled-in-pane: the words are the user's yes, given in your pane")
    here, n = crew.this_host(), f"{a.number:04d}"
    p["machine"] == here or fail(f"crew record runs on {p['machine']}, where {label}'s design agent holds its records' cards")
    v = sid = None
    if a.settled_in_pane:
        v, sid = CardActs(fleet).heard(a.excerpt)
        why = settled_refusal(a.number, a.kit, v)
        not why or fail(why)
    alternatives = None
    if a.alternatives:
        try:
            alternatives = pathlib.Path(a.alternatives).read_text()
        except (OSError, UnicodeDecodeError) as e:
            fail(f"crew can't read the alternatives file {a.alternatives}: {getattr(e, 'strerror', None) or e}. Nothing is raised.")
    facts, where, sha, subject = record_read(fleet, label, a.kit, a.number, a.status, alternatives)
    key, settled = f"record/{a.kit}/{n}", a.status == "proposed" and a.settled_in_pane
    frm = [f"session/{sid}/{v.uuid or f'line-{v.line_hash()[:16]}'}"] if settled else []
    record.emit(label, f"record.{a.status}", [key], frm=frm, commit=[f"{k['repo']}@{sha}"],
                State="settled in the pane" if settled else None, Chars=len(a.excerpt) if settled else None,
                Form="alternatives" if alternatives is not None else None)
    print(f"record {n} in {a.kit}: {a.status} at {sha[:7]}" + (", the user's yes given in the pane; no card is raised" if settled else ""))
    if a.status != "proposed":
        record_card_close(fleet, label, f"{label}-design", key, f"{a.status.capitalize()} at {sha[:7]}")
    elif not settled:
        raise_record(fleet, label, facts, where, f"Revised at {sha[:7]}: {subject}", dead=record_stranded(fleet, label, key))


def record_stranded(fleet, label, key):
    """Whether the design agent's newest card under a record's key is one this host's sign-in can't reach, posted from
    another host and not closed, or lost to it (cards.stranded), from the drive's run record of the last cards.DAYS
    days, read from its branch (record.gather); False, said, when the branch could not be read, so the card is posted
    as it would be."""
    since = (datetime.datetime.now(datetime.timezone.utc).date() - datetime.timedelta(days=cards.DAYS)).isoformat()
    entries, missing = record.gather(fleet, [label], since)
    if missing:
        print(f"card {key}: whether an older copy of it is held where this host's sign-in can't reach could not be looked for: "
              + "; ".join(f"{h}: {v}" for h, v in sorted(missing.items())), file=sys.stderr)
        return False
    return cards.stranded(entries, key, f"{label}-design", crew.this_host()) is not None


# ------------------------------------------------------------------------------- the rail's sweep of the cards

# The name crew's sweep gives Pending You when it asks after cards: no agent's, so it claims no agent's answers
# (briefs.17). Pending You refuses it another assistant's card as that assistant's ("This is crw-2-conductor's card;
# leave it."), so the card is there, and answers "not found" only for a card this host's sign-in no longer reaches
# (the recovery session, 2026-10-15 and 16), which is all the sweep asks.
SWEEPER = "crew"
# Each kind's raise, the function its change of the series gives it, handed a rail row (record 0031 §1): by the row
# key's first part, a name in this module or, as ops.<name>, in ops.py. A kind whose function is not there has none yet.
RAISES = {"proposal": "raise_proposal", "batch": "raise_batch", "land": "raise_landings_row", "deploy": "ops.raise_deploy",
          "op": "ops.raise_step", "record": "raise_record_again"}
SWEEP_LATER = "The rail's sweep changes nothing on this read."


class SweepActs(CardActs):
    """What the rail's sweep reaches beyond the act's own: herdr's listing of an asker, a kind's raise, a reading tried
    again and the clock. A logic test hands the sweep a stand-in (code.7)."""

    def listed(self, name):
        """Whether herdr lists an agent in the pane crew keeps for the asker, from one listing of its session (read.2,
        crew.read_pane_agent): (True or False, None), or (None, why) when that can't be read; never by the agent's
        name, which herdr drops when the pane's session changes."""
        return crew.read_pane_agent(self.fleet, name)

    def raise_of(self, kind):
        name = RAISES.get(kind)
        if name and name.startswith("ops."):
            import ops  # ops.py imports nothing of this module
            return getattr(ops, name[4:], None)
        return globals().get(name) if name else None

    def now(self):
        return datetime.datetime.now(datetime.timezone.utc)

    def main_at(self, label, kit, sv, runs):
        """The revision of main the rail's survey (sv) read a kit at in its folder where its work runs (gather.kit's
        main_at), as the runner that took the kit's newest work reported it (kit_at, from the drive's runners as
        the read holds them, runs), where its landings card's rows are forecast, as last fetched (plan.18): (sha,
        None), or (None, why) when crew can't tell where the kit's work runs, its host did not answer or its read
        names none. A kit the rail's survey did not read is surveyed alone."""
        try:
            t = kit_at(self.fleet, label, kit, (runs or {}).get(label))
        except Refusal as e:
            return None, str(e)
        host, main = t["machine"], t["kit"]["main"]
        v = sv.get(host)
        if v is None or (v["ok"] and main not in v["kits"]):
            v = survey(self.fleet, [(t, None)]).get(host) or {"ok": False, "error": "it was not read"}
        if not v["ok"]:
            return None, f"{host} did not answer ({v['error']})"
        k = v["kits"].get(main) or {}
        if not k.get("ok"):
            return None, f"{main} on {host} could not be read: {k.get('error') or 'it was not read'}"
        return (k["main_at"], None) if k.get("main_at") else (
            None, f"crew on {host} names no revision of main it read {main} at, as a crew older than the read of it does")

    def preview_note(self, label, key, note):
        """A card's change for its preview handed to its raise (preview_changed), what the raise says going to standard
        error, the rail's text saying what it did."""
        with contextlib.redirect_stdout(sys.stderr):
            return preview_changed(self.fleet, label, key, note)

    def raise_kit(self, label, kit):
        """A kit's landings card raised again as main moved under it (raise_landings, with no note of its own), what it
        says going to standard error, the rail's text saying what it did: the card's id, or None."""
        with contextlib.redirect_stdout(sys.stderr):
            return raise_landings(self.fleet, label, kit, self)

    def reading_again(self, label, key):
        """A card's reading opened again and its card changed to carry the link: a kit's landings card's, land/<kit>,
        by its raise with RELINKED as its note (raise_landings), which tries each row's reading on its team's host as
        crew card session land/<bolt> opens it, refused in the words its card then stands without one in (Unread) when
        one still will not open; a batch's or a proposal's as before (reading_again). As reading_open returns it: the
        link, None for a kit's card, whose links are its rows', whether the user decided in it, and whether it was
        started anew."""
        if not key.startswith("land/"):
            return reading_again(self.fleet, label, key, self)
        raise_landings(self.fleet, label, key.split("/", 1)[1], self, note=RELINKED)
        entries = self.entries(label)
        card = cards.card_under(entries, key, f"{label}-ops")
        if reading_unread(entries, key, card):
            fail(next((e["Unread"] for e in reversed(entries) if e.get("Card") == card and e.get("Unread") and not e.get("Refused")
                       and e.get("Act") in ("card.post", "card.update")), "a row's reading still stands unopened"))
        return None, False, True


def question_close(acts, label, c, words):
    """A question withdrawn by crew once its asker has ended (briefs.11): read in the asker's name, which no session
    holds now, and withdrawn with words, or acked with them when the user answered it to nobody; recorded on the
    asker. One Pending You ended already, followed up by its asker or dismissed by the user, is recorded so and sent
    nothing (cards.ended). Pending You's "not found" records it lost, and a refusal is said and recorded refused. The
    close's state, or None."""
    who, card, key = c["by"], c["card"], c["key"] or ""
    lost, outcome = None, words
    try:
        with acts.bridge(who, "The question stays open.") as py:
            got, lost = py.answer("get_request", {"requestId": card, "name": who})
            state = cards.ended(got) if lost is None else None
            if state:
                outcome = ENDED_ELSEWHERE
            elif lost is None:
                tool, args, state = cards.close_call(got, card, who, reason=words)
                _, lost = py.answer(tool, args)
            if lost is not None and not cards.lost(lost, who):
                fail(f"Pending You refused the close: {lost}")
    except Refusal as e:
        acts.emit(label, "card.close", [f"agent/{who}"], by=who, refused=str(e), Card=card, Key=key)
        print(f"question {card} of {who} not withdrawn: {e}", file=sys.stderr)
        return None
    if lost is not None:
        card_lost(acts, label, who, key, card, lost)
        return "lost"
    acts.emit(label, "card.close", [f"agent/{who}"], by=who, Card=card, Key=key, State=state, Outcome=outcome)
    return state


def sweep_judgments(fleet, read, here, now):
    """The judgments the rail's sweep of the cards acts on, made on this host (here) at now from a read (rail_read):
    each drive's whose plan was read and whose run record was read from its branch, [(label, owners, planner, j)],
    j as sweep_judged gives it, owners each row's owner by its key with each decision record's row the design agent's,
    planner the batches' owner, each land/ key told a kit's from a bolt's by the drive's kits the read holds, and
    each card's owner judged against the teams file's labels now, for a role that left the fleet; and
    each drive it can't judge with why, [{label, why}], its run record unread. A decision on plain facts (code.7)."""
    unswept, judged = [], []
    down = {h for h, v in read["sv"].items() if not v["ok"]}
    for l, _, _, pl in read["found"]:
        if not pl:
            continue
        unread = read["unread"].get(l, {})
        if unread:
            unswept.append(dict(label=l, why="; ".join(f"its run record could not be read from {b}, so which cards are open can't be told: {v}"
                                                       for b, v in sorted(unread.items()))))
            continue
        rows = [r for r in read["rows"] if r["label"] == l]
        owners = {r["key"]: row_owner(fleet, pl, r) for r in rows}
        blind = {b.name() for b in pl.bolts() if bolt_host(fleet, l, b, read.get("runs")) in down}
        blind |= {b.get("Repo") for b in pl.bolts() if b.name() in blind and b.get("Repo")}  # a kit's card, a bolt of it unread
        planner = row_owner(fleet, pl, dict(label=l, group="batches", key=None))
        design = (f"{l}-design", fleet["drives"][l]["machine"])
        j = sweep_judged(here, rows, [c for c in read["cards"] if c["label"] == l], read["logs"].get(l, []), owners, blind,
                         read["proposed"].get(l), now, planner, design, read["kits"][l],
                         {x["bolt"]: r["key"].split("/", 1)[1] for r in rows if r["group"] == "land" for x in r.get("bolts", [])},
                         labels=set(fleet["drives"]))
        judged.append((l, dict(owners, **{r["key"]: design for r, _ in j["again"] if r["group"] == "records"}), planner, j))
    return judged, unswept


def cards_asked(fleet, read, here, now):
    """The cards the rail's sweep asks Pending You whether it still finds, of the judgments it would act on
    (sweep_judgments): each card of a row that is gone, each held with its row, each question, each whose role left
    the fleet and each decision record's still open, each once, in order.
    The host's follower asks after them on its clock's tick (cards_fetched) and none when there are none. A decision
    on plain facts (code.7)."""
    judged, _ = sweep_judgments(fleet, read, here, now)
    return list(dict.fromkeys(c["card"] for _, _, _, j in judged for c in [c for c, *_ in j["gone"]] + [c for c, _ in j["held"]] + j["questions"]
                              + [c for c, _ in j["left_fleet"]] + j["records"]))


def cards_owned(judged, logs):
    """The cards the rail's sweep reads in their owners' names (design Decision 2 of
    a-wait-on-the-user-is-one-open-card-the-rail-agrees-with), from its judgments ([(label, j)], j as sweep_judged gives
    it) and each drive's run record (logs, {label: entries}): {owner: {card: whether the run record holds its
    answer (answer_due)}}, each card of a row that is gone, held with its row, each question and each decision record's
    still open, under the name its post was made in: a row's owner, a question's asker, the design agent; a card whose
    owner left the fleet is none, since that name is no one's now. In order. A decision on plain facts (code.7)."""
    out = {}
    for l, j in judged:
        es = logs.get(l) or []
        for c in [c for c, *_ in j["gone"]] + [c for c, _ in j["held"]] + j["questions"] + j.get("records", []):
            out.setdefault(c["by"], {}).setdefault(c["card"], not answer_due(es, c["card"]))
    return out


def owners_asked(fleet, read, here, now):
    """The owners whose pending lists the host's follower reads on its clock's tick, with the cards of each it asks
    after (cards_owned), of the judgments the rail's sweep would act on (sweep_judgments). A decision on plain facts
    (code.7)."""
    judged, _ = sweep_judgments(fleet, read, here, now)
    return cards_owned([(l, j) for l, _, _, j in judged], read.get("logs") or {})


def askers_asked(fleet, read, here, now):
    """The agents whose questions the rail's sweep would judge (sweep_judgments), each once, in order: whose panes herdr
    is asked about, the host's follower asking on its clock's tick beside Pending You (askers_listed). A decision on
    plain facts (code.7)."""
    judged, _ = sweep_judgments(fleet, read, here, now)
    return list(dict.fromkeys(c["by"] for _, _, _, j in judged for c in j["questions"]))


def askers_listed(fleet, names, acts=None):
    """herdr's listing of each asker's pane, as the card sweep reads it (SweepActs.listed), {name: (listed, why)}, read
    afresh at the follower's tick, its sessions listed once each; none read when no asker is named."""
    if not names:
        return {}
    crew.herdr_fresh()
    acts = acts or SweepActs(fleet)
    return {name: acts.listed(name) for name in names}


def cards_fetched(fleet, asked, acts=None, owned=None):
    """The card sweep's one ask of Pending You, in crew's own name (SWEEPER), whether it still finds each card asked,
    which it answers for another assistant's card by refusing it as that assistant's and for one this host's sign-in no
    longer reaches with "not found": ({card: (got, words)}, None), or ({}, why) when the bridge failed; no bridge when
    none is asked. With owned ({owner: {card: whether its answer is recorded}}, cards_owned), the same bridge reads each
    owner's pending list in the owner's name and the cards whose state it shows changed (owners_read), handed back
    third: ({card: (got, words)}, why, {card: (got, words)})."""
    if not asked and not owned:
        return ({}, None) if owned is None else ({}, None, {})
    acts = acts or SweepActs(fleet)
    try:
        with acts.bridge(SWEEPER, SWEEP_LATER) as py:
            found = {card: py.answer("get_request", {"requestId": card, "name": SWEEPER}) for card in asked}
            return (found, None) if owned is None else (found, None, owners_read(py, owned))
    except Refusal as e:
        return ({}, str(e)) if owned is None else ({}, str(e), {})


def owners_read(py, owned):
    """Each owner's cards read in its own name, in one session with Pending You (py), as crew reads its own cards
    (briefs.16; design Decision 2 of a-wait-on-the-user-is-one-open-card-the-rail-agrees-with): the owner's pending list,
    once (list_pending, cards.pending_turns), and get_request in the owner's name for each card asked (owned, {owner:
    {card: whether its answer is recorded}}) that is on the agent's turn with its answer not yet recorded, or that the
    list no longer holds, which it has ended, lost or holds in another name; an owner whose list it can't read reads none
    of its cards (read.1). {card: (got, words)}."""
    out = {}
    for owner, held in owned.items():
        listed, words = py.answer("list_pending", {"name": owner})
        turns = cards.pending_turns(listed) if words is None else None
        if turns is None:
            continue
        for card, recorded in held.items():
            if card not in turns or turns[card] == "agent" and not recorded:
                out[card] = py.answer("get_request", {"requestId": card, "name": owner})
    return out


def shown_heads(entries, card):
    """The rows a kit's landings card showed, as its last post or change the run record holds done recorded them
    (built_fields): its Heads, or None for none recorded."""
    return next((e.get("Heads") for e in reversed(entries) if e.get("Card") == card and not e.get("Refused")
                 and e.get("Act") in ("card.post", "card.update") and e.get("Heads")), None)


def offered_boxes(shown):
    """The boxes a kit's landings card offered, land:<bolt> of each row it showed (shown_heads' Heads) but those it
    showed taking main first, which carried none (heads_taking)."""
    return [f"land:{b}" for b, _, _ in card_heads(shown) if b not in heads_taking(shown)]


def sweep_cards(fleet, read, acts=None, answers=None, listed=None):
    """The rail read's sweep of the cards on this host, under its sign-in (record 0031 §1, §2, read.4): for each
    drive whose plan was read, and whose run record was read from its branch, it closes each card of a row that
    is gone with why (sweep_judged, row_gone), a proposal's only on the plan as this read holds it (read["proposed"],
    proposals_held), at or past the commit its card was raised at (older_than_card), and each decision record's card,
    under either key form, at the record's status
    (record_settled), withdraws each card of crew's whose owner left the fleet in its owner's name, saying so and how
    whoever holds its work now raises it again (sweep_judged's left_fleet, cards.left_said), the card alone, since its
    row's reading and previews are the drive's still and end with the row (card_closed, sweep_sessions),
    withdraws each question whose asker's pane herdr lists with no agent in it, naming the asker,
    and leaves one whose asker's pane it can't read, saying why (SweepActs.listed, read.1), posts again
    through its kind's raise each row's card Pending You no longer finds, and posts through its kind's raise each row's
    card that has none; a lost card of a kind with no raise is recorded lost, for its owner to raise again with the
    command that raised it, and a row of one is left as it is. Before any of it, where the drive's planner runs,
    it records crew's close of each batch that waits on nothing, once, as batch.close on batch/<n> in the planner's
    name with its card key and why (briefs.12), so a host not signed in still records it; a card open under its key is
    withdrawn with the same words, as a card whose row is gone. It asks Pending You in crew's own name
    (SWEEPER) whether it finds each card (cards_fetched), in one bridge and none when it asks after no card, and in
    that bridge reads each owner's pending list in the owner's name and each card it shows changed (owners_read,
    cards_owned), recording the user's answer on each it reads answered, once (answer_seen, did answered), and the close
    of each Pending You reports ended, on that read, sending it nothing (ended_close: closed as ended in Pending You
    already, with the answer and a landings card's send, or withdrawn), which it then acts on no more, a row of one that
    still waits being a row with none at the next read; or, for
    the host's follower, which asks on its clock's tick alone, takes answers, (found, why), the clock's last ask's,
    acting on no card that ask did not answer for, until the next tick does, and listed, herdr's listing of the askers
    read on that tick (askers_listed), judging no question whose asker it did not list. Every row's card this
    host's sign-in can't reach, posted from another host or lost to its owner, while the row's owner runs here, is
    posted again through its kind's raise, its summary saying the older copy is dead, the older copy reported lost and
    never asked after nor closed from here, and a raise that posts none reported left (sweep_judged's again, briefs.11,
    briefs.12, read.1). A card its owner's read finds Pending You holds in another assistant's name is lost to its owner
    (cards.lost given the owner, Decision 6), as one Pending You no longer finds is: its row's card posted again in the
    owner's name while its row waits, and recorded lost, posted by nobody, once its row is gone. A host not signed in,
    or a bridge that fails, changes nothing more, and is said, as is a drive whose record could not be read from its
    branch, which records no close either (read.1). crew board sweeps nothing (state.4). Returns {done: [{label, key,
    card, by, did, words, new}], unswept: [{label, why}]}, did answered, closed, withdrawn, lost, posted or left, a
    batch's close by crew with card and new None; and, when it recorded an answer, answered: {card: {at, answer,
    heads}}, each as record_reading would read it, for the read's open cards (swept_cards)."""
    acts = acts or SweepActs(fleet)
    here, now = acts.host(), acts.now()
    out, judged = {"done": [], "unswept": []}, []
    found_judged, out["unswept"] = sweep_judgments(fleet, read, here, now)
    for l, owners, planner, j in found_judged:
        for key, why in j.pop("settled"):
            got = acts.emit(l, "batch.close", [key.partition("-")[0]], by=planner[0], why="batch: closed by crew, it waits on nothing",
                            Key=key, Outcome=why)
            out["done"].append(dict(label=l, key=key, card=None, by=planner[0], did="closed" if got else "left",
                                    words=why if got else "crew's close was not recorded, as said above", new=None))
        j["none"] = [r for r in j["none"] if acts.raise_of(r["key"].split("/")[0])]
        j["again"] = [(r, c) for r, c in j["again"] if acts.raise_of(r["key"].split("/")[0])]
        if any(j.values()):
            judged.append((l, owners, j))
    if not judged:
        return out
    asked = list(dict.fromkeys(c["card"] for _, _, j in judged for c in [c for c, *_ in j["gone"]] + [c for c, _ in j["held"]] + j["questions"]
                               + [c for c, _ in j["left_fleet"]] + j["records"]))
    logs = read.get("logs") or {}
    fetched = answers if answers is not None else cards_fetched(fleet, asked, acts, cards_owned([(l, j) for l, _, j in judged], logs))
    found, error = fetched[:2]
    mine = fetched[2] if len(fetched) > 2 else {}  # the cards read in their owners' names (owners_read)
    if error is not None:
        out["unswept"] += [dict(label=l, why=error) for l, _, _ in judged]
        return out

    def did(l, key, card, by, what, words, new=None):
        out["done"].append(dict(label=l, key=key, card=card, by=by, did=what, words=words, new=new))

    def lost_words(c):
        """Pending You's words when a card is lost to its owner: its own ask's "not found", or the owner's read of it
        refused as another assistant's card (cards.lost given the owner, design Decision 6), which crew's own ask, in
        its own name, is refused as by design; None when it is not."""
        words = found.get(c["card"], (None, None))[1]
        if cards.lost(words):
            return words
        theirs = mine.get(c["card"], (None, None))[1]
        return theirs if cards.lost(theirs, c["by"]) else None

    def raised(l, row, owner):
        """The row's card posted through its kind's raise, in record 0031's key form alone: its id, or None, with
        whether the kind has a raise; a raise's refusal is said, and taken as no raise on this read."""
        up = acts.raise_of(row["key"].split("/")[0]) if cards.row_object(row["key"]) else None
        try:
            return (up(fleet, row, acts=acts) if up else None), bool(up)
        except Refusal as e:
            did(l, row["key"], None, owner, "left", f"its raise refused: {e}")
            return None, None
    recorded = {}  # each drive's run record with the answers this sweep recorded
    for l, owners, j in judged:  # the user's answers its owners' reads found, recorded first (Decision 1)
        es = recorded[l] = (logs.get(l) or []) + acts.entries(l)
        for c in [c for c, *_ in j["gone"]] + [c for c, _ in j["held"]] + j["questions"] + j["records"]:
            got, words = mine.get(c["card"], (None, None))
            if words is not None or not isinstance(got, dict) or got.get("status") != "answered":
                continue
            kit = (c["key"] or "").startswith("land/") and c["key"].split("/", 1)[1] in (read.get("kits") or {}).get(l, ())
            shown = shown_heads(es, c["card"]) if kit else None
            seen = answer_seen(acts, l, c["by"], c["key"] or "", c["card"], got, es, card_heads(shown) if kit else None,
                               offered_boxes(shown) if kit else ())
            if seen:
                es.append(dict(Act="card.answer", By=c["by"], **seen))
                did(l, c["key"], c["card"], c["by"], "answered", seen["Answer"])
                out.setdefault("answered", {})[c["card"]] = dict(at=now, answer=seen["Answer"], heads=seen.get("Heads"))
    ended = set()  # the cards its owners' reads found ended in Pending You, recorded so on this read (Decision 5)
    for l, owners, j in judged:
        for c in [c for c, *_ in j["gone"]] + [c for c, _ in j["held"]] + j["questions"] + j["records"]:
            got, words = mine.get(c["card"], (None, None))
            state = ended_close(acts, l, c["by"], c["key"] or "", c["card"], got, recorded[l]) if words is None and got else None
            if state:
                ended.add(c["card"])
                did(l, c["key"], c["card"], c["by"], state, "ended in Pending You already")
        j["gone"] = [g for g in j["gone"] if g[0]["card"] not in ended]
        j["held"] = [h for h in j["held"] if h[0]["card"] not in ended]
        j["unread"] = [u for u in j["unread"] if u[0]["card"] not in ended]
        j["questions"] = [q for q in j["questions"] if q["card"] not in ended]
    for l, owners, j in judged:
        kits = (read.get("kits") or {}).get(l, ())
        for c, bolts in j["waiting_on_owner"] + [(c, send_waits(recorded[l], c["card"])) for c, *_ in j["gone"]
                                                 if (land_key(c["key"], kits) or (None,))[0] == "kit" and send_waits(recorded[l], c["card"])]:
            did(l, c["key"], c["card"], c["by"], "left", f"{WAITS_ON_OWNER}waits on the runner to land {joined(bolts)}")
        waiting = {d["card"] for d in out["done"] if d["label"] == l and d["did"] == "left" and d["words"].startswith(WAITS_ON_OWNER)}
        for c, outcome, reason in j["gone"]:
            if c["card"] not in found or c["card"] in waiting:
                continue
            words = lost_words(c)
            if words:
                card_lost(acts, l, c["by"], c["key"], c["card"], words)
                did(l, c["key"], c["card"], c["by"], "lost", ("its row is gone" if card_kind(c["key"]) == "row" else "its record is settled")
                    + ", so nobody posts it again")
            elif row_card_close(fleet, l, c["by"], c["key"], outcome, reason, acts):
                did(l, c["key"], c["card"], c["by"], "closed" if outcome else "withdrawn", outcome or reason)
            else:
                did(l, c["key"], c["card"], c["by"], "left", "its close did not go through, as said above")
        for c, words in j["left_fleet"]:  # only the card goes: its row's reading and previews are the drive's still
            if c["card"] not in found:
                continue
            if cards.lost(found[c["card"]][1]):
                card_lost(acts, l, c["by"], c["key"], c["card"], found[c["card"]][1])
                did(l, c["key"], c["card"], c["by"], "lost", f"{c['by']} left the fleet, so nobody posts it again in that name")
                continue
            shut = card_closed(acts, l, c["by"], c["key"], None, words)
            if shut:
                did(l, c["key"], c["card"], c["by"], "withdrawn", words)
            else:
                did(l, c["key"], c["card"], c["by"], "left", "its close did not go through, as said above" if shut is False else
                    "no card of its owner's is held open under its key on this host, or Pending You no longer finds it, as said above")
        for c in j["questions"]:
            if c["card"] not in found:
                continue
            words = lost_words(c)
            if words:
                card_lost(acts, l, c["by"], c["key"] or "", c["card"], words)
                did(l, c["key"], c["card"], c["by"], "lost", "this host's sign-in no longer reaches it" if cards.lost(words)
                    else f"Pending You holds it in another name: {words}")
                continue
            if listed is not None and c["by"] not in listed:
                continue
            here_, why = listed[c["by"]] if listed is not None else acts.listed(c["by"])
            if here_ is None:
                did(l, c["key"], c["card"], c["by"], "left", f"whether {c['by']} still runs can't be told: {why}")
            elif not here_:
                state = question_close(acts, l, c, f"{c['by']} ended; ask again if it still matters")
                did(l, c["key"], c["card"], c["by"], state or "left", {None: "its close did not go through, as said above",
                                                                       "lost": "this host's sign-in no longer reaches it"}.get(state, f"{c['by']} ended"))
        for c, row in j["held"]:
            words = lost_words(c)
            if not words:
                continue
            new, kind_raises = raised(l, row, c["by"])
            if new:
                did(l, c["key"], c["card"], c["by"], "lost", f"posted again as {new}", new)
            elif kind_raises is False:
                card_lost(acts, l, c["by"], c["key"], c["card"], words)
                did(l, c["key"], c["card"], c["by"], "lost", f"crew raises no card for {c['key']} on a rail read, so {c['by']} raises it again with the command that raised it")
            elif kind_raises:
                did(l, c["key"], c["card"], c["by"], "left", ("Pending You no longer finds it" if cards.lost(words) else
                                                              "Pending You holds it in another name") + ", and its raise posted none")
        for row, older in j["again"]:
            owner = owners[row["key"]][0]
            new, kind_raises = raised(l, dict(row, dead=older), owner)
            if new:
                did(l, row["key"], older, owner, "lost", stranded_said(read["logs"].get(l, []), older, owner, new), new)
            elif kind_raises:
                did(l, row["key"], older, owner, "left",
                    "its batch no longer waits to be read" if row["key"].startswith("batch/") else "its raise posted none")
        for c, row in j["unread"]:
            if c["card"] not in found or lost_words(c):
                continue
            try:
                with acts.bridge(c["by"], SWEEP_LATER) as py:
                    got, words = py.answer("get_request", {"requestId": c["card"], "name": c["by"]})
                not words or fail(f"Pending You refused get_request: {words}")
            except Refusal as e:
                did(l, c["key"], c["card"], c["by"], "left", f"whether it waits on the user can't be read: {e}")
                continue
            if not card_waiting(got):
                continue
            try:
                url = acts.reading_again(l, c["key"])[0]
            except Refusal as e:
                did(l, c["key"], c["card"], c["by"], "left", f"its reading could not be opened: {e}")
            else:
                did(l, c["key"], c["card"], c["by"], "opened", f"its reading opened at {url}" if url else "its rows' readings opened")
        for row in j["none"]:
            owner = owners[row["key"]][0]
            new, _ = raised(l, row, owner)
            if new:
                did(l, row["key"], None, owner, "posted", "its row had none open", new)
    return out


def sweep_moved(fleet, read, acts=None):
    """The rail read's raise of each kit's landings card main moved under (rail-cards "Main moves under an open card"),
    once its sweep acted, on the drive's main machine alone, where main-level ops's cards are: for each drive
    whose plan was read, each landings card open on this host in ops's name (land/<kit>), the revision of main the
    survey read its kit at where its work runs, as last fetched with no fetch of its own (SweepActs.main_at,
    plan.18), and the one its rows were last forecast against (CardActs.kept_main) are compared (landings_moved), and
    each card main moved under is raised again (SweepActs.raise_kit), which fetches GitHub's main and forecasts its
    rows there; a card main has not moved under is fetched for and raised by none. Each card whose answer this read's
    sweep recorded (landings_answered) is raised too, so the user's send posts its lands by the first act that reads it,
    the host's follower among them (rail-cards "A send's lands are posted by the first act that reads it"). A raise
    refused is said, and the read goes on. Returns {raised: [{label, kit, was, now, card, said, sent}], unread: [{label,
    kit, why}]}, said the refusal's words or None, sent whether it was raised for the answer alone."""
    acts = acts or SweepActs(fleet)
    here, out = acts.host(), {"raised": [], "unread": []}
    for l, _, _, pl in read["found"]:
        if not pl or crew.drive_of(fleet, l)["machine"] != here:
            continue
        kits = read["kits"][l]
        open_ = [(l, kit) for c in read["cards"] if c["label"] == l and c["host"] == here and c["by"] == f"{l}-ops"
                 for kind, kit in [land_key(c["key"], kits) or (None, None)] if kind == "kit"]
        mains = {c: acts.main_at(l, c[1], read["sv"], read.get("runs")) for c in dict.fromkeys(open_)}
        kept = {c: acts.kept_main(*c) for c in mains}
        due, unread = landings_moved(open_, {c: m for c, (m, _) in mains.items()}, kept)
        out["unread"] += [dict(label=l, kit=c[1], why=mains[c][1]) for c in unread]
        sent = landings_answered(read, l, here, kits)
        for c in list(due) + [c for c in sent if c not in due]:
            moved = dict(label=l, kit=c[1], was=kept.get(c), now=(mains.get(c) or (None,))[0], card=None, said=None,
                         sent=c in sent and c not in due)
            try:
                moved["card"] = acts.raise_kit(l, c[1])
            except Refusal as e:
                moved["said"] = str(e)
            out["raised"].append(moved)
    return out


def landings_answered(read, label, here, kits):
    """The kits' landings cards of a drive, open on this host in its main-level ops's name, whose answer this rail
    read's card sweep recorded (sweep_cards' answered, by card), as [(label, kit)], from the read alone (code.7)."""
    answered = (read.get("swept") or {}).get("answered") or {}
    return list(dict.fromkeys((label, kit) for c in read.get("cards") or [] if c["label"] == label and c["host"] == here
                              and c["by"] == f"{label}-ops" and c["card"] in answered
                              for kind, kit in [land_key(c["key"], kits) or (None, None)] if kind == "kit"))


# How long an ask stands before the rail's read may take its card or row for gone (Decision 7 of
# a-cards-preview-is-asked-of-the-runner): a card raised since the read began is not yet in it.
PREVIEW_GRACE = 120


def previews_live(label, judgment, entries):
    """The work whose card stands, by the rail's judgment (sweep_judgment) of a drive, so the asks of its previews
    stand (Decision 7 of a-cards-preview-is-asked-of-the-runner): bolt/<bolt> for each live land/ key, and unit/<unit>
    for each unit of a live batch/<n> or batch/<n>-<k>, the batches read from the drive's run record (entries);
    and the kinds whose every ask stands, those a blind prefix covers (read.1). Returns (works, kinds)."""
    live = judgment["live"]
    works = {f"bolt/{k.split('/')[1]}" for k in live if k.startswith("land/") and len(k.split("/")) >= 2}
    alive = {int(k.split("/")[1].split("-")[0]) for k in live if re.fullmatch(r"batch/\d+(-\d+)?", k)}
    works |= {f"unit/{u}" for m, _, us in batches(entries) if m in alive for u, _, _ in us}
    kinds = {{"land/": "bolt/", "batch/": "unit/"}.get(b) for b in judgment["blind"]} - {None}
    return works, kinds


def ask_card(r, entries):
    """The card a preview's ask was made from, as its work names it (Decision 1 of
    a-cards-preview-is-asked-of-the-runner): a bolt's, its kit's landings card, land/<repo>; a unit's, the newest batch
    of the drive's run record (entries) that holds it, batch/<n>, or None when none does."""
    kind, _, name = (r.get("Work") or "").partition("/")
    if kind == "bolt":
        return f"land/{(r.get('Repo') or '').split('/')[-1]}"
    held = [m for m, _, us in batches(entries) for u, _, _ in us if u == name]
    return f"batch/{max(held)}" if held else None


def sweep_previews(fleet, read, acts=None):
    """The rail read's put-away of each preview crew asked for whose card or row is gone (rail-cards "A card closed
    elsewhere", "A row gone with no raise of its card"; Decision 7 of a-cards-preview-is-asked-of-the-runner), once its
    sweep acted, on the drive's main machine alone, where the cards are: for each drive whose plan was read,
    the standing asks (runner.previews_standing) the rail's judgment keeps neither by a live card's work nor by a blind
    prefix, batch/ while the drive's run record can't be read from its branch (previews_live), each written at least PREVIEW_GRACE seconds before now by its Date
    (runner.previews_put_away), have their done written, one plan write a card (preview_written). A write refused is
    said, and the next read tries again; nothing is put away that crew could not read (read.1). Returns [{label, work,
    revision, said}]."""
    acts = acts or SweepActs(fleet)
    here, now, out = acts.host(), acts.now(), []
    for l, _, _, pl in read["found"]:
        if not pl or crew.drive_of(fleet, l)["machine"] != here:
            continue
        rows = read["rows"]
        readings = {f"land/{b['bolt']}" for r in rows if r["label"] == l and r["group"] == "land" for b in r.get("bolts", []) if b["can"]}
        rowed = {r["key"] for r in rows if r["label"] == l} | readings
        entries = (read.get("logs") or {}).get(l, [])
        works, kinds = previews_live(l, sweep_judgment(l, rowed, read["cards"], read["unread"].get(l), read["batched"].get(l, {}), readings),
                                     entries)
        try:
            requests, reads = (read.get("runs") or {}).get(l) or acts.runner(l)
        except Refusal as e:
            out.append(dict(label=l, work=f"plan/{l}", revision="", said=f"its runners can't be read, so no preview is put away: {e}"))
            continue
        asks = {k: r for k, r in runner.previews_standing(requests, reads).items()
                if not any((r.get("Work") or "").startswith(kind) for kind in kinds)}
        gone = runner.previews_put_away(asks, set(), works, now, PREVIEW_GRACE)
        by = {}
        for r in gone:
            by.setdefault(ask_card(r, entries) or f"{r.get('Work')}", []).append(r)
        for key, rs in sorted(by.items()):
            things = joined(sorted({r.get("Work").split("/", 1)[1] for r in rs}))
            try:
                preview_written(fleet, l, key, things, rs, done=True, made=[],
                                by=f"{l}-ops" if key.startswith("land/") else f"{l}-planner")
                said = "put away, its card or row gone"
            except Refusal as e:
                said = f"not put away yet, the next read trying again: {e}"
            out += [dict(label=l, work=r.get("Work"), revision=r.get("Revision") or "", said=said) for r in rs]
    return out


def previews_changed(fleet, read, acts=None):
    """The rail read's change of each card whose preview the runner reports anew (rail-cards "A card is changed in place
    when the runner reports its preview anew"; Decision 8 of a-cards-preview-is-asked-of-the-runner), on the
    drive's main machine alone: for each card open on this host and not answered, by the run record's card.answer,
    that carries an ask of a preview not put away (runner.previews_asked), main-level ops's land/<kit> its asks of the
    bolts of its last recorded rows at their heads, the planner's batch/<n> its asks of its units, the word of what the
    runner now reports of each (runner.preview_word) is compared with what the card was last told (told_read), and,
    where any differs, the card is raised again with one note naming each such thing and what its preview now is
    (preview_changed, through acts.preview_note), its raise keeping what it then told it (told_kept). A card whose
    record of what it was told is lost is changed once. A card posted with no key, an agent's own question, carries
    no ask and is passed over. Returns [{label, key, note, said}], said a refusal's words or
    None."""
    acts = acts or SweepActs(fleet)
    here, out = acts.host(), []
    for l, _, _, pl in read["found"]:
        if not pl or crew.drive_of(fleet, l)["machine"] != here or read["unread"].get(l):
            continue
        entries = (read.get("logs") or {}).get(l, [])
        try:
            requests, reads = (read.get("runs") or {}).get(l) or acts.runner(l)
        except Refusal:
            continue
        asked, told, kits = list(runner.previews_asked(requests).values()), told_read(l), read["kits"].get(l, [])
        answered = {e.get("Card") for e in entries if e.get("Act") == "card.answer"}
        for c in [c for c in read["cards"] if c["label"] == l and c["host"] == here and c["card"] not in answered and c["key"]]:
            key, kind = c["key"], land_key(c["key"], kits)
            if c["by"] == f"{l}-ops" and kind and kind[0] == "kit":
                heads = card_heads(next((e.get("Heads") for e in reversed(entries) if e.get("Card") == c["card"] and e.get("Heads")
                                         and not e.get("Refused")), None))
                mine = [(b, r) for b, h, _ in heads for r in asked if r.get("Work") == f"bolt/{b}" and r.get("Repo") == kind[1]
                        and (r.get("Revision") or "").startswith(h)]
            elif c["by"] == f"{l}-planner" and re.fullmatch(r"batch/\d+", key):
                units = {u for m, _, us in batches(entries) if m == int(key.split("/")[1]) for u, _, _ in us}
                mine = [(r.get("Work").split("/", 1)[1], r) for r in asked if r.get("Work") in {f"unit/{u}" for u in units}]
            else:
                continue
            was = told.get(key, {})
            now = [(thing, r, runner.preview_report(reads, r)) for thing, r in mine]
            moved = [(thing, p) for thing, r, p in now if was.get(r.get("Request")) != runner.preview_word(p)]
            if not moved:
                continue
            note = "; ".join(asked_note(thing, p) for thing, p in moved)
            said = None
            try:
                acts.preview_note(l, key, note)
            except Refusal as e:
                said = str(e)
            out.append(dict(label=l, key=key, note=note, said=said))
    return out


def card_folder(rel):
    """The card key and unit (None but for an old batch card's, batch/<n>-<k>) whose session a folder under
    ~/.local/state/crew/cards/<label>/ keeps, from its path there: batch/<n> is a key's own folder, as a proposal's;
    None when the path is no key's folder."""
    path = "/".join(rel.parts)
    if any(re.fullmatch(k, path) for k in CARD_KEYS + (VERIFY_KEY,)):
        return path, None
    key = "/".join(rel.parts[:2])
    if len(rel.parts) == 3 and old_batch(key) and crew.NAME.match(rel.parts[2]):
        return key, rel.parts[2]
    return None


def card_sweep(fleet, a, acts=None):
    """crew card sweep --label L: the rail's, run on each host of the drive with its judgment on standard input as
    JSON, {"live": [card keys], "blind": [key prefixes], "landings": [{bolt, kit, dir, stages}]}, its landings given
    only to a host a started bolt's work runs on (landings_judged). It ends, through end_session, each session crew recorded on
    this host for the drive whose key is in no live entry and starts with no blind prefix, once it is at least two
    minutes old by its own start against this host's clock and its folder's lock is free (crew card session holds it
    while it starts one). It puts away no preview: the rail's read on the drive's main machine writes the done of
    each whose card or row is gone (sweep_previews). Then it acts on each reading of a live key the user sent and nobody has read (readings_sent):
    a batch's sent with no words is recorded read as the planner's read records it (sweep_wordless), and every other
    reading's owner is told once, the mark written only once the tell went through (sweep_told), since nothing of
    crew's waits on a reading (teams.24). Then it reads each landing the judgment names, of a bolt whose work runs
    here as the rail read it, that may have an outcome or a close nothing recorded (reap_judged), what that says on
    standard error. It prints, as a JSON list, each session and reading it acted on: its key, its unit (a batch card's)
    or null, what it said, whether it sent SIGTERM, and, for a reading, sent. A folder with no session.json, or whose path is no card key's, is left alone, and a record it can't
    read is kept and said (read.1, read.4)."""
    a.key is None or fail("crew card sweep takes no key: it judges every session crew recorded on this host, from the "
                          "rail's judgment on standard input")
    label = default_label(fleet, a) or fail("crew card sweep runs for a drive: add --label")
    try:
        j = json.loads(sys.stdin.read())
    except ValueError:
        j = None
    (isinstance(j, dict) and {"live", "blind"} <= set(j) <= {"live", "blind", "landings"}
     and all(isinstance(j[k], list) and all(isinstance(x, str) for x in j[k]) for k in ("live", "blind"))
     and all(isinstance(g, dict) and set(g) == {"bolt", "kit", "dir", "stages"} and all(isinstance(g[k], str) for k in ("bolt", "kit", "dir"))
             and isinstance(g["stages"], list) and all(isinstance(x, str) for x in g["stages"]) for g in j.get("landings", []))) or fail(
        'crew card sweep reads the rail\'s judgment on standard input as {"live": [card keys], "blind": [key prefixes], '
        '"landings": [{"bolt", "kit", "dir", "stages"}]}, its landings optional')
    live, blind, root = set(j["live"]), tuple(j["blind"]), CARDS / label
    now, out = datetime.datetime.now(datetime.timezone.utc), []
    for f in sorted(root.rglob("session.json")) if root.is_dir() else []:
        found = card_folder(f.parent.relative_to(root))
        if not judged_dead(found, live, blind):
            continue
        key, unit = found
        name = f"{key} {unit}" if unit else key
        try:
            lock = open(f.parent / ".lock", "a")
        except FileNotFoundError:
            continue  # ended while the sweep looked
        with lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                continue  # its session is being started
            try:
                s = card_recorded(f.parent)
            except Refusal as e:
                out.append(dict(key=key, unit=unit, said=f"{e}; crew ended nothing, and keeps {name}", ended=False))
                continue
            if not s:
                continue
            try:
                left = young(s["started"], now)
            except (ValueError, TypeError):
                out.append(dict(key=key, unit=unit, ended=False,
                                said=f"crew can't read when {name}'s session started ({s['started']}): it ended nothing, and keeps {name}"))
                continue
            if left:
                continue
            said, ended = end_session(label, key, unit)
            out.append(dict(key=key, unit=unit, said=said, ended=ended))
    acts = acts or CardActs(fleet)
    for key, step in readings_due(readings_sent(root, live, blind)):
        said = (sweep_wordless if step == "record" else sweep_told)(fleet, label, key, acts)
        if said:
            out.append(dict(key=key, unit=None, said=said, ended=False, sent=True))
    with contextlib.redirect_stdout(sys.stderr):  # the landings read here (plan.21), its words beside the sweep's list
        reap_judged(fleet, label, j.get("landings", []))
    print(json.dumps(out))


def readings_sent(root, live, blind):
    """The readings of a drive's live card keys on this host, as readings_due reads them: (key, the reading's
    result as card_result gives it, whether it carries crew's told mark), for each key folder under root, the
    drive's CARDS folder, holding a result, a batch's, a long proposal's or a bolt's reading, never an old batch
    card's unit, a key the rail's judgment holds dead or one it can't judge (judged_dead). A result crew can't read is
    left out, said on standard error, and read at the next refresh (read.1)."""
    found = []
    for f in sorted(root.rglob("result.json")) if root.is_dir() else []:
        got = card_folder(f.parent.relative_to(root))
        if not got or got[1] or got[0] not in live or got[0].startswith(tuple(blind)) or old_batch(got[0]):
            continue
        try:
            decided = card_result(f.parent)
        except Refusal as e:
            print(f"card {got[0]}: {e}", file=sys.stderr)
            continue
        found.append((got[0], decided, (f.parent / "told.json").exists()))
    return found


def readings_due(readings):
    """What the rail's refresh does with each reading the user may have sent (card-sessions "The rail's refresh tells
    a reading's owner once that the user sent it", review-batches "A batch whose reading session is sent is read"), a
    decision of facts alone (code.7), from (key, decided, told) as readings_sent gives them: [(key, "record")] for a
    batch's reading approved with no words, which crew records read, since there is nothing to pass on; [(key, "tell")]
    for every other reading approved or annotated that carries no told mark, whose owner crew tells to read it; nothing
    for a reading undecided, closed with no decision, or told already. A reading crew card read has read is set aside
    or ended, so it is no longer found."""
    due = []
    for key, decided, told in readings:
        if not decided or decided[0] not in ("approved", "annotated") or told:
            continue
        wordless = decided[0] == "approved" and not decided[1] and not decided[2]
        due.append((key, "record" if wordless and key.startswith("batch/") else "tell"))
    return due


def reading_owner(label, key):
    """Who reads a key's reading (card-sessions): the planner a batch's and a long proposal's, main-level ops a bolt's,
    land/<bolt>, as the owner of its kit's landings card (Decision 6 of the-team-machinery-leaves). A decision of the
    key alone (code.7)."""
    return f"{label}-ops" if key.startswith("land/") else f"{label}-planner"


def sweep_told(fleet, label, key, acts):
    """The owner of a reading the user sent told once that it was sent, by the rail's refresh (card-sessions "The rail's
    refresh tells a reading's owner once that the user sent it"): crew's tell (roles.4), naming the key and crew card
    read and holding no word of the user's (roles.6), and the reading marked told, told.json beside its result, only
    once the tell went through; a tell refused, the owner not up among it, leaves it untold for the next refresh, so
    delivery is at least once. What it did, in words."""
    owner = reading_owner(label, key)
    why = io.StringIO()
    try:
        with contextlib.redirect_stderr(why):
            told = acts.tell(owner, f"The user sent {key}'s reading. Run crew card read {key} for what they sent.")
    except Refusal as e:
        told, why = False, io.StringIO(str(e))
    if not told:
        return f"the user sent its reading, and crew could not tell {owner}: " + (
            (why.getvalue().strip().splitlines() or ["the tell failed"])[-1] + "; the next refresh tells it")
    d = CARDS / label / key
    try:
        (d / "told.json").write_text(json.dumps({"told": owner, "at": datetime.datetime.now(datetime.timezone.utc)
                                                 .strftime("%Y-%m-%dT%H:%M:%SZ")}) + "\n")
    except OSError as e:
        return f"the user sent its reading, and {owner} was told, but crew could not mark it told: {e.strerror or e}"
    return f"the user sent its reading, and {owner} was told to run crew card read {key}"


def sweep_wordless(fleet, label, key, acts):
    """A batch's reading the user approved with no words, recorded read by the rail's refresh on the main level's host
    (review-batches "The session approved"), as the planner's crew card read records it, whichever comes first: its
    card, read once, closed "Read; no notes", which ends the reading, and crew's own close of the batch recorded when
    no card closed (batch_read_close). A card the user answered with a note has words to pass on, so the planner is
    told instead (sweep_told), and a card crew can't read now leaves the batch to the next refresh. What it did, in
    words."""
    owner, d = f"{label}-planner", CARDS / label / key
    card = cards.card_under(acts.entries(label), key, owner)
    got = None
    if card:
        try:
            with acts.bridge(owner, "The next refresh reads it again.") as py:
                got, words = py.answer("get_request", {"requestId": card, "name": owner})
        except Refusal as e:
            words = str(e)
        if words is not None and cards.lost(words):
            card_lost(acts, label, owner, key, card, words)
            card, got = None, None
        elif words is not None:
            return f"the user approved its reading with no notes, and crew can't read its card {card} now: {words}; the next refresh reads it again"
    r = reading_read(key, got, card_result(d), pane_answered(acts.entries(label)).get(key), held=bool(card))
    if r["close"] != read_outcome(0):
        return sweep_told(fleet, label, key, acts)
    said = io.StringIO()
    with contextlib.redirect_stdout(said):
        closed = row_card_close(fleet, label, owner, key, outcome=r["close"], acts=acts) if card else None
        if batch_read_close(closed):
            acts.emit(label, "batch.close", [cards.row_object(key) or key], by=owner,
                      why=f"batch({key.split('/', 1)[1]}): read in its session", Key=key, State="read", Outcome=r["close"])
        ended = acts.end(label, key) if r["end"] and not closed else None
    words = [w for w in said.getvalue().strip().splitlines() + [ended] if w]
    return f"the user approved its reading with no notes, so crew recorded it read, {r['close']}" + (
        f": {'; '.join(words)}" if words else "")


def judged_dead(found, live, blind):
    """Whether the rail's judgment makes a recorded session's key dead: a card key's folder (found), in no live entry and
    under no blind prefix."""
    return bool(found) and found[0] not in live and not found[0].startswith(tuple(blind))


def young(started, now):
    """Whether a session started under CARD_GRACE seconds before now, so the rail's read may not have seen its row yet:
    left for a later sweep. Refused when its start can't be read."""
    return (now - utc(started)).total_seconds() < CARD_GRACE


def card_units(fleet, label, key):
    """The units a batch card holds, from the batch in the run record: every unit of the batch for batch/<n>, the k-th
    five for batch/<n>-<k>."""
    n = int(key.split("/")[1].split("-")[0])
    for m, _, units in batches(drive_entries(fleet, label)):
        if m == n:
            return [u for u, *_ in card_part(key, units)]
    fail(f"{label}'s run record holds no batch {n}")


# ----------------------------------------------------------------------------------------------------- the CLI

class _Unbuilt:
    """A command's parser this run does not need: it takes every definition parser() gives it and keeps none."""

    def __getattr__(self, name):
        return lambda *args, **kwargs: self


SIGNAL_ID = "a signal's full id, <capture>/<NN>-<slug>, or its short one, <capture>/<NN>"


def parser(cls=argparse.ArgumentParser, only=None):
    """crew's command line. With only, the one command a run names is built and the rest are not, since building
    every command's parser is a third of what starting plan.py costs; the names built are in parser.built."""
    ap = cls(prog="crew", add_help=False)
    sub = ap.add_subparsers(dest="cmd", required=True)
    ap.built = []
    if only:
        add = sub.add_parser

        def one(name, **kwargs):
            ap.built.append(name)
            return add(name, **kwargs) if name == only else _Unbuilt()
        sub.add_parser = one
    st = sub.add_parser("state").add_subparsers(dest="sub", required=True)
    i = st.add_parser("init")
    i.add_argument("label")
    # crew drive set: every key crew's module writes for a drive, and for the hosts, console and kept repositories it
    # needs, a flag named as the file names it, with no default and none required here, so drive_given refuses a flag
    # left out or given past its count in crew's own words (code.2, code.5); a flag of several words takes them apart:
    # --runs <role> standing|on-demand for each role's `runs`, --review <after_changes> <after_hours> for `review`. A
    # flag crew does not take, --flume among them, is refused by the parser before anything is read.
    d = sub.add_parser("drive").add_subparsers(dest="sub", required=True)
    i = d.add_parser("set", prog="crew drive set")
    i.add_argument("label")
    i.add_argument("--state", action="append", metavar="OWNER/NAME")
    i.add_argument("--blueprints", action="append", metavar="OWNER/NAME")
    i.add_argument("--machine", action="append", metavar="HOST")
    i.add_argument("--session", action="append", metavar="NAME")
    i.add_argument("--folder", action="append", metavar="PATH")
    i.add_argument("--repos", action="append", metavar="OWNER/NAME")
    i.add_argument("--accounts", action="append", nargs=2, metavar=("ROLE", "ACCOUNT"))
    i.add_argument("--runs", action="append", nargs=2, metavar=("ROLE", "STANDING_OR_ON_DEMAND"))
    i.add_argument("--review", action="append", nargs=2, metavar=("AFTER_CHANGES", "AFTER_HOURS"))
    i.add_argument("--hosts", action="append", nargs=3, metavar=("HOST", "SSH", "KIND"))
    i.add_argument("--roles", action="append", nargs=3, metavar=("ROLE", "KEY", "VALUE"))
    i.add_argument("--console", action="append", metavar="PATH")
    i.add_argument("--repositories", action="append", nargs=3, metavar=("OWNER/NAME", "DIR", "CHECKOUT"))
    i.add_argument("--json", action="store_true")

    v = sub.add_parser("bolts")
    v.add_argument("bolt", nargs="?")
    v.add_argument("--label")
    v.add_argument("--json", action="store_true")
    v = sub.add_parser("rail")
    v.add_argument("--label")
    v = sub.add_parser("answer")
    v.add_argument("work")
    v.add_argument("words")
    v.add_argument("--label")
    v = sub.add_parser("fix")
    v.add_argument("bolt")
    v.add_argument("name")
    v.add_argument("words", nargs="?")
    v.add_argument("--drop", action="store_true")
    v.add_argument("--label")
    ro = sub.add_parser("role").add_subparsers(dest="sub", required=True)
    ro.add_parser("start")
    v = ro.add_parser("end")
    v.add_argument("words")
    v.add_argument("--report", required=True)
    v = ro.add_parser("open")
    v.add_argument("role", choices=crew.KIND_ROLES)
    v.add_argument("--label")
    v = ro.add_parser("land")
    v.add_argument("repo")
    v.add_argument("name")
    v.add_argument("--brief-file", required=True)
    v = sub.add_parser("main").add_subparsers(dest="sub", required=True).add_parser("fix")  # up, down and status are _main's
    v.add_argument("kit")
    v.add_argument("name")
    v.add_argument("words", nargs="?")
    v.add_argument("--drop", action="store_true")
    v.add_argument("--send", action="store_true")
    v.add_argument("--excerpt")
    v.add_argument("--label")
    ca = sub.add_parser("card").add_subparsers(dest="sub", required=True)
    for c in ("session", "wait", "end"):
        x = ca.add_parser(c)
        x.add_argument("key")
        x.add_argument("unit", nargs="?")
        x.add_argument("--label")
    x = ca.add_parser("sweep")  # the rail's, run on each host; a key or unit given is refused
    x.add_argument("key", nargs="?")
    x.add_argument("unit", nargs="?")
    x.add_argument("--label")
    x = ca.add_parser("read")
    x.add_argument("key")
    x.add_argument("--label")
    x.add_argument("--json", action="store_true")
    x = ca.add_parser("preview")
    x.add_argument("key")
    x.add_argument("thing")
    x.add_argument("--done", action="store_true")
    x.add_argument("--label")
    x = ca.add_parser("answer")
    x.add_argument("key")
    x.add_argument("--excerpt", required=True)
    x.add_argument("--label")
    x = sub.add_parser("record")
    x.add_argument("kit")
    x.add_argument("number", type=int)
    g = x.add_mutually_exclusive_group(required=True)
    for status in ("proposed", "accepted", "rejected"):
        g.add_argument(f"--{status}", dest="status", action="store_const", const=status)
    x.add_argument("--settled-in-pane", action="store_true")
    x.add_argument("--excerpt")
    x.add_argument("--alternatives", metavar="FILE")
    x.add_argument("--label")

    bo = sub.add_parser("bolt").add_subparsers(dest="sub", required=True)
    x = bo.add_parser("new")
    x.add_argument("bolt")
    x.add_argument("goal")
    x.add_argument("--repo", required=True)
    x.add_argument("--source", action="append", default=[])
    x.add_argument("--before")
    x.add_argument("--label")
    x = bo.add_parser("start")
    x.add_argument("bolt")
    x.add_argument("--label")
    x = bo.add_parser("order")
    x.add_argument("bolt")
    g = x.add_mutually_exclusive_group(required=True)
    g.add_argument("--before")
    g.add_argument("--first", action="store_true")
    g.add_argument("--last", action="store_true")
    x.add_argument("--label")
    x = bo.add_parser("drop")
    x.add_argument("bolt")
    x.add_argument("reason")
    x.add_argument("--requeue", action="store_true")
    x.add_argument("--label")
    x = bo.add_parser("land")
    x.add_argument("bolt")
    x.add_argument("--label")
    x = bo.add_parser("submit")  # a refusal alone, whatever it is given (bolt_submit)
    x.add_argument("bolt", nargs="*")
    x.add_argument("--excerpt")
    x.add_argument("--label")
    x = bo.add_parser("leave")
    x.add_argument("bolt", nargs="+")
    x.add_argument("--excerpt", required=True, help="the user's words in your pane that stopped their landing, as they wrote them")
    x.add_argument("--label")

    un = sub.add_parser("unit").add_subparsers(dest="sub", required=True)
    x = un.add_parser("add")
    x.add_argument("unit")
    x.add_argument("intent")
    x.add_argument("--bolt")
    x.add_argument("--repo")
    x.add_argument("--source", action="append", default=[])
    x.add_argument("--after", action="append", default=[])
    x.add_argument("--before")
    x.add_argument("--signal", metavar="ID", help=SIGNAL_ID)
    x.add_argument("--unblocks", metavar="BOLT")
    x.add_argument("--label")
    x = un.add_parser("split")
    x.add_argument("unit")
    x.add_argument("intent")
    x.add_argument("--into", nargs=2, action="append", required=True, metavar=("UNIT", "INTENT"))
    x.add_argument("--label")
    x = un.add_parser("amend")
    x.add_argument("unit")
    x.add_argument("intent")
    x.add_argument("--label")
    x = un.add_parser("order")
    x.add_argument("unit")
    g = x.add_mutually_exclusive_group(required=True)
    g.add_argument("--before")
    g.add_argument("--first", action="store_true")
    g.add_argument("--last", action="store_true")
    x.add_argument("--label")
    x = un.add_parser("after")
    x.add_argument("unit")
    x.add_argument("deps", nargs="*")
    x.add_argument("--none", action="store_true")
    x.add_argument("--label")
    x = un.add_parser("move")
    x.add_argument("unit")
    x.add_argument("bolt", metavar="bolt|queue")
    x.add_argument("--unblocks", metavar="BOLT")
    x.add_argument("--label")
    x = un.add_parser("drop")
    x.add_argument("unit")
    x.add_argument("reason")
    x.add_argument("--label")

    # A chore's commands are a unit's of the same name, their subject in `unit` so the same ops build them (plan.11).
    ch = sub.add_parser("chore").add_subparsers(dest="sub", required=True)
    x = ch.add_parser("add")
    x.add_argument("unit", metavar="chore")
    x.add_argument("intent", metavar="words")
    x.add_argument("--bolt")
    x.add_argument("--repo")
    x.add_argument("--source", action="append", default=[])
    x.add_argument("--after", action="append", default=[])
    x.add_argument("--before")
    x.add_argument("--signal", metavar="ID", help=SIGNAL_ID)
    x.add_argument("--unblocks", metavar="BOLT")
    x.add_argument("--label")
    x = ch.add_parser("order")
    x.add_argument("unit", metavar="chore")
    g = x.add_mutually_exclusive_group(required=True)
    g.add_argument("--before")
    g.add_argument("--first", action="store_true")
    g.add_argument("--last", action="store_true")
    x.add_argument("--label")
    x = ch.add_parser("after")
    x.add_argument("unit", metavar="chore")
    x.add_argument("deps", nargs="*")
    x.add_argument("--none", action="store_true")
    x.add_argument("--label")
    x = ch.add_parser("move")
    x.add_argument("unit", metavar="chore")
    x.add_argument("bolt", metavar="bolt|queue")
    x.add_argument("--unblocks", metavar="BOLT")
    x.add_argument("--label")
    x = ch.add_parser("drop")
    x.add_argument("unit", metavar="chore")
    x.add_argument("reason")
    x.add_argument("--label")

    x = sub.add_parser("kit").add_subparsers(dest="sub", required=True).add_parser("rename")
    x.add_argument("old", type=kit_name)
    x.add_argument("new", type=kit_name)
    x.add_argument("--label")

    pp = sub.add_parser("plan").add_subparsers(dest="sub", required=True)
    x = pp.add_parser("propose")
    x.add_argument("file")
    x.add_argument("--replaces", type=int)
    x.add_argument("--label")
    x = pp.add_parser("proposed")
    x.add_argument("n", nargs="?", type=int)
    x.add_argument("--label")
    x.add_argument("--json", action="store_true")
    x.add_argument("--open", action="store_true")
    x = pp.add_parser("approve")
    x.add_argument("n", type=int)
    x.add_argument("--clear", nargs="+", action="extend", default=[], metavar="UNIT")
    x.add_argument("--label")
    x = pp.add_parser("answer")
    x.add_argument("n", type=int)
    x.add_argument("question")
    x.add_argument("answer", nargs="*")
    x.add_argument("--note")
    x.add_argument("--label")
    x = pp.add_parser("drop")
    x.add_argument("n", type=int)
    x.add_argument("reason")
    x.add_argument("--label")

    x = sub.add_parser("signal-move", prog="crew signal move")
    x.add_argument("signal", metavar="id", help=SIGNAL_ID)
    x.add_argument("move", choices=CURATION)
    x.add_argument("--target")
    x.add_argument("--reason")
    x.add_argument("--label")
    x = sub.add_parser("signal-show", prog="crew signal show")
    x.add_argument("signal", metavar="id", help=SIGNAL_ID)
    x.add_argument("--label")
    x = sub.add_parser("signal-land", prog="crew signal land")
    x.add_argument("dir", metavar="capture-dir")
    x.add_argument("--label")
    x = sub.add_parser("signal")
    x.add_argument("slug")
    x.add_argument("asserts")
    x.add_argument("--kind", choices=KINDS, help="constraint for an agent, ask for the user, unless given")
    x.add_argument("--subject", help="tags, separated by commas")
    g = x.add_mutually_exclusive_group()
    g.add_argument("--excerpt", help="the words that show it, verbatim, as the session received them")
    g.add_argument("--excerpt-file", help="a file holding them, for words the shell would mangle")
    x.add_argument("--label")

    # The commands on a drive's main level and on a kit's host, each one process on the host it acts on (bash crew
    # runs them, and forwards them when one names another host).
    x = sub.add_parser("_land-row")
    x.add_argument("label")
    x.add_argument("bolt")
    x.add_argument("--json", action="store_true")
    x = sub.add_parser("_land-card")
    x.add_argument("label")
    x.add_argument("kit")
    x.add_argument("--note")
    x.add_argument("--pane")  # an older crew's landing on the user's words in ops's pane, read as nothing (land_card_cmd)
    x = sub.add_parser("_made")
    x.add_argument("label")
    x.add_argument("unit", nargs="+")
    x.add_argument("--json", action="store_true")
    x = sub.add_parser("_batch-card")
    x.add_argument("label")
    x.add_argument("n", type=int)
    x.add_argument("--note")
    x = sub.add_parser("_sweep")
    x.add_argument("label")
    x.add_argument("kit")
    x.add_argument("--dir", required=True)
    x.add_argument("--landed")
    x.add_argument("--outcome")
    x.add_argument("--units", nargs="+", default=[])
    x.add_argument("--said")  # with --here, an older crew's landing on the user's words in ops's pane, read as nothing
    x.add_argument("--here", action="store_true")
    x = sub.add_parser("_main")
    x.add_argument("act", choices=("up", "down", "status"))
    x.add_argument("label")
    x.add_argument("--force", action="store_true")
    x = sub.add_parser("_review")
    x.add_argument("label")
    x.add_argument("--wait", action="store_true")
    x.add_argument("--timeout", type=int, default=3600000)
    x = sub.add_parser("review-delivered", prog="crew review delivered")
    x.add_argument("--label")
    x = sub.add_parser("_console")
    x.add_argument("act", choices=("up", "down"))
    x.add_argument("label")
    x.add_argument("tabs", nargs="*")
    sub.add_parser("_revive")
    sub.add_parser("_answered")
    return ap


COMMANDS = {
    ("state", "init"): state_init_cmd, ("bolts", None): bolts_view, ("rail", None): rail_view,
    ("card", "preview"): card_preview, ("card", "session"): card_session, ("card", "wait"): card_wait, ("card", "end"): card_end, ("card", "sweep"): card_sweep,
    ("card", "read"): card_read, ("card", "answer"): batch_answer,
    ("record", None): record_status, ("answer", None): answer, ("fix", None): fix, ("main", "fix"): main_fix,
    ("role", "start"): role_start, ("role", "end"): role_end, ("role", "open"): role_open, ("role", "land"): role_land,
    ("bolt", "new"): direct(("bolt", "new")), ("bolt", "start"): direct(("bolt", "start")), ("bolt", "order"): direct(("bolt", "order")), ("bolt", "drop"): direct(("bolt", "drop")),
    ("bolt", "land"): bolt_land, ("bolt", "submit"): bolt_submit, ("bolt", "leave"): bolt_leave,
    ("unit", "add"): direct(("unit", "add")), ("unit", "split"): direct(("unit", "split")), ("unit", "amend"): direct(("unit", "amend")),
    ("unit", "order"): direct(("unit", "order")), ("unit", "after"): direct(("unit", "after")),
    ("unit", "move"): direct(("unit", "move")), ("unit", "drop"): direct(("unit", "drop")),
    ("chore", "add"): direct(("chore", "add")), ("chore", "order"): direct(("chore", "order")), ("chore", "after"): direct(("chore", "after")),
    ("chore", "move"): direct(("chore", "move")), ("chore", "drop"): direct(("chore", "drop")),
    ("kit", "rename"): direct(("kit", "rename")),
    ("_land-row", None): land_row_cmd, ("_land-card", None): land_card_cmd,
    ("_made", None): made_cmd, ("_batch-card", None): batch_card_cmd,
    ("_sweep", None): kit_sweep, ("_main", None): main_cmd,
    ("_review", None): review_cmd, ("review-delivered", None): review_delivered, ("_console", None): console_cmd, ("_revive", None): revive_cmd,
    ("_answered", None): card_answered,
    ("signal", None): signal, ("signal-move", None): signal_move,
    ("signal-show", None): signal_show, ("signal-land", None): signal_land,
    ("plan", "propose"): plan_propose, ("plan", "proposed"): plan_proposed,
    ("plan", "approve"): plan_approve, ("plan", "drop"): plan_drop, ("plan", "answer"): plan_answer,
}
# The commands on a main level and on a kit's host, each one process on the host it acts on.
HOST_COMMANDS = {(c, None) for c in ("_sweep", "_main", "_review", "_console", "_revive")} | {("drive", "set")}
# The act a command that moves work records, done or refused. A command that only reads records nothing.
ACTS = {
    ("state", "init"): "state.init", ("drive", "set"): "drive.set", ("bolt", "new"): "bolt.new", ("bolt", "start"): "bolt.start", ("bolt", "order"): "bolt.order",
    ("bolt", "drop"): "bolt.drop", ("bolt", "land"): "bolt.land", ("bolt", "leave"): "bolt.leave",
    ("unit", "add"): "unit.add", ("unit", "split"): "unit.split",
    ("unit", "amend"): "unit.amend",
    ("unit", "order"): "unit.order", ("unit", "after"): "unit.after", ("unit", "move"): "unit.move", ("unit", "drop"): "unit.drop",
    ("chore", "add"): "chore.add", ("chore", "order"): "chore.order", ("chore", "after"): "chore.after", ("chore", "move"): "chore.move",
    ("chore", "drop"): "chore.drop", ("kit", "rename"): "kit.rename",
    ("signal", None): "capture", ("signal-move", None): "signal.move", ("signal-land", None): "capture",
    ("plan", "propose"): "plan.propose", ("plan", "approve"): "plan.approve",
    ("plan", "drop"): "plan.drop", ("answer", None): "stage.answer", ("card", "preview"): "card.preview",
}


def named(a):
    """The objects a command names on its command line: a refusal's entry names those. A unit or chore is named by
    its command's kind."""
    kind = "chore" if a.cmd == "chore" else "unit"
    out = [f"{kind}/{a.unit}"] if getattr(a, "unit", None) else []
    for bolt in (a.bolt if isinstance(getattr(a, "bolt", None), list) else [getattr(a, "bolt", None)]):  # crew bolt submit names several
        if bolt and bolt != "queue":
            out.append(f"bolt/{bolt}")
    if a.cmd == "signal-move":
        out.append(f"signals/{a.signal}")
    if a.cmd == "signal-land" and crew.NAME.match(pathlib.Path(a.dir).name):
        out.append(f"signals/{pathlib.Path(a.dir).name}")
    if a.cmd == "state":
        out.append(f"plan/{a.label}")
    if a.cmd == "drive":
        out.append(f"drive/{a.label}")
    if a.cmd == "kit":
        out.append(f"kit/{a.old}")
    if a.cmd == "plan" and getattr(a, "n", None) is not None:
        out.append(f"proposal/{a.n}")
    if a.cmd in ("answer", "card") and CONTEXT.get("work"):  # the work as requests name it, once its launch or thing was found
        out.append(CONTEXT["work"])
    return out


def refused(fleet, a, key, e):
    """A refused command that would have moved work, in its drive's run record, with crew's reason."""
    label = CONTEXT.get("label") or getattr(a, "label", None) or crew.caller_label(fleet)
    if label in fleet["drives"]:
        record.emit(label, ACTS[key], named(a), refused=getattr(e, "recorded", None) or str(e))


def main(argv):
    if argv[:2] in (["signal", "move"], ["signal", "show"], ["signal", "land"], ["review", "delivered"]):  # beside crew signal <slug> "<asserts>"
        argv = [f"{argv[0]}-{argv[1]}"] + argv[2:]
    ap = parser(only=argv[0]) if argv and not argv[0].startswith("-") else None
    ap = ap if ap is not None and argv[0] in ap.built else parser()
    crew.answer_usage(ap, argv)
    need_recutils()
    args = ap.parse_args(argv)
    key = (args.cmd, getattr(args, "sub", None))
    # a landing is the user's send on its kit's landings card alone: these refuse whoever asks, before anything is read,
    # the teams file among it (crew-lands-each-bolt-through-flumes-base-place, Decisions 1 and 5)
    key != ("bolt", "submit") or fail(submit_refused(args.bolt or ()))
    not (key == ("main", "fix") and (args.send or args.excerpt is not None)) or fail(send_refused(args.kit, args.name))
    if key in HOST_COMMANDS:  # one process says what each of its steps did, in the order they did it
        sys.stdout.reconfigure(line_buffering=True)
    if key == ("drive", "set"):  # writes this host's own teams file, so it runs before any is loaded, and asks no may_write
        try:
            return drive_set(args)
        except Refusal as e:
            drive_set_refused(args, e)
            raise
    fleet = crew.load()
    try:
        may_write(fleet, key, args)
        COMMANDS[key](fleet, args)
    except Refusal as e:
        if key in ACTS:
            refused(fleet, args, key, e)
        raise


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Refusal as e:
        sys.exit(str(e))
    except Stopped as e:
        sys.exit(e.code)
