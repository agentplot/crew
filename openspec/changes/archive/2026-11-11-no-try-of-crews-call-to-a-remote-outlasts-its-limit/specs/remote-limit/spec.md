## Purpose
How crew bounds each try of its calls to a remote, so a remote that takes a call and never answers holds no crew command, and no agent's shell behind it, past the family's limit (agentplot/blueprints `design/weir/requirements.md` 69 and C.3; sluice record 0109; `weir-bounded`): a try runs in a process group of its own and is ended with everything it started; its limit and grace are the family's, set by nothing of crew's; a stopped try is named in the family's words; the state repository's fetch, listing and push, and a kit's fetch of its origin, are such tries; and every local git call runs to its end.

## ADDED Requirements

### Requirement: A try runs to its limit in a process group of its own
crew SHALL run each try of a call to a remote in a process group of its own and wait no longer than its limit. A try SHALL have ended once its leader has exited and no process of its group is left. At the limit its group SHALL be asked to end, given the grace, then killed, so nothing it started outlives it, and the try SHALL be said stopped (weir 69, C.3; weir-bounded).

#### Scenario: A process that never ends is ended with its group
- **WHEN** a command prints `begun` on standard output and `said` on standard error, starts a `sleep 60` in the background, then sleeps sixty seconds itself, and is tried to a limit of 300 ms
- **THEN** it is said stopped well inside the sixty seconds, its standard output is `begun` and its standard error `said`, and the background sleep is gone soon after the try returns

#### Scenario: A process asked to end says so in its grace
- **WHEN** a command that prints `asked` and exits on being asked to end sleeps sixty seconds, and is tried to a limit of 300 ms
- **THEN** it is said stopped, and its standard output is `asked`

#### Scenario: A process that will not end is killed
- **WHEN** a command that ignores being asked to end loops for ever, and is tried to a limit of 300 ms
- **THEN** it is said stopped no sooner than the grace after the limit, and well inside the sixty seconds

#### Scenario: A child that outlives its leader is ended at the limit
- **WHEN** a command starts a `sleep 60` in the background with its output sent elsewhere, prints the sleep's process id, and exits 0 at once, and is tried to a limit of 300 ms
- **THEN** it is said stopped, its exit is 0, and the background sleep is gone soon after the try returns

### Requirement: A try that ends within its limit gives its exit and all it printed
A try that ends within its limit SHALL give its exit and everything it printed on each of standard output and standard error, and SHALL not be said stopped. Its standard input SHALL be what its caller gives it.

#### Scenario: A process that ends gives its exit and all it printed
- **WHEN** a command prints `out` on standard output and `err` on standard error and exits 3, tried to a limit of ten seconds
- **THEN** it is not said stopped, its exit is 3, and its standard output and error are `out` and `err`, each with its newline

#### Scenario: The input the caller gives is read
- **WHEN** `cat` is tried to a limit of ten seconds with `asked` as its input
- **THEN** its standard output is `asked`, and it is not said stopped

### Requirement: The limit and the grace are the family's
crew's limit for a try SHALL be thirty seconds and its grace two seconds, agentplot/sluice record 0109's, as `weir-bounded`'s `TRY_FOR` and `GRACE`. Python SHALL read them from `gather.py`, and bash SHALL take them as filled from there. No setting of crew's, environment variable or file SHALL set either (weir C.3).

#### Scenario: The limit and grace are the family's
- **WHEN** `gather.TRY_FOR` and `gather.GRACE` are read
- **THEN** they are thirty seconds and two seconds

#### Scenario: The bash try takes gather's limit and grace
- **WHEN** `plan.FETCH`'s text is read
- **THEN** it sets its limit to 30000 ms and its grace to 2000 ms, once each, and reads neither from anything else

#### Scenario: No setting reaches the limit
- **WHEN** the source of `gather.tried`, `gather.stopped` and `plan.FETCH` is read
- **THEN** none of them reads an environment variable, a file or the teams file

### Requirement: A stopped try is named with its call, its remote and its limit
A stopped try SHALL fail with git's last line on standard error and `; `, where git wrote one, then `<call> with <remote> was still going after <limit>, the most a try may take, and was stopped`. The limit SHALL be whole seconds as `30s` and else milliseconds as `300ms`. Its standard output SHALL never be read as an answer (weir C.3).

#### Scenario: A stopped try's words
- **WHEN** `gather.stopped` is given `git fetch`, `origin` and thirty seconds, and git wrote nothing on standard error
- **THEN** it gives `git fetch with origin was still going after 30s, the most a try may take, and was stopped`

#### Scenario: A stopped try's failure follows git's last line
- **WHEN** a stopped try's git wrote two lines on standard error, the last `fatal: x`
- **THEN** its failure is `fatal: x; ` and then the stopped try's words

#### Scenario: A limit in seconds or milliseconds
- **WHEN** `gather.span` is given thirty seconds, and then 300 ms
- **THEN** it gives `30s`, and then `300ms`

### Requirement: The state repository's calls to its remote are tries
Each git call crew makes in its bare cache of a state repository that reaches the remote (a `fetch`, an `ls-remote` or a `push`) SHALL be one try, its remote named by its address. Every other git call crew makes there SHALL run to its end as before.

#### Scenario: A fetch, a listing and a push are tries
- **WHEN** `plan.git` is asked to `fetch`, `ls-remote` or `push`
- **THEN** each runs once as a try to `gather.TRY_FOR`, naming the address it was given

#### Scenario: A local call runs to its end
- **WHEN** `plan.git` is asked to `rev-parse`, `commit-tree` or `update-ref`
- **THEN** it runs with no limit, as before

### Requirement: A kit's fetch of its origin is a try
Every fetch crew makes of a kit's origin SHALL be one try, on the host where its git runs, its remote named `origin`. gather's fetch SHALL run through `gather.tried`, and every other kit fetch through `FETCH`'s `origin_fetch`, which tries its `git fetch` as `tried` does, with the same words. A kit's stopped fetch SHALL fail the read that asked for it, naming the stopped try.

#### Scenario: Main now on an origin that never answers
- **WHEN** `MAIN` reads a kit whose origin takes the call and never answers, its limit 300 ms
- **THEN** it says `FETCHED=` with the stopped `git fetch`'s words naming `origin` and `300ms` well inside the sixty seconds, and the call's process is gone

#### Scenario: What a tip carries on an origin that never answers
- **WHEN** `CARRIES` reads a tip in a kit whose origin never answers, its limit 300 ms
- **THEN** it says `READ=` with the stopped `git fetch`'s words, and the call's process is gone

#### Scenario: gather on an origin that never answers
- **WHEN** gather fetches a kit whose origin never answers, its limit 300 ms
- **THEN** the fetch's failure is the stopped `git fetch`'s words naming `origin` and `300ms`, and the call's process is gone

#### Scenario: Every kit fetch is gather's or origin_fetch's
- **WHEN** `plan.py` and `gather.py` are read
- **THEN** no `git fetch` is made through `kit_git`, `ran` or a script's text outside `FETCH`, and the forecasts' and a reading's fetches run `ORIGIN_FETCH` through `fetch_told`
