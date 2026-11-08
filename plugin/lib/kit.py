"""A kit's policy, as sluice reads it, and what crew reads of a kit's main and its bolts (plan.18, plan.19).

A kit says what gates its branches, where each branch lives and whether it declares a preview once, in sluice's words:
the policy file DECLARATION, read at the revision in hand. crew readies no place: a unit's, chore's and fix's places
are Flume's, which has sluice equip each at its launch (`sluice equip`; Flume record 0036, sluice 147). sluice stands on
its own, and Boomdrive will use sluice's SDK for these same reads; the file becomes boomdrive.toml then, and DECLARATION
is the one name that changes.

These are the decisions, each a function of plain facts (code.7); plan.py runs their reads on the team's host."""
import base64
import binascii
import re
import tomllib

import crew
import gather

DECLARATION = ".config/sluice.toml"


def previewed(text, where=DECLARATION):
    """Whether a kit's DECLARATION, as a revision holds it, declares a preview of that revision, as sluice reads it
    there (sluice record 0021): True when its TOML holds a [preview] table, False when there is no file or no table.
    Refused, naming the file, when it is not TOML or `preview` is not a table (read.1)."""
    if text is None:
        return False
    try:
        preview = tomllib.loads(text).get("preview")
    except tomllib.TOMLDecodeError as e:
        crew.fail(f"{where} is not TOML, so crew can't read whether the kit declares a preview: {e}")
    if preview is not None and not isinstance(preview, dict):
        crew.fail(f"{where}: [preview] is a table, not {type(preview).__name__}")
    return preview is not None


# How a policy's branches are matched, as sluice matches them: gather's, since gather.py is sent to hosts on its own
# and reads where each bolt lives (gather.bolt_read).
branch_table = gather.branch_table


def bolt_checks(text, kit, where=DECLARATION, branch="bolt/a-bolt", ref="main"):
    """The checks a kit's policy requires of its bolt branches (teams.5, record 0026): the `required` list of the
    [branches."<pattern>"] table whose pattern matches a bolt's branch, the most specific first, as sluice matches it,
    in the policy as the kit's main holds it now (ref, origin/main for a kit on GitHub, plan.18). Refused, naming the
    file and the ref, when the kit has none, it is not TOML, or no table names bolt branches with a check: a kit merges
    and lands only through sluice, so crew starts none of its bolts until its policy says what gates one."""
    if text is None:
        crew.fail(f"{kit} merges only through sluice, and has no {where} on {ref}: write one whose "
                  f"[branches.\"bolt/*\"] names the checks a bolt's merges must pass, then start the bolt again")
    try:
        branches = tomllib.loads(text).get("branches", {})
    except tomllib.TOMLDecodeError as e:
        crew.fail(f"{kit}'s {where} is not TOML, so crew can't read what gates its bolt branches: {e}")
    table = branch_table(branches, branch)
    required = table.get("required") if table else None
    if not (isinstance(required, list) and required and all(isinstance(r, str) and r for r in required)):
        crew.fail(f"{kit} merges only through sluice, and its {where} names no checks for its bolt branches: give "
                  f"[branches.\"bolt/*\"] a `required` list of the checks a bolt's merges must pass, then start the bolt again")
    return required


def bolt_remote(text, branch="bolt/a-bolt", where=DECLARATION):
    """The remote a kit's policy names for a branch, as sluice routes it (plan.19, its rule core.15): the `remote` of the
    [branches."<pattern>"] table that matches the branch, the most specific first, as bolt_checks matches it, when it is
    a non-empty string; None for no policy (text None), no matching table or no remote, which sluice reads as a branch
    kept in the host's own refs. Refused, naming the file, when it is not TOML (read.1)."""
    try:
        return gather.policy_remote(text, branch)
    except ValueError as e:
        crew.fail(f"{where} is not TOML, so crew can't read where sluice keeps {branch}: {e}")


