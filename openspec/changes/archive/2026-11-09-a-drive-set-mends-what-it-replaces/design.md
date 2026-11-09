# Design

## Context

**What is asked.** Record 0065's amendment of 2026-11-09 (accepted by agentplot-design) gives point 8 as agentplot-design's, on batch 26's review of `a-drive-set-loses-no-drive-and-no-record`, and names this change as its build:

> 8. **A set mends what it replaces (agentplot-design's).** A file at crew's own version is written where every check passes once the drive's entry and the hosts the flags name are set as given, whatever the file held for them before. Where a check still fails, the file is refused, naming the check, with nothing written (point 6). The set replaces those parts whole anyway (point 3), so a fault there is one the set itself mends, and refusing it would ask the person for a hand edit, which record 0009's amendment never asks of them. Not taken: refusing every file at crew's version that fails a check before the set, as the build first did.

agentplot/boomdrive record 0009's amendment of 2026-11-09 is the person's side: setup asks no hand edit of them.

**What crew does now.** `crew.teams_step` (`plugin/lib/crew.py`) reads a teams file with `readable`. A file it cannot read at all is moved aside (record 0065, point 6). A file it can read, at crew's version 6, is checked whole with `fleet_of` before anything else. Any refusal there is the step's refusal, "`<teams file>` is at crew's version 6 and fails a check: …", with nothing written. Only a file that passes is set by `teams_set` and checked again as the file it would write. So a version-6 file whose one fault is `pat`'s relative folder is refused by `crew drive set pat --folder /abs`, though the file that command would write passes every check.

**What `teams_set` reads.** It reads a file's `drives` as a list of objects, each by `label`, `machine` and `repos`, and its `hosts`, `consoles` and `repositories` as objects. Today it only ever sees a file `fleet_of` passed, or none. Once the set comes before the check, it sees whatever `readable` gives: any object at version 6. A `consoles` that is a list, or a drive that is a string, would then end the command in a traceback (`code.2`).

**How the family does it.** crew's module replaces the whole file and moves every file that is no link aside (`nix/modules/activate.sh`). `crew drive set` keeps every other drive of a file it can read, so it moves aside only a file it cannot read at all (record 0065, points 6 and 9). Point 8 changes neither. It only moves the check after the set, so the set's own parts never stand in its way. Nothing changes in the module or in Boomdrive.

**Rules this design relies on:** `code.2`, `code.5`, `code.7`, `read.1`, `read.4`, `roles.2` (core.md); `teams.9` (teams.md); `record.1`, `record.3` (record.md); `tests.4`, `tests.11`, `tests.12` (tests.md); `docs.2`, `docs.4`, `docs.6`, `docs.7` (docs.md).

**Area pages this change touches:** `core.md`; `teams.md` (`plugin/lib/crew.py`, `plugin/bin/crew`); `plan.md` (`plugin/lib/plan.py`, its docstring and usage header alone); `briefs.md` (`plugin/skills/crew/SKILL.md`); `tests.md` (`tests/`); `docs.md` (README, `openspec/`).

## Goals / Non-Goals

**Goals:**
- A version-6 teams file whose faults all lie in what the set replaces is written by the set, with no hand edit.
- A version-6 file that still fails a check once the drive is set is refused, naming the check, with nothing written and nothing moved.
- No teams file `readable` gives ends `crew drive set` in a traceback.

**Non-Goals:**
- Any change to the checks `fleet_of` makes, their order or their words, or to `crew.load`.
- Moving aside, or mending, anything beyond what the flags give: another drive's entry, a host the flags do not name, another drive's console, a kept repository another drive of this host keeps, or a key the file holds beside them.
- Any change to the link's handling, the aside, the refusal of a file crew would write where there was no file or it was moved aside, the answer, or the set's run-record entry.

## Decisions

### 1. The set comes before the check

For a file `readable` gives, `teams_step` no longer calls `fleet_of` on the file as it stands. It sets the drive in it (`teams_set`) and checks the file it would write (`fleet_of`). Where that passes, the step is `write`, or `unchanged` where the text is the file's own, with the keys `teams_set` names as changed.

What the set replaces is what point 3 has it own: the drive's entry, whole; each host `--hosts` names; the drive's console, set or removed; and each kept repository `--repositories` gives, a kept repository no drive of this host lists leaving with it. A fault in any of those is mended by the set, whatever the file held there. Each key it mends is a key it changed, so the set's `drive.set` entry names it by its path, as for any set (`record.1`, `record.3`). Nothing changes in `drive_set`'s order of acts or its record.

Not taken:
- **Checking the file as it stands and the file it would write, and refusing where the first fails on a part the set does not replace.** It would read which part a check is about from its words, or run the checks twice to compare them. The file it would write is the one fact point 8 names, and the only one that decides whether the host's file loads after the set.
- **Mending only the drive's entry and hosts, as point 8's words name them, and still refusing a fault in the drive's console or a kept repository the flags give.** Point 3 has the set replace those too, so they are as much the set's as the entry. Point 8's reason, "the set replaces those parts whole anyway", covers them.

### 2. What the set does not mend is refused

Where the file it would write fails a check, the step refuses in `fleet_of`'s words for it, ended with one period (`crew.sentence`), followed by one tail:

> the teams file crew drive set would write is refused: `<fleet_of's words>` crew drive set sets only drive `<label>`'s entry and the hosts, console and kept repositories its flags give, and moves aside only a file crew cannot read at all, so `<teams file>` and every drive it names are left as they are, and nothing was written

It is the same refusal whether the check is about a part the set kept, such as another drive's folder, or about a part the flags gave, such as two accounts in one session. The tail is true of both. The refusal comes before anything is written, under the lock (`teams.9`): nothing is written, nothing is linked aside and `drive_set` makes no state. It is recorded nowhere, since the file does not load, as for any refusal of a file that does not load (record 0065's build, Decision 10). Whether the aside is taken does not matter to it.

