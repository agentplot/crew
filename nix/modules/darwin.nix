# The nix-darwin module, darwinModules.default (record 0058, flake.1):
# services.crew writes crew's teams file from `settings` (json.nix) and
# the activation links it at ~/.config/crew/teams.json as nix-darwin's
# primary user, under their home, given services.crew.host to hold this
# host's name to (activate.sh). crew goes in the system profile. Nothing
# else: no file under /etc, no launchd agent or daemon, no other tool's
# file, since crew runs no service (state.4).
{ packages }:
{
  config,
  lib,
  pkgs,
  ...
}:
let
  cfg = config.services.crew;
  render = import ./json.nix { inherit lib; };
  file = pkgs.writeText "crew-teams.json" (render cfg.settings);

  user = config.system.primaryUser;
  home = if user == null then null else config.users.users.${user}.home or null;
in
{
  imports = [ (import ./options.nix { inherit packages; }) ];

  config = lib.mkIf cfg.enable {
    system.requiresPrimaryUser = [ "services.crew.enable" ];

    assertions = [
      {
        assertion = user == null || home != null;
        message = "services.crew links crew's teams file as nix-darwin's primary user ${toString user}, whose home users.users.${toString user}.home is not set: set it, the home the file is linked under.";
      }
    ];

    environment.systemPackages = [ cfg.package ];

    # Activation runs as root, with root's HOME, so the link is made as the
    # primary user under their own home. A link that fails says why and
    # stops nothing else of the system's activation.
    system.activationScripts.postActivation.text = ''
      sudo --user=${lib.escapeShellArg user} -- /usr/bin/env HOME=${lib.escapeShellArg home} /bin/sh ${./activate.sh} link ${file} ${lib.escapeShellArg cfg.host} || true
    '';
  };
}
