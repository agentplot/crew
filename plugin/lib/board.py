#!/usr/bin/env python3
"""board.py: the board of a drive's flow, read from crew's state.

  crew board [--label L] [--json]    the flow as four lanes stacked one above the other, one object to a line:
                                     Inception (the signals no move has taken, by who captured them, and the
                                     explorations on each kit's main), Bolt plan (the open proposals, the planned
                                     bolts and the queue), Construction (each held bolt as a ledger of its units and
                                     fixes) and Operation (the bolts landed in the last seven days, then each
                                     environment's deploys of that week and those still open, and the operations
                                     waiting on it); every rail row a marker on its object, and what needs attention
                                     at the foot
  crew _views <label>                one drive's read as the host's follower makes it: the rail printed as crew
                                     rail prints it, the card sessions of closed cards and gone rows ended as crew rail
                                     ends them, and the board's data written for the board tab, with each agent's view
                                     of it for the band crew's mod draws above that agent's prompt
  crew _follow [--once]              the host's follower with no tab, the command a job of the host's runs: one read in
                                     its own process for every drive with an operator session here, fetching each
                                     repository once a minute on its clock and showing this host's writes within
                                     seconds, checking first what moved and reading only that, asking another host,
                                     Pending You or herdr only when something there could have moved, and learning
                                     that a submission moved from its runner's report, starting no sluice; the due
                                     restarts handed out once crew's checkout, the crew the host has installed or the
                                     teams file moved (crew _update), and each drive's rail, board and agents'
                                     views written as frames, stale after three minutes; it waits for the host's
                                     follower lock while a rail tab holds it, and follows only on the crew the host
                                     has installed, starting again as it before it reads while it runs another.
                                     --once makes one tick and ends
  crew _rail <label> [--once]        the rail tab: the latest rail the host's follower wrote, drawn whenever it
                                     changes, headed with its age once stale; while no one holds the host's follower
                                     lock, it takes it and follows itself, on the crew the host has installed as the
                                     job does. --once draws once and follows nothing
  crew _board <label> [--once]       the board tab: the latest board the host's follower wrote, drawn at the pane's
                                     width whenever it or the pane changes

Read from the plan, the proposals, the moves, the signals, the kits and the run record, in one read that also makes the
rail (plan.rail_read); no state is written, only the frames the host's follower hands the rail and board tabs and the
agents' mods, in crew's cache, each one redraw and not state (state.4). A host has one follower, holding its lock while
it follows: swancloud's job running crew _follow, or, where none runs, a rail tab's own loop. Its refresh, as it prints
the rail, ends the card sessions whose card is closed or whose row is gone, as crew rail does; crew board ends nothing.
The board answers nothing and prints no command: the rail and its shell are where things are answered."""
import argparse, contextlib, datetime, fcntl, io, json, os, pathlib, re, shlex, shutil, signal, subprocess, sys, tempfile, time

LIB = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(LIB))
import asks, crew, gather, ops, plan, record, runner  # noqa: E402
from crew import Refusal, fail  # noqa: E402

# Flywheel Next's glyph for the decision a rail row asks (S17): an approval, held on the card's button. An operation's
# card, a deploy's word or a step marked done or declined, is held too.
GLYPH = {"proposals": "✓", "land": "✓", "operations": "✓"}
ATTENTION = "!"
# A unit's stage as one pip, filling as it goes: not begun, being designed, coded, every task ticked, merged; a stage
# crew could not read is "?". A bolt is its units' pips in the plan's order; a crossed piece the runner is launching
# has not begun (pip).
PIP = {"queued": "○", "waiting": "○", "ready": "○", "launching": "○", "amended": "◔", "construct": "◔", "planned": "◔", "code": "◑",
       "verify": "◕", "merged": "●", "landed": "●"}
# How many explorations an agent's view names before it counts the rest.
SHOWN = 6
# The frames the host's follower writes for the rail and board tabs and the agents' mods, by label.
FRAMES = pathlib.Path.home() / ".cache/crew/board"
STALE = 3 * record.PERIOD  # seconds: three of the follower's periods
SIGNAL = re.compile(r"^signals/([^/]+)/([0-9]{2}-[^/]+)\.md$")
DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
STYLES = {"bold": "\033[1m", "dim": "\033[2m"}


def iso(t):
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") if t else None


def when(at):
    """A time the board was handed, an ISO time or a date alone, as an aware datetime, one without a zone taken as UTC
    (a date as its midnight there); None when it is neither."""
    try:
        t = datetime.datetime.fromisoformat(at.replace("Z", "+00:00")) if at else None
    except ValueError:
        return None
    return t if not t or t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)


def stamp(at):
    """A capture's time as the board's data holds it: a date alone as it is, a time in UTC whatever zone it was
    written in; None when it is neither. The board's text says it in the reader's own time."""
    t = when(at)
    return None if not t else at if DATE.fullmatch(at) else iso(t)


# ------------------------------------------------------------------------------------------------- the read

def texts(repo, tip, paths):
    """The text of each path at tip in crew's cache of the repo, {path: text}, a path that is not there left out: in one
    git cat-file --batch, or from the follower's kept blobs when it reads (plan.Kept)."""
    files = plan.kept_listing(repo, tip)
    if files is not None:
        got = {p: plan.READ.follower.text(repo, files[p]) for p in paths if p in files}
    else:
        got = dict(zip(paths, plan.cat_file(repo, [f"{tip}:{p}" for p in paths])))
    return {p: t for p, t in got.items() if t is not None}


def signals_at(repo, tip, home, moved):
    """Each signal at tip whose id has no move, with its capture's captured_by (its source when it has none) and when
    the capture was made (its at, else its event_date, which is what a signal's age counts from, as stamp gives it),
    its kind and the first line of its body."""
    sigs = [m.groups() for m in map(SIGNAL.match, plan.paths_at(repo, tip, "signals/")) if m]
    sigs = [(c, n) for c, n in sigs if f"{c}/{n}" not in moved]
    got = texts(repo, tip, sorted({f"signals/{c}/capture.md" for c, _ in sigs}) + [f"signals/{c}/{n}.md" for c, n in sigs])
    out = []
    for c, n in sigs:
        cap, text = got.get(f"signals/{c}/capture.md"), got.get(f"signals/{c}/{n}.md")
        body = re.sub(r"^---\n.*?\n---\n", "", text or "", count=1, flags=re.S)
        out.append({"signal": f"{c}/{n}", "home": home, "captured_by": plan.field(cap, "captured_by") or plan.field(cap, "source") or None,
                    "at": stamp(plan.field(cap, "at") or plan.field(cap, "event_date")), "kind": plan.field(text, "kind") or None,
                    "first": next((l.strip() for l in body.splitlines() if l.strip()), None)})
    return out


def signals(fleet, label, tip):
    """The label's signals no move has taken, in both homes: the drive's branch at the tip the plan was read from
    (None when the branch is not started, so nothing is moved), and main of the drive's first blueprints repo;
    and each home that could not be read, {what: why}. When the branch's signals and moves can't be read, which
    signals are moved can't be known, and none is listed (read.1)."""
    repo, ref = plan.state_of(fleet, label)
    try:
        moved = {m.get("Signal") for m in plan.Plan(plan.show(repo, tip, "moves.rec") or "").recs("Move")} if tip else set()
        out = signals_at(repo, tip, "branch", moved) if tip else []
    except Refusal as e:
        return [], {f"{ref} of {repo}": str(e)}
    srepo = crew.drive_of(fleet, label)["blueprints"][0]
    try:
        btip = plan.tip_of(srepo, "main")
        out += signals_at(srepo, btip, "blueprints", moved) if btip else []
    except Refusal as e:
        return out, {f"main of {srepo}": str(e)}
    return out, {}


def flow_read(fleet, labels, sweep=False):
    """One read of the labels' flow, which makes both the rail and the board: the rail's read with every team of the
    labels surveyed, its dev servers and explorations too (plan.rail_read), and the signals of each label whose
    plan was read; a plan that could not be read leaves its moves unknown, and is named already. With sweep, the rail
    tab's, the read ends the card sessions of closed cards and gone rows, as crew rail's does."""
    read = plan.rail_read(fleet, labels, board=True, sweep=sweep)
    read["signals"] = {l: signals(fleet, l, tip) for l, _, tip, _ in read["found"]}
    read["roles"] = roles_read(fleet, read["found"])
    return read


def roles_read(fleet, found):
    """What the board reads of each drive's roles that run as their kinds, for their runs' views and the attention
    line (kind_runs; Decision 15 of roles-run-as-flume-kinds), beside its plan in the same read (plan.12): {label:
    {"kinds": {role: the stream it runs in, the drive's own, named by its label}, "asks": asks.rec's text at the tip
    the read found, None where it holds none, "host": the main level's host, "reading": that host's runner as read
    beside the branch (plan.runners, runner.of_host)}}, for each drive read whose teams-file `runs` names a role
    on demand (crew.on_demand); one that runs none as its kind reads nothing more."""
    out = {}
    for l, repo, tip, _ in found:
        p = crew.drive_of(fleet, l)
        kinds = {r: l for r in crew.KIND_ROLES if crew.on_demand(p, r)}
        if kinds:
            out[l] = {"kinds": kinds, "asks": plan.show(repo, tip, "asks.rec") if tip else None, "host": p["machine"],
                      "reading": runner.of_host(plan.runners(repo, l), l, p["machine"])}
    return out


# ------------------------------------------------------------------------------------------------- the data

def marker(r, cards, label, logs):
    """A rail row as a marker: its group, its card key, its glyph, when it began to wait, its card, the one open in the
    row owner's name as the rail's card line names it (plan.row_cards), with when the user answered it, or None, and,
    when none is open, the words of
    Pending You's refusal of the last post under its key, as the rail's card line gives them (plan.last_refusal), or
    None; logs are the label's run-record entries the rail read."""
    card, _ = plan.row_cards(cards, dict(r, label=label))
    return {"group": r["group"], "key": r["key"], "glyph": GLYPH[r["group"]], "at": r.get("date") or iso(r["at"]),
            "card": {"by": card["by"], "host": card["host"], "at": iso(card["at"]),
                     "answered": iso(card["answered"]["at"]) if card.get("answered") else None} if card else None,
            "refused": None if card else plan.last_refusal(logs, r["key"])}


def markers(rows, cards, label, group, obj, logs):
    """The rail's rows for an object, as markers: a held bolt's landing row is its kit's, land/<kit>, which names it
    among its bolts (record 0031 as amended 2026-10-23); any other row is the object's by its key."""
    return [marker(r, cards, label, logs) for r in rows if r["label"] == label and r["group"] == group
            and (obj in [b["bolt"] for b in r.get("bolts", [])] if group == "land" else r["key"].split("/")[1] == obj)]


def keyed(rows, cards, label, key, logs):
    """The rail's row with that card key, as a marker, when there is one: an operation's, whose key names the deploy or
    the step itself."""
    return [marker(r, cards, label, logs) for r in rows if key and r["label"] == label and r["key"] == key]


def records_proposed(entries, cards):
    """The decision records proposed and not yet accepted or rejected, from the record.<status> entries crew record
    writes on record/<kit>/<number>, oldest first: each {kit, number, at, settled}, settled when the user's yes was
    given in the pane, and its card, {by, card, at} while one is open under the record's key, as record 0031 keys it or
    with the commit after it as it was keyed before, else None."""
    out = {}
    for e in entries:
        m = re.fullmatch(r"record\.(proposed|accepted|rejected)", e.get("Act") or "")
        obj = next((o for o in e.get("On") or [] if re.fullmatch(r"record/[a-z0-9][a-z0-9-]*/[0-9]{4}", o)), None)
        if not m or not obj or e.get("Refused"):
            continue
        out.pop(obj, None)
        if m.group(1) == "proposed":
            out[obj] = {"kit": obj.split("/")[1], "number": obj.split("/")[2], "at": e["At"], "settled": e.get("State") == "settled in the pane"}
    for obj, r in out.items():
        open_ = [c for c in cards if c["key"] and (c["key"] == obj or c["key"].startswith(obj + "/"))]
        r["card"] = {"by": open_[-1]["by"], "card": open_[-1]["card"], "at": iso(open_[-1]["at"])} if open_ else None
    return list(out.values())


def environments(fleet, label, entries, rows, cards, since, logs):
    """The drive's environments for the Operation lane: each one's deploys that moved since since or are still open,
    and the operations waiting on it, as ops.environments reads them from the run record (plan.14, state.4), each
    deploy and operation with its rail row's marker."""
    return [{"env": env,
             "deploys": [dict(d, markers=keyed(rows, cards, label, d["row"], logs)) for d in v["deploys"]],
             "waiting": [dict(w, markers=keyed(rows, cards, label, w["row"], logs)) for w in v["waiting"]]}
            for env, v in ops.environments(entries, iso(since)).items()]


