## MODIFIED Requirements

### Requirement: crew asks a host's runner for work by requests on the drive's branch
crew SHALL write every request for a host's runner as a record of `requests.rec` on the drive's branch: a launch of a place, or a retry, drop or priority of one it launched, or a preview of a branch at a revision on the host where the work it serves runs, brought up or, marked done, put away. Each SHALL be numbered once, appended by a crew command in the commit of the plan write that occasions it, and checked by `recfix --check` and crew's own rules. A request SHALL never be removed. It SHALL never be changed, except by `crew kit rename`, which renames a repository's name in a request's `Repo` and in a fix of its main's `Work`, in the rename's one commit. Any other write that changes a request SHALL be refused.

#### Scenario: Never renumbered
- **WHEN** `requests.rec` holds requests 1 to 7 and a drop is written
- **THEN** it is request 8, and requests 1 to 7 are as they were

#### Scenario: A preview and its done
- **WHEN** `requests.rec` holds requests 1 to 7, a preview is asked from a card, and later the user is done with it
- **THEN** the preview is request 8 and its done request 9, each in a commit of its own, and requests 1 to 8 are as they were when 9 is written

#### Scenario: A rename's write changes a request's repository
- **WHEN** the user renames `flywheel-cloud` to `boomdrive-cloud` and request 3 has `Repo: flywheel-cloud`
- **THEN** the write passes crew's append check with request 3's `Repo` renamed and nothing else of it changed

#### Scenario: Any other write that changes a request
- **WHEN** a write other than a rename would change request 3's `Repo`
- **THEN** it is refused, saying a request is never changed or removed, and nothing is pushed

### Requirement: crew reads each host's runner from that runner's own branch
crew SHALL read a host's runner from `<label>/runner/<host>` of the partition's state repository, fetched with `<label>/main` in one fetch, and SHALL never write it. The branch holds five files:
- `runner.rec` says a runner serves the partition there;
- `answers.rec` says where each request stands;
- `places.rec` holds Flume's status of each place, as Flume gave it;
- `repositories.rec` holds each repository the runner keeps on its host, by its forge address with the folder of its clone;
- `previews.rec` holds what the runner answered of each preview request, by its request's number: its outcome, `held`, `done` or `refused`; sluice's answer and sluice's listing of the preview, each as the runner carried it; whether sluice's last listing held it; the runner's words; and when.

crew SHALL hold `previews.rec`'s descriptor byte for byte as the runner writes it. A `repositories.rec` or a `previews.rec` that recfix refuses, or that holds a record with no address or no request's number, or one address or one request twice, SHALL make that host's runner unreadable, as the other files do. A branch with no `repositories.rec` SHALL be read as a runner that reports no repositories, and one with no `previews.rec` as a runner that has answered no preview. A preview's answer or listing that is no JSON object crew reads SHALL mark that preview alone as unread, naming it.

#### Scenario: One fetch
- **WHEN** a command reads the plan and the runners
- **THEN** it fetches the state repository once, `<label>/main` and `<label>/runner/*` together

#### Scenario: The repositories a runner keeps
- **WHEN** `madswan/runner/deneb` holds a `repositories.rec` naming `agentplot/boomdrive-cloud` at `/r/boomdrive-cloud`
- **THEN** crew reads that deneb's runner keeps `agentplot/boomdrive-cloud` in `/r/boomdrive-cloud`

#### Scenario: A runner that reports no repositories
- **WHEN** `madswan/runner/deneb` holds no `repositories.rec`
- **THEN** deneb's runner is read as before, reporting no repositories

#### Scenario: A repositories file crew can't read
- **WHEN** deneb's `repositories.rec` names `agentplot/boomdrive-cloud` twice
- **THEN** deneb's runner can't be read, naming the file, and only the work no runner crew read has taken reads unknown

#### Scenario: A preview the runner answered
- **WHEN** `madswan/runner/deneb` holds a `previews.rec` whose `Preview` for request 12 says `Outcome: done`, `Listed: yes`, and a `Status` that is sluice's listing of the preview `up` at `web`
- **THEN** crew reads request 12's preview as brought up and up, at sluice's address for `web`

#### Scenario: A runner that has answered no preview
- **WHEN** `madswan/runner/deneb` holds no `previews.rec`
- **THEN** deneb's runner is read as before, answering no preview

#### Scenario: A previews file crew can't read
- **WHEN** deneb's `previews.rec` holds request 12 twice
- **THEN** deneb's runner can't be read, naming the file

#### Scenario: A preview's listing that is no JSON
- **WHEN** request 12's `Status` in deneb's `previews.rec` is no JSON object
- **THEN** request 12's preview reads unread, naming deneb's file, and every other answer of deneb's reads as it stands

## ADDED Requirements

### Requirement: A preview names its host, its work, its repository, its branch and its revision
A preview request SHALL name the host whose runner reported the work it serves (the requirement "A kit's work is taken by a runner whose configuration names its repository"), since only that runner brings it up; the work it serves, `bolt/<bolt>` for a landings row's bolt or `unit/<unit>` for a batch line; its repository as the plan names it; the branch and the revision; and, to put it away, `Done: yes`. It SHALL name nothing else, and `bolt/<bolt>` SHALL be the work of no other request.

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
- **WHEN** a write would append a launch serving `bolt/y`
- **THEN** it is refused by crew's rules, saying `bolt/<bolt>` is the work of a preview alone

### Requirement: A preview is read from the runner on the host it names
crew SHALL read a preview request's answer from the runner on the host it names alone: from that runner's `previews.rec`, or from its `answers.rec` where that runner refused the request there, as a runner that cannot read it does. It SHALL read as asked while that runner has answered it neither way. crew SHALL read the previews of one host, repository and revision as one, and its ask as standing while the newest preview request naming all three is a bring-up that runner has not refused.

#### Scenario: A runner before previews
- **WHEN** deneb's runner, of a release that reads no preview, answers request 12 refused in `answers.rec` with the words `its Act preview, which crew's implementation does not read`
- **THEN** crew reads request 12's preview as refused, in the runner's words

#### Scenario: Put away, then asked again
- **WHEN** request 12 asks for `bolt/y` at `abc1234` on deneb, request 13 is its done, and request 14 asks for it again
- **THEN** crew reads the ask of `abc1234` on deneb as standing at request 14
