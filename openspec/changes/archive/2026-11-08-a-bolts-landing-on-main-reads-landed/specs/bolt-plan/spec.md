## ADDED Requirements

### Requirement: A bolt's landing is read from its kit's main
crew SHALL read a started bolt's landing from its kit's main's first-parent line, branch standing or not: the newest merge there since the bolt's first launch whose `Sluice-From` names `bolt/<bolt>`, or whose second parent is a head crew submitted of the bolt or its branch's head. An older merge SHALL be no landing of it. Where git can't read main's line, the landing SHALL be unread, said so.

#### Scenario: A bolt landed through a pull request, its branch gone
- **WHEN** swancloud's main holds `4acecf09`, with `Sluice-From: afterthought-ops (pull/377)` and second parent `900527e9`, the head of `x`'s `bolt.submit`, and GitHub has deleted `bolt/x`
- **THEN** `x`'s landing reads `4acecf09`

#### Scenario: A landing that names the bolt's branch
- **WHEN** main holds a merge whose `Sluice-From` is `bolt/x (bolt/x)`, made after `x`'s first launch, and crew recorded no submission of `x`
- **THEN** `x`'s landing reads that merge

#### Scenario: An earlier bolt of the same name
- **WHEN** main holds a merge whose `Sluice-From` names `bolt/x`, made before the standing `x`'s first launch by an `x` that landed and left the plan
- **THEN** it is no landing of the standing `x`

#### Scenario: main's line can't be read
- **WHEN** git can't list main's first-parent line in `x`'s kit
- **THEN** `x`'s landing is unread, said so, and nothing of `x` reads landed from it

### Requirement: A landed bolt's pieces are read from its landing
Once main holds a started bolt's landing, crew SHALL read the bolt's landings, by the branches they name, from that landing's second parent back to its first parent. It SHALL read each unit, chore and fix of the bolt from them, as "A unit whose work its bolt's branch holds is built" and "A fix whose place's landing its bolt's branch holds is merged" have it, whatever the runner carried of its places. A bolt whose every piece reads landed SHALL read landed.

#### Scenario: The landed unit of a bolt whose branch and places are gone
- **WHEN** `x`'s landing on main is `4acecf09`, `900527e9`'s first-parent line holds sluice's landing naming `change/a`, GitHub has deleted `bolt/x`, and deneb's runner answered `a`'s launch `launched` and carries no place of it
- **THEN** `a` reads `landed`, and `x` reads landed in `crew bolts` and on the board

#### Scenario: A piece its landing does not name
- **WHEN** `x`'s landing on main holds a landing naming `change/a` and none naming `change/b`, and the runner reads `b` at code
- **THEN** `a` reads `landed`, `b` reads code, and `x` does not read landed
