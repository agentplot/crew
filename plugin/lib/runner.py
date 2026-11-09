"""crew's side of the runner's interface (boomdrive core.2), and the decisions over a bolt's work given through
Flume: crew records a kit's work against its repository, and a runner whose configuration names that repository
takes it under a lease, while its host's stream has room, and launches it in Flume places on its host, in the stream
the host's Flume configuration maps the repository to (settled with the user 2026-11-01; Decision 4 of
the-team-machinery-leaves); crew names no stream, looks up no kit's host and models no account, and where it must say
or act where a kit's work runs, it reads what the runner reported for the work it took (taken, where).

crew asks the runners for work by requests on the drive's branch, requests.rec (REQUESTS), each appended in the
commit of the plan write that occasions it and checked by crew's own rules (request_refusal, append_refusal) as well as
recfix; each runner answers on a branch of its own, <label>/runner/<host>, which crew fetches with <label>/main and
reads (host_read) and never writes (state.5). A started piece's stage is read from its launch, the answer of the
runner that took it and Flume's status of its place as that runner carried it (stage_of, flume_facts), and shown with
its stream on every view (stream_said, piece_said).

A start launches its bolt whole, refused only where no runner answers for the partition (runnerless), and every plan
write reaches the places a started bolt launched as its own act: added work launched, dropped work dropped, a dependent
launched again when what it waits on is (reach), an amendment a retry of construct or a launch anew (amending), and a
move, split or change of After of launched work refused (launched_refusal); each launch's priority follows its bolt's
place in the plan (priorities).

A place that stopped short asking, or waits on its caller, is answered by a retry with the answer's words (answer_retry).
A fix on a started bolt is a launch of Flume's fix kind on the bolt's branch (fix_launch), dropped by a drop
(fix_drop_refusal), merged and waited on by Flume alone, and holds the bolt's landing while it is in flight
(fixes_in_flight); a started bolt whose landing sluice refused for a conflict with main takes main in by one
(take_main). A red main's fix is a launch of the fix kind on main with its submission held, taken by the runner that
keeps the kit (main_fix_launch); its kit's landings row carries it once its code has delivered and its submission
waits held (main_fixes_waiting), and the user's send of it is its kit's landings card's, carried to the runner as a land
of its launch (lands_due, sent_of).

A main-level role that runs as its kind has its run read from the runner's records (role_run), and its work that lands
is a launch of Flume's chore kind on its repository's default branch, the role's address its recipient (role_launch).

Each is a function of plain facts (code.7); plan.py, crew.py and hold.py read the facts and act on what they decide.
This module imports nothing outside the standard library and crew's own modules (code.1)."""
import json
import os
import re

def runnerless(label, tips):
    """Why a start is refused for want of a runner (Decision 5), or None: tips, the hosts whose runner branch the
    partition's state repository holds (plan.runner_tips); with none, no runner answers for the partition, so nothing
    would take the bolt's work."""
    if tips:
        return None
    return (f"no runner answers for {label}: its state repository holds no {runner_branch(label, '<host>')}, so nothing "
            "would take the bolt's work; a start waits for a runner (Boomdrive) to serve the partition")


REQUESTS = """\
# crew's requests of the runners: a launch of a Flume place for a started
# bolt's base place, its work, a fix or a role's work that lands, or a retry,
# drop, priority or land of a place launched.
# Written only by crew, each in the commit of the plan write that occasions it;
# numbered once, and never changed or removed. The runner whose configuration
# names a launch's Repo takes it, or for a role's the runner on its Host, and
# answers on <label>/runner/<host> of this repository, which crew reads and
# never writes.

%rec: Request
%doc: A request for Work: a launch of a Flume place of Kind named Name, cut from Base of Repo, taken by a runner whose configuration names Repo, in the stream its host maps it to, or by Host's runner in Stream for a role's work, a bolt's own launch its base place of crew's kind crew/bolt; or a retry, drop, priority or land of the place the launch Of names launched, taken by the runner that took it, a land the user's send of a bolt or a fix of main.
%key: Request
%type: Request,Of,After,Priority int
%type: Act enum launch retry drop priority land
%type: Kind regexp #^(change|chore|fix|crew/bolt)$#
%type: Hold enum submission
%type: Submission bool
%type: Host regexp /^[a-z0-9][a-z0-9-]*$/
%type: Date date
%mandatory: Request Act Work Date By
%allowed: Request Act Host Work Repo Kind Name Base Stream Priority Intent Recipient Hold After Brief Of Stage Submission Words Date By
"""
# A request's fields in the order requests.rec writes them (Decision 4's table).
FIELDS = ("Request", "Act", "Host", "Work", "Repo", "Kind", "Name", "Base", "Stream", "Priority", "Intent", "Recipient", "Hold",
          "After", "Brief", "Of", "Stage", "Submission", "Words", "Date", "By")
# What every request carries, and, by its act, what it must carry beside them and what else it may: a launch of a
# role's work names its Host and Stream, and a launch of a kit's work neither, and a bolt's own launch carries no Brief
# (request_refusal); a land names the launch it lands and nothing else (crew-lands-each-bolt-through-flumes-base-place,
# Decision 4).
COMMON = ("Request", "Act", "Work", "Date", "By")
ACTS = {
    "launch": (("Repo", "Kind", "Name", "Base", "Priority", "Intent", "Recipient", "Brief"), ("Hold", "After", "Host", "Stream")),
    "retry": (("Of",), ("Stage", "Submission", "Words")),
    "drop": (("Of",), ()),
    "priority": (("Of", "Priority"), ()),
    "land": (("Of",), ()),
}
# The kind of a bolt's own launch, its base place: crew's kind bolt@1, named by its source (record 0056; Decision 2).
BOLT_KIND = "crew/bolt"
# The work a request serves, as crew names it: a bolt's base place, a unit, a chore, a fix on a bolt or a fix of a
# kit's main, or a role's work that lands (Decision 10 of roles-run-as-flume-kinds).
WORK = re.compile(r"^(?:bolt/N|unit/N|chore/N|fix/N/N|fix/main/N/N|role/N/N)$".replace("N", "[a-z0-9][a-z0-9-]*"))


def needs(act, work):
    """What a request of act for work must carry beside COMMON (ACTS): a bolt's own launch, its base place, runs no
    agent and so carries no Brief."""
    need = ACTS[act][0]
    return tuple(f for f in need if f != "Brief") if act == "launch" and work.startswith("bolt/") else need


def number(v):
    """A record's number field as an int, None when it holds none or no number."""
    return int(v) if isinstance(v, str) and v.isdigit() else None


def next_request(requests):
    """The number the next request takes (Decision 4): one past the highest requests.rec holds, 1 for the first."""
    return max((number(r.get("Request")) or 0 for r in requests), default=0) + 1


def request_fields(n, act, work, given, date, by):
    """A request's fields in requests.rec's order (FIELDS), as (field, value): its number, act and work, what the
    command gives (given, {field: a value or a list of them, None or False for none and True written yes}), and when
    and by whom. A field FIELDS does not hold goes last, for request_refusal to name."""
    given = dict(given, Request=n, Act=act, Work=work, Date=date, By=by)
    out = []
    for f in list(FIELDS) + sorted(set(given) - set(FIELDS)):
        v = given.get(f)
        for x in v if isinstance(v, (list, tuple)) else [v]:
            if x is not None and x is not False:
                out.append((f, "yes" if x is True else str(x)))
    return out


def request_refusal(requests, new):
    """Why crew's own rules refuse a request (plan.1), beyond what recfix checks of requests.rec, or None: requests, the
    file's records before it, and new, the request appended, each a record of the plan's kind (plan.Rec). A request is
    the next by number; its work is a bolt's, a unit's, a chore's or a fix's as crew names them; it carries every field
    its act needs and none its act does not take; a launch of a role's work names the host and stream its role runs in,
    and a launch of a kit's work neither, a runner whose configuration names its repository taking it in the stream its
    host's Flume configuration maps the repository to (settled with the user 2026-11-01); a bolt's own launch, of
    bolt/<bolt>, names crew's kind crew/bolt and the base main, and no Brief or After, since its base place runs no
    agent, and no other launch names that kind, though no rule holds a bolt's pieces after its base place in the file,
    since a fix on a bolt started before bolts were base places, which has no launch of its own, is launched on its
    branch still (crew-lands-each-bolt-through-flumes-base-place, Decisions 3 and 9), and a start's order is its own
    (bolt_launch, reach); a retry, drop, priority or land names by Of a launch of the same work, and a land a launch of a bolt or
    of a fix of main; a launch's After names launches on the same base, the work of the same bolt; a fix of main holds
    its submission; and a retry starts a stage again or submits again, not both (Decision 4)."""
    n, act, work = new.get("Request"), new.get("Act"), new.get("Work")
    want = next_request(requests)
    if number(n) != want:
        return (f"request {n} is not the next in requests.rec: it holds "
                + (f"requests 1 to {want - 1}" if want > 2 else "request 1" if want == 2 else "none") + f", so the next is {want}")
    if act not in ACTS:
        return f"request {n} is a {act}, and a request is a launch, a retry, a drop, a priority or a land"
    need, may = needs(act, work or ""), ACTS[act][1] + (("Brief",) if act == "launch" and (work or "").startswith("bolt/") else ())
    missing = [f for f in COMMON + need if not new.get(f)]
    if missing:
        return (f"{act} {n} for {work} names no {' and no '.join(missing)}: a {act} carries "
                + ", ".join(COMMON + need))
    extra = sorted({f for f, _ in new.fields if f not in COMMON + need + may})
    if extra:
        return f"{act} {n} for {work} carries {', '.join(extra)}, which a {act} does not take"
    if not WORK.match(work):
        return (f"{act} {n} serves {work}, and a request serves bolt/<bolt>, unit/<unit>, chore/<chore>, fix/<bolt>/<name>, "
                "fix/main/<kit>/<name> or role/<role>/<name>")
    if act == "launch" and work.startswith("role/") and not (new.get("Host") and new.get("Stream")):
        return f"launch {n} of {work} names no Host or no Stream: a role's work runs on the host and in the stream its role runs in"
    if act == "launch" and not work.startswith("role/") and (new.get("Host") or new.get("Stream")):
        return (f"launch {n} of {work} names a Host or a Stream: a kit's work is taken by a runner whose configuration "
                "names its repository, in the stream its host's Flume configuration maps the repository to, and crew names neither")
    if act == "launch" and work.startswith("bolt/"):
        if new.get("Kind") != BOLT_KIND:
            return f"launch {n} of {work} names Kind {new.get('Kind')}: a bolt's base place is of crew's kind {BOLT_KIND}"
        if new.get("Base") != "main":
            return f"launch {n} of {work} names Base {new.get('Base')}: a bolt's base place is cut from main"
        if new.get("Brief"):
            return f"launch {n} of {work} names a Brief: a bolt's base place runs no agent, so it carries none"
        if new.all("After"):
            return (f"launch {n} of {work} names After {', '.join(new.all('After'))}: a bolt's base place lands after every "
                    "place on its branch, so it comes after no launch")
    if act == "launch" and not work.startswith("bolt/") and new.get("Kind") == BOLT_KIND:
        return f"launch {n} of {work} names Kind {BOLT_KIND}, which is a bolt's base place's alone, of bolt/<bolt>"
    by = {r.get("Request"): r for r in requests}
    if act != "launch":
        of = by.get(new.get("Of"))
        if of is None or of.get("Act") != "launch":
            return f"{act} {n} for {work} names request {new.get('Of')}, which is no launch" + (
                "" if of is not None else ": requests.rec does not hold it")
        if of.get("Work") != work:
            return f"{act} {n} for {work} names launch {of.get('Request')}, which is {of.get('Work')}'s"
        if act == "land" and not work.startswith(("bolt/", "fix/main/")):
            return (f"land {n} for {work} names launch {of.get('Request')}, which is no bolt's or fix of main's: a land is the "
                    "user's send of a bolt or of a fix of main")
    for a in new.all("After"):
        l = by.get(a)
        if l is None or l.get("Act") != "launch":
            return f"launch {n} of {work} comes after request {a}, which is no launch"
        if l.get("Base") != new.get("Base"):
            return (f"launch {n} of {work} on {new.get('Base')} comes after launch {a}, which is on {l.get('Base')}: an After "
                    "names work of the same bolt")
    if act == "launch" and work.startswith("fix/main/") and new.get("Hold") != "submission":
        return (f"launch {n} of {work} is a fix of main, which is launched with its submission held (Hold: submission) "
                "until the user's send (state.3)")
    if act == "retry" and new.get("Stage") and new.get("Submission"):
        return f"retry {n} of {work} names stage {new.get('Stage')} and the submission: a retry starts a stage again or submits again"
    return None


