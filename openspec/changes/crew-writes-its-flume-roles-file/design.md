# Design: crew writes its Flume roles file

## Context

Flume 0.17.0 reads every role, a standing agent's among them, from the roles file of a source the host declares: `~/.config/flume/sources/<source>.toml` names a `kinds_dir` and a `roles` file, the source's own tool writes the roles file whole and renames it over the old one, and Flume reads it at each launch, wake, start, stall and status and writes nothing in it (agentplot/flume v0.17.0, `guides/roles-and-wake.md`, "Roles come from a source" and "An address an agent already holds"; `reference/configuration.md`, "The host's sources" and "A source's roles"). A standing agent's entry gives `agent`, `session`, `answers` and `answerer`; one that gives `agent` beside `kind` or a run's other keys declares nothing. An entry whose address names a stream the host does not declare, and is not carried, declares nothing. A `kinds_dir` that does not exist faults no file, but refuses a launch naming the source.

Flume record 0039 (accepted 2026-11-05, amended 2026-11-06) has crew write that file from its partitions, each partition's operator standing behind its stream as its door, an address on another host carried, and the roles crossing onto their kinds in the order operator, ops, reviewer, then planner and design agent; its amendment declares a standing agent in the source's roles file, a crossing trading `agent` for `kind` there. swancloud record 0042 as amended 2026-11-07 (branch `design/flume-roles-one-deploy`, eae5cf10) has the fleet declare crew a source, `sources/crew.toml` naming crew's kinds folder and roles file, in the one deploy that brings Flume 0.17.0 and the crew that writes the file, and never write the file itself (`lists.1`).

deneb's teams file, read 2026-11-07 16:30Z: four partitions at version 5, agentplot, madswan and swancloud on deneb in sessions of their labels' names, wldn on chuck-herdr-alpha in `wldn-2` with its planner in `wldn-1`, every role `flume` false. crew reads it in `crew.load` (`code.5`), which already gives each partition its roles' sessions (`p["sessions"]`, `role_session`, record 0035).

Rules this design relies on: `code.1` (standard library only), `code.5` (the teams file read, never written), `code.7` (the entries a function of plain facts), `read.1` (a teams file crew refuses changes nothing), `state.4` (no service: the follower already writes derived frames, and the roles file is another such derived file, remade from the teams file and read by no decision of crew's), `roles.5` (crew declares; Flume delivers, and crew builds no delivery of its own), `roles.7` (each recipient named by a role's address), `teams.6` (a role's session from the teams file), `teams.9` (a file crew keeps is written new and moved over the old). Pages whose areas it touches: `teams.md` (`crew.py`, and `source.py` added to its paths), `briefs.md` (the sentence in three briefs), `tests.md` (a new end-to-end test and its task), `docs.md` (README). It departs from no rule. It adds `teams.25`.

## Goals / Non-Goals

**Goals:** the roles file always says what the teams file says on every host where crew keeps a main level, from crew alone, with nothing run by hand; Flume 0.17.0 finds every standing role of deneb's partitions at its address, and takes the runner's launches naming them.

**Non-Goals:** a role's run entry or crew's kinds as packages (the first crossing's); a carried address (the change by which a place on this host first names another host's role); the fleet's source file and its streams (swancloud's); anything on crew's main.

## Decisions

### Decision 1: crew writes the file, the fleet declares the source