def board_data(fleet, labels, read, now):
    """The board of each label as data, the fields the page reads (`crew board --json`); an object's drive and kit
    say whose it is, and nothing names a team (crew-board). Each drive lists its kits, the repositories its plan and
    its landings name (plan.drive_kits), which the fleet page lists. Each started bolt is a ledger of its units, chores and fixes,
    its host and stream where the runner that took its work reported them (plan.bolt_at), each unit or chore with its
    kind, and each of them with its stage from the runner's records and what goes with it (flume, Stages.crossed,
    Stages.fixes), a piece's submission among it as the runner carries it (runner.piece_said), and the ledger its landing
    as the run record holds it (record, landing_of), nothing of sluice's queue read (crew record 0056 points 1 and 4); a
    runner that could not be read is named for attention. Each ledger has its bolt's time to now (plan.held_time, plan.20): {age, shares: {team,
    kit, team_or_kit, user, hold, nobody}, now: {holder, what, since}, said}, in minutes, or {unknown: why, said}, with
    its age once its start is read. Each drive lists too its open cards, oldest first, each with whose it is and what
    it is, a row's, a decision record's or a question (plan.card_kind), and the decision records proposed and not yet
    accepted or rejected, which the design agent's band shows (records_proposed); the places that wait on an answer and
    the fixes of main and take-main fixes in flight (asking and fixing, flume_waits), which the planner's and main-level
    ops's bands show (crew-board "The planner's and ops's bands show what places wait on them for"); and each role it
    runs as its kind, for its run's view, with each such run that stopped short or was lost named for attention (runs,
    kind_runs; Decision 15 of roles-run-as-flume-kinds). A started bolt's ledger says whether it is marked to stay
    (stays), and each drive lists the holds standing on its landings or a kit's (holds, [{kit, why}], kit None for the
    drive's; plan.holds_of), which the planner's and ops's bands open with (Decision 7 of a-proven-bolt-lands-on-proof)."""
    here = crew.this_host()
    rows, cards, sv = read["rows"], read["cards"], read["sv"]
    since = plan.utc(record.when(None)[1])
    parts = []
    for l in labels:
        found = next(((repo, tip, pl) for x, repo, tip, pl in read["found"] if x == l), None)
        repo, tip, pl = found or (plan.state_of(fleet, l)[0], None, None)
        unread, logs = read["unread"].get(l, {}), read.get("logs", {}).get(l, [])
        hosts = {}  # each host asked for its kits, never for its run record, which is read from the branch (read.5)
        for h in plan.hosts_of(fleet, l, read.get("runs")):
            v = sv.get(h)
            hosts[h] = f"its kits: {v['error']}" if v and not v["ok"] else True
        attention = [{"what": "host", "name": h, "why": v} for h, v in hosts.items() if v is not True]
        attention += [{"what": "plan", "name": n, "why": f"its run record: {why}"} for n, why in unread.items()]
        attention += [{"what": "plan", "name": n, "why": why} for n, why in read["errors"].items() if n.startswith(f"{l}/main of ") or n == f"the plan of {l}"]
        if found and not tip:
            attention.append({"what": "plan", "name": f"{l}/main of {repo}", "why": "not started, so there is no plan to read"})
        sigs, sunread = read["signals"].get(l, ([], {}))
        attention += [{"what": "signals", "name": n, "why": why} for n, why in sunread.items()]

        explorations = []
        for kit in read["kits"].get(l, []):  # the kits its plan and its landings name (plan.drive_kits)
            t = plan.main_kit_read(fleet, l, kit)  # read in the checkout its main-level host keeps of it
            k = ((sv.get(t["machine"]) or {}).get("kits", {}).get(t["kit"]["main"]) or {}) if t else {}
            if k.get("ok") and "explorations" in k:
                explorations += [{"kit": kit, "name": e["name"], "first": e["first"]} for e in k["explorations"]]

        proposals = [{"proposal": d["proposal"], "by": d["by"], "opened": d["opened"], "case": (d["case"] or "").splitlines()[0] if d["case"] else None,
                      "markers": markers(rows, cards, l, "proposals", str(d.get("first") or d["proposal"]), logs)}
                     for d in read["props"] if d["label"] == l]
        planned, queue, construction = [], [], []
        runs = (read.get("runs") or {}).get(l)
        if pl:
            st = plan.Stages(fleet, pl, sv, read.get("runs"), l)
            for b in pl.bolts():
                units = pl.work_of(b.name())
                if not plan.started(b):
                    planned.append({"bolt": b.name(), "repo": b.get("Repo"), "goal": b.get("Goal"),
                                    "units": [{"unit": u.name(), "kind": plan.kind_of(u), "stage": st.of(u.name())["stage"]} for u in units]})
                    continue
                t = st.at(b)[0]  # where its work runs, as the runner that took it reported (plan.bolt_at)
                k, _ = st.kit(b) if t else (None, None)
                k = k or {}

                state = st.bolt_state(b) if t else "unknown"
                silent = st.unread(b)
                if silent:
                    attention.append({"what": "runner", "name": silent[0], "why": silent[1]})
                recorded = landing_of(logs, b.name())
                ledger = {"bolt": b.name(), "repo": b.get("Repo"), "goal": b.get("Goal"), "host": st.host(b),  # plan.Stages.host
                          "stays": b.get("Stays") == "yes",  # marked to stay: it lands on the user's send (record 0067)
                          "head": (k.get("bolts", {}).get(b.name()) or {}).get("head"),
                          "stream": t["stream"] if t else None, "state": state, "url": None,  # its places are Flume's (crew-board)
                          "markers": markers(rows, cards, l, "land", b.name(), logs), "units": [], "fixes": [],
                          "record": recorded, "landing": st.landing(b),
                          "time": plan.held_time(fleet, logs, read["unread"].get(l, {}), pl, b, k, now)}
                for u in units:
                    s = st.of(u.name())
                    ledger["units"].append({"unit": u.name(), "kind": plan.kind_of(u), "stage": s["stage"], "tasks": s["tasks"],
                                            "worktree": s["worktree"], "url": None, "flume": s.get("flume")})
                ledger["fixes"] = [{"fix": w, "merged": x["stage"] in ("merged", "landed"), "worktree": None,
                                    "url": None, "flume": x} for w, _, x in st.fixes(b)]
                construction.append(ledger)
                if state == "landed" or unclosed(ledger):
                    attention.append({"what": "landed", "name": b.name(), "why": f"it landed on main and was not closed: {unclosed(ledger)}"
                                      if unclosed(ledger) else "every unit has landed on main, and the bolt is still in the plan"})
            queue = [{"unit": u.name(), "kind": plan.kind_of(u), "repo": u.get("Repo"), "sources": u.all("Source")} for u in pl.queue()]
        asking, fixing = flume_waits(construction, runs, l)
        kinds, waits = kind_runs(l, (read.get("roles") or {}).get(l))
        attention += waits
        operation = [{"bolt": x["bolt"], "at": iso(x["at"]), "by": x["by"], "units": x["units"]}
                     for x in sorted(read["landings"], key=lambda x: x["at"], reverse=True) if x["label"] == l and x["at"] and x["at"] >= since]
        envs = environments(fleet, l, read.get("ops", {}).get(l, []), rows, cards, since, logs)
        mine = sorted((c for c in cards if c["label"] == l), key=lambda c: (c["at"], c["card"]))
        parts.append({"label": l, "plan": tip, "hosts": hosts, "kits": list(read["kits"].get(l, [])),
                      "cards": [{"key": c["key"], "card": c["card"], "by": c["by"], "host": c["host"], "at": iso(c["at"]),
                                 "kind": plan.card_kind(c["key"]), "answered": iso(c["answered"]["at"]) if c.get("answered") else None,
                                 "answer": c["answered"]["answer"] if c.get("answered") else None} for c in mine],
                      "records": records_proposed(logs, mine),
                      "inception": {"signals": sorted(sigs,
                                                      key=lambda s: (when(s["at"]) is None, when(s["at"]) or now, s["signal"])),
                                    "explorations": explorations},
                      "bolt_plan": {"proposals": proposals, "planned": planned, "queue": queue},
                      "construction": construction, "operation": operation, "environments": envs, "attention": attention,
                      "asking": asking, "fixing": fixing, "runs": kinds, "holds": plan.holds_of(pl)})
    return {"read_at": iso(now), "from": here, "drives": parts, "unread": read["errors"]}


def kind_runs(label, roles):
    """Each role the drive runs as its kind, for its run's view (crew-board "A role that runs as its kind has its
    view"), and what the attention line names of their runs ("The attention line names a role's run that waits"), a
    decision on the board's read of them (roles_read) alone (code.7): (runs, attention). Each run {role, run, stream,
    turn, waiting, since}: its name, <label>-<role>; the stream it runs in, the drive's own, named by its label; its turn as asks.run_view gives it,
    None while it has none; how many asks wait for its next run, and when the oldest was asked. The attention names a
    run Flume's status shows stopped short, with its words, or lost, with its place and host, and prints no command
    (crew-board "The board answers nothing"); and each run whose standing crew can't read, those of one why together
    (read.1). Nothing for a drive that runs no role as its kind."""
    if not roles:
        return [], []
    held, turns = asks.parse(roles["asks"])
    runs, attention, unread = [], [], {}
    for role, stream in roles["kinds"].items():
        turn, waiting = asks.run_view(held, turns, role)
        runs.append({"role": role, "run": f"{label}-{role}", "stream": stream, "turn": turn, "waiting": len(waiting),
                     "since": waiting[0]["At"] if waiting else None})
        address, host = f"{label}/{role}", roles["host"]
        why = runner.role_run(roles["reading"], address)["why"]
        if why:
            unread.setdefault(why, []).append(role)
            continue
        w = runner.run_waiting(roles["reading"], address)
        if w and w[0] in ("answer", "lost"):
            first = (w[1] or "").strip().splitlines()[0] if (w[1] or "").strip() else "no words"
            how = "stopped short" if w[0] == "answer" else "lost"
            attention.append({"what": "run", "name": f"{label}'s {role} run", "run": f"{label}-{role}", "how": how, "place": w[2],
                              "host": host, "words": w[1],
                              "why": f"{how}, its place {w[2]} on {host}" + (f": {first}" if how == "stopped short" else "")})
    for why, rs in unread.items():
        named = rs[0] if len(rs) == 1 else ", ".join(rs[:-1]) + " and " + rs[-1]
        attention.append({"what": "run", "name": f"{label}'s {named} {'run' if len(rs) == 1 else 'runs'}", "run": None, "how": "unknown",
                          "place": None, "host": roles["host"], "words": None,
                          "why": f"crew can't tell how {'it stands' if len(rs) == 1 else 'they stand'}: {why}"})
    return runs, attention


def flume_waits(construction, runs, label):
    """What a drive's places wait on its roles for (crew-board "The planner's and ops's bands show what places wait
    on them for"), a decision of facts alone (code.7): (asking, fixing). asking, for the planner's band, each unit, chore
    or fix of a started bolt, from its ledger (construction), whose place stopped short asking or waits on its caller,
    which crew answer answers (runner.answer_retry), {bolt, repo, name, stage, said}; fixing, for main-level ops's band,
    each fix of a kit's main (runs, the drive's (requests, runners) as the rail read them, runner.fixes_on) and each
    take-main fix of a started bolt that has not merged, landed or been dropped, the fixes of main first, {fix,
    repo, host, stage, said}; stage and said, as runner.piece_said says them; then each live landing fix of a started
    bolt's base place, read from its ledger's landing (plan.Stages.landing, runner.landing_fix;
    crews-bolt-kind-names-its-landing-fix, Decision 6), its stage `landing fix` and said its note."""
    asking, fixing = [], []
    for l, s in runner.fixes_on(*runs, "main") if runs else []:
        if s["stage"] not in ("merged", "landed", "dropped"):
            took = runner.taken(runs[1], runner.number(l.get("Request")))[0]
            fixing.append(dict(fix=l.get("Name"), repo=(l.get("Work") or "").split("/")[2], host=took["host"] if took else None,
                               **dict(zip(("stage", "said"), runner.piece_said(s)))))
    for b in construction:
        for x in b["units"] + b["fixes"]:
            s = x.get("flume")
            if not s:
                continue
            name, said = x.get("unit") or runner.bare(x["fix"]), dict(zip(("stage", "said"), runner.piece_said(s)))
            if runner.answer_retry(name, s)[0]:
                asking.append(dict(bolt=b["bolt"], repo=b["repo"], name=name, **said))
            if x.get("fix", "").startswith(f"fix/{b['bolt']}/take-main-") and s["stage"] not in ("merged", "landed", "dropped"):
                fixing.append(dict(fix=name, repo=b["repo"], host=b["host"], **said))
    for b in construction:  # each live landing fix of a bolt's base place, after the take-main fixes (runner.landing_fix)
        live = ((b.get("landing") or {}).get("fix") or {}).get("live")
        if live:
            fixing.append(dict(fix=live["name"], repo=b["repo"], host=b["host"], stage="landing fix", said=live["note"]))
    return asking, fixing


# ------------------------------------------------------------------------------------------------- the text

def fields(*xs):
    """Segments joined by two spaces, an empty one left out: each a string, (string, style), or a list of those."""
    out = []
    for x in xs:
        x = x if isinstance(x, list) else [x if isinstance(x, tuple) else (x, None)]
        if any(t for t, _ in x):
            out += ([("  ", None)] if out else []) + x
    return out


def named(repo, name):
    """A bolt's or a queued unit's name with its repository dim before it (S14)."""
    return [(repo, "dim"), (" ", None), (name, None)] if repo else [(name, None)]


def card_of(ms):
    """What each marker of a line says of its card at the line's end: open and who asked it, answered and whose act it
    waits on (design Decision 3 of a-wait-on-the-user-is-one-open-card-the-rail-agrees-with), none open, or none open
    because Pending You refused its row's last post, which the row then owes."""
    return [(f"card answered, waits on {m['card']['by']}" if m["card"] and m["card"].get("answered") else
             f"card open, asked by {m['card']['by']}" if m["card"] else
             "no card open, its post refused" if m.get("refused") else "no card open", None) for m in ms]


def row(segs, gutter=None, indent=0, ms=()):
    """One line as segments: a header or heading at the left edge, or, with a gutter, an object, its marker in the
    gutter and its card said at the line's end."""
    segs = ([(gutter.ljust(2) + " " * indent, None)] if gutter is not None else []) + segs
    for c in card_of(ms):
        segs += [("  ", None), c]
    return segs