def append_refusal(before, after):
    """Why a write is refused for changing requests.rec other than by appending to it (Decision 4: a request is never
    changed or removed), or None: before and after, the file's records at the tip and as the write leaves them, each
    as its fields, a list of (field, value)."""
    for i, old in enumerate(before):
        n = dict(old).get("Request")
        if i >= len(after) or list(after[i]) != list(old):
            return (f"request {n} would be {'removed from' if i >= len(after) else 'changed in'} requests.rec, and a request "
                    "is never changed or removed: a later request retries, drops or reprioritises what it launched")
    return None


# ------------------------------------------------------------------------------------------ the runners' branches

def runner_branch(label, host):
    """The branch a host's runner answers a partition's requests on, in the partition's state repository (Decision 4)."""
    return f"{label}/runner/{host}"


# A runner's branch as crew reads it: each file and the record set it holds, written by the host's runner alone with
# these descriptors (boomdrive core.2), and never by crew (state.5). runner.rec names the host and the runner
# serving the partition there, so a branch that exists says a runner answers; answers.rec where each request it has
# read stands; places.rec Flume's status of each place it launched, `flume status --json <place>`'s answer on one line
# as Flume gave it (boomdrive core.1), kept after Flume tidies the place until its work has left crew's plan,
# and after those each role's latest run on the host, a Run record keyed by the role's address (R4 of
# roles-run-as-flume-kinds), with Flume's status of its place, or the runner's words where no run could be launched
# (boomdrive's the-runner-carries-crews-work-into-flume, Decision 14); and repositories.rec each repository its
# configuration keeps on the host, by its forge address with the folder of its clone, where Flume cuts its places
# (roles.9; the drive-state spec, "A kit's work is taken by a runner whose configuration names its repository"), a
# branch with none reporting no repositories.
RUNNER = """\
%rec: Runner
%key: Host
%type: Since date
%mandatory: Host Version Since
%allowed: Host Version Since
"""
ANSWERS = """\
%rec: Answer
%key: Request
%type: Request int
%type: Outcome enum held launched done refused
%type: At date
%mandatory: Request Outcome At
%allowed: Request Outcome Place Words At
"""
PLACES = """\
%rec: Place
%key: Request
%type: Request int
%type: At date
%mandatory: Request Place At Status
%allowed: Request Place At Status
"""
RUNS = """\
%rec: Run
%key: Address
%type: At date
%mandatory: Address At
%allowed: Address Place At Status Words
"""
REPOSITORIES = """\
%rec: Repository
%doc: A repository the runner keeps on its host: its forge address as its configuration names it, and the folder of its clone, where Flume cuts its places.
%key: Repository
%mandatory: Repository Folder
%allowed: Repository Folder
"""
FILES = {"runner.rec": "Runner", "answers.rec": "Answer", "places.rec": "Place", "repositories.rec": "Repository"}


def host_read(label, host, tip, files, refused):
    """A host's runner as crew reads it from its branch (Decision 4), from facts: tip, the branch's commit in crew's
    cache, None when no such branch exists; files, each of FILES parsed at the tip as the plan is (plan.Plan), None
    for one the tip lacks, answers and places then none; refused, recfix's words for each file it refused. Returns
    the reading, its host, branch and tip, with either why it could not be read, which hides this host's work alone
    (read.1, read.3), or the runner's record, each answer by its request's number and each place by its launch's: the
    place's path, when the runner carried it, and its Status parsed, or with why it could not be; each role's run
    by its address, likewise, with the runner's words where it could launch none; and the repositories it keeps, each
    one's folder by its forge address, None where the tip holds no repositories.rec, a runner that reports none
    (roles.9)."""
    branch = runner_branch(label, host)
    out = {"host": host, "branch": branch, "tip": tip, "why": None}
    if tip is None:
        return dict(out, why=f"no runner answers on {host}: {branch} does not exist")
    at = f"{branch} at {tip[:7]}"
    for name, kind in FILES.items():
        if name in refused:
            return dict(out, why=f"{host}'s runner can't be read: {at}: {refused[name]}")
        if files.get(name) is not None and files[name].recs(None):
            return dict(out, why=f"{host}'s runner can't be read: {at}: {name} holds a record before its %rec: {kind}")
    run = files["runner.rec"].recs("Runner") if files.get("runner.rec") is not None else []
    if len(run) != 1 or run[0].get("Host") != host:
        return dict(out, why=f"{host}'s runner can't be read: {at}: " + (
            "it holds no runner.rec" if files.get("runner.rec") is None else
            f"runner.rec holds {len(run)} Runner records, and names one" if len(run) != 1 else
            f"runner.rec names host {run[0].get('Host')}"))
    answers, places = {}, {}
    for name, kind, into in (("answers.rec", "Answer", answers), ("places.rec", "Place", places)):
        for r in files[name].recs(kind) if files.get(name) is not None else []:
            n = number(r.get("Request"))
            if n is None or n in into:
                return dict(out, why=f"{host}'s runner can't be read: {at}: {name} holds "
                            + ("a record with no request's number" if n is None else f"request {n} twice"))
            into[n] = r
    for n, r in places.items():
        try:
            status, why = json.loads(r.get("Status") or ""), None
        except ValueError as e:
            status, why = None, f"{at}: places.rec's status of the place of request {n} is no JSON ({e})"
        places[n] = {"place": r.get("Place"), "at": r.get("At"), "status": status, "why": why}
    runs = {}
    for r in files["places.rec"].recs("Run") if files.get("places.rec") is not None else []:
        a = r.get("Address")
        if not a or a in runs:
            return dict(out, why=f"{host}'s runner can't be read: {at}: places.rec holds "
                        + ("a run with no role's address" if not a else f"the run of {a} twice"))
        try:
            status, why = (json.loads(r.get("Status")) if r.get("Status") is not None else None), None
        except ValueError as e:
            status, why = None, f"{at}: places.rec's status of the run of {a} is no JSON ({e})"
        runs[a] = {"place": r.get("Place"), "at": r.get("At"), "status": status, "words": r.get("Words"), "why": why}
    kept = {}
    for r in files["repositories.rec"].recs("Repository") if files.get("repositories.rec") is not None else []:
        a = r.get("Repository")
        if not a or a in kept or not r.get("Folder"):
            return dict(out, why=f"{host}'s runner can't be read: {at}: repositories.rec holds " + (
                "a record with no repository's address" if not a else f"{a} twice" if a in kept else f"{a} with no folder"))
        kept[a] = r.get("Folder")
    return dict(out, runner=run[0], answers=answers, places=places, runs=runs,
                repositories=kept if files.get("repositories.rec") is not None else None)


def role_run(reading, address):
    """A role's latest run on a host as its runner's records show it (R4 of roles-run-as-flume-kinds), from host_read's
    reading and the role's address, <label>/<role>: whether it is live, its place, the runner's words where it could
    launch none, and why crew can't tell, the host's runner unread or the run's status no JSON (read.1). A run is live
    while its place reads live or making in Flume's status, as the runner judges a run that stands; one tidied, over,
    gone, refused or never launched is not."""
    if reading.get("why"):
        return {"live": None, "place": None, "words": None, "why": reading["why"]}
    r = reading["runs"].get(address)
    if r is None:
        return {"live": False, "place": None, "words": None, "why": None}
    if r["why"]:
        return {"live": None, "place": r["place"], "words": r["words"], "why": r["why"]}
    facts = flume_facts(r["status"], r["place"]) if r["status"] is not None else None
    return {"live": bool(facts) and facts["phase"] in ("live", "making"), "place": r["place"], "words": r["words"], "why": None}


def run_waiting(reading, address):
    """What a role's latest run on a host waits on its caller for, as Flume's status the runner carried shows it (Decision
    15 of roles-run-as-flume-kinds): (why, words, place), why as Flume's `waiting_on.why` names it, answer for a turn
    that stopped short and lost for one whose agent was lost, the words the stop-short's own where it has them, else
    Flume's; None for a run that waits on nothing, is not live, or that crew can't read, which role_run says why (read.1)."""
    r = None if reading.get("why") else reading["runs"].get(address)
    if r is None or r["why"] or r["status"] is None:
        return None
    f = flume_facts(r["status"], r["place"])
    if not f or f["phase"] != "live" or not f["waiting"]:
        return None
    return f["waiting"], text(f["end"].get("words")) or f["waiting_words"], r["place"]


def of_host(reads, label, host):
    """A host's reading among a partition's (host_read's, by host), or why none is: no runner branch for it exists."""
    return reads.get(host) or host_read(label, host, None, {}, {})


def takers(reads, n):
    """The runners that took request n, from the partition's runners as crew read them (reads, host_read's by host): (the
    readings whose answers hold it, the readings crew could not read), each by host."""
    return ([r for _, r in sorted(reads.items()) if not r["why"] and n in r["answers"]],
            [r for _, r in sorted(reads.items()) if r["why"]])


