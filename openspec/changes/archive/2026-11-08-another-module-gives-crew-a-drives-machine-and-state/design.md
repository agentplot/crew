# Design

## Context

**What record 0032 asks of crew.** agentplot/boomdrive record 0032 (accepted 2026-11-08) has a host write a drive's machine and its account's crew state repository once, in `services.boomdrive.accounts`. Boomdrive's module then gives crew "each drive of every account, this host's and others', with its machine and its account's state repository, through crew's module options (core.46; crew `flake.2`)". "crew's own keys for a drive, its session, roles, blueprints and review, stay in crew's settings, named by the drive. A host that also writes a drive's machine or state in crew's settings fails its switch." And "Boomdrive's module sets crew's options as crew's file names them." Boomdrive's rule `core.46`: "Each tool's module writes that tool's file from one option per key, each named as the file names it, and the Boomdrive module sets the other tools' module options and writes no file of theirs." Two units build it, crew's first. This change is crew's.

**What crew's module is today** (read on this branch, `nix/modules/options.nix` and `json.nix`, 2026-11-08). `services.crew.settings.drives` is `types.nonEmptyListOf drive`. Each `drive` declares `label`, `blueprints`, `state`, `machine`, `session`, `review` and `flume` with no default, `roles` optional, and passes undeclared keys to the file. An assertion fails a label listed twice. `json.nix` renders the settings with `builtins.toJSON`, nulls left out. Because a list merges by concatenation, another module that sets `drives` adds entries. It can't reach the host's entry for the same drive. So Boomdrive can't give one drive's `machine` and leave its `session` to the host.

**The stopgap this enables Boomdrive to retire.** Until crew's module can take the two keys, Boomdrive's bolt `the-boomdrive-flake-configures-the-whole-host` keeps a guard. Its change `a-drive-and-its-crew-partition-name-one-machine` (`nix/modules/machines.nix`, read on its branch at e98775e on 2026-11-08) fails a switch where a drive of the accounts and crew's drive of its name give different machines. The guard's proposal: "The change that retires it, once crew's module takes a drive's machine from another module, removes that file, its imports and its cases." That is record 0032's Boomdrive unit. It follows this change.

**One owner.** Two places that could write one fact are reconciled by putting a single option on it, in the module that writes the file. That module is crew's (`flake.2`; Boomdrive `core.18`, `core.46`). crew's module therefore owns the rule that each of the two keys is written once. Boomdrive owns where its values come from, and the name its definitions carry when a second writing fails. crew's module names no other tool (`flake.1`'s details: "Not ruled out: … the Boomdrive module setting `services.crew`'s options"). Flume's module is configured the same way: Boomdrive gives it per-key values by name (`services.flume.settings.streams.<stream>`, `repos."<owner>/<name>"`, Boomdrive's `nix/modules/drives.nix`). That works because Flume's settings are keyed by name. This change gives crew's drives the same property.

**Area pages this change touches:** `flake.md` (`flake.1`, `flake.2`, `flake.3`), `tests.md` (`tests.4`, `tests.5`) and `docs.md` (`docs.4`, `docs.7`). Rules relied on:
- `flake.2`: the file is written whole from `services.crew.settings`, each key named as the file names it, with no default for a key crew requires, and the module's file pinned byte for byte.
- `code.4`: a drive's name is one crew accepts.
- `code.5`: no field of the teams file has a default, and crew's reading doesn't change.
- `flake.3`: the cases are `nix:test`'s, evaluated offline against no store.
- `tests.4`: the lowest tier for a module's evaluation is `nix:test`.
- `code.8`: nothing crew models changes, so neither crew's views nor its mod do.

No rule page or record is edited by this change (`docs.7`). Its one departure is under *Departures*.

## Goals / Non-Goals

**Goals:**
- Another module can give a drive its `machine` and `state` by the drive's label, as the file names them, while the host's settings keep crew's own keys for that drive.
- Each of the two keys is written once: a second writing fails evaluation, whether or not the values are equal.
- A host with crew alone still writes every key of a drive in crew's settings.
- For deneb's drives, the file's bytes don't change.

**Non-Goals:**
- Where another module's values come from, the priority it gives them at, and the name its definitions carry. Those are Boomdrive's (record 0032's second unit).
- A default for `machine` or `state`, this host's name among them (`code.5`, `flake.2`). Record 0032 makes a drive that names no machine this host's on Boomdrive's side, and Boomdrive gives crew that host's name.
- Carrying any host's settings from the list to the keyed shape (the user's ruling of 2026-11-08). No host sets `services.crew` yet.
- Changing crew's reading of the teams file, its version, or anything crew reads at run time.

## Decisions

### 1. The drives are keyed by label and written as the file's list in label order

