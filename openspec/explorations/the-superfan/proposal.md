> A proposal (2026-11-09), from the research talk `the-superfan-watches-the-family-at-work`: how the family's superfans watch its tools at work and turn what they see into signals for the plan. It decides nothing. Its shape is the user's: afterthought/swancloud record 0062 as amended through 910edb62, and their answers on their card of 2026-11-09. The rest is this talk's, for the user to accept or turn down. The facts it rests on are in `reading.md` beside it. Its decisions are crew record 0063 and Boomdrive record 0033, both accepted by the user on 2026-11-11. What the user decided is in §10.

# The superfan: the proposal

## In one paragraph

There is one superfan for each tool running on deneb: the Boomdrive runner, Flume, sluice and crew.

- **The pass.** Every four hours each superfan makes a pass. It reads its tool's metrics and logs in Dash0 with the `dash0` command line, and its tool's own logs, sessions and JSON on deneb. It looks with intent for anything strange.
- **The watch.** Beside the passes runs a watch, with no model, for each tool. It knows a problem only where the tool already names one, and wakes that tool's superfan at once.
- **Read-only.** A superfan only reads. Its kind's settings allow exact read commands and nothing else.
- **Where findings go.** Each finding becomes a signal, keyed so a repeat can be told. Until millpond's intake is built, a superfan records findings straight into crew with `crew signal`. Once it is, a pass writes millpond's capture lines instead, and only where the findings go changes.
- **The clock.** millpond's tick runs the passes and the watches on their schedules, and the runner's pass runs the tick, so the host keeps one clock.
- Nothing reaches the user when nothing is found.

## 1. The pattern, and what carries over

Anthropic describes superfans in one paragraph: Claudes "obsessively focused on the health of a single component", with "access to our telemetry and logs", that "act like an experienced engineer who has nothing better to do than to refresh charts and look for anything strange", beside the team's traditional alerts (`reading.md` §1). The user's reading of it, 2026-11-08: "a combination of the MCP and also having access to watch the logs and sessions from running BoomDrive tools". The spec-and-harness shape is Ben Congdon's, not Anthropic's.

