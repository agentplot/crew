# The crew-flake spec's file (record 0058, flake.2), over options.nix
# evaluated alone beside a system's `assertions`: deneb's drives
# render nix/tests/files/deneb.json byte for byte, with its kept
# repositories nix/tests/files/runner.json (record 0061), the version is crew's,
# and what crew refuses fails evaluation, by tryEval where the module
# system refuses it and by the assertions' messages where the module does.
t:
let
  inherit (t) lib;
  render = import ../modules/json.nix { inherit lib; };
  inherit (import ./settings.nix) deneb runner;
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

  # deneb's drives with the first one changed by `change`.
  first =
    change:
    deneb
    // {
      drives = [ (change (lib.head deneb.drives)) ] ++ lib.tail deneb.drives;
    };
  noState = first (p: removeAttrs p [ "state" ]);
  dispatcher = first (p: lib.recursiveUpdate p { flume.dispatcher = false; });
  planner = first (p: lib.recursiveUpdate p { flume.planner = true; });
  madswan = lib.elemAt deneb.drives 2;
  twice = deneb // {
    drives = deneb.drives ++ [ madswan ];
  };
  teams = deneb // {
    teams = [ ];
  };
  # deneb's drives under the version-5 file's key, with no `drives`.
  partitions = removeAttrs deneb [ "drives" ] // {
    partitions = deneb.drives;
  };

  # runner's settings with crew's kept repository changed by `change`, and
  # with a kept repository named `crew`, with no owner.
  crew =
    change:
    runner
    // {
      repositories = runner.repositories // {
        "agentplot/crew" = change runner.repositories."agentplot/crew";
      };
    };
  noCheckout = crew (e: removeAttrs e [ "checkout" ]);
  relative = crew (e: e // { dir = "repositories/agentplot/crew"; });
  view = crew (e: e // { view = "/Users/chuck/Code/boomdrive/agentplot/crew"; });
  ownerless = runner // {
    repositories = {
      crew = runner.repositories."agentplot/crew";
    };
  };
in
{
  "deneb's drives" =
    t.expect (renders deneb) "deneb's settings do not evaluate"
    ++ lib.optionals (renders deneb) (
      t.expect (
        text deneb == pinned
      ) "deneb's settings render ${text deneb}, not nix/tests/files/deneb.json"
      ++ t.expect (failures deneb == [ ]) "deneb's settings fail: ${toString (failures deneb)}"
      ++ t.expect (
        !(lib.head rendered.drives) ? roles
      ) "afterthought's drive, which gives no roles, renders a roles key"
    );

  "A runner host's kept repositories" =
    t.expect (renders runner) "runner's settings do not evaluate"
    ++ lib.optionals (renders runner) (
      t.expect (
        text runner == builtins.readFile ./files/runner.json
      ) "runner's settings render ${text runner}, not nix/tests/files/runner.json"
      ++ t.expect (failures runner == [ ]) "runner's settings fail: ${toString (failures runner)}"
    )
    ++ t.expect (
      renders deneb && !(rendered ? repositories) && !(lib.hasInfix "repositories" pinned)
    ) "deneb's file, which gives no repositories, has a repositories key";

  "An entry with no checkout" = t.expect (
    !renders noCheckout
  ) "a kept repository with no checkout evaluates";

  "A relative folder" = t.expect (
    !renders relative
  ) "a kept repository whose dir is relative evaluates";

  "A repository named with no owner" =
    t.expect (
      failures ownerless != [ ]
    ) "services.crew.settings.repositories names crew, and no assertion fails"
    ++
      lib.concatMap
        (
          words:
          t.expect (says ownerless words) "the failure names no ${words}: ${toString (failures ownerless)}"
        )
        [
          "services.crew.settings.repositories"
          "crew, which is no owner/name"
        ];

  "A key crew has no place for" = t.expect (!renders view) "a kept repository giving view evaluates";

  "The version is crew's" =
    t.expect (renders deneb && rendered.version == crewVersion)
      "the module writes version ${
        toString (rendered.version or null)
      }, not crew.py's ${toString crewVersion}"
    ++ t.expect (
      !renders (deneb // { version = 4; })
    ) "a host's settings set version 4, and evaluation holds";

  "A drive with no state repository" = t.expect (!renders noState) "a drive with no state evaluates";

  "A label twice" =
    t.expect (
      failures twice != [ ]
    ) "services.crew.settings.drives lists madswan twice, and no assertion fails"
    ++
      lib.concatMap
        (words: t.expect (says twice words) "the failure names no ${words}: ${toString (failures twice)}")
        [
          "services.crew.settings.drives"
          "madswan"
        ];

  "Drives under `partitions`" = t.expect (
    !renders partitions
  ) "services.crew.settings lists its drives under partitions with no drives, and evaluation holds";

  "A role crew has no kind for" =
    t.expect (!renders dispatcher) "a drive's flume names dispatcher, and evaluation holds"
    ++ t.expect (!renders planner) "a drive's flume gives planner true, and evaluation holds";

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