def taken(reads, n):
    """The runner that took request n (takers): (its reading, None) for the one whose answers hold it; (None, None)
    while none read holds it and every one was read, the request not taken yet; (None, why) when two hold it, or none
    read holds it and one could not be read, or no runner answers for the partition at all (read.1, read.3). crew names
    no host on a kit's launch: a runner whose configuration names its repository takes it (the user's ruling of
    2026-11-01)."""
    if not reads:
        return None, f"no runner answers for the partition: no <label>/runner/<host> branch exists, so nothing takes request {n}"
    hits, unread = takers(reads, n)
    if len(hits) > 1:
        return None, (f"request {n} was taken by the runners on {' and '.join(r['host'] for r in hits)}, whose configurations "
                      "each name its repository, so crew can't tell which place is its work")
    if hits:
        return hits[0], None
    if unread:
        return None, f"no runner crew read has taken request {n}, and " + "; ".join(r["why"] for r in unread)
    return None, None


def kept_folder(reading, kit, what):
    """The folder a host's runner keeps a kit's clone in, as its repositories.rec reports it (roles.9: where a kit lives
    on a host is its runner's report), from host_read's reading and the kit as the plan gives it (kit), matched by its
    name or forge address: (folder, None); (None, None) for a runner that reports no
    repositories, whose folder Flume's status of a place names (where); or (None, why) where it reports none by the
    kit's name, naming the host, what it keeps and the rename that may be why, or two by it (read.1). A kit named by
    its forge address is the repository of that address before any other of its name."""
    kept = reading.get("repositories")
    if kept is None:
        return None, None
    named = [a for a in kept if a.split("/")[-1] == kit.split("/")[-1]]
    found = [a for a in named if a == kit] or named
    if len(found) > 1:
        return None, (f"the runner on {reading['host']} keeps {' and '.join(found)} by the name {kit}, so crew can't tell "
                      f"which holds {what}'s work")
    if not found:
        return None, (f"the runner on {reading['host']} took {what}'s work and keeps no {kit}: it keeps "
                      + (", ".join(sorted(kept)) or "no repository") + f", so crew can't tell where {kit} is there; if "
                      f"{kit} was renamed on its host, crew kit rename {kit} <new> names it so in the plan")
    return kept[found[0]], None


def where(reads, launches, what, kit):
    """Where a runner reported taking work (the user's ruling of 2026-11-01; Decision 4), from the partition's runners as
    crew read them (reads), the launches of the work (launches, requests.rec's records, a bolt's on its branch or a
    kit's) and the kit as the plan gives it (kit): the host whose runner took the newest of them taken (takers); the
    kit's folder there as that runner's repositories.rec reports it (kept_folder), or, where it reports none, as
    Flume's status of the newest place it carries of them names it; and the stream its work runs in, as that status
    names it (roles.9); each None where it carries no place
    naming it yet; as ({"host", "dir", "stream"}, None); (None, None) while no runner has taken any of them and every
    runner was read; or (None, why) when none has and one could not be read, naming what (what) and that runner, two
    runners took the newest, or the one that did keeps no repository by the kit's name (read.1)."""
    unread = sorted({r["host"]: r["why"] for _, r in reads.items() if r["why"]}.items())
    for l in sorted(launches, key=lambda l: -(number(l.get("Request")) or 0)):
        hits, _ = takers(reads, number(l.get("Request")))
        if len(hits) > 1:
            return None, (f"crew can't tell where {what}'s work runs: request {l.get('Request')} was taken by the runners on "
                          f"{' and '.join(r['host'] for r in hits)}, whose configurations each name its repository")
        if not hits:
            continue
        reading = hits[0]
        folder, why = kept_folder(reading, kit, what)
        if why:
            return None, why
        mine = sorted((number(x.get("Request")) for x in launches if number(x.get("Request")) in reading["places"]), reverse=True)
        facts = [f for n in mine for p in [reading["places"][n]] if not p["why"] for f in [flume_facts(p["status"], p["place"])] if f]
        return {"host": reading["host"], "dir": folder or next((f["repository"] for f in facts if f["repository"]), None),
                "stream": next((f["stream"] for f in facts if f["stream"]), None)}, None
    return None, (f"no runner has reported taking {what}'s work yet, so crew can't tell where it runs"
                  + "".join(f"; {why}" for _, why in unread)) if unread else None


# ------------------------------------------------------------------------------------------- a name's branch

def kit_launches(requests, kit):
    """Every launch of a partition's work in a kit's repository, by its name or forge address, dropped or not, a role's
    left out: what the runners that took them report where the kit's work runs by (where)."""
    return [r for r in requests if r.get("Act") == "launch" and not (r.get("Work") or "").startswith("role/")
            and (r.get("Repo") or "").split("/")[-1] == kit.split("/")[-1]]


def launch_repositories(reads, launches, kit):
    """The repositories a launch of a kit's work would be made in, where Flume would cut its place and read whether
    its branch stands (flume 3), from the partition's runners as crew read them (reads, host_read's by host) and the
    kit's launches (kit_launches): the kit's folder where its work runs, as where reads it from the runner that took the
    newest of them, and the folder each runner's repositories.rec reports it keeps the kit in, since a runner whose
    configuration names the repository may take the launch; as ([{"host", "dir"}], None), each once. ([], None) while no
    runner has taken any of the kit's work and none reports keeping it: no launch of the partition's has cut a place
    of the kit, and crew can name no repository to read. ([], why) when crew can't tell (read.1): where's own why, the
    runner that took the kit's work carrying no place naming its folder, or one keeping two repositories by its name."""
    at, why = where(reads, launches, kit, kit)
    if why:
        return [], why
    if at and not at["dir"]:
        return [], (f"the runner on {at['host']} took {kit}'s work and carries no place of it naming the folder it keeps {kit} "
                    "in, so crew can't tell where a launch of it would be made")
    out = [{"host": at["host"], "dir": at["dir"]}] if at else []
    for reading in sorted(reads.values(), key=lambda r: r["host"]):
        kept = reading.get("repositories") or {}
        named = [a for a in kept if a.split("/")[-1] == kit.split("/")[-1]]
        found = [a for a in named if a == kit] or named
        if len(found) > 1:
            return [], (f"the runner on {reading['host']} keeps {' and '.join(found)} by the name {kit}, so crew can't tell "
                        "which a launch of its work would be made in")
        if found and {"host": reading["host"], "dir": kept[found[0]]} not in out:
            out.append({"host": reading["host"], "dir": kept[found[0]]})
    return out, None


def refs_standing(out, branches):
    """{branch: commit} of the branches among branches that stand, from `git for-each-ref --format='%(objectname)
    %(refname)'` over refs/heads/<branch> (out), which also lists a ref below one; a branch absent from it stands not."""
    refs = dict(reversed(line.split(" ", 1)) for line in out.splitlines() if " " in line)
    return {b: refs[f"refs/heads/{b}"] for b in branches if f"refs/heads/{b}" in refs}


def branch_refusal(kit, kind, names, found):
    """Why a unit or chore (kind) named one of names can't be planned in kit, or None (flume 3, 67): found, each
    repository a launch of it would be made in (launch_repositories) with the branches standing there, [{"host", "dir",
    "refs": refs_standing's}]. Flume refuses a launch whose place's branch (place_branch) stands, and keeps a dropped
    place's branch while it holds work, so the first name whose branch stands in any of them is refused, naming the
    branch, the folder and host it stands in and its commit, and the two ways on: the work proposed under a fresh name,
    or the branch removed first, which is the planner's or the user's to do, never crew's (read.4)."""
    for n in names:
        b = place_branch(f"{kind}/{n}")
        for r in found:
            c = r["refs"].get(b)
            if c:
                return (f"{kind} {n} can't be planned in {kit}: Flume's branch {b} stands in {r['dir']} on {r['host']}, at "
                        f"{c[:7]}, where a launch of {n} would make its place, and Flume refuses a launch that would make "
                        f"it again while it stands; propose the {kind} under a fresh name, or have the planner or the user "
                        f"remove the branch first, which may hold work and which crew never removes (git -C {r['dir']} "
                        f"branch -D {b}, on {r['host']})")
    return None


def drop_kept_said(kind, name, base):
    """What a drop of a unit or chore whose launch stands says, as it prints and on its entry (Note): Flume drops its
    place and keeps its branch while that holds work its base lacks (flume 67), and the name stays taken while the
    branch stands, since Flume refuses a launch that would make it again (flume 3; branch_refusal)."""
    b = place_branch(f"{kind}/{name}")
    return (f"Flume keeps {b} while it holds work {base} lacks, and the name {name} stays taken while that branch stands: "
            f"a {kind} added as {name} again is refused until the planner or the user removes it")


# ------------------------------------------------------------------------------------------- a crossed piece's stage

def launch_of(requests, work):
    """The launch a piece's stage is read from (Decision 8): the newest launch request of the work that no drop request
    names, None when it has none; requests in requests.rec's order."""
    dropped = {r.get("Of") for r in requests if r.get("Act") == "drop"}
    return next((r for r in reversed(requests)
                 if r.get("Act") == "launch" and r.get("Work") == work and r.get("Request") not in dropped), None)


def after_work(requests, launch):
    """The work each launch a launch comes after serves, as its waiting stage names it (Decision 5)."""
    by = {r.get("Request"): r for r in requests}
    return [by[a].get("Work") if a in by else f"request {a}" for a in launch.all("After")]


def at(d, *path):
    """The value at a path of keys in a JSON value, None where any step is absent or not an object (read.2)."""
    for k in path:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def tagged(v):
    """A Rust enum as Flume's JSON gives it (serde's external tag): its variant's name and its fields, ("name", {}) for
    a unit variant given as its name and ("name", fields) for one given as {name: fields}; (None, {}) for neither."""
    if isinstance(v, str):
        return v, {}
    if isinstance(v, dict) and len(v) == 1:
        (k, f), = v.items()
        return k, f if isinstance(f, dict) else {}
    return None, {}


def text(v):
    """A JSON string as text, None for anything else (read.2)."""
    return v if isinstance(v, str) else None


