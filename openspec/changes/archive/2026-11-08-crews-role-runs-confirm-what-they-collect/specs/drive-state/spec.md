## MODIFIED Requirements

### Requirement: crew asks a host's runner for work by requests on the drive's branch
crew SHALL write every request for a host's runner as a record of `requests.rec` on the drive's branch: a launch of a place, or a retry, drop or priority of one it launched, or a confirm, for a role's address, of ends of a place it launched, or a preview of a branch at a revision on the host where the work it serves runs, brought up or, marked done, put away. Each SHALL be numbered once, appended by a crew command in the commit of the plan write that occasions it, and checked by `recfix --check` and crew's own rules. A request SHALL never be removed. It SHALL never be changed, except by `crew kit rename`, which renames a repository's name in a request's `Repo` and in a fix of its main's `Work`, in the rename's one commit. Any other write that changes a request SHALL be refused.

#### Scenario: Never renumbered
- **WHEN** `requests.rec` holds requests 1 to 7 and a drop is written
- **THEN** it is request 8, and requests 1 to 7 are as they were

#### Scenario: A preview and its done
- **WHEN** `requests.rec` holds requests 1 to 7, a preview is asked from a card, and later the user is done with it
- **THEN** the preview is request 8 and its done request 9, each in a commit of its own, and requests 1 to 8 are as they were when 9 is written

#### Scenario: A confirm in a turn's end
- **WHEN** `requests.rec` holds requests 1 to 7, request 3 a launch of unit `a`, and the planner's run ends a turn that took two ends of `a`'s place
- **THEN** request 8 is a confirm of request 3 for `madswan/planner` with two `Delivery` lines, in the commit that ends the turn, and it passes `recfix --check`

#### Scenario: A rename's write changes a request's repository
- **WHEN** the user renames `flywheel-cloud` to `boomdrive-cloud` and request 3 has `Repo: flywheel-cloud`
- **THEN** the write passes crew's append check with request 3's `Repo` renamed and nothing else of it changed

#### Scenario: Any other write that changes a request
- **WHEN** a write other than a rename would change request 3's `Repo`
- **THEN** it is refused, saying a request is never changed or removed, and nothing is pushed

### Requirement: A launch names everything the runner passes to Flume
A launch of a kit's work SHALL name the work it serves, its repository as the plan names it, its kind, name and base, its priority, intent and recipient, and its brief, and SHALL name no host or stream, a runner whose configuration names its repository taking it, in the stream its host's Flume configuration maps the repository to; a launch of a role's work SHALL also name the host and stream its role runs in. A launch MAY name launches that must land first and a held submission. A retry, drop, priority or confirm SHALL name the launch it acts on and no host. A confirm SHALL name as its recipient the address of one of crew's five roles, `<label>/<role>`, and at least one delivery key, for the runner that holds the launch to confirm to Flume as that recipient. crew's rules SHALL refuse a request that lacks what its act needs or names what its act does not take.

#### Scenario: A launch with no stream
- **WHEN** a bolt's start appends a launch of a kit's work naming no `Stream`
- **THEN** it is appended, a runner whose configuration names the kit's repository giving its stream

#### Scenario: A kit's launch naming a host
- **WHEN** a bolt's start would append a launch naming a `Host` or a `Stream`
- **THEN** the write is refused by crew's rules and the branch is unchanged

#### Scenario: A retry of nothing
- **WHEN** a retry would name request 9, which is no launch
- **THEN** the write is refused naming request 9

#### Scenario: A confirm with no key, or for no role
- **WHEN** a confirm of request 3 would name no `Delivery`, or name `madswan/coder` as its `Recipient`
- **THEN** the write is refused by crew's rules, naming what the confirm lacks or the recipient, and the branch is unchanged
