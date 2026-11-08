# The crew-flake spec's package carrying its release (flake.1): the flake's
# outputs called with `self` given a commit, each system's crew.release
# that commit and the package's version, its install writing them to
# plugin/release.json; with the tests' own `self`, which has no commit, as
# a tree with uncommitted changes has none, no release and no file.
t:
let
  inherit (t) lib systems;
  rev = "fcedc22e6df6380f1f640efac5f796416b1fb4c9";
  committed = t.flake.outputs (
    t.inputs
    // {
      self = t.self // {
        inherit rev;
      };
    }
  );

  # A system's failures where its package carries `commit`'s release, or
  # none where `commit` is null.
  carries =
    outputs: commit: system:
    let
      crew = outputs.packages.${system}.crew;
      writes = lib.hasInfix "plugin/release.json" crew.installPhase;
    in
    if commit == null then
      t.expect (
        crew.release == null
      ) "packages.${system}.crew.release is ${builtins.toJSON crew.release}, not null"
      ++ t.expect (!writes) "packages.${system}.crew's install writes plugin/release.json"
    else
      t.expect
        (
          crew.release == {
            inherit commit;
            inherit (crew) version;
          }
        )
        "packages.${system}.crew.release is ${builtins.toJSON crew.release}, not ${commit} at ${crew.version}"
      ++ t.expect writes "packages.${system}.crew's install writes no plugin/release.json"
      ++ t.expect (lib.hasInfix (builtins.toJSON crew.release) crew.installPhase) "packages.${system}.crew's install writes another release than its own";
in
{
  "A build from a commit" = lib.concatMap (carries committed rev) systems;
  "A build from a tree with no commit" = lib.concatMap (carries t.outputs null) systems;
}
