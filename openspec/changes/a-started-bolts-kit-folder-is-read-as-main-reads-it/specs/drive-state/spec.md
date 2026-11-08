## MODIFIED Requirements

### Requirement: A kit's work is taken by a runner whose configuration names its repository
crew SHALL record a kit's work against its repository and look up no kit's host. A runner whose configuration names the repository takes the work, under a lease and while its host's stream has room, and launches it there, in the stream its host's Flume configuration maps the repository to.

crew SHALL read a launched piece's stage from the runner whose answers hold its launch, and read it as launching while none does. Where two runners hold it, or none crew read holds it and a runner could not be read, the piece SHALL read unknown, naming them.

Where crew must act on or say where a bolt's work runs, it SHALL read what the runner reported for the work it took. This covers the bolt's landing, its reads of the bolt and its kit, its reading and preview, the sweep after a landing or a drop, its site row, and its ledger's host and stream.
- The host is the one whose runner took the newest of the bolt's launches taken. While no runner has taken any of the bolt's own work, it is the host whose runner took its kit's newest work taken.
- The kit's folder there is the one that runner's `repositories.rec` names for the kit's repository, by the name or forge address the plan gives the kit, where that runner reports its repositories. Where it reports none, the folder is the one Flume's status of that runner's newest place of the bolt's work names. Where it carries no place of the bolt's work naming one, the folder is the one its newest place of the kit's other work names, on that host alone. crew SHALL NOT refuse a runner for reporting no repositories alone.
- The stream is the one Flume's status of that runner's newest place of the work names, and none while it carries no such place.

The kit SHALL be named as unread, nothing of it landed and every other bolt read as it stands, in each of these cases:
- the runner reports no repositories and carries no place of the kit's work naming its folder. The refusal names the host and says its runner reports no repositories it keeps and carries no place of the kit's work naming its folder;
- a runner that reports its repositories names none by the kit's name. The refusal names the host, the repositories it keeps and `crew kit rename`;
- no runner has reported the bolt or the kit;
- the runner that took it reports two repositories by the kit's name, and the plan names the kit by its name alone;
- two runners took the bolt's newest launch.

#### Scenario: The runner that took the work
- **WHEN** deneb's runner answers launch 1 of crew's unit `a` on `bolt/x` and carries Flume's status of its place, naming its stream `madswan`, and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `a`'s stage is read from deneb's records, and `x` is read and landed on deneb in `/w/crew`, its ledger saying deneb and `madswan`

#### Scenario: A runner that reports no repositories
- **WHEN** deneb's runner answers launch 1 of `x`'s unit `a` and carries Flume's status of its place, naming its repository `/w/crew`, and its branch holds no `repositories.rec`
- **THEN** `x` is read and landed on deneb in `/w/crew`, as crew main reads it

#### Scenario: A runner that reports no repositories and carries no place of the kit
- **WHEN** deneb's runner answered every launch of `x` launched, carries no place of any of them nor of crew's other work, and its branch holds no `repositories.rec`, as on 2026-11-08
- **THEN** crew can't tell where `x`'s kit is kept on deneb, saying deneb's runner reports no repositories it keeps and carries no place of crew's work naming its folder, and nothing of `x` is read or landed

#### Scenario: A bolt none of whose own work is taken
- **WHEN** `x` is started and no runner has taken its launches, and deneb's runner took crew's work on another bolt and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `x` is read and landed on deneb in `/w/crew`

#### Scenario: A bolt whose every launch was refused
- **WHEN** deneb's runner refused launch 1 of `x`'s unit `a`, the base bolt already holding its change, carries no place of crew's work, and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `x` is read and landed on deneb in `/w/crew`, and `crew bolts` says where it runs; with no `repositories.rec` on deneb's branch, `x` is read in the folder deneb's place of crew's work on bolt `y` names, and were that place on chuck-herdr-alpha's runner instead, crew could not tell where `x`'s kit is kept on deneb

#### Scenario: A bolt whose places the runner no longer carries
- **WHEN** deneb's runner answered every launch of `x` launched, carries no place of any of them nor of crew's other work, and its `repositories.rec` names `afterthought/crew` at `/w/crew`
- **THEN** `x` is read and landed on deneb in `/w/crew`, and `crew bolts` says where it runs

#### Scenario: Taken by two runners
- **WHEN** deneb's and chuck-herdr-alpha's runners both answer launch 1
- **THEN** its piece reads unknown naming both, and crew can't tell where `x` runs, landing nothing of it

#### Scenario: No runner has reported the kit
- **WHEN** no runner has taken any launch of crew's work
- **THEN** a landing of `x` is refused naming that no runner has reported taking its work, and a piece of it reads launching

#### Scenario: A kit renamed under its place
- **WHEN** deneb's runner carries request 1's place, Flume's status naming its repository `/r/flywheel-cloud`, its `repositories.rec` names `agentplot/boomdrive-cloud` at `/r/boomdrive-cloud`, and the bolt's kit is `boomdrive-cloud`, as the plan gives it
- **THEN** the bolt is read and landed on deneb in `/r/boomdrive-cloud`

#### Scenario: A runner that does not keep the kit
- **WHEN** deneb's `repositories.rec` names only `agentplot/boomdrive-cloud`, and the bolt's kit is `flywheel-cloud`, as the plan gives it
- **THEN** its landing is refused naming deneb, `flywheel-cloud`, the repositories deneb's runner keeps and `crew kit rename`, and nothing is landed
