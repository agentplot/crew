---
status: accepted
date: 2026-11-07
decision-makers: agentplot-design (what the roles file says, who writes it, the kinds folder); the construct stage of crew-writes-its-flume-roles-file (when crew writes it, and the one text the answers come from)
---

# 0057. crew writes its Flume roles file: each standing role its agent, the operator each stream's door, and an empty kinds folder

Status: decided 2026-11-07 by agentplot-design, in its brief of the change `crew-writes-its-flume-roles-file` on `teamless/deneb`, ahead of the hold on the user's word (req_b5647697a83e4a0da81e), and by that change's construct stage for the parts its brief left open; nothing in it is the user's alone, and each part is cheap to change.

Deciders: agentplot-design, 2026-11-07, for what must be true: crew's roles file says what crew's teams file says, written whole by crew alone; its entries; the kinds folder; what must not change. The construct stage, for when crew writes it (decision 2) and the one text the answers come from (decision 4), from the code and the rules as written.

Adds the rule `teams.25`. Sources: agentplot/flume v0.17.0, `site/src/content/docs/guides/roles-and-wake.md` and `reference/configuration.md` (a source's roles, written whole by the source's own tool; a standing agent's keys; a missing `kinds_dir` faults no file but refuses a launch naming the source); Flume record 0039, accepted 2026-11-05 and amended 2026-11-06 (crew writes its roles file from its partitions; the operator as each stream's door; a standing agent declared in the source's roles file; the order of crossing: operator, ops, reviewer, then planner and design agent); swancloud record 0042 as amended 2026-11-07 (branch `design/flume-roles-one-deploy`, eae5cf10: the fleet declares crew a source and never writes the file, in the one deploy that brings Flume 0.17.0 and this crew); deneb's `~/.config/crew/teams.json` as read 2026-11-07 16:30Z.

## Context and problem statement

Flume 0.17.0 reads every role from the roles file of a source the host declares, and refuses a launch naming an address no source declares where no answerer stands behind its stream. crew's runner names `<label>/planner` or `<label>/ops` as the recipient of every place it launches (`plugin/lib/runner.py`), and every main-level role on deneb stands as a Claude Code agent crew keeps in herdr. So a host on Flume 0.17.0 needs crew's roles file, declaring those agents at their addresses, or it refuses every launch crew asks for.

## Decision

1. **crew writes `~/.local/state/crew/flume/roles.toml`, and nothing else does.** On each host where crew keeps a main level, whole, renamed over the old one, never edited in place, from the teams file. The fleet declares the source alone, `sources/crew.toml` naming this file and the kinds folder.
2. **crew's follower writes it at each read of the teams file, and a main-level start writes it again.** The follower, swancloud's job, which the deploy starts again whenever crew's pin moves, already reads the teams file at each tick and within seconds of it moving; so the deploy that brings this crew brings the file, with nothing run by hand. crew writes it again when it starts a main-level role's agent. It writes only when the bytes differ, and runs no `flume` command.
3. **One standing entry for each role that stands, at `<label>/<role>`.** For each of the five roles of each partition whose machine is this host, the stream being the partition's own: `agent` the herdr name crew gives it, `<label>-<role>`; `session` the session crew opens it in, the role's own where the teams file names one, else the partition's (the reviewer beside the planner, record 0035); no kind or run key. A partition on another host gets no entry until a place here must reach it, then a carried one; a role whose `flume` names a stream gets none until its crossing, which brings its run's entry.
4. **What a role answers is the words crew's briefs give for whom to ask, from one text.** The design agent the design; the planner the plan; ops a live system, a deploy or a landing. The briefs' sentence is built from the same table, so ops's words there gain "a landing", which the operator's brief already sends to ops. The operator gives `answerer = true`, its stream's door, and no `answers`, the briefs giving no words for asking it; the reviewer gives neither, so nothing asks it questions.
5. **crew's kinds folder, `~/.local/share/flume/kinds/crew`, exists and is empty.** No role runs as its kind yet, so the host locks nothing of crew's; crew's role kinds go into it as packages with the first crossing.
6. **Unchanged:** the teams file and its version, any launch's recipient, and anything on crew's main.

## Considered options

- **crew writes the file from its teams file (chosen).**
- **The fleet writes it from `lib/crew-teams.nix`.** Not taken: swancloud 0042's own reason, a second list of crew's agents' names and sessions beside crew's (swancloud `lists.1`), in a file Flume gives to the source's own tool.
- **wldn declared carried on deneb now.** Not taken: no place on deneb reaches wldn's roles, and a carried address is listed in every stage's prompt there for nothing.
- **crew's role kinds shipped as packages in this release.** Not taken: the host would lock and trust content no role runs yet.
- **The deploy runs a crew command that writes the file.** Not taken: the fleet would run crew's write beside declaring the source, where the follower the deploy already starts again writes it.
- **crew's session-start hook writes it.** Not taken: every Claude session on the host runs it, under every account, many at once after a restart.

## Consequences

- The change `crew-writes-its-flume-roles-file` builds it on `teamless/deneb`; once it lands, agentplot-design names the tip to swancloud for the deploy that brings Flume 0.17.0, `sources/crew.toml` and that pin to deneb together.
- Each role's crossing trades its standing entry for a run's entry, `agent` for `kind`, in the order of Flume record 0039, the operator's bringing crew's first kind into the kinds folder.
- The rule `teams.25`.
