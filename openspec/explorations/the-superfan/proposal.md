> A proposal (2026-11-09), from the research talk `the-superfan-watches-the-family-at-work`: how the family's superfans watch its tools at work and turn what they see into signals for the plan. It decides nothing. Its shape is the user's, given in afterthought/swancloud record 0062 as amended through 910edb62; the rest is this talk's, for the user to accept or turn down. The facts it rests on are in `reading.md` beside it. Its decisions are crew record 0063 and Boomdrive record 0033, both proposed. What is still the user's is in §10.

# The superfan: the proposal

## In one paragraph

There is one superfan for each tool running on deneb: the Boomdrive runner, Flume, sluice and crew. Each runs every four hours. A pass reads its tool's metrics and logs in Dash0 and the tool's own logs, sessions and JSON on deneb, and looks for anything strange. It only reads. Its findings come out in millpond's capture contract: one keyed capture for each anomaly, so two passes that see the same thing land it once, then a cursor and a `done` line. A pass is therefore a millpond adapter whose source is a running tool. millpond's tick runs it on its schedule, and the tick itself runs on the runner's pass, so the host keeps one clock. Each superfan is a Flume kind of crew's, its agent's settings allowing exact read commands and nothing else. Its findings land in the drive's inbox and are curated like any signal. Nothing reaches the user when a pass finds nothing.

## 1. The pattern, and what carries over

Anthropic describes superfans in one paragraph: Claudes "obsessively focused on the health of a single component", with "access to our telemetry and logs", that "act like an experienced engineer who has nothing better to do than to refresh charts and look for anything strange", beside the team's traditional alerts (`reading.md` §1). The user's reading of it, 2026-11-08: "a combination of the MCP and also having access to watch the logs and sessions from running BoomDrive tools". The spec-and-harness shape is Ben Congdon's, not Anthropic's. Anthropic's on-call kit puts detection elsewhere: "Claude is never the detector".

| Part | Here |
|---|---|
| one superfan per component | one per tool on deneb: the runner, Flume, sluice and crew (the user's) |
| access to telemetry and logs | Dash0, and the tool's own logs, sessions and JSON (the user's) |
| refreshing charts with nothing better to do | a bounded pass every four hours, never a standing poll (the user's) |
| traditional alerts beside it | none yet in the family. A deterministic watch could detect and wake a superfan; whether it should is the user's (§5) |
| what a superfan finds | a keyed capture in millpond's contract, curated like any signal (the user's, §3, §7) |
| escalation to humans | through curation alone: a finding reaches the user only as the work or decision it becomes (swancloud 0062) |

What is known to go wrong (`reading.md` §2), and the answer here:

| Failure | Answer |
|---|---|
| alerts nobody reads | a pass that finds nothing writes nothing; a finding is one capture per anomaly, however many passes see it (millpond 9) |
| the wrong cause, said with confidence | a capture's excerpt is the tool's own words, verbatim, and its raw material is banked whole beside it (millpond 14 to 17) |
| instructions planted in logs | everything a superfan reads is data, never instructions (oncall-kit rule 9a, in its brief); its settings allow no command that acts (§2) |
| token cost | a pass reads only from its cursor onward, and is bounded in time; §5 weighs what a watch would save |

## 2. The superfans

**What each reads.** Dash0 holds of the family only what is sent to deneb's collector (swancloud 0062). Today that is sluice's export, where `SLUICE_OTEL` is set, and Claude Code's metrics and events, where an account's environment turns them on. Flume, the runner and crew export nothing (`reading.md` §4). So:

| Superfan | In Dash0 | On deneb |
|---|---|---|
| **sluice** | sluice's metrics (queue depth, verdicts, landed-after, tested-for) and its failed-task log records, once sluice's wrapper sets `SLUICE_OTEL` | `sluice overview --json`, `sluice status --json`, the host reader's documents, each branch's `log.jsonl` and `results.jsonl`, `~/Library/Logs/sluice-run-*.log` |
| **Flume** | none of Flume's own; its agents' Claude Code metrics and events, once their accounts send them, though no attribute names the place (Flume `core.30`) | `flume status --json`, `flume list --json`, each place's held state, `~/.local/state/flume/flume.log`, the transcripts of the agents its places run |
| **the runner** | none (its OTLP export is off unless the host names a collector, Boomdrive record 0013) | its report, `report.json`; its branch, `<label>/runner/<host>`; `~/Library/Logs/swancloud-boomdrive.log`; Flume's host watch, which says whether its passes still settle the host |
| **crew** | its agents' Claude Code telemetry, as for Flume | the board's frames, `crew board --json`, `crew bolts --json`, `crew events --json`, the run record, `~/.local/state/crew/usage/<host>.json`, the main level's transcripts |

