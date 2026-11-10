# The crew-flake spec's package version from the release file
# (nix/version.nix): a release's x.y.z as it is, main's 0.0.0 as
# 0-unstable-<date> of the tree's last change, and any other version
# failing evaluation.
t:
let
  versionOf = import ../version.nix { inherit (t) lib; };
  date = "20261109123456";
  given =
    version:
    versionOf {
      release = { inherit version; };
      inherit date;
    };
  odd = builtins.tryEval (builtins.seq (given "0.56") null);
in
{
  "At a release" = t.expect (given "0.56.0" == "0.56.0") "0.56.0 gives ${given "0.56.0"}";
  "On main" = t.expect (
    given "0.0.0" == "0-unstable-2026-11-09"
  ) "0.0.0 on 2026-11-09 gives ${given "0.0.0"}, not 0-unstable-2026-11-09";
  "A version that is neither" = t.expect (!odd.success) "0.56 evaluates, where it fails";
}