def gutter(ms, attention=False):
    return ATTENTION if attention else (ms[0]["glyph"] if ms else " ")


def stage_of(u):
    """A unit's stage with its tasks, a chore's with `chore` before it (plan.11), in the board and each agent's view; a
    crossed piece's as the runner's records give it (runner.piece_said)."""
    if u.get("flume"):
        return ("chore " if u.get("kind") == "chore" else "") + runner.piece_said(u["flume"])[0]
    return (("chore " if u.get("kind") == "chore" else "") + u["stage"]
            + (f" {u['tasks'][0]}/{u['tasks'][1]}" if u["stage"] in ("code", "verify") and u["tasks"] else ""))


def fix_stage(f):
    """A fix's stage on its line: merged or not, or a crossed fix's as the runner's records give it."""
    return "fix " + runner.piece_said(f["flume"])[0] if f.get("flume") else "fix merged" if f["merged"] else "fix"


def detail_of(x):
    """What goes with a crossed piece's stage on its line (runner.piece_said), nothing for any other."""
    return runner.piece_said(x["flume"])[1] if x.get("flume") else ""


def stream_of(b):
    """A started bolt's Flume stream on its head line, as the runner that took its work reported it
    (runner.stream_said), nothing where none is reported."""
    return runner.stream_said(b.get("stream"))


def local(at):
    return f"{plan.utc(at).astimezone():%Y-%m-%d %H:%M}"


def deploy_state(d):
    """Where a deploy stands, as the board says it: waiting on the user's word, replaced unanswered, once the word
    went to another commit or once a newer deploy ended first, its outcome and when it ended, at the step that failed,
    deploying, or approved and not yet deployed."""
    if d["answer"] == "waiting":
        return "waits on the user's word"
    if d["answer"] == "replaced" and d.get("spent"):
        return f"approved, then the deploy of {d['spent'][:7]} ended first"
    if d["answer"] == "replaced":
        return "approved, then the word went to a newer offer" if d["word"] else "replaced by a newer offer, unanswered"
    if d["ended"]:
        failed = next((x["step"] for x in d["steps"] if x["outcome"] == "failed"), None)
        return f"{d['outcome'] or 'ended'} {local(d['ended'])}" + (f" at the {failed}" if failed else "")
    if d["started"]:
        return f"deploying since {local(d['started'])}"
    return "approved, not yet deployed"


def deploy_fields(env, d):
    """A deploy on one line: its environment, the commit and the one it comes from, where it stands, whose word it was
    deployed on, and the bolts it carries, or why the record can't tell."""
    frm = "from nothing deployed" if d["from"] in (None, "", "none") else f"from {d['from'][:7]}"
    carries = (f"carrying {', '.join(d['bolts'])}" if d["bolts"] else "carrying no landing") if d["bolts"] is not None else f"carrying what can't be read: {d['bolts_why']}"
    return fields(env, f"deploy {d['to'][:7]} {frm}", deploy_state(d), f"approved by {d['word']['by']}" if d["word"] and d["word"]["by"] else "",
                  (carries, "dim"))


def waiting_fields(env, w):
    """An operation waiting on an environment: its key, who has it, held for the user's word or not, a deploy waiting
    at its gate for the user (plan.14), and its first line or note."""
    said = {"handed": f"handed to {w['agent'] or w['doer']}", "failed": "failed"}.get(w["state"]) or (
        "waits at its gate for the user" if w.get("gate") else
        "waits on the user" if w["doer"] == "user" else
        f"held for the user's word, for {w['agent'] or w['doer'] or 'its doer'}" if w.get("held") else
        f"waits for {w['agent'] or w['doer'] or 'its doer'}")
    return fields(env, w["key"], said, w["text"] or w["note"] or "")


def board_text(data, width=None, color=False, stale=None):
    """The board as text: for each drive a header, the four lanes in order, each a bold heading with its objects
    under it or none, then attention. A marker sits in a two-column gutter at the left of its object's line, its card
    said at the line's end. Each line is cut to width when that is given; bold and dim only with color. stale, when
    given, is how long ago the board was read, said in its header."""
    out = []
    read_at = plan.utc(data["read_at"])

    def line(segs, gutter=None, indent=0, ms=()):
        """One line: a header or heading at the left edge, or, with a gutter, an object, its marker in the gutter."""
        segs = row(segs, gutter, indent, ms)
        text, n = "", 0
        for s, style in segs:
            if width is not None:
                s = s[:max(0, width - n)]
            n += len(s)
            text += f"{STYLES[style]}{s}\033[0m" if color and style and s else s
        out.append(text.rstrip())

    def heading(name):
        line([(name, "bold")])
    for i, p in enumerate(data["drives"]):
        if i:
            out.append("")
        answered = [h for h, v in p["hosts"].items() if v is True]
        line([(f"{p['label']} board, as of {read_at.astimezone():%H:%M:%S}" + (f" ({stale} ago: the host's follower has not refreshed it since)" if stale else "")
                      + f", read from {', '.join(answered) or 'no host'}", None)])

        heading("Inception")
        sigs, groups = p["inception"]["signals"], {}
        for s in sigs:
            groups.setdefault(s["captured_by"], []).append(s)
        for who, mine in groups.items():
            oldest = next((s["at"] for s in mine if when(s["at"])), None)
            said = "" if not oldest else f", the oldest captured {oldest}" if len(oldest) == 10 else f", the oldest captured {plan.age(when(oldest), read_at)} ago"
            line(gutter=" ", segs=fields(f"signals captured by {who or 'no one named'}", f"{len(mine)} not moved{said}"))
            for s in mine:
                line(fields(s["kind"] or "-", s["first"] or "", (s["signal"], "dim")), " ", 2)
        for e in p["inception"]["explorations"]:
            line(fields("exploration", named(e["kit"], e["name"]), e["first"] or ""), " ")
        if not sigs and not p["inception"]["explorations"]:
            line([("none", None)], " ")

        heading("Bolt plan")
        bp = p["bolt_plan"]
        for d in bp["proposals"]:
            line(fields(f"proposal {d['proposal']} by {d['by']}", d["case"] or ""), gutter(d["markers"]), 0, d["markers"])
        for b in bp["planned"]:
            line(fields(named(b["repo"], b["bolt"]), b["goal"] or ""), " ")
            for u in b["units"]:
                line(fields(u["unit"], stage_of(u)), " ", 2)
        for u in sorted(bp["queue"], key=lambda u: u["repo"] or ""):
            line(fields(named(u["repo"], u["unit"]), "chore queued" if u.get("kind") == "chore" else "queued", ", ".join(u["sources"])), " ")
        if not (bp["proposals"] or bp["planned"] or bp["queue"]):
            line([("none", None)], " ")

        heading("Construction")
        for b in p["construction"]:
            line(fields(named(b["repo"], b["bolt"]), f"on {b['host']}" if b["host"] else "", stream_of(b),
                        head_said(b), time_of(b)), gutter(b["markers"], needs_eye(b)), 0, b["markers"])
            for u in b["units"]:
                line(fields(u["unit"], stage_of(u), detail_of(u), u["url"] or ""), " ", 2)
            for f in b["fixes"]:
                line(fields(f["fix"], fix_stage(f), detail_of(f), f["url"] or ""), " ", 2)
            if b["url"]:
                line(fields("server", b["url"]), " ", 2)
        if not p["construction"]:
            line([("none", None)], " ")

        heading("Operation")
        for o in p["operation"]:
            line(gutter=" ", segs=fields(o["bolt"], f"landed {local(o['at'])}" + (f" by {o['by']}" if o["by"] else ""),
                               ", ".join(o["units"])))
        envs = p.get("environments", [])
        for e in envs:
            for d in e["deploys"]:
                line(deploy_fields(e["env"], d), gutter(d["markers"]), 0, d["markers"])
            for w in e["waiting"]:
                line(waiting_fields(e["env"], w), gutter(w["markers"]), 0, w["markers"])
        if not p["operation"] and not any(e["deploys"] or e["waiting"] for e in envs):
            line([("none", None)], " ")

        heading("attention")
        for a in p["attention"]:
            line([(attention_text(a), None)], ATTENTION)
        if not p["attention"]:
            line([("none", None)], " ")
    return "\n".join(out)


def attention_text(a):
    """What needs attention, as the board says it."""
    return {"host": f"{a['name']} did not answer ({a['why']})", "plan": f"the plan, {a['name']}: {a['why']}",
            "signals": f"the signals on {a['name']}: {a['why']}", "landed": f"bolt {a['name']}: {a['why']}",
            "runner": f"{a['name']} can't be read ({a['why']}): the stages of the work crossed to Flume there are unknown",
            "run": f"{a['name']}: {a['why']}"}[a["what"]]


# ------------------------------------------------------------------------------------------------- the agents' views

def many(n, one, more):
    return f"{n} {one if n == 1 else more}"


def pip(u):
    """A unit's stage as its pip; a crossed piece waiting on its caller as the stage it waits at, and one submitted as
    every task ticked."""
    st = u["stage"]
    if st in ("needs", "waits", "stalled") and (u.get("flume") or {}).get("of"):
        st = u["flume"].get("of")
    return PIP.get("verify" if st == "submitted" else st, "?")


def pips(units):
    """Units' stages as pips, one to a unit in the plan's order."""
    return "".join(pip(u) for u in units)


def merged(b):
    return f"{sum(u['stage'] in ('merged', 'landed') for u in b['units'])} of {len(b['units'])} merged"


def state_said(state):
    """A started bolt's state as a line draws it: nothing while active, "waits to land" once proven (teams.16), else the
    state."""
    return "" if state == "active" else "waits to land" if state == "waits" else state


def time_of(b):
    """A held bolt's age and who held its time, as its head line ends with them (plan.time_said, plan.20); nothing for
    a ledger made without it."""
    return (b.get("time") or {}).get("said") or ""


def landing_of(entries, bolt):
    """What the run record holds of a held bolt's landing for its head line, its ledger's record (plan.21, Decision 5),
    from the drive's entries the rail read, oldest first, each state its own: {state: unclosed, words} once its last
    bolt.submit landed and its last bolt.land since is refused, in that refusal's words; else its landing queued, landing
    again or rejected as plan.landing_phase reads it (bolt-teams "A bolt's landing reads queued, rejected or landing again from the run record"); else None. A
    decision of facts alone (code.7)."""
    last, refused = None, None
    for e in entries:
        if f"bolt/{bolt}" not in (e.get("On") or []):
            continue
        if e.get("Act") == "bolt.submit":
            last, refused = e, None
        elif e.get("Act") == "bolt.land":
            refused = e.get("Refused")  # None once a close went through
    if last and last.get("Outcome") == "landed" and refused:
        return {"state": "unclosed", "words": refused}
    return plan.landing_phase(entries, bolt)


def unclosed(b):
    """The words of a held bolt's last refused close, once it landed on main and was not closed (landing_of), or None."""
    record = b.get("record") or {}
    return record["words"] if record.get("state") == "unclosed" else None


def head_said(b):
    """A held bolt's state as its head line says it, from what the run record holds of its landing (its record,
    landing_of): landed on main and not closed, in its last refused close's words; its landing queued, landing again or
    rejected at its head, each in words of its own with its number (plan.phase_said); else its state (state_said)."""
    if unclosed(b):
        return f"landed on main, not closed: {unclosed(b)}"
    return plan.landing_line(b.get("landing"), b.get("record"), b.get("head"), b.get("bolt")) or state_said(b["state"])


def record_landing(b):
    """A held bolt's landing as ops's band names it (crew-lands-each-bolt-through-flumes-base-place, Decision 10): one in
    flight, asked of the runner with its land's request, or in the merge queue with its entry and its state, as the
    runner reports it and the run record holds it (plan.landing_line), or queued or landing again as an older crew
    recorded it, with its number; nothing for any other state or none."""
    record, landing = b.get("record") or {}, b.get("landing") or {}
    if landing.get("outcome") in ("asked", "submitted") or record.get("state") in ("queued", "again", "asked"):
        return plan.landing_line(landing if landing.get("outcome") in ("asked", "submitted") else None, record, b.get("head"),
                                 b.get("bolt")) or ""
    return ""


def legacy(b):
    """Whether a held bolt was started before bolts were base places, and lands under the crew that started it (its
    landing's outcome legacy; crew-lands-each-bolt-through-flumes-base-place, Decision 9)."""
    return (b.get("landing") or {}).get("outcome") == "legacy"


def needs_eye(b):
    """Whether a held bolt's head line has the attention gutter: every unit of it landed, or its close refused."""
    return b["state"] == "landed" or bool(unclosed(b))


def bolt_row(b):
    """A started bolt on one line, led by its product, the repository it builds; then its pips, its name, its stream
    (stream_of), its state unless active, or what its landing is (head_said), how many of its units have merged, and its
    age and who held its time (time_of); its landing's marker in the gutter, or attention once every unit has
    landed or its close was refused (needs_eye). A bolt marked to stay says so beside its name (record 0067)."""
    return row(fields(b["repo"] or "", pips(b["units"]), b["bolt"], ("stays", "dim") if b.get("stays") else "", stream_of(b), head_said(b),
                      merged(b), time_of(b)), gutter(b["markers"], needs_eye(b)), 0, b["markers"])


def ledger_rows(b):
    """A started bolt as a ledger: the bolt (bolt_row), then a unit or chore to a line, its pip, its stage and what goes
    with it, a submission among it as the runner carries it, then each fix with its stage; no slot."""
    return ([bolt_row(b)]
            + [row(fields(pip(u), u["unit"], stage_of(u), detail_of(u)), " ", 2) for u in b["units"]]
            + [row(fields(f["fix"], fix_stage(f), detail_of(f)), " ", 2) for f in b["fixes"]])


