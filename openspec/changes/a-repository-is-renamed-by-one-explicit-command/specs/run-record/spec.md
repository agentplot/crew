## MODIFIED Requirements

### Requirement: The run record is files on the host, appended and never rewritten
Entries SHALL be recutils records in `~/.local/state/crew/<label>/runs/<host>/<date>.rec` on the host where the command ran, one file per UTC day, each append one write. crew SHALL never rewrite or remove an entry in a host's file. The drive's branch's copy of an entry SHALL be rewritten only by `crew kit rename`, and only to rename a repository's name, in the rename's one commit, which holds what each entry said before. A failed append SHALL be reported on standard error and SHALL NOT change the command's result or exit status.

#### Scenario: After a restart
- **WHEN** a host restarts
- **THEN** every entry written before it is still in its file

#### Scenario: The record cannot be written
- **WHEN** the run record's directory cannot be written
- **THEN** the command does its work and exits as it would have, with one line on standard error saying the entry was not recorded

#### Scenario: Read with recutils alone
- **WHEN** `recsel -e "On = 'unit/<unit>'"` is run over a host's run-record files
- **THEN** it prints that unit's entries, with no crew command involved

#### Scenario: A rename's rewrite
- **WHEN** the user renames `tailrace` to `timber` and the branch's run record holds a `bolt.land` entry with `Repo: tailrace`
- **THEN** the rename's commit changes that entry's `Repo` to `timber` and its parent holds it as it was, and the file on the host that wrote it still says `tailrace`

### Requirement: A kit's rename is one entry naming both its names
`crew kit rename` SHALL leave one `kit.rename` entry per act, done or refused. The entry SHALL name the repository by its new name, `On: kit/<new>`, and by the name it had, `From: kit/<old>`, with `proposal/<n>` beside it when a proposal's approval applies the rename. Its `Repo` SHALL be the new name and its `Count` the number of records the rename renamed, all files together. The rename's commit SHALL name the entry in its `Crew-Entry`, and the entry SHALL reach the branch as the commit after. It SHALL hold no text anyone typed. The entry SHALL be the record of the act alone: no `kit.rename` entry, done or refused, SHALL rename anything crew reads, a later rename SHALL leave it as written, and `crew events` and `crew trace` SHALL print it as written. An entry already written SHALL stay valid under the run record's descriptor, so a branch holding one takes every write.

#### Scenario: The entry of a rename
- **WHEN** the user runs `crew kit rename tailrace timber --label madswan`, renaming a Source, two requests and five entries
- **THEN** madswan's run record holds one `kit.rename` entry with `On: kit/timber`, `From: kit/tailrace`, `Repo: timber` and `Count: 8`, its commit's `Crew-Entry` naming it, and the day file holding it passes `recfix --check`

#### Scenario: A refused rename renames nothing
- **WHEN** a rename of `tailrace` to `timber` is refused because deneb's runner still keeps `agentplot/tailrace`
- **THEN** its entry is a refusal, and every record that named `tailrace` still does

#### Scenario: A rename's entry renames nothing
- **WHEN** a tip's run record holds a `bolt.land` under `tailrace` and, after it, a done `kit.rename` entry of `tailrace` to `timber` that a rename made before this change left
- **THEN** the landings at that tip are that one `bolt.land`, read in one read of the run record, and the partition's kits name `tailrace` as written

#### Scenario: A later rename leaves it
- **WHEN** the run record holds a `kit.rename` of `tailrace` to `timber`, and the user later renames `timber` to `trc`
- **THEN** the first entry still says `On: kit/timber`, `From: kit/tailrace` and `Repo: timber`
