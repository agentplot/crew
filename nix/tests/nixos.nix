# The crew-flake spec on NixOS (record 0058, flake.1, flake.2): the module
# evaluated in a system of x86_64-linux whose normal users are alice, who
# runs crew, and bob, its user activation read as text, its assertions,
# the system profile, the system beside the same one without it, and the
# module imported twice.
t:
let
  inherit (t) lib;
  set = t.outputs.packages.x86_64-linux;

  base = t.nixosSystem { };
  inherit (base) pkgs;

  # The module's file for deneb's drives: nix/tests/files/deneb.json.
  file = (pkgs.writeText "crew-teams.json" (builtins.readFile ./files/deneb.json)).outPath;

  # Compared as text: a regular expression may not hold a store path.
  activationOf =
    evaluated: builtins.unsafeDiscardStringContext evaluated.config.system.userActivationScripts.script;
  # alice's alone: the link, with the module's file and the host.
  link = builtins.unsafeDiscardStringContext ''
    if [ "$(id -un)" = alice ]; then
      ${pkgs.runtimeShell} ${../modules/activate.sh} link ${file} host-a || true
    fi
  '';

  noUser = t.nixosSystem { services.crew.user = lib.mkForce "carol"; };
  saysNoUser = words: lib.hasInfix words (toString (t.failures noUser));

  own = t.nixosSystem (
    { pkgs, ... }:
    {
      services.crew.package = pkgs.writeTextDir "bin/crew" "";
    }
  );
  ownPackage = own.config.services.crew.package.outPath;

  # The same system without the module, crew installed in its profile by
  # hand: what differs is what the module adds beyond the package.
  off = t.nixosSystem {
    services.crew.enable = lib.mkForce false;
    environment.systemPackages = [ set.crew ];
  };

  # The module imported again inside another module's imports, as a host
  # imports it directly and through Boomdrive's.
  twice = t.nixosSystem { imports = [ { imports = [ t.outputs.nixosModules.crew ]; } ]; };

  profileOf = evaluated: map (p: p.outPath) evaluated.config.environment.systemPackages;
  holds = evaluated: path: builtins.elem path (profileOf evaluated);

  names = attrs: builtins.attrNames attrs;
  same =
    what: of:
    t.expect (names (of base.config) == names (of off.config))
      "${what} differ beside the system without crew: ${toString (names (of base.config))} and ${toString (names (of off.config))}";
  # The user activation's text without the snippet `name`: NixOS frames
  # each snippet from its headline to the next one's, or to the script's
  # exit.
  without =
    name: text:
    lib.concatStringsSep "\n"
      (builtins.foldl'
        (
          state: line:
          let
            skipping =
              line == "#### Activation script snippet ${name}:"
              || (
                state.skipping
                && !(lib.hasPrefix "#### Activation script snippet " line || lib.hasPrefix "exit $_status" line)
              );
          in
          {
            inherit skipping;
            kept = state.kept ++ lib.optional (!skipping) line;
          }
        )
        {
          skipping = false;
          kept = [ ];
        }
        (lib.splitString "\n" text)
      ).kept;
  lingers =
    config:
    map (user: config.users.users.${user}.linger) [
      "alice"
      "bob"
    ];
in
{
  "On NixOS" =
    t.expect (t.failures base == [ ]) "the system fails: ${toString (t.failures base)}"
    ++ t.expect (lib.hasInfix link (activationOf base)) "the user activation runs no `${link}`";

  "A user the system does not declare" =
    t.expect (t.failures noUser != [ ]) "the module evaluates for a user users.users does not declare"
    ++
      lib.concatMap
        (
          words: t.expect (saysNoUser words) "the failure names no ${words}: ${toString (t.failures noUser)}"
        )
        [
          "services.crew.user"
          "users.users.carol"
        ];

  "The flake's crew on NixOS" =
    t.expect (holds base set.crew.outPath) "the system profile holds no packages.x86_64-linux.crew";

  "A host's own crew on NixOS" =
    t.expect (holds own ownPackage) "the system profile holds no crew of the host's own"
    ++ t.expect (
      !holds own set.crew.outPath
    ) "the system profile holds the flake's crew beside the host's own"
    ++ t.expect (lib.hasInfix link (activationOf own)) "the user activation links another file beside a host's own crew";

  "Nothing else on the host on NixOS" =
    same "environment.etc's files" (c: c.environment.etc)
    ++ same "systemd.services" (c: c.systemd.services)
    ++ same "systemd.user.services" (c: c.systemd.user.services)
    ++ same "users.users" (c: c.users.users)
    ++
      t.expect (lingers base.config == lingers off.config)
        "alice's and bob's linger are ${builtins.toJSON (lingers base.config)}, beside ${builtins.toJSON (lingers off.config)} without crew"
    ++ t.expect (lib.hasInfix link (activationOf base)) "the user activation holds no crew's link"
    ++ t.expect (
      without "crew" (activationOf base) == activationOf off
    ) "the user activation, crew's snippet removed, is not the system's without crew";

  "The module imported twice on NixOS" =
    let
      evaluates = (builtins.tryEval twice.config.system.build.toplevel.drvPath).success;
      declared = builtins.length twice.options.services.crew.enable.declarations;
    in
    t.expect evaluates "a system importing the module twice does not evaluate"
    ++ lib.optionals evaluates (
      t.expect (declared == 1) "services.crew.enable is declared ${toString declared} times"
    );
}