Dash0 matters most to the sluice superfan, and to all four for what the agents spend. For Flume, the runner and crew, the tool's own logs and sessions are what there is to read. A tool that sends nothing to Dash0 is the superfans' first finding, and their first signals of each tool's own gaps will say so.

**A pass.** A pass is one run of its tool's superfan, every four hours. It is given its run's raw directory and the cursor the last complete pass left (millpond 20). It reads from that cursor onward and writes the capture contract's lines (millpond C.1):

- one `capture` for each anomaly:
  - `key`: its tool, the anomaly's kind and the tool's own name for the instance, for example `superfan/sluice/flaky/<task>/<hash>` or `superfan/flume/stalled/<place>/<since>`. One anomaly seen by two passes lands once (9, 11).
  - `source`: `superfan`.
  - `event_at`: when the strange thing happened at its tool, never when the pass saw it (12).
  - `title`, and `url`, the Dash0 link where there is one.
  - `raw`: what it read, the tool's output and Dash0's answer, written whole in its raw directory and banked off git (14 to 16).
  - `excerpt`: its own excerpt, the lines it read verbatim, which become the capture's one signal (17).
- a `cursor`, where the next pass reads from, such as the last log time it read (25);
- a `done` line, with how many anomalies it listed and anything it could not read (23).

A pass that finds nothing writes only its cursor and `done`.

**How it reads Dash0.** swancloud gives it two ways, both reading one read-only token from deneb's secret (swancloud 0062):
- the plugin `dash0@swancloud`, which holds Dash0's MCP server and Dash0's skills, installed on deneb and off;
- the `dash0` command line, in agent mode, with `--auth-token-file`.

Two findings:

- **A session's own settings do turn that plugin on.** Flume hands an agent its kind's settings as one file, named by `--settings` (Flume 195; `crates/flume/src/profiles/agent/claude/settings.rs`). `enabledPlugins` is not among the keys Flume reserves. Read on Claude Code 2.1.319 on deneb in a scratch configuration (`reading.md` §5): a plugin installed and off was loaded, with its MCP server, at a session's start once its `--settings` file said `"enabledPlugins": {"<plugin>": true}`. That held whether the user's settings had it `false` or did not name it, and nothing loaded without the flag.
- **The command line is enough on its own.** Its read commands, all JSON, cover what a pass reads: `dash0 logs query`, `dash0 spans query`, `dash0 traces get`, `dash0 metrics instant`, and `dash0 failed-checks query` for check rules once there are any. A command line costs a session nothing until it is used. It is allowed by exact command prefix, and the read-only token makes its asset commands fail at Dash0 as well. The MCP server adds SQL, the service catalog and the same reads again. Its tool definitions are in every superfan session's context, and it is allowed by tool name. Whether to keep it beside the command line is the user's, since the MCP server was their word (§10).

**Read-only, enforced by the kind's settings** (Flume 195; crew `roles.3`):

- The mode is `dontAsk`, so any command not allowed is refused, not asked about.
- **Allowed** by exact prefix:
  - the dash0 reads: `Bash(dash0 logs query:*)`, `Bash(dash0 spans query:*)`, `Bash(dash0 traces get:*)`, `Bash(dash0 metrics instant:*)` and `Bash(dash0 failed-checks query:*)`;
  - the tool's own read commands: `sluice overview`, `sluice status`; `flume status`, `flume list`; `crew board`, `crew bolts`, `crew events`, `crew card read`, `crew signal show`; the runner's `boomdrive status` once built (Boomdrive record 0011);
  - reading files, `Read(...)`, under the tool's log and state paths in the table above.
