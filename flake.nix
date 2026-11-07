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

  outputs = _: { };
}
