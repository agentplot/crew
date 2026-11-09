#!/usr/bin/env python3
"""gather.py: read a host's kits for the bolt plan, in one run per host.

  python3 gather.py '<request>'      or, sent over ssh:  python3 - '<request>' < gather.py

The request is JSON: {"kits": [{"main": <kit's main checkout>, "dir": <the kit's folder>, "bolts": [<bolt>, ...],
"fetch": <true to fetch the kit's GitHub, its origin, before reading it, never given for the runner's clone, which crew
fetches nothing in>}],
"sites": <true to also read each worktree's dev server names with devurl, and the host's running portless routes>,
"board": <true to also read the explorations on the kit's main>,
"stamped": <true to also give each kit's stamp, taken before it is read>,
"stamp": <true to give each kit's stamp alone and read nothing else: the host's follower's check that nothing moved,
answered {"kits": {<main>: <stamp>}, "readings": <the stamp of the card readings folders of the partitions named>}>,
"labels": <with stamp, the partitions whose card readings folders on the host to stamp>,
"routes": <with stamp, true to read the host's portless routes too, answered "routes">}.
The answer, on stdout, is JSON keyed by each kit's main checkout: the changes main holds (open or archived) and the
chores its history holds (each `Chore:` trailer's name), and for each local bolt/* branch, and each bolt asked for,
read where the bolt lives (bolt_read, at: GitHub's origin/bolt/<bolt> for a bolt on GitHub, else the host's bolt/<bolt>),
whether it exists, the changes and chores it holds, those it holds archived, its worktree, its head and the head's
time, and the commits it holds that are another bolt's own, on that bolt's first-parent line beyond main, every bolt
GitHub holds among them (carries, carried_bolts, bolt_lines), or why that can't be read (carries_error), and the
branches sluice's landings on it name, each with the newest landing's commit and time (landings, bolt_landings), or
why they can't be read (landings_error); each place under <dir>/places with its branch, its head and the head's time, its change's tasks and whether
its planning is complete, read from the change archived there once its merge has archived it; each chore's place,
<dir>/places/chore-<name> on chore/<name>, with its bolt,
head, head's time and how many commits of its own it holds beyond the bolt; the kit's
policy, its main's .config/sluice.toml as text. It runs no sluice and reads nothing of sluice's queue or records: a
bolt's verification and each piece's submission are read from the runner's report (crew record 0056 points 1 and
4). With sites, each worktree's devurl names and the host's
portless routes; with board, each
folder under openspec/explorations/ on main with the first line of its first .md file. It reads with git, the file
system, devurl and portless and, for a change whose workflow it does not read itself, openspec, and changes
nothing.
It needs nothing but python3's standard library, since it is sent to hosts whose crew may be older."""
import datetime, fnmatch, hashlib, json, os, re, subprocess, sys, tomllib


def run(args, cwd):
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    except FileNotFoundError:
        return None
    return r.stdout if r.returncode == 0 else None


def changes(main, ref):
    """The OpenSpec changes a branch holds, open or archived (an archived one loses its YYYY-MM-DD- prefix)."""
    out = run(["git", "ls-tree", "-d", "--name-only", ref, "openspec/changes/", "openspec/changes/archive/"], main) or ""
    names = set()
    for line in out.splitlines():
        rest = line[len("openspec/changes/"):]
        if rest == "archive":
            continue
        if rest.startswith("archive/"):
            rest = rest[len("archive/"):]
            if len(rest) > 11 and rest[4] == "-" and rest[7] == "-" and rest[10] == "-":
                rest = rest[11:]
        names.add(rest)
    return sorted(names)


# The prefix openspec archive gives a change's folder: the day it was archived.
DATED = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}-")


def archived(main, ref):
    """The OpenSpec changes a branch holds archived, by name, without the archive's YYYY-MM-DD- prefix: what a unit's
    merge has delivered once the bolt holds its change so (teams.17)."""
    out = run(["git", "ls-tree", "-d", "--name-only", ref, "openspec/changes/archive/"], main) or ""
    return sorted({n[11:] for n in (l[len("openspec/changes/archive/"):] for l in out.splitlines())
                   if len(n) > 11 and DATED.fullmatch(n[:11])})


# A chore's name, as a commit's `Chore:` trailer gives it (plan.11).
CHORE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def chores(main, ref):
    """The chores a branch's history holds: the name each commit's `Chore:` trailer gives, as git parses trailers, of
    the commits whose message has a line starting `Chore: `. [] for a branch that is not there."""
    out = run(["git", "log", "--grep=^Chore: ", "--format=%(trailers:key=Chore,valueonly,separator=%x0a)", ref, "--"], main) or ""
    return sorted({l.strip() for l in out.splitlines() if CHORE.match(l.strip())})


def chore_place(path, bolt, ref):
    """A chore's place: its head and the head's time, and how many commits of its own it holds beyond its bolt (ahead),
    read at the ref the bolt is read at (ref, bolt_at): its first-parent line with no merges, so the work it took of
    what it comes after is not counted; None when it tracks no bolt crew can read or git can't count them."""
    ahead = (run(["git", "rev-list", "--count", "--first-parent", "--no-merges", f"{ref}..HEAD"], path) or "").strip() if bolt and ref else ""
    return {"path": path, "head": (run(["git", "rev-parse", "HEAD"], path) or "").strip() or None, "head_at": head_at(path, "HEAD"),
            "ahead": int(ahead) if ahead.isdigit() else None}