def in_flight(p):
    """The drive's started bolts, product by product, each kit's in the plan's order."""
    return sorted(p["construction"], key=lambda b: b["repo"] or "")


def proposal_row(d):
    """An open proposal: who made it and its case; its marker in the gutter."""
    return row(fields(f"proposal {d['proposal']} by {d['by']}", d["case"] or ""), gutter(d["markers"]), 0, d["markers"])


def next_rows(p):
    """What comes after the work in hand: for each product, the repository it builds, its first planned bolt, the rest
    counted, then the queued units counted by product."""
    bp = p["bolt_plan"]
    planned, queued = bp["planned"], bp["queue"]
    out = []
    for repo in dict.fromkeys(b["repo"] for b in planned):
        mine = [b for b in planned if b["repo"] == repo]
        out.append(row(fields(repo or "", ("next", "dim"), mine[0]["bolt"], f"and {len(mine) - 1} more planned" if len(mine) > 1 else ""), " "))
    counts = {}
    for u in queued:
        counts[u["repo"] or "no repository"] = counts.get(u["repo"] or "no repository", 0) + 1
    return out + ([row(fields(("queued", "dim"), ", ".join(f"{n} in {r}" for r, n in counts.items())), " ")] if counts else [])


def attention_rows(p, keep=lambda a: True):
    return [row([(attention_text(a), None)], ATTENTION) for a in p["attention"] if keep(a)]


def hold_rows(p):
    """A line for each hold standing on the drive's landings or a kit's (Decision 7 of a-proven-bolt-lands-on-proof;
    crew-board "A bolt marked to stay is marked in the bands, and each hold opens them"): what it holds, its words, and
    that no land is posted until the user lifts it with crew plan go, in the attention gutter. They open a band below its
    head line rather than above it, so the head line keeps the crew its agent runs at its end (agent_views)."""
    return [row(fields(("held", "bold"), h["kit"] or f"every kit of {p['label']}", f"\"{h['why']}\"",
                       "no land is posted until the user lifts it with crew plan go"), ATTENTION) for h in p.get("holds") or []]


def planner_view(p):
    """The planner's: the plan in brief, counting the places that wait on an answer (asking); each bolt in flight as a
    ledger (ledger_rows), since ordering within a bolt, batches and amendments are the planner's (Decision 6 of
    the-team-machinery-leaves), a place that waits on an answer drawn on its line with its question or Flume's words
    (crew-board "A question in the planner's band"); the open proposals, what is planned next and queued, and what needs
    attention. Each hold standing opens it, below its head line (hold_rows)."""
    bp, asking = p["bolt_plan"], p.get("asking", [])
    head = row(fields((f"{p['label']} plan", "bold"), f"{len(p['construction'])} in flight", f"{len(bp['planned'])} planned",
                      f"{len(bp['queue'])} queued", many(len(bp["proposals"]), "proposal open", "proposals open"),
                      many(len(asking), "place waits on an answer", "places wait on an answer") if asking else ""))
    return ([head] + hold_rows(p) + [r for b in in_flight(p) for r in ledger_rows(b)] + [proposal_row(d) for d in bp["proposals"]]
            + next_rows(p) + attention_rows(p))


def record_row(r):
    """A decision record proposed and not yet accepted or rejected, as the design agent reads it: the kit, dim, and the
    record's number, when it was proposed, and its card, open or none, or that the user's yes was given in the pane, so
    it has none."""
    ms = [] if r["settled"] else [{"glyph": "✓", "card": r["card"]}]
    return row(fields(named(r["kit"], f"record {r['number']}"), f"proposed {local(r['at'])}", "settled in the pane" if r["settled"] else ""),
               gutter(ms), 0, ms)


def design_view(p):
    """The design agent's: the signals no move has taken, counted by who captured them, the decision records proposed
    and not yet accepted or rejected with their cards, and the explorations on each kit's main, the first few named and
    the rest counted; and what keeps the signals or the plan from being read."""
    inc, groups, records = p["inception"], {}, p.get("records", [])
    for s in inc["signals"]:
        groups.setdefault(s["captured_by"], []).append(s)
    es = inc["explorations"]
    head = row(fields((f"{p['label']} inception", "bold"), many(len(inc["signals"]), "signal not moved", "signals not moved"),
                      many(len(records), "record proposed", "records proposed") if records else "",
                      many(len(es), "exploration", "explorations")))
    return ([head]
            + [row(fields(f"signals captured by {who or 'no one named'}", f"{len(mine)} not moved"), " ") for who, mine in groups.items()]
            + [record_row(r) for r in records]
            + [row(fields(named(e["kit"], e["name"]), e["first"] or ""), " ") for e in es[:SHOWN]]
            + ([row(fields(("and " + many(len(es) - SHOWN, "more exploration", "more explorations"), "dim")), " ")] if len(es) > SHOWN else [])
            + attention_rows(p, lambda a: a["what"] in ("plan", "signals")))


def environment_row(e):
    """An environment in brief: its latest deploy, where it stands, and how many operations wait on it; the marker of a
    deploy or an operation of it waiting on the user in the gutter."""
    ms = [m for d in e["deploys"] for m in d["markers"]] + [m for w in e["waiting"] for m in w["markers"]]
    d = e["deploys"][0] if e["deploys"] else None
    return row(fields(e["env"], f"deploy {d['to'][:7]}  {deploy_state(d)}" if d else "",
                      many(len(e["waiting"]), "operation waiting", "operations waiting") if e["waiting"] else ""), gutter(ms))


def operator_view(p):
    """An operator's: the drive's board in brief, a line to each lane with each bolt in flight under Construction
    (bolt_row) and each environment with a deploy or an operation waiting under Operation, the rail's rows waiting on the user counted,
    and what needs attention."""
    inc, bp, lands, envs = p["inception"], p["bolt_plan"], p["operation"], [e for e in p.get("environments", []) if e["deploys"] or e["waiting"]]
    approve = (sum(len(d["markers"]) for d in bp["proposals"]) + len({m["key"] for b in p["construction"] for m in b["markers"]})
               + sum(len(x["markers"]) for e in envs for x in e["deploys"] + e["waiting"]))  # a kit's landing row once, whatever it names
    last = f"the last {lands[0]['bolt']}, {plan.utc(lands[0]['at']).astimezone():%a %H:%M}" if lands else ""
    return ([row(fields((f"{p['label']} board", "bold"), f"read from {', '.join(h for h, v in p['hosts'].items() if v is True) or 'no host'}")),
             row(fields(("Inception", "bold"), many(len(inc["signals"]), "signal not moved", "signals not moved"),
                        many(len(inc["explorations"]), "exploration", "explorations"))),
             row(fields(("Bolt plan", "bold"), many(len(bp["proposals"]), "proposal open", "proposals open"), f"{len(bp['planned'])} planned",
                        f"{len(bp['queue'])} queued")),
             row([("Construction", "bold")])]
            + [bolt_row(b) for b in in_flight(p)]
            + [row(fields(("Operation", "bold"), f"{len(lands)} landed in seven days", last))]
            + [environment_row(e) for e in envs]
            + ([row(fields(("waits on the user", "bold"), f"✓ {approve} to approve"))] if approve else [])
            + attention_rows(p))


def ops_view(p):
    """Main-level ops's: the drive's operations in brief; each fix of a kit's main, each take-main fix in flight and
    each landing fix Flume runs on a bolt, with its stage (fixing; crew-board "A fix of main in ops's band" and "Ops's
    band lists each landing fix Flume runs on a bolt"); each kit's landing row, its landings card ops's, naming
    the bolts that wait on its main in the plan's order, each with its landing asked of the runner with its request or
    in the merge queue with its entry (record_landing), with its card, saying crew asks the runner to land what the user
    ticked once they have answered it, and each started bolt whose landing stands on no such row; the head line of each
    bolt that landed on main and whose close was refused, with its words (plan.21), and of each bolt started before
    bolts were base places, which lands under the crew that started it (legacy); then, environment by environment, each
    deploy waiting on the user's word with its card, each approved and not yet deployed, each running, and each
    operation step waiting, handed or failed, with the deploy it comes after, or whose gate it is, and its doer; and
    what keeps a host or the plan from being read. Each hold standing opens it, below its head line (hold_rows)."""
    pending = [(e["env"], d) for e in p.get("environments", []) for d in e["deploys"] if not d["ended"] and d["answer"] != "replaced"]
    steps = [(e["env"], w) for e in p.get("environments", []) for w in e["waiting"]]
    word = sum(d["answer"] == "waiting" for _, d in pending)
    running = sum(bool(d["started"]) for _, d in pending)
    fixing = p.get("fixing", [])
    head = row(fields((f"{p['label']} operations", "bold"), many(word, "deploy waits on the user's word", "deploys wait on the user's word"),
                      many(running, "deploy running", "deploys running"), many(len(steps), "operation waiting", "operations waiting"),
                      many(len(fixing), "fix in flight", "fixes in flight") if fixing else ""))
    out = [head] + hold_rows(p) + [row(fields(f["repo"] or "", f"fix {f['fix']}", f["stage"], f["said"], (f"on {f['host']}", "dim")), " ")
                                    for f in fixing]
    lands = {}
    for b in p.get("construction", []):
        for m in b["markers"]:
            if m["group"] == "land":
                lands.setdefault(m["key"], (m, []))[1].append(b["bolt"])
    marked = {b["bolt"] for b in p.get("construction", []) if b.get("stays")}  # a bolt marked to stay says so (record 0067)

    def named_(x):
        return f"{x} stays" if x in marked else x
    landing = {b["bolt"]: f"{named_(b['bolt'])} {record_landing(b)}" for b in p.get("construction", []) if record_landing(b)}
    for key, (m, bolts) in lands.items():  # a card the user answered: crew carries the send to the runner (Decision 4)
        out.append(row(fields(key, ", ".join(landing.get(x, named_(x)) for x in bolts), "wait to land" if len(bolts) > 1 else "waits to land",
                              "answered: crew asks the runner to land what the user ticked" if m["card"] and m["card"].get("answered") else ""),
                       gutter([m]), 0, [m]))
    rowed = {x for _, bolts in lands.values() for x in bolts}
    out += [row(fields(b["repo"] or "", named_(b["bolt"]), record_landing(b)), " ") for b in p.get("construction", [])
            if record_landing(b) and b["bolt"] not in rowed]
    out += [bolt_row(b) for b in p.get("construction", []) if unclosed(b) or legacy(b)]
    for e in p.get("environments", []):
        for d in (d for env, d in pending if env == e["env"]):
            out.append(row(fields(e["env"], f"deploy {d['to'][:7]}", deploy_state(d)), gutter(d["markers"]), 0, d["markers"]))
        for w in (w for env, w in steps if env == e["env"]):
            doer = (w["doer"] or "no doer named") + (f", {w['agent']}" if w["agent"] else "") + (", held for the user's word" if w.get("held") else "")
            of = (f"gate of {w['to'][:7]}" if w["to"] else "gate") if w.get("gate") else f"after {w['to'][:7]}" if w["to"] else ""
            out.append(row(fields(e["env"], w["key"], (of, "dim") if of else "", w["state"], f"doer {doer}"),
                           gutter(w["markers"]), 0, w["markers"]))
    return out + attention_rows(p, lambda a: a["what"] in ("host", "plan"))


def run_rows(r, now):
    """A role's run's own lines, at the head of its view (crew-board "A role that runs as its kind has its view"): its
    name and stream, what its turn took, the ends Flume held for the role among it counted and never listed (design
    Decision 7 of crews-role-runs-confirm-what-they-collect), and how many asks wait for the role's next run and for how
    long the oldest has, or that nothing waits; then each ask and waiting place the turn took, an ask by its number with
    what it is, who asked and the record it names, a waiting place by its key."""
    t = r["turn"]
    ends = t.get("ends", 0) if t else 0
    took = "no turn taken" if t is None else f"turn {t['turn']} took {len(t['took'])}" + (
        f" and {ends} {'end' if ends == 1 else 'ends'}" if ends else "") + (", ended" if t["ended"] else "")
    n, since = r["waiting"], when(r["since"]) if r["since"] else None
    old = plan.age(since, now) if since else "a time crew can't read"
    waits = ("nothing waits" if not n else f"1 ask waits, for {old}" if n == 1 else f"{n} asks wait, the oldest for {old}")
    head = row(fields((f"{r['run']} run", "bold"), f"in stream {r['stream']}", took, waits))
    return [head] + [row(fields(f"ask {x['took'][4:]}" if x["took"].startswith("ask/") else x["took"],
                                f"{x['what']} from {x['from']}" if x["what"] else "", f"on {x['names']}" if x["names"] else ""), " ")
                     for x in (t["took"] if t else [])]


def card_line(c, now):
    """An open card of an agent's own, as its band shows it above its view: its question or the row's card, its key,
    its id, dim, and how long it has been open, or, once the user has answered it, how long ago and that it is the
    agent's to act on (crew-board "An agent's band says which of its cards the user answered")."""
    what = {"question": "your question", "record": "your record's card"}.get(c["kind"], "your card")
    since = (f"answered {plan.age(when(c['answered']), now)} ago, yours to act on" if c.get("answered") else
             f"open {plan.age(when(c['at']), now)}")
    return row(fields(what, c["key"] or "", (c["card"], "dim"), since), " ")


