# Design

## Context

This section records what was read on 2026-11-08 at this change's base, `579dd1f4`, so the decisions below rest on it. The proposal's *Why* says what the change is for.

**The base.** The place was cut at `4b813f18` from `bolt/crew-lands-through-the-runners-land-message`. Before anything of this change was written, main landed `bolt/crew-talks-only-to-its-runner` (#23), which built `crew-calls-no-tool-but-its-runner`: the gather, the follower and the views read a bolt's queue and verification from the runner's report and run no sluice. The place held no commit of its own, so it was brought to `579dd1f4` by a fast-forward, and this change is planned against the code as that commit holds it. Path not taken: planning against `4b813f18` and leaving the overlap to a take-main fix at the bolt's landing. That fix would have had to reconcile two rewrites of the same functions, `standing_said`, `submission_rows`, `queue_read` and `landing_standing` among them, which that change kept for this one to remove.

**What crew still runs for a bolt.** `crew-calls-no-tool-but-its-runner`'s design tables every sluice call crew makes and names this unit as the taker of these (its *Context*, "Where crew runs sluice today"):

| Step | What crew runs or reads (`plugin/lib/plan.py` at `579dd1f4`) |
|---|---|
| start | `GIVE_READ` (the kit's policy and `sluice --version`, `kit.sluice_refusal`), `BOLT_CREATE` (`sluice branch create bolt/<b> --from main`), `BOLT_FOUND`, `made_said`, `unstarted_said`, the `branch.bolt/<b>.crew` mark |
| submit | `bolt_submit`, `landing_submitted`, `SUBMIT` (levels the host's copy, cuts `<kit>/places/land-<b>`, readies the pull request, `wt submit main --no-wait --json`), `PULL`, `PULL_MARK`, `LAND_COPIES`, `pull_hold` |
| wait | `WAIT` (`sluice wait <n> --timeout 9m`), the landing's waiter, `landing_ended` |
| read | `LANDED` (which levels the main checkout with `git read-tree -m -u`), `LANDED_MARK`, `QUEUE`, `SUBMISSIONS`, `SUBMISSION_STATUS`, `HISTORY`, `landing_read`, `_landing-read`, `landing_time`; the leftovers kept for it: `landing_standing`, `standing_said`, `submission_rows`, `queue_read`, and `gather.submissions_of`, `status_read`, `sluice_said` |
| close | `BOLT_DELETE` from `land_delete`, `bolt_branch_asked` and a drop's `sweep_on`; the tidy's `sluice_read(main, "overview")` and `sluice release --worktree` of crew's landing places |
| pull request | `PULL` and `PULL_MARK` (`gh pr list`, `gh pr ready`), `pull_hold`, `landing_unheld` |
| fix of main | `crew main fix --send`, a retry of the fix's submission (`main_fix_change`, `runner.send_refusal`, `runner.sent_of`) |

Two signals name defects of this path: `crew bolt submit` named a submission by a number that was not sluice's and read it from another queue (`2026-11-07-agentplot-ops-38152130/01`), and it levelled the host's main checkout with `git read-tree` after a landing (`2026-11-07-agentplot-ops-b785032d/01`). Both go with the path. A third says the retrofit was in no plan (`2026-11-07-chuck-deneb-809395f6/01`); this unit is that plan.

**What the runner takes.** Boomdrive's `bolt/the-runner-lands-on-a-land-message` landed on its main (#53, `8911d44`), with `land-is-the-message-for-a-works-landing` archived into its specs:

- `crew-control-plane`, "A retry, a land, a drop and a priority are acts on the launch they name": a request `Act: land`, `Of: <n>` is given as an act landing `<label>/<n>`, and no other field of it is read. "An act naming no host is given to the runner that holds its launch" holds for a land.
- `work-into-flume`, "A retry, a land, a drop, a priority and a done are Flume's own commands on the launch's place": a land is `flume retry <place> --submission`, whatever the launch's kind. A land of a launch held unlaunched is answered refused and changes nothing of it.
- `work-into-flume`, "A bolt is a launch": a launch of a kind that lands with no stages is taken as any launch, under its lease, while its stream has room, counted against that room within the pass, by one `flume launch`, and the runner asks no tool to make, move or remove a branch. "A bolt is landed on a land": Flume's answer is the act's, its refusal while a place on its branch is live among them.
- `work-into-flume`, "An offer waits for each launch it comes after": an offer whose After names a launch whose place has not read landed is held.
- `work-into-flume`, "Flume's status of each place is carried as Flume gave it" and "A place the listing no longer holds keeps its last status".

**What Flume does with a base place** (agentplot/flume `site/src/content/docs/guides/merge-queue.md`, "Branches that land on branches", and `guides/kinds.mdx`, at `81d57226`; Flume 0.17.0 runs on deneb). A kind that lands with `stages = []` is a base place. Its launch has sluice make its branch from the base and takes no room. Places launched with `--base <its branch>` are cut there and land there. It is submitted only on its caller's `flume retry <place> --submission`, refused while a place on its branch is live, as `sluice submit main --head <branch>` (sluice 0.71.0 or later). Its outcome is read from sluice's record and reaches its recipients; a failed or conflicting submission starts nothing and waits on its caller with sluice's words. A drop is refused while a place on its branch is live. Once landed or dropped it is tidied, and sluice removes its branch, keeping and naming one that holds work main lacks. Flume carries no such kind: a repository, a source on the host or a launch declares one. A source's kind is named `<source>/<name>`, lies in the source's `kinds_dir` as `<name>@<version>/kind.toml`, and runs only once a lock records its hash.

`runner.flume_facts` already reads what a base place's status gives: its phase, `over` and landed `commit`, its submission's entry and state, `submits`, `send_backs`, the verdict and its words, and what it waits on its caller for.

**Rules this design relies on:** `state.3`, `state.4`, `state.5`, `roles.2`, `roles.5`, `roles.6`, `roles.7`, `roles.9`, `read.1`, `read.2`, `code.1`, `code.7`, `code.8`, `code.9`, `code.11`, `plan.1`, `plan.8`, `plan.16` and `plan.19` as record 0056 amends them, `plan.20`, `plan.21`, `teams.24`, `teams.25`, `record.1`, `record.3`, `docs.2`, `docs.6`, `tests.4`, `tests.10`, `tests.11`.

**Pages whose areas this change touches:** `core.md`; `plan.md` (`plan.py`, `gather.py`, `kit.py`); `teams.md` (`plugin/bin/crew`, `source.py`); `record.md` (`record.py`); `briefs.md` (`plugin/roles/`, `plugin/skills/`); `tests.md` (`tests/`); `docs.md` (README, CLAUDE.md, `openspec/`).

**Departures**, each the design agent's to amend after the landing (`docs.7`, as `crew-calls-no-tool-but-its-runner` left its own), no rule page or record being edited here:

- `plan.8`, `plan.16` and `plan.19` carry record 0056's amendments "from the release that carries crew's unit for it". This is that unit: their old text, ops's submission, `crew bolt submit`, `crew bolt land`'s branch delete, the landing worktree, the all-or-none act, the user's words in ops's pane as a word to land and `sluice withdraw`, stops being true at its release (Decisions 1, 4, 5 and 9).
- `plan.9` has crew remove its landing worktrees and its legacy bolt worktrees by sluice's release, then the kit's worktree tool. crew makes no landing worktree now and calls no sluice, so the tidy removes neither and names any it finds (Decision 8).
- `plan.18`'s reading of 2026-10-24 holds a refusal as the bolt's only when it names the bolt's content, and a check the host could not run as a stop. Flume's verdict `failed` carries sluice's words alone, with no mark of a check that never ran, so crew reads every failed verdict as the bolt's (Decision 6). Its "a landing is submitted from a short-lived worktree" goes.
- `plan.20` and `plan.21`: a landing's split is read from no sluice history, and its record from the runner's report (Decisions 6 and 7).
- `teams.25` rules out "a package in the kinds folder before the first crossing"; record 0057 decision 5 has it empty. The bolt kind is its first package (Decision 2).
- `teams.5`'s details and CLAUDE.md's *Tests* say the one `wt submit` an agent runs is a landing's by `crew bolt submit`. No agent runs one now. CLAUDE.md is changed here (Task notes 6.2); the rule's details are the design agent's.
- `openspec/config.yaml`'s tasks rule asks for a last task running `tests/suite --affected`. This stage's brief has each task name the narrowest check that shows it done, and the verify stage runs the repository's whole checks once after every task, so the tasks end without it.
- `state.3` has a kit's main move by "main-level ops's submission of a bolt", and a fix of main "submitted to main through sluice ... by main-level ops or the user on reading the red". Both move by the runner's land on the user's send (Decisions 4 and 5).

## Goals / Non-Goals

**Goals:**

- A bolt is a base place of crew's own kind, launched to the runner at its start, its pieces after it. crew makes, submits, waits on and deletes no bolt branch, and runs no sluice, `wt` or `gh` command for one.
- The user's send of a row on a kit's landings card makes crew post one `land` for that row's bolt or fix of main, once per send and head, read and posted by crew's own act with no agent's hand.
- A landing's outcome, its hold, its stop and its close are read from the runner's report alone, by the first act of crew's that reads the bolt after it.
- Nothing of crew's makes a worktree on a bolt's branch, moves a host's checkout, or lands anything.

**Non-Goals:**

- Flume launching a conflicting bolt's landing fix of its own (agentplot/flume `a-conflicting-base-place-gets-its-fix-launched`); crew's kind naming its landing fix (`crews-bolt-kind-names-its-landing-fix`). Until both, crew's read of a conflict launches the take-main fix as today.
- Reading a piece's or a bolt's end once Flume has tidied its place without the runner carrying it (`crew-reads-each-pieces-end-from-the-runners-report`, after Boomdrive's `the-runner-carries-each-places-end`); record 0062's stopgap readings stay as they stand.
- A card's preview, still brought up through sluice (`a-cards-preview-is-asked-of-the-runner`, after Boomdrive's `the-runner-brings-up-a-preview-its-control-plane-asks-for`).
- Stopping a landing once its `land` is posted: the runner carries no act for it, so a posted land runs to its outcome.
- The host's lock of `crew/bolt@1`, the package on a runner host where crew keeps no main level, and the move of a host's pin to this release (*After deploy*).

## Decisions

### Decision 1: crew runs nothing for a bolt's branch or its landing

Every script and function in the *Context* table goes, with its cases, and so does `crew bolt submit`'s path through `landing_submitted`, `landing_ended`, `landing_close_out`, `landing_not_landed`, `landing_read`, `landing_read_on`, `landing_time` and `landing_split`'s sluice history. The landing's waiter and its `CLAUDE_PID` handling go with them. `crew _landing-read` goes from the command.

These stay, since none runs a tool for a bolt: `pull_of` (a parse of a landing's `Sluice-From` trailer, for the card's link), `CARRIES` and `bolts_carried` (git, a bolt carrying another's work), `BOLT_LIVES` and `BOLT_HOME` (git, where a bolt lives), the forecast's `git merge-tree`, the verification `crew-calls-no-tool-but-its-runner` built, record 0062's `Sluice-From` readings, and every preview call.

A logic case reads `plan.py`, `gather.py`, `kit.py`, `board.py` and `plugin/bin/crew` and finds no `sluice`, `wt submit`, `wt merge` or `gh` command in any of them, but `sluice preview`, `sluice previews` and `sluice release` of a preview. An end-to-end case runs a bolt from its start to its close on the stubs and finds no sluice, `wt` or `gh` call in the stubs' log, and no write to any checkout's `HEAD`, index or refs (Task notes 7.1, 7.2).

`crew bolt submit` is kept as a word, so an agent whose brief predates this release is told the way: run with any arguments, it refuses at once, before it reads anything, saying a bolt lands on the user's send of its row on the kit's landings card, which crew carries to the runner. `crew main fix --send` refuses the same way. Path not taken: removing both from the parser, which would answer an old brief with "unknown command" and no way on.

### Decision 2: a bolt is a base place of crew's kind `crew/bolt@1`

crew ships one package, `plugin/flume/kinds/bolt@1/kind.toml`:

```toml
[kinds.bolt]
version = 1
branch = "bolt"
lands = true
stages = []
```

Its places' branches are `bolt/<bolt>`, which every kit's sluice policy already gates (`[branches."bolt/*"]`) and every view of crew's already reads. A launch names it `crew/bolt`, since Flume takes a source's kind only when the launch names the source.

`source.keep`, which writes the roles file at each follower read and each main-level start, copies the package into crew's kinds folder, `~/.local/share/flume/kinds/crew/bolt@1/kind.toml`, wherever it makes that folder: whole, by a new file renamed over the old, only when the bytes differ, and making nothing else. A version's bytes never change (Flume, "Packages side by side"); a logic case pins them, so a change to the kind is `bolt@2` beside it.

The host locks `crew/bolt@1` (Flume record 0039). Until it does, Flume refuses the bolt's launch naming the lock, the runner answers it refused, and the bolt's row says so in those words (`read.1`).

Paths not taken: a kind in each kit's `.config/flume.toml`, a file of every kit's that crew does not write; a launch's own `--kinds` file, which the runner never passes (boomdrive `crew-control-plane`: "It names no kinds file"); a kind of Flume's own, which Flume carries none of.

### Decision 3: a start launches the bolt's base place, then its pieces

`crew bolt start <bolt>` makes one plan write, `bolt.start`, refused as today for a bolt started already and for no runner (`runner.runnerless`). It reads no host, makes no branch, and reads neither the kit's policy nor the host's sluice version: `main_kit`, the context's `start_checked` remote and version reads, `prepare` and `undo` go from it. It marks the bolt `Path: flume` and appends, in order:

1. The bolt's launch: `Work: bolt/<bolt>`, `Repo` the bolt's, `Kind: crew/bolt`, `Name: <bolt>`, `Base: main`, `Priority` the bolt's place in the plan (`priority_of`), `Intent: <label>/<bolt>`, `Recipient: <label>/ops`, and no `Brief`, since a base place runs no agent.
2. Each unit's and chore's launch as `runner.reach` makes it today, on `Base: bolt/<bolt>`, after the bolt's launch in the file and naming no After on it.

A piece's launch names no After on the bolt's: the runner holds an offer until each launch it comes after reads landed, and a base place lands only after every place on its branch. The runner takes a pull's launches in the control plane's order and counts the bolt against its stream's room within the pass ("A bolt counts against its stream's room within its pass"), so the bolt is launched before any piece on its branch. Path not taken: an After on the bolt's launch, which would hold every piece until the bolt landed, and so for ever.

`ops` is the recipient because what follows a landing, a failed check's fix or a stop, is ops's (`plan.16`).

`runner.REQUESTS` changes to take it: `Kind` becomes `%type: Kind regexp #^(change|chore|fix|crew/bolt)$#`, since recutils' `enum` takes no `/` and its `regexp` ends at the next occurrence of its delimiter, escaped or not; `WORK` takes `bolt/<bolt>`; `request_refusal` takes a launch of `bolt/<bolt>` only with `Kind: crew/bolt`, `Base: main` and no `Brief` or `After`. It holds no rule of the base place's order: `requests.rec` is only appended to, so a piece appended first in a start's own write could not be told from a fix on a bolt started before this release (Decision 9), whose fixes, a take-main fix among them, are still launched on its branch. The start's order is its own decision's (`runner.bolt_launch`), proven by its cases. Path not taken: refusing a launch on `bolt/<bolt>` that follows no launch of the bolt or of other work on that branch, which tells the two apart only by what the file held before and would have every logic case that models a started bolt's pieces carry a base place's launch it does not read. `ACTS["launch"]` makes `Brief` optional for a bolt's launch alone. The descriptor reaches each branch's `requests.rec` by `in_step`, as today.

**A launch the runner refused.** A bolt whose own launch the runner answered refused, as for a lock missing, stays started with nothing made, and its row says the runner's words. `crew bolt start` run again on it is the way on: one write appends a drop of each of its pieces' launches not yet launched, then a launch anew of the bolt and of those pieces, as above (`runner.restart`). A start of any other started bolt is refused as today. Path not taken: crew launching it again on its own read, which would loop on a refusal nothing has mended.

### Decision 4: the user's send posts one `land` for each row

`runner.REQUESTS`' `Act` gains `land`, which `ACTS` gives `Of` and nothing else, and `request_refusal` takes only `Of` a launch of `bolt/<bolt>` or `fix/main/<kit>/<name>` of the same work. The name is record 0056 decision 6's: `land`, for a bolt and a fix of main alike, and the retry naming the submission goes.

**Where it is posted.** crew already reads the user's send in its own act: the raise of a kit's landings card (`land_hand`, `kit_card_state`) records their answer the first time it reads it (`answer_seen`, `card.answer` with `Heads`), and every later raise reads which bolts that send still lands (`landings_sent`, `rows_unsent`, `sent_left`). That raise now posts the lands, in the same command, by one plan write on the drive's branch: one `land` for each row the send lands, in the card's order, a fix of main first as ops sends it today, its `Of` the row's launch. The raise runs in the follower, in a card's read and at every act that raises the card, on whatever host reads the card first, so nothing waits on an agent's session (`roles.6`, `teams.24`).

**Which rows are due.** `runner.lands_due(rows, sent, requests, reads)` decides it on plain facts (`code.7`): a row is due when its box is ticked on a send that stands for it (`send_stands`), it can land, and no `land` of its launch was posted at its head now nor stands undecided. So a send that stands through a take-main fix lands the bolt again once it reads proven at its new head, with nothing asked (record 0031 as amended 2026-10-24), and a send read twice posts once.

**What is recorded.** The lands are posted in main-level ops's name, the card's owner, as the raise's other acts on the card are. The write's act is `bolt.submit` on `bolt/<bolt>` for a bolt's row and `fix.merge` on `fix/main/<kit>/<name>` for a fix of main's, one entry per row, each naming the card whose send it carries (`Card`), the head the send ticked (`Head`) and the request's number (`Request`, a field the run record's descriptor gains), with `Outcome: asked`. crew names it a request, never a submission: a submission's number is only the entry Flume's status names, which retires signal `38152130/01`.

**The ticks are the word, in the card's order.** A note on the send moves no row and holds none. It reaches ops as the card's answer does today, and a defect it names is a fix ops starts on the bolt, which lands on the bolt after the land if the land is already carried. The card's words say so beside the boxes. Path not taken: holding a send that carries a note until ops reads it, which would have ops decide the landing.

**No other word lands.** The user's words in ops's pane are no word to land: record 0056 decision 5 has main-level ops ask for nothing at a landing. Ops answers such words by telling the user that their send on the kit's landings card lands it. `crew bolt leave`, which records the user's words stopping a landing, stays as it is: before a land is posted it leaves the row unticked, and once one is posted it records the words and says the land runs to its outcome. Path not taken: keeping `crew bolt submit --excerpt` to post a land on the pane's words, which would have ops ask for the landing.

**Rows that are never due.** A row is due no land while it cannot land: a batch waiting on the user (review-batches), a fix in flight, another bolt's work carried, a conflict forecast, or Decision 9's bolt. The rail's land row carries no tell to ops and names no command: it says the row lands on the user's send of `land/<kit>`.

### Decision 5: a fix of main is landed by the same send

A fix of main's row on its kit's landings card is ticked and sent as a bolt's is. Its due land (Decision 4) is `Of` the fix's launch, which holds its submission (`Hold: submission`), and the runner carries it out as `flume retry <place> --submission`. `runner.send_refusal` and `runner.sent_of` become the fix's half of `lands_due`, read from `land` requests; the newest land not answered refused stands, so no send is made twice. The fix's row leaves once its place reads landed, as today.

### Decision 6: a landing's outcome is read from the runner's report

`runner.landing_of(launch, lands, reads)` is a decision of plain facts (`code.7`). Its inputs are the bolt's launch, the lands of it in `requests.rec`, and the partition's runners as crew read them. It reads the base place by `flume_facts` from the runner that took the launch:

| What the runner reports | Outcome |
|---|---|
| the bolt's launch unanswered, held or refused | **unlaunched**, with the runner's words |
| no land stands | **none** |
| the newest land unanswered | **asked**, with its request |
| the runner answered the land refused | **stopped**, in the runner's words, as when a place on the branch is live |
| a submission entry waiting or under test | **submitted**, with the entry's number and state |
| the place over, landed, with its commit | **landed**, with the commit |
| the verdict failed, waiting on its caller | **refused**, the bolt's, with Flume's words |
| the verdict conflict | **refused**, a conflict, with the files and main's revision Flume's words name |
| the verdict withdrawn or refused, waiting on its caller | **stopped**, with Flume's words |
| Flume could not read the submission, or the runner's branch can't be read | **unknown**, naming why; nothing recorded |
| the place over, dropped | **dropped** |

The first act of crew's that reads the bolt once its outcome is decided records it (`plan.21`): the raise of its kit's card, the rail's sweep in the host's follower, a kit's read, or `crew bolt land`. `crew bolts` is a view and writes nothing (`state.4`); it says the outcome as read. The record is a plan write of its own in ops's name (`landing_record`), deciding at the tip it is applied to whether the run record holds the outcome already (`landing_entry` over `w.entries()`), so two reads at once record once; `crew bolt land` records it in its close's commit where no read has. It writes one `bolt.submit` entry with the outcome, the head, the merge queue's entry as `Submission` where Flume names one, and the words for a refusal or a stop. A write replayed on a tip that already holds the outcome writes nothing, and a close another read made meanwhile is no refusal of this one's (`closed_already`). The rail hands a host's sweep only the bolts whose landing the runner reports decided, so an idle sweep reads nothing (`plan.12`), and its read raises a kit's card whose answer its sweep recorded, so the send's lands are posted by the follower too. Path not taken: recording in every plan write that reads a bolt's landing, which would leave the ask of ops to a read that then finds it recorded. The runners' branches are in the partition's state repository, so any host reads the outcome with no ssh to the kit's host (`read.5`).

Flume delivers the same end to `<label>/ops`. crew rests nothing on that notice: its own read records it whether ops is up or not (`roles.6`). A refused or stopped landing is also an ask of ops's run, keyed by the land's request and carrying Flume's or the runner's words, as `unlanded_ask` asks today, so ops starts the fix or records the stop.

An outcome crew can't tell holds nothing: the row, the rail line and the head line say it can't be told and why, and no second land is posted at that head (`read.1`).

**Departs from `plan.18`'s reading of 2026-10-24**, as the *Context* says: a failed verdict is the bolt's.

### Decision 7: what each outcome does

- **Landed:** the read closes the bolt by `bolt_land`'s own code, in ops's name: `bolt.land` with `Head` Flume's commit, the bolt and its pieces out of the plan, and its kit's landings card closed naming the commit and the fleet's timer. It deletes no branch and removes no worktree: Flume tidies the base place and sluice ends `bolt/<bolt>`. The entry's `Age` and `Split` are those the views' `bolt_time` gives from the run record, since no sluice history is read (`plan.20`): from the bolt's newest `bolt.start`, or an older crew's `bolt.give`, to the `bolt.land` entry's own time. `crew bolt land` on a started bolt that has not read landed is refused, recording nothing and naming the landing's outcome; on a bolt never started it closes as today, on the user's word, nothing merged.
- **Asked or submitted:** no unit, chore or fix joins the bolt until its outcome is read (`landing_hold`, as today).
- **Refused, failed:** the row is held with no box, in Flume's words, waiting for a fix on the bolt that ops starts with those words (`crew fix <bolt> <name> "<Flume's words>"`). Once the fix lands on the bolt and the bolt reads proven, the send that ticked it stands only where the bolt's own work is unchanged (rail-cards).
- **Refused, conflict:** the read appends the take-main fix on the bolt, `runner.take_main`, with Flume's words and main's revision, once however often it is read, and the row says it takes main first. Once the fix lands and the bolt reads proven at its new head, the send still stands, so the next raise posts a land again (Decision 4).
- **Stopped:** the row keeps its box with the runner's or Flume's words, and the send that ticked it is spent: a land is posted again only on a new send. The answered card closes naming the bolt stopped, and the card that follows asks for it again with its box. Ops records a signal and tells the planner, as *After landing* says. Path not taken: posting again on the same send, which would loop on a stop nothing of the bolt's caused and nothing has cleared.
- **Unlaunched:** the row has no box and says the runner's words, and `crew bolt start` again is the way on (Decision 3).

### Decision 8: crew deletes no bolt branch and removes no landing worktree

A landed bolt's branch goes by Flume's tidy and sluice's close. A drop of a started bolt appends, in the drop's commit, a drop of each piece's launch still standing (`runner.reach`, as today), then a drop of the bolt's launch. Flume refuses the base place's drop while a place on its branch is live. Where the runner answered the bolt's drop refused, the next plan write that finds the bolt gone from the plan, its launch standing and no piece of it live asks the drop again, once for each refusal (`runner.base_drop_due`). A dropped bolt's branch that holds work main lacks is kept by sluice and named in Flume's answer, which the runner carries; it is the user's to keep or delete (record 0003), and crew asks nothing for it.

These go: `BOLT_DELETE`, `land_delete`, `bolt_branch_asked`, `bolt_branch_over`, the `branch.bolt/<bolt>.crew` marks and `unmark_gone`, the drop's `sweep_on` of the branch, and the tidy's sluice overview and `sluice release --worktree`. The tidy removes no `<kit>/places/land-<bolt>` and no `<kit>/bolts/<bolt>` now: one it finds is named in its output, with the commands that remove it, `sluice release --worktree <path>` then `wt remove`, as the user's to run. Path not taken: keeping sluice's release for them, which would keep crew calling sluice against record 0056 point 1 for worktrees no landing makes any more.

### Decision 9: a bolt started before this release lands under the crew that started it

A started bolt with no launch of `bolt/<bolt>` in `requests.rec` had its branch made by sluice and has no base place, and Flume refuses to open one over a branch already present. Under this crew its row has no box and says it was started before bolts were base places and lands under the crew that started it, and so do `crew bolts` and the ops band. No land is posted for it. A drop of it drops its pieces' launches and asks nothing for its branch, which stays, named, the user's.

The user moves a host's pin to this release once `crew bolts` names no such bolt in the partitions whose main level runs there (*After deploy*). Path not taken: keeping the sluice path for such bolts, a mechanism record 0056 removes, with no move named to retire it (`roles.5`).

### Decision 10: what the views say of a landing

- **Head line:** a bolt's landing says its outcome from `landing_of` with the run record: `landing asked, request 57`; `landing #412 under test`; `landed at <commit>`; refused or stopped in its words; and for a bolt of Decision 9, that it lands under the crew that started it. `phase_said` reads `bolt.submit` entries as they are now written, `asked` among them, and the entries older crews wrote as before (`record.4`).
- **The landings card and the rail:** a row's box, its hold and its words follow `landing_of` and Decision 7. `crew card read land/<kit>` prints the bolts the send lands and the lands crew posted for them, with their requests, and no command for ops to run.
- **The bands:** `board.agent_views`' ops view lists each landing asked or in flight with its request or entry, from the same reads, and keeps the keys `status.js` reads; the mod's cases follow its words (`code.8`).
- **Words that named ops as the lander** say the runner: an answered card's line and the sweep's "waits on the runner to land them" (`answered_waits`), a held bolt's line "crew asks the runner to land it on that send" (`stand_said`), and ops's band "crew asks the runner to land what the user ticked" where it said the landing is ops's.

### Decision 11: the words

- `plugin/roles/main-ops.md`, *Landing a bolt*: the word to land is the user's send on the kit's landings card, and crew carries it to the runner; ops runs no landing, submits nothing and closes nothing by hand. What stays ops's: a fix for a failed check with Flume's words, a signal and a line to the planner for a stop, answering the user's words in its pane by pointing to the card, and `crew bolt leave`. *After landing*: a fix of main's row is sent on the same card, with nothing for ops to run.
- `plugin/roles/planner.md` and `operator.md`, wherever they name ops's submission or `crew bolt submit`.
- `plugin/bin/crew`'s usage: `crew bolt submit`'s and `crew main fix --send`'s lines say they refuse and name the way; `crew bolt start`'s line says it launches the bolt's base place. README's and `plugin/skills/crew/SKILL.md`'s landing and start sections say the same (`docs.2`).
- CLAUDE.md, *Tests* and *Proving and landing a bolt*: a bolt lands on the user's send through the runner; no agent runs `crew bolt submit` or any `wt submit`.

## Risks / Trade-offs

- **[A runner host where crew keeps no main level has no package for `crew/bolt@1`.]** → `source.keep` writes it where crew's follower or a main level runs. On deneb the runner and the main levels share the host. A host whose runner takes a kit's work and keeps no main level of crew's needs the package and its lock by its configuration, which is named under *After deploy* and refused in Flume's words until then (Decision 2).
- **[Two runners keep one repository and take a bolt and its piece apart.]** → The piece would be cut from the bolt's branch on GitHub by a Flume that holds no base place of it, and the base place could be submitted while that piece is live elsewhere. Today's pieces carry the same risk across hosts, and every partition's kits are kept by one runner now. The runner's claim is Boomdrive's to hold together.
- **[A landing posted cannot be stopped.]** → The runner carries no withdrawal (*Non-Goals*). `crew bolt leave` stops a bolt before its send is carried.
- **[Flume tidies the base place before the runner carries its landing.]** → The runner keeps a tidied place's last status and asks Flume for it by its location ("A place the listing no longer holds keeps its last status"), and Flume's status of a tidied place keeps its landed commit. Where neither carries it, the bolt reads asked or submitted until Boomdrive's `the-runner-carries-each-places-end` ships, and is never read landed wrongly (`read.1`).
- **[A bolt's time loses its gate minutes.]** → The views already place none (`crew-calls-no-tool-but-its-runner`, Decision 5); the landing's entry now matches them.

## Migration Plan

Nothing in a file crew writes changes shape but two additions: `requests.rec`'s descriptor (`Kind` a regexp, `land` among the acts), which `in_step` brings each branch to at its next write, and the run record's `Request` field, which an older crew's descriptor lacks and reads past. A bolt started under an older crew is Decision 9's. A `bolt.submit` entry an older crew wrote is read as it was.

## After deploy

- **Lock `crew/bolt@1` on each runner host before this release reaches it** (Flume record 0039). The doer is the host's configuration, swancloud's or Boomdrive's flake's, by `flume kinds lock --host crew/bolt@1` at the package's hash, in every environment whose runner takes crew's partitions' work. It is no check of crew's, since the lock is the host's file. Until it is there, every bolt start answers refused naming the lock.
- **Put the package on a runner host where crew keeps no main level.** The same doer, from crew's release. There is no such host today.
- **Move a host's crew pin to this release only once `crew bolts` names no bolt started before it** (Decision 9), and only once the host's runner takes `land` (Boomdrive's `the-runner-lands-on-a-land-message`, `8911d44`, released). The doer is the user, on swancloud's pin, since it is their bump; nothing in crew can see a host's pin.

## Task notes

**1.1** `plugin/flume/kinds/bolt@1/kind.toml` holds exactly the four keys of Decision 2, with a comment line above them naming record 0056 and Decision 2. `plugin/lib/source.py` gains `KIND_PACKAGES`, the package's path in crew's plugin and its path under `KINDS_DIR`. `keep(fleet, host, asks, roles=None, kinds=None, packages=None)` writes each package where it makes the kinds folder: read, compared with the bytes at the destination, written to `<dest>.<pid>.tmp` and renamed over only when they differ. With no entry it writes none, as it makes no folder. Its docstring and the module's say so. Cases in `tests/py/test_source.py`: the package written once with an entry; not written again with the same bytes (its mtime kept); written over when the bytes differ; not written with no entry; the package's bytes pinned to a literal in the test, so a change to them fails it. `tests/t-flume-source.sh` checks the package lands in the scratch HOME's kinds folder at a main-level start; its `# Reads:` line gains `plugin/flume/kinds/`, and `tests/moon-tasks` is run and `tests/moon.yml` committed (`tests.10`).

**2.1** In `plugin/lib/runner.py`: `REQUESTS`' `%doc` and comment name a bolt's base place and a land; `%type: Kind regexp #^(change|chore|fix|crew/bolt)$#`; `%type: Act enum launch retry drop priority land`. `WORK` takes `bolt/N`. `ACTS["land"] = (("Of",), ())`, and a launch's `Brief` is required unless its work is `bolt/`. `request_refusal`:

- a launch of `bolt/<b>` names `Kind: crew/bolt`, `Base: main`, no `Brief` and no `After`, else refused naming the field;
- any other launch names no `Kind: crew/bolt`;
- a land's `Of` names a launch of `bolt/` or `fix/main/` work, the land's `Work` the same.

`flume_facts` needs nothing new; add a fixture pair of a base place's status to `tests/py/flume-0.17.0/` (submitted under test, landed with its commit, failed, conflict with files, withdrawn), written from Flume 0.17.0's `crates/flume-core/src/status.rs` shapes as `tests/py/flume-0.17.0/README` says its others are, and read them in `tests/py/test_runner.py`. Cases in `tests/py/test_runner.py`, class `TestBoltRequests`: each refusal above, a land accepted, the descriptor passing `recfix --check` with a `crew/bolt` launch and a land (`tests/contract/test_recfix.py`, one case).

**3.1** `op_bolt_start` in `plugin/lib/plan.py` loses `main_kit`, the two contexts' `start_checked` reads (near 6062 and 6134), `prepare`, `undo`, `MADE_BRANCH`, `started_said`'s branch words and `made_said`. Its `change` appends the bolt's launch (`runner.bolt_launch(plan, bolt, label)`, a new decision returning `("launch", "bolt/<b>", fields)`) and then `reach_places` as today. `after` prints that the bolt's base place and its N pieces were asked of the runner, with their requests. These go with their cases: `GIVE_READ`, `BOLT_CREATE`, `BOLT_FOUND`, `made_said`, `unstarted_said`, `kit.sluice_refusal`, `kit.branch_said`, `kit.bolt_found`, the start's `branch.bolt/<b>.crew` mark. `runner.restart(plan, requests, reads, bolt, label)` gives Decision 3's drops and launches for a bolt whose own launch the runner refused, and `op_bolt_start` uses it instead of refusing such a bolt. Cases: `tests/py/test_runner.py` `TestBoltLaunch` (the launch's fields; the pieces after it, naming no After on it; priority; restart after a refusal; no restart for a launch held or launched) and `tests/py/test_made.py`, whose sluice cases go and whose start cases read the requests appended. `tests/py/test_bolt_commands.py`'s start cases follow, `TestStart` gaining one where the main-level host keeps no checkout of the kit and the start goes on; and `TestBoltRequests` one where a fix is launched on a bolt with no launch of `bolt/<b>` (Decision 9).

**3.2** `runner.stage_of` reads `bolt/<b>` as a piece of its own for the bolt's own row: `unlaunched` with the runner's words while its launch is unanswered, held or refused. `plan.Stages` gives each started bolt its base place's facts beside its pieces, and a started bolt with no launch of `bolt/<b>` reads Decision 9's words (`runner.legacy_said`). Cases in `tests/py/test_stages.py`.

**4.1** `runner.lands_due(rows, sent, requests, reads)`: rows as `landing_rows` gives them, a fix of main's among them; sent, `{row's work: the head the send ticked}` from `landings_sent` and the card's answer; it returns `[(work, Of)]` in the card's order, fixes of main first, each whose send stands at its head now, which can land, and whose launch has no land posted at that head nor one standing undecided (`landing_of`'s asked or submitted). Cases in `tests/py/test_landings.py`, class `TestLandsDue`: a send read twice posts once; two rows in the card's order; a fix of main first; a row taking main first posts nothing, then posts once at its new head; a stopped row posts nothing on the same send; a Decision 9 bolt posts nothing; a bolt carrying another bolt's work posts nothing; a row whose units wait on a batch the user has not answered posts nothing, whatever send stands; an outcome crew can't tell posts nothing again at that head.

**4.2** The raise of a kit's landings card (`land_hand` and the function that runs its `landings_step`) posts the due lands by one plan write after `answer_seen` and before it acts on the card: `request(w, "land", work, Of=n)` for each, the write's subject `plan(<kit>): land <rows> on the user's send`, one `bolt.submit` or `fix.merge` entry per row with `Card`, `Head`, `Request` and `Outcome: asked`. `record.DESCRIPTOR`'s `%allowed` gains `Request`, and its field comment says what it holds. The card's close and its follow say "asked of the runner" where they said "landing as you ticked". `crew card read land/<kit>` prints the lands posted for the send with their requests and no command. The rail's land row (near `plan.py` 11671) carries no `crew tell <label>-ops "Land …"` and says the row lands on the user's send of `land/<kit>`; the words Decision 10 lists follow. Cases: `tests/py/test_landings.py` (the write's requests and entries, the replay that writes nothing), `tests/py/test_card_commands.py` (what `card read` prints), `tests/py/test_record.py` (the descriptor). End to end, `tests/t-journey-land.sh`: the stub Pending You answers the landings card with two rows ticked; the next raise appends two lands in order to `requests.rec` on the stub state branch, and a second raise appends none.

**4.3** `bolt_submit` and its parser entry become a refusal before any read: "crew bolt submit lands nothing: a bolt lands on the user's send of its row on its kit's landings card, which crew carries to the runner as a land" (code.11 still answers `--help`). `crew main fix --send` and `--excerpt` refuse the same way, before any read. `main_fix_change`'s send branch, `runner.send_refusal` and `runner.sent_of` go into `lands_due` (Decision 5). Cases: `tests/py/test_main_fix.py`, `tests/py/test_send.py`, `tests/py/test_bolt_commands.py`; `tests/t-help.sh` keeps both commands' `--help`; `tests/t-journey-main-fix.sh` sends the fix's row on the stub card and finds a land of its launch in `requests.rec`.

**5.1** `runner.landing_of(launch, lands, reads)` as Decision 6's table, each fact guarded (`read.2`). Cases in `tests/py/test_runner.py`, class `TestLandingOf`, one per row of the table, on the fixtures of 2.1.

**5.2** The first read after a decided outcome records it and acts as Decision 7: `landing_recorded`, `landing_phase`, `landing_pending`, `landing_hold`, `refusals`, `stops`, `sent_back` and `take_main_launch` read `landing_of` instead of sluice's record; a landed outcome calls `bolt_land(..., by=ops)` with Flume's commit; `bolt_land` no longer reads a queued landing on a host (`landing_read_on`) and no longer runs `landing_time`, recording `Age` and `Split` from `bolt_time` over the run record, and refuses a started bolt not read landed (Decision 7); a refused or stopped outcome writes ops's ask (`unlanded_ask`) keyed by the land's request; a stopped bolt counts as no longer landing on the send that ticked it (`landings_step` near 3220), so the answered card closes naming it and the card that follows asks again. Then delete the *Context* table's submit, wait and read rows, their scripts, `crew _landing-read`, the landing's waiter, and the leftovers `crew-calls-no-tool-but-its-runner` kept for them: `landing_standing`, `standing_said`, `submission_rows`, `queue_read`, `gather.submissions_of`, `status_read`, `sluice_said`. Cases: `tests/py/test_landing.py`, `tests/py/test_landing_state.py`, `tests/py/test_landings.py`, `tests/py/test_bolt_submissions.py` (its sluice-parsing cases go), `tests/py/test_pane_landing.py` (its submit-on-words cases go; its close-on-words cases follow 4.3), `tests/py/test_rail.py`, and `tests/py/test_bolt_commands.py` `TestLand` (a close by hand before the bolt read landed is refused, recording nothing). A case in `tests/py/test_landings.py` reads a landing's outcome as a host away from the kit's would, with every ssh refused, and records it. The fixtures `tests/py/sluice-0.18.0/`, `sluice-0.36.4/` and `sluice-0.51.3/` go once no case reads them. The stub `sluice` loses each of `overview`, `wait`, `status`, `inbox`, `branch` and `submit` that no test still calls once crew calls none (`grep -n` over `tests/`), keeping `preview`, `previews` and `release` of a preview; `tests/stubs/wt-submit` and `tests/stubs/gh` go once no test reads them.

**5.3** `tests/t-journey-land.sh` runs a bolt from its start to its close: start (the base place's launch and its unit's in `requests.rec`); the stub runner's branch carries the unit merged and the base place live; the bolt reads proven and its row can land; the stub card is answered; the raise posts the land; the runner's branch carries the base place submitted, then landed at a commit; the next raise records `bolt.submit` landed and `bolt.land` at that commit, the bolt leaves the plan and its card closes naming the commit. A second bolt's base place carries a conflict verdict: its take-main fix's launch is appended once, and after the fix merges and the bolt reads proven the raise posts a second land on the standing send. A third carries `failed`: its row is held in Flume's words. Its `# Reads:` line follows, and `tests/moon-tasks` is run.

**6.1** `runner.base_drop_due` and `op_bolt_drop`: Decision 8's drops, the bolt's last; the drop's `after` no longer calls `sweep_on` for the branch. `tidy` keeps no sluice read: `sluice_read(main, "overview")`, `release_kept`'s sluice release, `land_delete`, `bolt_branch_asked`, `bolt_branch_over`, `unmark_gone` and the marks go, and a `places/land-<b>` or `bolts/<b>` it finds is named with the commands of Decision 8. Cases: `tests/py/test_tidy.py`, `tests/py/test_runner.py` `TestBaseDrop` (a drop's requests in order; a refused bolt drop asked again once no piece is live, once per refusal).

**7.1** `tests/py/test_no_tool_for_a_bolt.py`: reads each of `plugin/lib/plan.py`, `gather.py`, `kit.py`, `board.py`, `runner.py` and `plugin/bin/crew` and, in every string the code runs as a command (a script constant, or an argument list handed to `subprocess`, `crew.on_machine` or `host_run`), never in a docstring or a comment, finds no `sluice` command, `wt submit`, `wt merge`, `wt remove`, `gh ` or `read-tree` outside the preview functions, each a `def` whose name holds `preview` (`previews_of`, `preview_release`, `head_previewed`, `landing_preview` and the rest), and the scripts only they run, which the case names one by one so a new caller of sluice fails it.

**7.2** `tests/t-journey-land.sh` (5.3's run) ends by reading `$CREW_TEST_LOG` and finding no `sluice`, `wt` or `gh` call, and by finding each scratch kit's `HEAD`, index and `refs/` unchanged from before the start but `refs/remotes/`.

**8.1** The mod: `board.agent_views`' ops view gives each landing asked or in flight with its request or entry and words, under the keys it has; `plugin/tests/status.test.ts` draws `landing asked, request 57` and `landing #412 under test` lines; `tests/py/test_board.py` pins the keys (`code.8`).

**9.1** The words of Decision 11. `tests/t-briefs.sh` checks main-ops's brief names the landings card's send as the one word and names no `crew bolt submit`, `wt submit` or `sluice withdraw`; `tests/t-docs.sh` checks the usage and README agree (`docs.2`).
