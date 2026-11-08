## MODIFIED Requirements

### Requirement: A kit's rename is one entry naming both its names
`crew kit rename` SHALL leave one `kit.rename` entry per act, done or refused. The entry SHALL name the kit by its new name, `On: kit/<new>`, and by the name it had, `From: kit/<old>`, with `Repo` its new name and `Count` the number of plan records it renamed. It SHALL hold no text anyone typed. The entry SHALL be the record of the act alone: no `kit.rename` entry, done or refused, SHALL rename anything crew reads, and `crew events` and `crew trace` SHALL print it as written. An entry already written SHALL stay valid under the run record's descriptor, so a branch holding one takes every write.

#### Scenario: The entry of a rename
- **WHEN** the user runs `crew kit rename tailrace timber` on madswan's plan, renaming 21 records
- **THEN** madswan's run record holds one `kit.rename` entry with `On: kit/timber`, `From: kit/tailrace`, `Repo: timber` and `Count: 21`, its commit's `Crew-Entry` naming it, and the day file holding it passes `recfix --check`

#### Scenario: A refused rename renames nothing
- **WHEN** a rename of `tailrace` to `timber` is refused because deneb still keeps `agentplot/tailrace`
- **THEN** its entry is a refusal, and crew still reads `tailrace` as written

#### Scenario: A rename's entry renames nothing
- **WHEN** a tip's run record holds a `bolt.land` under `tailrace` and, after it, a done `kit.rename` entry of `tailrace` to `timber`
- **THEN** the landings at that tip are that one `bolt.land`, read in one read of the run record, and the partition's kits name `tailrace` as written