The roles file is crew's: every fact in it, which agents crew starts, what it names them, which session it opens each in and what each answers, is crew's own, and Flume gives the file to the source's own tool. The fleet declares the source alone. Not taken: the fleet writing the file from `lib/crew-teams.nix`, a second list of crew's agents' names and sessions beside crew's (swancloud 0042's own reason, `lists.1`).

### Decision 2: the follower writes it at each read of the teams file, and a main-level start writes it again

crew's follower already runs on every host that holds an operator session, as swancloud's job (`lib/crew-follow.nix`), which the fleet's deploy starts again whenever crew's pin moves, and it already reads the teams file afresh at each tick and within seconds of its bytes moving (`Follower.fleet`, `moved_at`). So `Follower.fleet`, after each read that loads, writes the roles file. A deploy that brings this release and a new teams file has the file written at the follower's first read, with nothing run by hand, and every later rewrite of the teams file reaches the roles file within seconds. A host with no job has a rail tab's own loop as its follower (`state.4`'s reading of 2026-10-28), the same `Follower`.

crew also writes it in `Agents.start` once a main-level role's agent is up (`crew main up`, `restart`, `resume`, `revive`), the act by which crew changes a role's agent, so a host whose follower is not yet running has the file once its main level starts. Each write compares the bytes it would write with the file's and writes nothing when they match, so the follower's ticks write nothing between changes.

Not taken: a crew command the deploy runs, which would have the fleet run crew's write beside declaring the source; crew's session-start hook, which every Claude session on the host runs, under every account, many of them at once after a restart.

### Decision 3: one standing entry per standing role, at `<label>/<role>`

The stream is the partition's own, its label as the teams file names it, which is also how crew's runner names a place's recipient (`<label>/planner`, `<label>/ops`) and how the role records name an address (role-runs, "A role record names its run"). The roles are `KIND_ROLES`, the five a partition's `flume` names, each written as the role names its agent: `design`, `planner`, `reviewer`, `ops`, `operator`. Each entry gives `agent = "<label>-<role>"`, the herdr name `Agents.agent_of` gives, and `session`, always written, from `p["sessions"][role]`: the role's own session where `roles.<definition>.session` names one, the reviewer beside the planner where only the planner's is named (record 0035), else the partition's. Writing the session crew opens the agent in, rather than leaving it out for Flume to take the stream's, finds the agent where crew put it whatever session the host gives the stream.

A role whose `flume` names a stream gets no entry: its run's entry comes with its crossing, in Flume 0039's order. A partition whose machine is another host gets none: on deneb no place reaches wldn's roles, and the carried entry comes with the first change by which one must. Not taken: declaring wldn carried now, an address no place on deneb names, which would list wldn's roles in every stage's prompt there.

### Decision 4: what each role answers comes from one table, the briefs' sentence built from it

crew's briefs say whom to ask about what in one sentence, `cards_how`, shared by the planner's, ops's and the design agent's briefs: "`<label>-design` for the design, `<label>-ops` for a live system or a deploy, `<label>-planner` for the plan". crew.py gains `ASKS`, the role to its words, `design` "the design", `planner` "the plan", `ops` "a live system, a deploy or a landing", and `cards_how` builds its sentence from it in that order; the roles file's `answers` reads the same table. ops's words gain "a landing", which the operator's brief already sends to ops ("a landing, a deploy or a live system: main-level ops"), so the one table says what both briefs say.

The operator stands behind its stream with `answerer = true` and gives no `answers`: the briefs give no words for asking it, the operator asking and being asked nothing (`briefs.11`), and every stall in its stream reaches it as the door all the same. The reviewer gives neither, so nothing lists it for a question. No entry gives `kind` or a run's keys, which beside `agent` would declare nothing.

### Decision 5: the file is written whole, renamed over, only when it differs

`source.py` decides the entries (`entries(fleet, host, asks)`) and their text (`text(entries, host)`) on plain facts (`code.7`); `keep(...)` reads the file's bytes, and where they differ writes the text to a new file in the same folder and renames it over the old one (`os.replace`), as `teams.9` has crew keep a file. The text opens with comment lines saying crew writes it whole from the teams file and a hand edit is lost, carries no clock, and lists partitions in the teams file's order and roles in `KIND_ROLES` order, so the same teams file always gives the same bytes. Strings are TOML basic strings; every value is a name crew checks (`code.4`) or a word of `ASKS`, and the logic tier reads the text back with `tomllib`.

On a host that is no partition's machine there are no entries: crew makes no file there, and writes one already there with no entry, so a host whose main level moved away declares nothing for it. When `crew.load` refuses, no write is reached: `crew _follow` refuses at its start naming the teams file, and a running follower keeps what it had and says why (`read.1`). crew runs no `flume` command for any of this.

### Decision 6: the kinds folder exists, empty

Where crew writes a file with an entry it makes `~/.local/share/flume/kinds/crew` when missing, so the source's `kinds_dir` exists and the host's status shows no missing folder; it puts nothing there. No role runs as its kind in this release, so the host locks nothing of crew's. `plugin/flume/kinds.toml` stays as it is. Not taken: crew's role kinds shipped as packages in this release, which the host would lock and trust before any role runs them.

### Decision 7: the record and the rule

These choices are record 0057, agentplot-design's, each cheap to change, with the paths not taken; `teams.25` states what the file always says, `plugin/lib/source.py` joins `teams.md`'s paths, and both are in this change's own commit.

## Risks / Trade-offs

- A host on Flume 0.17.0 before this release refuses every runner launch: swancloud 0042's amendment moves Flume, the source and crew's pin in one deploy.
- An address whose stream the host does not declare declares nothing: the fleet declares each partition's stream (swancloud's `flume-streams`).
- The reviewer is often not up: Flume says none of that name is there, which is no fault, and its ends wait for its next start.

## After deploy

- **On deneb, once swancloud's deploy brings Flume 0.17.0, `~/.config/flume/sources/crew.toml` naming crew's roles file and kinds folder, and crew's pin at the `teamless/deneb` tip that carries this change**, swancloud-ops reads `flume status` and finds every `agentplot/`, `madswan/` and `swancloud/` address held by the standing agent `<label>-<role>` in its session, no fault under crew's source, each stream's answerer its operator declared by crew, and the next runner launch naming `<label>/planner` or `<label>/ops` taken. Why it is no check: it needs the host's Flume 0.17.0, the fleet's source file and its streams, and the live herdr agents, none of which crew's tiers hold (`code.1` keeps Flume out of crew's shell).

## Task notes

**1.1** `plugin/lib/source.py`, importing only the standard library (`code.1`), with no import of `crew`: `ROLES_FILE = Path.home() / ".local/state/crew/flume/roles.toml"`, `KINDS_DIR = Path.home() / ".local/share/flume/kinds/crew"`; `entries(fleet, host, asks)`, a list of `(address, entry)` in the teams file's partition order and `("design", "planner", "reviewer", "ops", "operator")` order, for each partition whose `machine` is `host` and each role whose `p["flume"][role] is False`: `agent = f"{label}-{role}"`, `session = p["sessions"][role]`, `answers = asks[role]` where the role has words, `answerer = True` for the operator; `text(entries, host)`, the comment header and one `[roles."<address>"]` table per entry. `plugin/lib/crew.py`: `ASKS = {"design": "the design", "planner": "the plan", "ops": "a live system, a deploy or a landing"}` beside `cards_how`. `tests/py/test_source.py`: fleets built with `crew.load` from a teams file and a hosts file written to `tmp_path` (monkeypatching `crew.TEAMS` and `crew.HOSTS`), deneb's three partitions plus wldn on chuck-herdr-alpha as read on 2026-11-07, and wldn's planner in `wldn-1`; each scenario of the spec's first five requirements; the text read with `tomllib`, its one key `roles`, every entry's keys within `{"agent", "session", "answers", "answerer"}`; the same fleet giving the same text twice.

**1.2** `cards_how` builds "`<label>-design` for the design, `<label>-ops` for a live system, a deploy or a landing, `<label>-planner` for the plan" from `ASKS`, in that order. `tests/t-briefs.sh`'s case at its line 56 expects the new words; `tests/py/test_source.py` checks the planner's brief, `crew.brief(fleet, "madswan", "planner")`, holds each `ASKS` word beside its agent's name, where building the brief needs no tool, else that check stays in `t-briefs`.

**2.1** `source.keep(fleet, host, asks)`: the entries; with none and no file there, nothing; else the text compared with the file's bytes, and where they differ written to `roles.toml.<pid>.tmp` in the file's folder (made when missing) and `os.replace`d over `roles.toml`; with an entry, `KINDS_DIR.mkdir(parents=True, exist_ok=True)`. It returns whether it wrote. `crew.keep_roles(fleet)` calls it with `this_host()` and `ASKS`, and an `OSError` is said on standard error, naming the file, and never stops the caller. `board.py` `Follower.fleet`: after a load that did not refuse, `crew.keep_roles(self.fleet_)`. `tests/t-flume-source.sh` (new; `# Reads: plugin/lib/board.py`), on the stubs' mac-studio and chuck-herdr-alpha: `crew _follow --once` on mac-studio writes madswan's and swancloud's ten entries and no `wldn/` one, makes `kinds/crew` empty, leaves the teams file's bytes as they were, and the calls log shows no `flume`; a second run leaves the file's inode and mtime alone; with a hard link kept to the file, the teams file rewritten (`rewrite` from `tests/lib.sh`) naming madswan's planner the session `madswan-2`, a run gives the new session while the link holds the old text; the teams file at version 4, a run refuses naming it and the roles file is unchanged; with wldn's main level moved to mac-studio's session `wldn-5`, a run on chuck-herdr-alpha with no roles file there makes none, and, after a run there with wldn back on it wrote wldn's entries, a run with wldn moved again leaves a file with no entry. Run `tests/moon-tasks` and commit `tests/moon.yml`.

**2.2** `crew.py` `Agents.start`: once a role's agent of a main level (`self.kind`'s main level, not a console) is up, `keep_roles(self.fleet)`. `tests/t-journey-main.sh`: after its `crew main up wldn`, chuck-herdr-alpha's `~/.local/state/crew/flume/roles.toml` holds `wldn/design`, `wldn/planner`, `wldn/reviewer`, `wldn/ops` and `wldn/operator`.

**3.1** README's "The main level and the console" says, in a few sentences, that crew writes `~/.local/state/crew/flume/roles.toml` from the teams file on every host where it keeps a main level, declaring each standing role at `<label>/<role>` as its agent, the operator its stream's door, with the empty `~/.local/share/flume/kinds/crew` beside it, both named by the fleet's `sources/crew.toml`, and that crew's follower and a main-level start keep it; no command changes, so the usage header and the skill need no line (`docs.2`).

**3.2** `tests/suite --affected`, once, when the rest is done.
