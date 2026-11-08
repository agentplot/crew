# Design

## Context

`crew kit rename <old> <new>` on main is what `a-kit-renamed-on-its-host-is-renamed-across-the-plan` built (`plan.py` `op_kit_rename`, `rename_refusal`, `renamed_in`). It:

- sets the `Repo` of every Bolt and Unit record naming `<old>`, a started bolt's included;
- writes a `kit.rename` entry;
- is refused unless the main-level host's spaces keep `<new>` and not `<old>`;
- refuses a name an earlier rename renamed, through `kit_now`.

Everything else stays under `<old>`, for readers to map through `kit.rename` entries.

Record 0060, accepted by the user on 2026-11-07, decides otherwise. A repository's state is renamed by one explicit command, once its work is finished. Around the rename:

1. the repository's work lands or is dropped;
2. the repository is removed from the runner, Flume and sluice;
3. it is renamed on its forge;
4. crew's rename runs;
5. it is added back under the new name.

The rename renames every record a reader matches the repository by, as record 0055's decision 2 lists them. It closes and raises no card, since none may stand. A partition is never renamed. `plan.22` and `record.4` (as amended) say so.

The held fix `fix/a-kit-rename-renames-every-record-naming-it` (a31916d7 in deneb's crew repository, built on `teamless/deneb` for record 0055) holds the renaming of every record: `renamed_kit`, `renamed_object`, `renamed_source`, `renamed_field`, `rename_rec`, `rename_branch`, `proposal_names` and `appended_refusal`. This change takes those as its start. It leaves out the fix's card step (`rename_cards`, `keep_alternatives`), its rename of kept entries at push (`record.renamed_kept`) and its rename of `asks.rec`. It replaces the fix's refusals with record 0060's.

**What names a repository on a drive's branch, read on main at 7a7b8acd:**

| File | Field naming a repository | Renamed |
|---|---|---|
| `plan.rec` | Bolt and Unit `Repo`; a `Source` `<owner>/<repo>:docs/adr/<n>` (`RECORD_REF`) | Sources; no Bolt or Unit names `<old>` when the rename runs (Decision 2) |
| `requests.rec` | `Repo`; `Work` of a fix of main, `fix/main/<repo>/<name>` | both |
| `runs/<host>/<day>.rec` | `Repo` (`bolt.land`, a landing's submission, `role.land`, `kit.rename`); `On`/`From` objects `kit/`, `land/`, `queue/`, `record/<repo>/<n>`, `fix/main/<repo>/<name>`; a card's `Key` | `Repo`, `On`, `From`, but no `kit.rename` entry and no `Key` |
| `asks.rec` | an ask's `Key`, `submission/<repo>/<n>` | no |
| `roles.rec` | a role's `Repository`, the partition's first blueprints repo | no |
| `proposals.rec`, `moves.rec`, `signals/` | words | no |
| `<label>/runner/<host>` | the runner's own records (`state.5`) | no |

**Rules this rests on:**

- core: `state.1`, `state.4`, `state.5`, `roles.1`, `roles.2`, `roles.9`, `read.1`, `read.2`, `read.5`, `code.2`, `code.4`, `code.7`, `code.8`;
- `plan.md`: `plan.1`, `plan.2`, `plan.3`, `plan.4`, `plan.12`, `plan.22`;
- `record.md`: `record.1`, `record.2`, `record.3`, `record.4`;
- `briefs.md`, for the planner's brief: `tests.6`;
- `docs.md`: `docs.2`, `docs.4`, `docs.6`, `docs.7`;
- `tests.md`: `tests.4`, `tests.10`, `tests.11`, `tests.12`.

## Goals / Non-Goals

**Goals:**

- `crew kit rename <old> <new>` runs only once `<old>`'s work is finished and no host keeps `<old>`. It names everything that stands when it refuses.
- After it, every record a reader matches the repository by names `<new>`, in one commit with its `kit.rename` entry.
- Running it again renames whatever an earlier rename left.
- `requests.rec` and the run record keep their append-only rules, except for the rename.
- No crew command renames a partition.

**Non-Goals:**

- Taking out `kit_now`, `renames_in`, `renames_at`, `launches_now`, `Write.renames`, `kit_given`, `former_said` and every other read through `kit.rename` entries. That is `no-reader-maps-a-kits-former-name` (Decision 9).
- Removing the repository from the runner, Flume or sluice, renaming it on its forge, or adding it back. Each is that tool's own removal and addition (record 0060, decision 2).
- The way-on words of `main_kit_said` and `runner.kept_folder`, which name `crew kit rename` for a kit a host keeps none of. The rename's own refusal now names what stands, which is the way on.
- A drive's name on disk in a hosted Boomdrive, which is Boomdrive's to design (record 0060, decision 6).

## Decisions

### 1. What the rename renames, field by field

Taken from the held fix:

- `renamed_kit(value, old, new)` renames a field holding a repository and keeps its form:
  - a name becomes `<new>`'s name;
  - a forge address `<owner>/<old>` becomes `<owner>/<new>`, unless `<new>` is given as an address, so a reader matching by address keeps the owner.
- `renamed_object(obj, old, new)` renames `kit/<old>`, `land/<old>`, `queue/<old>`, `record/<old>/<n>` and `fix/main/<old>/<name>` to `<new>`'s name, and leaves any other object as it is (`KIT_OBJECT`, without the fix's `submission/`).
- `renamed_source(source, old, new)` renames each decision-record reference whose repository names `<old>` (`RECORD_REF`), and leaves the rest of the line as written.
- `renamed_field(field, value, old, new)` dispatches by field: `Repo` to `renamed_kit`, `Source` to `renamed_source`, and `On`, `From` and `Work` to `renamed_object`.
- `rename_rec(text, fields, old, new)` rewrites a recutils text record by record:
  - it renames only the fields named, and leaves every `kit.rename` entry whole;
  - it keeps descriptors, comments and the order of records and fields byte for byte;
  - it returns the text and how many records changed.
- `RENAMED_FIELDS`: `plan.rec`: `Source`; `requests.rec`: `Repo`, `Work`; `runs/`: `Repo`, `On`, `From`.

`rename_branch(w, old, new)`, in the write, renames:

- the plan's records, by `Source`;
- `requests.rec`;
- every `.rec` file under `runs/` at the tip.

It replaces a file only where a record of it changed. It records the rename on the write (`w.renaming`) and returns the count, which is the entry's `Count`. `Write` gains `paths(prefix)` and `texts(paths)`, which list and read the branch's files at the tip in one pass, as `runs_at` reads them (`paths_at`, `cat_file`; `plan.12`).

What is left as written, and why:

- **No Bolt or Unit `Repo`.** None names `<old>` when the rename runs, since one would refuse it (Decision 2), so the plan's part of the rename is its Sources.
- **No `Key`.** A card's key is the key Pending You held it under. No card under `<old>` stands open (Decision 2), so every key naming `<old>` belongs to a closed card and is history. Renaming it would name a key Pending You never held.
- **No `kit.rename` entry.** It records an earlier act. The held fix kept only its `From`. A later rename that renamed its `On` and `Repo` would say the earlier act gave a name it never gave.
- **No `asks.rec`.** An ask's `Key` is matched whole, to write an ask once (`ask_write`), and nothing looks a repository up from it. Record 0060's decision 4 lists the plan, `requests.rec`, the run record and sources. The held fix renamed `submission/<repo>/<n>`; not taken.
- **Words, the runners' branches and each host's own files.** No reader looks a repository up from words (record 0055, decision 3). The runners' branches are the runner's (`state.5`). A host's file is never rewritten (`record.4`); the branch's copy of each entry it pushed wins, as `record.unpushed` takes the branch's lines for an `Id` the branch holds.

**Alternatives considered:**

- *Rename every occurrence of the name, words included.* Not taken: a Goal's "tailrace" may name a tool or a folder, and a closed proposal's `Do` is what the user approved (`plan.4`).
- *Keep renaming Bolt and Unit `Repo`.* Dead code once Decision 2 refuses any.

### 2. When the repository's work stands

`rename_standing(old, plan, requests, reads, entries, proposals, own)` is a decision of plain facts (`code.7`). Its inputs:

- the plan as the write holds it;
- `requests.rec`'s records;
- the partition's runners as the write read them (`w.runners()`);
- the whole run record at the tip, parsed from the files `rename_branch` reads, each entry once, by `At` and `Id`;
- `proposals.rec`'s records;
- `own`, the number of the proposal applying the rename, or None for a direct run.

It returns what stands and what crew could not read, each as words. `<old>` matches by name or address (`kit_in`) throughout. What stands:

- **Plan work.** Each bolt whose `Repo` names `<old>`, "bolt `<b>` has not landed", and each unit or chore of the queue naming it. A unit in a bolt is in a bolt of its own repository (`plan.1`), so naming the bolt covers it. A landed or dropped bolt has left the plan, which is how crew knows its work finished (`state.2`).
- **A fix of main or a role's work.** This is work the plan never holds: a launch of `fix/main/…` or `role/…` whose `Repo` names `<old>`, standing (`runner.standing`). Its stage is read by `runner.piece_stage`. It stands unless that stage is `landed`, `dropped` or `refused`. `unknown` is unread, with its why. The runner keeps a place record of such work after Flume tidies it (boomdrive's `the-runner-carries-crews-work-into-flume`, "Work the plan never holds keeps its last record"), so its end stays readable.
- **A live place.** Each place a runner carries (`reading["places"]`) whose launch's `Repo` names `<old>`, and whose phase in Flume's status (`runner.flume_facts`) is `live` or `making`. A place whose status can't be read is unread, and so is a reading whose `why` is set (`read.1`). This catches a unit's place still live after its unit was dropped, which the plan no longer shows. A place of a fix of main or a role's work is left to the item above, which judges it by its stage, so one piece of work is named once.
- **A card.** Each key under which the newest card is open or closed as lost (`cards.posted_cards`), keyed `land/<old>`, `record/<old>/<n>` or `record/<old>/<n>/<commit>`, named with its owner. A card lost to its owner is raised again by the rail, so it still stands.
- **A batch.** Each batch key neither closed (`batch_closed`) nor settled (`batch_settled`) that holds a unit of `<old>`'s work. A unit is `<old>`'s by the plan's unit, or by a `bolt.land` entry naming `unit/<u>` with `Repo` naming `<old>`. Settled means the batch waits on nothing, and the rail's sweep closes it.
- **A proposal.** Each open proposal other than `own`, any of whose `Do` lines names `<old>` (`proposal_names`). That is any word after the command's own that holds the name or address, an object built on it, or a decision record's source in its repository. A quoted goal or intent is one word, so a name inside its prose names nothing. Another open proposal holding the same rename names `<old>` too.

