# Design

## Context

What was read on 2026-11-08, so the decisions below rest on it.

**The runner's copy on deneb.**
- The runner's container for `agentplot/crew` is `/Users/chuck/.local/share/flywheel/repositories/agentplot/crew`. It holds `crew.git` (bare), a `.git` file reading `gitdir: ./crew.git`, and `places/`. It has no `main`.
- The runner's view is `/Users/chuck/Code/boomdrive/agentplot/crew`, a worktree of that bare clone: its `.git` names `crew.git/worktrees/crew`.
- Flume's places of crew's work, this one among them, are worktrees of the same `crew.git`.
- So `git -C <container>`, `git -C <view>` and `git worktree add` from either reach the one clone.

**Where crew names a kit's folder today.** One function builds the hosts-file layout: `crew.checkout(sess, repo)`, `<sess dir>/<name>/main`. Everything below reads it:
- `load`: the partition's `checkout`, its first blueprints repo's, the main level's cwd (`launch`, `crew-role`).
- `kept_on(fleet, host, repo)`: the first session whose space keeps the address. It serves:
  - `blueprints_on`, the main level's other blueprints folders;
  - `TEAMS_DOORS`, the partitions whose host keeps swancloud;
  - `crew_on`, crew's command on another host.
- `kit_kept(fleet, host, kit)`: `{name, repo, dir, main}` by address or name alone, refused for two addresses by one name. It serves:
  - `plan.main_kit`, everything done before a runner takes a kit's work;
  - `kits_kept` and `kits_on`, the main level's kit folders;
  - `main_tokens`, `KIT_CHECKOUTS` and `CARDS`.
- `ops.kit_range`: `crew.checkout(sess, r)` for each repo the main level's session keeps.
- `grep` finds no other `/main` built from a folder in `plugin/lib`, `plugin/bin` or `plugin/hooks`.

**Where the folders are the runner's already.** A bolt's or kit's work once a runner took it is read at the folder the runner reports in `repositories.rec` (`runner.where`, `plan.kit_of`), with `main` and `dir` both that folder, the container on a runner host. This change leaves that alone.

**The briefs.**
- `design.md` names `{{CHECKOUT}}` ("this directory") and `{{KIT_CHECKOUTS}}`, and cuts design worktrees at `<the kit's folder>/places/design-<topic>`. The folder is left for the agent to infer from the checkout, which only the `<dir>/<name>/main` layout allows.
- `operator.md` hard-codes `~/Code/github_afterthought/swancloud/main` and `~/Code/github_afterthought/swancloud/places/crew-teams-<label>`, pinned by `tests/t-briefs.sh`.

**The file's writers.** swancloud's `lib/crew-teams.nix` and crew's module, `services.crew` (`flake.1`, `flake.2`), render the same cleaned `builtins.toJSON`. The module's settings are free-form beside the keys it declares. swancloud's change `each-repository-is-queued-in-the-runners-copy` is planned in record 0060 but not written (its bolt `one-copy-of-each-repository-on-deneb` holds the record alone), so the key's shape is crew's to set here.

**A restart when folders change.** `launch_digest` covers a role's folders, so a standing agent whose cwd or dirs change is due a restart (`teams.19`). The restart resumes its last conversation in the folder that conversation began in, since Claude Code finds a conversation only from there (`last_conversation`, `resolve`).

**Area pages this change touches:**
- `core.md`: `code.5`, `code.7`, `read.1`, `roles.9`, `code.8`.
- `plan.md`: `plan.18`.
- `teams.md`: `teams.6`, `teams.10`, `teams.19`.
- `briefs.md`: the briefs' words.
- `flake.md`: `flake.2`, `flake.3`.
- `tests.md`: `tests.6`, `tests.11`, `tests.12`.
- `docs.md`: `docs.2`, `docs.4`, `docs.7`.

No rule page is edited by this change (`docs.7`).

## Goals / Non-Goals

**Goals:**
- On a host whose teams file names its kept repositories, every folder and checkout crew names there for a kit, in a brief or in a read, is the file's: the runner's container and view on a runner host.
- Where the file names none, every folder is what it is today.
- The flake's module writes the key, and its tests pin it (`flake.2`, `flake.3`).

