## MODIFIED Requirements

### Requirement: A preview names its host, its work, its repository, its branch and its revision
A preview request SHALL name the host whose runner reported the work it serves (the requirement "A kit's work is taken by a runner whose configuration names its repository"), since only that runner brings it up; the work it serves, `bolt/<bolt>` for a landings row's bolt or `unit/<unit>` for a batch line; its repository as the plan names it; the branch and the revision; and, to put it away, `Done: yes`. It SHALL name nothing else ("A bolt's work is its base place's and its preview's").

#### Scenario: A preview of a landings row's bolt
- **WHEN** `crew card preview land/crew y` appends a preview naming `Host: deneb`, `Work: bolt/y`, `Repo: crew`, `Branch: bolt/y` and `Revision: abc1234`
- **THEN** the write passes crew's rules and recfix

#### Scenario: A preview naming no host
- **WHEN** a write would append a preview naming no `Host`
- **THEN** it is refused by crew's rules, saying a preview names the host whose runner brings it up, and the branch is unchanged

#### Scenario: A preview carrying what it does not take
- **WHEN** a write would append a preview naming a `Kind` or a `Stream`
- **THEN** it is refused by crew's rules, naming the fields, and the branch is unchanged

#### Scenario: A bolt's work on any other request
- **WHEN** a write would append a launch serving `bolt/y` of the kind `change`
- **THEN** it is refused by crew's rules, saying a bolt's base place is of crew's kind `crew/bolt`

## ADDED Requirements

### Requirement: A bolt's work is its base place's and its preview's
`bolt/<bolt>` SHALL be the work of the bolt's base place, its launch of crew's kind `crew/bolt` and the retry, drop, priority and land of it ("A launch names everything the runner passes to Flume"), and of a landings row's preview, and of no other request. A retry, drop, priority or land SHALL name a launch by `Of`, never a preview.

#### Scenario: A preview and a land of one bolt
- **WHEN** `requests.rec` holds `bolt/y`'s base place's launch as request 1 and a preview of `bolt/y` as request 2, and a write would append a land of `bolt/y` naming request 1
- **THEN** the write passes crew's rules, and a land naming request 2 is refused, saying request 2 is no launch

#### Scenario: A retry or drop naming a preview
- **WHEN** `requests.rec` holds a preview of `bolt/y` as request 1, and a write would append a retry or a drop of `bolt/y` naming request 1
- **THEN** it is refused by crew's rules, saying request 1 is no launch
