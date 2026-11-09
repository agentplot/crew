# crew's teams file, rendered from services.crew.settings at evaluation
# (record 0058, flake.2): every key whose value is null left out, at any
# depth, lists included, then builtins.toJSON, which sorts each object's
# keys and adds no space, with no newline after. That is what the fleet's
# writer gives (swancloud's lib/herdr-published.nix `teamsJsonFor`), so for
# the same drives the module's file holds the same bytes, and the gate
# compares the text without building it.
{ lib }:
let
  clean =
    value:
    if builtins.isAttrs value then
      lib.mapAttrs (_: clean) (lib.filterAttrs (_: v: v != null) value)
    else if builtins.isList value then
      map clean (builtins.filter (v: v != null) value)
    else
      value;
in
settings: builtins.toJSON (clean settings)