def worktrees(main):
    """The checkout's worktrees: each one's path, its branch when it is on one, and whether it is locked."""
    out, cur = [], {}
    for line in (run(["git", "worktree", "list", "--porcelain"], main) or "").splitlines() + [""]:
        if not line:
            if cur:
                out.append(cur)
            cur = {}
        elif line.startswith("worktree "):
            cur["path"] = os.path.realpath(line[9:])
        elif line.startswith("branch refs/heads/"):
            cur["branch"] = line[18:]
        elif line == "locked" or line.startswith("locked "):
            cur["locked"] = True
    return out


def upstreams(main):
    out = {}
    for line in (run(["git", "for-each-ref", "--format=%(refname:short) %(upstream:short)", "refs/heads/unit/", "refs/heads/chore/"],
                     main) or "").splitlines():
        b, _, up = line.partition(" ")
        out[b] = up
    return out


def bolt_ref(up):
    """The bolt a branch's upstream names, and the ref it names, from its short form as for-each-ref's
    %(upstream:short) prints it, which still names an upstream that is gone: (bolt, ref) for bolt/<bolt>, the host's
    refs/heads/bolt/<bolt>, or for origin/bolt/<bolt>, GitHub's refs/remotes/origin/bolt/<bolt> as this host last
    fetched it (plan.19); (None, None) for any other."""
    for short, ref in (("bolt/", "refs/heads/bolt/"), ("origin/bolt/", "refs/remotes/origin/bolt/")):
        if up.startswith(short) and up[len(short):]:
            return up[len(short):], ref + up[len(short):]
    return None, None


def bolt_of(up):
    """The bolt a place's branch was cut from, from its upstream (plan.19, bolt_ref): bolt/<bolt>, a bolt made before
    gives went through sluice, or origin/bolt/<bolt>, a bolt on GitHub; None for any other upstream, or none."""
    return bolt_ref(up or "")[0]


# A kit's policy, where sluice reads how each branch is gated and routed (kit.DECLARATION).
POLICY = ".config/sluice.toml"


def branch_table(branches, branch):
    """The [branches."<pattern>"] table of a policy's branches whose pattern matches the branch, the most specific
    first, as sluice matches it; None when none does."""
    matching = sorted((p for p in (branches if isinstance(branches, dict) else {}) if fnmatch.fnmatchcase(branch, p)),
                      key=lambda p: (p.count("*"), -len(p)))
    return branches[matching[0]] if matching and isinstance(branches[matching[0]], dict) else None


def policy_remote(text, branch):
    """The remote a policy's text names for a branch, as sluice routes it (plan.19): the `remote` of the matching
    [branches."<pattern>"] table (branch_table) when it is a non-empty string; None for no policy (text None), no
    matching table or no remote, which sluice reads as a branch kept in the host's own refs. Raises ValueError
    (tomllib's TOMLDecodeError) on text that is not TOML."""
    if text is None:
        return None
    table = branch_table(tomllib.loads(text).get("branches", {}), branch)
    remote = table.get("remote") if table else None
    return remote if isinstance(remote, str) and remote else None


def bolt_at(bolt, tracked, local, remote_at_tracked):
    """The ref a bolt is read at (plan.19): GitHub's copy, refs/remotes/origin/bolt/<bolt> as this host last fetched
    it, when the host holds it (tracked) and the policy in it names a remote for the bolt's branch (remote_at_tracked);
    else the host's own refs/heads/bolt/<bolt> when it is there (local), the bolt itself for a bolt kept on its host or
    one this host has not fetched; None when the host has neither, the bolt missing. The host's copy of a bolt on
    GitHub is sluice's, and nothing of the bolt is read from it."""
    if tracked and remote_at_tracked is not None:
        return f"refs/remotes/origin/bolt/{bolt}"
    return f"refs/heads/bolt/{bolt}" if local else None


def bolt_read(main, bolt, tracked=None, local=None):
    """Where a bolt is read in a kit's main checkout (bolt_at), from what the host holds of it, asked of git unless the
    caller has listed it (tracked, local): (ref, None), (None, None) when the host has no copy of it, or (None, why)
    when the policy at GitHub's copy is not TOML, which reads nothing from the host's copy (read.1)."""
    def there(ref):
        return run(["git", "rev-parse", "--verify", "-q", f"{ref}^{{commit}}"], main) is not None
    github = f"refs/remotes/origin/bolt/{bolt}"
    tracked = there(github) if tracked is None else tracked
    remote = None
    if tracked:
        try:
            remote = policy_remote(run(["git", "show", f"{github}:{POLICY}"], main), f"bolt/{bolt}")
        except ValueError as e:
            return None, f"{POLICY} at origin/bolt/{bolt} is not TOML, so crew can't read bolt {bolt}: {e}"
    return bolt_at(bolt, tracked, there(f"refs/heads/bolt/{bolt}") if local is None else local, remote), None


