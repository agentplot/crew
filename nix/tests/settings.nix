# The crew-flake spec's settings: deneb's four partitions, in the order and
# with the values of deneb's ~/.config/crew/teams.json read 2026-11-07,
# which nix/tests/files/deneb.json holds byte for byte.
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
in
{
  deneb = {
    partitions = [
      {
        label = "afterthought";
        partition = "personal";
        blueprints = [ "afterthought/blueprints" ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "afterthought";
        inherit review;
        flume = standing;
      }
      {
        label = "agentplot";
        partition = "agentplot";
        blueprints = [ "agentplot/blueprints" ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "agentplot";
        inherit review;
        flume = standing;
      }
      {
        label = "madswan";
        partition = "business";
        blueprints = [
          "afterthought/blueprints"
          "agentplot/blueprints"
        ];
        state = "afterthought/crew-state";
        machine = "deneb";
        session = "madswan";
        inherit review;
        flume = standing;
      }
      {
        label = "wldn";
        partition = "clients/willdan";
        blueprints = [ "WilldanGroup/willdan-blueprints" ];
        state = "WilldanGroup/crew-state";
        machine = "chuck-herdr-alpha";
        session = "wldn-2";
        inherit review;
        roles.planner.session = "wldn-1";
        flume = standing;
      }
    ];
  };
}
