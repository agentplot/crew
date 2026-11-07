"""crew as a source of its host's Flume (record 0057, teams.25; Flume record 0039): the roles file crew writes from the
teams file, one standing entry at `<label>/<role>` for each role that stands of each partition whose main level runs on
the host, and the kinds folder the host's `sources/crew.toml` names beside it. The entries and their text are decided
here on plain facts (code.7), from the fleet crew.load gives; this module imports nothing of crew's (code.1)."""
import json
from pathlib import Path

# The file the fleet's `~/.config/flume/sources/crew.toml` names as crew's roles, and the folder it names as crew's
# kinds (swancloud record 0042 as amended 2026-11-07).
ROLES_FILE = Path.home() / ".local/state/crew/flume/roles.toml"
KINDS_DIR = Path.home() / ".local/share/flume/kinds/crew"

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
