# The crew-flake spec on nix-darwin (record 0058, flake.1, flake.2): the
# module evaluated in a system of aarch64-darwin whose primary user is
# alice, at /Users/alice, its activation read as text, its assertions, the
# system profile, the system beside the same one without it, and the module
# imported twice.
t:
let
  inherit (t) lib;
  set = t.outputs.packages.aarch64-darwin;

  base = t.darwinSystem { };
  inherit (base) pkgs;

  # The module's file for deneb's drives: nix/tests/files/deneb.json.
  file = (pkgs.writeText "crew-teams.json" (builtins.readFile ./files/deneb.json)).outPath;

  # Compared as text: a regular expression may not hold a store path.
  activationOf =
    evaluated:
    builtins.unsafeDiscardStringContext evaluated.config.system.activationScripts.script.text;
  # As the primary user, under their home, with the module's file and the
  # host.
  link = builtins.unsafeDiscardStringContext ''
    sudo --user=alice -- /usr/bin/env HOME=/Users/alice /bin/sh ${../modules/activate.sh} link ${file} host-a || true
  '';

  noHome = t.darwinSystem { users.users.alice.home = lib.mkForce null; };
  saysNoHome = words: lib.hasInfix words (toString (t.failures noHome));

  own = t.darwinSystem (
    { pkgs, ... }:
    {
      services.crew.package = pkgs.writeTextDir "bin/crew" "";
    }
  );
  ownPackage = own.config.services.crew.package.outPath;

  # The same system without the module, crew installed in its profile by
  # hand, whose applications the activation copies: what differs is what
  # the module adds beyond the package. crew is given one import deep, as
  # the keyed module gives it, so the profile lists it in the same place.
  off = t.darwinSystem {
    services.crew.enable = lib.mkForce false;
    imports = [ { environment.systemPackages = [ set.crew ]; } ];
  };

  # The module imported again inside another module's imports, as a host
  # imports it directly and through Boomdrive's.
  twice = t.darwinSystem { imports = [ { imports = [ t.outputs.darwinModules.crew ]; } ]; };

  profileOf = evaluated: map (p: p.outPath) evaluated.config.environment.systemPackages;
  holds = evaluated: path: builtins.elem path (profileOf evaluated);

  names = attrs: builtins.attrNames attrs;
  same =
    what: of:
    t.expect (names (of base.config) == names (of off.config))
      "${what} differ beside the system without crew: ${toString (names (of base.config))} and ${toString (names (of off.config))}";
in
{
  "On nix-darwin" =
    t.expect (t.failures base == [ ]) "the system fails: ${toString (t.failures base)}"
    ++ t.expect (lib.hasInfix link (activationOf base)) "the activation runs no `${link}`";

  "A primary user with no home" =
    t.expect (t.failures noHome != [ ]) "the module evaluates for a primary user with no home"
    ++
      lib.concatMap
        (
          words: t.expect (saysNoHome words) "the failure names no ${words}: ${toString (t.failures noHome)}"
        )
        [
          "alice"
          "users.users.alice.home"
        ];

  "The flake's crew" =
    t.expect (holds base set.crew.outPath) "the system profile holds no packages.aarch64-darwin.crew";

  "A host's own crew" =
    t.expect (holds own ownPackage) "the system profile holds no crew of the host's own"
    ++ t.expect (
      !holds own set.crew.outPath
    ) "the system profile holds the flake's crew beside the host's own"
    ++ t.expect (lib.hasInfix link (activationOf own)) "the activation links another file beside a host's own crew";

  "Nothing else on the host" =
    same "environment.etc's files" (c: c.environment.etc)
    ++ same "launchd.agents" (c: c.launchd.agents)
    ++ same "launchd.daemons" (c: c.launchd.daemons)
    ++ same "launchd.user.agents" (c: c.launchd.user.agents)
    ++ same "users.users" (c: c.users.users)
    ++ t.expect (lib.hasInfix link (activationOf base)) "the activation holds no crew's link"
    ++ t.expect (
      builtins.replaceStrings [ link ] [ "" ] (activationOf base) == activationOf off
    ) "the activation, crew's link removed, is not the system's without crew";

  "The module imported twice on nix-darwin" =
    let
      evaluates = (builtins.tryEval twice.system.drvPath).success;
      declared = builtins.length twice.options.services.crew.enable.declarations;
    in
    t.expect evaluates "a system importing the module twice does not evaluate"
    ++ lib.optionals evaluates (
      t.expect (declared == 1) "services.crew.enable is declared ${toString declared} times"
    );
}
