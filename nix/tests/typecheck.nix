# nix:typecheck: everything the flake gives evaluates (record 0058,
# flake.1, flake.3).
t:
let
  inherit (t) lib outputs systems;

  # A package's failures: none where it is a derivation whose path
  # evaluates.
  evaluates =
    system: name: package:
    let
      drvPath = builtins.tryEval (builtins.seq package.drvPath true);
    in
    if !lib.isDerivation package then
      [ "packages.${system}.${name} is not a derivation" ]
    else
      t.expect drvPath.success "packages.${system}.${name} does not evaluate to a derivation";

  # A system's packages: crew and default alone, each evaluating, default
  # crew itself, its main program crew.
  givesCrew =
    system:
    let
      packages = outputs.packages.${system};
      given = builtins.attrNames packages;
      evaluated = lib.concatLists (lib.mapAttrsToList (evaluates system) packages);
    in
    t.expect (
      given == [
        "crew"
        "default"
      ]
    ) "packages.${system} gives ${toString given}, not crew and default"
    ++ evaluated
    ++ lib.optionals (evaluated == [ ] && packages ? default && packages ? crew) (
      t.expect (
        packages.default.drvPath == packages.crew.drvPath
      ) "packages.${system}.default is not packages.${system}.crew"
      ++ t.expect (
        (packages.crew.meta.mainProgram or null) == "crew"
      ) "packages.${system}.crew's main program is ${toString (packages.crew.meta.mainProgram or null)}, not crew"
    );
in
{
  "Every system's packages" =
    t.expect (
      builtins.attrNames outputs.packages == lib.sort lib.lessThan systems
    ) "packages gives ${toString (builtins.attrNames outputs.packages)}, not ${toString systems}"
    ++ lib.concatMap (
      system: if outputs.packages ? ${system} then givesCrew system else [ "packages gives no ${system}" ]
    ) systems;
}
