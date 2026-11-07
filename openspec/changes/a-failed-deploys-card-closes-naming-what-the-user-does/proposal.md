# A failed deploy's card closes naming what the user does

## Why

swancloud's `deploy.6` asks that a failed deploy's card close by naming the step that failed and what the user does about it. swancloud's deployer already works those words out for each failure, by its cause and the environment's policy (`deployer.sh`, `does_text` and `user_does`). It writes them at the end of the failed step's log and keeps them in its own record. But crew's deploy card closes with the step and its log alone, "The deploy of abc1234 to srv failed at guests; its log: <its log>.", and `crew ops record` takes no field to carry the words. A deployer that handed them would have its record refused as an unknown flag. This was found in the review of swancloud's `a-failed-deploy-is-offered-again-only-on-the-users-word`, batch 37.

## What Changes

- **`crew ops record` takes `--does <words>`.** The deployer hands its failed step's own words of what the user does with the deploy's end, `--act end --outcome failed --does <words>`. crew takes the flag on every record, so the deployer's record is never refused for it, and keeps the words on the entry as `Does`, the run record's new field.
- **A failed deploy's card closes naming them.** After the step that failed and its log, the close gives the words as the deployer wrote them: "The deploy of abc1234 to srv failed at guests; its log: <its log>. What you do: <words>."
- **A deploy recorded with no such words closes as today**, with the step that failed and its log alone. A deploy that ends well closes as today, whatever words it was handed.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `rail-cards`: a failed deploy's card closes naming, after the step that failed and its log, the words of what the user does that the deployer handed its end.

## Impact

- `plugin/lib/ops.py`: `--does` on `crew ops record`, kept on the entry, and `deploy_outcome`'s failed close; the usage.
- `plugin/lib/record.py`: the run record's field `Does`.
- `README.md`: the `crew ops record` line and what its end closes with (`docs.2`).
- `tests/py/test_ops.py`, `tests/py/test_record.py`: the cases.
- swancloud's deployer hands `--does` with a failed end: swancloud's own change, not this one.
- No change to the views or crew's mod (`code.8`): no bolt, unit, stage, card key or rail row changes shape.