def branch_said(out, code):
    """What sluice's `branch create` or `branch delete` said with --json (read.2, as sluice 0.36.4 says it,
    tests/py/sluice-0.36.4/): (the commit it made the branch at or removed it from, None) for its document of a branch
    made or removed, exit 0; (None, its message) for its refusal, {"error": {"kind", "message"}}, exit 1 when the
    branch or the one it is made from is not there, 2 when it refused, 3 on its own failure. Refused, naming what it
    said, on anything else."""
    import json
    try:
        doc = json.loads(out or "")
    except ValueError:
        doc = None
    sha = re.compile(r"[0-9a-f]{40,64}")
    if code == 0 and isinstance(doc, dict) and isinstance(doc.get("branch"), str):
        made = doc.get("created", doc.get("deleted"))
        if isinstance(made, str) and sha.fullmatch(made):
            return made, None
    err = doc.get("error") if isinstance(doc, dict) else None
    if code in (1, 2, 3) and isinstance(err, dict) and isinstance(err.get("message"), str) and err["message"]:
        return None, err["message"]
    crew.fail(f"crew can't read what sluice's branch command said (exit {code}): {(out or '').strip()[:200] or 'nothing'}")


def bolt_lives(said, bolt):
    """Where a bolt's branch lives, as sluice routes it (plan.19): the remote the policy at the host's own bolt/<bolt>
    names for it, or at origin/bolt/<bolt> when the host has no branch of its own; None for a bolt made before gives
    went through sluice, kept in its host's refs. said is what BOLT_AT printed in the kit's main checkout: LOCAL and
    TRACKED, the commit of each ref or -, and AT_LOCAL and AT_TRACKED, the policy at each, base64, or - when that
    revision holds none. Refused when the host has neither ref, or the output is not BOLT_AT's (read.1, read.2)."""
    f = said_of(said)
    if not {"LOCAL", "TRACKED", "AT_LOCAL", "AT_TRACKED"} <= set(f):
        crew.fail(f"crew can't read where bolt/{bolt} lives from: {(said or '').strip()[:200] or 'nothing'}")
    where = "LOCAL" if f["LOCAL"] != "-" else "TRACKED" if f["TRACKED"] != "-" else None
    where or crew.fail(f"crew can't tell where bolt/{bolt} lives: this host has neither bolt/{bolt} nor origin/bolt/{bolt}")
    at = f[f"AT_{where}"]
    try:
        text = None if at == "-" else base64.b64decode(at, validate=True).decode()
    except (binascii.Error, UnicodeDecodeError) as e:
        crew.fail(f"crew can't read bolt/{bolt}'s {DECLARATION} as it was sent: {e}")
    return bolt_remote(text, f"bolt/{bolt}", f"{DECLARATION} at bolt/{bolt}")


def bolt_home(said, bolt):
    """Where a bolt lives (bolt_lives) and the remote the policy at its kit's main now names for its bolt branches
    (bolt_remote), from what BOLT_HOME printed: (the bolt's remote or None, main's remote or None). Refused as
    bolt_lives refuses, and when AT_MAIN is not there or can't be read (read.2)."""
    lives = bolt_lives(said, bolt)
    at = said_of(said).get("AT_MAIN")
    at is not None or crew.fail(f"crew can't read the policy at main from: {(said or '').strip()[:200] or 'nothing'}")
    try:
        text = None if at == "-" else base64.b64decode(at, validate=True).decode()
    except (binascii.Error, UnicodeDecodeError) as e:
        crew.fail(f"crew can't read main's {DECLARATION} as it was sent: {e}")
    return lives, bolt_remote(text, f"bolt/{bolt}", f"{DECLARATION} at main")


def delete_ran(said):
    """sluice's document and exit as BOLT_DELETE printed them, SAID, base64, and RC (read.2): (document, exit). Refused,
    naming what was printed, when they are not there."""
    f = said_of(said)
    try:
        return base64.b64decode(f["SAID"]).decode(), int(f["RC"])
    except (KeyError, ValueError, UnicodeDecodeError):
        crew.fail(f"crew can't read what sluice's branch delete said from: {(said or '').strip()[-200:] or 'nothing'}")


