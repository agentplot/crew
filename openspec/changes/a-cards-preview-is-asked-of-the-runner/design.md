# Design

## Context

**The ruling.** Record 0056, rewritten and accepted by the user on 2026-11-08, point 1: "crew is the control plane, and talks only to Boomdrive's runner. crew never calls Flume or sluice, reads neither one's records or files, and names neither in what it decides. It posts messages the runner pulls, and it reads the runner's report." Its consequence on previews, agentplot-design's choice that day:
- what the user sees on a card stays: a row or a batch line says it has a preview, the preview comes up when the user asks on the card, the card lists its addresses while it is up, and it goes when they are done or the row ends;
- crew posts `preview`, naming the repository, the branch and the revision, and the same message marked `done` to put it away;
- a runner that keeps the repository, on the host where the work runs, carries it out through sluice's own preview command, once, and reports sluice's answer as sluice gave it;
- crew reads whether a kit has a preview, and each preview's addresses, from the runner's report alone. Where the report cannot yet say whether a kit declares one, the row offers it, and a kit that declares none answers in sluice's words;
- crew puts away only previews it asked for, and the runner only what its control plane asked it to bring up.

**Boomdrive's half, landed.** agentplot/boomdrive `the-runner-brings-up-a-preview-its-control-plane-asks-for`, on its main at 5e9c753, tagged v0.6.0, read on 2026-11-08:
- `crates/boomdrive-crew/src/read.rs` `want`: `Act: preview` gives a preview of its `Branch` at its `Revision`, its repository its `Repo` resolved as a launch's is, done where `Done` reads `yes`, `true` or `1`. One missing `Branch` or `Revision` is refused with words naming the field.
- A preview naming no `Host` is given nothing (crew-control-plane spec, "A preview naming no host is given nothing"), since two runners keeping its repository would each bring it up.
- The runner runs `sluice preview <branch> <revision> --json` with a patience of twenty seconds, answering `held` at sluice's bound and asking again each pass. It reads `sluice previews --json` once a pass for each repository with a preview held or done. It carries of sluice's answer and listing only `name`, `branch`, `revision`, `state`, `made` and `addresses`, never the preview command's output (previews spec).
- A done puts away each preview of its report, not marked done, of the done's repository and revision, by `sluice release <name> --json`. A done with nothing to put away is refused, `no preview of <revision> in <repository> was brought up here at the control plane's asking`.
- It writes `previews.rec` on its branch, one `Preview` per preview request answered, under `crates/boomdrive-crew/src/write.rs` `PREVIEWS`, "this change's proposal of crew's", which crew's unit is to hold "in `runner.py` byte for byte".
- Its tests' copy of crew's `requests.rec` descriptor (`crates/boomdrive-crew/tests/common/mod.rs`) has `%type: Act enum launch retry land drop priority preview`, `%type: Done bool`, and `Branch Revision Done` after `Base` in `%allowed`, and its `FIELDS` the same.
- A runner of a release before it refuses `Act: preview` in `answers.rec`: `its Act preview, which crew's implementation does not read` (`read.rs`, `Some(other)`).
- Its `Main::plans` reads `unit/<u>`, `chore/<c>` and `fix/<bolt>/<n>` as leaving crew's plan, and any other work as never leaving it.

**Where crew touches sluice for a preview today**, read by grep of `plugin/` on 2026-11-08:
- `plan.py` `preview_handed` runs `sluice preview <branch> <revision> --wait --json`, handed to a process of its own by `preview_hand` as `crew _preview`.
- `previews_of` reads `sluice previews`; `preview_released` runs `sluice release`, both through `sluice_read`.
- `head_previewed` reads `.config/sluice.toml` at the bolt's head with git, judged by `kit.previewed`.
- crew keeps a record of each preview under `~/.local/state/crew/previews/<label>/<key>/<thing>.json` on the work's host, and an older crew's at `<label>/<bolt>.json`.
- `crew card preview` forwards to the main machine, then `crew _card-preview` to the work's host. A batch card's close hands `crew _preview-release` to each host. Each host's `crew card sweep` releases the previews whose card is dead.
- deneb holds no such record (`~/.local/state/crew/previews` read on 2026-11-08, no `.json` file under it). The box was not read.

**Area pages this change touches:**
- `core.md`: `roles.1`, `roles.5`, `roles.9`, `state.1`, `state.4`, `state.5`, `read.1`, `read.2`, `code.3`, `code.7`, `code.8`, `code.9`.
- `plan.md`: `plan.1`, `plan.2`, `plan.12`, for `plan.py`'s writes.
- `teams.md`: `plugin/bin/crew`'s internal commands and usage.
- `record.md`: `record.1`, `record.3`, for `card.preview`.
- `briefs.md`: the two briefs' words, and `briefs.13`, no card asks the user to run a command.
- `tests.md`: `tests.4`, `tests.6`, `tests.10`, `tests.11`.
- `docs.md`: `docs.2`, `docs.7`.