The refusal of a file crew would write where there was no file, or where the file was moved aside, keeps its words: "the teams file crew drive set would write is refused: `<words>` Nothing was written." There is no file there to leave as it is.

Two version-6 files point 9 names fall either side:
- **A file that lists `teams`** keeps its `teams` key through the set (point 3: "Everything else in the file stays, unknown keys included"), so the file it would write still fails "lists teams" and is refused, as point 9 has it.
- **A file that lists no drives** gives the file it would write the drive, so every check passes and it is written. Point 9 calls such a file crew's own and never to be moved aside, which holds. Its "is refused" was the build's under point 6, before point 8 had the set mend what it replaces, and point 8 has this file written ("whatever the file held for them before"). The design agent may bring point 9's words to it once this lands.

Not taken:
- **Two texts, one for a file that loaded before the set and one for a file that did not.** Telling them apart needs `fleet_of` run on the file as it stands too. A mixed file, a fault of its own and a fault from the flags, would get a text that names the wrong one.
- **Naming in the refusal the drive whose set would mend it.** The check's words already name the drive or host, and reading a drive back out of them would be a decision made on text.

### 3. A part of another shape is refused

`crew.settable(data)` refuses a teams file's data where the set cannot keep what a part holds beside the drive:
- `drives` given, not null, and no list: `<teams file>: 'drives' lists each drive as an object, not <its JSON, cut at 80>`;
- a drive in `drives` that is no object: `<teams file>: 'drives' lists <its JSON, cut at 80>, which is no drive's object`;
- `hosts`, `consoles` or `repositories` given, not null, and no object: `<teams file>: '<key>' is an object, not <its JSON, cut at 80>`.

A part that is absent or null holds nothing to keep, and passes. `teams_set` calls `settable` first on any file it is given. On the readable path, `teams_step` gives its refusal as:

> `<teams file>` is at crew's version 6, and crew drive set cannot keep what it holds beside drive `<label>`: `<settable's words>` `<the tail of Decision 2>`

Within a list of objects, `teams_set` reads another drive's `label` and `machine` as they are and its `repos` only where it is a list, and only that list's strings. It keeps every other drive as the file holds it, however wrong, so the check of the file it would write refuses it in `fleet_of`'s words (Decision 2). The drives with a string label come first, in the order of their labels, then any other in the file's order. Such a file is refused anyway, so the order only spares a traceback from comparing labels that are no strings.

Not taken:
- **Replacing a part of another shape with what the flags give.** A `hosts` that is a list holds something crew cannot read, and the set would drop it unread. Point 3 keeps everything else in the file.
- **Moving such a file aside.** It is at crew's own version, and moving it would drop every drive it names (point 6).
- **Giving these shapes their own checks in `fleet_of`.** `fleet_of`'s words for `hosts`, `consoles` and `repositories` that are no object stand, and a file that reaches `fleet_of` from `crew drive set` has passed `settable`. Where `crew.load` reads a `drives` that is no list, that is `fleet_of`'s own defect, outside this change.

### 4. The drive listed more than once

Where the file lists the drive's label more than once, `teams_set` writes one entry for it, the flags', in its place among the labels. It names `drives.<label>` as changed, as it does for a new drive, since no one entry was the drive's to compare key by key. `fleet_of`'s "lists drive `<label>` twice" is then a check the set mends. Another label listed twice is kept, and refused (Decision 2).

## Departures

- `openspec/config.yaml` asks that the last task run `tests/suite --affected`. This change's stage brief asks that no task run the repository's whole checks, which `--affected` is for any change to crew's command core (CLAUDE.md, *Tests*). The verify stage runs them once, after the last task.

## Risks / Trade-offs

- [A hand's change to the drive's own entry is replaced without a word] → It always was: point 3 replaces the entry whole for a file that loads. The set's entry on the drive's branch names each key it changed, so the branch says which were.
- [A fault in another drive's entry, or in a host no flag names, still refuses the set] → The check's words name the drive or host. Setup's `crew drive set` of that drive, with its own flags, mends it. A `teams` key, or a part of another shape, is mended by no set, as record 0065's point 9 has it. These come only from a hand, since crew's module and this command write neither.
- [A version-6 file that lists no drives, which the build refused, is now written] → It holds no drive to lose. Whatever else it holds stays, or the check of the file it would write refuses it.

## Migration Plan

None. A host's file changes only when the command runs there.

## After deploy

None: every scenario is proved by a check in crew's tiers.

## Task notes

**1.1** `plugin/lib/crew.py`:
- Add `settable(data)`, Decision 3's checks and words. It returns nothing and refuses through `fail` (`code.2`). Its docstring says it is the shape the set needs to keep what a part holds beside the drive, and that absent and null parts pass.
- `teams_set(data, given, here)`: call `settable(data)` first where `data` is not None.
  - Read the drive's old entry as the one entry whose `label` is the drive's. Where the file lists the label more than once, `changed` names `drives.<label>` (Decision 4).
  - `others`: every entry whose `label` is not the drive's, kept as it is.
  - Sort by `(0, label)` for an entry whose label is a string, else `(1, "")`, so the sort is stable for the rest.
  - `kept_by` reads an entry's `repos` only where it is a list, taking its strings.
  - Update the docstring.

`tests/py/test_drive_set.py`:
- A new class `TestSettable`:
  - `settable` passes `{"version":6}` and a file whose `drives`, `hosts`, `consoles` and `repositories` are each null.
  - It refuses `drives` given as `{}` and as `"pat"`, naming `'drives' lists each drive as an object`.
  - It refuses a drive given as `"pat"`, naming `'drives' lists "pat", which is no drive's object`.
  - It refuses `hosts` `[]`, `consoles` `[]` and `repositories` `"x"`, each naming `'<key>' is an object, not`.
- `TestTeamsSet`:
  - A file listing `pat` twice, both as the flags give it, is set to one `pat`, its text the one-`pat` file's and `changed` `["drives.pat"]`.
  - A file holding `pat`, then a drive with no `label`, then a drive `lab` whose `repos` is `7`, both on `pats-mac`, is set with no traceback. The drives are `lab` and `pat`, then the one with no label, each other drive as the file held it.
  - Every case there now passes unchanged.