def said_of(out):
    """The KEY=value lines a script printed, as {key: value}."""
    return dict(line.split("=", 1) for line in (out or "").splitlines() if "=" in line)


def carries_of(out, bolt):
    """What a branch holds and each bolt's own line, from what CARRIES printed in a kit's main checkout after its
    fetch (plan.8, plan.19): (holds, lines, None), holds the commits the tip holds beyond main (and beyond its bolt,
    for a merge), lines {bolt: its first-parent commits beyond main}, every bolt GitHub holds, and the host's own for
    a bolt it keeps, the bolt read itself at the tip judged (OWN) when CARRIES judged its landing; or (None, None, why)
    when git could not fetch or list one (READ), or the output is not CARRIES's (read.1, read.2)."""
    f = said_of(out)
    if "READ" in f:
        return None, None, f["READ"].strip() or "git said nothing"
    if not {"HOLDS", "OWN", "LANDING"} <= set(f):
        return None, None, f"crew can't read what bolt/{bolt} carries from: {(out or '').strip()[:200] or 'nothing'}"
    lines = {}
    for line in (out or "").splitlines():
        if line.startswith("LINE "):
            _, b, *commits = line.split()
            lines[b] = commits
    if f["LANDING"] == "yes":
        lines[bolt] = f["OWN"].split()
    return f["HOLDS"].split(), lines, None


def main_now(out, kit, host):
    """Which of a kit's mains is its main now, from what MAINS read in its main checkout on its host (plan.18): (ref,
    sha, None), or (None, None, why). A kit with an origin remote has its main on GitHub, where sluice lands every
    branch and which the host's own main lags on every host that did not land, so main now is origin/main after the
    command's one fetch, or, in the runner's clone, which crew fetches nothing in (FETCHED=runner, crew.fetches_in),
    origin/main as the runner last fetched it; a fetch that failed or an origin with no main refuses (read.1); a kit
    with no origin remote has no GitHub to lag, so its own main is main now. What is not MAINS's words refuses too
    (read.2)."""
    said = said_of(out)
    sha = re.compile(r"[0-9a-f]{40,64}")
    origin, fetched, github, own = said.get("ORIGIN"), said.get("FETCHED"), said.get("GITHUB"), said.get("OWN")
    if origin not in ("yes", "no") or not all(v == "-" or (v and sha.fullmatch(v)) for v in (github, own)):
        return None, None, f"crew can't read what {kit}'s main on {host} holds: {(out or '').strip()[:200] or 'nothing was said'}"
    if origin == "yes":
        if fetched == "runner":
            return (("origin/main", github, None) if github != "-" else
                    (None, None, f"the runner's clone of {kit} on {host} holds no origin/main yet, and crew fetches "
                                 "nothing there: its runner's next fetch brings it"))
        if fetched != "ok":
            return None, None, f"cannot fetch {kit} from GitHub on {host}, so cannot read its main now: {(fetched or 'no word').strip()}"
        return ("origin/main", github, None) if github != "-" else (None, None, f"{kit}'s GitHub has no main, fetched on {host}")
    return ("main", own, None) if own != "-" else (None, None, f"{kit}'s main checkout on {host} has no branch main and no origin")


def policy_said(out, kit, host):
    """What POLICY printed of a kit's policy at its main now (main_now): (the policy text, or None when that main holds
    none; the ref, origin/main or main; the commit). Refused when main now can't be told or the output is not POLICY's
    (read.1, read.2)."""
    ref, sha, why = main_now(out, kit, host)
    if why:
        crew.fail(why)
    text = said_of(out).get("AT_GITHUB" if ref == "origin/main" else "AT_OWN")
    if text is None:
        crew.fail(f"crew can't read what {kit}'s main holds of {DECLARATION} from: {(out or '').strip()[:200] or 'nothing'}")
    if text == "-":
        return None, ref, sha
    try:
        return base64.b64decode(text).decode(), ref, sha
    except (binascii.Error, UnicodeDecodeError) as e:
        crew.fail(f"crew can't read {kit}'s {DECLARATION} as it was sent: {e}")
