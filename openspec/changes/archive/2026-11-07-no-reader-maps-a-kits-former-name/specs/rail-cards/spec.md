## REMOVED Requirements

### Requirement: A kit's landings card follows its rename
**Reason**: It read a card key's kit through the partition's renames, so a card under `land/<old>` or `record/<old>/<n>` was taken for the renamed kit's. No reader maps a former name (`plan.22`, record 0060; bolt-plan "crew reads each kit by the name its record gives it").
**Migration**: A card under `land/<kit>` or `record/<kit>/<n>` is read by the kit its key names, as every other card is. No partition holds a card under a kit's former name: madswan's renames of 2026-11-06 left its landings cards to its rows, and no other partition holds a `kit.rename` entry.
