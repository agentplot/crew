# The crew-flake spec's file (record 0058, flake.2), over options.nix
# evaluated alone beside a system's `assertions`: deneb's partitions
# render nix/tests/files/deneb.json byte for byte, the version is crew's,
# and what crew refuses fails evaluation, by tryEval where the module
# system refuses it and by the assertions' messages where the module does.
t:
let
  inherit (t) lib;
  render = import ../modules/json.nix { inherit lib; };
  inherit (import ./settings.nix) deneb;
  pkgs = t.inputs.nixpkgs.legacyPackages.x86_64-linux;

  # options.nix enabled with `given` as its settings.
  evaluated =
    given:
    (lib.evalModules {
      modules = [
        (import ../modules/options.nix { inherit (t.outputs) packages; })
        {
          options.assertions = lib.mkOption {
            type = lib.types.listOf lib.types.unspecified;
            default = [ ];
          };
        }
        {
          _module.args = { inherit pkgs; };
          services.crew = {
            enable = true;
            host = "host-a";
            settings = given;
          };
        }
      ];
    }).config;

  text = given: render (evaluated given).services.crew.settings;
  # Whether `given` renders at all: false where evaluation fails.
  renders = given: (builtins.tryEval (builtins.seq (text given) true)).success;
  failures = given: map (a: a.message) (lib.filter (a: !a.assertion) (evaluated given).assertions);
  says = given: words: lib.hasInfix words (toString (failures given));

  pinned = builtins.readFile ./files/deneb.json;
  rendered = builtins.fromJSON (text deneb);

  # crew.py's VERSION line, read here on its own.
  crewVersion = lib.toInt (
    lib.head (builtins.match ".*\nVERSION = ([0-9]+)\n.*" (builtins.readFile ../../plugin/lib/crew.py))
  );

  # deneb's partitions with the first one's partition changed by `change`.
  first =
    change:
    deneb
    // {
      partitions = [ (change (lib.head deneb.partitions)) ] ++ lib.tail deneb.partitions;
    };
  noState = first (p: removeAttrs p [ "state" ]);
  dispatcher = first (p: lib.recursiveUpdate p { flume.dispatcher = false; });
  planner = first (p: lib.recursiveUpdate p { flume.planner = true; });
  madswan = lib.elemAt deneb.partitions 2;
  twice = deneb // {
    partitions = deneb.partitions ++ [ madswan ];
  };
  teams = deneb // {
    teams = [ ];
  };
in
{
  "deneb's partitions" =
    t.expect (renders deneb) "deneb's settings do not evaluate"
    ++ lib.optionals (renders deneb) (
      t.expect (
        text deneb == pinned
      ) "deneb's settings render ${text deneb}, not nix/tests/files/deneb.json"
      ++ t.expect (failures deneb == [ ]) "deneb's settings fail: ${toString (failures deneb)}"
      ++ t.expect (
        !(lib.head rendered.partitions) ? roles
      ) "afterthought's partition, which gives no roles, renders a roles key"
    );

  "The version is crew's" =
    t.expect (renders deneb && rendered.version == crewVersion)
      "the module writes version ${
        toString (rendered.version or null)
      }, not crew.py's ${toString crewVersion}"
    ++ t.expect (
      !renders (deneb // { version = 4; })
    ) "a host's settings set version 4, and evaluation holds";

  "A partition with no state repository" = t.expect (
    !renders noState
  ) "a partition with no state evaluates";

  "A label twice" =
    t.expect (
      failures twice != [ ]
    ) "services.crew.settings.partitions lists madswan twice, and no assertion fails"
    ++
      lib.concatMap
        (words: t.expect (says twice words) "the failure names no ${words}: ${toString (failures twice)}")
        [
          "services.crew.settings.partitions"
          "madswan"
        ];

  "A role crew has no kind for" =
    t.expect (!renders dispatcher) "a partition's flume names dispatcher, and evaluation holds"
    ++ t.expect (!renders planner) "a partition's flume gives planner true, and evaluation holds";

  "Teams" =
    t.expect (failures teams != [ ]) "services.crew.settings gives teams, and no assertion fails"
    ++
      lib.concatMap
        (words: t.expect (says teams words) "the failure says no ${words}: ${toString (failures teams)}")
        [
          "services.crew.settings.teams"
          "version ${toString crewVersion} has no place for teams"
        ];
}
