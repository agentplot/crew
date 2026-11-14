---
status: accepted
date: 2026-11-14
decision-makers: boomdrive-design (the record and every choice in it)
---

# 0068. A send reaches a drive on another host from the sender's own crew

Status: accepted, boomdrive-design's.

Deciders: boomdrive-design, on afterthought-planner's question of 2026-11-14 relayed by boomdrive-operator, which named the two ways and held the constraint that no token is kept in a plain file.

Sources: afterthought/crew-state `signals/2026-11-14-afterthought-ops-a2377e97/01` (afterthought/main); `briefs.10`, `read.5`, `code.3`, `record.2`; `plugin/lib/crew.py` `send`, `send_door`, `tell`, `on_machine` and `plugin/lib/record.py` `emit`, `reach` on crew's main at 53631532; boomdrivedev/boomdrive record 0007 (every tool takes the family's forge token from the runner).

## Context and problem statement

wldn's agents run on chuck-herdr-alpha and send to deneb's drives. `crew send` there refuses deneb's drives, since alpha's teams file names none of them, so the agents run `ssh deneb crew send …` themselves. Each such send types its prompt into deneb's operator, but its record entry can't reach the drive's branch. macOS keeps an ssh session out of the login keychain, where gh holds deneb's GitHub token: `security: SecKeychainCopySettings …: User interaction is not allowed.` The entry stays in deneb's file and goes up with deneb's next push (`record.2`), so nothing is lost. The workaround itself breaks `briefs.10`, though, which rules out an agent working out which host a drive runs on. The path matters more once wldn's agents run on the Willdan box after its Boomdrive cutover.

## Considered options

1. **The sender's own crew reaches the drive (chosen).** The host's teams file names every drive its agents may send to, with the machine and session it runs on. `crew send <drive>` on that host types the prompt into the drive's operator over ssh, as `crew tell` already reaches an agent on another host (`code.3`). It then writes the send's entry on the sending host and pushes it from there, in that host's own session.
2. **A crew run on deneb over ssh pushes all the same.** That needs a credential an ssh session on macOS can read. A token in a plain file is ruled out. A bridge from the login session's keychain into ssh sessions undoes what macOS's session isolation protects, and it would serve a path option 1 removes.
3. **The runner's forge token.** On a Boomdrive host every tool takes the family's forge token from `boomdrive forge-token` (boomdrive record 0007). crew's state writes are the person's own, signed and authored as them, not the family App's, and the runner serves its drives' repositories, not crew's state repositories.

## Decision outcome

Option 1.

- **No agent runs ssh to send.** `crew send <drive>` works the same on every host whose teams file names the drive. The agent names the drive by its label and nothing else (`briefs.10`). The host's configuration names the drives its agents send to beside its own, each with its machine and session. Such a drive has no session on the host, so the host's follower reads nothing of it.
- **The prompt goes by herdr over ssh.** Typing into the operator's pane runs `herdr agent prompt` on the drive's machine through `ssh -o BatchMode=yes` (`code.3`). No crew process on the drive's machine runs under ssh for a send, so its keychain never comes into it.
- **The entry is the sending host's.** The send's entry goes into the receiving drive's record. It is written on the sending host and pushed from there as its own commit (`read.5`), with the credential the host already uses for its own drives' state, in the session the sending agent runs in. A push that is refused keeps the entry in the host's file, says so once, and the next push takes it (`record.2`). The send itself has already been typed and is never undone or blocked for it.
- **Nothing secret moves.** No token is written to a file or passed through an ssh connection, and nothing reads the login keychain from an ssh session.

### Consequences

- A host's teams file grows by the drives its agents send to. afterthought's host configuration writes alpha's, and the Willdan box's after its cutover.
- The sending host's GitHub sign-in must be able to push to each receiving drive's state repository. Where it can't, sends still arrive and their entries wait in the sending host's file, said once.
- Other commands forwarded to deneb over ssh (`code.3`) still push from an ssh session. Each meets the same keychain wall, and this record does not decide them.
