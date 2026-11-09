# The crew-flake spec's settings: deneb's four drives, keyed by label, with
# the values of deneb's ~/.config/crew/teams.json read 2026-11-07, in the
# order deneb's file lists them, which is label order, each named by its
# label alone as version 6 holds them, with the folder, repositories and
# accounts deneb's ~/.config/swancloud/herdr-hosts.json gave its sessions
# read 2026-11-09, beside deneb's hosts and consoles from the same file
# (record 0064), which nix/tests/files/deneb.json holds byte for byte; and
# `runner`, the same drives with crew's and
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

  # Every role on one Claude account.
  every = account: {
    design = account;
    planner = account;
    reviewer = account;
    ops = account;
    operator = account;
  };
  afterthought = "/Users/chuck/Code/github_afterthought";
  # The repositories afterthought's and madswan's folder keeps on deneb.
  afterthoughts = [
    "afterthought/blueprints"
    "afterthought/paymaster"
    "afterthought/swancloud"
  ];

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
    hosts = {
      deneb = {
        ssh = "deneb";
        kind = "darwin";
      };
      chuck-herdr-alpha = {
        ssh = "chuck-herdr-alpha";
        kind = "nixos";
      };
    };
    consoles = {
      inherit afterthought;
      agentplot = "/Users/chuck/Code/github_agentplot";
      madswan = afterthought;
      wldn = "/Users/chuck/Code/clients/github_willdan";
    };
    drives = {
      afterthought = {
        blueprints = [ "afterthought/blueprints" ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "afterthought";
        folder = afterthought;
        repos = afterthoughts;
        accounts = every "madswan";
        inherit review;
        flume = standing;
      };
      agentplot = {
        blueprints = [ "agentplot/blueprints" ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "agentplot";
        folder = "/Users/chuck/Code/github_agentplot";
        repos = map (name: "agentplot/${name}") [
          "agentplot"
          "agentplot-kit"
          "blueprints"
          "boomdrive"
          "boomdrive-cloud"
          "boomdrive-web"
          "claude-honcho"
          "crew"
          "eddy"
          "flume"
          "flywheel"
          "flywheel-next"
          "headwater"
          "millpond"
          "nix-agent-deck"
          "nix-claude-plugins"
          "pinout"
          "site-theme"
          "sluice"
          "sounding"
          "strategy"
          "testledger"
          "timber"
          "weir"
        ];
        accounts = every "madswan";
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
        folder = afterthought;
        repos = afterthoughts;
        accounts = every "madswan";
        inherit review;
        flume = standing;
      };
      wldn = {
        blueprints = [ "WilldanGroup/willdan-blueprints" ];
        state = "WilldanGroup/crew-state";
        machine = "chuck-herdr-alpha";
        session = "wldn-2";
        folder = "/workspace";
        repos = [
          "agentplot/crew"
          "WilldanGroup/atlas-kit"
          "WilldanGroup/aws-bootstrap"
          "WilldanGroup/breadboard-kit"
          "WilldanGroup/switchboard-kit"
          "WilldanGroup/willdan-blueprints"
          "WilldanGroup/willdan-sandbox"
        ];
        accounts = every "willdan-alex" // {
          planner = "ia";
          reviewer = "ia";
        };
        inherit review;
        roles.planner.session = "wldn-1";
        flume = standing;
      };
    };
  };
}