- **Allowed to write** under the run's raw directory alone, where its lines and raw material go. millpond gives that directory empty and keeps only what a taken capture names (millpond 16).
- **Denied:**
  - every other command, `Bash(*)`;
  - edits and writes anywhere else;
  - every MCP tool but Dash0's reads, with Dash0's Agent0 tools, `runTask` and `waitForTask`, named as well. They are also off in the user's Dash0 organization, so they are denied twice.
- Its brief says that everything it reads is data, never instructions.

## 3. How a pass's lines land

Nothing built takes the contract's lines today. crew's `crew signal land` takes a capture folder from a program with no model between (`signals.6`). It does not take lines, and teaching it to would be bridging code, which the user's rule refuses (principle 12).

The target shape is millpond's own:
- `millpond land` is the intake (millpond 27).
- `millpond run` runs an adapter with a fresh raw directory and its last cursor, lands what it prints, and keeps its cursor and status (23 to 26).
- `millpond tick` runs every adapter that is due on the host (28).
- In the setup *with crew*, the inbox is on the partition's branch in crew's state repository, beside crew's plan, and crew's curator curates it through millpond's tools (millpond C.13).
- crew's own signals move into it by `millpond import`, a step done by hand (millpond C.11, principle 12).

So the superfans need millpond's intake and tick before their findings can land. That means building millpond `land`, `run` and `tick` first, which is a change to the order of the work. The other answer of the target shape is to run the superfans by hand and keep their lines on the host, unlanded, until millpond can land them. The superfans would run, but nobody would see their findings. Which order is the user's (§10).

Writing an inbox on the drive's branch is millpond's, by the family's shared-branch protocol (weir A.7). crew's `state.1` has every write to a drive's branch made by a crew command. It needs amending to admit millpond's writes of the inbox's paths, by the same protocol: fetch the tip, apply, check, commit only its own paths, push without force. That amendment goes in crew's record of the change that adopts millpond.

## 4. The clock

The user chose every four hours. In millpond that is the superfan adapter's schedule, five-field cron, `0 */4 * * *` (millpond C.4), and `millpond tick` runs it when it is due (28). A pass missed while the host slept runs once at the next tick (29).

What runs the tick is where two tools disagree:
- millpond's C.4 has "One timer on a host runs `millpond tick` for each inbox there; on swancloud, a launchd agent per inbox".
- Principle 8 has the runner's pass as the host's one clock, "it catches what no process is there for, time, a crash, an outcome decided elsewhere".
- The user chose the runner over any other process for the host's watch: "I'd rather it be the Boomdrive process" (Boomdrive record 0029).

Reconciled, the runner's pass runs `millpond tick`, as it runs Flume's settle. That is Boomdrive record 0033, and an amendment of millpond's C.4, written below for agentplot-design to take to the statement once accepted.

## 5. The watch

The user's shape has the superfans themselves notice what is strange, on a timer. Every published shape meant for anyone but Anthropic detects deterministically and wakes the model only to read: "Claude is never the detector" (Anthropic's on-call kit), "a harness that allows the agent to write a spec of how to monitor, along with a deterministic system for running those specs, produces significantly cleaner signals with dramatically lower token usage" (Congdon).

**A watch, in this design's terms**, would be a millpond adapter of its own with no model, `source` `watch`, run by the same tick. It reads each tool's JSON against a list of checks and offers one capture for each standing cause. Each check is keyed on the tool's own name for the cause and when it began, so a cause standing for a day is one capture (`reading.md` §4: sluice's `core.47` keeps its refusals so already). Its captures carry raw material and no own excerpt, so they are *unread*, and the inbox's reader takes them (millpond 17, 33). The reader would be the tool's superfan, woken at once by the tick.

Three ways it could stand:

| Shape | Runs a day (4 tools) | Tokens a day, estimated | What it misses |
|---|---|---|---|
| **The user's: a pass every four hours, no watch** | 24 | 1.4–3.6M | up to four hours of anything, and what a pass does not think to look at |
| **The watch feeds each superfan; the four-hourly passes stay** | 24, plus a run per new cause | 1.4–4.3M | less: a named failure wakes its superfan at once, and the pass stays as the open look |
| **The watch replaces the timer; one open look a day for each tool** | 4, plus a run per new cause | 0.6–1.4M | what no check names, between open looks |

The estimates come from the sizes measured on deneb (`reading.md` §4), at 60–150k tokens a pass: a session's own floor of some 30k, and the reads from the cursor onward. They are not measurements, and the first week's passes measure them.