**Non-Goals:**
- Writing the key for deneb. That is swancloud's change, and Boomdrive's module once the flake is ready (record 0061, Consequences).
- A folder on another host. The file names the repositories of the host it is written on alone.
- The folder the runner reports for work it took, which is already the runner's.
- Moving, making or removing anything in the runner's container or view (boomdrive `core.14`). crew names them, and agents cut their own worktrees there, as record 0060 has every agent that submits do.
- `crew_on`, which runs crew on another host from the checkout that host's spaces keep.

## Decisions

### 1. One top-level `repositories` object, keyed by address, each with `dir` and `checkout`

```json
"repositories": {"agentplot/crew": {"checkout": "/Users/chuck/Code/boomdrive/agentplot/crew",
                                    "dir": "/Users/chuck/.local/share/flywheel/repositories/agentplot/crew"}}
```

- **The keys are record 0061's.** `dir` is the folder crew names as the kit's, where worktrees are cut. `checkout` is the working tree crew names as the kit's checkout.
- **The key sits beside `partitions`, not in one.** A repository is the host's, kept once for every partition that names it, as the runner keeps it once.
- **It is keyed by the address** crew already matches kits by (`kit_in`), so no repository can be listed twice, and a nix attribute set keyed the same way is the module's natural shape.
- **Not taken:**
  - A list of `{repository, dir, checkout}`, which can list one repository twice and needs a check the object does not.
  - Boomdrive's `_dir` suffix (its `core.12`), which binds Boomdrive's configuration. Record 0061 names these keys.

### 2. The file stays at version 5

