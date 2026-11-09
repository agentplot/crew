## MODIFIED Requirements

### Requirement: crew asks a host's runner for work by requests on the drive's branch
crew SHALL write every request for a host's runner as a record of `requests.rec` on the drive's branch: a launch of a place, or a retry, drop, priority or land of one it launched. Each SHALL be numbered once, appended by a crew command in the commit of the plan write that occasions it, and checked by `recfix --check` and crew's own rules. A request SHALL never be removed. It SHALL never be changed, except by `crew kit rename`, which renames a repository's name in a request's `Repo` and in a fix of its main's `Work`, in the rename's one commit. Any other write that changes a request SHALL be refused.

#### Scenario: Never renumbered
- **WHEN** `requests.rec` holds requests 1 to 7 and a drop is written
- **THEN** it is request 8, and requests 1 to 7 are as they were

#### Scenario: A land is a request
- **WHEN** `requests.rec` holds requests 1 to 7, request 1 the launch of `bolt/x`, and the user's send of `x`'s row is carried to the runner
- **THEN** request 8 is a land of request 1, and requests 1 to 7 are as they were

#### Scenario: A rename's write changes a request's repository
- **WHEN** the user renames `flywheel-cloud` to `boomdrive-cloud` and request 3 has `Repo: flywheel-cloud`
- **THEN** the write passes crew's append check with request 3's `Repo` renamed and nothing else of it changed

#### Scenario: Any other write that changes a request
- **WHEN** a write other than a rename would change request 3's `Repo`
- **THEN** it is refused, saying a request is never changed or removed, and nothing is pushed

### Requirement: A launch names everything the runner passes to Flume
A launch of a kit's work SHALL name the work it serves, its repository as the plan names it, its kind, name and base, its priority, intent and recipient, and its brief, and SHALL name no host or stream, a runner whose configuration names its repository taking it, in the stream its host's Flume configuration maps the repository to; a launch of a role's work SHALL also name the host and stream its role runs in. A bolt's own launch, of `bolt/<bolt>`, SHALL name the kind `crew/bolt` and the base `main`, and no brief and no launch to land first, since its base place runs no agent; and any other launch SHALL NOT name the kind `crew/bolt` (record 0056 point 2). A start SHALL append the bolt's launch before its pieces' (bolt-teams), and a launch on the base `bolt/<bolt>` SHALL be taken with no launch of `bolt/<bolt>` before it, as a fix on a bolt started before bolts were base places is. A launch MAY name launches that must land first and a held submission. A retry, drop, priority or land SHALL name the launch it acts on and no host, and a land SHALL name a launch of a bolt or of a fix of main, its work the same as that launch's. crew's rules SHALL refuse a request that lacks what its act needs or names what its act does not take.

#### Scenario: A launch with no stream
- **WHEN** a bolt's start appends a launch of a kit's work naming no `Stream`
- **THEN** it is appended, a runner whose configuration names the kit's repository giving its stream

#### Scenario: A kit's launch naming a host
- **WHEN** a bolt's start would append a launch naming a `Host` or a `Stream`
- **THEN** the write is refused by crew's rules and the branch is unchanged

#### Scenario: A retry of nothing
- **WHEN** a retry would name request 9, which is no launch
- **THEN** the write is refused naming request 9

#### Scenario: A bolt's own launch
- **WHEN** a bolt's start appends a launch of `bolt/x` of the kind `crew/bolt` on the base `main`, with no brief and no launch to land first
- **THEN** it is appended; had it named a brief, a launch to land first, another kind or another base, the write would be refused naming the field

#### Scenario: A fix on a bolt with no launch of its own
- **WHEN** a write would append a fix's launch on the base `bolt/x`, and `requests.rec` holds `x`'s units' launches and no launch of `bolt/x`
- **THEN** it is appended

#### Scenario: A land of a unit
- **WHEN** a land would name request 4, the launch of unit `a` on `bolt/x`
- **THEN** the write is refused naming request 4, since a land names a bolt's or a fix of main's launch

### Requirement: What comes before a runner takes a kit's work is done on the main-level host
Some of what crew does on a kit comes before any runner has taken the work in hand:
- a new unit's or chore's name, checked against the kit's main;
- a bolt never started, landed by its close alone;
- the design agent's records, and a proposal's records, read in the kit;
- the board's explorations on the kit's main;
- the main level's folders of the partition's kits.