`services.crew.settings.drives` becomes `types.attrsOf drive`, keyed by each drive's label. `drive` is a submodule taking its name. Its `label` is `readOnly`, with its default set to that name and its type the name type of `code.4`. So a name crew does not accept fails the label's type check, and a host that sets `label` fails as read-only, as a host setting `version` does. `json.nix` writes `drives` as `builtins.attrValues` of the set, which lists the drives in the order of their names, each carrying its `label`, before it leaves out nulls and renders as before. The file's shape and version are unchanged, and crew's reading is untouched (`code.5`). An empty set fails an assertion naming `services.crew.settings.drives`, as the non-empty list did. This keeps crew's own refusal of a file with no drives from being the first word. The label-twice assertion goes, since a set names each drive once. Two definitions of one key of a drive merge or conflict as the module system merges any option.

Not taken:
- **A separate option keyed by label beside the list**, such as `services.crew.given.<label>.machine`, merged into the list's entries by crew's module. The file's `machine` would then have two option paths. That is not one option per key named as the file names it (Boomdrive `core.46`, crew `flake.2`), and crew's module would carry the merge and its checks in code of its own.
- **The list kept, with another module adding whole entries.** The host's entry and the other module's entry for one drive would be two entries with one label, which crew refuses.
- **The drives' order kept as given.** A Nix attribute set keeps no order of its names. Label order is the only order the module can give, and crew reads drives by label (`crew.load` builds them into a dict). Order changes only the order of a few listings.

### 2. `machine` and `state` are unique options

A drive's `machine` is `types.unique { message = …; } <name type>` and its `state` is `types.unique { message = …; } <repository type>`. Each keeps its inner type's check and has no default. The module system fails a unique option given more than one definition at the winning priority, even equal ones. Its words are "The option `services.crew.settings.drives.<label>.machine' is defined multiple times while it's expected to be unique.", then crew's message, then each definition's file and value (nixpkgs `lib/options.nix` `mergeUniqueOption`, read in the locked nixpkgs on 2026-11-08). crew's message says the key is written once: where another module gives it, the host's configuration writes it nowhere else in `services.crew.settings`. Without another module, the host's one writing is the only definition. A drive's other keys keep their types, so the host's settings and another module's settings for one drive merge as before.

Not taken:
- **The plain types, which merge equal definitions.** Two equal writings would pass, and the host would keep writing the fact twice, which record 0032 ends ("fails its switch"). An equality check is what Boomdrive's stopgap guard does, and this change exists to retire it.
- **An assertion in crew's words that reads the options' definitions.** The raw definitions carry `mkIf`, `mkMerge` and priorities, so reading them would re-implement the module system. The unique option already names each place that writes the key.
- **crew's message naming `services.boomdrive.accounts`.** crew's module serves any other module (`flake.1`). Boomdrive's definitions can carry that name as their file (`lib.mkDefinition`, or the giving module's `_file`), so the failure names it as record 0032 asks. That choice is Boomdrive's.

### 3. A drive given and not configured fails as a drive missing a key

Another module that gives a drive's `machine` and `state` creates that drive under `services.crew.settings.drives`. If the host's settings name it nowhere, its `blueprints`, `session`, `review` and `flume` have no value and evaluation fails, as it does for any drive missing a key crew requires (`code.5`). If the host names a drive that no module gives a `machine` or `state`, evaluation fails the same way. crew adds no check of its own for either case, since the module system's missing-value failure names the option. Record 0032 gives crew every drive of every account. A host that runs crew therefore configures crew's keys for each of them, or its switch fails.

### Departures

- **`flake.2`'s details rule out "partitions keyed by label".** That came from record 0058, which kept the fleet's list order so the module's bytes matched the fleet's. Decision 1 keys the drives by label in the module's options. Record 0032 has another module give a drive's keys "named by the drive" and "as crew's file names them", and only an option per drive by its name allows that, since a list merges by concatenation. The file still lists its drives, now in label order. For deneb's drives, which `nix/tests/files/deneb.json` pins, the bytes are the same. A fleet that lists drives in another order would get other bytes, and no host writes crew's file through the module yet. The design agent amends `flake.2` and its details after the landing (`docs.7`).

## Risks / Trade-offs