- The key is optional, and `load` ignores a key it does not read. So a crew before this change loads a file that has it and names today's folders. Those folders stay on disk until the user removes them (record 0060).
- swancloud writes the key once deneb's crew carries this change, on the user's word (record 0060's amendment, `herdr.15`), so no host's crew reads a file it misreads.
- Not taken: version 6. Every host's file would be refused until both writers and every pin moved together, for a key that changes nothing where it is absent.

### 3. The key is checked whole at load, and its absence names none

- `load` checks `repositories` before any entry is used (`code.5`):
  - it is an object;
  - each key matches `^[^/\s]+/[^/\s]+$`;
  - each value is an object of exactly `dir` and `checkout`;
  - each of those is a non-empty absolute path.
- A failure is a `Refusal` naming the file, the repository and the fix. The fix is the one the other checks give: regenerate the file from the machine's configuration, swancloud's `lib/crew-teams.nix` (`code.2`, `read.1`).
- `load` does not check that the paths exist. A checkout that is not there reads as it does today, `no checkout at <path>` in `gather.py`, and `last_conversation` skips a folder that is gone (`read.1`).
- A file with no `repositories` names no repository. That is record 0061's decision ("Where it names none, crew names them as it does today"), not a default for a field (`code.5`).

### 4. The file's repositories are this host's alone

- The file names repositories "for the host it is written on" (record 0061), and names no host (`flake.2`: `services.crew.host` is no key of the file).
- So `load` keeps the entries on the fleet with the host they are for: `fleet["repositories"] = {"host": <this_host()>, "named": {<address>: {"dir", "checkout"}}}`, or `{}` for none. `this_host()` is read only when the file names any repository, so a load of a file with none runs no process.
- The resolver compares a host with that `host` and starts no process itself (`code.7`). Fleets built by hand in the logic tier, which have no `repositories`, name none.
- For another host crew names folders from the hosts file, as today. A main-level command forwards to its main level's host before it reads (`code.3`), so a main level's folders are read where its own file is.
- Not taken:
  - Reading another host's teams file over ssh, which `read.5` rules out for anything but its kits' stages.
  - Asking the runner's report, which record 0061 turned down for briefs built before any launch.

### 5. One resolver, and a repository the file names is kept whether or not a space lists it

- `crew.kept_at(fleet, host, sess, repo)` gives `{"dir", "main"}`:
  - the file's `dir` and `checkout` where `host` is the file's host and the file names `repo`;
  - else `<sess dir>/<name>` and `checkout(sess, repo)`.
- `crew.kept(fleet, host)` lists every repository a host keeps as `{"name", "repo", "dir", "main"}`. On the file's host, the file's entries come first. Then come the sessions' repositories the file does not name by address, each at the first session whose space keeps it, as `kit_kept` takes it today.
- `kit_kept` matches a kit against `kept`, by address or name alone. It refuses a name alone that matches two addresses, counting both sources (`read.1`).
- `kept_on` is the `main` of `kept`'s entry for an exact address.
- `checkout` stays the hosts-file layout and is called only inside `kept_at`.
- Why a file's entry counts as kept with no space behind it: record 0061 makes the file the host's configuration of the runner, and the hosts file is the one the flake retires. A repository the runner keeps and no space lists is still the host's.
- Not taken: the hosts file deciding which repositories are kept and the file only moving their folders. A file's entry would then be silently ignored wherever swancloud's spaces lag.

### 6. The partition's checkout, and the session it runs in

- `load` sets the partition's `checkout` through `kept_at` for its first blueprints repo on its machine. On a runner host that is the runner's view of the blueprints, where its main level starts (`launch`).
- `load`'s check that the main level's session keeps its first blueprints repo stays the hosts file's. Which session a partition runs in is the hosts file's to say, and record 0061 moves only the folders.

### 7. The briefs name each folder beside its checkout

- **`design.md`** names `{{SIGNALS_REPO}}`'s checkout `{{CHECKOUT}}` with its folder `{{FOLDER}}`, a new token, `kept_at`'s `dir` of the first blueprints repo. `{{KIT_CHECKOUTS}}` names each kit as `` `<main>` (its folder `<dir>`) `` and still says "none on this host" for none.
  - The brief stops calling the checkout "this directory": a resumed session works on in the folder it began in (Context).
  - Its worktree line, `<the kit's folder>/places/design-<topic>`, then reads against a folder the brief names.
  - Its anchor sentence says a kit's checkout is moved to GitHub's main by its host, the fleet's timer or the runner on a runner host, and by nobody else.
- **`operator.md`** names `{{SWANCLOUD_CHECKOUT}}` and `{{SWANCLOUD_FOLDER}}` in place of the hard-coded paths, in its partition sentence, its fetch, its `worktree add`, its `places/crew-teams-<label>` and its `wt -C … remove`. The tokens are `kit_kept(fleet, p["machine"], "afterthought/swancloud")`'s `main` and `dir`.
  - Where the host keeps none, as on the box, each says so in words, `swancloud's checkout, which <host> does not keep` and `its folder, which <host> does not keep` (`teams.10`).
  - That brief already sends a box's change to the teams to a door.
- `tests/t-briefs.sh` pins the new phrases (`tests.6`).
- No other brief names a kit's folder, by grep of `plugin/roles` and `plugin/skills`.

### 8. ops's deploy range reads its checkouts through the resolver

`ops.kit_range` takes its candidate checkouts from a pure `crew.session_checkouts(fleet, host, sess)`: each repo the main level's session keeps, at `kept_at(fleet, host, sess, repo)["main"]`. It then probes them with git as before. The set is still the session's repos, so a deploy's range is read in the same kits as today, at the folders the file names.

### 9. The flake declares the key, and a second pinned file holds its bytes

- `nix/modules/options.nix` declares `settings.repositories`:
  - its type is `nullOr (attrsOf (submodule { dir; checkout; }))`, default `null`, so an unset key is left out by `json.nix`;
  - `dir` and `checkout` are absolute paths (`strMatching "/.*"`), each with no default;
  - the submodule has no free-form type, so another key fails evaluation;
  - an assertion names any key that is no `<owner>/<name>`.
- `nix/tests/files/deneb.json` stays deneb's file as read on 2026-11-07.
- `nix/tests/files/runner.json` is deneb's partitions with `repositories` for `agentplot/crew` and `afterthought/swancloud`, at the container and view record 0060 lays out, as `builtins.toJSON` gives it: keys sorted, no space. `settings.nix` gains `runner`, and `file.nix` pins it byte for byte and adds the four failing cases.
- `tests/py/test_module_file.py` loads `runner.json` on deneb, so crew's logic tier reads what the module writes (`flake.3`).
- Not taken: rewriting `deneb.json`, which would no longer be a file anyone read.

### 10. README and the crew skill

README's teams-file line and the crew skill's partitions paragraph say the file may name the host's kept repositories, their folders and checkouts, which crew names on that host, and today's folders where it names none. No command's usage changes, so `plugin/bin/crew`'s header stays (`docs.2`).

### Rules relied on

- `code.5`: the key is checked at load, every entry before any is used, crew never writes it, and it has no default for `dir` or `checkout`.
- `code.7`: `kept_at`, `kept`, `kit_kept` and `session_checkouts` are decisions on plain facts. The host is read once at load.
- `read.1`: a bad entry, or one name for two repositories, is refused naming what it could not tell. A missing path is read as missing.
- `roles.9`: the runner keeps the repositories and swancloud or Boomdrive's module writes crew's file. crew records nothing against a host and moves no view.
- `plan.18`: crew never moves an anchor or levels a checkout, the runner's view among them.
- `teams.10`: every token fills with text, a host that keeps no swancloud among them.
- `teams.19`: once a host's file names its repositories, the folders it changes make each standing agent there due a restart.
- `flake.2`, `flake.3`: the file's shape changes the module and a pinned file in the same change, and the logic tier loads it.
- `code.8`: no bolt, unit, stage, card or rail row changes shape, so `board.agent_views` and `status.js` are untouched.

### Departures

- **`code.5`** says the file at version 5 holds "partitions alone". Record 0061 (accepted 2026-11-08) adds the optional `repositories` beside them, at the same version (Decision 2). The rule's words are the design agent's to amend after this lands, not this change's (`docs.7`).
- **`plan.18`** says the fleet's timer alone moves a kit's main folder. On a runner host the runner moves its view (boomdrive `core.14`; swancloud record 0060). The brief says so (Decision 7). The rule's words are the design agent's, as above.
- **`openspec/config.yaml`** asks the last task to run `tests/suite --affected`. This change's tasks end at their own checks, since the verify stage runs the repository's checks once after every task is done.

## Risks / Trade-offs

- **A resumed session keeps its old folder.** After the file names a host's repositories, each standing agent's due restart resumes its conversation where it began, the person's checkout, which stays on disk (record 0060). Its brief and `--add-dir` name the runner's folders. → The brief names every path it means and stops calling the cwd "this directory" (Decision 7). A fresh start opens in the view. Not taken: starting each role fresh when its folder moved, which loses its conversation (`teams.19` keeps it).
- **Another host's runner folders are not known here.** A read from another host of a runner host's kit before a runner takes its work names the hosts-file folder, which gather reads as no checkout. → Main-level commands forward to the main level's host (`code.3`). The rest is a view, which names what it could not read (`read.3`).
- **crew fetches in the runner's clone.** crew's reads fetch GitHub into a kit's checkout before deciding (`plan.18`, `gather.py` `fetched`), and the design brief has the agent fetch there. On a runner host that is the runner's clone, whose rule says "the runner alone fetches it" (boomdrive `core.14`). That rule's details rule out a fetch the runner makes on its timer for a tool, and they let sluice work in the container, where sluice fetches itself. A fetch moves only origin's tracking refs, which the runner reads. → This change keeps crew's fetches as they are. Whether a tool's own fetch of the runner's clone is allowed is a question for agentplot-design against `core.14`, raised in this stage's report.
- **The key's shape is set before swancloud writes it.** → It is the shape record 0061 names. Both writers render one `builtins.toJSON` of the same attributes, and `runner.json` pins the bytes the module gives.

## Migration Plan

None. A host whose file names no repositories behaves as today. deneb moves when swancloud's change writes the key and deneb's crew pin moves to a release carrying this change, both on the user's word (record 0061, Consequences; record 0060's amendment).

