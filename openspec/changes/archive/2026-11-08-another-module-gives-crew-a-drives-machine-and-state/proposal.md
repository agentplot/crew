# Another module gives crew a drive's machine and state

## Why

agentplot/boomdrive record 0032 (accepted 2026-11-08 by agentplot-design, on the user's record 0028) has a host name a drive's machine and its account's crew state repository once, in `services.boomdrive.accounts`. Boomdrive's module then gives crew each drive's machine and state "through crew's module options", as crew's file names them, while "crew's own keys for a drive, its session, roles, blueprints and review, stay in crew's settings, named by the drive". "A host that also writes a drive's machine or state in crew's settings fails its switch."

crew's module can't take that today. `services.crew.settings.drives` is a list (record 0058, `flake.2`). A list merges by concatenation, so another module can't set one drive's `machine` beside the host's entry for that drive: whatever it gives is a second entry, and the label is listed twice. Until crew's module can take the two keys by the drive's name, Boomdrive keeps a stopgap: a guard (`nix/modules/machines.nix`, its change `a-drive-and-its-crew-partition-name-one-machine`) that fails a switch where the host's two writings of a machine differ. Record 0032 retires that guard with two units, crew's first. This change is crew's unit.

The user's ruling of 2026-11-08 holds here too: "I want the system to be built the way it should be and then have agents fucking fix the data transition as necessary". So no code carries a host's settings from the old shape to the new one.

## What Changes

- **BREAKING** `services.crew.settings.drives` is an attribute set keyed by each drive's label. Each drive is a `drive` whose `label` is read-only and taken from its name, so no host sets it. The module still writes the file's `drives` as a list, in the order of the labels, each with its `label`. The file's shape and version don't change, and for deneb's drives the bytes don't change either: they are already in label order.
- Another module can give a drive its `machine` and its `state` as `services.crew.settings.drives.<label>.machine` and `.state`. The host's settings keep crew's own keys for the same drive under the same label: `blueprints`, `session`, `review`, `flume` and, where given, `roles`.
- `machine` and `state` are each written once. Where they are written twice at the same priority, by another module and by the host's settings, evaluation fails even when the values are equal. The failure says each is written once and names every place that writes it.
- If another module gives a drive and the host's settings give none of crew's own keys for it, evaluation fails, as it does for any drive that lacks a key crew requires.
- Evaluation fails for drives given as a list, a label the host sets, a drive's name that is not a name crew accepts, and no drive at all. "A label listed twice" goes away, since an attribute set names each drive once.
- README's The flake describes the keyed drives and the two keys another module can give.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `crew-flake`: the module takes its drives keyed by label and writes them as the file's list, in label order. Another module can give a drive's `machine` and `state` by its label, each written once, and the host's settings keep crew's own keys.

## Impact

- **Code**: `nix/modules/options.nix` (the keyed `drive` submodule, its read-only `label`, the unique `machine` and `state`, the empty-drives assertion in place of the label-twice one) and `nix/modules/json.nix` (the drives written as a list in label order).
- **Tests**: `nix/tests/settings.nix` (deneb's and the runner's drives keyed by label, and the split into the keys another module gives and crew's own) and `nix/tests/file.nix` (the delta's cases). The darwin, NixOS and typecheck cases read the new settings unchanged. `nix/tests/files/deneb.json` and `runner.json` don't change, so neither does the logic tier that loads them.
- **Docs**: README's The flake.
- **Unchanged**: crew's reading of the teams file (`plugin/lib/crew.py`, `code.5`), its version, and every file crew reads at run time. Since nothing crew models changes, crew's views and mod don't change either (`code.8`). `docs/architecture/` and `docs/adr/` belong to the design agent (`docs.7`). It amends `flake.2`'s details, which ruled out drives keyed by label, after this lands (design, *Departures*).
- **Other repositories**: no host sets `services.crew` yet (afterthought/swancloud writes the teams file itself, read at its `origin/main` on 2026-11-08), so no host's configuration has to move. agentplot/boomdrive's bolt `the-boomdrive-flake-configures-the-whole-host` still reads crew's drives as a list (`crews-partitions-give-the-runner-its-crew-table`) and keeps the stopgap guard. Record 0032's Boomdrive unit gives each drive's `machine` and `state` from the accounts at normal priority, builds the runner's crew table from the same accounts, and removes the guard. That work is Boomdrive's, and this change's caller passes it on.
