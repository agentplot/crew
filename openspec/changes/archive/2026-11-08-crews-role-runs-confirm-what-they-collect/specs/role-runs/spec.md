## ADDED Requirements

### Requirement: A run's start takes every end Flume holds for its role
`crew role start` SHALL take into its turn, beside the asks and the places that wait on the role, each end that a place's status in the runners' records gives as owed to the role's address `<label>/<role>`, by its delivery key.

#### Scenario: A unit's ends taken with an ask
- **WHEN** madswan's planner run starts with an ask from the design agent pending, and the runner's records carry unit `a`'s place, launched by request 12, whose status gives its construct's and its code's ends each owed to `madswan/planner` with its delivery key
- **THEN** the turn takes the ask and both ends, each recorded in the turn by request 12 and its delivery key

#### Scenario: An end owed to another role
- **WHEN** unit `a`'s status gives an end owed to `madswan/operator` and not to `madswan/planner`
- **THEN** the planner's start does not take it

### Requirement: An end a confirm names is not taken again
A start SHALL take no end that a `confirm` of the role's address in `requests.rec` already names, whatever the runner answered that confirm.

#### Scenario: An end already asked confirmed
- **WHEN** an ended turn took unit `a`'s construct's end and its confirm is in `requests.rec`, and the runner's records still carry that end owed to `madswan/planner`
- **THEN** the next start does not take it

#### Scenario: A refused confirm
- **WHEN** the runner answered that confirm `refused`, and its end is still carried owed to `madswan/planner`
- **THEN** the next start does not take it

### Requirement: An owed end makes no role wanted
An end owed to a role's address SHALL NOT make the role wanted: with no ask and no place waiting on the role, its run's start SHALL record no turn and take no end.

#### Scenario: Ends alone start no turn
- **WHEN** the planner's run starts with no ask and no place waiting on it, and unit `a`'s delivered ends are owed to `madswan/planner`
- **THEN** no turn is recorded, no end is taken, and the start says nothing waits

### Requirement: An end crew cannot read is not taken
A start SHALL take no end whose status gives no delivery key or no `owed` crew can read, and SHALL leave the ends on a host whose runner can't be read for the role's next run, as its waits are.

#### Scenario: A status with no delivery keys
- **WHEN** the runner carried unit `a`'s status from a Flume whose ends give no `delivery` and no `owed`
- **THEN** the start takes no end of it, and still takes what waits on the role

### Requirement: A run's end asks the runners to confirm each end its turn took
`crew role end` SHALL append to `requests.rec`, in the commit that ends the turn, one `confirm` for each launch whose ends the turn took, oldest first, naming the launch as its `Of`, the launch's work, the role's address as its `Recipient`, and one `Delivery` for each of those ends' keys in the order taken. A turn that took no end SHALL append none.

#### Scenario: Two places' ends
- **WHEN** the planner's turn took two ends of request 12's place and one of request 14's, and the run runs `crew role end --report <path> "acted on the stop-short"`
- **THEN** the commit that records the turn ended appends a confirm of request 12 naming `madswan/planner` and its two delivery keys, then a confirm of request 14 naming its one

#### Scenario: A turn with no ends
- **WHEN** the planner's turn took one ask and no end, and the run ends its turn
- **THEN** `requests.rec` is unchanged by the end

### Requirement: A lost run confirms nothing
A run that ends taking no turn, and a turn superseded before its end, SHALL append no confirm, so the next run takes those ends again.

#### Scenario: A lost run
- **WHEN** the planner's run took an end and was lost before its end, and its run is retried
- **THEN** no confirm names the end, and the new start takes it again

### Requirement: A turn's report counts its ends
The report `crew role end` writes SHALL say how many ends the turn took, of which launches, and that their confirmation was asked of the runners.

#### Scenario: Three ends of two places
- **WHEN** the planner's turn took two ends of request 12's place and one of request 14's, and its run ends the turn
- **THEN** the report says three ends of requests 12 and 14 were taken and their confirmation asked of the runners

## MODIFIED Requirements

### Requirement: A turn's prompt starts and ends the turn
`plugin/flume/turn.md` SHALL have the run start with `crew role start` and end with `crew role end`, writing its report at `{{report}}`, and SHALL say that the end asks the runners to confirm to Flume each end the turn took, so none is taken again. It SHALL place `{{needs}}` in a sentence saying the run asks the user only on a card and stops short only when `crew role start` refuses. It SHALL ask for no `{{brief}}`.

#### Scenario: The prompt's parts
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** every part in double braces is one Flume fills for a stage with a report deliverable and no `makes`, `{{needs}}` among them, and `{{brief}}` is not among them

#### Scenario: The end confirms
- **WHEN** `plugin/flume/turn.md` is read
- **THEN** its step that runs `crew role end` says the end asks the runners to confirm each end the turn took

### Requirement: A run's start gives its brief and what it took
`crew role start` SHALL write the role's brief, filled for its partition as `crew-role` fills it, to a file on the host, and print the file's path to read whole first, then each ask it took, oldest first, with who asked, what, the record it names and its words, then each place that waits on the role, with its work, its place and its words, then the ends it took that Flume holds for the role, one line for each launch, with its work, its place, its request and each end's key, an expired end marked so, saying they are confirmed when the turn ends, and last the role's answered cards, read in the role's own Pending You name, each with its key and the answer.

#### Scenario: What the planner's run reads
- **WHEN** the planner's start took an ask from the design agent and a card's answer
- **THEN** it prints the brief's path, then the design agent's words, then the card's ask, then the card's key and the user's answer, read in madswan-planner's name

#### Scenario: The ends it took
- **WHEN** the planner's start took an ask and unit `a`'s construct's and code's ends of request 12, the code's expired
- **THEN** after the ask it prints one line for unit `a` naming its place and request 12, `stage/construct/1/delivered` and `stage/code/1/delivered` marked expired, and that they are confirmed when the turn ends
