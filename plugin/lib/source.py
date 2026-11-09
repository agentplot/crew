"""crew as a source of its host's Flume (record 0057, teams.25; Flume record 0039): the roles file crew writes from the
teams file, one standing entry at `<label>/<role>` for each role that stands of each partition whose main level runs on
the host, and the kinds folder the host's `sources/crew.toml` names beside it, holding crew's one kind package, its bolt
kind `crew/bolt@1` (record 0056). The entries and their text are decided here on plain facts (code.7), from the fleet
crew.load gives, and keep is the one act that writes them and the package; this module imports nothing of crew's
(code.1)."""
import json, os
from pathlib import Path

# The file the fleet's `~/.config/flume/sources/crew.toml` names as crew's roles, and the folder it names as crew's
# kinds (swancloud record 0042 as amended 2026-11-07).
ROLES_FILE = Path.home() / ".local/state/crew/flume/roles.toml"
KINDS_DIR = Path.home() / ".local/share/flume/kinds/crew"

# crew's kind packages, as (the package in crew's plugin, its path under the kinds folder): the bolt kind, a base place
# that lands with no stages on `bolt/<bolt>` (record 0056; crew-lands-each-bolt-through-flumes-base-place, Decision 2).
# A version's bytes never change: a change to the kind is a new version beside it.
KIND_PACKAGES = ((Path(__file__).resolve().parent.parent / "flume/kinds/bolt@1/kind.toml", Path("bolt@1/kind.toml")),)

# A partition's main-level roles, each as it names its agent, in the order the file lists them: crew.KIND_ROLES.
ROLES = ("design", "planner", "reviewer", "ops", "operator")


def entries(fleet, host, asks):
    """The roles file's entries on host, as (address, entry) in the teams file's partition order and ROLES' order: for
    each partition whose machine is host, each role its `flume` names False, a standing agent's entry, `agent` the name
    crew gives it, `<label>-<role>`, `session` the session crew opens it in, `answers` its words in asks where it has
    any, and the operator its stream's answerer. None for another host's partition, nor for a role that runs as its
    kind, whose run's entry comes with its crossing (Decision 3)."""
    found = []
    for label, p in fleet["partitions"].items():
        if p["machine"] != host:
            continue
        for role in ROLES:
            if p["flume"][role] is not False:
                continue
            entry = {"agent": f"{label}-{role}", "session": p["sessions"][role]}
            if role in asks:
                entry["answers"] = asks[role]
            if role == "operator":
                entry["answerer"] = True
            found.append((f"{label}/{role}", entry))
    return found


def quoted(value):
    """A TOML basic string, or a boolean: JSON's string escapes are TOML's."""
    return ("true" if value else "false") if isinstance(value, bool) else json.dumps(str(value))


def text(entries, host):
    """The roles file's text: comment lines saying whose it is and that an edit by hand is lost, then one table per
    entry, `[roles."<address>"]`, its keys in the order entries gives them. No clock: the same entries give the same
    bytes. With no entry it gives `roles` none, which Flume reads as declaring nothing."""
    lines = [f"# crew's roles for Flume on {host}, written whole from crew's teams file by crew's follower and each start",
             "# of a main-level role, and renamed over the old one: an edit by hand is lost at the next write. Each role",
             "# that stands, of each partition whose main level runs on this host, at <label>/<role> (crew record 0057)."]
    for address, entry in entries:
        lines += ["", f"[roles.{quoted(address)}]"] + [f"{k} = {quoted(v)}" for k, v in entry.items()]
    return "\n".join(lines) + "\n"


def replace(path, new):
    """path holds new: written whole to a new file beside it and renamed over it, only when it differs from the file's
    bytes. Returns whether it wrote."""
    try:
        if path.read_bytes() == new:
            return False
    except FileNotFoundError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_bytes(new)
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)
    return True


def keep(fleet, host, asks, roles=None, kinds=None, packages=None):
    """The roles file kept on host (Decisions 5 and 6): its text written whole to a new file beside it and renamed over
    it, only when it differs from the file's bytes; with no entry and no file, nothing made, and a file already there
    written with no entry, so a host whose main levels moved away declares nothing for them. With an entry, the kinds
    folder made when missing, and each of crew's kind packages written into it whole the same way, read from crew's
    plugin and renamed over only when its bytes differ; with no entry, no folder and no package. Runs no flume command,
    locks no kind and writes nothing else. Returns whether it wrote the roles file; an OSError is the caller's to say."""
    roles, kinds = roles or ROLES_FILE, kinds or KINDS_DIR
    packages = KIND_PACKAGES if packages is None else packages
    found = entries(fleet, host, asks)
    if found:
        kinds.mkdir(parents=True, exist_ok=True)
        for package, under in packages:
            replace(kinds / under, package.read_bytes())
    elif not roles.exists():
        return False
    return replace(roles, text(found, host).encode())
