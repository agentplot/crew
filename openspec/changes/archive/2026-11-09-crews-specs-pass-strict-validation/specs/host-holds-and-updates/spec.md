## ADDED Requirements

### Requirement: A standing agent whose brief, model, effort or folders changed is due a restart
crew SHALL record at each agent's start the crew it loaded and what it was started with, and SHALL judge whether a standing agent is due against the crew the host has installed now, which its commands run. A standing agent whose brief, model, effort or folders changed since its start SHALL be due a restart.

#### Scenario: A brief changed
- **WHEN** a landing changes the planner's brief
- **THEN** the planner is due a restart

### Requirement: A standing agent is due when the plugin it loaded is no longer the installed crew's
Where the installed crew is a checkout, an agent whose loaded part of crew's plugin changed between its start's commit and the checkout's SHALL be due, and a change to crew's code alone SHALL make none due, since every command runs crew's checkout as it is. Where the installed crew is a build, an agent whose start recorded another commit SHALL be due, since its session loaded that build's plugin folder whole and its hooks run from that folder.

#### Scenario: Code alone changed
- **WHEN** a landing changes only `plugin/lib/plan.py`, and the host's installed crew is a checkout
- **THEN** no agent is due

#### Scenario: A release is installed
- **WHEN** wldn-ops started on a build whose release names commit `1111111111111111111111111111111111111111`, and the host's installed crew is a build whose release names `2222222222222222222222222222222222222222`
- **THEN** wldn-ops is due a restart, crew's release having changed

#### Scenario: The same release
- **WHEN** wldn-ops started on the release the host's installed crew is now, its brief, model, effort and folders unchanged
- **THEN** wldn-ops is not due

### Requirement: crew makes no agent due for its plugin where it can't tell, and says why
Where the start recorded no commit, or crew can't read the installed crew, crew SHALL make no agent due for crew's plugin and SHALL say it can't tell, and why.

#### Scenario: A start that recorded no release
- **WHEN** wldn-ops's start recorded its launch and no crew commit, and its brief, model, effort and folders are unchanged
- **THEN** wldn-ops is not due, and crew says it can't tell whether its plugin changed since that start, which recorded no release of crew's

#### Scenario: The installed crew can't be read
- **WHEN** wldn-ops's start recorded a commit and crew can't read the crew the host has installed
- **THEN** wldn-ops is not due, and crew says it can't read the crew this host has installed, and why

### Requirement: A due agent is restarted once herdr reads it idle, resumed and told what changed
crew SHALL restart a due agent once herdr reads it idle with no question open and no background work of its own but crew's waits: at the end of its turn, and for one sitting idle when crew's checkout, the crew the host has installed or the teams file moves, or on `crew update`. Every standing role SHALL resume its conversation and be told what changed. Nothing SHALL be restarted on a held host.

#### Scenario: At the end of its turn
- **WHEN** the planner is due and ends its turn
- **THEN** the planner is resumed with its new brief and told the crew it now runs and what changed

#### Scenario: Running a submission
- **WHEN** swancloud-ops is due and is waiting in the background on a landing it submitted
- **THEN** it is restarted only once the submission is over and its turn ends

#### Scenario: An install moves while an agent sits idle
- **WHEN** crew's follower runs from a build, and the host's installed command's real path moves from one build to another
- **THEN** the follower's next refresh hands out the restarts the install made due, running `crew _update` through the installed command, and starts again through the installed command's `crew _follow`

### Requirement: A restart ends with its agent running, on crew as it now is or as it was
A restart SHALL end with its agent running: on crew as it now is once the agent has exited, or as it was when it could not be ended. A restart whose agent has not exited when its stop gives up SHALL watch it for ten minutes and start it the moment it exits; one whose agent still runs after that SHALL leave it running, still due, and say so.

#### Scenario: Slow to exit
- **WHEN** swancloud-ops is due and is restarted, and it is still up when the stop's `/exit` and Ctrl+C have had their time, then exits a few seconds later
- **THEN** it is resumed on crew as it now is and told what changed, and its restart's log ends "swancloud-ops is restarted on crew"

#### Scenario: Never exits
- **WHEN** swancloud-ops is due and is restarted, and it is still up ten minutes after its stop gave up
- **THEN** it is left running as it was, nothing is started in its pane, and its restart's log says it did not exit and runs on, its next turn's end handing it back

### Requirement: A later restart starts an agent an earlier restart's keys exited
A later restart that finds the agent exited by an earlier restart's keys, its pane kept and no start of it since, SHALL start it without a stop. No restart SHALL leave its agent's pane a shell with no agent in it.

#### Scenario: Exits after the restart gave up
- **WHEN** a restart of swancloud-ops gave up and left it running, and it later exits with its pane kept and nothing has started it since, and its restart is handed again
- **THEN** that restart starts it in its pane without a stop, resumed and told what changed

#### Scenario: Exited by something else
- **WHEN** swancloud-ops is due and not up, and no restart of its session gave up on it, or its main level was taken down with `crew main down`
- **THEN** the restart starts nothing and says it is not up

## REMOVED Requirements

### Requirement: An update makes a standing agent due a restart
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A standing agent whose brief, model, effort or folders changed is due a restart", "A standing agent is due when the plugin it loaded is no longer the installed crew's" and "crew makes no agent due for its plugin where it can't tell, and says why".

### Requirement: A due agent is restarted at its next stop
**Reason**: Its text was past the 500 characters `openspec validate --strict` allows a requirement; it is split into requirements that together say the same.
**Migration**: Its text and scenarios are in "A due agent is restarted once herdr reads it idle, resumed and told what changed", "A restart ends with its agent running, on crew as it now is or as it was" and "A later restart starts an agent an earlier restart's keys exited".