**Alternatives considered:**

- *Judge every launch naming `<old>` by its stage.* Not taken: the runner may drop a place record once its work has left the plan, and `stage_of` reads a launch answered with no place record as `launching`, so every repository with history would read as standing forever. The plan judges plan work. The place records judge what the plan never holds, and what is live.
- *Refuse only on what the plan holds.* Not taken: record 0060's decision 3 lists places, cards, batches and proposals, each of which outlives a plan record.

### 3. Where crew reads what a host keeps

`rename_kept(old, hosts)` is a decision of plain facts. `hosts` holds, for each host read:

- its runner's report: `reading["repositories"]`, None for a runner that reports none, or the reading's `why`;
- its spaces in the hosts file: the repositories its sessions keep, or None for a host the hosts file doesn't list.

The hosts read are each host with a runner branch of the partition (`runners`), together with the partition's main-level host, whose spaces `main_kit` already reads. For each host:

- the runner's report, where it gives one;
- otherwise the host's spaces;
- a host whose runner can't be read, or that neither reports nor is listed, is unread (`read.1`).

A host keeps `<old>` where a repository it keeps has `<old>`'s name, or is `<old>`'s address when `<old>` is given as one. Two kept by the name are both named. No host needs to keep `<new>`: the repository is added back under it after the rename.