- **Priorities pass a second writing.** A unique option fails only between definitions at the winning priority. A host that writes `machine` with `lib.mkForce` overrides another module's value without a word, and one that writes it with `lib.mkDefault` yields without a word. Each is an explicit override, which the module system offers everywhere. Boomdrive gives its values at normal priority, unlike its `mkDefault` for Flume's streams, so a plain second writing fails. That is its change's to build.
- **Equal writings fail.** A host moving from writing the machine twice (the stopgap's shape) fails its switch until it removes crew's copy. That is record 0032's intent, and the user's ruling leaves the move to whoever writes the host's configuration.
- **Label order.** Listings that follow the file's order (`crew` with no arguments listing the drives) list them by label on a host configured through the module.

## Migration Plan

None in this repository. No host sets `services.crew` (afterthought/swancloud writes the teams file itself, read at its `origin/main` on 2026-11-08). Boomdrive's bolt reads `services.crew.settings.partitions` as a list, already stale since `crews-partition-is-a-drive`. It moves in record 0032's Boomdrive unit, when Boomdrive takes this commit of crew.

## After deploy

None. Every outcome is a case of `nix:test`, and no host's configuration sets the module, so nothing is deployed with this change.

## Task notes

**1.1** `nix/modules/options.nix`:
- `drive` becomes a submodule function taking `{ name, ... }`. Rename the let-bound name type (today `name`) so the argument does not shadow it, and use the renamed type everywhere it is used now.
- `label` becomes `mkOption { type = <name type>; default = name; readOnly = true; description = "The drive's label, its name under services.crew.settings.drives, which names its main level and its state branch `<label>/main`; no host sets it."; }`.
- `settings.drives` becomes `types.attrsOf drive`, described as every drive by its label.
- Remove `labels`, `twice` and their assertion. Add one assertion `cfg.settings.drives != { }` with the message "services.crew.settings.drives names no drive: crew's teams file lists every drive, by its label."
- The file's opening comment says the drives are keyed by label and written as the file's list in label order.
- No "partition" in any comment (`t-word` reads `nix/modules/`).

`nix/modules/json.nix`: render `clean (settings // { drives = builtins.attrValues settings.drives; })`, and its comment says why: the file's list, in the order of the labels.

`nix/tests/settings.nix`:
- `deneb.drives` becomes an attribute set keyed afterthought, agentplot, madswan, wldn, each entry without `label`, the values as now. `runner` stays `deneb // { repositories = …; }`.
- The opening comment says the drives are keyed by label, in the order deneb's file lists them, which is label order.

`nix/tests/file.nix`:
- `first` becomes a change to `deneb.drives.afterthought`.
- `noState` and a new `noMachine` remove that key from afterthought.
- `labelled` sets `madswan.label = "madswan"`.
- `capital` renames madswan to `Madswan`.
- `listed` gives `drives = builtins.attrValues` of deneb's drives with each `label` added (`lib.mapAttrsToList (label: d: d // { inherit label; })`).
- `none` gives `drives = { }`.
- Remove `madswan` and `twice`, and the case "A label twice".
- `partitions` gives `partitions = deneb.drives` with no `drives`.
- `dispatcher` and `planner` are unchanged in what they set.
- The case "deneb's drives" checks `!(rendered.drives's first entry) ? roles` as now, and also that the rendered labels are `[ "afterthought" "agentplot" "madswan" "wldn" ]` in that order.
- New cases, named as the delta's scenarios: "A drive with no machine", "A label the host sets", "A name crew does not accept", "Drives as a list" (each `!renders`), and "No drive" (an assertion failing whose message names `services.crew.settings.drives` and "names no drive").
- The opening comment names the keyed drives.

**1.2** `nix/modules/options.nix`: in `drive`, `machine` becomes `types.unique { message = "A drive's machine is written once: where another module gives it, the host's configuration writes it nowhere else in services.crew.settings, and each place that writes it is named below."; } <name type>`, and `state` is the same with "state repository" and the repository type. The descriptions say each is written once, by the host's settings or by another module that gives it by the drive's label.

`nix/tests/settings.nix`: add `given`, each of deneb's drives with its `machine` and `state` alone, and `own`, each drive without them, both written with `builtins.mapAttrs` and `builtins.removeAttrs`, since the file takes no `lib`.

`nix/tests/file.nix`:
- `evaluated` takes a list of further modules beside `given` settings, the existing calls passing `[ ]`.
- `giving = drives: { services.crew.settings.drives = drives; }`, a module giving drives' keys.
- Cases, named as the delta's scenarios:
  - "deneb's drives from two modules": settings `{ drives = own; }` with `giving given`. It renders `files/deneb.json` byte for byte and fails no assertion.
  - "A machine written twice": settings `deneb` (every key) with `giving { agentplot = { machine = "deneb"; }; }`, `!renders`.
  - "A state repository written twice": the same with `state = "afterthought/crew-state"`, `!renders`.
  - "A drive given and not configured": settings `deneb` with `giving { extra = { machine = "deneb"; state = "afterthought/crew-state"; }; }`, `!renders`.

**1.3** `nixfmt` over every nix file 1.1 and 1.2 touched, and `statix` and `deadnix` clean: no binding left unused once `labels` and `twice` go.

**1.4** `README.md`, The flake, the `settings` bullet:
- `drives` is every drive by its label, each with its `blueprints`, `state`, `machine`, `session`, `review`, `flume` and, where given, `roles`, none with a default and no `partition` among them. Its `label` is its name, which no host sets.
- The file lists the drives in the order of their labels, the bytes swancloud's writer gives for the same drives in that order.
- Another module, as the Boomdrive flake's does from its accounts, can give a drive its `machine` and `state` by its label, while the host's settings keep the drive's other keys. Each of the two is written once: a second writing fails evaluation, naming each place that writes it.
- The list of what fails evaluation drops "a label listed twice" and adds drives given as a list, a label the host sets, and no drive.
