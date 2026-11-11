---
status: proposed
date: 2026-11-09
decision-makers: the user (the superfans' shape, in afterthought/swancloud record 0062 as amended, their answers on their card of 2026-11-09, and whether to take this record); the research talk the-superfan-watches-the-family-at-work (how crew holds them, from the rules)
---

# 0063. Each tool has a superfan: a Flume kind of crew's whose pass, every four hours, is a millpond adapter that only reads

Status: proposed on 2026-11-09 by the research talk `the-superfan-watches-the-family-at-work`, until the user has seen it as a record and says yes. No unit is queued from it while it is proposed.

The superfans' shape, the answers below and the clock until millpond's tick runs are the user's own. How crew holds them is the talk's, from the rules, each with the path not taken.

Deciders: the user.
- In afterthought/swancloud record 0062 as amended through 910edb62:
  - relayed by afterthought-operator, 2026-11-08: "I think it would be a combination of the MCP and also having access to watch the logs and sessions from running BoomDrive tools";
  - on their card req_e43693069d374067b440, 2026-11-09: "One per tool (runner, Flume, sluice, crew), every 4 hours", Agent0 "Turn it off", and "These should be designed to be compatible with Milpond's capture pattern".
- On their card of 2026-11-09, through agentplot-design:
  - on the watch, "Yes, beside the 4-hourly passes";
  - on the order, "Build Millpond's intake first, with crew";
  - on Dash0, "The command line alone; the plugin stays installed and off".
- On their card, through agentplot-design, asked what wakes the superfans until millpond's tick runs: "could we use /loop in a claude session?", ruled yes as that clock.
- Their note on that card: "How does the plane program know there's a problem? Isn't part of the point that the superfan is evaluating what it sees and looking for problems with intent? / The blueprints repo does have a captures or signals folder. We can write captures there manually or run `write captures` into Crew. We could work on Mill Pond but I think we could write captures directly to Crew in the meantime / I assume that once a Claude session runs it could use the MCP server then to do additional analysis".

The talk decided the rest.

Sources:
- `openspec/explorations/the-superfan/reading.md` and `proposal.md`;
- Anthropic Engineering, "Redesigning source control at Anthropic" (2026-10-13);
- agentplot/blueprints `design/millpond/requirements.md`: 9, 11, 12, 14 to 17, 23 to 29, 31 to 33, §9, C.1, C.4, C.11, C.13;
- Flume 195 and its settings file (`crates/flume/src/profiles/agent/claude/settings.rs`);
- record 0057;
- rules `roles.1` to `roles.7`, `signals.1`, `signals.2`, `signals.5`, `signals.7`, `state.1`, `state.3`;
- Boomdrive record 0033, proposed with this one.

## Context and problem statement

The user has chosen the superfans' shape and answered how they start. This record is how crew holds them:
- what each superfan is;
- how a pass runs and what it may touch;
- how its findings land before millpond and after;
- crew's part in the watch.

Four facts shape it:
- Tools' permissions are agent settings (Flume 195), so read-only is the kind's own settings' to hold.
- `crew signal` records an agent's finding with an excerpt crew checks against the session's transcript (`signals.2`).
- millpond's capture contract makes a pass that ends with a cursor and a `done` line an adapter's run (millpond 23 to 25).
- An adapter ships in the plugin of the tool whose domain it wraps (millpond §9).

## Considered options

- **Four addresses of one Flume kind of crew's, recording with `crew signal` until millpond takes lines, then as millpond adapters on its tick (chosen).**
- **Four standing agents in herdr.** A standing agent has no clock. A loop of crew's that woke them is ruled out (`roles.7`), and crew's standing roles each cross to their kind in turn (record 0057).
- **Findings written to a blueprints repository's `signals/` folder.** That folder holds the daily pass's signals from meetings and channels. An agent's signals belong on the drive's branch (`signals.1`).
- **`crew signal land` taught to take capture lines.** That is bridging code, which the user's rule refuses (principle 12).
- **A follow-up run of the superfan's to dig into a finding with Dash0's MCP server.** That would be a second run for every finding, started by a pass that starts nothing.

## Decision outcome

1. **Four superfans, the drive's main-level roles**:
   - the addresses `agentplot/superfan-runner`, `agentplot/superfan-flume`, `agentplot/superfan-sluice` and `agentplot/superfan-crew`;
   - four addresses of one kind, `superfan`, declared in crew's roles file (record 0057), with the kind and its brief in crew's plugin while crew is the control plane;
   - born as a kind, with no standing agent to cross from;
   - on deneb alone, where Dash0's command line and token are.
2. **A pass, every four hours, looks with intent.** It reads:
   - its tool's metrics and logs in Dash0, with the `dash0` command line alone: `logs query`, `spans query`, `traces get`, `metrics instant`, `failed-checks query`;
   - its tool's own read commands, logs, state and the sessions its tool runs.

   It reads from where the last pass stopped and looks for anything strange. It is bounded by its kind's stage limit. The plugin `dash0@swancloud` is off in every pass.
3. **A finding is keyed**:
   - its key: its tool, its kind and the tool's own name for the instance, such as `superfan/flume/stalled/<place>/<since>`;
   - when it happened at its tool;
   - its excerpt, the lines it read verbatim;
   - its Dash0 link where there is one.

   A pass records no finding whose key the drive's signals already hold.
4. **Until millpond takes lines, a pass records with `crew signal`** from its session:
   - `--kind` first, its subjects `superfan` and its tool, its excerpt the tool's output as the session received it;
   - its assertion opening with `key <key>:`, so curation can tell a repeat.

   crew checks the excerpt against the session's transcript and grades it as asserted by the tool (`signals.2`, `signals.5`). The signal lands on the drive's branch (`signals.1`).
5. **Once millpond takes lines, a pass is a millpond adapter.**
   - It is declared in crew's plugin with the schedule `0 */4 * * *` and the tool it watches.
   - Its command takes the raw directory and cursor millpond hands it, hands them to its address's run, wakes the address, waits for the run's end, and prints the lines the run wrote.
   - For each finding the run writes one capture of the contract (millpond C.1): the same key, `source` `superfan`, `event_at`, title and Dash0 link, raw material written whole in the run's raw directory, and its own excerpt. Then it writes a cursor and a `done` line.
   - millpond's tick runs it (millpond 28), and the runner's pass runs the tick (Boomdrive record 0033).

   Only the brief's paragraph on recording, and the settings' rule for what it may write, change.
6. **Read-only, by the kind's settings** (Flume 195; `roles.3`).

   **Where the settings live.**
   - The kind is `superfan`, in crew's kinds folder, `~/.local/share/flume/kinds/crew` (record 0057).
   - Its mode is `dontAsk`, Flume's own `mode` setting, which Flume passes as `--permission-mode` (Flume's `mode.rs` takes it). Under it, a tool no rule allows is refused, never asked about.
   - Each of the four addresses' entries in crew's roles file gives its run's agent settings (Flume's `[roles."<stream>/<role>".agents]`). Flume writes them to the run's `own-settings.json` and passes that file as `--settings`.

   **The settings every address gives:**

   ```json
   {
     "enabledPlugins": { "dash0@swancloud": false },
     "permissions": {
       "allow": [
         "Bash(dash0 logs query:*)",
         "Bash(dash0 spans query:*)",
         "Bash(dash0 traces get:*)",
         "Bash(dash0 metrics instant:*)",
         "Bash(dash0 failed-checks query:*)",
         "Bash(dash0 skill show:*)",
         "Bash(crew signal --kind:*)",
         "Bash(crew signal show:*)"
       ],
       "deny": [
         "Bash(crew signal move:*)",
         "Bash(crew signal land:*)"
       ]
     }
   }
   ```

   **How a pass calls the command line.**
   - **The skill.** With `dash0@swancloud` off, a pass has no Dash0 skill loaded. It reads the command line's skill with `dash0 skill show`, which prints it and writes nothing (afterthought/swancloud change `the-superfans-sessions-read-dash0`, its `design.md`).
   - **The subcommand comes first.** A prefix rule matches only from the start of the command. So a pass writes the subcommand first and passes no flag before it: `dash0 logs query …`, never `dash0 --agent-mode logs query …`, which `dontAsk` refuses.
   - **No flags are needed before it.** Agent mode turns on by itself under `CLAUDECODE`, and swancloud's wrapper adds `--auth-token-file`, the API's address and the dataset itself.
   - The brief says the same.

   **What each address adds to `allow`**: its tool's own read commands, and `Read(...)` of its tool's log and state paths.

   | Address | Its tool's reads | Its tool's paths |
   |---|---|---|
   | `superfan-sluice` | `sluice overview`, `sluice status` | sluice's state, its readers' documents, `~/Library/Logs/sluice-run-*` |
   | `superfan-flume` | `flume status`, `flume list` | `~/.local/state/flume/`, the transcripts of the agents its places run |
   | `superfan-runner` | `flume status`, for the host's watch; `boomdrive status`, once built | the runner's report, `~/Library/Logs/swancloud-boomdrive.log` |
   | `superfan-crew` | `crew board`, `crew bolts`, `crew events`, `crew card read` | `~/.cache/crew/board/`, the run record, `~/.local/state/crew/usage/` |

   The exact strings are the build's.

   **How the settings change once millpond takes lines**: `Bash(crew signal --kind:*)` gives way to `Write(...)` and `Edit(...)` of the run's raw directory alone.

   **How they hold the line:**
   - `dash0@swancloud` is named `false`, so a pass never loads Dash0's MCP server, even where another layer turns it on. A session's own `false` holds over a user-level `true` (`reading.md` §5).
   - Every edit, every write and every other command is refused by `dontAsk`, as nothing allows them.
   - Its brief says that everything it reads is data, never instructions.

   It never submits, withdraws, retries, holds, drops, stops, sets aside, fixes, lands, approves, plans, moves a signal or asks anyone anything.