def flume_facts(status, place):
    """What crew reads of Flume's status of a place (Decision 8), as flume 0.3.6's `flume status --json <place>` gives it
    and the runner carried it (tests/py/flume-0.3.6/), each field guarded so one absent or of another shape reads None
    and never becomes text (read.2): the place's entry, the one at its path or, tidied, at <path>@<when>; its phase
    (live, making, over, gone or tidied) and, once its work is over, how (landed, dropped or done) and the commit it
    landed; its current stage, that stage's state and end; its tasks, ticked and in all; its submission: the merge
    queue's entry's number and state, why Flume could not read it, the pull request its last submit opened, how often
    it was submitted and sent back, the last verdict and its words, and whether it is held; what it waits on its caller
    for, the stage named, why, Flume's words and since when, in seconds, and whether it is stalled. None when status
    holds no entry for it. Each also names the folder of the place's repository on its host, and the stream it runs in,
    which say where the runner that took it keeps the kit (where)."""
    places = at(status, "status", "places")
    mine = [p for p in places if isinstance(p, dict) and isinstance(p.get("place"), str)
            and (p["place"] == place or p["place"].startswith(f"{place}@"))] if isinstance(places, list) and place else []
    if not mine:
        return None
    p = mine[-1]
    phase, pf = tagged(p.get("phase"))
    over, of = tagged(pf.get("over")) if phase in ("over", "gone", "tidied") else (None, {})
    current = text(p.get("current"))
    stage = next((s for s in p.get("stages") or [] if isinstance(s, dict) and s.get("name") == current), None) \
        if isinstance(p.get("stages"), list) else None
    tasks = p.get("tasks")
    tasks = (sum(1 for t in tasks if t["ticked"]), len(tasks)) if isinstance(tasks, list) and all(
        isinstance(t, dict) and isinstance(t.get("ticked"), bool) for t in tasks) else None
    sub = p.get("submission") if isinstance(p.get("submission"), dict) else {}
    read, rf = tagged(sub.get("read"))
    entry = at(rf, "submission") if read == "found" else None
    verdict, vf = tagged(sub.get("verdict"))
    count = lambda v: v if isinstance(v, int) and not isinstance(v, bool) else None
    waiting = p.get("waiting_on") if isinstance(p.get("waiting_on"), dict) else {}
    entry_state, ef = tagged(at(entry, "state"))
    return {
        "repository": text(p.get("repository")), "stream": text(at(p, "stream", "name")), "head": text(p.get("head")),
        "phase": phase, "over": over, "commit": text(of.get("commit")) if over == "landed" else None,
        "current": current, "state": text(at(stage, "state")), "end": at(stage, "end") if isinstance(at(stage, "end"), dict) else {},
        "tasks": tasks,
        "entry": text(at(entry, "id")), "entry_state": entry_state,
        "entry_base": text(ef.get("base")) if entry_state == "conflict" else None,
        "files": tuple(f for f in (vf.get("files") if isinstance(vf.get("files"), list) else ef.get("files") if isinstance(ef.get("files"), list)
                                   else []) if isinstance(f, str)) if verdict == "conflict" or entry_state == "conflict" else (),
        "unread": text(rf.get("reason")) if read == "could_not_read" else None,
        "request": text(sub.get("request")), "submits": count(sub.get("submits")), "send_backs": count(sub.get("send_backs")),
        "verdict": verdict, "verdict_words": text(vf.get("words")) or text(vf.get("reason")), "held": sub.get("held") is True,
        "waiting": text(waiting.get("why")), "waiting_stage": text(waiting.get("stage")), "waiting_words": text(waiting.get("words")),
        "waiting_since": count(waiting.get("since")), "stalled": p.get("stalled") is True,
    }


def stage_of(work, launch, answer, place, read, after=()):
    """A crossed piece's stage (Decision 8), from plain facts: work, as requests name it (bolt/<bolt>, unit/<u>,
    chore/<c>, fix/<bolt>/<name>, fix/main/<kit>/<name>); launch, its newest launch not dropped (launch_of), None for none;
    answer, the runner's answer to that launch, None while it has none; place, the runner's record of the place it
    launched (host_read's), None while it has none; read, True when its host's runner branch was read, else why not;
    after, the work its launch's After names (after_work). Returns {"stage", and what goes with it}: unknown, with why,
    for an unread host, no launch, or a fact crew can't read; launching while unanswered or unplaced, and while the
    runner holds a launch whose After names no work, with the runner's words, since the runner answers held for its
    claim of a launch (boomdrive's crew-control-plane, Decision 18) and for a stream with no room as well as for After
    work, so a launch with no After is never read as held for After work; waiting, on the work after names, while the
    runner holds a launch that names some; refused, with the runner's words; then from Flume's status: merged on
    a bolt and landed on main once its place landed, with the commit; dropped; queued for room; needs, with the agent's
    words, once its stage stopped short asking or found work; stalled, or else waits, with Flume's words and why, while
    it waits on its caller, the submission held among them; submitted, with sluice's number; its stage, with sluice's
    words, once sent back after a failed or conflicting submission; else its current stage. Each names its place, and
    a stage of a change its tasks, ticked and in all. A bolt's base place, bolt/<bolt>, is read as a piece of its own
    for the bolt's own row (crew-lands-each-bolt-through-flumes-base-place, Decision 3): unlaunched, with the runner's
    words, while its launch is unanswered, held or refused (refused then marked); live while its place is, since it has
    no stage, its landing read apart (landing_of); and landed, dropped or unknown as any piece's."""
    if read is not True:
        return {"stage": "unknown", "why": read}
    if launch is None:
        return {"stage": "unknown", "why": f"{work} has no launch in requests.rec"}
    n, outcome = launch.get("Request"), answer.get("Outcome") if answer is not None else None
    if work.startswith("bolt/") and outcome in (None, "held", "refused"):
        return dict({"stage": "unlaunched"}, **({"words": answer.get("Words")} if answer is not None and answer.get("Words") else {}),
                    **({"refused": True} if outcome == "refused" else {}))
    if answer is None:
        return {"stage": "launching"}
    if outcome == "held" and not launch.all("After"):
        return dict({"stage": "launching"}, **({"words": answer.get("Words")} if answer.get("Words") else {}))
    if outcome == "held":
        return {"stage": "waiting", "after": list(after)}
    if outcome == "refused":
        return {"stage": "refused", "words": answer.get("Words")}
    if outcome != "launched":
        return {"stage": "unknown", "why": f"the runner answered launch {n} of {work} {outcome}, and a launch is answered held, launched or refused"}
    if place is None:
        return {"stage": "launching", "place": answer.get("Place")}
    res = {"place": place["place"]}
    if place.get("why"):
        return dict(res, stage="unknown", why=place["why"])
    f = flume_facts(place["status"], place["place"])
    if f is None:
        return dict(res, stage="unknown", why=f"Flume's status of {work}'s place, as the runner carried it, holds no place {place['place']}")
    if f["tasks"] is not None:
        res["tasks"] = f["tasks"]
    if f["over"] == "landed":
        return dict(res, stage="landed" if launch.get("Base") == "main" else "merged", commit=f["commit"])
    if f["over"] == "dropped":
        return dict(res, stage="dropped")
    if f["phase"] == "making":
        return dict(res, stage="launching")
    if f["phase"] != "live":
        said = f"Flume's status of {work}'s place {place['place']}"
        return dict(res, stage="unknown", why=(
            f"{said} says its work is {f['over']}, and a place of a kind that lands ends landed or dropped" if f["over"] else
            f"{said} gives phase {f['phase']}, which crew does not read" if f["phase"] else f"{said} gives no phase crew reads"))
    if work.startswith("bolt/"):
        return dict(res, stage="live")
    if f["state"] == "waiting_for_room":
        return dict(res, stage="queued", of=f["current"])
    if f["waiting"] == "answer":
        return dict(res, stage="needs", of=f["waiting_stage"] or f["current"], words=text(f["end"].get("words")) or f["waiting_words"],
                    found=f["end"].get("needs") == "found_work", stalled=f["stalled"])
    if f["waiting"]:
        return dict(res, stage="stalled" if f["stalled"] else "waits", of=f["waiting_stage"], why=f["waiting"], words=f["waiting_words"],
                    held=f["held"] and not f["waiting_stage"])
    if f["entry_state"] in ("waiting", "under_test", "landed") or (f["request"] and f["entry"] is None and f["submits"]):
        return dict(res, stage="submitted", submission=f["entry"] or f["request"])
    if f["unread"] and f["submits"]:
        return dict(res, stage="unknown", why=f"Flume could not read {work}'s submission: {f['unread']}")
    if f["current"] is None:
        return dict(res, stage="unknown", why=f"Flume's status of {work}'s place {place['place']} names no current stage")
    if f["send_backs"] and f["verdict"] in ("failed", "conflict"):
        return dict(res, stage=f["current"], words=f["verdict_words"], sent_back=f["send_backs"], verdict=f["verdict"])
    return dict(res, stage=f["current"])


def legacy_said(bolt):
    """What every view says of a started bolt with no launch of bolt/<bolt> (crew-lands-each-bolt-through-flumes-base-place,
    Decision 9): sluice made its branch before bolts were base places, and it lands under the crew that started it."""
    return f"{bolt} was started before bolts were base places and lands under the crew that started it"


def base_said(s):
    """A bolt's base place's stage (stage_of of bolt/<bolt>) as its head line says it, or "" while it reads live or has
    landed, when its landing says the rest (landing_of): unlaunched with the runner's words, refused or held, or that no
    runner has answered it yet; launching while the runner has carried none of Flume's status of it; dropped; or why
    crew can't tell."""
    st = s.get("stage")
    first = (s.get("words") or "").strip().splitlines()[0] if (s.get("words") or "").strip() else ""
    if st == "legacy":
        return s.get("words") or ""
    if st == "unlaunched":
        return ("its base place is unlaunched: " + ("the runner refused its launch" if s.get("refused") else
                "the runner holds its launch" if first else "no runner has answered its launch yet")
                + (f": {first}" if first else "") + ("; crew bolt start runs it again" if s.get("refused") else ""))
    if st == "launching":
        return "its base place is launching"
    if st == "dropped":
        return "its base place is dropped"
    if st == "unknown":
        return f"can't tell its base place: {s.get('why')}"
    return ""


def place_branch(work):
    """The branch Flume cuts a unit's or chore's place on, as Flume's status names it (`branch`): <kind>/<name>, the
    kind and name its launch gives (reach), a unit's kind change; the same whichever partition's launch made the place,
    since it is the work's own name and carries no partition's (crew record 0055, rejected). None for a fix or a role's
    work, which the bolt's landings do not build."""
    kind, _, name = work.partition("/")
    return f"{'change' if kind == 'unit' else kind}/{name}" if kind in ("unit", "chore") and name else None


def built_on_bolt(work, s, landings):
    """A started piece's stage as its bolt's branch holds it (crew record 0056 decision 2; read.1, read.2), from facts:
    work, as requests name it; s, its stage as the runner's records give it (stage_of); landings, the branches the
    landings sluice made on its bolt name (gather.bolt_landings), None where they could not be read. Once a landing
    names its place's branch (place_branch), the piece is merged at that landing's commit, whatever the runner reports
    of its place: launching, refused because the bolt already holds its change, submitted, tidied or unknown, and
    whichever partition's launch made the place, keeping the place and tasks the runner gave; on (bolt) says it was read
    from the bolt, landed its landing's time. s as given where no landing names it, the landings could not be read, or
    the runner already reads it merged or landed at a commit, which is that landing's (Flume's landed commit)."""
    landing = (landings or {}).get(place_branch(work) or "")
    if not landing or (s["stage"] in ("merged", "landed") and s.get("commit")):
        return s
    kept = {k: s[k] for k in ("place", "tasks") if s.get(k)}
    return dict(kept, stage="merged", commit=landing["commit"], landed=landing["at"], on="bolt", branch=place_branch(work))


