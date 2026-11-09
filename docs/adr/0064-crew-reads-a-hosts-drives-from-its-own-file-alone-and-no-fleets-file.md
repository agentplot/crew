---
status: accepted
date: 2026-11-09
decision-makers: agentplot-design
---

# 0064. crew reads a host's drives from its own file alone, and no fleet's file

Status: accepted on 2026-11-09 by agentplot-design. It is the design agent's own choice, made on the rules and records written (`briefs.15`), to carry the user's choice in agentplot/boomdrive record 0009's amendment of 2026-11-09.

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
- swancloud gives crew those facts through crew's module options on each host it configures. At the switch that takes the crew release reading its own file alone, an agent moves each host's facts from the hosts file into those options by hand. No code reads the hosts file meanwhile.
