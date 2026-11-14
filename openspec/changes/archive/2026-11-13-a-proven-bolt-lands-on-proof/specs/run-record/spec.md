## ADDED Requirements

### Requirement: A land crew posts on proof is one entry marked as on proof
Each `land` crew posts on proof SHALL be recorded as one `bolt.submit` on `bolt/<bolt>` carrying `Outcome: asked`, `Form: proof`, the head it was posted at as `Head` and the land's number in `requests.rec` as `Request`, with no `Card` and no `Submission`. A land SHALL be recorded once, however often the bolt is read proven at that head.

#### Scenario: A land on proof
- **WHEN** the raise of `land/crew` posts land 63 of `y`'s launch on proof at `abc1234`
- **THEN** the run record holds a `bolt.submit` on `bolt/y` with `Outcome: asked`, `Form: proof`, `Head` `abc1234`'s commit and `Request: 63`, and no `Card` or `Submission`

#### Scenario: Read proven again
- **WHEN** a later raise reads `y` proven at `abc1234`, land 63 not answered
- **THEN** no land is posted and no entry is written

### Requirement: The mark's lift and the holds each leave one entry holding none of their words
`crew bolt unstay` SHALL leave one `bolt.unstay` entry on `bolt/<bolt>`. `crew plan hold` and `crew plan go` SHALL each leave one entry, `plan.hold` or `plan.go`, on `kit/<kit>` for a kit's hold and on `plan/<label>` for the drive's. None SHALL hold the hold's words or the user's (`record.3`).

#### Scenario: A hold and its lift
- **WHEN** the user runs `crew plan hold "Cutover" --repo crew --label swancloud` and later `crew plan go --repo crew --label swancloud`
- **THEN** the run record holds a `plan.hold` and then a `plan.go`, each on `kit/crew`, and neither holds the word "Cutover"
