## ADDED Requirements

### Requirement: A decision reads the drive's branch at its tip
A decision SHALL read a drive's branch at its tip, whatever entries the commits there name, and no command SHALL say it read the branch below its tip. An older crew wrote a commit in two steps: the act's commit names an entry, and the next commit adds it. Such a commit SHALL be read at the tip like any other. Its entry SHALL join the run record when it reaches the branch.

#### Scenario: A write whose entry has not arrived
- **WHEN** `wldn/main` holds a write by `swb-1-conductor`, made by an older crew, whose entry the branch lacks, and the planner's proposal 6 was written after it
- **THEN** `crew plan proposed 6` prints proposal 6, and nothing it prints says the branch was read below its tip

#### Scenario: The entry arrives later
- **WHEN** that write's entry reaches the branch as its own commit
- **THEN** `crew events --label wldn` prints it in time order with the rest

## MODIFIED Requirements

### Requirement: Each commit on a drive's branch names the run-record entry it describes or adds
Each commit crew makes on a drive's branch SHALL name, in a `Crew-Entry:` trailer, each run-record entry it adds to `runs/<host>/<day>.rec`. An act's commit, such as a plan write, SHALL add the entry of that act and of each act it holds, and no other entry. A commit holding an entry alone, for an act that wrote no commit on the branch, SHALL add that entry and change no other file.

#### Scenario: From a commit to its entry
- **WHEN** a plan write's commit on `wldn/main` is read
- **THEN** each of its `Crew-Entry` ids is the `Id` of an entry that commit adds to its host's `runs/<host>/<day>.rec`, the write's own entry among them, and none of those entries names a commit of `wldn/main`

#### Scenario: An approval's one commit
- **WHEN** `crew plan approve` applies a proposal that adds a unit to the queue
- **THEN** its one commit adds the `plan.approve` entry and the `unit.add` entry, and names both in its `Crew-Entry` trailers

#### Scenario: An entry's own commit
- **WHEN** the commit that adds a tell's entry on `wldn/main` is read
- **THEN** its `Crew-Entry` id is the `Id` of the entry it adds to `runs/<host>/<day>.rec`, its subject ends with ` (<agent>)`, and it changes no other file

### Requirement: Every plan write is an act whose entry is pushed before it returns
Every plan write SHALL be an act. Its entry SHALL be in the write's own commit, added to its host's `runs/<host>/<day>.rec` beside the plan's change and made again on each replay. Once its push is accepted, the write SHALL append the entry to the host's own file. crew SHALL refuse a write that names no act before it reads or pushes anything, since its commit would name an entry nothing writes.

#### Scenario: Once a write returns
- **WHEN** a plan write on `wldn/main` returns, its push accepted
- **THEN** the branch's tip is the write's commit, which holds the plan's change and the write's entry in `runs/<host>/<day>.rec`, and the host's own file holds the same entry

#### Scenario: A write applied again
- **WHEN** a write's push is refused because another command on the same host has pushed an entry to that day's file
- **THEN** the write is applied again on the new tip, and its commit's file holds the other command's entry as it was, with the write's beside it

#### Scenario: A write that names no act
- **WHEN** crew is asked to write the plan with no act
- **THEN** it refuses, naming the write, and the branch is where it was

## REMOVED Requirements

### Requirement: A decision reads an act whole and says when it read below the tip
**Reason**: An act's commit now carries its entry, so the branch never holds an act without it. The read below an act whose entry had not arrived held every decision while that entry was missing. That was ten minutes and more three times on 2026-11-09 and 11-10, when an entry's push failed every retry and nothing recovered it.
**Migration**: None. Every decision reads the tip ("A decision reads the drive's branch at its tip"). A commit an older crew wrote in two steps is read there too, and its entry joins the record whenever it arrives.