**1.2** `crew.teams_step`, the path of a file `readable` gives (Decisions 1 to 3):
- Remove the `fleet_of(old, here)` check before the set and its refusal.
- Set the drive with `teams_set(old, given, here)`. A refusal from it is refused in Decision 3's words.
- Check the result with `fleet_of`. A refusal is refused in Decision 2's words.
- Otherwise `unchanged` or `write`, as now.
- The `checked` closure, used where there was no file or it was moved aside, keeps its words. The link's path is unchanged.
- Update the docstring.

`tests/py/test_drive_set.py`, `TestTeamsStep`:
- `test_a_file_at_crews_own_version_that_fails_a_check_is_refused_and_never_moved_aside`, with and without the aside taken (scenario One wrong field beside another drive): refused, starting `the teams file crew drive set would write is refused: drive lab in /Users/pat/.config/crew/teams.json: 'folder' is the absolute folder of its herdr session on pats-mac, not "Users/pat/lab"`, holding `crew drive set sets only drive pat's entry and the hosts, console and kept repositories its flags give, and moves aside only a file crew cannot read at all, so /Users/pat/.config/crew/teams.json and every drive it names are left as they are, and nothing was written`, and ending with it. It holds no `cannot load` and no `is taken`.
- The parametrized case of a file that lists no drives or lists teams becomes two cases.
  - `{"version":6,"drives":[],"hosts":{}}` is written, its text `self.written()` and its `changed` starting `drives.pat` (A file that lists no drives).
  - `{"version":6,"teams":[]}` is refused naming `lists teams, which version 6 has no place for` and the tail (A file that lists teams).
- New, A fault in the drive's own entry: `both()` with `pat`'s folder made relative in place of `lab`'s is written, its text the file `both()` builds before its edit, and its `changed` `["drives.pat.folder"]`.
- New, A fault in a host the flags name: `self.written()` with `hosts.pats-mac.kind` `macos` is written, its text `self.written()` and its `changed` `["hosts.pats-mac"]`.
- New, The drive listed twice: `self.written()` with `pat`'s entry listed twice is written, its text `self.written()` and its `changed` `["drives.pat"]`.
- New, A part of another shape: `{"version":6,"hosts":[]}` is refused, starting `/Users/pat/.config/crew/teams.json is at crew's version 6, and crew drive set cannot keep what it holds beside drive pat: /Users/pat/.config/crew/teams.json: 'hosts' is an object, not []` and ending with the tail.
- `test_a_file_crew_would_refuse_is_refused_in_its_words_with_nothing_written`:
  - with no file, it ends `Nothing was written.` as now;
  - with `text=self.written()`, it also holds the tail.
- Update the class's docstring to name the renamed requirement.

**2.1** README's *State*, its `crew drive set` paragraph: where it says a file at crew's own version that fails any other check is refused, it says instead:
- such a file is crew's own and never moved aside, since that would drop every other drive of the host;
- the set mends what it replaces, so the file is written wherever every check passes once the drive's entry and the hosts, console and kept repositories its flags give are set, whatever it held for them before;
- where a check still fails, or a part of it is of a shape the set cannot keep, it is refused in crew's words, the file and every drive it names left as they are, with nothing written.

`plugin/skills/crew/SKILL.md` says the same in its sentence on `crew drive set`, in place of "refuses one at crew's own version that fails a check". The usage headers of `plugin/bin/crew` and `plugin/lib/plan.py` say it in their `crew drive set` lines (`docs.2`). `plan.drive_set`'s docstring says so where it says a file at crew's own version that fails a check is refused.

`tests/t-docs.sh`: README and the skill each say that `crew drive set` mends what it replaces, by the phrase `mends what it replaces`, and that a check that still fails is refused, by the phrase `a check still fails`. Add that to its opening comment. Its `# Reads:` line already names README and `plugin/skills/`, so `tests/moon.yml` stays.