No rule page is edited (`docs.7`). The design departs from no rule.

## Goals / Non-Goals

**Goals:**
- Every preview a card carries is asked of the runner by a request on the drive's branch, put away by its done, and read from the runner's report.
- crew runs no `sluice` command and reads no file of sluice's for a preview, `.config/sluice.toml` among them.
- What the user sees and does on a card is as today: what brings a preview up on each row or line, the user's words to bring it up and put it away, its addresses while it is up, and its going with its row or card.

**Non-Goals:**
- crew's other calls to sluice that record 0056 names: a landing's reads, gather's, the board's watch of `sluice overview`. Each is its own unit.
- A preview through the hosted protocol, which Boomdrive's later version carries.
- Previews in the views or the agents' bands, which carry none today (`code.8`).

## Decisions

### 1. A preview is a request, named as the runner reads it

- **Its fields.**
  - `Act: preview`, with the `Request`, `Work`, `Date` and `By` every request carries.
  - `Host`: the host whose runner reported the work, as `runner.where` reads it for the bolt (`bolt_at`) or the batch's unit (`batch_unit_at`).
  - `Repo`: the kit as the plan names it, resolved by the runner as a launch's is.
  - `Branch` and `Revision`: what the row or the line names.
  - `Done: yes` to put it away, and no `Done` to bring it up.
  - Nothing else.
- **Its work.** `bolt/<bolt>` for a landings row's bolt, `unit/<unit>` for a batch line. `bolt/<bolt>` is the work of no other request.
- **The descriptor.**
  - `Act`'s enum gains `preview`, last.
  - `%type: Done bool` follows `Submission`'s line.
  - `%allowed` and `FIELDS` gain `Branch Revision Done` after `Base`.
  - `%doc` stays as it is; the comment above the descriptor names a preview.
  - Once the `land` change adds `land` after `retry`, the descriptor is Boomdrive's tests' copy byte for byte. crew's existing branches take it at their next write (`in_step`).
- **Naming a host keeps `roles.9`.** That rule rules out "a launch naming a host or a stream crew chose" and "crew reading a kit's host from anywhere but the runner's report". A preview's `Host` is the runner's own report of where the work runs. crew's rules refuse a preview naming none.
- **Not taken:**
  - No `Host`, the runner that keeps the repository claiming it. Boomdrive gives such a preview nothing, and two runners keeping the repository would each bring it up.
  - A field naming the card's key. The runner's copy of the descriptor takes none. The work already names the card: a bolt's row on its kit's landings card, or a unit's lines on a batch's.

### 2. One preview per host, repository and revision

- sluice keeps one preview of a revision on a host, and the runner's done puts away every preview of its report of that repository and revision. So crew reads an ask by its `(Host, Repo, Revision)`.
- **Standing.** The ask stands while the newest preview request naming those three is a bring-up that the host's runner has not refused (`runner.previews_standing`). A done ends it, and so does the runner's refusal. A bring-up written after a done stands again.
- **Shared by every card.** Every card carrying that revision on that host shows that one preview, and a done from any of them puts it away for all, each changed in place to say so (Decision 8).
  - This departs from today's `shared_by`, which kept sluice's preview while another of crew's records named the revision.
  - It is cheap: a landings row's head and a batch line's revision meet only where a stage recorded the bolt's own head as a made thing, and no Flume place reports made things to crew yet (record 0043).
  - Not taken: a count of cards for each ask, which needs the card's key on the request (Decision 1).

### 3. The runner's answer is read from its branch

- **`previews.rec` is a fifth file.** `runner.PREVIEWS` is Boomdrive's `write.rs` `PREVIEWS` at v0.6.0, byte for byte. `FILES` gains `previews.rec`.
- **`host_read` reads it.**
  - It keys each `Preview` by its request's number: its outcome, `Text` and `Status` parsed as JSON, `Listed`, `Words` and `At`.
  - A file recfix refuses, a record before its `%rec`, or a request missing or twice makes the host's runner unreadable, as the other files do (`read.1`).
  - A `Text` or `Status` that is no JSON marks that preview alone, naming the file.
  - A branch with no `previews.rec` answers no preview.
- **`runner.preview_report(reads, request)`** reads one request from the runner on the host it names, from facts alone (`code.7`):
  - a `Preview` of it: `held`; `done`, its state and addresses from the listing where `Status` is carried, else from sluice's answer in `Text`, `Listed: no` making it `unlisted`; or `refused`, with its `Words`;
  - else a refused `Answer` of it in `answers.rec`: `refused` with its words, as an unreadable request or a runner before v0.6.0 is answered;
  - else `asked`;
  - `unread` with why, where that host's runner can't be read or the preview's JSON can't.
