## Context

`crew-makes-a-new-drives-state` (archived 2026-11-09, its design's Decision 14) gave the operator's *Changing the drives* its first words for a host whose `~/.config/crew/teams.json` is a file and no link into the Nix store: a drive is "added, changed or removed through Boomdrive's setup", which gives crew the drive's entry with `crew drive set`. Record 0065, written on that change's landing, settles that `crew drive set` removes no drive and that agentplot/boomdrive record 0009's amendment asks for none: setup's later changes there are a repository of the drive added or removed. Its consequences name this chore to bring the brief to what setup can do.

**Area pages this change touches:** `briefs.md` (`briefs.1`: the operator writes nothing but the teams file, on the user's word), `tests.md` (`tests.6`), `docs.md` (`docs.4`, `docs.6`).

## Goals / Non-Goals

**Goals:** the brief says a drive is added or changed through setup, and names no removal of one there.

**Non-Goals:** a removal of a drive on a host Nix does not configure, by setup or by crew, which no record asks for; the steps through swancloud's `lib/crew-teams.nix` for a teams file that is a Nix link, step 4's removal among them, which stand.

## Decisions

### 1. The brief drops the removal and adds nothing in its place

The sentence reads "a drive is added or changed through Boomdrive's setup on the user's word", and the rest of the paragraph stands: the operator tells the user so and never edits the teams file by hand, itself or through another agent. A removal asked on such a host meets that same bar, so the operator edits nothing for it. Not taken: a sentence telling the operator that no tool removes a drive there, which would state, in a brief, a gap of Boomdrive's that its own design may close, and which record 0065 keeps out ("The operator's brief says only what setup can do").

`t-briefs` pins the new phrase and checks the brief lacks "added, changed or removed through Boomdrive's setup" (`tests.6`).

## Risks / Trade-offs

- [A user asks the operator to remove a drive on a host setup set up] → The brief gives no step for it and forbids a hand edit, so the operator changes nothing; the user's ask stays theirs to carry to Boomdrive.

## Departures

None.

## After deploy

None: the brief is read by each operator at its start, and `t-briefs` proves its words.

## Task notes

**1.1** `plugin/roles/operator.md`, *Changing the drives*, its first paragraph: "a drive is added, changed or removed through Boomdrive's setup" becomes "a drive is added or changed through Boomdrive's setup". `tests/t-briefs.sh`, the case "the operator's brief says a teams file that is no link into the Nix store changes through Boomdrive's setup": the pinned phrase reads "added or changed", and the case `lacks` "added, changed or removed through Boomdrive's setup".
