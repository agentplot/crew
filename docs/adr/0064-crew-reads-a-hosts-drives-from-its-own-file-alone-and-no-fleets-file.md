---
status: accepted
date: 2026-11-09
decision-makers: agentplot-design
---

# 0064. crew reads a host's drives from its own file alone, and no fleet's file

Status: accepted on 2026-11-09 by agentplot-design. It is the design agent's own choice, made on the rules and records written (`briefs.15`), to carry the user's choice in agentplot/boomdrive record 0009's amendment of 2026-11-09. Amended the same day, below: each role's way of running and the batch setting say what they mean, on the user's words in the pane.

Deciders: agentplot-design, on the question of the construct of `crew-makes-a-new-drives-state` (2026-11-09): "crew loads only with swancloud's hosts file, ~/.config/swancloud/herdr-hosts.json [...] Such a Mac runs no swancloud, so it has no hosts file, and principle 10 lets neither crew nor setup write swancloud's file". The user chose, on their card of 2026-11-09, that a colleague's Mac gets Boomdrive's programs from Nix with "a setup command does the rest", running their own drive with crew "the same way I'm working today" (agentplot/boomdrive record 0009, amendment of 2026-11-09).

Sources: record 0058, which says "A host configured only through the module still needs the hosts file until crew stops reading it"; record 0061, which calls the hosts file swancloud's, "which the flake retires"; agentplot/boomdrive records 0009 (amendment of 2026-11-09) and 0023; rule `code.5`.

## Context and problem statement

crew reads two files: its own teams file and swancloud's hosts file. The hosts file gives each drive's machine, its herdr session and that session's folder, the Claude account each role runs under, and each host's kind and ssh name. crew refuses to load without it. A person's Mac set up by Boomdrive's setup runs no swancloud, so it has no hosts file. Neither crew, nor its module, nor setup may write swancloud's file.

## Considered options

1. **crew reads every fact of a host's drives from its own file (chosen).** The facts the hosts file gives move into crew's teams file. crew's module writes them where Nix configures the host, and crew's own command writes them where setup does.
2. Setup writes a hosts file for the person. Not taken: it is swancloud's file, and no tool writes another's (record 0058, principle 10).
3. crew reads the hosts file where one exists and its own file elsewhere. Not taken: two sources for one fact, and a fallback the user's rule rules out ("I want the system to be built the way it should be and then have agents fucking fix the data transition as necessary").

## Decision outcome

Option 1.

- **One file.** crew reads a host's drives, and everything it needs of the hosts that serve them, from its teams file alone, on every host: each drive's machine, its herdr session and folder, the Claude account each role runs under, and each host's kind and ssh name. It reads no file of swancloud's or of any fleet's.
- **Every fact written out.** As `code.5` has it, no field has a default. The values a person's Mac takes are setup's to write: a session named for the drive, herdr's own folder for it, and the login's own Claude account.
- **Who writes it.** crew's module, from its options, on a host Nix configures (record 0058). crew's own command, at setup's asking, on a host Nix does not configure (agentplot/boomdrive record 0009). The command writes nothing where Nix links the file, and says so.
- `code.5` is amended in this commit: crew reads its teams file alone.

### Consequences

- A unit makes crew run from its own file alone. `crew-makes-a-new-drives-state` follows it, so a new drive's entry holds every fact crew then reads.
- swancloud gives crew those facts through crew's module options on each host it configures, filled at build time from its own one list of hosts (swancloud `herdr.1`), in the change that takes the crew release reading its own file alone. That is swancloud reading its own list. No code of crew's reads the hosts file, which swancloud keeps publishing for its other readers.

## Amendment, 2026-11-09: each role's way of running and the batch setting say what they mean

Status: accepted on 2026-11-09. The direction is the user's, in the pane, reading a drive's settings as the Boomdrive flake would write them. Of `flume = { design = false; planner = false; reviewer = false; ops = false; operator = false; };` they said: "I don't understand what this section is about and why we're turning these things off". Of a number among the settings: "a comment should explain the units/options". The names are agentplot-design's own choice, cheap to change.

### Context

A drive's `flume` gives each of its five main-level roles `false` while the role stands, crew keeping its agent running in its pane on the drive's machine, or the name of the Flume stream its runs run in, the host's runner having Flume run it while something is pending for it (record 0047, move 6; record 0057). Read as a setting, `design = false` says Flume is turned off for the design agent, and nothing of a standing agent. The stream it names can only be the drive's own: a drive is its stream, named by its label (agentplot/boomdrive record 0028), and the address crew declares for a role in its roles file is `<label>/<role>`, which Flume reads as a role of the stream `<label>`. And `review = { every = 5; hours = 4; }` says what `hours` counts and not what `every` does.

### Decision outcome

- **`runs`, how each role runs, in place of `flume`.** It names each of the five main-level roles, `design`, `planner`, `reviewer`, `ops` and `operator`, with `"standing"`, crew keeping the role's agent running in its pane on the drive's machine, or `"on-demand"`, the host's runner having Flume run the role in the drive's own stream while something is pending for it, each run ending when its work is done. No stream is named: it is the drive's. Every role is still written out, never once for all (record 0065, point 2; `code.5`).
- **`review`'s keys say their units.** `after_changes`: a batch is due once this many constructed changes wait for the user's read, a whole number of at least 1. `after_hours`: or once this many hours have passed since the last batch with at least one change waiting, a number above 0. The module's description of each option says its unit and its range.
- **`crew drive set` takes them as the file names them**: `--runs <role> standing|on-demand`, given for each of the five roles, and `--review <after_changes> <after_hours>`.
- **The file stays at version 6.** crew v0.54.0, the first to read version 6, was released the same day, and no host writes a version-6 file yet: deneb's file is version 5, under the crew 0.49.0 swancloud pins. A version-6 file naming `flume` or `every` is refused naming the key, and is written again by the module or by `crew drive set`. No code reads the older names (the user's rule against transition code, quoted above).
- `code.5` and `flake.2` are amended in this commit.

Not taken:

- **`standing`, a list of the roles that stand, every other on demand.** It names the five roles once for all, the default record 0065's point 2 refuses.
- **A stream name kept for a role on demand.** It can only be the drive's, so it would be one fact written twice.
- **`true` and `false` under a renamed key, `stands`.** A reader still has to learn what the other value does.
- **Version 7.** A new version for names no host has written.

### Consequences

- A unit renames them in crew's module and its option descriptions, crew's reading of the file and its refusals, `crew drive set`, the README, the operator's brief and the crew skill, and the test files, crew's next release carrying it.
- Whatever writes crew's file, swancloud's configuration or the Boomdrive flake's, writes `runs` and `review.after_changes` and `review.after_hours` once it takes that release.