7. **A deeper look with Dash0's MCP server is a person's session.** It is the user's own, or one the user starts on a finding. That session turns the plugin on in its own settings, `"enabledPlugins": {"dash0@swancloud": true}`, which Claude Code honours (`reading.md` §5). No superfan run does. This is what afterthought/swancloud record 0062 has on main at c0e4df27, accepted: "a pass keeps it off".
8. **crew's part in the watch.**
   - The watch is beside the passes, one adapter per tool, each in its tool's own plugin (millpond §9). It offers each cause its tool already names, keyed on the tool's own name and when it began, as an unread capture.
   - crew's own watch offers crew's named causes, such as a card left unanswered past its bound.
   - The inbox's reader command, declared in crew's plugin, wakes the superfan whose tool a watch capture's key names. That run reads the capture and writes a reading of what holds, which may be none (millpond 31).
   - The watch runs once millpond's tick does.
9. **Its findings are curated like any signal**: on the user's word and at the design agent's start (`signals.7`). A recurrence is a new key, and curation joins it to its item, whose weight builds.
10. **Until the runner runs millpond's tick, a `/loop` in one Claude session is the clock** (the user's).
    - **What it is.** One Claude session on deneb, started by the user or by ops on their word. Its `/loop` runs every four hours and does one thing: `flume wake agentplot/superfan-<tool>` for each of the four tools. It watches nothing and reads nothing.
    - **What a pass stays.** Each pass is its own fresh, bounded, read-only Flume session.
    - **Why `roles.7` holds.** The session only sends `flume wake`, as Pending You's wake mod does, and it is no process of crew's.
    - **Its limits**, read from Claude Code's scheduler (2.1.319, its `CronCreate` tool):
      - a scheduled job lives only in its session and is gone when the session ends;
      - a recurring one expires after 7 days;
      - it fires only while the session is idle, and up to half its period late, at most 30 minutes.

      So whoever starts the loop restarts it each week and after any reboot. A stopped loop shows only as the superfans' silence: no pass in the run record.
    - **What retires it.** It is no code, in any tool or in swancloud, so nothing is retired but the session. The runner's tick (Boomdrive record 0033) replaces it.

