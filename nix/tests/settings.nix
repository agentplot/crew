# The crew-flake spec's settings: deneb's four drives, keyed by label, with
# the values of deneb's ~/.config/crew/teams.json read 2026-11-07, in the
# order deneb's file lists them, which is label order, each named by its
# label alone as version 6 holds them, which nix/tests/files/deneb.json
# holds byte for byte; and `runner`, the same drives with crew's and
# swancloud's kept repositories at the runner's container and view record
# 0060 lays out, which nix/tests/files/runner.json holds byte for byte;
# and deneb's drives split in two: `given`, each drive's `machine` and
# `state` alone, as another module gives them, and `own`, each drive's
# other keys, crew's own, which the host's settings keep.
let
  # Every role stands on deneb.
  standing = {
    design = false;
    planner = false;
    reviewer = false;
    ops = false;
    operator = false;
  };
  review = {
    every = 5;
    hours = 4;
  };

  # A repository the runner keeps on deneb: its container and its view.
  kept = address: {
    dir = "/Users/chuck/.local/share/flywheel/repositories/${address}";
    checkout = "/Users/chuck/Code/boomdrive/${address}";
  };
in
rec {
  given = builtins.mapAttrs (_: drive: { inherit (drive) machine state; }) deneb.drives;
  own = builtins.mapAttrs (
    _: drive:
    builtins.removeAttrs drive [
      "machine"
      "state"
    ]
  ) deneb.drives;

  runner = deneb // {
    repositories = {
      "agentplot/crew" = kept "agentplot/crew";
      "afterthought/swancloud" = kept "afterthought/swancloud";
    };
  };

  deneb = {
    drives = {
      afterthought = {
        blueprints = [ "afterthought/blueprints" ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "afterthought";
        inherit review;
        flume = standing;
      };
      agentplot = {
        blueprints = [ "agentplot/blueprints" ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "agentplot";
        inherit review;
        flume = standing;
      };
      madswan = {
        blueprints = [
          "afterthought/blueprints"
          "agentplot/blueprints"
        ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "madswan";
        inherit review;
        flume = standing;
      };
      wldn = {
        blueprints = [ "WilldanGroup/willdan-blueprints" ];
        state = "WilldanGroup/crew-state";
        machine = "chuck-herdr-alpha";
        session = "wldn-2";
        inherit review;
        roles.planner.session = "wldn-1";
        flume = standing;
      };
    };
  };
}