def agent_views(data):
    """Each crew agent's view of its drive's board, by the agent's name, for the band crew's mod draws above its
    prompt (plugin/hooks/status.js): the planner's, the design agent's, main-level ops's and the drive's operator's,
    and no other standing agent's (Decision 11 of the-team-machinery-leaves), every line a list of (text, style)
    segments; and each role's run the drive runs as its kind, under the run's name, <label>-<role>, its own lines
    first (run_rows) and then its role's view, the reviewer's its own lines alone (crew-board "A role that runs as its
    kind has its view"). With what this host's agents run of crew (data's `here`, here_read), each standing agent here
    with a recorded start has the crew it started on at the end of its view's first line, with the version it is
    restarted on at its next stop once an update made it due; and while this host is held every view opens with the
    hold (teams.19). The planner's and ops's views open, below their head lines, with each hold standing on the drive's
    landings or a kit's, and every bolt line marks a bolt marked to stay (hold_rows, bolt_row; Decision 7 of
    a-proven-bolt-lands-on-proof). Any other agent has no view, and its mod draws nothing.
    Beside them, cards: each of those agents' open cards, oldest first, its questions among them, by the agent's name,
    the lines the mod draws above its view. With them, the line the mod draws in place of the view and the cards once
    the frame is stale_after_ms old, so a band names no bolt that has landed since, nor a card closed since (read.1):
    the day and time it was read, since a frame a restart or a follower that stopped left can be days old, and that the
    host's follower has not refreshed it since.

    A change to what crew models (bolts, units, stages, proposals, explorations and elaborations, cards, rail rows)
    changes these views and plugin/hooks/status.js with it, each with its cases (code.8)."""
    views, cards, now = {}, {}, plan.utc(data["read_at"])
    for p in data["drives"]:
        views.update({f"{p['label']}-planner": planner_view(p), f"{p['label']}-design": design_view(p), f"{p['label']}-ops": ops_view(p)})
        views[f"{p['label']}-operator"] = operator_view(p)
        for r in p.get("runs", []):  # a role's run, under the name its standing agent had, its own lines first
            views[r["run"]] = run_rows(r, now) + views.get(r["run"], [])
        for c in p.get("cards", []):
            cards.setdefault(c["by"], []).append(card_line(c, now))
    here = data.get("here")
    if here:
        for name, f in here["agents"].items():  # each a main-level role (crew.agents_here), which has a view
            if views.get(name):
                views[name] = [views[name][0] + [("  ", None), (crew_said(f, here["version"]), "dim")]] + views[name][1:]
        if here["held"]:
            views = {name: [held_row(here["host"], here["held"])] + v for name, v in views.items()}
    return {"read_at": data["read_at"], "stale_after_ms": STALE * 1000,
            "stale": row([(f"crew: the board was last read at {local(data['read_at'])}, too long ago to show; crew's follower on "
                           f"{data['from']} has not refreshed it since", "dim")]),
            "views": views, "cards": {a: lines for a, lines in cards.items() if a in views}}


def crew_said(f, now):
    """The crew an agent runs, as its band says it (teams.19): the version it started on, or that it started on a crew
    older than crew's versions in its bands; and once an update made it due a restart, the version it is restarted on
    at its next stop."""
    was = f"crew {f['version']}" if f["version"] else "an older crew"
    return f"{was} \u2192 {now or 'crew as it now is'} at its next stop" if f["due"] else was


def held_row(host, h):
    """The line every band on a held host opens with (teams.19): who held it, since when, and why."""
    since = f" since {h['at']}" if h.get("at") else ""
    return row([(f"{host} is held", "bold"), (f" by {h['by']}{since}: {h['why']}. Start nothing new; crew go {host} lifts it", None)])


def here_read(fleet, label):
    """What this host's agents of a drive run of crew, for their bands (agent_views): this host, the version of the
    crew it has installed (crew.installed), which a due agent takes at its next stop, its hold, and each main-level role
    of the drive here with a recorded start, by name (crew.agents_here): the version it started on, and whether an
    update has made it due a restart (crew.due_of), judged against the installed crew."""
    now = crew.installed()
    version = now["version"]
    started, agents = crew.starts(), {}
    for name in crew.agents_here(fleet, label):
        if name in started:
            due, _, _ = crew.due_of(fleet, name, started[name], now)
            agents[name] = {"version": started[name]["version"], "due": due}
    return {"host": crew.this_host(), "version": version, "held": crew.held(), "agents": agents}

# ------------------------------------------------------------------------------------------------- the board tab

def frame_path(label):
    return FRAMES / f"{label}.json"


def agents_path(label):
    """The agents' views beside the board's frame, which crew's mod reads (plugin/hooks/status.js)."""
    return FRAMES / f"{label}.agents.json"


def write_frame(label, data, path=None):
    """The board's data for the board tab, or the agents' views for their mods at path, written whole: a temporary
    file in the same folder, then moved over the last one, so no reader ever reads half of one."""
    FRAMES.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=FRAMES, prefix=f".{label}.")
    try:
        with os.fdopen(fd, "w") as f:
            f.write(json.dumps(data, indent=1) + "\n")
        os.replace(tmp, path or frame_path(label))
    except OSError:
        os.unlink(tmp)
        raise


def no_frame(label):
    return (f"No board for {label} yet: the host's follower writes it each time it refreshes, swancloud's job or the console's "
            f"rail tab, which crew console up {label} opens while no job runs.")


def frame_text(label, data, width, color, now):
    if data is None:
        return no_frame(label)
    read_at = plan.utc(data["read_at"])
    stale = plan.age(read_at, now) if (now - read_at).total_seconds() > STALE else None
    return board_text(data, width, color, stale)


def read_frame(label):
    try:
        data = json.loads(frame_path(label).read_text())
        return data if isinstance(data, dict) and plan.utc(data.get("read_at")) and isinstance(data.get("drives"), list) else None
    except (OSError, ValueError, AttributeError):
        return None


def follow(label, once=False):
    """The board tab: the latest frame drawn at the pane's width, again whenever the frame, the pane's size or how
    stale the frame is changes; checked once a second."""
    tty = sys.stdout.isatty()
    color = tty and not os.environ.get("NO_COLOR")
    seen, data, mtime = None, None, False
    while True:
        try:
            m = frame_path(label).stat().st_mtime_ns
        except OSError:
            m = None
        if m != mtime:
            mtime, data = m, read_frame(label) if m is not None else None
        now = datetime.datetime.now(datetime.timezone.utc)
        width = shutil.get_terminal_size().columns if tty else None
        text = frame_text(label, data, width, color, now)
        if (text, width) != seen:
            seen = (text, width)
            sys.stdout.write(("\033[H\033[2J" if tty else "") + text + "\n")
            sys.stdout.flush()
        if once:
            return
        time.sleep(1)


# ------------------------------------------------------------------------------------------------- the host's follower

def lock_path():
    """The host's follower lock, beside the frames the follower writes."""
    return FRAMES / "follower.lock"


def lock_follower(kind, label=None, wait=True):
    """The host's follower lock taken for a follower of kind job (crew _follow) or tab (a rail tab, of label): an OS lock
    on the open file, which the caller keeps open for as long as it follows, so the OS lifts it when the follower ends,
    however it ends, and nothing is left to go stale (state.4). Once taken, the file says who holds it, `job <pid>
    <time>` or `tab <label> <pid> <time>`. With wait it waits for the lock, reading nothing meanwhile; without, None
    when another holds it. A follower started again as crew moved (Follower.again) adopts the lock it held, its open
    file handed on across the exec, so the host is never without its follower between the two."""
    held = os.environ.pop("CREW_FOLLOWER_LOCK", None)
    if held:
        try:
            return os.fdopen(int(held), "a+")
        except (OSError, ValueError):
            pass
    FRAMES.mkdir(parents=True, exist_ok=True)
    f = open(lock_path(), "a+")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | (0 if wait else fcntl.LOCK_NB))
    except BlockingIOError:
        f.close()
        return None
    f.truncate(0)
    f.write(" ".join([kind] + ([label] if kind == "tab" else []) + [str(os.getpid()), iso(datetime.datetime.now(datetime.timezone.utc))]) + "\n")
    f.flush()
    return f


def follower_of(line, free):
    """Who follows on the host, from the lock's line and whether the lock was free: none when it was free, job or tab
    as the line says, and unknown when the line is neither, as one read between a holder's lock and its write would be
    (read.1)."""
    if free:
        return "none"
    words = (line or "").split()
    if words[:1] == ["job"] and len(words) == 3:
        return "job"
    if words[:1] == ["tab"] and len(words) == 4 and re.fullmatch(r"[a-z0-9][a-z0-9-]*", words[1]):
        return "tab"
    return "unknown"


def follower_here():
    """Who follows on this host (follower_of): the lock tried without waiting, and released at once when it was free;
    when it is held, the holder's line read."""
    FRAMES.mkdir(parents=True, exist_ok=True)
    with open(lock_path(), "a+") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            f.seek(0)
            return follower_of(f.readline(), False)
        fcntl.flock(f, fcntl.LOCK_UN)
        return follower_of(None, True)


def labels_here(fleet, host):
    """The drives with an operator session on the host, which its follower refreshes: those the teams file's `consoles`
    names, for the host the file is written on alone, as crew.operator_session reads it, in the teams file's order, and
    none on another host (record 0064)."""
    consoles = fleet.get("consoles") or {}
    if not consoles or host != crew.this_host():
        return []
    return [l for l in fleet["drives"] if l in consoles]


def rail_path(label):
    """The rail's frame beside the board's: the rail as the follower's last round printed it, which the rail tab draws."""
    return FRAMES / f"{label}.rail.json"


def read_rail(label):
    try:
        data = json.loads(rail_path(label).read_text())
        return data if isinstance(data, dict) and plan.utc(data.get("read_at")) and isinstance(data.get("text"), str) else None
    except (OSError, ValueError, AttributeError):
        return None


def rail_frame_text(label, data, now):
    """The rail tab's text: the rail as the follower's last round printed it, with what handing out the due restarts
    said when that round did; headed with its age once it is older than STALE; and, when there is none, that the host's
    follower writes it."""
    if data is None:
        return (f"No rail for {label} yet: the host's follower writes it each time it refreshes, swancloud's job or the "
                f"console's rail tab, which crew console up {label} opens while no job runs.")
    read_at = plan.utc(data["read_at"])
    head = (f"{label}'s rail as read at {read_at.astimezone():%Y-%m-%d %H:%M:%S}, {plan.age(read_at, now)} ago: the host's follower"
            f"{' on ' + data['from'] if data.get('from') else ''} has not refreshed it since\n\n") if (now - read_at).total_seconds() > STALE else ""
    return head + data["text"] + (f"\n\n{data['updated']}" if data.get("updated") else "")


def moved(kept, now):
    """What moved between the stamps the follower's last read was made at (kept) and the stamps now (now), each
    {"crew": (crew's head, the teams file's bytes), "state": {label: tip}, "runners": {label: {host: tip}},
    "blueprints": {label: tip}, "kits": {(host, main): stamp}, "readings": {host: stamp}, "cards": cards_stamp's}, a tip ""
    for a branch the cache does not hold: whether crew's checkout or
    the teams file moved, the labels whose state tip or one of whose runners' branches moved, which the read rests on
    as it rests on the drive's own, and whose blueprints tip moved, the kits that moved, the hosts whose card
    readings folders moved, whether the cards
    moved, whether anything the read rests on moved (read: a tip, a kit or crew), and
    whether anything did. A stamp None, which could not be read, counts as moved, as does one either side lacks
    (read.1); with no kept read, everything has moved. A decision on plain facts (code.7)."""
    if kept is None:
        return {"crew": True, "state": set(now["state"]), "blueprints": set(now["blueprints"]), "kits": set(now["kits"]),
                "readings": set(now.get("readings", {})), "cards": True, "read": True, "any": True}

    def apart(a, b):
        return {k for k in a.keys() | b.keys() if a.get(k) is None or b.get(k) is None or a[k] != b[k]}
    out = {"crew": None in kept["crew"] or None in now["crew"] or tuple(kept["crew"]) != tuple(now["crew"]),
           "state": apart(kept["state"], now["state"]) | apart(kept.get("runners", {}), now.get("runners", {})),
           "blueprints": apart(kept["blueprints"], now["blueprints"]),
           "kits": apart(kept["kits"], now["kits"]), "readings": apart(kept.get("readings", {}), now.get("readings", {})),
           "cards": kept.get("cards") != now.get("cards")}
    # a kit's main the clock's fetch moved (look's mains) is read again, its started bolts read on it (Decision 7)
    read = bool(out["crew"] or out["state"] or out["blueprints"] or out["kits"] or apart(kept.get("mains", {}), now.get("mains", {})))
    return dict(out, read=read, any=read or bool(out["readings"]) or out["cards"])


def cards_stamp(found, why, left, asks, listed=None, owned=None):
    """What the follower's check compares of the cards (Decisions 3 and 8 of a-rail-refresh-after-no-change-reads-nothing):
    of each card Pending You was asked after at the clock's last ask (plan.cards_fetched, found {card: (got, words)}),
    whether it answered it lost, the fact the card sweep acts on, [[card, lost]], of each card read in its owner's name
    at that ask (plan.owners_read, owned {card: (got, words)}), its status or that it was refused, [["owned", card,
    state]], since an answer or an end the sweep records is read there (Decision 2 of
    a-wait-on-the-user-is-one-open-card-the-rail-agrees-with), and of each asker herdr was asked
    about with it (plan.askers_listed, listed {name: (listed, why)}), whether its pane holds an agent, [["asker",
    name, listed]]; but the ask itself, ["again", asks], the count of asks made, when its bridge failed (why) or the
    last card sweep left a card, its act not gone through (left), so the cards count as moved at each ask until the
    sweep acts, and only at an ask (cards_due), never at a tick that asks nothing (Decision 2 of
    a-followers-tick-reads-nothing-while-nothing-moved). A decision on plain facts (code.7)."""
    if why is not None or left:
        return ["again", asks]
    return sorted([card, plan.cards.lost(words)] for card, (_, words) in found.items()) + sorted(
        ["owned", card, "refused" if words is not None else str((got or {}).get("status"))] for card, (got, words) in (owned or {}).items()) + sorted(
        ["asker", name, here] for name, (here, _) in (listed or {}).items())