def verification(head, pieces):
    """A bolt's verification (record 0025 point 4, crew record 0056 points 1 and 4; read.1, read.2), from plain facts:
    head, the bolt's head as read where the bolt lives (gather.bolt_read), None where there is none; pieces, its units,
    chores and fixes as [(work, s)], work as requests name it and s its stage as stage_of or built_on_bolt gives it.
    Returns (state, words): "green", naming the head and the work, for the first piece in the order given that reads
    merged or landed with its commit the head, since every piece lands on its bolt through a submission sluice lands
    only on its required checks passing, or beside its queue when none of them reads its changes (teams.5, sluice
    clause 140), so a head that is a piece's landing is one the kit's checks passed, a landing beside reading the same;
    "none" for any other head, a commit pushed another way or a landing the runner does not report among them; and
    "unknown" with no head. A piece with no commit matches nothing, and the commits compare whole."""
    if not head:
        return "unknown", "no head crew can read"
    for work, s in pieces:
        if s.get("stage") in ("merged", "landed") and s.get("commit") and s["commit"] == head:
            how = "as its landing on the bolt names it" if s.get("on") == "bolt" else "as the runner reports it"
            return "green", f"its head {head[:7]} is {bare(work)}'s landing, {how}"
    return "none", f"its head {head[:7]} is no landing of its work that the runner reports"


def working(reading):
    """The places a host's runner carries Flume's status of whose current stage is working, begun with its phase live
    (flume_facts), from reading, host_read's, read: (each place's folder name, in its launches' order, None), or (None,
    why one of them can't be read) (read.1)."""
    out = []
    for n, p in sorted((reading.get("places") or {}).items()):
        if p.get("why"):
            return None, p["why"]
        f = flume_facts(p.get("status"), p.get("place"))
        if f is not None and f["phase"] == "live" and f["state"] == "begun":
            out.append(os.path.basename(p["place"].rstrip("/")))
    return out, None


# --------------------------------------------------------------------------- a bolt given through Flume as it is shown

def stream_said(stream):
    """The Flume stream a started bolt's work runs in, in the words of its head line (Decision 14), as Flume's status
    of its places names it (where); nothing while crew reads none."""
    return f"in Flume stream {stream}" if stream else ""


def bare(work):
    """A piece of work as a line names it: a unit or chore by its own name, a fix by its place's, <bolt>--<name>."""
    kind, _, rest = work.partition("/")
    return rest.replace("/", "--", 1) if kind == "fix" else rest if kind in ("unit", "chore") else work


def piece_said(s):
    """A crossed piece's stage (stage_of) as its line in crew bolts and the board says it (Decision 14): (its stage, as
    today's piece's word, with the tasks of a stage that has them and sluice's number of a submission; what goes with
    it, or ""): the work it waits on; the question it stopped short with, or the work it found; sluice's words it was
    sent back with; Flume's words of what it waits on its caller for, its held submission waiting on the user's send;
    the room it is queued for; the runner's words refusing it, or holding a launch with no After work; or why crew
    can't tell its stage; and, for one read merged from its bolt's landing (built_on_bolt), the branch and commit
    that landing names."""
    st = s["stage"]
    tasks = f" {s['tasks'][0]}/{s['tasks'][1]}" if s.get("tasks") and s["tasks"][1] and st in ("code", "verify") else ""
    stage = f"submitted #{s['submission']}" if st == "submitted" and s.get("submission") else st + tasks
    first = (s.get("words") or "").strip().splitlines()[0] if (s.get("words") or "").strip() else ""
    detail = (
        "on " + ", ".join(bare(w) for w in s.get("after", [])) if st == "waiting" else
        (f"found at {s.get('of')}: {first}" if s.get("found") else f"asks at {s.get('of')}: {first}") if st == "needs" else
        f"sent back by sluice: {first}" if s.get("sent_back") else
        "its submission waits held for the user's send" if st in ("waits", "stalled") and s.get("held") else
        f"waits on its caller at {s.get('of') or 'its submission'}: {first or s.get('why') or 'no words'}" if st in ("waits", "stalled") else
        f"for room at {s['of']}" if st == "queued" and s.get("of") else
        f"refused by the runner: {first or 'no words'}" if st == "refused" else
        f"held by the runner: {first}" if st == "launching" and first else
        f"{s.get('branch')} landed on its bolt at {(s.get('commit') or '')[:7]}" if st == "merged" and s.get("on") == "bolt" else
        s.get("why") or "" if st == "unknown" else "")
    return stage, detail


# ------------------------------------------------------------------------------------- a started bolt's launches

def work_of(u):
    """How a request names a unit or chore of the plan (Decision 4): unit/<unit>, or chore/<chore> for one marked
    Kind: chore (plan.11)."""
    return f"{'chore' if u.get('Kind') == 'chore' else 'unit'}/{u.name()}"


def brief(u):
    """A launch's brief for a unit or chore (Decision 5): the work's own words, less what the stage itself is told,
    which is its kind's: a unit's intent with its sources, and a chore's words."""
    sources = u.all("Source") if u.get("Kind") != "chore" else []
    return (u.get("Intent") or "") + (" Sources: " + "; ".join(sources) + "." if sources else "")


def priority_of(plan, bolt):
    """A crossed bolt's priority (Decision 6): its place among the plan's bolts given through Flume (Path: flume),
    counted from the end, so the first in the plan's order has the highest and Flume starts its waiting stages first
    (flume record 0010); None for a bolt not given through Flume, or gone from the plan."""
    given = [b.name() for b in plan.bolts() if b.get("Path") == "flume"]
    return len(given) - given.index(bolt) if bolt in given else None


def standing(requests):
    """The launches no drop names, in requests.rec's order."""
    dropped = {r.get("Of") for r in requests if r.get("Act") == "drop"}
    return [r for r in requests if r.get("Act") == "launch" and r.get("Request") not in dropped]


def built_order(work):
    """A bolt's work in the order its launches are numbered (Decision 5): the file's order, but each after the work its
    After names, so a dependent's After names launches written before it. A cycle, which crew's rules refuse (plan.1),
    leaves the rest in the file's order."""
    names, order, placed = {u.name() for u in work}, [], set()
    while len(order) < len(work):
        u = next((u for u in work if u.name() not in placed and all(d in placed or d not in names for d in u.all("After"))),
                 next(u for u in work if u.name() not in placed))
        order.append(u)
        placed.add(u.name())
    return order


def bolt_launch(plan, bolt, label):
    """The launch of a started bolt's base place (crew-lands-each-bolt-through-flumes-base-place, Decision 3), as (act,
    work, its fields as plan.request takes them): a place of crew's kind crew/bolt named the bolt, cut from main, in
    the bolt's repository as the plan names it, for a runner whose configuration names it to take in the stream its
    host maps it to, at the bolt's priority (priority_of), its intent the bolt's, main-level ops as its recipient,
    since what follows a landing is ops's (plan.16), and no Brief, since a base place runs no agent, and no After, since
    it lands after every place on its branch. A start appends it before its pieces' launches (reach)."""
    return ("launch", f"bolt/{bolt}", {
        "Repo": plan.bolt(bolt).get("Repo"), "Kind": BOLT_KIND, "Name": bolt, "Base": "main",
        "Priority": priority_of(plan, bolt), "Intent": f"{label}/{bolt}", "Recipient": f"{label}/ops"})


def restart(plan, requests, reads, bolt, label):
    """What crew bolt start appends for a started bolt whose own launch the runner refused, as Flume refuses it while
    its host has not locked crew/bolt@1 (crew-lands-each-bolt-through-flumes-base-place, Decision 3; bolt-teams "A
    start run again launches a bolt whose launch the runner refused"), from facts: plan, as the write leaves it;
    requests, requests.rec's records before it; reads, the partition's runners as crew read them (host_read's, by
    host). Returns (the requests to append, each (act, work, its fields), None): a drop of each of its pieces' launches
    standing that the runner has not answered launched, then a launch anew of its base place (bolt_launch), its pieces
    following by reach; or (None, why) for any other started bolt: one with no launch of its own, started before bolts
    were base places (Decision 9), one whose launch is unanswered, held or launched, and one whose launch, or a piece's,
    crew can't tell the runner's answer to (read.1)."""
    started = f"bolt {bolt} is started already"
    own = launch_of(requests, f"bolt/{bolt}")
    if own is None:
        return None, f"{started}, before bolts were base places, and lands under the crew that started it"
    n = number(own.get("Request"))
    reading, why = taken(reads, n)
    if why:
        return None, f"{started}, and crew can't tell whether the runner refused its launch: {why}"
    answer = reading["answers"].get(n) if reading else None
    if answer is None or answer.get("Outcome") != "refused":
        return None, started
    drops = []
    for l in standing(requests):
        if l.get("Base") != f"bolt/{bolt}":
            continue
        m = number(l.get("Request"))
        r, why = taken(reads, m)
        if why:
            return None, f"{started}, and crew can't tell whether {l.get('Work')}'s launch was launched: {why}"
        if r is None or (r["answers"].get(m) or {}).get("Outcome") != "launched":
            drops.append(("drop", l.get("Work"), {"Of": l.get("Request")}))
    return drops + [bolt_launch(plan, bolt, label)], None


def reach(plan, requests, bolt, label, again=()):
    """What a plan write asks of the runners for a started bolt (Decisions 5 and 7), as the requests to append in order,
    each (act, work, its fields as plan.request takes them), from facts: plan, as the write leaves it; requests,
    requests.rec's records before them; label, the bolt's partition; again, the work (as requests name it) whose launch
    is dropped and launched anew, an amendment of a unit whose place is not launched. Each unit and chore of the bolt
    with no launch standing is launched, as a start launches them: in the file's order, each after the work its After
    names, cut from the bolt's branch, carrying the bolt's repository as the plan names it, for a runner whose
    configuration names it to take in the stream its host maps it to (the user's ruling of 2026-11-01), the bolt's priority, its
    intent, the planner as recipient, its brief, and the launches of its After work; a launch standing whose After no longer names
    its After work's standing launches, one of them dropped, launched anew or gone from its After, is dropped and the
    work launched again, so no place waits on a launch that will never land; and each unit's or chore's launch on the
    bolt whose work has left it is dropped, every launch on the bolt's branch, its fixes' too, once the bolt has left
    the plan. The drops come first, numbered from the next request, then the launches."""
    base = f"bolt/{bolt}"
    on = [r for r in standing(requests) if r.get("Base") == base]
    newest = {r.get("Work"): r for r in on}
    work = plan.work_of(bolt) if plan.bolt(bolt) is not None else []
    names = {u.name(): work_of(u) for u in work}
    order = built_order(work)
    fresh = set()
    for u in order:
        wk, l, deps = names[u.name()], newest.get(names[u.name()]), [d for d in u.all("After") if d in names]
        if l is None or wk in again or any(names[d] in fresh for d in deps) or \
                sorted(l.all("After")) != sorted(newest[names[d]].get("Request") for d in deps):
            fresh.add(wk)
    left = [r for r in on if r.get("Work") not in names.values()
            and (plan.bolt(bolt) is None or r.get("Work").startswith(("unit/", "chore/")))]
    drops = [r for r in on if newest[r.get("Work")] is not r or r.get("Work") in fresh or r in left]
    out = [("drop", r.get("Work"), {"Of": r.get("Request")}) for r in drops]
    n, num = next_request(requests) + len(out), {}
    for u in order:
        wk = names[u.name()]
        if wk not in fresh:
            num[u.name()] = number(newest[wk].get("Request"))
            continue
        num[u.name()], n = n, n + 1
        out.append(("launch", wk, {
            "Repo": plan.bolt(bolt).get("Repo"), "Kind": "chore" if u.get("Kind") == "chore" else "change", "Name": u.name(),
            "Base": base, "Priority": priority_of(plan, bolt), "Intent": f"{label}/{bolt}", "Recipient": f"{label}/planner",
            "After": [num[d] for d in u.all("After") if d in num], "Brief": brief(u)}))
    return out


