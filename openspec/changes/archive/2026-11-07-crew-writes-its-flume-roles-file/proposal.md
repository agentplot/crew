# crew writes its Flume roles file

## Why

Flume 0.17.0 takes a role's entry, a standing agent's among them, only from the roles file of a source the host declares in `~/.config/flume/sources/`, a file the source's own tool writes whole and renames over the old one; the host's configuration names no role, and refuses a `[roles]` table (agentplot/flume v0.17.0, `site/src/content/docs/guides/roles-and-wake.md` and `reference/configuration.md`). It refuses a launch naming a role's address that no source declares where no answerer stands behind its stream, and crew's runner names `<label>/planner` or `<label>/ops` as the recipient of every place it launches (`plugin/lib/runner.py`). So a host on Flume 0.17.0 without crew's roles file refuses every launch crew asks for.

Flume record 0039 (accepted 2026-11-05) has crew write that file from its partitions, the operator standing behind each partition's stream as its door. swancloud record 0042 as amended 2026-11-07 has the fleet only declare crew a source, naming its kinds folder and its roles file, in the one deploy that brings Flume 0.17.0 and the crew that writes the file; the fleet writing the file from `lib/crew-teams.nix` would be a second list of crew's agents' names and sessions (swancloud `lists.1`). agentplot-design briefed this change on `teamless/deneb` on 2026-11-07, ahead of the hold on the user's word (req_b5647697a83e4a0da81e).

## What Changes

- **crew writes `~/.local/state/crew/flume/roles.toml`** on every host where it keeps a main level, whole, renamed over the old one, never edited in place, and only when what it would write differs from what is there. crew's follower writes it each time it reads the teams file, so at its first read after a deploy starts it and within seconds of the teams file moving; and crew writes it again whenever it starts a main-level role's agent. No one runs anything by hand, and crew runs no `flume` command for it.
- **One standing entry for each role that stands**, at the address `<label>/<role>` of each partition whose machine is this host, the stream being the partition's own: `agent` the herdr name crew gives the role, `<label>-<role>`; `session` the session crew opens it in, the role's own where the teams file names one, else the partition's; `answers` the words crew's briefs give for whom to ask (the design agent: the design; the planner: the plan; ops: a live system, a deploy or a landing); the operator `answerer = true` and no `answers`; the reviewer neither. No kind or run key beside `agent`.
- **One source for the words.** The sentence crew's briefs give for whom to ask is built from the same table the roles file reads, so ops's words there become "a live system, a deploy or a landing".
- **No entry** for a partition whose machine is another host, nor for a role whose teams-file `flume` names a stream: a carried address comes once a place on this host must reach it, and a run's entry with that role's crossing.
- **The kinds folder `~/.local/share/flume/kinds/crew`** exists beside the file and stays empty in this release, so the host locks nothing of crew's; crew's role kinds go into it as packages with the first crossing.
- **Unchanged:** the teams file and its version (`code.5`), every launch's recipient, `plugin/flume/kinds.toml`, and anything on crew's main.
- Record 0057 holds these choices with the paths not taken, and rule `teams.25` states what the file always says.

## Capabilities

### New Capabilities

- `flume-source`: crew as a source of its host's Flume: the roles file it writes from the teams file, and the kinds folder beside it.

### Modified Capabilities

None. The sentence in the briefs is no requirement of any spec.

## Impact

- `plugin/lib/source.py` (new): the roles file's entries and text from the partitions, decided on plain facts (`code.7`), and the act that writes the file and makes the folder.
- `plugin/lib/crew.py`: `ASKS`, the words for whom to ask; `cards_how` built from it; `keep_roles`, called by `Agents.start` once a main-level role's agent is up.
- `plugin/lib/board.py`: `Follower.fleet` writes the file after each read of the teams file.
- `docs/architecture/teams.md`: `teams.25`, and `plugin/lib/source.py` among its paths. `docs/adr/0057-…`. README's main-level section.
- Tests: `tests/py/test_source.py`; `tests/t-flume-source.sh` with its task in `tests/moon.yml`; `tests/t-briefs.sh` and `tests/t-journey-main.sh` amended.
- Nothing crew models changes, so the board, the agents' views and the mod are untouched (`code.8` not reached). Nothing outside the standard library is imported (`code.1`).
- swancloud declares the source (`~/.config/flume/sources/crew.toml`) and the partitions' streams; its deploy brings Flume 0.17.0, the source and the pin of this release together (swancloud record 0042 as amended 2026-11-07).

## Touches

```
plugin/lib/source.py
plugin/lib/crew.py
plugin/lib/board.py
docs/architecture/teams.md
docs/adr/0057-crew-writes-its-flume-roles-file-each-standing-role-its-agent-the-operator-each-streams-door-and-an-empty-kinds-folder.md
README.md
tests/py/test_source.py
tests/t-flume-source.sh
tests/t-briefs.sh
tests/t-journey-main.sh
tests/moon.yml
```
