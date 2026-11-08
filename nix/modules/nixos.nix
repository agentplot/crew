# The NixOS module, nixosModules.default (record 0058, flake.1):
# services.crew writes crew's teams file from `settings` (json.nix), and
# the user activation of services.crew.user alone links it at
# ~/.config/crew/teams.json, given services.crew.host to hold this host's
# name to (activate.sh). Every user's activation runs at their manager's
# start and at a switch, so the link is made whenever that user's
# processes, crew among them, can run; nothing lingers for it. crew goes in
# the system profile. Nothing else: no file under /etc, no systemd unit,
# no other tool's file, since crew runs no service (state.4).
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
  inherit (cfg) user;
in
{
  imports = [ (import ./options.nix { inherit packages; }) ];

  options.services.crew.user = lib.mkOption {
    type = lib.types.nonEmptyStr;
    example = "alice";
    description = "The user who runs crew, under whose home the teams file is linked.";
  };

  config = lib.mkIf cfg.enable {
    assertions = [
      {
        assertion = config.users.users ? ${user};
        message = "services.crew.user is ${user}, whom users.users.${user} does not declare: declare the user who runs crew, under whose home the teams file is linked.";
      }
    ];

    environment.systemPackages = [ cfg.package ];

    # Run by every user's activation, with coreutils on its PATH and no
    # hostname; any user's but services.crew.user's does nothing. A link
    # that fails says why and stops nothing else.
    system.userActivationScripts.crew.text = ''
      if [ "$(id -un)" = ${lib.escapeShellArg user} ]; then
        ${pkgs.runtimeShell} ${./activate.sh} link ${file} ${lib.escapeShellArg cfg.host} || true
      fi
    '';
  };
}