- **Checking sluice's shape.** Each of sluice's fields is read only where it holds what crew reads (`read.2`): `name` text, `state` one of `waiting`, `starting`, `up` or `failed`, `addresses` an object of text. Anything else is `unread`, naming the field.
- **Older runners.** crew writes the request whatever the runner's release. A runner before v0.6.0 refuses it in its own words, which the card shows.
  - Not taken: reading `runner.rec`'s `Version` and refusing before writing. crew would keep a table of runner releases, and the runner's refusal already says it.

### 4. What a card says of a preview

`cards.preview_said` takes one shape per state, and `cards.made_said` the same under a batch line:

| shape | the card says |
|---|---|
| `{branch, head, state: "ask"}`, not asked | as today: write on this card to bring it up, and that you are done to put it away; it is not held while the card waits |
| `{head, host, state: "asked"}` | a preview of `<h>` is asked of the runner on `<host>`, which brings it up at its next pass; nothing waits on it |
| `{head, host, state: "held"}` | a preview of `<h>` waits for room on `<host>`; its runner asks for it again at its next pass; nothing waits on it |
| `{head, name, addresses, state}`, waiting, starting or up | as today, its addresses listed |
| `{head, host, state: "failed"}` | asked for and not there: it did not come up, as sluice on `<host>` lists it; nothing waits on it |
| `{head, host, state: "refused", words}` | asked for and not there: the runner's or sluice's words |
| `{head, host, state: "unlisted"}` | asked for and not there: sluice on `<host>` no longer lists it |
| `{head, why}` | asked for and not there: why crew can't read it |

- `released` still marks a revision put away, "as the head moved" or not.
- The shapes `none` ("No preview.") and `policy` go with the policy's read (Decision 5).
- A failed preview carries no output. The runner carries none (Boomdrive previews spec, "What is carried of a preview holds no output of its command").
- **One word per state.** `runner.preview_word` gives each state one word for the change note and for what the card was told (Decision 8): `ask`, `asked`, `held`, `coming` (waiting or starting), `up`, `failed`, `refused`, `unlisted`, `unread`.
- **The change notes.** `asked_note` says `<thing>: Its preview of <h>` then:
  - is asked of the runner on `<host>`
  - waits for room on `<host>`
  - is coming up
  - is up
  - did not come up
  - could not be brought up
  - is gone
  - is put away

### 5. Every row that can land offers a preview

- crew reads no `.config/sluice.toml` for a preview: `head_previewed` and `kit.previewed` go.
- Each row that can land carries `{branch: "bolt/<bolt>", head, state: "ask"}` until an ask of its head stands.
- A kit that declares none answers in sluice's words when the user asks, as a refusal (Decision 3). This is the record's own reading of "where the report cannot yet say whether a kit declares one".

### 6. `crew card preview` writes the request and answers

**Where it runs.** On the partition's main machine, where the card is, as today, forwarded there when run elsewhere (`code.3`). Nothing is done on the work's host, so `crew _card-preview` goes.

**What it may bring up.**
- **For `land/<kit>`:** a bolt among the card's last recorded rows (`card_heads`), any of them, read afresh through `CardActs.land_row` as the raise reads it. It is refused when that row can't land now, naming why. Its `Revision` is the row's full head.
- **For `batch/<n>`:** a line `<unit>/<name>` with a branch and a revision, as the unit's made lines hold them. They are read through `CardActs.made` from the host its unit was built on (`batch_unit_at`), as the batch's raise reads them.
- **Who may ask.** The owner check stands (`preview_owner`, `preview_caller`). `REQUESTERS` gains `card preview` for `main-ops` and the planner, so the role table names every command that writes a request (`roles.1`).

**What it does.**
- **Bringing it up.** `runner.ask_step(ask, report)` decides:
  - `keep`, where the ask of that revision stands and the runner has neither refused it, nor reported it failed, unlisted or unread. crew prints what the card shows and writes nothing.
  - `ask`, otherwise. crew writes one bring-up.
- **Putting it away.** With `--done`, crew writes the standing ask's done. With no ask standing, it says it asked for no preview of the thing that stands, and writes nothing.

**The write.** One plan write (`state.1`, `plan.1`):
- its commit holds the request alone;
- its subject is `plan(card): preview of <thing> asked from <key>`, or `put away from <key>`;
- its entry's act is `card.preview`, on the work, with the card's key as `Key` and `asked` or `done` as `State` (`record.1`). It holds no words (`record.3`).

It answers once the write is made, printing the request's number and what the card now says (`code.9`). There is no wait for sluice: the runner answers at its next pass, and the rail's read follows it (Decision 8).

**The card.** It is changed in place with the note, through `land_hand` or `batch_hand`, as today.

### 7. The done is written where crew released before

One decision, `runner.previews_put_away(asks, carried, works, now, grace)`, gives the standing asks to put away. An ask is kept when:
- its `(Host, Repo, Revision)` is in `carried`;
- its work is in `works`; or
- its request is under `grace` seconds old at `now`.