**This design recommends the second**, the watch feeding the superfans while the four-hourly passes stay. The passes are the user's choice. The watch adds the cheap, certain half of the pattern, so a stuck submission or a host whose runner stopped wakes its superfan at once instead of within four hours. Whether to widen the timer, toward the third shape, is a question for the first week's measured cost. The choice is the user's (§10).

## 6. What a superfan may act on

**It only reads, and writes only its pass's lines** (swancloud 0062; §2). It never:
- submits, withdraws, retries, holds, drops or stops a place;
- sets aside a result (sluice: "the operator's to do, never a session's");
- launches a fix (`state.3`);
- writes the plan (`roles.1`: crew refuses any agent outside the role table);
- approves or lands anything (`roles.2`);
- asks the user anything ("only the design agent, the planner and ops ask", swancloud 0062).

**Where the line may move later**, each by its own record and the user's word:
1. A notice to ops, by ops's address, for a finding that cannot wait for curation, such as main red or a host's watch lapsed. Today that finding waits for curation like any other.
2. A superfan drafting check rules for Dash0 as code, which the keeper applies, once there are rules to watch.
3. An inquiry, a sounding, proposed for an item whose weight keeps building.

It never gains landing, retrying, setting aside, deploying or fixing. Those are roles' acts on the user's word (`roles.2`). A reader of untrusted text that can also act is the lethal trifecta (`reading.md` §2).

## 7. How what it sees reaches the plan without flooding it

- **One capture for each anomaly.** The key is built from the tool's own identity of the instance and when it began, so the same anomaly gives the same key on every pass, and the inbox holds each key once (millpond 9, 11). A pass keeps no list of what it offered (weir 12); the key absorbs every repeat.
- **A recurrence is a new capture, and its weight builds on the item.** When an anomaly clears and returns, its time is new, so its key is new, and it lands once more. Curation joins it to the item the first went to. An item's weight is "how many signals it holds, from which sources, over what span of event times" (millpond's *weight*). A test that flakes every week reads as one item of growing weight.
- **Curation as today**: on the user's word and at the design agent's start, over the signals with no move (`signals.7`). No superfan curates.
- **A silent superfan is shown, never read as health.** Every run of an adapter leaves its status (millpond 26): when it ran, whether it was complete, and what it took, held and refused. `millpond status --json` gives each adapter's status (millpond §9). A superfan whose last complete run is older than twice its schedule reads as lapsed there. crew's rail shows that lapse for an inbox crew keeps, as a reading of crew's (`roles.5`). "A missing signal is never a green signal" (oncall-kit rule 18).

## 8. Where it lives

| Option | What it would cost |
|---|---|
| **Four Flume kinds of crew's, each pass an adapter on millpond's tick, the tick on the runner's pass (recommended)** | millpond's intake and tick, built first (§3); Boomdrive's `core.13` amended for the tick (record 0033); millpond's statement amended twice (below) |
| **Four standing agents in herdr** | four standing sessions with no clock of their own; crew may run no loop that wakes roles (`roles.7`), and crew's standing roles each cross to their kind in turn (record 0057) |
| **A timer of the host's that wakes each kind** | a second clock beside the runner's pass (principle 8), and a schedule kept outside the inbox whose adapter it is |
| **The hosted control plane, later** | it would see a fleet's runners by the protocol (Boomdrive record 0013) and could keep the superfans of many hosts; it needs the host's first, and its commercial side is in agentplot/strategy |

- **The superfans are the drive's main-level roles**: `agentplot/superfan-runner`, `agentplot/superfan-flume`, `agentplot/superfan-sluice` and `agentplot/superfan-crew`. The tools are Agent Plot's, and "a finding about a tool's own defect goes to Agent Plot" (swancloud 0062). They are four addresses of one kind, `superfan`, born as a kind with no standing agent to cross from. Each address is declared in crew's roles file (record 0057), and the kind and its brief are in crew's plugin while crew is the control plane.
- **Each superfan's adapter** is declared in crew's plugin, beside its kind, since an adapter ships in the plugin of the tool whose domain it wraps (millpond §9). Its command takes the run's raw directory and cursor as millpond hands them (millpond C.1, *run*). It hands them to the run, wakes its address, waits for the run's end, and prints the lines the run wrote. How it hands them over is the build's to settle. Its declaration names its schedule, `0 */4 * * *`, and the tool it watches.
- **Bounded**: a pass is one run of its kind, bounded in time by the kind's stage limit, and reads only from its cursor onward.
- **On deneb alone**, where Dash0's plugin and token are (swancloud 0062).