def kept_stamp(kept, left, asks, listed):
    """cards_stamp of the follower's kept answers (kept, plan.cards_fetched's (found, why) or (found, why, owned))."""
    found, why, *owned = kept
    return cards_stamp(found, why, left, asks, listed, owned[0] if owned else None)


def card_left(swept):
    """Whether a card sweep (plan.sweep_cards) left a card or a drive unswept, its act not gone through: what the
    clock's next tick tries again (cards_stamp). A landings card left as the user answered it, waiting on its owner to
    land what they ticked (plan.WAITS_ON_OWNER), is no act that did not go through: the landing's own entry moves the
    record, and the read after it sweeps the card."""
    return bool(swept) and (any(d["did"] == "left" and not (d["words"] or "").startswith(plan.WAITS_ON_OWNER) for d in swept["done"])
                            or bool(swept["unswept"]))


def routes_moved(kits, asked):
    """The hosts whose portless routes the clock's tick read (asked, {host: routes}) differ from those a kit answer of the
    kept read holds there (kits, {host: {main: (request, answer)}}): their routes are drawn again with nothing
    gathered (Decision 8 of a-rail-refresh-after-no-change-reads-nothing). A decision on plain facts (code.7)."""
    return {h for h, r in asked.items() if any(a.get("routes") != r for _, a in kits.get(h, {}).values() if (a or {}).get("ok"))}


# seconds: the longest the follower goes without asking a host for its check, or Pending You and herdr after the cards,
# while nothing it reads says either moved (hosts_due, cards_due): what only they can say, a dev server started by hand,
# an exploration landed on a kit's main with no act of crew's, a card the user dismissed, is seen within it. The ten
# minutes the card sweep already leaves a refused card before trying it again (plan.CARD_RETRY).
DISCOVERY = plan.CARD_RETRY


def host_basis(host, labels, tips, runners):
    """What says something on a host could have moved (Decision 1 of a-followers-tick-reads-nothing-while-nothing-moved),
    read with no process: the branch of each drive the host serves (labels), its tip as this host's cache
    holds it (tips, {label: tip}), since every act on the host reaches that branch as it is written (read.5); and the
    host's own runner's branch of each (runners, {label: {host: tip}}), where its runner reports the places it runs, a
    piece's submission among them, so a submission's move is a move of its runner's branch (crew record 0056 points 1
    and 4). Text, compared whole (hosts_due). A decision on plain facts (code.7)."""
    return json.dumps([[l, tips.get(l), (runners.get(l) or {}).get(host)] for l in sorted(labels)])


def hosts_due(bases, asked, now):
    """The hosts the follower asks (Decision 1 of a-followers-tick-reads-nothing-while-nothing-moved), from each host's
    basis now (bases, {host: host_basis}) and the basis and time each was last asked at and answered (asked, {host:
    (basis, at)}): each never asked or whose last ask went unanswered, whose basis moved since, or that was last asked
    DISCOVERY seconds ago or more; none other, so a refresh after nothing moved asks no host. A decision on plain facts
    (code.7)."""
    return sorted(h for h, b in bases.items() if h not in asked or asked[h][0] != b or now - asked[h][1] >= DISCOVERY)


def cards_due(cards, askers, answers, listed, at, now):
    """Whether the clock's tick asks Pending You after the cards and herdr after the askers its card sweep would judge
    (Decision 2 of a-followers-tick-reads-nothing-while-nothing-moved), from those it would ask after now (cards,
    askers), the last ask's answers ((found, why), plan.cards_fetched) and listing ({name: (listed, why)},
    plan.askers_listed), and when it was made (at): when there is any to ask after, and the last ask did not answer one
    of them, its bridge failed, herdr could not read an asker's pane, none was made, or it was made DISCOVERY seconds
    ago or more; never when there is none, which needs no bridge. A decision on plain facts (code.7)."""
    if not cards and not askers:
        return False
    if answers is None or listed is None or at is None or answers[1] is not None:
        return True
    return (any(c not in answers[0] for c in cards) or any(a not in listed or listed[a][0] is None for a in askers)
            or now - at >= DISCOVERY)


def fetches(fleet, labels, kits=()):
    """The clock's fetches (Decision 3 of a-followers-tick-reads-nothing-while-nothing-moved): each repository once, with
    every branch the follower reads of it, {repo: [ref]}, in the drives' order: each drive's branch,
    which brings its runners' branches beside it (plan.beside), and its first blueprints repo's main; then the main of
    each kit's repository in kits, those of the started bolts the follower's last read held (kit_mains), which a
    bolt's landing is read on (a-landed-bolt-is-closed-and-offered-no-more, Decision 7). A decision on plain facts
    (code.7)."""
    out = {}
    for l in labels:
        for repo, ref in (plan.state_of(fleet, l), (crew.drive_of(fleet, l)["blueprints"][0], "main")):
            if ref not in out.setdefault(repo, []):
                out[repo].append(ref)
    for repo in kits:
        if "main" not in out.setdefault(repo, []):
            out[repo].append("main")
    return out


def kit_mains(fleet, read):
    """The repositories whose main the follower's clock fetches (a-landed-bolt-is-closed-and-offered-no-more, Decision
    7), from its last read: the forge address of the kit of each started bolt of each plan the read found, as
    plan.main_repository gives it over the drive's requests and runners the read holds, sorted, each once; none for a
    bolt not started, or one whose repository crew can't name by its owner. A decision on plain facts (code.7)."""
    runs, out = (read or {}).get("runs") or {}, set()
    for l, _, _, pl in (read or {}).get("found") or []:
        run = runs.get(l)
        for b in pl.bolts() if pl else []:
            if plan.started(b):
                repo = plan.main_repository(fleet, l, b, run if isinstance(run, tuple) else None)
                if repo:
                    out.add(repo)
    return sorted(out)


def crew_stamp():
    """What says the crew this host runs has moved, read with no process: where crew runs from a checkout, its commit,
    read from its files (crew.head_here); else the real path of the command of the crew the host has installed
    (crew.installed_here), a read of links each install moves; else None, which a refresh reads as unread and acts on
    with no update (read.1)."""
    if (crew.HOME / ".git").exists():
        return crew.head_here()
    cmd = crew.installed_here()
    return os.path.realpath(cmd) if cmd else None


def behind(mine, theirs):
    """Whether a follower runs a crew other than the one its host has installed (crew-board "A follower follows on the
    crew its host has installed"), from crew_read's facts of each (code.7): True when both name a commit and the commits
    differ, False when they name one, and None when either names none, which starts nothing again on a guess (read.1)."""
    if not (mine or {}).get("commit") or not (theirs or {}).get("commit"):
        return None
    return mine["commit"] != theirs["commit"]


def behind_here():
    """Whether this process follows on a crew other than the one its host has installed (behind): False, read with no
    process, where the installed command is this crew's own, as a checkout's always is, or the host has none, since
    then there is no other crew to follow on; else this build's release against the installed crew's answer to crew
    _release, asked once for each real path of the installed command (crew.installed), so a follower asks again only
    once an install moves it."""
    cmd = crew.installed_here()
    if cmd is None or crew.own_command(cmd):
        return False
    return behind(crew.crew_read(), crew.installed())


def moved_at():
    """What says crew or the teams file has moved since a refresh: crew's stamp (crew_stamp) and the teams file's bytes,
    each None when it can't be read."""
    try:
        teams = crew.TEAMS.read_bytes()
    except OSError:
        teams = None
    return (crew_stamp(), teams)


PERIOD = record.PERIOD  # seconds: the follower's clock, on which it fetches the state and blueprints caches (plan.12)
BURST = 2  # seconds: a look that sees a write waits this long for what follows, so a burst of writes is one refresh


def look(fleet, labels, kits=()):
    """What the follower's look reads each second, with no process (plan.12): crew's checkout and the teams file
    (moved_at), each drive's state and blueprints tips as this host's caches hold them (plan.tip_here), its
    runners' branches there (plan.runner_tips), where a runner's reports of the places it runs arrive with no move of
    the drive's own branch, and this host's card readings folders (gather.readings_stamp), so a reading sent back
    here is swept within seconds; and, as mains, the main of each kit's repository in kits (kit_mains) as this host's
    cache holds it, {repo: tip}, which the read hands in (a-landed-bolt-is-closed-and-offered-no-more, Decision 7),
    named mains since a refresh's stamps hold its kits' answers under kits."""
    return {"crew": moved_at(), "state": {l: plan.tip_here(*plan.state_of(fleet, l)) for l in labels},
            "runners": {l: plan.runner_tips(plan.state_of(fleet, l)[0], l, fetch=False) for l in labels},
            "blueprints": {l: plan.tip_here(crew.drive_of(fleet, l)["blueprints"][0], "main") for l in labels},
            "mains": {repo: plan.tip_here(repo, "main") for repo in kits},
            "readings here": gather.readings_stamp(readings_hosts(fleet, labels).get(crew.this_host(), []))}


def wake(now, tick_at, seen, looked):
    """What the follower does at a look (Decision 3 of a-rail-refresh-after-no-change-reads-nothing): "tick" once its
    clock's tick is due, when it fetches and then refreshes; "refresh" when what the look reads now (looked) is not what
    its last refresh rested on (seen), a write on this host having moved a cache, crew or the teams file; else None,
    and it reads nothing. A decision on plain times and tips (code.7)."""
    if now >= tick_at:
        return "tick"
    return "refresh" if looked != seen else None


def refresh_plan(m, kept, crew_read=True, lag=False):
    """What a refresh does, from what moved since its last read (moved), whether it kept one, whether crew's stamp
    (crew_stamp) and the teams file could be read then and now (crew_read), and whether the follower runs a crew other
    than the one its host has installed (lag, behind_here's): "update" while it does, with a read kept or none, before
    anything is read or swept, since a follower on another crew reads rows and judges their cards as that crew does,
    and one older than the host's withdraws as gone a row the installed crew reads and posts again (crew-board "A
    follower follows on the crew its host has installed"); "read" with none kept, its first, or when a tip or a kit
    moved, reading only what moved and running every sweep; "update" once crew's checkout, the crew the host has
    installed or the teams file moved, the due restarts handed out and the follower started again as the new crew, but
    a read when either can't be read, which hands out nothing on a guess (read.1); "sweep" when only a host's card
    readings folder, the cards or a host's routes moved, reading nothing, taking the routes into the kept read and
    running against it only the sweeps of what moved (sweeps_after); "render" when nothing moved, the frames written
    again from the kept read and the card sessions swept only on the hosts the last refresh could not check
    (plan.sessions_unchecked). A decision on plain facts (code.7)."""
    if lag:
        return "update"
    if not kept:
        return "read"
    if m["crew"]:
        return "update" if crew_read else "read"
    if m["read"]:
        return "read"
    return "sweep" if m["any"] else "render"


def sweeps_after(m, readings, unchecked):
    """The sweeps a refresh that reads nothing runs against its kept read (Decision 5 of
    a-rail-refresh-after-no-change-reads-nothing): the card sweep when the cards moved, with the clock's last answers;
    and the card session sweep on each host whose card readings folder moved, for each drive swept there
    (readings, {host: labels}), which is where a reading sent back is told to its owner, and on each host the last
    refresh could not check (unchecked, plan.sessions_unchecked), {label: hosts}; none other. A decision on plain facts
    (code.7)."""
    only = plan.sessions_unchecked(unchecked)
    for h in m["readings"]:
        for l in readings.get(h, ()):
            only.setdefault(l, set()).add(h)
    return {"cards": bool(m["cards"]), "sessions": only}


def readings_hosts(fleet, labels):
    """The hosts whose card readings folders the follower stamps, with the drives of each, {host: [labels]}: each
    drive's main machine and every host its runners answer on, as crew's cache holds their branches with no fetch
    (plan.drive_hosts, plan.12), where its card sessions are swept (plan.sweep_sessions)."""
    out = {}
    for l in labels:
        for h in plan.drive_hosts(fleet, l, fetch=False):
            out.setdefault(h, []).append(l)
    return out


def stamps_now(fleet, kits, readings, routes=(), hosts=None):
    """The follower's check of the hosts (plan.stamped): each kit's stamp now (gather.stamp), of the kits the last read
    surveyed, {host: {main: (request, answer)}}, by (host, main), and each host's card readings folders' stamp
    (gather.readings_stamp), of the drives readings names for it, by host: in this process on this host, in one ssh
    to each other, of the hosts named (hosts, every one when None) and no other (hosts_due). Every stamp of a host that
    did not answer is None, which moved() takes as moved (read.1). At the clock's tick, in the same request, the portless
    routes of each host routes names whose kits were surveyed, by host, one that did not answer left out. It asks no
    sluice."""
    out = {"kits": {}, "readings": {}, "routes": {}}
    for host in sorted(set(kits) | set(readings)):
        if hosts is not None and host not in hosts:
            continue
        ks = kits.get(host, {})
        got, why = plan.stamped(fleet, host, [req for req, _ in ks.values()], readings.get(host, ()), host in routes and bool(ks))
        out["kits"].update({(host, m): ((got or {}).get("kits") or {}).get(m) for m in ks})
        if host in readings:
            out["readings"][host] = (got or {}).get("readings")
        if got is not None and "routes" in got:
            out["routes"][host] = got["routes"]
    return out