Its callers each write their dones in one plan write, act `card.preview`, `State: done`:
- **The raise of a kit's landings card** (`landings_raised`), before the card is built.
  - `asks`: the standing asks of `bolt/<b>` in the kit's repository.
  - `carried`: each row that can land, at its host, the kit and its head.
  - So a row held for a fix, gone, landed or dropped, or at a moved head, has its ask put away.
  - A row whose bolt had an ask at another head put away carries `released`.
- **A batch card's close** (`row_card_close` for `batch/<n>`).
  - `asks`: the standing asks of `unit/<u>` for the batch's units.
  - `works`: the units of each other batch card still open.
- **The rail's read on the partition's main machine** (`sweep_previews`, after `sweep_moved`).
  - `asks`: every standing ask.
  - `works`: `bolt/<b>` for each live `land/<b>`, and `unit/<u>` for each unit of a live `batch/<n>`, from `sweep_judgment`'s live keys. A blind prefix keeps every ask of its kind.
  - `grace`: two minutes, as `preview_dead` gave each host's sweep.
  - It says each preview it put away, beside the sessions it ended.

A write refused is said, and the next raise or rail read tries again. Nothing is put away that crew could not read (`read.1`).

Not taken: leaving every done to the rail's read. A moved head's preview would stand until a read noticed, and the row's word "released as the head moved" needs the done written at the raise that says it.

### 8. A card changes when the runner reports anew

**When.** At each rail read on the partition's main machine (`previews_changed`, after `sweep_previews`), for each card open there, not answered, that carries a standing ask:
- in ops's name under `land/<kit>`, its asks of the bolts of its last rows;
- in the planner's name under `batch/<n>`, its asks of its units.

`preview_word` of the runner's report now is compared with what the card was last told of that request. Where any differs, the card is raised again with one note naming each thing and its word:
- a landings card through `land_hand`, with `landing_act("preview")`;
- a batch's through `batch_hand`.

A card the user answered is left (its raise leaves it). A card posted with no key, an agent's own question, carries no ask and is passed over, so the rail's read never fails on one (`code.2`).

**What the card was told.** It is kept on the main machine in `~/.local/state/crew/cards/<label>/previews.json`: `{key: {request: word}}`, beside the card folders and in none, as `landings_main` keeps a card's main. It is written by every post or change of a card that carries an ask, by `landings_raised`, `raise_batch` and `previews_changed`. It is a cache of what crew read (`state.4`): lost or unreadable, it reads as empty, which costs one more change of each card.

**Not taken:**
- Comparing the runner's `At` with the card's last post or change in the run record. Hosts' clocks differ, and a runner's running ahead of the main machine's would change the card at every read until the clocks met.
- A field of the card's run-record entry for what it showed. The run record's descriptor takes none for it, and an entry holds names, not a card's state.

### 9. What goes

- **`plan.py`'s preview section, `PREVIEWS` to `card_preview_cmd`.** Gone:
  - the host records and their lock;
  - the handed process (`preview_hand`, `preview_awaited`, `preview_handed`, `preview_ended`);
  - the reads and releases of sluice (`previews_of`, `preview_listed`, `preview_released` and those built on them);
  - `preview_row`, `preview_step`, `asked_step`, `shared_by`, `preview_others`, `preview_files`, `preview_row_key`, `previews_card`, `rows_previewed`, `card_preview_here`, `PREVIEW_STATES`, `preview_change`.
- `head_previewed`, `landing_preview`'s policy read, `land_end`'s release, and `land_row`'s release of a held or gone row's preview.
- `CardActs.preview`, `release_preview`, `release_previews` and `preview_up`. `_made`'s `previews`.
- `preview_dead` and the preview part of `card_sweep`.
- `kit.previewed`.
- The internal commands `_preview`, `_preview-release` and `_card-preview`: their parsers, their dispatch and their lines in `plugin/bin/crew`.
- **Kept:**
  - `preview_owner`, `preview_caller` and `preview_target`, the last fed by the card's rows and lines;
  - `asked_note` and `preview_changed`, with Decision 4's words;
  - `dashed`, where other code uses it.
- **A guard against its return.** A logic case reads `plugin/` and finds no `sluice preview`, `sluice previews` or `sluice release` run, and no `[preview]` read of a kit's policy (`roles.3`).

### 10. The briefs and the docs

- Main-level ops's and the planner's briefs keep the user's words and the commands. "crew brings it up through sluice on the host where the bolt's work ran" becomes "crew asks the runner on the host where the work runs to bring it up, and the card is changed in place once the runner reports it".
- Ops's brief opens with "Each row that can land carries what brings its preview up" in place of "A row whose kit's policy names a preview". "or sluice cannot bring it up" becomes "or the card says it could not be brought up".
- `tests/t-briefs.sh` pins the new phrases (`tests.6`).
- README's paragraph on a card's preview, the crew skill's row and the usage header of `crew card preview` say the same, together (`docs.2`).

## Risks / Trade-offs