Where the design and the build go:

- **crew record 0063**, *each tool on deneb has a superfan: a Flume kind of crew's whose pass, every four hours, is a millpond adapter that only reads*. It covers the roles, the kind, its settings, the adapters and the read-only line. It is built in agentplot/crew, once millpond's intake runs.
- **Boomdrive record 0033**, *the runner's pass runs millpond's tick as it runs Flume's settle, so the host keeps one clock*. It amends Boomdrive `core.13`, and is built in agentplot/boomdrive.
- **Two amendments of millpond's statement**, below, which agentplot-design takes to agentplot/blueprints once accepted.
- **What is commercial** is in agentplot/strategy, `commercial/the-superfan.md`, never here.

## 9. The steps

1. **millpond's intake, its run and its tick**, in the setup *with crew*, with crew's `state.1` amended for the inbox's writes, if the user puts them first (§10).
2. **The runner's pass runs the tick** (Boomdrive record 0033).
3. **The superfans**: their kind, brief, settings, the four addresses and the four adapters (crew record 0063). The Dash0 plugin, command line and token are swancloud's (swancloud 0062).
4. **The watch**, if the user takes it (§5): its adapter and first checks, its captures read by the tool's superfan.
5. **The line moves** (§6), each on its own record.

## 10. What the user decides

Each goes to the user through agentplot-design, on their card.

1. **The watch**: whether a deterministic watch feeds each tool's superfan, replaces the four-hour timer, or neither (§5). Recommended: it feeds them, and the four-hourly passes stay.
2. **The order**: build millpond's intake, run and tick before the superfans, or run the superfans by hand meanwhile with their lines kept unlanded on the host (§3). Recommended: millpond's intake, run and tick first.
3. **Dash0's MCP server beside the command line** in a superfan's session, or the command line alone, or the MCP server alone (§2). Recommended: the command line alone, the plugin kept installed and off.
4. **Whether to take the design**: crew record 0063, Boomdrive record 0033 and the two amendments of millpond's statement, each proposed until the user says yes.

## Proposed amendments to millpond's statement

For agentplot-design to take to agentplot/blueprints `design/millpond/requirements.md` once the user accepts them.

**C.4, the clock.** In place of "One timer on a host runs `millpond tick` for each inbox there; on swancloud, a launchd agent per inbox.":

> On a host that keeps the runner, the runner's pass runs `millpond tick` for each inbox there, once a pass and awaited, as it runs Flume's settle (Boomdrive record 0033; the family's principle 8). A host with no runner runs it on a timer of its own, one per inbox.

**§9, where a model runs, and I2.** A superfan's pass is an adapter whose session is a model. In place of "A model runs in two places only, a reader and curation, each a Claude session working through millpond's tools.":

> A model runs in three places only: a reader and curation, each a Claude session working through millpond's tools, and an adapter whose source only a session can read, such as a superfan's pass over a running tool, which speaks the capture contract as any adapter does and offers only own excerpts that stand verbatim in the raw material it banks.

And I2 reads: "No model judges anything inside millpond. A reader, curation and a session's adapter judge, outside it (70)."

## Rules this relies on, and departs from

**Relies on:**
- crew: `signals.6`, `signals.7`, `roles.1` to `roles.7`, `state.3`, `read.1`, `code.7`;
- Flume 195 and `core.30`; Boomdrive `core.1`, `core.11`, `core.28`; sluice `core.28`, `core.47`;
- weir 3, 12, A.7, C.1; millpond 9, 11, 12, 14 to 17, 20, 23 to 29, 33, C.1, C.4, C.11, C.13;
- the family's principles 3, 7, 8 and 12 (proposed);
- swancloud record 0062 as amended.

**Departs from:**
- Boomdrive `core.13`, which lets the runner run Flume's settle alone of its own accord. Record 0033 amends it, for the reason in §4.
- millpond C.4 and §9, amended above.
- crew `state.1`, amended in the change that adopts millpond's intake (§3).
