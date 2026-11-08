---
status: accepted
date: 2026-11-08
decision-makers: agentplot-design
---

# 0061. crew names a kept repository's folder and checkout from its teams file: the runner's container and view on a runner host

Status: accepted on 2026-11-08 by agentplot-design, the design agent's own choice, made on the rules and records written (`briefs.15`).

Deciders: agentplot-design, on afterthought-design's ask of 2026-11-08, relayed by agentplot-operator, for afterthought/swancloud record 0060 (accepted by the user that day; afterthought/swancloud:docs/adr/0060-a-runner-host-keeps-one-copy-of-each-repository-now-its-queues-on-the-runners-clone-before-the-boomdrive-flake-is-ready.md, d7c8c3bc).

Sources: swancloud record 0060, under which a runner host keeps one copy of each repository, the runner's clone, and every agent that submits works in worktrees of it; agentplot/boomdrive's `core.14`, under which the runner's clone is the host's one clone; agentplot/boomdrive record 0023, under which the Boomdrive flake configures the host, crew by its own module; this repository's record 0058 and `flake.1` and `flake.2`, under which crew's module writes crew's teams file whole from `services.crew.settings`, which Boomdrive's module may set; `roles.9`; `read.2`.

## Context and problem statement

crew names a kit's folder `<session dir>/<name>` and its checkout `<session dir>/<name>/main`, from the sessions the host's hosts file lists (`crew.py` `checkout`, `kit_kept`). On a runner host after swancloud record 0060, a kept repository's one copy is the runner's container, which holds the bare clone and the places and has no `main`, and its default branch's working tree is the runner's view. Every main level's brief must name those, and crew must learn them from somewhere.

## Considered options

1. **crew's own teams file names each kept repository's folder and checkout (chosen).** It is written for the host by whatever configures it: swancloud today, and Boomdrive's module through `services.crew.settings` once the flake is ready. That is one source, the host's configuration of the runner.
2. **The hosts file swancloud publishes.** Not taken: it is swancloud's file, which the flake retires, and crew would read the runner's layout from a second tool's list.
3. **The runner's report on its branch.** Not taken: crew could not name a folder until the runner had reported, and a brief is built before any launch. It also adds to the control-plane contract something that is the host's configuration and no part of the work.

## Decision outcome

Option 1.

- crew's teams file may name, for the host it is written on, each kept repository by its address, `<owner>/<name>`, with its `dir`, the folder crew names as the kit's, and its `checkout`, the working tree crew names as the kit's checkout. On a runner host these are the runner's container and the runner's view.
- Where the file names a repository, crew names that folder and checkout in every main level's brief and wherever it reads a kit's folder on the host. Where it names none, crew names them as it does today.
- Design worktrees and every other worktree crew's agents cut are worktrees of that folder's clone.
- A change to the file's shape changes crew's module and its pinned file in the same change (`flake.2`).

## Consequences

- One crew unit builds it on crew's main. deneb's pin moves to the release that carries it on the user's word. No fix is made only for the teamless line.
- swancloud writes the key for deneb's kept repositories in its change `each-repository-is-queued-in-the-runners-copy`. Boomdrive's module writes it once the flake is ready.