**Alternatives considered:**

- *The runner's report alone, refusing for a runner that reports none.* Not taken today. No runner writes `repositories.rec` yet: boomdrive's runner at origin/main, read 2026-11-07, writes `runner.rec`, `answers.rec` and `places.rec`, and madswan's, afterthought's and agentplot's runner branches on deneb hold just those. Every rename would be refused until boomdrive builds the report.
- *The main-level host's spaces alone*, as today's rename reads them. Not taken: record 0060's decision 2 names any host's runner.
- *Require `<new>` kept.* Today's check. It contradicts record 0060's order, where the repository is added back after the rename.

This reads whether a host still keeps a name, and only to refuse. It never reads where a kit's work runs, which `roles.9` keeps to the runner's report. The hosts file is swancloud's, written from the same host configuration as the runner's file (`roles.9`).

### 4. The refusal

`rename_refusal(label, old, new, bolts, stands, unread, kept, unkept, count)` is a decision of plain facts. It refuses, in this order:

1. two names of one repository;
2. a `<new>` that is a bolt's name, since `land/<new>` would name the bolt;
3. any work that stands or that crew could not read, in one message: "crew can't rename `<old>` while its work stands: …; its work lands or is dropped first", then what crew could not read;
4. any host that still keeps `<old>`, or whose keeping crew could not read: "…; `<old>` is removed from the runner, Flume and sluice before crew renames its records";
5. with `count` 0 once `rename_branch` has run: "no record of `<label>`'s names `<old>`: neither its plan's sources, its requests nor its run record".

