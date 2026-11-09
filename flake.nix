# crew's flake (agentplot/boomdrive record 0023; record 0058, flake.1): crew's
# package, built from this tree's plugin/, and its services.crew module for
# nix-darwin and NixOS, which writes crew's teams file and no other tool's.
# The Boomdrive flake takes it as a locked input and re-exports the module.
# The development shell is devenv's (devenv.nix); everything else of the
# flake's is under nix/, the moon project `nix` (flake.3).
{
  description = "crew: its package and the services.crew module that writes its teams file";

  inputs = {
    # Boomdrive's nixpkgs, so a host's `follows` lines the two up.
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    # The tests' nix-darwin. A host's configuration follows its own, which
    # changes none of the packages.
    nix-darwin = {
      url = "github:nix-darwin/nix-darwin";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    { self, nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      # Boomdrive's systems: nixpkgs refuses x86_64-darwin.
      systems = [
        "aarch64-darwin"
        "aarch64-linux"
        "x86_64-linux"
      ];
      # nixpkgs' form for an untagged commit: crew keeps its version in no
      # file (code.10), and reports its own from git.
      date = self.lastModifiedDate or "19700101";
      version = "0-unstable-${builtins.substring 0 4 date}-${builtins.substring 4 2 date}-${builtins.substring 6 2 date}";

      packages = lib.genAttrs systems (
        system:
        let
          crew = nixpkgs.legacyPackages.${system}.callPackage ./nix/packages/crew.nix {
            inherit version;
            platforms = systems;
            # The commit the package's release file names; none for a tree
            # with uncommitted changes, whose build carries no release.
            commit = self.rev or null;
          };
        in
        {
          inherit crew;
          default = crew;
        }
      );

      # A module of a platform, keyed as Flume's flake keys its own, so a
      # configuration that imports it twice, directly and through
      # Boomdrive's module, declares services.crew once (flake.1).
      moduleOf = platform: file: {
        _file = file;
        key = "github:agentplot/crew#${platform}Modules.crew";
        imports = [ (import file { inherit packages; }) ];
      };
    in
    {
      inherit packages;

      # services.crew, which writes crew's teams file (flake.1, flake.2),
      # its package the flake's own above.
      darwinModules = rec {
        crew = moduleOf "darwin" ./nix/modules/darwin.nix;
        default = crew;
      };
      nixosModules = rec {
        crew = moduleOf "nixos" ./nix/modules/nixos.nix;
        default = crew;
      };
    };
}