def carried_bolts(holds, lines, own):
    """What a branch carries of other bolts' work (plan.8, plan.19): each commit it holds beyond main (holds) that is
    another bolt's own, on that bolt's first-parent line beyond main (lines, {bolt: [commits]}, each line as git
    lists it, newest first), and not on the line of the bolt it is of (own), by bolt: {bolt: [commits]}, in each
    line's order; {} when it carries none. A bolt's first-parent line beyond main is the landings sluice made on it,
    so a commit there is that bolt's work, whichever branch it reached by a merge; read from the branches alone,
    never a commit's words. A decision of facts alone (code.7)."""
    held, mine = set(holds), set(lines.get(own) or ())
    out = {}
    for b in sorted(lines):
        if b == own:
            continue
        got = [c for c in lines[b] if c in held and c not in mine]
        if got:
            out[b] = got
    return out


def bolt_lines(main, now, refs):
    """Each bolt's first-parent line beyond the kit's main now (now), from the ref each is read at (refs, {bolt: ref}):
    ({bolt: [commits]}, None), or (None, why) when git could not list one (read.1). A ref another command removed while
    this read ran, as a fetch prunes a landed bolt's, is left out: the branch is gone, and no bolt."""
    lines = {}
    for b, ref in sorted(refs.items()):
        out = run(["git", "rev-list", "--first-parent", ref, f"^{now}"], main)
        if out is None:
            if run(["git", "rev-parse", "-q", "--verify", ref], main) is None:
                continue
            return None, f"git could not list bolt/{b}'s own commits beyond main at {short(ref)}"
        lines[b] = out.split()
    return lines, None


# What a landing sluice made says it landed (sluice clause 23; its text.rs): `Sluice-From: <agent> (<worktree>)`, naming
# the branch submitted as the one or the other, a Flume place's branch as both (change/<u> (change/<u>)), a session's
# as the agent (fix/<f> (pull/<n>)) or the worktree (<agent> (unit/<u>)).
FROM = re.compile(r"^(\S+) \((\S+)\)$")


