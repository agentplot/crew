# A send reaches another host's drive from the sender's crew

## Why

wldn's agents run on chuck-herdr-alpha and send to deneb's drives. alpha's teams file names none of those drives, so `crew send` there refuses them. The agents work around it with `ssh deneb crew send …`. That typed the prompt into deneb's operator, but the entry could not reach the drive's branch: macOS keeps an ssh session out of the login keychain, where gh holds deneb's GitHub token (afterthought/crew-state `signals/2026-11-14-afterthought-ops-a2377e97/01` on afterthought/main, "security: SecKeychainCopySettings …: User interaction is not allowed."). alpha's own GitHub sign-in can push afterthought/crew-state from a non-interactive ssh session (`signals/2026-11-14-boomdrive-planner-14f4a237/01` on boomdrive/main).

Record 0068 (accepted, boomdrive-design's) decides that a send reaches a drive on another host from the sender's own crew. The host's teams file names the drives its agents send to. The prompt is typed into the drive's operator through herdr over ssh. The entry is pushed from the sending host. So no agent runs ssh to send. `briefs.10` already rules out the ssh workaround and allows this way.

crew's send path already works this way for a drive the sending host's teams file names: deneb's file names wldn on alpha, and a send from deneb to wldn types over ssh and pushes from deneb. Nothing proves the box-to-Mac direction, though. The refusal that led wldn's agents to ssh names no way on. And nothing an agent reads says a send runs on its own host.

## What Changes

- **A send to another host's drive runs on the sender's host, proven.** An end-to-end case sends from the box to a Mac's drive its teams file names. The prompt is typed through `ssh -o BatchMode=yes` and herdr on the Mac. No `crew` command runs there. The entry is the box's own, pushed from the box as its own commit on the drive's branch.
- **A send whose entry's push is refused still stands.** The entry stays in the sending host's file, said once (`record.2`), and `crew send` reports the send made. A logic case pins it.
- **The refusal of a drive this host's teams file does not name points to the way on.** It names the host and the drives its file names, and says the host's configuration names each drive its agents send to, wherever it runs, never an ssh to another host. Nothing is sent.
- **Every brief's one line says where a send runs.** `crew send` is run on the agent's own host, never over ssh, and reaches the drive's operator wherever it runs (`briefs.10`).
- **README, the crew skill and `crew`'s usage say so** (`docs.2`): a host's teams file names each drive its agents send to, and a send types over ssh by herdr and pushes its entry from the sending host.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `operator-agent`: a send to a drive on another host runs on the sender's host and runs no crew command there; the refusal of a drive the host's teams file does not name says the host's configuration names it; every brief's line says a send runs on the agent's own host, never over ssh.
- `run-record`: a send's entry is pushed from the sending host, and a refused push keeps it there and leaves the send standing.

## Impact

- `plugin/lib/crew.py`: `send_door` takes this host's name and its refusal says the way on; `send` passes it; `sends`, the brief's line beside the roster.
- `plugin/bin/crew`'s usage header, `README.md`, `plugin/skills/crew/SKILL.md` (`docs.2`).
- Tests: `tests/py/test_send.py`, `tests/t-journey-main.sh`, `tests/t-briefs.sh`, `tests/t-docs.sh`, `tests/t-help.sh` where it pins the usage.
- No change to the teams file's shape, to `record.py` or to what crew models: no view and no mod change (`code.8`).
- No rule or record changes: `briefs.10` already carries record 0068 (`docs.7`).
- Outside crew: alpha's teams file naming deneb's drives is afterthought's host configuration's (record 0068, Consequences). This change neither needs it nor waits on it.
