## ADDED Requirements

### Requirement: Ops's band lists each landing fix Flume runs on a bolt
Main-level ops's band SHALL list each live landing fix of a started bolt's base place among its fixes in flight, after the take-main fixes, with its kit, its name, that it is a landing fix, and what it does, and its head line SHALL count it among the fixes in flight. The mod SHALL draw the band's lines as the views give them (`code.8`).

#### Scenario: A landing fix in ops's band
- **WHEN** `y`'s base place lists `y-1`, for a conflict, live
- **THEN** ops's band lists `fix y-1`, a landing fix taking main in, and its head line counts one fix in flight

#### Scenario: The mod draws it
- **WHEN** the views file gives ops's view with `y-1`'s line
- **THEN** the mod draws that line above ops's prompt as given

### Requirement: A bolt's head line names its landing fix
A bolt's head line and its line in `crew bolts` SHALL end its landing's words with its landing fix: which fix takes main in or makes the failed checks pass, that Flume launches it, or that Flume ran its landing fixes and the bolt waits on ops.

#### Scenario: A landing fix taking main in
- **WHEN** `y`'s landing was refused for a conflict and its base place lists `y-1` live
- **THEN** `y`'s head line ends saying Flume's landing fix `y-1` takes main in

#### Scenario: The bound spent on the head line
- **WHEN** `y`'s landing was refused with its three landing fixes run
- **THEN** `y`'s head line ends saying Flume ran its 3 landing fixes, and it waits on ops