def landed_from(log):
    """The branches a bolt's landings name (crew record 0056 decision 2; read.2), from `git log --first-parent
    --format=%H%x1f%ct%x1f%(trailers:key=Sluice-From,valueonly,separator=%x1d)%x1e` over the bolt's own line (log),
    newest first: {name: {"commit", "at"}}, each name its Sluice-From gives, the agent and the worktree, at the newest
    landing naming it, at as UTC ISO 8601 from its committer time; a commit with no Sluice-From names nothing. A
    decision of facts alone (code.7)."""
    out = {}
    for rec in log.split("\x1e"):
        parts = rec.strip("\n").split("\x1f")
        if len(parts) != 3 or not parts[0] or not parts[1].isdigit():
            continue
        at = datetime.datetime.fromtimestamp(int(parts[1]), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        for v in (x.strip() for x in parts[2].split("\x1d") if x.strip()):
            m = FROM.match(v)
            for name in (m.groups() if m else (v,)):
                out.setdefault(name, {"commit": parts[0], "at": at})
    return out


LANDINGS = "--format=%H%x1f%ct%x1f%(trailers:key=Sluice-From,valueonly,separator=%x1d)%x1e"


def bolt_landings(main, ref, now, landing=None):
    """The landings sluice made on a bolt, by the branches they name (landed_from), read on the bolt's own first-parent
    line. Given the bolt's landing on main (landing, main_landing's), on that landing's line, its head back to its base,
    the bolt's own line as main holds it, whether or not its branch stands (ref None) (Decision 3 of
    a-bolts-landing-on-main-reads-landed). Given none, where the bolt is read (ref, bolt_at): beyond the kit's main now
    (now) while main does not hold the bolt's head, and, once it does, beyond main as it stood when the bolt landed, the
    first parent of the merge on main's first-parent line whose other parent is the head, so a landed bolt still names
    what landed on it until its close; a head main holds with no such merge, a bolt with nothing of its own, names none.
    ({name: {"commit", "at"}}, None), or (None, why) when git could not read it (read.1)."""
    if landing:
        log = run(["git", "log", "--first-parent", LANDINGS, landing["head"], f"^{landing['base']}", "--"], main)
        if log is None:
            return None, f"git could not list the landings on main's landing {landing['commit'][:7]}, {landing['head'][:7]} beyond {landing['base'][:7]}"
        return landed_from(log), None
    head = (run(["git", "rev-parse", "--verify", "-q", f"{ref}^{{commit}}"], main) or "").strip()
    if not head:
        return None, f"git could not read bolt/{ref.rsplit('bolt/', 1)[-1]}'s head at {short(ref)}"
    code, _, err = ran(["git", "merge-base", "--is-ancestor", head, now], main)
    if code not in (0, 1):
        return None, f"git could not tell whether main holds {short(ref)} at {head[:7]}: {(err or '').strip() or f'exit {code}'}"
    base = now
    if code == 0:
        merges = run(["git", "log", "--first-parent", "--format=%H %P", now, f"^{head}"], main)
        if merges is None:
            return None, f"git could not find where {short(ref)} landed on main"
        base = next((ps[1] for ps in (l.split() for l in merges.splitlines()) if head in ps[2:]), None)
        if base is None:
            return {}, None
    log = run(["git", "log", "--first-parent", LANDINGS, ref, f"^{base}", "--"], main)
    if log is None:
        return None, f"git could not list the landings on {short(ref)}"
    return landed_from(log), None


# main's first-parent line as main_landing reads it: each commit, its parents, its committer time and its Sluice-From.
LANDED = "--format=%H%x1f%P%x1f%ct%x1f%(trailers:key=Sluice-From,valueonly,separator=%x1d)%x1e"


def main_landing(log, bolt, heads, since):
    """The landing that landed a bolt on its kit's main (Decision 2 of a-bolts-landing-on-main-reads-landed), from facts:
    log, `git log --first-parent --since=<since> LANDED <main now> --`, newest first; heads, the bolt's heads crew knows
    (each Head of its bolt.submit entries, and its branch's head where it was read); since, the bolt's first launch as
    UTC ISO 8601. The newest merge made at or after since whose Sluice-From names bolt/<bolt>, as the agent or the
    worktree, or whose second parent is one of heads, as {"commit", "at", "base", "head"}: its first parent the base, its
    second the head, at as UTC ISO 8601 from its committer time; None where none does. sluice's landing commit always
    has the entry's head as its second parent (sluice clause 23; read.2), so a commit of fewer than two parents is no
    landing, and a landing through a pull request names `<agent> (pull/<n>)` and no branch, as 4acecf09 did on swancloud's
    main, read 2026-11-08, its second parent 900527e9 the Head of the bolt's bolt.submit. A commit older than since is
    passed over, since a bolt's name is free again once it lands and git may list one past its --since. A decision of
    facts alone (code.7)."""
    try:
        bound = datetime.datetime.strptime(since, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc).timestamp()
    except (TypeError, ValueError):
        return None
    named, known = f"bolt/{bolt}", set(heads or ())
    for rec in log.split("\x1e"):
        parts = rec.strip("\n").split("\x1f")
        if len(parts) != 4 or not parts[0] or not parts[2].isdigit():
            continue
        parents, at = parts[1].split(), int(parts[2])
        if len(parents) < 2 or at < bound:
            continue
        names = {n for v in (x.strip() for x in parts[3].split("\x1d") if x.strip())
                 for n in (FROM.match(v).groups() if FROM.match(v) else (v,))}
        if named in names or parents[1] in known:
            return {"commit": parts[0], "base": parents[0], "head": parents[1],
                    "at": datetime.datetime.fromtimestamp(at, datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    return None


def short(ref):
    """A ref's short form, as git takes it and a person reads it: origin/bolt/<bolt> or bolt/<bolt>; None for None."""
    for long in ("refs/remotes/", "refs/heads/"):
        if ref and ref.startswith(long):
            return ref[len(long):]
    return ref


def head_at(cwd, ref):
    """The committer time of a ref, as ISO 8601, or None."""
    return (run(["git", "log", "-1", "--format=%cI", ref], cwd) or "").strip() or None


# A change's tasks and whether its planning is complete, read from its files by openspec 1.14.1's own rules for its
# spec-driven schema (dist/utils/task-progress.js, dist/core/artifact-graph, dist/utils/change-metadata.js), so
# neither needs openspec started. tests/t-stage-facts.sh holds this reading to openspec's on the same worktrees.
# JavaScript's \s, written out, since Python's differs; JavaScript's `.` stops at a line or paragraph separator.
SPACE = "\t\n\v\f\r \u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000\ufeff"
WS = f"[{SPACE}]"
# openspec's TASK_LINE_PATTERN: a list item (-, *, + or 1. / 1)) holding a checkbox of at most one marker; only x or X
# is done. Not anchored at the end, so a CRLF line still matches.
TASK = re.compile(rf"^{WS}*(?:[-*+]|[0-9]{{1,9}}[.)]){WS}*\[(?:{WS}*([^\]{SPACE}]?){WS}*\](?![(\[])|{WS}+\]){WS}*([^\n\r\u2028\u2029]*)")
# The spec-driven schema's outputs: an artifact is complete when a file it generates exists.
PLANNED = ("proposal.md", "design.md", "tasks.md")


def tasks_of(text):
    """Each task of a tasks file, in order, as (done, description), as openspec parses them."""
    out = []
    for line in text.split("\n"):
        m = TASK.match(line)
        if m:
            out.append(((m.group(1) or "").lower() == "x", re.sub(rf"^{WS}+|{WS}+$", "", m.group(2))))
    return out


def yaml_lines(path):
    """A small YAML file's top-level lines as [(key, value, indented lines under it)], or None when crew does not read
    it: a line that is not a plain `key: value` at the left edge or a key's indented continuation, or a key twice.
    [] when the file is not there."""
    try:
        with open(path, encoding="utf-8", newline="") as f:
            text = f.read()
    except FileNotFoundError:
        return []
    except (OSError, UnicodeDecodeError):
        return None
    out = []
    for line in text.split("\n"):
        line = line[:-1] if line.endswith("\r") else line
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith(" ") and out:
            out[-1][2].append(line)
            continue
        m = re.match(r"^([a-z_]+):(?:[ ]+(\S.*?))?[ ]*$", line)
        if not m or any(k == m.group(1) for k, _, _ in out):
            return None
        out.append((m.group(1), m.group(2) or "", []))
    return out


def data_dir():
    """openspec's global data folder: $XDG_DATA_HOME/openspec when that is set, else ~/.local/share/openspec
    (getGlobalDataDir, on every system but Windows)."""
    base = os.environ.get("XDG_DATA_HOME") or os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(base, "openspec")


def planned(change, root):
    """Whether a change's planning is complete, as `openspec status` would say it in the project at root: True or
    False when the change uses openspec's own spec-driven schema and crew reads all its metadata, else None, meaning
    read it through openspec. The schema is the change's .openspec.yaml's, else the project's openspec/config.yaml's
    (config.yml's when there is no .yaml), else spec-driven; a spec-driven of the project's or the user's own, any
    other schema, or a line crew does not read hands the change to openspec. .openspec.yaml is read when it holds
    only schema, created and skip_specs; config.yaml when its schema is plain and its other keys are context, rules
    and operations, which openspec reads for its instructions only."""
    if os.path.islink(change):
        return None
    metadata = os.path.join(change, ".openspec.yaml")
    meta = yaml_lines(metadata)
    config = os.path.join(root, "openspec", "config.yaml")
    conf = yaml_lines(config if os.path.exists(config) else os.path.join(root, "openspec", "config.yml"))
    if meta is None or conf is None:
        return None
    if os.path.lexists(metadata) and not any(k == "schema" for k, _, _ in meta):
        return None  # openspec refuses metadata with no schema
    for k, v, more in meta:
        if more or not (k == "schema" and v == "spec-driven" or k == "created" and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", v)
                        or k == "skip_specs" and v in ("true", "false")):
            return None
    for k, v, more in conf:
        if k == "schema" and (more or v != "spec-driven") or k not in ("schema", "context", "rules", "operations"):
            return None
    if any(os.path.exists(os.path.join(d, "spec-driven")) for d in (os.path.join(root, "openspec", "schemas"), os.path.join(data_dir(), "schemas"))):
        return None
    if not os.path.isdir(change):
        return False
    if not all(os.path.isfile(os.path.join(change, f)) for f in PLANNED):
        return False
    return ("skip_specs", "true", []) in meta or specs_written(os.path.join(change, "specs"))


def specs_written(specs):
    """Whether specs/**/*.md matches a file, as openspec's glob does: a regular file, symbolic links followed, no
    part of its path below specs/ starting with a dot."""
    for d, dirs, files in os.walk(specs, followlinks=True):
        dirs[:] = [x for x in dirs if not x.startswith(".")]
        if any(f.endswith(".md") and not f.startswith(".") and os.path.isfile(os.path.join(d, f)) for f in files):
            return True
    return False


def change_tasks(change):
    """A change's tasks, as tasks_of reads its tasks.md; [] when there is none to read."""
    try:
        with open(os.path.join(change, "tasks.md"), encoding="utf-8", errors="replace", newline="") as f:
            return tasks_of(f.read())
    except OSError:
        return []


def place(path, unit):
    """A unit's place: its head and the head's time, its change's tasks, whether its planning is complete, and the open
    tasks. The tasks and the planning are read from the change's files, or
    through openspec when planned() hands the change to it. A change its merge archived in the place, as a unit's merge
    stage does first (teams.17), is read from the archive, its planning complete, and the place says it is archived."""
    info = {"path": path, "head": (run(["git", "rev-parse", "HEAD"], path) or "").strip() or None,
            "head_at": head_at(path, "HEAD"), "tasks": None, "planning": False, "open": [], "archived": False}
    change, archive = os.path.join(path, "openspec", "changes", unit), os.path.join(path, "openspec", "changes", "archive")
    if not os.path.isdir(change) and os.path.isdir(archive):
        gone = sorted(d for d in os.listdir(archive) if d[11:] == unit and DATED.fullmatch(d[:11]))
        if gone:
            change, info["archived"] = os.path.join(archive, gone[-1]), True
    tasks = change_tasks(change)
    info["open"] = [d for done, d in tasks if not done]
    if info["archived"]:
        info["tasks"], info["planning"] = [sum(done for done, _ in tasks), len(tasks)], True
        return info
    planning = planned(change, path)
    if planning is not None:
        info["planning"] = planning
        if os.path.isdir(change):  # openspec lists a change folder, not a link to one
            info["tasks"] = [sum(done for done, _ in tasks), len(tasks)]
    else:
        listed = run(["openspec", "list", "--json"], path)
        if listed:
            for c in json.loads(listed).get("changes", []):
                if c.get("name") == unit:
                    info["tasks"] = [c.get("completedTasks", 0), c.get("totalTasks", 0)]
        status = run(["openspec", "status", "--change", unit, "--json"], path)
        if status:
            info["planning"] = bool(json.loads(status).get("isPlanningComplete"))
    return info


def devurl(path):
    """The worktree's names as swancloud's devurl gives them: here (this host's local name) and tailnet (its
    dev.swancloud.net name, None when the host does not publish)."""
    out = run(["devurl"], path)
    if out is None:
        return {"here": None, "tailnet": None, "error": "devurl did not answer"}
    names = {}
    for line in out.splitlines():
        key, _, rest = line.strip().partition(" ")
        rest = rest.strip()
        names[key] = rest if rest.startswith("https://") else None
    return {"here": names.get("here"), "tailnet": names.get("tailnet")}


def routes():
    """The host's running dev servers, from portless's active routes: each URL and the name it serves."""
    out, found = run(["portless", "list"], None), []
    for line in (out or "").splitlines():
        m = re.match(r"\s*(https?://(\S+?))(:\d+)?\s+->\s+", line)
        if m:
            host = m.group(2)
            name = host.rsplit(".", 1)[0] if host.rsplit(".", 1)[-1] in ("local", "localhost") else host
            found.append({"url": m.group(1) + (m.group(3) or ""), "name": name})
    return found if out is not None else None


def has_origin(main):
    """Whether a kit's main checkout has an origin remote, its GitHub."""
    return run(["git", "remote", "get-url", "origin"], main) is not None


def ran(args, cwd):
    """A command's exit and what it said, (exit, stdout, stderr); (None, "", why) when it can't be started."""
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    except (FileNotFoundError, NotADirectoryError) as e:
        return None, "", str(e)
    return r.returncode, r.stdout, r.stderr


def fetched(main):
    """A kit's GitHub fetched into its main checkout, as a read a decision of the moment rests on fetches it (plan.18,
    plan.19), `git fetch -q origin`: None once it fetched, or for a kit with no origin remote, which has no GitHub;
    git's words when the fetch failed."""
    if not has_origin(main):
        return None
    code, out, err = ran(["git", "fetch", "-q", "origin"], main)
    return None if code == 0 else (err or out).strip() or f"git fetch exited {code}"


def now_ref(origin):
    """The ref a kit's main is read at now (plan.18), from whether it has an origin remote: GitHub's,
    refs/remotes/origin/main as this host last fetched it, for a kit with one, since sluice lands there and the host's
    own main lags it on every host that did not land; its own main for a kit with none, which has no GitHub to lag. A
    read of every kit fetches nothing: sluice's push moves origin/main on the host that landed, and the fleet's timer
    fetches on every other within minutes; a command that must have GitHub's main at once fetches it (plan.MAINS)."""
    return "refs/remotes/origin/main" if origin else "refs/heads/main"


def explorations(main, ref="main"):
    """Each folder under openspec/explorations/ on main (ref), in name order, with the first non-blank line of its first
    .md file, its leading "> " dropped; None when it has no .md file or that line can't be read."""
    out = []
    for path in (run(["git", "ls-tree", "-d", "--name-only", ref, "openspec/explorations/"], main) or "").splitlines():
        name = path.rstrip("/").rsplit("/", 1)[-1]
        files = (run(["git", "ls-tree", "--name-only", ref, f"openspec/explorations/{name}/"], main) or "").splitlines()
        md = next((f for f in files if f.endswith(".md")), None)
        text = run(["git", "show", f"{ref}:{md}"], main) if md else None
        first = next((l.strip() for l in (text or "").splitlines() if l.strip()), None)
        out.append({"name": name, "first": first[2:] if first and first.startswith("> ") else first})
    return out


def git_dirs(main):
    """A checkout's git folder and the common folder its worktrees share, read from its .git (a folder, or a file
    naming one, as a linked worktree's is) and the git folder's commondir; None when there is none."""
    dot = os.path.join(main, ".git")
    if os.path.isdir(dot):
        gitdir = dot
    else:
        with open(dot, encoding="utf-8") as f:
            line = f.read().strip()
        if not line.startswith("gitdir: "):
            return None
        gitdir = os.path.join(main, line[len("gitdir: "):])
    try:
        with open(os.path.join(gitdir, "commondir"), encoding="utf-8") as f:
            return gitdir, os.path.normpath(os.path.join(gitdir, f.read().strip()))
    except FileNotFoundError:
        return gitdir, gitdir


def stamp(req):
    """A kit's stamp, what moves whenever anything kit() reads of it moves, read with os.stat and os.scandir alone so a
    check that nothing moved starts no process (plan.12): the size and time of every file of the kit's git folder the
    gather reads through git (HEAD, packed-refs, config, every loose ref, each worktree's HEAD and gitdir), of every file
    of each unit's place's change folder and its archive and openspec config, hashed to one value. It reads nothing under
    the git folder's sluice/: a submission's move is in its runner's report, which the host's follower reads (crew
    record 0056 points 1 and 4). None when a file it reads can't be read (read.1); a kit with no checkout
    stamps as such, and its gather says so."""
    main, kdir = req["main"], os.path.realpath(req["dir"])
    seen = Seen()
    note, tree = seen.note, seen.tree
    try:
        if not os.path.isdir(main):
            return hashlib.sha256(f"no checkout at {main}".encode()).hexdigest()[:32]
        dirs = git_dirs(main)
        if dirs is None:
            return None
        _, common = dirs
        for f in ("HEAD", "packed-refs", "config"):
            note(os.path.join(common, f))
        tree(os.path.join(common, "refs"))
        places = os.path.join(kdir, "places")
        try:
            linked = sorted(e.path for e in os.scandir(os.path.join(common, "worktrees")) if e.is_dir(follow_symlinks=False))
        except FileNotFoundError:
            linked = []
        for w in linked:
            note(os.path.join(w, "HEAD"))
            note(os.path.join(w, "gitdir"))
            try:
                with open(os.path.join(w, "gitdir"), encoding="utf-8") as f:
                    path = os.path.dirname(os.path.realpath(f.read().strip()))
                with open(os.path.join(w, "HEAD"), encoding="utf-8") as f:
                    head = f.read().strip()
            except FileNotFoundError:
                continue
            if os.path.dirname(path) != places or not head.startswith("ref: refs/heads/unit/"):
                continue
            unit, changes = head[len("ref: refs/heads/unit/"):], os.path.join(path, "openspec", "changes")
            tree(os.path.join(changes, unit))
            note(os.path.join(changes, "archive"))
            try:
                for d in sorted(os.listdir(os.path.join(changes, "archive"))):
                    if d[11:] == unit and DATED.fullmatch(d[:11]):
                        tree(os.path.join(changes, "archive", d))
            except (FileNotFoundError, NotADirectoryError):
                pass
            for f in ("config.yaml", "config.yml"):
                note(os.path.join(path, "openspec", f))
    except OSError:
        return None
    return seen.digest()


class Seen:
    """The size and time of files, read with os.stat and os.scandir alone, a missing one noted as missing, hashed to
    one value: what a stamp reads."""

    def __init__(self):
        self.files = []

    def note(self, path):
        try:
            st = os.stat(path)
            self.files.append((path, st.st_size, st.st_mtime_ns))
        except FileNotFoundError:
            self.files.append((path, None))

    def tree(self, top):
        """Every file under a folder, by name."""
        stack = [top]
        while stack:
            d = stack.pop()
            try:
                with os.scandir(d) as it:
                    for e in sorted(it, key=lambda e: e.name):
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        else:
                            self.note(e.path)
            except (FileNotFoundError, NotADirectoryError):
                self.files.append((d, None))

    def digest(self):
        return hashlib.sha256(json.dumps(self.files).encode()).hexdigest()[:32]


# Where crew keeps each card's reading session on a host, by partition, as plan.CARDS: its session.json, plannotator's
# result.json once the user sends a reading back, told.json once its owner is told, a landings card's main.
CARDS = "~/.local/state/crew/cards"


def readings_stamp(labels):
    """A host's card readings folders' stamp, ~/.local/state/crew/cards/<label>/ for each partition named: every file
    under each, read with os.stat and os.scandir alone, so the follower sees a reading sent back and sweeps that host's
    card sessions, where its owner is told (the card-sessions spec, A reading sent on one host). A missing folder stamps
    alike each time; None when one can't be read (read.1)."""
    seen = Seen()
    try:
        for label in sorted(labels):
            seen.tree(os.path.join(os.path.expanduser(CARDS), label))
    except OSError:
        return None
    return seen.digest()


def text(v):
    """A field that is text, else None, so a missing or mistyped value never becomes text (read.2)."""
    return v if isinstance(v, str) and v else None


def kit(req, sites=False, running=None, board=False, fetch=False, stamped=False):
    main, kdir = req["main"], os.path.realpath(req["dir"])
    if not os.path.isdir(main):
        return {"ok": False, "error": f"no checkout at {main}"}
    # A read a decision of the moment rests on fetches GitHub first (fetch, fetched); every other reads it as this host
    # last fetched it.
    why = fetched(main) if fetch else None
    if why:
        return {"ok": False, "error": f"cannot fetch {main} from GitHub: {why}"}
    trees = worktrees(main)
    at = {t["path"]: t.get("branch") for t in trees}
    ups = upstreams(main)
    # The kit's main now (now_ref): which changes and chores have landed, and the explorations, are read there.
    now = now_ref(has_origin(main))
    main_at = run(["git", "rev-parse", "--verify", "-q", f"{now}^{{commit}}"], main)
    if main_at is None:
        return {"ok": False, "error": f"{main} has no {now[len('refs/remotes/'):] if now.startswith('refs/remotes/') else 'branch main'} to read"}
    # main_at, the revision of main it was read at, by which the rail's sweep tells main moved under a kit's landings
    # card (plan.landings_moved).
    out = {"ok": True, "main": changes(main, now), "chores": chores(main, now), "main_at": main_at.strip(), "bolts": {},
           "places": {}, "chore_places": {}}
    # The kit's policy, as its main holds it: what gates its bolt branches, which crew reads before it gives a bolt.
    out["policy"] = run(["git", "show", f"{now}:.config/sluice.toml"], main)
    # Every local bolt branch, so one answer serves every step of a command, whichever bolt it asks about; a bolt
    # asked for, or tracked by a place, that has no branch is marked missing. Each is read where it lives (bolt_read):
    # GitHub's copy as this host last fetched it for a bolt on GitHub, never the host's copy, which is sluice's.
    refs = (run(["git", "for-each-ref", "--format=%(refname)", "refs/heads/bolt/", "refs/remotes/origin/bolt/"], main) or "").split()
    have = [r[len("refs/heads/bolt/"):] for r in refs if r.startswith("refs/heads/bolt/")]
    github = {r[len("refs/remotes/origin/bolt/"):] for r in refs if r.startswith("refs/remotes/origin/bolt/")}
    tracked = [b for b in map(bolt_of, ups.values()) if b]
    reads = {}
    for b in sorted(set(have + req.get("bolts", []) + tracked)):
        ref, why = bolt_read(main, b, b in github, b in have)
        reads[b] = ref
        wt = os.path.join(kdir, "bolts", b)
        out["bolts"][b] = {"exists": ref is not None, "at": short(ref), "changes": changes(main, ref) if ref else [],
                           "archived": archived(main, ref) if ref else [],
                           "chores": chores(main, ref) if ref else [],
                           "worktree": wt if at.get(wt) == f"bolt/{b}" else None,
                           "head": (run(["git", "rev-parse", "--verify", "-q", f"{ref}^{{commit}}"], main) or "").strip() or None if ref else None,
                           "head_at": head_at(main, ref) if ref else None,
                           **({"error": why} if why else {})}
    # Each bolt's own line beyond main, read where it lives, every bolt GitHub holds among them (bolt_lines), and what
    # each bolt read carries of another's (carries, carried_bolts): a bolt never carries another bolt's work to main
    # (plan.8). A line git can't list is said on each bolt (carries_error), never read as none (read.1).
    lines, lwhy = bolt_lines(main, now, {b: reads.get(b) or (f"refs/remotes/origin/bolt/{b}" if b in github else f"refs/heads/bolt/{b}")
                                         for b in sorted(github | set(have) | {b for b, r in reads.items() if r})})
    # Each bolt the request seeks the landing of on main (seek, {bolt: {"since", "heads"}}, plan.landing_sought): main's
    # first-parent line read once, from the oldest since asked, and each sought bolt's landing on it (main_landing), by
    # the heads crew submitted and its branch's head where read, its branch standing or not; a line git can't list is
    # said on each bolt sought (landed_error), never read as no landing (read.1; Decision 2 of
    # a-bolts-landing-on-main-reads-landed).
    sought = {b: s for b, s in (req.get("seek") or {}).items() if s and s.get("since")}
    if sought:
        since = min(s["since"] for s in sought.values())
        code, log, err = ran(["git", "log", "--first-parent", f"--since={since}", LANDED, now, "--"], main)
        for b, s in sorted(sought.items()):
            facts = out["bolts"].setdefault(b, {"exists": False})
            if code != 0:
                facts["landed_error"] = (f"git could not list main's first-parent line at {short(now)} since {since}: "
                                         + ((err or "").strip() or f"exit {code}"))
                continue
            facts["landed"] = main_landing(log, b, list(s.get("heads") or []) + ([facts["head"]] if facts.get("head") else []), s["since"])
    for b in sorted(sought):
        landing = out["bolts"][b].get("landed")
        if landing and not reads.get(b):
            landed, why = bolt_landings(main, None, now, landing)
            out["bolts"][b].update({"landings": landed} if why is None else {"landings_error": why})
    for b, ref in reads.items():
        if not ref:
            continue
        holds = run(["git", "rev-list", ref, f"^{now}"], main) if not lwhy else None
        if holds is None:
            out["bolts"][b]["carries_error"] = lwhy or f"git could not list what bolt/{b} holds beyond main at {short(ref)}"
        else:
            out["bolts"][b]["carries"] = carried_bolts(holds.split(), lines, b)
        # The landings sluice made on it, by the branches they name: a unit's or chore's place is built once one names
        # its branch, whichever partition's launch made it (crew record 0056 decision 2); one git can't list is said.
        landed, why = bolt_landings(main, ref, now, out["bolts"][b].get("landed"))
        out["bolts"][b].update({"landings": landed} if why is None else {"landings_error": why})
    places = os.path.join(kdir, "places")
    for path, branch in at.items():
        if os.path.dirname(path) != places or not branch:
            continue
        if branch.startswith("unit/"):
            unit = branch[5:]
            bolt = bolt_of(ups.get(branch))
            out["places"][unit] = dict(place(path, unit), branch=branch, bolt=bolt)
        elif branch.startswith("chore/") and os.path.basename(path) == f"chore-{branch[6:]}":
            bolt = bolt_of(ups.get(branch))
            out["chore_places"][branch[6:]] = dict(chore_place(path, bolt, reads.get(bolt)), branch=branch, bolt=bolt)
    if sites:
        out["sites"] = {path: devurl(path) for path, branch in at.items()
                        if os.path.dirname(path) in (places, os.path.join(kdir, "bolts")) and branch}
        out["routes"] = running
    if board:
        out["explorations"] = explorations(main, now)
    return out


def read(request, running=None):
    """The answer to a request: with stamp, each kit's stamp alone by its main checkout and the stamp of the card readings
    folders of the partitions it names, the follower's check that nothing moved, and, at its clock's tick, the host's
    portless routes (routes) when asked; else, by each kit's main checkout, each kit as kit() reads it, with stamped,
    the host's follower's, its stamp too, taken before the kit is read, so anything that moves while it is read moves
    the stamp the follower next compares. It runs no sluice."""
    if request.get("stamp"):
        return {"kits": {k["main"]: stamp(k) for k in request["kits"]}, "readings": readings_stamp(request.get("labels", [])),
                **({"routes": routes()} if request.get("routes") else {})}
    out = {}
    for k in request["kits"]:
        s = stamp(k) if request.get("stamped") else None
        out[k["main"]] = dict(kit(k, request.get("sites"), running, request.get("board"), k.get("fetch"), request.get("stamped")),
                              **({"stamp": s} if request.get("stamped") else {}))
    return out


if __name__ == "__main__":
    request = json.loads(sys.argv[1])
    print(json.dumps(read(request, routes() if request.get("sites") and not request.get("stamp") else None)))
