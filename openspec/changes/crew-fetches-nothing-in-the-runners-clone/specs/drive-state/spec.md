## ADDED Requirements

### Requirement: crew fetches nothing in the runner's clone
Where the host's teams file names a repository, its `dir`, its `checkout` and every folder under either SHALL be the runner's clone. crew SHALL run no `git fetch` there, and no brief crew writes SHALL have an agent fetch or pull there. Where another requirement has crew fetch a kit before it reads, crew SHALL read the runner's clone at origin's tracking refs as the runner last fetched them. A checkout the file does not name, and every checkout on another host, SHALL be fetched as before.

#### Scenario: crew bolts on a runner host
- **WHEN** box's teams file names a kit's repository, whose container is the folder box's runner reported for the kit's work, and `crew bolts` runs
- **THEN** the kit is read with no fetch, at `origin/bolt/<bolt>` as the runner last fetched it, and no ref of the clone moves

#### Scenario: Main now in the runner's clone
- **WHEN** a read of main now runs in the runner's clone while GitHub's main is past the runner's last fetch, and origin cannot be reached
- **THEN** main now is `origin/main` as the runner last fetched it, no ref moves, and once the runner fetches, main now is GitHub's main

#### Scenario: What a tip carries in the runner's clone
- **WHEN** a landing reads what its tip carries in the runner's clone while main's landing of another bolt is on GitHub and not yet fetched
- **THEN** it reads the branches as the runner last fetched them, moving no ref, and reads main's landing once the runner fetches

#### Scenario: A forecast in the runner's clone
- **WHEN** a landings card's forecast reads the kit in the runner's container on deneb, whose teams file names it
- **THEN** it reads the kit's origin and fetches nothing, while a kit the file does not name is fetched as before

#### Scenario: Another host or another checkout
- **WHEN** crew reads a kit on alpha, whose teams file crew does not read, or a checkout on deneb that deneb's file does not name
- **THEN** it fetches as before

### Requirement: A landing in the runner's clone waits for the runner's fetch
A landing whose tracking ref of `bolt/<bolt>` in the runner's clone is not at the commit GitHub's `bolt/<bolt>` is at, as `git ls-remote` reads it, SHALL submit nothing, saying it waits for the runner's next fetch.

#### Scenario: A landing waits for the runner's fetch
- **WHEN** a landing reads its bolt's copies in the runner's clone while GitHub's `bolt/b` holds two merges beyond the clone's `origin/bolt/b`
- **THEN** it submits nothing, saying the runner's clone holds `origin/bolt/b` at one commit while GitHub's is at another and that it waits for the runner's next fetch, and once the runner fetches, it reads both copies as before