Steps 1 to 4 are checked before anything is renamed, and step 5 after, as the held fix did. Each check runs in the change function at the tip it is applied to (`plan.1`), so a replay checks again. A refusal writes nothing and leaves a refused `kit.rename` entry (`record.1`). Its words are crew's own (`record.3`, `code.2`).

### 5. Running again, and this host's kept entries

`<old>` may be any name a record still holds. Today's refusal of "a name a rename already renamed" goes, with its `kit_now`. So a repository renamed before this change, madswan's `flywheel-cloud` and `tailrace` among them, is finished by running the same rename again. That run renames what the first left and writes its own entry.

Entries a host kept unpushed (`record.2`) still name `<old>` in that host's file. The rename's `prepare` runs `record.reach(label)` on the host it runs on, before the write reads the branch, so that host's kept entries reach the branch first and are renamed with the rest. `prepare` returns None, since `direct` and an approval call what it returns as an undo. A push that is refused refuses the rename, naming it, as `crew events --push` does. An entry another host pushes under `<old>` after the rename is renamed by running the rename again.

**Alternatives considered:**

- *Rename a kept entry at its push by the `kit.rename` entries written after it* (the held fix's `record.renamed_kept`). Not taken: it reads the run record's `kit.rename` entries to map a name, which `plan.22` rules out.

### 6. Append-only, except for the rename

`appended(w)` checks that a write only appends to `requests.rec` (`runner.append_refusal`). It reads the tip's requests through each rename the write made (`w.renaming`, `rename_rec`), as the held fix's `appended_refusal` does. A request may change by its repository's name alone, and only in a rename's write. Every other change is refused as before. The run record's files on the branch are checked by `recfix --check` as every file a commit holds (`plan.1`). The rename's commit holds what each record said before (`state.1`), so no history is lost (`record.4`).

### 7. Who runs it, and the proposal's card

Who may run it is unchanged:

- the user at a shell;
- the planner by proposal; its direct run is refused naming `crew plan propose`;
- every other agent crew started is refused naming the planner (`roles.1`, `may_write`).

An approval applies it at the tip (`plan.3`). The proposal applying it is `own` and names nothing against itself.

`cards.renamed_drawn` draws a RENAME KIT block naming `<old> → <new>`. It says the repository's work is finished and that its launches, landings and record sources are renamed. It names no bolt or unit and returns no section, so the picture draws nothing for it. The card stays a plain approval. The rest of its signature is kept, so `drawn` calls it as before. `drawn` writes a block drawn in no section after the sections in the card's text, and a card of renames alone, which has no section to title it by, is titled by the repositories it renames, "Plan change to flywheel-cloud and tailrace"; titling it by the new names was not taken, since the card asks about the repositories as their records name them now.

### 8. A partition is never renamed

There is nothing to build: crew has no command that renames a label, and `crew kit rename --label <l>` acts within `<l>` alone. A label the teams file no longer names is refused by `crew.partition_of`, naming the partitions it has. A new label's state is its own branch, `<label>/main` (`state_of`), made by `crew state init`. rail-cards' "A card in a former name cards no row" already maps no former name and takes no partition as another's successor. The change pins this with a logic case and says it in README and the skill.

### 9. Where this change ends and `no-reader-maps-a-kits-former-name` begins

Both units are in the bolt `crew-reads-a-kit-by-its-name-alone`, cut from the same main, with no `After` between them.

This change owns the rename's own functions:

- `op_kit_rename`, `rename_refusal`, `renamed_in` and the functions above;
- `appended`;
- `cards.renamed_drawn`;
- the rename's words in README, the skill, the usage and the planner's brief;
- the requirements its delta names.

It drops the rename's own use of `kit_now`, `w.renames()` and `w.renamed`, since the records themselves now carry the new name; the other unit takes each of them out of crew.

The other unit owns every reader through the renames, and their requirements:

- bolt-plan's "What crew recorded under a kit's former name is read under its name now" and "A command given a kit's former name writes its name now";
- rail-cards' "A kit's landings card follows its rename";
- drive-state's name-now clauses.

So this delta leaves those requirements alone. The other unit's delta also adds bolt-plan's "requests.rec and the run record are only appended to", whose rename appends only its entry; this change's rewrite contradicts it, so this delta removes it, the rule and its one exception standing in drive-state's and run-record's requirements as this delta modifies them. Both units change run-record's "A kit's rename is one entry naming both its names": this delta's block holds the other unit's sentences and its scenario "A rename's entry renames nothing" beside its own. Where the two units edit the same code and words (`rename_refusal`'s signature, `Write`, `test_kit_rename.py`, `test_recfix.py`'s rename case, README's rename paragraph, the skill, the usage and the planner's brief), this change takes the other's edit in: the rename's command and refusals are this change's, every read is as written, and nothing says a former name is read under the name now. The two meet on the bolt by a merge of it into this change's branch, never a rebase (`plan.8`).

### Departures

- **From `openspec/config.yaml`'s last-task rule** ("The last task runs the tests the change affects, `tests/suite --affected`"). This change's construct brief says no task runs the repository's whole checks or checks every part the change touches, since the verify stage runs the repository's whole checks once after every task. So no task runs `--affected`. Each task names its narrowest check: one test class or test by node id, or one end-to-end test by name.
- No departure from a rule in `docs/architecture/`. This change edits no page there or in `docs/adr/` (`docs.7`).

## Risks / Trade-offs

- **A rename rewrites every run-record file naming the repository in one commit.** Accepted: it is a rare act on the user's word, and only files holding a renamed entry are written.
- **An entry another host pushes under `<old>` after the rename.** It stays under `<old>` until the rename runs again. Accepted: record 0060's order removes the repository first, so little writes under it after.
- **The other unit's intent says the run record and `requests.rec` stay append-only "without exception".** That was written from record 0055's rejection. `record.4` as amended by record 0060, accepted, keeps the rename's one rewrite. Where the two meet, `docs/architecture/` wins (CLAUDE.md): this delta removes bolt-plan's requirement saying so, and this change's append check allows the rename alone.

## Migration Plan

1. This change is submitted to its bolt, `crew-reads-a-kit-by-its-name-alone`, through sluice, and lands on main with the bolt (`plan.16`).
2. A host gets it by its mode (`plan.19`): live at the timer's next move, released once swancloud's pin reaches a tag holding it.

**Rollback.** Run `crew kit rename <new> <old> --label <l>` once `<new>`'s work is finished and no host keeps `<new>`. It renames every record back and writes its own entry. The landing itself reverts like any other.

## After deploy

- **madswan's former names.** Once deneb's crew carries this change, and each repository's work under its former name is finished, the user runs:
  - `crew kit rename flywheel-cloud boomdrive-cloud --label madswan`
  - `crew kit rename tailrace timber --label madswan`

  That way no record of madswan's names either former name (record 0060, Consequences). The rename refuses, naming what stands, until each is finished.
  - Why no check can be code: it writes madswan's live records on afterthought/crew-state, which takes the user's word (`roles.1`, `roles.2`), and no test reaches that branch.
  - Environment: deneb, partition madswan. Doer: the user.

## Task notes

These hold for every task:

- A logic check runs one test class or test by its node id, as written: `devenv shell -- bash -c 'moon run tests:venv && tests/.venv/bin/python -m pytest -q -p no:cacheprovider <node>'`, from the worktree's root.
- A contract check runs the same command with a node under `tests/contract/`.
- An end-to-end check is `tests/suite <name>`, ending with "0 failed".
- Facts for logic cases go in `tests/py/facts.py` or at the top of `tests/py/test_repository_rename.py`.
- No task adds or removes an end-to-end test, so `tests/moon.yml` is unchanged (`tests.10`).
- Never run `wt submit --help` (CLAUDE.md).

**1.1** In `plan.py`, beside `kit_in`, add `renamed_kit`, `renamed_object` (with `KIT_OBJECT`: `kit|land|queue`, `record/<repo>/<n>`, `fix/main/<repo>/<name>`), `renamed_source`, `renamed_field`, `RENAMED_FIELDS` and `rename_rec`, as Decision 1 has them. They are pure functions over text; start from a31916d7's (`git -C ~/Code/github_afterthought/crew/crew.git show a31916d7:plugin/lib/plan.py`). Add a new `tests/py/test_repository_rename.py`, with class `TestWhatAFieldBecomes`. Cases:
- each object kind renamed by name;
- a forge address keeps its owner, unless the new name is an address;
- an object of another repository, `kit/tailrace-web`, unchanged;
- a Source's decision-record reference renamed and its words kept, and a Source naming no decision record unchanged;
- a `kit.rename` entry left whole;
- a text naming no `<old>` returned byte for byte with count 0.

**1.2** `Write` gains `renaming` (a list, in `__init__`), `paths(prefix)` and `texts(paths)`, reading at the tip as `runs_at` does. `FactsWrite` serves `paths` and `texts` from its `files`. Add `rename_branch(w, old, new)` as Decision 1 has it. Class `TestWhatTheRenameRenames`, over madswan's shape:
- request 3 with `Repo: flywheel-cloud` and a fix of main's `Work`;
- a runs file with a `bolt.land`, a closed `card.post` on `kit/flywheel-cloud` with `Key: land/flywheel-cloud`, and an entry whose `On` names `fix/main/flywheel-cloud/x`;
- a second runs file naming nothing;
- a crew unit's Source `agentplot/flywheel-cloud:docs/adr/0017`.

The case checks:
- each renamed;
- `Key` kept;
- the second file not replaced;
- the count 4 (or as the facts add up);
- `w.renaming == [("flywheel-cloud", "boomdrive-cloud")]`;
- a Goal naming the old name unchanged;
- `proposals.rec`, holding a closed proposal whose `Do` names the old name, not replaced.

**1.3** In `appended`, read the tip's `requests.rec` through `w.renaming` (`appended_refusal(was, now, renaming)`), as Decision 6 has it. Class `TestAppendOnly`:
- a rename's write with request 3 renamed passes;
- the same change with no rename on the write is refused, saying a request is never changed or removed;
- a rename's write that also changes request 3's `Name` is refused.

**2.1** `rename_standing(old, plan, requests, reads, entries, proposals, own)`, with `proposal_names` from a31916d7, as Decision 2 has it. It returns `(stands, unread)`, each a list of words. Class `TestWhatStands`, one case each:
- a bolt in `tailrace`, named as not landed;
- a queued chore in `tailrace`;
- a standing `fix/main/tailrace/x` at code, named with its stage, and one landed, one dropped and one refused named nothing;
- a `role/design/…` launch in `agentplot/tailrace`, not landed;
- a place of request 4 (`Repo: tailrace`) whose status reads live, and one reading over;
- a place whose status is no JSON, and a reading with `why`, each unread;
- a card open under `land/tailrace` by madswan-ops, one under `record/tailrace/17` by madswan-design, and one closed as lost;
- a closed card under `land/tailrace`, named nothing;
- batch 12, unanswered and unsettled, holding a unit a `bolt.land` with `Repo: tailrace` names; a settled one, named nothing;
- proposal 170 open with `--repo tailrace`; one naming `agentplot/tailrace:docs/adr/0017`; one whose goal's prose mentions tailrace, named nothing; the proposal `own`, named nothing; a closed one, named nothing;
- nothing standing: both lists empty.

**2.2** `rename_kept(old, hosts)` as Decision 3 has it. It returns `(kept, unread)`. Class `TestWhatAHostKeeps`:
- a runner reporting `agentplot/tailrace`;
- a runner reporting only `agentplot/timber`, whose host's spaces keep `agentplot/tailrace`, named nothing, since the report wins;
- a runner reporting none, whose host's spaces keep `agentplot/tailrace`;
- a runner reporting none on a host the hosts file doesn't list, unread;
- an unreadable reading, unread;
- the main-level host with no runner branch, its spaces keeping `tailrace`;
- two repositories by the name, both named;
- no host keeping it.

**2.3** `rename_refusal(label, old, new, bolts, stands, unread, kept, unkept, count)` as Decision 4 has it, replacing today's. Class `TestRefused`, one case per refusal, each asserting the message whole:
- one repository;
- a bolt's name;
- work standing, with two items in one message;
- unread work;
- a host keeping it;
- unread keeping;
- count 0;
- None when all is clear.

**3.1** `op_kit_rename`, as Decisions 2 to 5 have it:
- its `prepare` runs `record.reach(label)` and returns None;
- its change reads the write's plan, `requests.rec`, the run record's files (`w.paths("runs/")`, `w.texts`), `proposals(w)` and `w.runners()`;
- `own` is `None if ctx.direct else str(ctx.n)`;
- the hosts for `rename_kept` are the runner hosts with the main-level host, their spaces from `ctx.fleet["hosts"]`;
- it refuses (steps 1 to 4), runs `rename_branch`, refuses on count 0, and sets `Repo` and `Count`;
- the `after` prints "`<old>` is `<new>` in `<label>`'s records: N records renamed".

It drops its spaces tuple, `kit_now`, `w.renames()`, `w.renamed` and `renamed_in`'s use. Update `record.py`'s descriptor comment on `kit.rename`'s `Count`, every record renamed. In `tests/py/test_kit_rename.py`, remove `TestTheRename`, `TestRefused` and `TestTheStartedBolt`, whose behaviour this change replaces, and leave the rest of the file as it is. Class `TestTheCommand`, through `plan.OPS[("kit", "rename")]` with `known(...)` and `FactsWrite`:
- a direct run over finished work, with a fleet whose spaces keep neither name, renames and fills `Repo` and `Count`;
- a started bolt refuses, naming it, with the write's files and plan as they were;
- `prepare` called before the change, with `record.reach` monkeypatched to record its call;
- an approval's `own` excluded.

**3.2** Class `TestRunAgain`:
- a write whose plan already names `boomdrive-cloud`, while request 3 and two `bolt.land` entries name `flywheel-cloud`, renames those 3;
- an earlier `kit.rename` entry is unchanged byte for byte;
- a rename of `timber` to `trc` leaves the entry of `tailrace` to `timber` whole.

**3.3** Class `TestAPartitionIsNeverRenamed`:
- with a fleet naming `afterthought` and not `swancloud`, `crew.partition_of(fleet, "swancloud")` is refused naming the partitions, and `plan.state_of(fleet, "afterthought")[1] == "afterthought/main"`;
- `plan.do_args` reads `kit rename` as a repository's rename alone, with `--label` its partition.

**3.4** In `cards.renamed_drawn`, draw the block of Decision 7, with no section. In `tests/py/test_proposal_card.py`, replace `test_a_kits_rename_is_a_block_of_its_own_naming_what_it_renames_and_the_card_a_plain_approval` with `test_a_rename_is_a_block_naming_both_names_and_no_bolt`: two renames proposed over a plan holding neither repository's work, two blocks, no section in the picture, a plain approval.

**4.1** In `tests/contract/test_recfix.py`, replace `test_a_rename_is_one_commit_whose_plan_passes_recfix_and_its_entry_names_both_names` with `test_a_rename_is_one_commit_whose_files_pass_recfix_and_its_entry_names_both_names`. Its fixture holds:
- madswan's plan with no bolt in `tailrace` and a unit whose Source names `agentplot/tailrace:docs/adr/0017`;
- `requests.rec` with a landed fix of main in `tailrace`;
- a runs file with a `bolt.land` under `tailrace`;
- a fleet whose spaces keep `agentplot/timber`.

The test checks, through the real git and recfix:
- the rename is one commit holding `plan.rec`, `requests.rec` and the runs file, each passing `recfix --check`;
- its parent holds each as it was;
- the `kit.rename` entry is the commit after, naming both names and `Count: 3`.

**4.2** In `tests/t-journey-plan.sh`, rewrite the rename steps (from line 281):
- the user's `crew kit rename` over a kit whose bolt has landed, its request and landing named by the new name to `recsel` on the branch, while the host's own runs file still names the old one;
- the planner's direct run refused naming `crew plan propose`;
- a proposal holding a rename checked, its card drawing the block, and the user's approval renaming in its one commit, its entry's `From` naming the proposal.

The refusals are logic cases (`tests.12`).

**4.3** In `README.md`, rewrite the rename's paragraph (now "A kit renamed on its host is renamed across the plan…") from Decisions 1 to 8:
- the order around the rename;
- what stands and refuses it;
- what a host keeps;
- what it renames and leaves;
- running it again;
- a partition never renamed.

Also say `kit.rename` in the run-record fields' list as "a repository's records renamed". Write the same in `plugin/skills/crew/SKILL.md`'s sentence and `plugin/bin/crew`'s usage header for `crew kit rename` (`docs.2`). Leave the sentences on reading a former name to `no-reader-maps-a-kits-former-name`.

**4.4** In `plugin/roles/planner.md`:
- the table row becomes "rename a repository once its work is finished";
- the paragraph "**A kit renamed on its host**…" becomes "**A repository renamed on its forge** is removed and added back, its work finished first", saying the order (record 0060), that crew refuses the rename while any of its work stands or a host keeps the old name, naming what stands, and that a partition is never renamed.

Change `tests/t-briefs.sh`'s two pins (line 99 on) to the new phrases (`tests.6`).