## After deploy

None. Every outcome here is a logic, nix or end-to-end case. Writing the key on a host is swancloud's change, and moving deneb's pin is the user's word, neither a step of this change.

## Task notes

**1.1** `plugin/lib/crew.py` `load`:
- reads `data.get("repositories")` and checks it as Decision 3 says, in a function of its own, `repositories_of(data)`, which raises through `fail`;
- sets `fleet["repositories"]` as Decision 4 says, calling `this_host()` only when the file names any.

Cases in `tests/py/test_teams.py`, beside the existing load cases:
- a file naming `agentplot/crew` loads, and the fleet carries it with the host monkeypatched as `deneb`;
- each bad shape is refused with words naming the file and the repository: not an object, key `crew`, no `checkout`, a relative `dir`, a `view` key, an empty `dir`;
- a file with none gives `{}` and runs no process (the logic tier's fixture refuses one).

**1.2** `crew.kept_at(fleet, host, sess, repo)` and `crew.kept(fleet, host)` (Decision 5). `kit_kept` and `kept_on` read `kept`. `load`'s partition `checkout` reads `kept_at` (Decision 6).

Cases in `tests/py/test_kits.py` `TestBeforeARunnerTookIt`, with a fleet whose `repositories` names `agentplot/crew` at `/r/agentplot/crew` and `/v/agentplot/crew` for `deneb`:
- `plan.main_kit` for `crew` and `agentplot/crew` gives `dir` `/r/agentplot/crew` and `main` `/v/agentplot/crew`;
- a repository the file names and no space keeps is found;
- the same fleet asked for `alpha` gives the spaces' folders;
- a name alone matching the file's `agentplot/blueprints` and a space's `afterthought/blueprints` is refused naming both;
- `crew.kits_on` gives the view;
- the existing cases, with no `repositories`, are unchanged.

**1.3** `crew.load` on a file naming the first blueprints repo of a partition whose machine is this host sets that partition's `checkout` to the file's `checkout`. `crew.launch`'s `cwd` is it. Case in `tests/py/test_teams.py`.

**1.4** `crew.session_checkouts(fleet, host, sess)` (Decision 8), and `ops.kit_range` reads its candidates from it. Case in `tests/py/test_ops.py`: a session keeping `agentplot/crew` and `agentplot/flume` on a host whose file names crew gives crew's view and flume's `<dir>/flume/main`, in the session's order.

**2.1** `main_tokens` (Decision 7):
- `FOLDER` is the first blueprints repo's `dir`;
- `KIT_CHECKOUTS` is `` `<main>` (its folder `<dir>`) `` joined by ", ", or "none on this host";
- `SWANCLOUD_CHECKOUT` and `SWANCLOUD_FOLDER` come from `kit_kept(fleet, p["machine"], "afterthought/swancloud")`, or the words for none.

Cases in `tests/py/test_teams.py`'s brief case:
- with no `repositories`, `KIT_CHECKOUTS` is `` `<T>/deneb/madswan/crew/main` (its folder `<T>/deneb/madswan/crew`) ``;
- with the file naming crew and swancloud for `deneb`, the tokens name the file's paths;
- for the box, the swancloud tokens say the box keeps none.

**2.2** `plugin/roles/design.md`, line 13 and the anchor sentence, and `plugin/roles/operator.md`'s partitions paragraph and steps 1 and 2 (Decision 7). `tests/t-briefs.sh`:
- the operator's phrases name the folder its host's spaces keep, `<T>/hosts/mac-studio/work/madswan/swancloud`, for a Mac main level;
- one case writes `repositories` into one host's teams file, builds the design and operator briefs there, and finds the file's paths in them and no `~/Code/github_afterthought/swancloud`.

**3.1** `nix/modules/options.nix`, `settings.repositories` (Decision 9), described in each option's `description`.

**3.2** `nix/tests/settings.nix` gains `runner`: `deneb` with `repositories."agentplot/crew"` and `repositories."afterthought/swancloud"` at `/Users/chuck/.local/share/flywheel/repositories/<owner>/<name>` and `/Users/chuck/Code/boomdrive/<owner>/<name>`. `nix/tests/files/runner.json` holds its bytes, written by hand from `deneb.json` with `repositories` in its sorted place, no newline at the end. `nix/tests/file.nix` adds:
- "A runner host's kept repositories": `text runner == pinned runner.json`, and `deneb.json` has no `repositories`;
- the four failing cases: no `checkout`, a relative `dir`, a key `crew`, a `view` key.

**3.3** `tests/py/test_module_file.py` loads `runner.json` with `this_host` monkeypatched to `deneb`. It finds the four partitions, and `crew.kit_kept(fleet, "deneb", "crew")` at the file's container and view.

**4.1** `README.md`'s teams-file line and `plugin/skills/crew/SKILL.md`'s partitions paragraph (Decision 10).