- **A preview comes up later than today.** It waits for the runner's next pass, a minute by default, and the card changes at the rail's read after the runner's report. Today the ask waits up to twenty seconds for sluice to name the addresses. The card says at once that the preview is asked and of which host's runner, so the user is not left wondering.
- **The rail's read writes.** A dead ask's done is one commit on the drive's branch, written once: the decision finds nothing standing after it. The rail's read already acts this way, raising cards main moved under and recording landings (`sweep_moved`, `reap_judged`).
- **One preview per revision** (Decision 2): a done from one card puts it away for another carrying the same revision on that host, each changed in place to say so.
- **A person's preview of the very revision crew asked for** is put away by crew's done, since sluice keeps one preview of a revision on a host. That is the runner's risk (its design's *Risks*), as crew's own release had it.
- **An unreadable `previews.rec` hides the host's runner** whole, as any of its files does (`read.1`).
- **A landed bolt's previews stay on the runner's branch.** Boomdrive's `Main::plans` never reads `bolt/<b>` as leaving the plan. They cost only bytes (*Follow-ups*).
- **Mixed releases.** A main machine on this crew sends no `_card-preview`. A main machine on an older crew sends one to a work host on this crew, which refuses it as no command and says so on the card. That lasts only between the two hosts' updates.

## Migration Plan

- **Requests.** `requests.rec`'s descriptor reaches each branch at its next write (`in_step`). A request already written is unchanged (`append_refusal`).
- **The runners.** A runner before Boomdrive v0.6.0 refuses a preview in its own words, which the card shows. Runners on v0.6.0 or later bring it up.
- **crew's old records.** crew no longer reads `~/.local/state/crew/previews`, and no longer runs sluice for what they name. A preview such a record names stays up until a person puts it away (*After deploy*).
- **Rollback.** A crew rolled back reads no `previews.rec`. Its preview path runs as before, and the requests written stand unanswered by it.

## After deploy

- **crew's old preview records**, on each host crew's release reaches that holds one under `~/.local/state/crew/previews`. deneb held none on 2026-11-08; the box was not read.
  - **Doer:** the user, once the release is on that host.
  - **The step:** for each record whose `name` sluice there still lists, `sluice release <name>` in the record's `main`; then remove the folder.
  - **Why it is no code:** putting it away is a sluice command, which record 0056 point 1 rules out for crew. The runner puts away only a preview its control plane asked it to bring up (Boomdrive previews spec, "A done with nothing to put away runs nothing"), so crew cannot ask it to.

## Follow-ups

For the orchestrator to carry:
- **agentplot/boomdrive.** `Main::plans` (`crates/boomdrive-crew/src/read.rs`) reads `bolt/<b>` as in the plan while it holds `Bolt: <b>`, so a landed or dropped bolt's previews leave the runner's files as a unit's do.
- **agentplot/crew, `crew-lands-each-bolt-through-flumes-base-place`, record 0056's `land` change.** Its proposal, design, specs and tasks are at 56520fe0, on its own branch and not landed. It edits:
  - the same descriptor, `Act`'s enum gaining `land` after `retry`;
  - the same requirement of `drive-state`, "crew asks a host's runner for work by requests on the drive's branch", adding a land;
  - the same requirement of `rail-cards`, "A landing row carries what brings its bolt's preview up", whose "Approved without a preview" has crew post `y`'s land.

  Whichever is built second carries both (`docs.3`).

## Open Questions

None.

## Task notes

**1.1** `plugin/lib/runner.py`:
- `REQUESTS`: as Decision 1. The comment above `%rec` says a request may also be "a preview of a branch at a revision on the host whose runner took the work it serves, or its done".
- `FIELDS`: `Branch`, `Revision`, `Done` after `Base`.
- `ACTS["preview"] = (("Host", "Repo", "Branch", "Revision"), ("Done",))`.
- `WORK`: a pattern `PREVIEW_WORK` of `bolt/N` and `unit/N`. `request_refusal` takes a preview's work from `PREVIEW_WORK` alone and any other act's from `WORK` alone, so `bolt/<b>` on a launch is refused saying it is a preview's work alone.
- A preview naming no `Host` is refused: "a preview names the host whose runner brings it up". `Done` other than `yes` is refused.
- `preview_fields(host, repo, branch, revision, done=False)` gives the `given` that `plan.request` takes beside the act and the work.

Cases in `tests/py/test_runner.py`, class `TestPreviewRequest`:
- a preview's fields in the file's order, and `Done: yes` for a done;
- a preview of `bolt/y` and one of `unit/a` pass;
- naming no `Host`, `Repo`, `Branch` or `Revision`, each refused naming it;
- carrying `Kind` or `Stream`, refused naming them;
- a launch, retry or drop of `bolt/y` refused;
- the descriptor's text holding `preview` last in `Act`'s enum, `%type: Done bool` after `Submission`'s line, and `Branch Revision Done` after `Base` in `%allowed`, as `FIELDS` orders them.

**1.2** `plugin/lib/runner.py` `PREVIEWS`, byte for byte:

```
%rec: Preview
%key: Request
%type: Request int
%type: Outcome enum held done refused
%type: Listed enum yes no
%type: At date
%mandatory: Request Outcome At
%allowed: Request Outcome Text Status Listed Words At
```

- `FILES["previews.rec"] = "Preview"`.
- `host_read`: `previews` by request number, each `{outcome, text, status, listed, words, at, why}`. `text` and `status` are parsed JSON or `None`; `listed` is `True`, `False` or `None`; `why` is set where either is no JSON.
- A request missing or twice makes the host unreadable, naming `previews.rec`.

Cases in class `TestHostReadPreviews`:
- read by number;
- no file reads none;
- twice and missing number each unreadable;
- a record before `%rec` unreadable;
- a `Status` that is no JSON marks that preview alone;
- `previews.rec` refused by recfix (given in `refused`) unreadable.

**1.3** `plugin/lib/runner.py`:
- `previews_asked(requests)`: `{(host, repo, revision): request}` for each whose newest preview request is a bring-up, whatever the runner answered. A row or a line carries this ask's report, so a refusal is said on the card until the user asks again.
- `previews_standing(requests, reads)`: those of `previews_asked` whose host's runner has not refused them (`preview_report`). Only a standing ask is kept, given back or put away.
- `preview_report(reads, request)`: Decision 3, returning `{state, host, head, name?, addresses?, words?, at?, why?}`. `head` is the request's `Revision`. Its states are `asked`, `held`, `waiting`, `starting`, `up`, `failed`, `refused`, `unlisted` and `unread`.
- `ask_step(ask, report)`: `keep` or `ask`, Decision 6.
- `preview_word(shown)`: Decision 4's words, from a card's shape.