def kept_stamps(kits):
    """The stamp each kit the last read used was read at, by (host, main), None for one whose host did not answer."""
    return {(host, m): (answer or {}).get("stamp") for host, ks in kits.items() for m, (_, answer) in ks.items()}


def here_key(head):
    """What here_read rests on besides the drive: crew's checkout and the teams file (moved_at), and the size and
    time of each agent's start record and of the host's hold file, read with no process; here_read is read again only
    when it moves."""
    try:
        starts = sorted((e.name, e.stat().st_size, e.stat().st_mtime_ns) for e in os.scandir(crew.SESSIONS))
    except FileNotFoundError:
        starts = []
    try:
        st = crew.HOLD.stat()
        hold = (st.st_size, st.st_mtime_ns)
    except FileNotFoundError:
        hold = None
    return json.dumps([head[0], head[1].decode(errors="replace") if head[1] else None, starts, hold])


def label_errors(errors, label):
    """The plans' errors of one drive's read: its branch's, named <label>/main of <repo>, or its plan's."""
    return {k: v for k, v in errors.items() if k.startswith(f"{label}/main of ") or k == f"the plan of {label}"}


# Pending You's notice for an always-on script, `pendingyou watch -- <command>` (pendingyou 0.39.0, read 2026-10-31):
# the command run once for each change on a card of the host's sign-in. What it and each crew _answered say, the
# follower's child's words, are appended here.
HEARD = FRAMES.parent / "heard.log"


def answers_watched(fleet, host):
    """Whether the host's follower runs Pending You's notice (design Decision 5 of roles-run-as-flume-kinds, role-runs
    "The follower hears Pending You's notice while a role here runs as its kind"): while a drive whose main level
    runs on the host names a role on demand in its `runs` (crew.on_demand), and only then, since the notice marks each
    change it hands in the host's Pending You state, which a session's pickup at its start reads."""
    return any(p["machine"] == host and any(crew.on_demand(p, r) for r in crew.KIND_ROLES) for p in fleet["drives"].values())


def notice_argv():
    """The notice the follower runs: Pending You's watch, running crew _answered for each change on a card, which asks
    a role whose run the card's asker is and reads nothing else of the card (plan.card_answered)."""
    return ["pendingyou", "watch", "--", "bash", crew.crew_command(), "_answered"]


