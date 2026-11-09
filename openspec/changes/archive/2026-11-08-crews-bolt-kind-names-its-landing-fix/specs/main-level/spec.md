## MODIFIED Requirements

### Requirement: Main-level ops answers a landing that does not land
What follows a landing that does not land SHALL be main-level ops's, read from the runner's report alone (record 0056 decision 5). Where the bolt's row says Flume's landing fix covers it, whether that fix takes main in, makes a failed check pass, or is still to be launched, ops SHALL start nothing and tell the user in one line. Where the row names no landing fix of Flume's: for a check that failed, ops SHALL start a fix on the bolt with Flume's words; for a conflict, whose take-main fix crew's read launches, ops SHALL start nothing; and for a forecast conflict, ops SHALL start the take-main fix. Where crew asks ops because Flume ran its bound of landing fixes, or its fix was dropped or not launched, ops SHALL start a fix on the bolt with Flume's words, or tell the planner and the user in one line where the bolt should not land. A landing fix that asks reaches ops as its recipient, and ops SHALL tell the user it waits and on what. A landing the runner or Flume stopped, nothing of the bolt's, ops SHALL record as a signal and tell the planner of in one line, the bolt landing again only on the user's next send.

#### Scenario: What follows a landing that does not land
- **WHEN** main-level ops's brief is read
- **THEN** it says a check that failed is a fix on the bolt ops starts with `crew fix <bolt> <name> "<Flume's words>"`, that a conflict's take-main fix is crew's to launch and ops starts nothing for it, and that a stop is recorded as a signal and told to the planner, the bolt landing again on the user's next send

#### Scenario: Flume's landing fix
- **WHEN** main-level ops's brief is read
- **THEN** it says that where the bolt's row says Flume's landing fix takes main in, makes the failed checks pass, or is launched by Flume, ops starts nothing and tells the user in one line, and that where crew asks it after Flume ran its landing fixes, ops starts a fix by hand with Flume's words or tells the planner and the user
