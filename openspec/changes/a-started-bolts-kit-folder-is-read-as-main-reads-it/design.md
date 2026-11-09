# Design: a started bolt's kit folder is read as main reads it

## Context

**The ruling.** agentplot-design, on the bolt `crew-reads-each-piece-as-the-tools-hold-it`, resting on crew record 0061, the kit-rename change's design R2, and record 0055. The proposal quotes it whole.

**What the bolt had built.** Decision 1 of the archived `a-bolts-landing-on-main-reads-landed` took a kit's folder from the taking runner's `repositories.rec` alone:
- `runner.kept_folder` refused a runner that reports no repositories;
- `runner.where` took no folder from a place's status;
- `plan.launched_at` and `kit_at` lost their fallbacks to the kit's other work's places.

Its Decisions 2 and 3, the landing read from main's first-parent line and a landed bolt's pieces read from that landing, and its stub runner's `repositories.rec` (Decision 4), stand.

**What crew main reads, at `origin/main` on 2026-11-08.**
- `runner.where`: the folder `repositories.rec` names, else Flume's status of the newest place the taking runner carries of the launches.
- `plan.launched_at`: where that gives none, `kit_at` of the same host, by its newest place of the kit's other work.
- `kit_at` and `launch_repositories`: refused, naming the host, where none is given.

**Why the report alone was early.**
- Boomdrive's runner does not write `repositories.rec` yet: R2 of `a-kit-renamed-on-its-host-is-renamed-across-the-plan` is not built (agentplot/boomdrive `c6eb79b`). R2 itself says what crew does meanwhile: "Without R2, crew takes a kit's folder from a place's status as today".
- Record 0061 names a kept repository's folder from crew's own teams file. It turned down the runner's report as the one source (its option 3), since crew could not name a folder until the runner had reported.
- Record 0055 is rejected, but its Decision 6, the runner reporting what it keeps, stands. So `repositories.rec` is read first wherever a runner writes it.

**Rules this change relies on:**
- `read.1`: a kit neither the report nor a place names is unread, and the refusal names the host and both readings that failed.
- `read.2`: Flume's status is read as `runner.flume_facts` checks it.
- `roles.9`: crew reads where a kit's work runs from the runner that took it, never from a host it chose.
- `roles.5`: the fallback is crew main's read, kept until the runner reports its repositories, not a new mechanism.
- `code.7`: `kept_folder`, `where` and `launch_repositories` stay functions of facts.
- `docs.2`: README, the crew skill and the usage header change together.
- `tests.4`, `tests.11`: each case is in the logic tier.

**Area pages this change touches:**
- `core.md` (`read.1`, `roles.5`, `roles.9`, `code.7`);
- `plan.md` (`plugin/lib/plan.py`);
- `teams.md` (`plugin/bin/crew`);
- `briefs.md` (`plugin/skills/`);
- `tests.md` (`tests/`);
- `docs.md` (`README.md`, `openspec/`).

It departs from no rule. No rule page is edited (`docs.7`).

**The family.** Where a repository is kept is Boomdrive's runner's (`core.5`, `core.11`). crew reads its report first, and reads a place's folder only while the runner reports nothing. Once R2 is built, every reading takes the report, and the fallback reads nothing. Retiring the fallback is a change of its own, made once every host's runner writes `repositories.rec` (`roles.5`).

## Decisions

### 1. The folder: the report, else the newest place of the kit on that host

`runner.kept_folder(reading, kit, what)` answers `(None, None)` for a runner that reports no repositories (`repositories` None). It answers as before where the runner reports them: the folder, none by the kit's name with the rename named, or two by it.

`runner.where` takes the folder `kept_folder` gives. Where that is None, it takes the `repository` Flume's status names of the newest place the taking runner carries of the launches. Where neither names one, it gives `dir` None.

`plan.launched_at`, for a bolt whose `where` gives no folder, asks `kit_at` for the kit. It takes that folder only when `kit_at`'s host is the bolt's taking runner's host, with the bolt's stream or else the kit's. This is crew main's code, restored.

The path not taken is the report alone. It holds every started bolt unread on a host whose runner reports no repositories, which is every host whose runner Boomdrive has not yet given R2.

### 2. The refusal names the host and both readings

Where no folder is given, `launched_at`, `kit_at` and `launch_repositories` refuse:

> the runner on `<host>` took bolt `<bolt>`'s work, reports no repositories it keeps and carries no place of `<kit>`'s work naming its folder, so crew can't tell where it keeps `<kit>` there

`kit_at` says the same of `<kit>`'s work. `launch_repositories` ends "so crew can't tell where a launch of it would be made". Each names both readings that failed (`read.1`): crew main's words named the place alone, and the bolt's the report alone.

### 3. A runner that reports its repositories is read by them alone

A runner whose `repositories.rec` names none by the kit's name is still refused, naming what it keeps and `crew kit rename`. Its places are not read for the folder: a runner that reports what it keeps has said where the kit is not. This is unchanged from crew main and from the bolt.

## Risks / Trade-offs

- **A place's folder can be stale.** A place cut before its clone moved names the old folder. Accepted: that is crew main's read today, and a runner that reports its repositories wins over its places (drive-state "A kit renamed under its place").
- **On a host like deneb on 2026-11-08 the bolt still reads unread.** No `repositories.rec` and no place carried leaves nothing to read. Accepted on the ruling: the kit reads unread, naming the host, until the runner writes `repositories.rec`.

## Task notes

**1.1** `plugin/lib/runner.py`:
- `kept_folder`: `(None, None)` where `reading["repositories"]` is None.
- `where`: `"dir": folder or` the first `repository` of the newest carried places' `flume_facts`.
- `launch_repositories`: refuses `at` with no `dir`, in Decision 2's words.

Cases in `tests/py/test_runner.py` `TestWhere`, and `tests/py/test_branch_stands.py` `TestWhereALaunchWouldBeMade` and `TestAtItsProposal`.

**1.2** `plugin/lib/plan.py`:
- `launched_at`: crew main's fallback to `kit_at` on the same host, then the refusal in Decision 2's words.
- `kit_at`: the refusal where `at["dir"]` is None.

Cases in `tests/py/test_kits.py` `TestWhereABoltRuns`: a runner reporting no repositories read by its place of the bolt's work and by its place of the kit's other work; the 2026-11-08 reading refused naming deneb. Cases in `tests/py/test_stages.py` `TestABoltWhoseLaunchesWereAllRefused`: read on deneb by its place of `y`'s work with no `repositories.rec`, and refused where that place is alpha's.

**2.1** README's State sentence on where a started bolt's work runs, and its runner branch's `repositories.rec`; the crew skill's Flume paragraph; `crew`'s usage header.