def priorities(plan, requests):
    """The priority requests a write that launches or reorders bolts appends (Decision 6): [(launch, its priority now)]
    for each launch standing on a bolt given through Flume whose priority, its bolt's place in the plan now
    (priority_of), differs from the last its requests set, its launch's or a later priority's; none for a fix of main,
    or a bolt gone from the plan."""
    last = {}
    for r in requests:
        if r.get("Act") == "launch" or (r.get("Act") == "priority" and r.get("Of") in last):
            last[r.get("Request") if r.get("Act") == "launch" else r.get("Of")] = r.get("Priority")
    out = []
    for r in standing(requests):
        base = r.get("Base") or ""
        p = priority_of(plan, base[len("bolt/"):]) if base.startswith("bolt/") else None
        if p is not None and str(p) != last.get(r.get("Request")):
            out.append((r, p))
    return out


def amending(work, launch, answer, place, read):
    """How an approved amendment of a started bolt's unit reaches its place (Decision 7), from the facts stage_of takes:
    ("again", None) while its launch is held, refused or unanswered, or it has none, its launch dropped and the unit
    launched anew with the amended intent; ("retry", None) once its place is launched, construct started again with
    the amendment's words, the place's later stages then running again as Flume runs its kind through (plan.15);
    ("refused", why) when crew can't tell which, its host's runner or its place unread (read.1), or its place has
    merged, landed or been dropped, which is not amended (plan.6)."""
    outcome = answer.get("Outcome") if answer is not None else None
    if launch is None or (read is True and outcome != "launched"):
        return "again", None
    s = stage_of(work, launch, answer, place, read)
    if s["stage"] == "unknown":
        return "refused", f"can't tell how far {work}'s place has got, so the amendment can't reach it: {s['why']}"
    if s["stage"] in ("merged", "landed", "dropped"):
        how = {"merged": "merged into its bolt", "landed": "landed on main", "dropped": "been dropped"}[s["stage"]]
        return "refused", f"{work}'s place {s['place']} has {how}, so it is not amended: a defect in it is a fix, and new work is a new unit"
    return "retry", None


def launched_refusal(requests, work, how):
    """Why a move out of a bolt given through Flume, a split, or a change of After is refused for work whose launch is
    written (Decision 7), or None while none stands: a place's base and order are fixed at its launch, so the way on is
    to drop the work and add it again as it should be. how says what the write would do to it."""
    l = launch_of(requests, work)
    if l is None:
        return None
    kind, name = work.split("/", 1)
    return (f"{kind} {name} is launched as Flume place {l.get('Name')} on {l.get('Base')} (request {l.get('Request')}), whose "
            f"base and order are fixed at its launch, so it is not {how}: drop it (crew {kind} drop {name}) and add it "
            f"again as it should be (crew {kind} add)")


# ------------------------------------------------------------------------------------------ answers and fixes

def piece_stage(requests, reads, launch):
    """A launch's piece's stage (stage_of), from requests.rec's records and the partition's runners as crew read them
    (reads, host_read's by host): the answer of the runner that took the launch (taken) and its record of the place
    launched; launching while none has taken it, and unknown where crew can't tell which did."""
    n = number(launch.get("Request"))
    reading, why = taken(reads, n)
    answer, place = (reading["answers"].get(n), reading["places"].get(n)) if reading else (None, None)
    return stage_of(launch.get("Work"), launch, answer, place, why or True, after_work(requests, launch))


def named_launch(requests, work):
    """The launch standing for the work a command names (Decision 9), as (launch, None), or (None, why): named as
    requests name it (unit/<u>, chore/<c>, fix/<bolt>/<name>, fix/main/<kit>/<name>), by its place's name (<u>,
    <bolt>--<name>, main--<name>), or a unit or chore by its own name. None stands for work Flume
    does not build, and a name two works answer to is said with both."""
    hits = {r.get("Work"): r for r in standing(requests)
            if work in (r.get("Work"), r.get("Name")) or r.get("Work") in (f"unit/{work}", f"chore/{work}")}
    if not hits:
        return None, (f"no launch of {work} stands in requests.rec, so no Flume place of it waits on an answer: crew answer "
                      "answers a place of work Flume builds, by its unit's, chore's or place's name")
    if len(hits) > 1:
        return None, f"{work} names {' and '.join(sorted(hits))}: name the one meant as requests.rec does"
    return next(iter(hits.values())), None


def stage_said(s):
    """A crossed piece's stage (stage_of) in a few words, for a refusal to name."""
    st = s["stage"]
    return {"launching": "launching", "waiting": "held for its After work", "refused": "refused by the runner",
            "queued": f"queued for room at {s.get('of')}", "submitted": f"submitted to sluice ({s.get('submission')})",
            "merged": "merged", "landed": "landed", "dropped": "dropped"}.get(st, f"at {st}")


def answer_retry(work, s):
    """What crew answer asks of a crossed piece's place (Decision 9), from its stage as stage_of gives it: ("stage", the
    stage) to start again with the words, for a place whose stage stopped short asking or that waits on its caller to
    retry a stage, stalled or not; ("submission", None) to submit again with them, for one whose submission waits on its
    caller and is not held; else (None, why), naming its stage: crew can't tell it (read.1), since its stage is unknown
    or it is launching, the runner having carried no status of its place in Flume, holding its launch or not having
    answered it, so no reading says it waits on nothing; its submission waits held for the user's send, which no answer
    gives (state.3); or it neither stopped short nor waits on its caller. A stop-short whose agent Flume keeps open for
    its answer reads needs like any other, and its retry naming the stage is that answer, reaching the session kept
    open as a tell answering it does (flume 42, 49, 198)."""
    st, place = s["stage"], f"{work}'s place" + (f" {s['place']}" if s.get("place") else "")
    if st == "unknown":
        return None, f"can't tell whether {work}'s place waits on an answer: {s['why']}"
    if st == "launching":
        return None, f"can't tell whether {place} waits on an answer: " + (
            "the runner that took it has carried none of Flume's status of it yet" if s.get("place") else
            f"the runner holds its launch, in its words: {s['words']}" if s.get("words") else
            "no runner has answered its launch yet")
    if st == "needs" or (st in ("waits", "stalled") and s.get("of")):
        return "stage", s["of"]
    if st in ("waits", "stalled") and s.get("held"):
        send = "crew main fix {} {} --send".format(*work.split("/")[2:]) if work.startswith("fix/main/") else "its send"
        return None, (f"{place} has delivered, and its submission waits held for the user's send, which no answer gives: "
                      f"{send}, on the user's word")
    if st in ("waits", "stalled"):
        return "submission", None
    return None, (f"{place} is {stage_said(s)}, with no question and nothing it waits on its caller for, so there is nothing "
                  "to answer: crew bolts shows its stage")


def fix_launch(plan, requests, bolt, label, name, words):
    """The launch crew fix <bolt> <name> "<words>" appends for a fix on a started bolt (Decision 10), as (act, work, its
    fields as plan.request takes them), or (None, why): a place of the fix kind named <bolt>--<name>, cut from the
    bolt's branch, in the bolt's repository for a runner whose configuration names it to take, as reach launches its
    units, with the bolt's priority and its partition's (label) intent, the planner as recipient, the fix's words as its
    brief and nothing held. Refused while a launch of that fix stands on the bolt, merged or not, since the name is in
    use there (teams.3)."""
    work, base = f"fix/{bolt}/{name}", f"bolt/{bolt}"
    l = launch_of(requests, work)
    if l is not None:
        return None, (f"fix {name} is in use on bolt {bolt}: it is launched as Flume place {l.get('Name')} (request "
                      f"{l.get('Request')}), so name this fix differently")
    return ("launch", work, {
        "Repo": plan.bolt(bolt).get("Repo"), "Kind": "fix", "Name": f"{bolt}--{name}", "Base": base,
        "Priority": priority_of(plan, bolt), "Intent": f"{label}/{bolt}", "Recipient": f"{label}/planner", "Brief": words}), None


def take_main_name(main, request=None):
    """A take-main fix's name: take-main-<main's revision, seven>, or, where the merge queue recorded no revision of main,
    take-main-l<the land's request>, so each conflict read launches its fix once."""
    return f"take-main-{main[:7]}" if main else f"take-main-l{request}"


def take_main(plan, requests, bolt, label, main, words, request=None):
    """The launch of a crossed bolt's take-main fix (Decision 10, plan.8), once sluice refused its landing for a
    conflict with main at main (its revision): a fix as fix_launch makes it, named take-main-<main, seven>, its brief
    saying to take origin/main into the bolt and resolve, with sluice's words of the conflict, and beginning as every
    take-main fix's does, so the bolt's row says it takes main first (plan.TAKE_MAIN); None while a fix of that name
    stands on the bolt, so a refusal read twice launches it once."""
    name = take_main_name(main, request)
    if launch_of(requests, f"fix/{bolt}/{name}") is not None:
        return None
    return fix_launch(plan, requests, bolt, label, name, (
        f"Take main into the bolt: merge origin/main" + (f", at {main[:7]}," if main else "") + f" into this place, cut from "
        f"bolt/{bolt}, resolving each conflicting path keeping both intents, main's and the bolt's; the merge queue refused "
        f"the bolt's landing for its conflict with main: {words}"))[0]


def fix_drop_refusal(of, work, launch, s):
    """Why crew fix --drop of a fix on a started bolt, or crew main fix --drop of a fix of main, is refused (Decisions
    10 and 11, teams.3), or None to drop the launch standing: none stands, so what it would fix (of, bolt <bolt> or the
    kit) has no such fix; crew can't tell how far its place got (read.1); or its place has merged into its base, so
    what it changed is the bolt's, or main's, and a new fix undoes it. s, its stage (piece_stage)."""
    if launch is None:
        return f"{of} has no fix {work}: no launch of it stands in requests.rec"
    if s["stage"] == "unknown":
        return f"can't tell whether {work}'s place has merged into {launch.get('Base')}, so it is not dropped: {s['why']}"
    if s["stage"] in ("merged", "landed"):
        return (f"{work} has merged into {launch.get('Base')}, so it is not dropped: what it changed is "
                f"{'main' if launch.get('Base') == 'main' else 'the bolt'}'s, and a new fix undoes it")
    return None