| Part | Here |
|---|---|
| one superfan per component | one per tool on deneb: the runner, Flume, sluice and crew (the user's) |
| access to telemetry and logs | Dash0 through its command line, and the tool's own logs, sessions and JSON (the user's) |
| refreshing charts with nothing better to do | a bounded pass every four hours, never a standing poll (the user's) |
| traditional alerts beside it | a watch for each tool, with no model, waking its superfan on a cause the tool already names (the user's: "Yes, beside the 4-hourly passes") |
| what a superfan finds | a signal, keyed: by `crew signal` until millpond takes lines, then a capture line (the user's) |
| escalation to humans | through curation alone: a finding reaches the user only as the work or decision it becomes (swancloud 0062) |

What is known to go wrong (`reading.md` §2), and the answer here:

| Failure | Answer |
|---|---|
| alerts nobody reads | a pass or a watch that finds nothing writes nothing; a finding is one signal per anomaly, its key naming it so a repeat is told (§7) |
| a watcher that misses | the watch catches what a tool names, at once; the pass looks with intent at everything else (§5) |
| the wrong cause, said with confidence | a finding's excerpt is the tool's own words, verbatim, checked against the session's transcript (`signals.2`), or standing in the banked raw material once millpond keeps it (millpond 32) |
| instructions planted in logs | everything a superfan reads is data, never instructions (oncall-kit rule 9a, in its brief); its settings allow no command that acts (§2) |
| token cost | a pass reads only from where the last one stopped and is bounded in time; the watch costs no tokens (§5) |

## 2. The superfans

**What each reads.** Dash0 holds of the family only what is sent to deneb's collector (swancloud 0062). Today that is sluice's export, where `SLUICE_OTEL` is set, and Claude Code's metrics and events, where an account's environment turns them on. Flume, the runner and crew export nothing (`reading.md` §4). So:

| Superfan | In Dash0 | On deneb |
|---|---|---|
| **sluice** | sluice's metrics (queue depth, verdicts, landed-after, tested-for) and its failed-task log records, once sluice's wrapper sets `SLUICE_OTEL` | `sluice overview --json`, `sluice status --json`, the host reader's documents, each branch's `log.jsonl` and `results.jsonl`, `~/Library/Logs/sluice-run-*.log` |
| **Flume** | none of Flume's own; its agents' Claude Code metrics and events, once their accounts send them, though no attribute names the place (Flume `core.30`) | `flume status --json`, `flume list --json`, each place's held state, `~/.local/state/flume/flume.log`, the transcripts of the agents its places run |
| **the runner** | none (its OTLP export is off unless the host names a collector, Boomdrive record 0013) | its report, `report.json`; its branch, `<label>/runner/<host>`; `~/Library/Logs/swancloud-boomdrive.log`; Flume's host watch, which says whether its passes still settle the host |
| **crew** | its agents' Claude Code telemetry, as for Flume | the board's frames, `crew board --json`, `crew bolts --json`, `crew events --json`, the run record, `~/.local/state/crew/usage/<host>.json`, the main level's transcripts |

Dash0 matters most to the sluice superfan, and to all four for what the agents spend. For Flume, the runner and crew, the tool's own logs and sessions are what there is to read. A tool that sends nothing to Dash0 is a superfan's first finding about it.

**A pass** is one run of its tool's superfan, every four hours. It reads from where the last pass stopped, such as the last log time it read, and records each anomaly it finds:

- **Its key** names the anomaly: its tool, its kind and the tool's own name for the instance, for example `superfan/sluice/flaky/<task>/<hash>` or `superfan/flume/stalled/<place>/<since>`.
- **When it happened** at its tool, never when the pass saw it.
- **Its excerpt** is the lines it read, verbatim: a tool's output, or Dash0's answer to a query.
- **Its Dash0 link**, where there is one.

How a pass records them is §3's. A pass that finds nothing records nothing.

**How it reads Dash0: the command line alone** (the user's: "The command line alone; the plugin stays installed and off").
- The `dash0` command line runs in agent mode and reads the read-only token with `--auth-token-file` (swancloud 0062).
- Its read commands, all JSON, cover what a pass reads: `dash0 logs query`, `dash0 spans query`, `dash0 traces get`, `dash0 metrics instant` and `dash0 failed-checks query` (`reading.md` §5).
- The plugin `dash0@swancloud`, which holds Dash0's MCP server, stays installed on deneb and off in every pass. The kind's settings name it `false`, which holds over any other layer that turns it on (`reading.md` §5).

**A session that digs further into a finding may turn the plugin on**, in its own settings, `"enabledPlugins": {"dash0@swancloud": true}`. A session's own settings were shown to turn such a plugin on, with its MCP server (`reading.md` §5). The user's note: "I assume that once a Claude session runs it could use the MCP server then to do additional analysis".
- **That session is a person's.** It is the user's own, or one the user starts on a finding. It is not a follow-up of the superfan's.
- The superfan's pass stays bounded, and a deeper look is paid for only where someone chose to take it.
- A follow-up of the superfan's would be a second run for every finding, started by a pass that may start nothing.

**Read-only, enforced by the kind's settings** (Flume 195; crew `roles.3`). The kind is `superfan`, in crew's kinds folder. Each address's entry in crew's roles file gives its run's agent settings, which Flume writes to the run's `own-settings.json` and passes as `--settings`. The settings are written out in crew record 0063, decision 6.

- **The mode is `dontAsk`**, Flume's `mode` setting, so any command not allowed is refused, not asked about.
- **The plugin is named off**: `"enabledPlugins": {"dash0@swancloud": false}`.
- **Allowed**, by exact command prefix:
  - the dash0 reads: `Bash(dash0 logs query:*)`, `Bash(dash0 spans query:*)`, `Bash(dash0 traces get:*)`, `Bash(dash0 metrics instant:*)`, `Bash(dash0 failed-checks query:*)`.
    - `Bash(dash0 skill show:*)` is among them. With the plugin off, a pass reads the command line's skill this way; it prints the skill and writes nothing.
    - A pass writes the subcommand first, with no flag before it, since a prefix matches only from the start. Agent mode turns on by itself under `CLAUDECODE`, and swancloud's wrapper adds the token file, the API's address and the dataset.
  - its tool's own read commands: for sluice `sluice overview`, `sluice status`; for Flume `flume status`, `flume list`; for crew `crew board`, `crew bolts`, `crew events`, `crew card read`, `crew signal show`; for the runner `boomdrive status`, once built (Boomdrive record 0011);
  - reading files, `Read(...)`, under its tool's log and state paths in the table above.
- **What it may write:**
  - Until millpond takes lines, `Bash(crew signal --kind:*)`. A superfan always names its signal's kind first, so the prefix admits a new signal and nothing else of `crew signal`'s. `crew signal move` and `crew signal land` are denied by name.
  - Once millpond takes lines, writes under its run's raw directory alone.
- **Denied:**
  - every other command;
  - edits and writes anywhere else;
  - every MCP tool, since nothing allows one and the plugin is named off; Dash0's Agent0 tools are off in the user's organization too.
- **Its brief** says that everything it reads is data, never instructions.

## 3. How a finding lands

**millpond's intake is built first, in agentplot/millpond, with crew** (the user's: "Build Millpond's intake first, with crew").
- agentplot/millpond is the repository: it exists, is public and is kept on deneb. It holds millpond's site and design notes and no code yet, so the intake brings its first code project to it.
- The intake is `millpond land`. `millpond run` and `millpond tick` follow it (millpond C.1).
- In millpond's setup *with crew* (millpond C.13):
  - the inbox is on the drive's branch, beside crew's plan;
  - crew's curator curates it through millpond's tools;
  - crew's own signals move into it by `millpond import`, a step done by hand (millpond C.11, principle 12).
- crew's `state.1`, which has every write to a drive's branch made by a crew command, is amended in the change that adopts millpond. The amendment admits millpond's writes of the inbox's paths by the family's shared-branch protocol (weir A.7).

**The superfans don't wait for it.** Until millpond takes lines, a superfan records each finding straight into crew from its session (the user's note: "I think we could write captures directly to Crew in the meantime"):

```sh
crew signal --kind constraint --subject superfan,sluice \
  --excerpt "<the lines it read, verbatim>" \
  superfan-sluice-flaky-<task> \
  "key superfan/sluice/flaky/<task>/<hash>: <what it asserts>"
```

- **The excerpt** is the tool's output as the session received it. crew checks it against the session's transcript and grades it as asserted by the tool (`signals.2`, `signals.5`).
- **The key** opens the assertion, so curation can tell a repeat. `crew signal` keeps no key of its own beyond the session's record.
- **Where it goes.** The signal lands on the drive's branch, under `signals/`. It never goes in a blueprints repository, whose `signals/` holds the daily pass's signals from meetings and channels (`signals.1`).

**Once millpond takes lines**, a pass writes the capture contract instead (millpond C.1), as millpond's adapter:
- for each anomaly, one `capture`, with:
  - the same `key`, so two passes that see it land it once (9, 11);
  - `source` `superfan`;
  - `event_at`;
  - its `title` and Dash0 `url`;
  - its `raw` material, the tool output and Dash0 answers it read, written whole in the run's raw directory and banked off git (14 to 16);
  - its own `excerpt`, which becomes its signal (17);
- then a `cursor`, where the next pass reads from (25), and a `done` line (23).

Only where findings go changes: its brief's one paragraph on recording, and its settings' one write rule. A finding still standing across the change may land once more, as a capture whose key millpond has not yet held. Curation joins it to its item.

## 4. The clock

Once millpond's tick runs:
- each superfan's pass is a millpond adapter on the schedule `0 */4 * * *`;
- each tool's watch is an adapter on a schedule of its own (millpond C.4);
- `millpond tick` runs each of them when it is due (28), and a pass missed while the host slept runs once at the next tick (29).

What runs the tick is where two tools disagree:
- millpond's C.4: "One timer on a host runs `millpond tick` for each inbox there; on swancloud, a launchd agent per inbox".
- Principle 8: the runner's pass is the host's one clock, "it catches what no process is there for, time, a crash, an outcome decided elsewhere".
- The user, on the host's watch: "I'd rather it be the Boomdrive process" (Boomdrive record 0029).

Reconciled, the runner's pass runs `millpond tick`, as it runs Flume's settle. That is Boomdrive record 0033, and an amendment of millpond's C.4, written below.

**Until millpond's tick runs**, nothing built wakes a superfan every four hours:
- Flume keeps no schedule.
- crew may run no loop that wakes roles (`roles.7`).
- The runner runs no housekeeping but the settle (Boomdrive `core.13`).

**The clock for those weeks is a `/loop` in one Claude session** (the user's: "could we use /loop in a claude session?").
- **What it is.** One session on deneb, started by the user or by ops on their word. Its `/loop` runs every four hours and only sends `flume wake agentplot/superfan-<tool>` for each of the four tools. It watches and reads nothing.
- **What a pass stays.** Each pass stays its own fresh, bounded, read-only Flume session.
- **Why `roles.7` holds.** The session only sends `flume wake`, as Pending You's wake mod does, and is no process of crew's.
- **Its limits**, from Claude Code's scheduler: a job lives only in its session, a recurring one expires after 7 days, and it fires only while the session is idle and up to 30 minutes late. So whoever starts it restarts it each week and after any reboot, and a stopped loop shows only as the superfans' silence.
- **What retires it.** It is no code anywhere, so nothing is retired but the session. The runner's tick replaces it (crew record 0063, decision 10).

## 5. The watch and the pass

The user's answer: "Yes, beside the 4-hourly passes". Their note: "How does the plane program know there's a problem? Isn't part of the point that the superfan is evaluating what it sees and looking for problems with intent?"

**The two do different work.**

- **The watch knows a problem only where its tool already names one.** Each tool keeps some of its own troubles by name, with when each began:
  - sluice's standing refusals, kept once per cause and host with their count, first and last (sluice `core.28`, `core.47`);
  - a check that flaked, `failed[].flaky`;
  - a Flume place stalled, with its `waiting_on.since`;
  - a failing `boomdrive check`, once built (Boomdrive record 0011);
  - a card of crew's left unanswered past its bound.

  The watch reads those, keys each on the tool's own name for it and when it began, and wakes the tool's superfan for each one it has not offered before. It judges nothing. It is fast because the tool has already done the judging.
- **The pass looks with intent at everything else.** It reads what no tool names: a queue that has crept, a run of slow candidates, a log line that never used to appear, an agent spending more than its kind usually does. Deciding whether it is a problem is the superfan's.
- **Neither stands alone.** A superfan is never the only detector of what a tool already names: the watch catches that within its schedule. And the watch never decides what a tool has not named.

**A watch is an adapter of its tool's, with no model**:
- shipped in its tool's own plugin, as "an adapter ships inside millpond when its source needs no other tool, and otherwise in a plugin of the tool whose domain it wraps" (millpond §9);
- one for each of sluice, Flume, the runner and crew;
- printing the capture contract, each standing cause as one capture with raw material and no own excerpt.

Such a capture is *unread* (millpond 17). The tick starts the inbox's reader for it (millpond 33). The reader's command, declared in crew's plugin, wakes the superfan whose tool the capture's key names. That run reads the capture and writes a reading of what holds, which may be no signal at all (millpond 31). A cause that is no problem then never reaches curation.

**The watch runs once millpond's tick does.** It needs the intake to take its lines, and a tick to run it. Until then the four-hourly passes are the superfans' whole watch.

**What it costs.** Estimated for the four tools, from the sizes measured on deneb (`reading.md` §4), at 60–150k tokens a pass: some 1.4–3.6M tokens a day for the passes, plus 60–150k for each run a new standing cause wakes. The watch costs none. The first week's passes measure it.

## 6. What a superfan may act on

**It only reads, and records its findings** (§2, §3). It never:
- submits, withdraws, retries, holds, drops or stops a place;
- sets aside a result (sluice: "the operator's to do, never a session's");
- launches a fix (`state.3`);
- writes the plan (`roles.1`: crew refuses any agent outside the role table);
- moves a signal;
- approves or lands anything (`roles.2`);
- asks the user anything ("only the design agent, the planner and ops ask", swancloud 0062).

**Where the line may move later**, each by its own record and the user's word:
1. A notice to ops, by ops's address, for a finding that cannot wait for curation, such as main red or a host's watch lapsed. Today such a finding waits for curation like any other.
2. A superfan drafting check rules for Dash0 as code, which the keeper applies, once there are rules to watch.
3. An inquiry, a sounding, proposed for an item whose weight keeps building.

It never gains landing, retrying, setting aside, deploying or fixing. Those are roles' acts on the user's word (`roles.2`), and a reader of untrusted text that can also act is the lethal trifecta (`reading.md` §2).

## 7. How what it sees reaches the plan without flooding it

- **One finding for each anomaly.** The key is built from the tool's own identity of the instance and when it began.
  - Until millpond, it opens the signal's assertion. Before it records, a pass looks for the key among the drive's signals, read from the drive's branch, and records none whose key a signal already holds. `crew signal show` takes an id, so how the pass reads them is the build's to settle: a listing of crew's, or the branch in crew's cache, allowed by exact prefix like any read.
  - Once millpond keeps the inbox, it is the capture's key, and the inbox holds each key once (millpond 9, 11).
- **A recurrence is a new finding, and its weight builds on the item.** When an anomaly clears and returns, its time is new, so its key is new, and it lands once more. Curation joins it to the item the first went to. An item's weight is "how many signals it holds, from which sources, over what span of event times" (millpond's *weight*). A test that flakes every week reads as one item of growing weight.
- **Curation as today**: on the user's word and at the design agent's start, over the signals with no move (`signals.7`). No superfan curates.
- **A silent superfan is shown, never read as health.**
  - Once millpond runs it, every run leaves its status (millpond 26). `millpond status --json` gives it, and crew's rail shows a superfan whose last complete pass is older than twice its schedule as lapsed, a reading of crew's (`roles.5`).
  - Until then, the run record shows each pass's run. "A missing signal is never a green signal" (oncall-kit rule 18).

## 8. Where it lives

| Option | What it would cost |
|---|---|
| **Four addresses of a Flume kind of crew's; their passes and the tools' watches adapters on millpond's tick; the tick on the runner's pass (recommended)** | millpond's intake and tick, built first (§3); Boomdrive's `core.13` amended for the tick (record 0033); a watch adapter in each tool's plugin; millpond's statement amended twice (below) |
| **Four standing agents in herdr** | four standing sessions with no clock of their own; crew may run no loop that wakes roles (`roles.7`), and crew's standing roles each cross to their kind in turn (record 0057) |
| **One watch of every tool, in Boomdrive** | one program knowing four tools' causes, where each tool knows its own; millpond §9 has a tool ship the adapters of its own domain |
| **The hosted control plane, later** | it would see a fleet's runners by the protocol (Boomdrive record 0013) and could keep the superfans of many hosts; it needs the host's first, and its commercial side is in agentplot/strategy |

- **The superfans are the drive's main-level roles**: `agentplot/superfan-runner`, `agentplot/superfan-flume`, `agentplot/superfan-sluice` and `agentplot/superfan-crew`.
  - The tools are Agent Plot's, and "a finding about a tool's own defect goes to Agent Plot" (swancloud 0062).
  - They are four addresses of one kind, `superfan`, born as a kind with no standing agent to cross from.
  - Each address is declared in crew's roles file (record 0057). The kind and its brief are in crew's plugin while crew is the control plane.
- **Each superfan's pass**, once millpond runs it, is an adapter declared in crew's plugin beside the kind, with the schedule `0 */4 * * *` and the tool it watches. Its command:
  - takes the run's raw directory and cursor as millpond hands them (millpond C.1, *run*);
  - hands them to the run;
  - wakes its address and waits for the run's end;
  - prints the lines the run wrote.

  How it hands them over is the build's to settle.
- **Each tool's watch** is an adapter in that tool's own plugin (§5). The runner's is Boomdrive's (record 0033) and crew's is crew's (record 0063). sluice's and Flume's are each that tool's, by records of their own in agentplot/sluice and agentplot/flume.
- **Bounded**: a pass is one run of its kind, bounded in time by the kind's stage limit. It reads only from where the last one stopped.
- **On deneb alone**, where Dash0's command line and token are (swancloud 0062).

Where the design and the build go:

| Piece | Built in |
|---|---|
| **crew record 0063**: the roles, the kind, its settings, the recording before and after millpond, the passes' adapters, crew's watch, the reader's command | agentplot/crew |
| **Boomdrive record 0033**: the runner's pass runs millpond's tick; the runner's own watch. Amends Boomdrive `core.13` | agentplot/boomdrive |
| **millpond's intake, run and tick** | agentplot/millpond |
| **sluice's and Flume's watches** | agentplot/sluice and agentplot/flume, each by its own record |
| **two amendments of millpond's statement** (below), which agentplot-design takes once accepted | agentplot/blueprints |
| **what is commercial**: `commercial/the-superfan.md`, never here | agentplot/strategy |

## 9. The steps

1. **The superfans**, recording with `crew signal` (crew record 0063): their kind, brief, settings and four addresses, woken every four hours by a `/loop` session (§4).
2. **millpond's intake**, `land`, in agentplot/millpond, in the setup *with crew*, with crew's `state.1` amended for the inbox's writes. Then `run` and `tick`.
3. **The runner's pass runs the tick** (Boomdrive record 0033). The passes become adapters on it, writing capture lines.
4. **The watches**: each tool's adapter, and crew's reader command that wakes the tool's superfan.
5. **The line moves** (§6), each on its own record.

## 10. What the user decides

**The design is taken.** The user accepted crew record 0063 and Boomdrive record 0033 on their card of 2026-11-11, "Make the superfan plan official: a read-only Claude session per tool every 4 hours, reporting what it finds?", answering "Approved". Crew's rule `roles.10` holds the superfan to reading. The two amendments of millpond's statement below go to agentplot/blueprints by agentplot-design.

## Proposed amendments to millpond's statement

For agentplot-design to take to agentplot/blueprints `design/millpond/requirements.md` once the user accepts them.

**C.4, the clock.** In place of "One timer on a host runs `millpond tick` for each inbox there; on swancloud, a launchd agent per inbox.":

> On a host that keeps the runner, the runner's pass runs `millpond tick` for each inbox there, once a pass and awaited, as it runs Flume's settle (Boomdrive record 0033; the family's principle 8). A host with no runner runs it on a timer of its own, one per inbox.

**§9, where a model runs, and I2.** A superfan's pass is an adapter whose session is a model. In place of "A model runs in two places only, a reader and curation, each a Claude session working through millpond's tools.":

> A model runs in three places only: a reader and curation, each a Claude session working through millpond's tools, and an adapter whose source only a session can read, such as a superfan's pass over a running tool, which speaks the capture contract as any adapter does and offers only own excerpts that stand verbatim in the raw material it banks.

And I2 reads: "No model judges anything inside millpond. A reader, curation and a session's adapter judge, outside it (70)."

## Rules this relies on, and departs from

**Relies on:**
- crew: `signals.1`, `signals.2`, `signals.5`, `signals.6`, `signals.7`, `roles.1` to `roles.7`, `state.3`, `read.1`, `code.7`;
- Flume 195 and `core.30`;
- Boomdrive `core.1`, `core.11`, `core.28`;
- sluice `core.28`, `core.47`;
- weir 3, 12, A.7, C.1;
- millpond 9, 11, 12, 14 to 17, 20, 23 to 29, 31 to 33, §9, C.1, C.4, C.11, C.13;
- the family's principles 3, 7, 8 and 12 (proposed);
- swancloud record 0062 as amended.

**Departs from:**
- Boomdrive `core.13`, which lets the runner run Flume's settle alone of its own accord. Record 0033 amends it, for the reason in §4.
- millpond C.4 and §9, amended above.
- crew `state.1`, amended in the change that adopts millpond's intake (§3).
