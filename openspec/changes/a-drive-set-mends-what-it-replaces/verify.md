# Verify: a-drive-set-mends-what-it-replaces

Verified 2026-11-09 on `change/a-drive-set-mends-what-it-replaces` at d34e8290, cut from `bolt/crew-names-each-drive-once`.

## The whole checks

Run once, as CLAUDE.md's *Tests* names them for a finished change: `tests/suite --affected`, every `check-full` task whose inputs differ from the merge-base with `main`, as sluice selects them.

**Outcome: passed.** `35 passed (4 replayed), 0 failed`, exit 0. Replayed from a pass on this host with identical inputs: `mod`, `nix:format`, `nix:lint`, `t-docs`. Run: `contract`, `logic`, `nix:test`, `nix:typecheck` and every affected end-to-end test, `t-drive-set` among them.

`openspec validate a-drive-set-mends-what-it-replaces --strict`: valid.

## Tasks

All three are ticked, and each holds:

- **1.1** `crew.settable` (`plugin/lib/crew.py`) refuses `drives` that is no list, a drive that is no object, and `hosts`, `consoles` or `repositories` that is no object, naming the key in Decision 3's words; absent and null parts pass. `teams_set` calls it first on any file, writes a drive listed twice once naming `drives.<label>`, sorts string labels first and others after in the file's order, and reads another drive's `repos` only where it is a list, and only its strings. Cases: `TestSettable`, `TestTeamsSet.test_a_drive_listed_twice_is_written_once_and_named_whole`, `test_other_drives_of_any_shape_are_kept_as_the_file_holds_them`.
- **1.2** `teams_step`'s readable path no longer checks the file as it stands: it sets the drive (`teams_set`), refusing a `settable` refusal as "`<teams file>` is at crew's version 6, and crew drive set cannot keep what it holds beside drive `<label>`: …", then checks the file it would write (`fleet_of`), refusing as "the teams file crew drive set would write is refused: …", each ending with the tail that the set sets only what its flags give, moves aside only a file crew cannot read at all, and leaves the file and every drive it names as they are. The no-file and aside paths keep "Nothing was written."; the link path is unchanged. The step is decided under the lock before anything is written (`plan.drive_set`), so a refusal writes nothing, links nothing aside and makes no state.
- **2.1** README's *State*, `plugin/skills/crew/SKILL.md`, the usage headers of `plugin/bin/crew` and `plugin/lib/plan.py` and `plan.drive_set`'s docstring say the set mends what it replaces in a file at crew's own version and refuses it only where a check still fails or a part is of a shape it cannot keep. `tests/t-docs.sh` holds README and the skill to "mends what it replaces" and "a check still fails"; its opening comment says so.

## Requirement and scenarios

**A teams file at crew's own version is written where the set mends it** (renamed from "…that fails a check is refused"): met. Each scenario has its logic-tier case in `tests/py/test_drive_set.py`, `TestTeamsStep`:

| Scenario | Case | Holds |
|---|---|---|
| A fault in the drive's own entry | `test_a_fault_in_the_drives_own_entry_is_mended` | written, `lab` as it was, `changed` `["drives.pat.folder"]`, step `write`, not `aside` |
| A fault in a host the flags name | `test_a_fault_in_a_host_the_flags_name_is_mended` | written with `darwin`, `changed` `["hosts.pats-mac"]` |
| The drive listed twice | `test_the_drive_listed_twice_is_written_once` | one `pat`, `changed` `["drives.pat"]` |
| A file that lists no drives | `test_a_file_that_lists_no_drives_is_written` | written naming `pat`, step `write`, no aside |
| One wrong field beside another drive | `test_a_file_at_crews_own_version_that_fails_a_check_is_refused_and_never_moved_aside` (aside taken and not) | refused naming `lab`'s folder, ending with the tail, no "cannot load" or "is taken" |
| A file that lists teams | `test_a_file_that_lists_teams_is_refused` | refused naming `lists teams`, ending with the tail |
| A part of another shape | `test_a_part_of_another_shape_is_refused` | refused naming `'hosts' is an object, not []`, ending with the tail |

The requirement's other clauses: each key changed is named (`changed`, carried to the `drive.set` entry unchanged); a check's refusal on the flags' own parts carries the same tail (`test_a_file_crew_would_refuse_is_refused_in_its_words_with_nothing_written`, `text=self.written()`); a file at crew's own version never reaches the aside path, which only `readable`'s refusal takes.

## Rules and the rest

- `code.2`: every refusal goes through `fail`; no file `readable` gives ends in a traceback (the other-shapes cases).
- `code.7`: `settable`, `teams_set` and `teams_step` stay decisions on plain facts; nothing new reaches a tool.
- `code.8`: nothing the agents' views or `plugin/hooks/status.js` draw changed.
- `read.1`, `read.4`: a file at crew's own version is never moved aside or taken over; a part crew cannot keep is refused, never dropped.
- No rule or record is written here (`docs.7`). Once this lands, the design agent may mark record 0065's point 8 built and bring point 9's words on a version-6 file that lists no drives to point 8 (design, Decision 2).

## Notes

- The link path calls `teams_set`, and so `settable`, only on a file `fleet_of` passed. Should `fleet_of` pass a file `settable` refuses, the refusal is `settable`'s words without the link's: still a refusal, never a traceback, and the design leaves `fleet_of`'s own reading of a `drives` that is no list outside this change (Decision 3, *Not taken*).

Verdict: the whole checks pass and the work holds. Archived.