def unlanded(bolt, kit, work, held):
    """Why a bolt given through Flume is not closed as landed (Decision 12), or None, from facts: work, each of its
    units and chores as (name, kind, its stage as stage_of gives it, with the commit its place landed at on the bolt);
    held, {commit: git's exit asking whether the kit's main now holds it, 0 yes, 1 no, any other git could not tell}.
    Its close reads each piece merged from the runner's records where today's reads a change archived or a chore's
    trailer on main, a Flume chore's commits carrying no crew trailer, and lands once main holds the commit each place
    landed at on the bolt, so a bolt sluice has not landed is not closed; a piece crew can't tell is not taken as
    landed (read.1)."""
    for name, kind, s in work:
        if s["stage"] == "unknown":
            return f"cannot tell whether {kind} {name} has landed: {s.get('why')}"
        if s["stage"] not in ("merged", "landed"):
            return f"{kind} {name} has not merged into bolt/{bolt}: it is {s['stage']}"
        c = s.get("commit")
        if not c:
            return (f"cannot tell whether {kind} {name} has landed on {kit}'s main: Flume's status of its place, as the runner "
                    "carried it, names no commit it landed at")
        if held.get(c) == 1:
            return (f"{kind} {name} has not landed on {kit}'s main: its place landed on bolt/{bolt} at {c[:7]}, which main does "
                    "not hold")
        if held.get(c) != 0:
            return f"cannot tell whether {kind} {name} has landed on {kit}'s main: git could not read {c[:7]} there"
    return None


def fixes_on(requests, reads, base):
    """Each fix whose launch stands on a base, bolt/<bolt> or main, in requests.rec's order, as (its launch, its stage),
    read from the runner that took it (reads, by host; piece_stage)."""
    return [(l, piece_stage(requests, reads, l)) for l in standing(requests)
            if l.get("Base") == base and (l.get("Work") or "").startswith("fix/")]


def fixes_in_flight(requests, reads, bolt):
    """The fixes in flight on a bolt given through Flume (Decision 10), {fix/<bolt>/<name>: its brief}: each whose launch
    stands and whose place has not merged into the bolt, landed or been dropped, its stage read from the runner that
    took it (fixes_on), one crew can't read counted in flight (read.1). A fix in flight holds the bolt's landing as
    today's does (plan.landing_unready, landing_rows)."""
    return {l.get("Work"): l.get("Brief") for l, s in fixes_on(requests, reads, f"bolt/{bolt}")
            if l.get("Work").startswith(f"fix/{bolt}/") and s["stage"] not in ("merged", "landed", "dropped")}


def base_drop_asked(plan, requests):
    """Whether base_drop_due has anything to judge, from requests.rec and the plan alone: a launch of bolt/<bolt> whose
    bolt has left the plan, that a drop names. A plan write reads the runners for base_drop_due only then."""
    drops = {r.get("Of") for r in requests if r.get("Act") == "drop"}
    return any(l.get("Act") == "launch" and (l.get("Work") or "").startswith("bolt/") and l.get("Request") in drops
               and plan.bolt(l.get("Work")[5:]) is None for l in requests)


def base_drop_due(plan, requests, reads):
    """The drops a plan write asks again of a bolt's base place (crew-lands-each-bolt-through-flumes-base-place,
    Decision 8; bolt-teams "A bolt's drop drops its base place last" and "A base place's drop the runner refused is
    asked again once nothing on its branch is live"), from plain facts: plan, as the write leaves it; requests,
    requests.rec's records; reads, the partition's runners as crew read them. For each launch of bolt/<bolt> whose bolt
    has left the plan, that a drop names, the newest drop of it answered refused by the runner that took the launch, as
    Flume refuses one while a place on its branch is live: its drop asked again, (act, work, its fields), once no piece
    of the bolt reads live, each piece's launch on its branch read dropped, merged, landed or refused, and once for each
    refusal, a drop asked and not yet answered asking none. None where crew can't tell (read.1)."""
    out = []
    for l in requests:
        work = l.get("Work") or ""
        if l.get("Act") != "launch" or not work.startswith("bolt/") or plan.bolt(work[5:]) is not None:
            continue
        drops = [r for r in requests if r.get("Act") == "drop" and r.get("Of") == l.get("Request")]
        n = number(l.get("Request"))
        reading, why = taken(reads, n)
        if not drops or why or reading is None:
            continue
        answer = reading["answers"].get(number(drops[-1].get("Request")))
        if answer is None or answer.get("Outcome") != "refused":
            continue
        place = reading["places"].get(n)
        f = flume_facts(place["status"], place["place"]) if place and not place.get("why") else None
        if f and f["over"]:
            continue
        pieces = [p for p in requests if p.get("Act") == "launch" and p.get("Base") == work]
        if any(piece_stage(requests, reads, p)["stage"] not in ("dropped", "merged", "landed", "refused") for p in pieces):
            continue
        out.append(("drop", work, {"Of": l.get("Request")}))
    return out


# ------------------------------------------------------------------------------------- a landing through the runner

def lands_of(requests, launch):
    """The land requests of a launch (Decision 4 of crew-lands-each-bolt-through-flumes-base-place), in requests.rec's
    order: each land whose Of names it."""
    n = launch.get("Request") if launch is not None else None
    return [r for r in requests if r.get("Act") == "land" and n is not None and r.get("Of") == n]


def landing_of(launch, lands, reads):
    """A bolt's landing, or a fix of main's, as the runner reports it (crew-lands-each-bolt-through-flumes-base-place,
    Decision 6; bolt-teams "A landing's outcome is read from the runner's report"), from plain facts: launch, the
    newest launch not dropped of bolt/<bolt> or fix/main/<kit>/<name> (launch_of); lands, the land requests of it
    (lands_of); reads, the partition's runners as crew read them (host_read's, by host). The base place is read from
    the runner that took the launch, its answers to the launch and the lands and Flume's status of the place as it
    carried it (flume_facts), each fact guarded (read.2). Returns {"outcome", and what goes with it}:
    unlaunched, with the runner's words, while the launch is unanswered, held or refused; landed, with Flume's commit,
    the merge queue's entry where Flume names one and the newest land's request, once the place is over landed; dropped, once it is over dropped; none, while no land stands; asked, with the
    newest land's request, while the runner has not answered it or Flume has not submitted it yet, the place's
    submissions fewer than the lands the runner carried; stopped, in the runner's words, when it answered the newest
    land refused, as when a place on the branch is live; submitted, with the merge queue's entry and its state, while
    it waits or is under test; refused, the bolt's, for a failed check, with Flume's words; refused, a conflict, with
    the files and main's revision where the merge queue records one; stopped, in Flume's words, for a submission
    withdrawn or refused; unknown, naming why, where crew can't read the runner, the place's status, or the submission
    (read.1)."""
    if launch is None:
        return {"outcome": "unknown", "why": "no launch of it stands in requests.rec"}
    work, n = launch.get("Work"), number(launch.get("Request"))
    reading, why = taken(reads, n)
    if why:
        return {"outcome": "unknown", "why": why}
    answer = reading["answers"].get(n) if reading else None
    if answer is None or answer.get("Outcome") in ("held", "refused"):
        return dict({"outcome": "unlaunched"}, **({"words": answer.get("Words")} if answer is not None and answer.get("Words") else {}),
                    **({"refused": True} if answer is not None and answer.get("Outcome") == "refused" else {}))
    if answer.get("Outcome") != "launched":
        return {"outcome": "unknown", "why": f"the runner answered launch {n} of {work} {answer.get('Outcome')}, and a launch is "
                                             "answered held, launched or refused"}
    place = reading["places"].get(n)
    if place is not None and place.get("why"):
        return {"outcome": "unknown", "why": place["why"]}
    f = flume_facts(place["status"], place["place"]) if place is not None else None
    if place is not None and f is None:
        return {"outcome": "unknown", "why": f"Flume's status of {work}'s place, as the runner carried it, holds no place {place['place']}"}
    if f and f["over"] == "landed":
        return dict({"outcome": "landed", "commit": f["commit"]}, **({"entry": f["entry"]} if f["entry"] else {}),
                    **({"request": number(lands[-1].get("Request"))} if lands else {})) if f["commit"] else {
            "outcome": "unknown", "why": f"Flume's status of {work}'s place says it landed and names no commit"}
    if f and f["over"] == "dropped":
        return {"outcome": "dropped"}
    if not lands:
        return {"outcome": "none"}
    land = lands[-1]
    asked = {"outcome": "asked", "request": number(land.get("Request"))}
    la = reading["answers"].get(number(land.get("Request")))
    if la is None:
        return asked
    if la.get("Outcome") == "refused":
        return dict(asked, outcome="stopped", by="runner", words=la.get("Words") or "the runner refused the land")
    carried = sum(1 for l in lands if (reading["answers"].get(number(l.get("Request"))) or {}).get("Outcome") not in (None, "refused"))
    if f is None or (f["submits"] is not None and f["submits"] < carried):
        return asked
    if f["unread"]:
        return dict(asked, outcome="unknown", why=f"Flume could not read {work}'s submission: {f['unread']}")
    if f["entry_state"] in ("waiting", "under_test"):
        return dict(asked, outcome="submitted", entry=f["entry"], state=f["entry_state"])
    entry = {"entry": f["entry"]} if f["entry"] else {}
    if f["verdict"] == "failed":
        return dict(asked, outcome="refused", why="failed", words=f["verdict_words"] or f["waiting_words"] or "", **entry)
    if f["verdict"] == "conflict":
        return dict(asked, outcome="refused", why="conflict", words=f["verdict_words"] or f["waiting_words"] or "",
                    files=list(f["files"]), main=f["entry_base"], **entry)
    if f["verdict"] in ("withdrawn", "refused"):
        return dict(asked, outcome="stopped", by="flume", words=f["waiting_words"] or f["verdict_words"] or f"the merge queue {f['verdict']} it",
                    **entry)
    if f["entry_state"] == "landed":
        return dict(asked, outcome="submitted", entry=f["entry"], state="landed")
    return asked


