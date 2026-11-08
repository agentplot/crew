## MODIFIED Requirements

### Requirement: A proposal's card draws a kit's rename
A proposal holding `kit rename <old> <new>` SHALL draw it on its card as a block of its own. The block SHALL name the old name and the new, and say that the repository's work is finished and that its launches, landings and decision-record sources are renamed. Since a rename stands with no bolt or unit of the repository, the block SHALL name none, and the card's picture SHALL draw no section for it. A proposal whose changes add no unit SHALL stay a plain approval, with the rename asking no question of its own.

#### Scenario: madswan's renames proposed
- **WHEN** madswan-planner proposes `kit rename flywheel-cloud boomdrive-cloud` and `kit rename tailrace timber`, once each repository's work is finished
- **THEN** its card draws two rename blocks, each naming its two names and no bolt or unit, its picture draws nothing for either, and the card is a plain approval
