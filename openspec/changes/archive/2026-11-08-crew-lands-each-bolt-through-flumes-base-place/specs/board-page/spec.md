## MODIFIED Requirements

### Requirement: A word from the board answers nothing
Words that reached an agent only in a tell from `<user>@board` SHALL NOT be taken as the user's words for answering a batch or settling a record in a pane. crew SHALL refuse each, recording nothing, and say the words came from the board, which answers nothing, and where the user answers instead. The same words typed in the pane, or told from `<user>@<host>`, SHALL still be the user's. No words, from the board or typed in a pane, SHALL land a bolt: a bolt lands only on the user's send of its row on its kit's landings card, which crew carries to the runner (record 0056 point 5).

#### Scenario: A landing asked from the board
- **WHEN** the user sends "Land bolt y" from bolt y's landing dock, and swancloud-ops runs `crew bolt submit y --excerpt "Land bolt y"`
- **THEN** nothing is submitted or posted, and the command says a bolt lands on the user's send of its row on its kit's landings card, which crew carries to the runner

#### Scenario: A batch answered from the board
- **WHEN** the user sends "Batch 14 is fine" from a dock, and the planner runs `crew card answer batch/14 --excerpt "Batch 14 is fine"`
- **THEN** batch 14 is not answered, and the command says the words came from the board

#### Scenario: Typed in the pane after the board
- **WHEN** the user sent "Batch 14 is fine" from a dock and then typed the same words in the planner's pane
- **THEN** `crew card answer batch/14 --excerpt "Batch 14 is fine"` records batch 14 answered