def landing_said(l, bolt=None, head=None):
    """A landing (landing_of) in the words of its head line and its row (Decision 10): asked with its request;
    under test or waiting with the merge queue's entry; landed at its commit; refused in Flume's words; stopped in the
    runner's or Flume's; unknown with why; "" for none, unlaunched (base_said) and dropped. Given the bolt and the head
    its land was posted at, the words a view shows say that head and what comes next (bolt-teams "A landing that did not
    land is the bolt's only for its own content"): a failed check, that the bolt is open for work and ops starts a fix
    on it with Flume's words, crew fix <bolt> <name> "<words>"; a conflict, that it takes main first, by the fix crew
    launches to take main into it, ops starting nothing; a stop, at that head. Without them, the words the run record
    keeps of a refusal (landing_entry)."""
    o = l.get("outcome")
    first = (l.get("words") or "").strip().splitlines()[0] if (l.get("words") or "").strip() else ""
    at = f" at {head[:7]}" if head else ""
    if o == "asked":
        return f"landing asked, request {l['request']}"
    if o == "submitted":
        state = {"under_test": "under test", "waiting": "waiting in the merge queue", "landed": "landed in the merge queue"}.get(l.get("state"), l.get("state") or "")
        return f"landing #{l['entry']} {state}" if l.get("entry") else f"landing submitted, request {l['request']}"
    if o == "landed":
        return f"landed at {(l.get('commit') or '')[:7]}"
    if o == "refused" and l.get("why") == "conflict":
        main = f" at {l['main'][:7]}" if l.get("main") else ""
        if bolt is None:
            return f"landing refused in conflict with main{main}: {first}"
        return (f"takes main first: its landing{at} was refused in conflict with main{main}: {first}; crew launches the "
                "fix that takes main into it, ops starting nothing, and it lands again once that fix moves its head")
    if o == "refused":
        if bolt is None:
            return f"landing refused, a check failed: {first}"
        return (f"landing refused{at}, a check failed, the bolt's, open for work: {first}; it waits for a fix on the bolt, "
                f"which ops starts with Flume's words, crew fix {bolt} <name> \"{first}\", and lands again once that fix "
                "moves its head")
    if o == "stopped":
        return f"landing stopped{at}, nothing of the bolt's: {first}"
    if o == "unknown":
        return f"can't tell its landing: {l.get('why')}"
    return ""


def lands_due(rows, sent, requests, reads, posted=(), work=None):
    """The lands the user's send on a kit's landings card makes due (crew-lands-each-bolt-through-flumes-base-place,
    Decisions 4 and 5; rail-cards "A landings row is due one land for each send and head"), from plain facts (code.7):
    rows, the card's rows in its order (landing_rows' and each fix of main's), each {bolt, box, facts: {head}}, a fix of
    main's naming its work fix/main/<kit>/<name> as work; sent, {a row's work: (the card whose send ticked it, the head
    it ticked)}, for each row a send stands for, the card's answer's and an earlier one's (landings_sent); requests,
    requests.rec's records; reads, the partition's runners as crew read them; posted, the lands crew recorded posting,
    [{work, card, head, request}] (lands_posted); work, each bolt's own work between the head ticked and its head now
    where it moved (bolt_work), by which the send still stands (send_stands). Returns [(work, the launch's number)] in
    the card's order with the fixes of main first, one for each row whose box is ticked on a send that stands for it at
    its head now, that can land (a box), whose launch stands, and none of whose lands was posted at its head now nor
    stands undecided (landing_of: asked or submitted) nor is read unknown, and no land of which posted on the same send
    was stopped, the send then spent; a bolt started before bolts were base places, with no launch of its own, none."""
    work, due = work or {}, []
    posted = list(posted)
    for r in sorted(rows, key=lambda r: not (r.get("work") or "").startswith("fix/main/")):
        w = r.get("work") or f"bolt/{r['bolt']}"
        if not r.get("box") or w not in sent:
            continue
        card, at = sent[w]
        head = (r.get("facts") or {}).get("head") or ""
        if not send_stood(at, head, work.get(r["bolt"])):
            continue
        launch = launch_of(requests, w)
        if launch is None:
            continue
        mine = [p for p in posted if p.get("work") == w]
        if any(p.get("head") and head and (head.startswith(p["head"]) or p["head"].startswith(head)) for p in mine):
            continue
        l = landing_of(launch, lands_of(requests, launch), reads)
        if l["outcome"] in ("asked", "submitted", "unknown", "unlaunched", "landed", "dropped"):
            continue
        if l["outcome"] == "stopped" and any(p.get("card") == card and str(p.get("request")) == str(l.get("request")) for p in mine):
            continue
        due.append((w, number(launch.get("Request"))))
    return due


def send_stood(sent, head, work):
    """plan.send_stands, which this module may not import: whether a send at sent still stands at head, the heads one
    by prefix, or the bolt's own work between them unchanged (work, bolt_work's), read with no why (read.1)."""
    if sent and head and (head.startswith(sent) or sent.startswith(head)):
        return True
    return bool(work) and not work.get("why") and not work.get("gained") and not work.get("lost")


# ------------------------------------------------------------------------------------------------ a fix of main

def main_priority(plan):
    """A fix of main's priority at its launch (Decision 11): one above every bolt given through Flume (priority_of), so
    Flume starts its code ahead of theirs, a red main holding back every landing on it."""
    return sum(1 for b in plan.bolts() if b.get("Path") == "flume") + 1


def main_fix_launch(plan, requests, label, repo, name, words, served):
    """The launch crew main fix <kit> <name> "<the failure's words>" appends (Decision 11; Decision 15 of
    the-team-machinery-leaves), as (act, work, its fields as plan.request takes them), or (None, why): a place of the fix
    kind named main--<name>, cut from main, in the kit's repository (repo, as the partition's kits name it) for the
    runner whose configuration names it to take in the stream its host maps it to (the user's ruling of 2026-11-01), ahead of every
    bolt (main_priority), its intent the kit's main, main-level ops as its recipient, the failure's words as its brief,
    and its submission held for the user's send (state.3). Refused while no runner answers for the partition (served,
    whether any runner's branch exists), since nothing would take it and the red main waits on it, the fix then being a
    bolt of one chore (state.3); and while a launch of that fix of the kit's main stands, landed or not, since the name
    is in use there."""
    kit = repo.split("/")[-1]
    if not served:
        return None, (f"no runner answers for {label}: its state repository holds no {runner_branch(label, '<host>')}, so nothing "
                      f"would take the fix; until a runner (Boomdrive) serves {label}, a fix of {kit}'s red main is a bolt "
                      f"of one chore, proposed first among the planned (state.3); tell {label}-planner, who proposes it")
    work = f"fix/main/{kit}/{name}"
    l = launch_of(requests, work)
    if l is not None:
        return None, (f"fix {name} of {kit}'s main is in use: it is launched as Flume place {l.get('Name')} (request "
                      f"{l.get('Request')}), so name this fix differently")
    return ("launch", work, {
        "Repo": repo, "Kind": "fix", "Name": f"main--{name}", "Base": "main", "Priority": main_priority(plan),
        "Intent": f"{label}/main/{kit}", "Recipient": f"{label}/ops", "Hold": "submission", "Brief": words}), None


def sent_of(requests, reads, launch):
    """The land that carries the user's send of a fix of main's row (crew-lands-each-bolt-through-flumes-base-place,
    Decision 5), standing for its launch: the newest land of it (lands_of), unless the runner that took the launch
    (reads, by host; taken) answered it refused; None while none stands. One whose runner crew can't read or tell
    stands, so no send is carried twice on a reading crew lacks (read.1); which lands are due is lands_due's."""
    lands = lands_of(requests, launch)
    sent = lands[-1] if lands else None
    reading = taken(reads, number(launch.get("Request")))[0] if sent is not None else None
    answer = reading["answers"].get(number(sent.get("Request"))) if reading else None
    return None if answer is not None and answer.get("Outcome") == "refused" else sent


def main_fixes_waiting(requests, reads):
    """Each fix of main a kit's landings row carries (Decision 11; crew-rail "A fix of main waits to land on its kit's
    row"): those whose launch stands and whose code has delivered with its submission waiting held, their stage read
    from the runner that took them (reads, by host; taken, piece_stage), in requests.rec's order, each {kit, name, host,
    brief, since, carried, head, launch, sent}: kit, the kit its launch's Repo names; since, when Flume read it waiting,
    in seconds, or None; carried, when the runner carried that status; head, the head Flume's status names its place
    at, or None; launch, its launch's number; sent, the number of the land that carries the user's send of it (sent_of),
    None while it waits on that send. One crew can't read is left off, as a bolt whose stage crew can't
    read is, being in no state it can tell to send (read.1)."""
    out = []
    for l in standing(requests):
        work = l.get("Work") or ""
        if not work.startswith("fix/main/"):
            continue
        s = piece_stage(requests, reads, l)
        if s["stage"] not in ("waits", "stalled") or not s.get("held"):
            continue
        reading = taken(reads, number(l.get("Request")))[0]
        place, sent = reading["places"][number(l.get("Request"))], sent_of(requests, reads, l)
        _, _, kit, name = work.split("/", 3)
        f = flume_facts(place["status"], place["place"])
        out.append(dict(kit=(l.get("Repo") or kit).split("/")[-1], name=name, host=reading["host"], brief=l.get("Brief") or "",
                        since=f["waiting_since"], carried=place["at"], head=f["head"], launch=number(l.get("Request")),
                        sent=number(sent.get("Request")) if sent is not None else None))
    return out


# ------------------------------------------------------------------------------------- a role's work that lands

# The branch a role's work lands on, its repository's default: main, as crew reads every kit's main (plan.18) and cuts a
# fix of it (main_fix_launch).
ROLE_BASE = "main"
FORGE = re.compile(r"^[^/\s]+/[^/\s]+$")


def role_launch(requests, named, label, role, host, stream, repo, name, brief):
    """The launch crew role land <repo> <name> --brief-file <file> appends for a role's work that lands (Decision 10 of
    roles-run-as-flume-kinds; roles.7 part 3), as (act, work, its fields as plan.request takes them), or (None,
    why): a place of Flume's own chore kind named name, cut from repo's default branch (ROLE_BASE), on the main level's
    host and in the role's stream, at priority 0, its intent the role's run, <label>-<role>, its recipient the role's
    address, <label>/<role>, so its landing, or a wait on its caller, reaches the role's next run, and its brief the
    file's text whole, since the stage's agent is fresh. Refused for a repository not named as its forge address,
    <owner>/<name>, or one crew does not name (named: the blueprints repositories the teams file names and the
    partition's kits, plan.land_named), for a brief with no words, and
    while a launch of role/<role>/<name> stands, since the name is in use there."""
    if not FORGE.match(repo):
        return None, f"a repository is named by its forge address, <owner>/<name>, which the runner resolves to its clone, not {repo}"
    if repo not in named:
        return None, (f"crew names no repository {repo}: a role's work lands in a blueprints repository the teams file names or "
                      "a kit the partition's plan or landings name, and it names " + ", ".join(sorted(n for n in named if FORGE.match(n))))
    if not brief.strip():
        return None, f"the brief for {name} holds no words, and a chore's agent starts fresh with its brief alone"
    work = f"role/{role}/{name}"
    l = launch_of(requests, work)
    if l is not None:
        return None, (f"{name} is in use for {label}/{role}: request {l.get('Request')} launched it in {l.get('Repo')} as Flume "
                      f"place chore--{l.get('Name')}, so name this work differently")
    return ("launch", work, {
        "Repo": repo, "Kind": "chore", "Name": name, "Base": ROLE_BASE, "Host": host, "Stream": stream, "Priority": 0,
        "Intent": f"{label}-{role}", "Recipient": f"{label}/{role}", "Brief": brief}), None