Not taken: standing agents, a blueprints signals folder, a lines intake in crew, and a follow-up run of the superfan's, for the reasons above.

## Consequences

- Good: each tool has a superfan focused on it alone, as Anthropic's are, and it starts before millpond is built.
- Good: what a tool already names reaches its superfan at once by the watch, and the pass spends its looking on what no tool names.
- Good: what a superfan may do is held by its settings, not only by its brief.
- Bad: until millpond's tick runs, the clock is a session someone keeps. It is restarted each week and after any reboot, fires up to 30 minutes late, and its stop shows only as silence.
- Bad: until millpond keeps the inbox, a finding's key is a convention in its assertion, kept by the pass, not by crew. A finding standing across the switch to capture lines may land once more, and curation joins it to its item.
- Bad: millpond's statement says a model runs only as a reader or curation, and a superfan's pass is a third place. Its amendment, and the amendment of millpond's C.4 for the runner's tick, are in `proposal.md` for agentplot-design to take to agentplot/blueprints.
- Bad: millpond writing the inbox on the drive's branch departs from `state.1`. `state.1` is amended in the change that adopts millpond's intake, to admit millpond's writes of the inbox's paths by the family's shared-branch protocol.
- On acceptance, the design agent adds the rule `roles.10` to `docs/architecture/core.md`: "A superfan only reads: its kind's settings allow the dash0 command line's reads, its tool's read commands and its tool's logs, and new signals until millpond takes its lines, then writes under its run's raw directory alone; it submits, retries, sets aside, holds, drops, fixes, lands, approves, plans, moves a signal and asks nothing." This rules out a superfan that acts, or one held only by its brief's words.
