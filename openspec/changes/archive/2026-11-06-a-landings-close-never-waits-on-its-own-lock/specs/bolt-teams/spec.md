## MODIFIED Requirements

### Requirement: A landing is recorded by the first act that reads the bolt after it
The first crew act on any host to read a bolt once sluice's record has its landing's submission out SHALL record the outcome: the landing's waiter as it stops, `crew bolt submit`'s end, the rail's sweep on the kit's host, or `crew bolt land`. It SHALL take the number from the bolt's last queued `bolt.submit`, read sluice's record on the kit's host one read at a time, record nothing while the submission stands, and close a landed bolt with no word asked (`plan.21`). A read SHALL never wait on itself: the kit's read that a read's close of a landed bolt runs on the kit's host, which the close waits on while the read holds the bolt's turn, SHALL read no bolt's landing, and the kit's next read or the rail's next sweep SHALL read the landings of its other bolts.

#### Scenario: The submitter is gone before sluice decides
- **WHEN** `crew bolt submit z` queues submission 412 and its process is killed, and sluice then lands 412 on main
- **THEN** the waiter's read records `z` landed at the commit main holds and closes it, and no one runs `crew bolt land`

#### Scenario: The rail's sweep records it
- **WHEN** the waiter on the kit's host was stopped before sluice decided 412, and sluice's record later has 412 landed
- **THEN** the rail's next sweep on that host records `z` landed and closes it

#### Scenario: Two reads at once
- **WHEN** the waiter's read and `crew bolt submit`'s own end read `z`'s landing at the same moment
- **THEN** the run record holds one `bolt.submit` outcome for 412 and one `bolt.land`, and each says the bolt landed

#### Scenario: A close's kit read reads the plan from before the close
- **WHEN** the waiter's read of `z` finds 412 landed and closes `z`, and the kit's read the close runs on the kit's host reads the plan as it stood before the close, its `bolt.land` entry not yet on the branch, so the plan still holds `z` with every unit landed
- **THEN** the kit's read reads no landing, the read ends, and the run record holds one `bolt.submit` outcome for 412 and one `bolt.land`

#### Scenario: Still standing
- **WHEN** a read finds sluice's record of 412 still under test
- **THEN** nothing is recorded, and the bolt's last `bolt.submit` stays queued

#### Scenario: A conflict recorded by a later read
- **WHEN** the submitter is gone and sluice's record has 412 in conflict
- **THEN** the next read records `z`'s landing refused at the head submitted, in sluice's verdict, drafts its pull request, and raises its kit's landings card with `z` held on its row

#### Scenario: The user's words are kept on another host
- **WHEN** ops on mac-studio runs `crew bolt submit z` on the user's words in its pane, `z`'s kit is kept on deneb, and the waiter's read on deneb finds 412 landed
- **THEN** the read closes `z` and its landing card naming ops's pane and the time the word was given, none of the words, says the words are kept on mac-studio, and reaches no other host for them

#### Scenario: sluice's record can't be read
- **WHEN** `sluice status 412 --json` on the kit's host fails
- **THEN** the read records nothing, and says it cannot read sluice's record of 412 on that host, with sluice's words