Cases in class `TestPreviewReport`:
- each outcome of `previews.rec`;
- a `Status` winning over `Text`;
- `Listed: no` reading `unlisted`;
- a refused `Answer` read as refused, in the runner's words, as `its Act preview, which crew's implementation does not read`;
- no answer reading `asked`;
- the host unread reading `unread`;
- a `state` crew does not read, or `addresses` that is no object, reading `unread` naming the field;
- standing ended by a done and by a refusal, and standing again after a bring-up following a done;
- `ask_step`'s two outcomes;
- `preview_word` of each shape.

**1.4** `plugin/lib/runner.py` `previews_put_away(asks, carried, works, now=None, grace=0)`: the standing asks, as `previews_standing` gives them, that no carried triple, no work and no grace keeps, each the bring-up request whose done is to be written.

Cases in class `TestPreviewsPutAway`:
- a row that can land at the head keeps its ask;
- a head moved puts the old one away;
- a held or gone row puts it away;
- a work in `works` keeps it;
- an ask under two minutes old kept by `grace`, and one over it put away;
- a person's preview, which no request names, is never in the output.

**1.5** `tests/contract/test_recfix.py`, recfix run for real:
- `test_requests_of_every_act_pass_and_the_descriptor_refuses_what_it_does_not_allow` gains a preview and its done, as `request_fields` writes them from `preview_fields`, which pass under `runner.REQUESTS`, and a `Done: maybe`, which recfix refuses;
- a new case: a `previews.rec` under `runner.PREVIEWS`, holding a `Preview` of each outcome with `Text` and `Status` on one line each, as Boomdrive's `write.rs` writes them, passes `recfix --check`, and one with `Outcome: up` is refused.

**2.1** `plugin/lib/cards.py`:
- `preview_said`: Decision 4's shapes; `none` and `policy` go. The words for `ask` and for waiting, starting and up stay as today. Failed carries no output, and `last_lines` stays for its other callers.
- `made_said`: the same states under a line. "it could not be brought up: <words>" for refused, unread and failed; "it waits for room on <host>" for held; "it is asked of the runner on <host>" for asked.
- `landing_card`'s and `landings_card`'s links: unchanged, the addresses still coming from `preview_said`.

Cases in `tests/py/test_cards.py`:
- the existing cases of `none` and `policy` removed;
- one case for each new shape on a landing row and a batch line;
- a failed preview saying it did not come up with no output.

**3.1** `plugin/lib/plan.py`:
- `card_preview`, Decision 6. It runs on the main machine and takes the thing from `preview_target` over every row of the card's last `Heads` (`card_heads`) for `land/<kit>`, or over the unit's made lines for `batch/<n>`.
- For a landings row: read through `CardActs.land_row(label, bolt, host)`; the host is `bolt_at`'s `machine`, `Revision` the row's full `facts["head"]`, `Repo` the bolt's.
- For a batch line: `CardActs.made(label, host, [unit], key)["made"]`, the line by its name with both `branch` and `revision`; the host is `batch_unit_at`'s; `Repo` the bolt's newest launch's `Repo`.
- The ask (`previews_standing`) and the report (`preview_report`), from `runner_facts`. `ask_step`, or the done.
- The write: `write(fleet, label, change, subject, act="card.preview", on=[work], fields={"Key": key, "State": "asked" or "done"})`, `change` calling `request(w, "preview", work, **runner.preview_fields(...))` with each fact read again at the tip (`plan.1`). It is refused and recorded as refused where the write is.
- Then `preview_changed(fleet, label, key, asked_note(thing, shown))`, and the printed line naming the request's number and what the card says.
- `REQUESTERS["card preview"] = ("main-ops", "planner")`.
- `record.py`'s docstring names `card.preview` among crew's card acts.

Cases in `tests/py/test_card_commands.py`, replacing those of `card_preview_here` and the forward to the work's host:
- ops's ask writing one preview naming deneb, `bolt/y`, the kit, `bolt/y` and the full head;
- the card changed with the asked note;
- asked twice while the runner reports it up writing nothing;
- asked again after a refusal writing a second;
- `--done` writing the done, and with none standing writing nothing and saying so;
- a batch line's ask naming `unit/a` and the line's branch and revision;
- a thing the card does not carry refused, writing nothing;
- a conductor refused, writing nothing;
- `sluice` never run (the fakes record no call).

**3.2** `plugin/lib/plan.py`:
- `land_row` reads no preview and releases none: `landing_preview`, `land_end`'s release and `acts.release_preview` go.
- `landings_previews`, called by `landings_raised` before `landings_step` builds the card, makes Decision 7's write in main-level ops's name, then gives each row that can land its preview, from `runner_facts`, `previews_asked` and `preview_report`: the ask of `(host, kit, head)` as reported, else `{branch: "bolt/<b>", head, state: "ask"}`, with `released` where that write put an ask of that bolt at another head away.
- After a post or change, what each row was told is kept (Decision 8, `told_kept`). `told_read(label)` and `told_keep(label, key, {request: word})` read and write `CARDS/<label>/previews.json` atomically, as `landing_word_keep` writes, and only when it changes; unreadable, it reads as `{}`. 3.3 and 3.4 use them too.
- `CardActs.preview` and `release_preview` go; `LandActs` in the tests follow.

Cases in `tests/py/test_landings.py`:
- a row that can land carrying `ask`, with no policy read;
- a row whose ask stands carrying the runner's report;
- a moved head writing the old ask's done, the row saying it was released as the head moved and no ask written at the new head;
- a held row writing its done;
- a bolt gone from the plan writing its done;
- a refused ask writing none.

**3.3** `plugin/lib/plan.py`:
- `batch_made` gives each unit's `up`, `{name: shown}`, from the runner's reports of the asks (`previews_asked`) at each line's revision on the unit's host, in its repository as its bolt's newest launch names it (`unit_repo`), not from `acts.made`'s `previews`; it returns what each line was told.
- `made_cmd` prints `{"made": ...}` alone and takes no `--card`; `made_listed` reads an older crew's `previews` beside it as nothing.
- `row_card_close` for `batch/<n>` writes Decision 7's dones in the planner's name (`batch_previews_put_away`) in place of `acts.release_previews`.
- `CardActs.release_previews` and the `_preview-release` command go.
- `raise_batch` keeps what each line was told (`told_keep`).

Cases in `tests/py/test_batches.py`:
- a line's `up` from the runner's report;
- the close writing the dones of its units' standing asks;
- the close keeping an ask whose unit another open batch card holds.

`tests/py/test_card_commands.py`'s `test_a_batch_cards_close_hands_its_previews_release_on_and_no_other_card_does` is removed.

**3.4** `plugin/lib/plan.py`:
- **`sweep_previews(fleet, read, acts)`**, called in `rail_read` after `sweep_moved` and only for partitions whose main machine is this host, as `sweep_moved` is.
  - It takes `sweep_judgment`'s live keys and blind prefixes for each partition, as `sweep_sessions` builds them.
  - It writes Decision 7's dones with a grace of 120 seconds by each ask's `Date`, one write for each card the asks came from (`ask_card`: `land/<repo>` for a bolt's, the newest batch holding a unit for a unit's), in that card's owner's name.
  - It returns `[{label, work, revision, said}]` in `read["previews"]`, which `rail_text` lists beside the sessions it ended.
- **`previews_changed(fleet, read, acts)`**, after it: Decision 8, through `told_read` and `told_keep` (Task notes 3.2), and `SweepActs.preview_note`, which hands the note to `preview_changed` (`land_hand` or `batch_hand`). A card answered is one the run record holds a `card.answer` for. It returns `[{label, key, note, said}]` in `read["previewed"]`, which `rail_text` lists too.
- **`card_sweep`** releases no previews, and its docstring and the judgment it reads say so. `preview_files`, `preview_row_key` and `preview_dead` go.

Cases in `tests/py/test_rail.py`, its `release_preview` and `release_previews` fakes removed:
- a dead ask written its done on the main machine and none on another host;
- an ask under two minutes old kept;
- a blind prefix keeping its asks;
- a waiting card changed once when the runner's report moves, and not on the read after;
- an answered card left;
- a lost cache changing the card once.

**3.7** `previews_changed` passes over a card whose key is `None`, as `rail_times` keeps the key of a card posted with no `Key` (an agent's own question, as t-cards posts the planner's). Before, the planner's such card reached `re.fullmatch(r"batch/\d+", None)` and the whole rail read on the main machine failed with a traceback. The case in `tests/py/test_rail.py`'s `TestPreviews`: a keyless card in the planner's name and one in ops's, beside the kit's landings card, which is still changed.

**3.5** Remove Decision 9's code from `plugin/lib/plan.py`, `plugin/lib/kit.py` and `CardActs`, with the cases of it:
- `tests/py/test_landing.py`, its preview cases from `test_what_a_rows_read_does_with_the_preview_brought_up_from_its_card` to `test_how_sluices_preview_ended_is_read_from_its_exit_and_its_words`, keeping `test_the_close_names_the_commit_landed_and_says_nothing_of_a_preview`;
- `tests/py/test_kit.py`'s cases of `previewed`;
- `tests/py/test_batch_answer.py`'s fakes.

The guard `test_crew_runs_no_sluice_command_for_a_preview`, in `tests/py/test_runner.py`, reads `plugin/lib/*.py` and `plugin/bin/crew`. It finds:
- no `"preview"`, `"previews"` or `"release"` argument passed to `sluice_read`, nor a `sluice preview`, `sluice previews` or `sluice release` command line;
- no `previewed(` call;
- no `.local/state/crew/previews` path.

**3.6** `plugin/bin/crew`: `_preview`, `_card-preview` and `_preview-release` leave the internal commands' list and the dispatch comments. `plan.py`'s parser and `COMMANDS` drop them. `tests/t-help.sh` drops their lines from the internal commands it asks for `--help`.

**4.1** End to end:
- **`tests/lib.sh`** gains `runner_previews <host> <request> <outcome> [<text JSON> [<status JSON> <listed>]] [<words>]`. It writes `previews.rec` under `runner.PREVIEWS` beside the files `runner_writes` keeps, one call adding or replacing a request's record, in the same commit-tree way. `runner_writes` carries `previews.rec` when present.
- **`tests/stubs/sluice`**: `preview`, `previews` and `release` go, with the flags `sluice-preview-holds` and `sluice-preview-fails`.
- **`tests/t-journey-land.sh`'s preview steps:**
  - ops's `crew card preview land/switchboard-kit tenant-environments` writes one preview on `wldn/main`'s `requests.rec`, naming `chuck-herdr-alpha`, `bolt/tenant-environments`, the kit and the head; the card is changed with the asked note; no `sluice preview` is called;
  - `runner_previews` answers it done with a listing `starting` and an address; at the rail's read the card is changed listing it;
  - a listing `failed`; the card is changed saying it did not come up;
  - `--done` writes the done and changes the card;
  - after the take-main fix, a second ask; the landing's raise writes its done;
  - no step reads `~/.local/state/crew/previews`.
- Run `tests/moon-tasks` and commit `tests/moon.yml` if the test's `# Reads:` line changes (`tests.10`).

**4.2** The verify run's `t-journey-land` (moon `exitCode: -1` after 3 m 15 s, at 18:54:53 on 2026-11-08, nothing captured) was its runner ended by a signal and not the test failing:
- Its scratch folder, `/tmp/crew-test.NWyoVP`, made at 18:51:37 when the task started, still holds all 29 of the test's `ok` lines, written until 18:56:44, two minutes after moon recorded the end. `tests/run` removes a passed test's folder and prints its line, and did neither.
- `tests/slot`, and the test under it, ran on. `tests/slot` passes a TERM, INT or HUP to the test's group, and a KILL of it ends the group through its keeper. So the signal reached `tests/run` alone. It was not sent to the group, and not to `tests/slot`.
- Nothing the test or crew runs signals a pid outside its own test. The test's kills reach only processes it started (`submitters`, `stopped`, the decoy). crew's own kills are a card session's recorded plannotator pid and the landing waiter's own children.
- Alone and through moon, `tests/run t-journey-land` and `tests/suite t-journey-land` end "1 passed, 0 failed" on the change, in 5 m 18 s and 4 m 40 s. Nothing in the change is fixed for it.

**5.1** `plugin/roles/main-ops.md` and `plugin/roles/planner.md` as Decision 10. `tests/t-briefs.sh`'s phrases at its batch-card and landings-card checks follow them.

**5.2** `README.md`, `plugin/skills/crew/SKILL.md` and `plugin/bin/crew`'s usage of `crew card preview` say the preview is asked of the runner on the host where its work runs. They also say every row that can land offers one, and the card lists its addresses once the runner reports them. README's sentences on `[preview]` and "no preview" go, and so does "sluice's one preview of a revision kept while another of crew's records still names it". `tests/t-docs.sh`'s preview checks stand.