That work SHALL be done in the checkout the partition's main-level host keeps of the kit, found by the kit's forge address or, for a kit the plan names by its name alone, by that name. Where the main-level host is the host crew runs on and its teams file names the repository among its `repositories`, the kit's checkout SHALL be that entry's `checkout` and its folder that entry's `dir`, whether or not a session's space lists the repository. Otherwise they SHALL be the checkout and folder that host's spaces in the hosts file keep, `<session dir>/<name>/main` and `<session dir>/<name>`. Nothing SHALL be asked of a runner for it. It SHALL be refused, naming the host and the kit, where that host keeps none or keeps two repositories by the kit's name, counting those its teams file names with those its spaces keep. A refusal for a kit the host keeps none of SHALL also name `crew kit rename <kit> <new>` as the way on for a kit renamed on its host.

A bolt's start SHALL be none of that work: it SHALL read no host's checkout, make no branch and run nothing on any host, and SHALL read neither the kit's policy nor any host's sluice, the bolt's base place and its pieces asked of the runner by requests on the drive's branch alone (record 0056 point 2).

#### Scenario: A kit's first bolt is started
- **WHEN** `crew bolt start x` runs for crew's first bolt, no runner has taken any of crew's work, and deneb, madswan's main-level host, keeps `afterthought/crew` at `/d/madswan/crew/main`
- **THEN** `requests.rec` gains `x`'s base place's launch and then its pieces' launches, no branch is made, and nothing is read or run in `/d/madswan/crew/main` or anywhere on deneb

#### Scenario: A start where the main-level host keeps no checkout of the kit
- **WHEN** `crew bolt start x` runs and deneb's spaces keep no checkout of crew
- **THEN** the start is not refused for it, and `x`'s launches are appended as for any start

#### Scenario: A kit the main-level host keeps no checkout of
- **WHEN** the planner adds unit `a` to crew and deneb's spaces keep no checkout of crew
- **THEN** it is refused naming deneb and crew, and the plan is unchanged

#### Scenario: A kit renamed on its host before the plan
- **WHEN** deneb's spaces keep `agentplot/timber` and nothing by `tailrace`, and the planner adds unit `a` to `tailrace`, with no rename
- **THEN** it is refused naming deneb, `tailrace` and `crew kit rename tailrace <new>`, and nothing is written

#### Scenario: A unit's name and a record
- **WHEN** the planner adds unit `a` to crew and the design agent runs `crew record crew 53 --proposed`
- **THEN** `a`'s name is checked against crew's main, and record 0053 read, in `/d/madswan/crew/main` on deneb

#### Scenario: The main level's kit folders
- **WHEN** madswan's plan names crew and sluice, deneb keeps both and a role of madswan's main level starts there
- **THEN** it may reach deneb's checkouts of crew and sluice, and a kit its plan names that deneb keeps none of is left out

#### Scenario: A kit in the runner's copy
- **WHEN** crew runs on deneb, madswan's main-level host, and deneb's teams file names `agentplot/crew` with `dir` `/r/agentplot/crew` and `checkout` `/v/agentplot/crew`, while a session's space also keeps `agentplot/crew` at `/d/agentplot`
- **THEN** crew is read and acted on before any runner takes its work in `/v/agentplot/crew`, its folder `/r/agentplot/crew`, by the name `crew` or the address `agentplot/crew`, and a role of madswan's main level may reach `/v/agentplot/crew`

#### Scenario: A repository the file names and no space keeps
- **WHEN** crew runs on deneb, deneb's teams file names `agentplot/weir`, and no session's space on deneb keeps it
- **THEN** weir is a kit deneb keeps, at the file's `checkout` and `dir`

#### Scenario: Another host's kit
- **WHEN** crew runs on deneb, its teams file names `WilldanGroup/atlas-kit`, and wldn's main level runs on chuck-herdr-alpha, whose spaces keep atlas-kit at `/workspace`
- **THEN** wldn's atlas-kit is read in `/workspace/atlas-kit/main` on chuck-herdr-alpha, since deneb's file names deneb's repositories alone

#### Scenario: One name, two repositories
- **WHEN** crew runs on deneb, its teams file names `agentplot/blueprints`, and a session's space on deneb keeps `afterthought/blueprints`
- **THEN** a kit named `blueprints` alone is refused naming both, and `agentplot/blueprints` is the file's checkout