class Follower:
    """The host's follower once it holds the lock (lock_follower): on its clock, every PERIOD seconds, it fetches each
    repository it reads once, every branch it reads of it in that one fetch (fetches), and refreshes; between ticks it
    looks each second at what this host's caches hold, crew's checkout, the teams file and this host's card readings
    folders, with no process, and refreshes within seconds when one moved. A refresh is one read, in this process, for
    every drive with an operator session on the host (labels_here), kept between refreshes (plan.Kept, state.4): it
    checks first whether anything the refresh acts on moved (moved) and then reads nothing when nothing did, or only
    what moved, running only the sweeps of what moved when no tip or kit did (sweeps_after); each drive's rail,
    board and agents' views are written from it. Its check asks another host only when something there could have
    moved (hosts_due): this host's kits and readings it stamps in this process each time. At a tick, and only then, it
    asks Pending You after the cards its card sweep would act on, and herdr after their askers, when something there
    could have moved (cards_due), in one bridge, and every sweep judges with those answers until the next ask. So a tick
    after nothing moved starts nothing but its fetches (Decisions 1 to 3 of
    a-followers-tick-reads-nothing-while-nothing-moved). It runs no sluice and keeps no submission of its own: a
    piece's submission is in its runner's report, so a submission's move reaches it as a move of the runner's branch,
    which its look reads and its clock fetches (crew record 0056 points 1 and 4). SIGUSR1 makes the next tick now."""

    def __init__(self, lock, period=PERIOD):
        self.lock, self.period, self.kept, self.last = lock, period, plan.Kept(), None
        self.labels, self.fleet_, self.tick_at, self.seen, self.unfetched, self.here = [], None, 0.0, None, {}, {}
        # the drives a refresh found a batch due for, by the state tip its read held and whether the tell went
        # through (plan.batch_told)
        self.told = {}
        # the asks of Pending You made, whether the last card sweep left a card, the cards' stamp (cards_stamp) as of the
        # last ask, and when that ask was made (cards_due), on the monotonic clock
        self.asks, self.left, self.cards, self.cards_at = 0, False, None, None
        # what each host was last asked at and answered, {host: (host_basis, monotonic time)}: for its check at any
        # refresh, and for its routes at a tick (hosts_due)
        self.asked, self.asked_at_tick = {}, {}
        # what handing out the restarts said before the follower started again as the new crew (again)
        self.updated = json.loads(os.environ.pop("CREW_FOLLOWER_UPDATED", "") or "{}")
        # whether this process was started again as the installed crew for running another (again's lag), and whether
        # it has said that it still runs another (lagging)
        self.started_lagging, self.said_lag = os.environ.pop("CREW_FOLLOWER_LAGGED", None) == "1", False
        # Pending You's notice while a role here runs as its kind (hear), None while it runs none
        self.notice = None
        # the repositories whose main the clock fetches, those of the started bolts of the last read (kit_mains)
        self.kits = []

    def fleet(self):
        """The teams file read afresh, not as this process first read it, the drives its `consoles` names followed
        (labels_here), and crew's Flume roles file kept from it (crew.keep_roles, teams.25); a teams file crew refuses
        leaves both as they were, said (read.1)."""
        crew.load.cache_clear()
        try:
            self.fleet_ = crew.load()
            self.labels = labels_here(self.fleet_, crew.this_host())
            crew.keep_roles(self.fleet_)
        except Refusal as e:
            print(f"crew's follower keeps the drives it had ({', '.join(self.labels) or 'none'}): {e}", file=sys.stderr)
        return self.fleet_

    def tick_now(self):
        self.tick_at = 0.0

    def fetch(self, fleet):
        """The clock's fetch: each repository once, every branch the follower reads of it in that one fetch (fetches,
        plan.tips_of), into this host's caches; what could not be fetched is said in each drive's frames until a
        fetch of it lands."""
        self.unfetched, failed = {}, {}
        for repo, refs in fetches(fleet, self.labels, self.kits).items():
            try:
                plan.tips_of(repo, refs)
            except Refusal as e:
                failed.update({(repo, ref): " ".join(str(e).split()) for ref in refs})
        for l in self.labels:
            for repo, ref in (plan.state_of(fleet, l), (crew.drive_of(fleet, l)["blueprints"][0], "main")):
                if (repo, ref) in failed:
                    self.unfetched.setdefault(l, {})[f"{ref} of {repo}"] = failed[(repo, ref)]

    def ask(self, fleet):
        """The clock's ask of Pending You after the cards the kept read's card sweep would act on (plan.cards_asked), in
        one bridge (plan.cards_fetched), and of herdr after the panes of the questions' askers (plan.askers_listed),
        made only when something there could have moved (cards_due) and never when there is nothing to ask; the answers
        kept for every card sweep until the next ask, and the cards' stamp taken from them. With no read kept, the
        tick's read asks itself (plan.rail_read)."""
        read = (self.last or {}).get("read")
        if read is None:
            self.kept.cards = self.kept.listed = None
            return
        now, at = datetime.datetime.now(datetime.timezone.utc), time.monotonic()
        cards, askers = plan.cards_asked(fleet, read, crew.this_host(), now), plan.askers_asked(fleet, read, crew.this_host(), now)
        owned = plan.owners_asked(fleet, read, crew.this_host(), now)  # each owner's cards, read in its name (plan.owners_read)
        if not cards and not askers:  # nothing to ask after: no bridge and no listing
            self.kept.cards, self.kept.listed = ({}, None), {}
        elif cards_due(cards, askers, self.kept.cards, self.kept.listed, self.cards_at, at):
            self.asks, self.cards_at = self.asks + 1, at
            self.kept.cards = plan.cards_fetched(fleet, cards, owned=owned) if owned else plan.cards_fetched(fleet, cards)
            self.kept.listed = plan.askers_listed(fleet, askers)
        else:
            return
        self.cards = kept_stamp(self.kept.cards, self.left, self.asks, self.kept.listed)

    def tick(self, hear=True):
        """The clock's tick: the caches fetched, the cards asked after, Pending You's notice heard (hear) but by a tick of
        its own (once), and a refresh; a tick whose read asked nothing, failing before its sweep, leaves the sweeps until
        the next with no answer to judge by, rather than ask between."""
        fleet = self.fleet()
        self.fetch(fleet)
        self.ask(fleet)
        if hear and fleet is not None:
            self.hear(fleet)
        self.refresh(tick=True)
        if self.kept.cards is None:
            self.kept.cards = ({}, None)

    def once(self):
        """One tick, waiting for nothing and starting no notice: crew _follow --once, for the tiers."""
        self.tick(hear=False)

    def hear(self, fleet):
        """Pending You's notice (notice_argv) run as a child of the follower's own while a role whose main level is
        here runs as its kind (answers_watched), started again at a tick when it ended, and let go when none does; its
        words and crew _answered's appended to HEARD. One a host, as the follower is (design Decision 5)."""
        if self.notice is not None and self.notice.poll() is not None:
            self.notice = None
        if not answers_watched(fleet, crew.this_host()):
            self.unhear()
            return
        if self.notice is not None:
            return
        try:
            HEARD.parent.mkdir(parents=True, exist_ok=True)
            with open(HEARD, "a") as log:
                self.notice = subprocess.Popen(notice_argv(), stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
        except OSError as e:
            print(f"crew's follower could not run Pending You's notice, `{shlex.join(notice_argv()[:2])}`: {e.strerror or e}", file=sys.stderr)

    def unhear(self):
        if self.notice is None:
            return
        self.notice.terminate()
        try:
            self.notice.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.notice.kill()
            self.notice.wait()
        self.notice = None

    def look(self, fleet):
        """What the look reads (look), each kit's main the last read named among it."""
        return look(fleet, self.labels, self.kits)

    def step(self, most=None):
        """A look: the clock's tick when it is due, a refresh when a cache, crew or the teams file moved, else nothing;
        then a wait of a second, or of most seconds when that is less."""
        how = wake(time.monotonic(), self.tick_at, self.seen, self.look(self.fleet_) if self.fleet_ else None)
        if how == "tick":
            self.tick_at = time.monotonic() + self.period
            self.tick()
        elif how == "refresh":
            time.sleep(BURST)
            self.refresh()
        time.sleep(1 if most is None else min(1, most))

    def bases(self, fleet, kits, readings):
        """What says something on each host the check reads could have moved (host_basis), read with no process: the
        drives' tips and their runners' as this host's caches hold them."""
        tips = look(fleet, self.labels)["state"]
        runners = {l: plan.runner_tips(plan.state_of(fleet, l)[0], l, fetch=False) for l in self.labels}
        return {h: host_basis(h, readings.get(h, ()), tips, runners) for h in sorted(set(kits) | set(readings))}

    def check(self, fleet, kits, readings, tick, kept):
        """The check's stamps (stamps_now): this host's in this process each time, which starts nothing; another host's
        only when something there could have moved (hosts_due), the rest as the last read was made at, so they move
        nothing; and at a tick, of each host something could have moved on since the last tick asked it, its routes.
        Each host asked that answered whole is kept as asked at its basis now."""
        here, at = crew.this_host(), time.monotonic()
        bases = self.bases(fleet, kits, readings) if kept else {}
        due = set(hosts_due(bases, self.asked, at)) if kept else None
        clock = set(hosts_due(bases, self.asked_at_tick, at)) if kept and tick else set(kits) if tick else set()
        hosts = None if due is None else due | clock | {here}
        now = stamps_now(fleet, kits, readings, routes=clock, hosts=hosts)
        if kept:
            for (h, m), s in kept["stamps"]["kits"].items():
                if h not in hosts:
                    now["kits"][(h, m)] = s
            for h, s in kept["stamps"]["readings"].items():
                if h not in hosts:
                    now["readings"][h] = s
        return now, hosts, clock

    def answered(self, fleet, now, hosts, clock):
        """Each host the check asked that answered whole, its kits' and readings' stamps all read, kept as asked at its
        basis as the refresh leaves it; one that did not is asked again. With none
        kept before (hosts None), the read asked every host for everything, its gathers their routes among it."""
        if hosts is None:
            hosts = clock = set(self.kept.kits) | set(readings_hosts(fleet, self.labels))
        at, bases = time.monotonic(), self.bases(fleet, self.kept.kits, readings_hosts(fleet, self.labels))
        for h in hosts:
            whole = all(s is not None for (sh, _), s in now["kits"].items() if sh == h) and now["readings"].get(h, "") is not None
            for memo, asked in ((self.asked, True), (self.asked_at_tick, h in clock)):
                if not asked:
                    continue
                if whole and h in bases:
                    memo[h] = (bases[h], at)
                else:
                    memo.pop(h, None)

    def refresh(self, tick=False):
        fleet = self.fleet()
        kept = self.last if self.last and self.last["read"] is not None else None
        kits = self.kept.kits if kept else {}
        readings = readings_hosts(fleet, self.labels)
        now, hosts, clock = self.check(fleet, kits, readings, tick, kept)
        looked = self.look(fleet)
        stamps = dict(looked, kits=now["kits"], readings=now["readings"], cards=self.cards)
        self.seen = looked
        m = moved(kept and kept["stamps"], stamps)
        routes = routes_moved(kits, now["routes"])  # read on the clock's tick alone (Decision 8)
        m = dict(m, routes=routes, any=m["any"] or bool(routes))
        lag = self.lagging()
        how = refresh_plan(m, kept is not None, None not in looked["crew"] and None not in (kept["stamps"]["crew"] if kept else ()), lag)
        if how == "update":
            self.again(fleet, lag=lag)
            how = "read"
        if how == "read":
            self.read(fleet, looked, stamps)
        else:
            self.render(fleet, m, stamps, tick)
        if self.last["read"] is not None:
            self.reroute(routes, now["routes"])
            self.answered(fleet, now, hosts, clock)
        self.write(fleet)

    def reroute(self, hosts, routes):
        """Each host whose portless routes the tick read moved has them in every kit answer kept of it, the board's dev
        servers drawn from them with nothing gathered (Decision 8)."""
        for host in hosts:
            for _, answer in self.kept.kits.get(host, {}).values():
                if (answer or {}).get("ok"):
                    answer["routes"] = routes[host]

    def read(self, fleet, looked, stamps):
        """A read of what moved: the tips this host's caches hold handed in (no fetch), each kit's main the look read
        among them, each unmoved kit served from what was kept, and every sweep run; what the read said on standard
        error kept for the rail's frames, and the kits whose main the clock fetches next taken from it (kit_mains)."""
        plan.READ.memory.clear()
        for l in self.labels:
            for (repo, ref), tip in ((plan.state_of(fleet, l), looked["state"][l]),
                                     ((crew.drive_of(fleet, l)["blueprints"][0], "main"), looked["blueprints"][l])):
                if tip is not None:
                    plan.READ.keep_tip(repo, ref, tip)
        for repo, tip in (looked.get("mains") or {}).items():  # each kit's main, which plan.main_tip serves (Decision 7)
            if tip is not None:
                plan.READ.keep_tip(repo, "main", tip)
        self.kept.stamps, plan.READ.follower, said, asked = stamps["kits"], self.kept, io.StringIO(), self.kept.cards is None
        try:
            with contextlib.redirect_stderr(said):
                read = flow_read(fleet, self.labels, sweep=True)
        except Exception as e:  # a read that fails is said in the frames, and the follower goes on
            print(f"crew's follower could not read: {e}" if isinstance(e, Refusal) else
                  f"crew's follower could not read: {type(e).__name__}: {e}", file=said)
            read = None
        finally:
            plan.READ.follower = None
            self.kept.settle()
        if asked and self.kept.cards is not None:  # the read's sweep made the tick's ask
            self.asks, self.cards_at = self.asks + 1, time.monotonic()
            self.cards = kept_stamp(self.kept.cards, False, self.asks, self.kept.listed)
        if read is not None:
            self.kits = kit_mains(fleet, read)
            self.left = card_left(read.get("swept"))
            self.told = {l: (tip, read["told"][l]) for l, _, tip, _ in read["found"] if l in (read.get("told") or {})}
            self.last = {"read": read, "stamps": dict(looked, kits=kept_stamps(self.kept.kits), readings=stamps["readings"], cards=self.cards),
                         "said": said.getvalue().strip()}
        else:
            self.last = {"read": None, "stamps": None, "said": said.getvalue().strip()}

    def render(self, fleet, m, stamps, tick=False):
        """Nothing the read rests on moved: the kept read stands, its sweeps' acts are not said again, and only the sweeps
        of what moved run against it (sweeps_after, the card-sessions spec): the card sweep with the clock's last answers
        when the cards moved, and the card sessions swept on each host whose readings folder moved and each the last
        refresh could not check; what they did is said, and the stamps they rest on kept. Whatever moved, a batch due by
        the hours is reckoned from the kept read and the time now, reading nothing (plan.reckon_batches), and a drive
        told at its read's tip is not told again, nor one whose tell did not go through before the clock's next tick
        (plan.batch_told)."""
        read = self.last["read"]
        todo = sweeps_after(m, readings_hosts(fleet, self.labels), read.get("unchecked"))
        swept = {"done": [], "unswept": []}
        if todo["cards"]:
            swept = plan.sweep_cards(fleet, read, answers=self.kept.cards, listed=self.kept.listed)
            read = dict(read, cards=plan.swept_cards(read["cards"], swept, crew.this_host(), datetime.datetime.now(datetime.timezone.utc),
                                                     read["kits"]))
            self.left = card_left(swept)
        ended, unchecked = plan.sweep_sessions(fleet, read["found"], read["sv"], read["rows"], read["cards"], read["unread"],
                                               read.get("batched") or {}, todo["sessions"], read.get("runs")) if todo["sessions"] else ([], [])
        said = io.StringIO()
        with contextlib.redirect_stderr(said):
            told = plan.reckon_batches(fleet, read["found"], read, plan.batch_told(self.told, read["found"], tick))
        self.told.update({l: (tip, told[l]) for l, _, tip, _ in read["found"] if l in told})
        self.last = dict(self.last, said=said.getvalue().strip(), read=dict(read, swept=swept, moved={"raised": [], "unread": []}, ended=ended, unchecked=unchecked),
                         stamps=dict(self.last["stamps"], readings=stamps["readings"], cards=self.cards))

    def lagging(self):
        """Whether this follower is to start again as the installed crew before it reads, running another (behind_here):
        never once it was started again for that and still runs another, as a crew whose release disagrees with its own
        answer to crew _release would, which it says once and follows on as it is rather than start again for ever."""
        lag = behind_here()
        if lag and self.started_lagging:
            if not self.said_lag:
                print(f"crew's follower on {crew.this_host()} was started again as the crew the host has installed and still "
                      "runs another, its release not the one the installed crew names: it follows as it is", file=sys.stderr)
                self.said_lag = True
            return False
        return lag

    def again(self, fleet, lag=False):
        """crew's checkout, the crew the host has installed or the teams file moved, or the follower runs a crew other
        than the installed one (lag, behind_here): each drive's agents here that it made due a restart are handed
        theirs by the installed crew (crew _update, teams.19), and the follower starts again as the new crew, its lock
        handed on and what the update said with it, and whether it started again for running another: through the
        installed command where it is not crew's own, as after an install of a build, else as this crew's board.py; the
        kept read goes with this process. When it can't start again it reads afresh here."""
        installed = crew.installed_here()
        cmd = ["bash", installed or crew.crew_command()]
        updated = {l: subprocess.run(cmd + ["_update", "--label", l], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout.strip() or None
                   for l in self.labels}
        self.unhear()
        try:
            os.set_inheritable(self.lock.fileno(), True)
            sys.stdout.flush()
            env = dict(os.environ, CREW_FOLLOWER_LOCK=str(self.lock.fileno()), CREW_FOLLOWER_UPDATED=json.dumps(updated),
                       CREW_FOLLOWER_LAGGED="1" if lag else "0")
            if installed and not crew.own_command(installed):
                os.execvpe("bash", ["bash", installed, *sys.argv[1:]], env)
            else:
                os.execve(sys.executable, [sys.executable, str(LIB / "board.py"), *sys.argv[1:]], env)
        except OSError as e:
            print(f"crew's follower could not start again as the new crew ({e.strerror or e}); it reads afresh as it is", file=sys.stderr)
            self.updated, self.last = updated, None

    def write(self, fleet):
        """Each drive's frames from the one read, as of now: its rail, with what the read said and what could not be
        read or fetched; its board; and its agents' views, with what this host's agents run of crew."""
        now = datetime.datetime.now(datetime.timezone.utc)
        last = self.last or {"read": None, "said": ""}
        for l in self.labels:
            read, unfetched = last["read"], self.unfetched.get(l, {})
            if read is None:
                text = last["said"] or f"crew's follower on {crew.this_host()} has no read of {l}"
                data = None
            else:
                read = dict(read, errors={**read["errors"], **{k: f"could not fetch it, so it is shown as this host last fetched it: {v}"
                                                               for k, v in unfetched.items() if k.startswith(f"{l}/main of ")}})
                sigs, sunread = read["signals"].get(l, ([], {}))
                read["signals"] = dict(read["signals"], **{l: (sigs, {**sunread, **{k: f"could not fetch it: {v}" for k, v in unfetched.items()
                                                                                       if not k.startswith(f"{l}/main of ")}})})
                errors = label_errors(read["errors"], l)
                text = "\n".join([plan.rail_text(fleet, [l], read, now)] + ([last["said"]] if last["said"] else []) + list(errors.values()))
                data = dict(board_data(fleet, [l], read, now), unread=errors)
            try:
                write_frame(l, {"read_at": iso(now), "from": crew.this_host(), "text": text, "updated": self.updated.get(l)}, rail_path(l))
                if data is not None:
                    key = here_key(self.seen["crew"])
                    if self.here.get(l, (None,))[0] != key:
                        self.here[l] = (key, here_read(fleet, l))
                    write_frame(l, data)
                    write_frame(l, agent_views(dict(data, here=self.here[l][1])), agents_path(l))
            except OSError as e:
                print(f"crew could not write {l}'s frames in {FRAMES}: {e.strerror or e}", file=sys.stderr)
        self.updated = {}

    def close(self):
        self.unhear()
        self.lock.close()


def run_follow(once=False):
    """crew _follow: the host's follower with no tab, the command a job of the host's runs (swancloud's): it waits for
    the lock while another follows, reading nothing, then follows every drive with an operator session here."""
    lock = lock_follower("job", wait=True)
    f = Follower(lock, int(os.environ.get("CREW_TEST_PERIOD") or PERIOD))
    signal.signal(signal.SIGUSR1, lambda *_: f.tick_now())
    try:
        if once:
            f.once()
            for l in f.labels:
                print(f"{l}'s rail, board and agents' views written on {crew.this_host()}")
            return
        print(f"crew's follower on {crew.this_host()} follows its drives' rails and boards", flush=True)
        while True:
            f.step()
    finally:
        f.close()


def rail_follow(label, once=False):
    """The rail tab: the latest rail frame drawn whenever it changes, or how stale it is does; checked once a second.
    Each second, while no one follows on the host, it takes the follower lock without waiting and is the host's
    follower itself, for every drive with an operator session here, on the follower's clock and look (Follower); so a
    tab drawing the job's frames follows itself within a second of the job ending. With once, one draw, following
    nothing."""
    tty = sys.stdout.isatty()
    seen, data, mtime, follower = None, None, False, None
    try:
        while True:
            try:
                m = rail_path(label).stat().st_mtime_ns
            except OSError:
                m = None
            if m != mtime:
                mtime, data = m, read_rail(label) if m is not None else None
            text = rail_frame_text(label, data, datetime.datetime.now(datetime.timezone.utc))
            if text != seen:
                seen = text
                sys.stdout.write(("\033[H\033[2J" if tty else "") + text + "\n")
                sys.stdout.flush()
            if once:
                return
            if follower is None:
                lock = lock_follower("tab", label, wait=False)
                follower = Follower(lock) if lock else None
                if follower:
                    signal.signal(signal.SIGUSR1, lambda *_: follower.tick_now())
            if follower:
                follower.step(1)
            else:
                time.sleep(1)
    finally:
        if follower:
            follower.close()


def ended_by_signal():
    """A follower told to end, by its job's manager or its pane's close, ends its follows and lets go of its lock."""
    for s in (signal.SIGTERM, signal.SIGHUP):
        signal.signal(s, lambda *_: sys.exit(0))


# ------------------------------------------------------------------------------------------------- commands

def main(argv):
    sub, argv = (argv[0], argv[1:]) if argv else ("board", [])
    sub in ("board", "_views", "_board", "_rail", "_follow") or fail(f"board.py runs crew board, _views, _board, _rail or _follow, not {sub}")
    ap = argparse.ArgumentParser(prog=f"crew {sub}")
    if sub in ("_board", "_rail", "_views"):
        ap.add_argument("label")
    if sub in ("_board", "_rail", "_follow"):
        ap.add_argument("--once", action="store_true")
    if sub == "board":
        ap.add_argument("--label")
        ap.add_argument("--json", action="store_true")
    crew.answer_usage(ap, argv)
    plan.need_recutils()
    fleet = crew.load()
    a = ap.parse_args(argv)
    if sub in ("_board", "_rail"):
        if sub == "_rail":
            ended_by_signal()
        (follow if sub == "_board" else rail_follow)(crew.drive_of(fleet, a.label)["label"], a.once)
        return
    if sub == "_follow":
        ended_by_signal()
        run_follow(a.once)
        return
    if sub == "_views":
        labels = [crew.drive_of(fleet, a.label)["label"]]
    else:
        label = plan.default_label(fleet, a)
        labels = [label] if label else list(fleet["drives"])
    read = flow_read(fleet, labels, sweep=sub == "_views")
    now = datetime.datetime.now(datetime.timezone.utc)
    data = board_data(fleet, labels, read, now)
    if sub == "_views":
        print(plan.rail_text(fleet, labels, read, now))
        try:
            write_frame(labels[0], data)
            write_frame(labels[0], agent_views(dict(data, here=here_read(fleet, labels[0]))), agents_path(labels[0]))
        except OSError as e:
            print(f"crew could not write the board's frame in {FRAMES}: {e.strerror or e}", file=sys.stderr)
    elif a.json:
        print(json.dumps(data, indent=1))
    else:
        tty = sys.stdout.isatty()
        print(board_text(data, shutil.get_terminal_size().columns if tty else None, tty and not os.environ.get("NO_COLOR")))
    if read["errors"]:
        sys.exit("\n".join(read["errors"].values()))


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Refusal as e:
        sys.exit(str(e))
