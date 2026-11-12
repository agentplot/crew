# crew's package (record 0058, flake.1): crew is bash and Python the host
# runs, so nothing compiles. Its source is the tree's plugin/ alone, so no
# other file of the tree changes its path, copied to $out/plugin unpatched,
# as the fleet's is; and $out/bin/crew, a wrapper that puts jq, Python 3.13,
# the hosts' minor (code.1), and recutils (state.1) first on its PATH and
# runs the plugin's own bin/crew. A wrapper, never a link: plugin/bin/crew
# finds its root from its own path unresolved. git, herdr, wt and openspec
# stay the host's. The package holds the tree's plugin/release.json, the
# version alone, 0.0.0 on main and the release's at its tag (crew-release),
# which crew reads where it runs from a build (crew_read); where the flake
# knows the commit it is built from, the install writes that commit and the
# package's version over it. A caller names `commit` itself, the flake as
# self.rev or null, since nixpkgs has a package of that name callPackage
# would otherwise pass.
{
  lib,
  stdenvNoCC,
  runtimeShell,
  jq,
  python313,
  recutils,
  version,
  platforms,
  commit ? null,
}:
let
  # What the install writes over the tree's release file: null where the
  # flake knows no commit, as for a tree with uncommitted changes, which
  # then holds the tree's file as the tree gives it.
  release = if commit == null then null else { inherit commit version; };
in
stdenvNoCC.mkDerivation {
  pname = "crew";
  inherit version;
  src = lib.fileset.toSource {
    root = ../..;
    fileset = ../../plugin;
  };
  dontConfigure = true;
  dontBuild = true;
  installPhase = ''
    runHook preInstall
    mkdir -p "$out/bin"
    cp -R plugin "$out/plugin"
    ${lib.optionalString (release != null) ''
      printf '%s\n' ${lib.escapeShellArg (builtins.toJSON release)} >"$out/plugin/release.json"
    ''}
    cat >"$out/bin/crew" <<EOF
    #!${runtimeShell}
    PATH=${
      lib.makeBinPath [
        jq
        python313
        recutils
      ]
    }:\$PATH
    exec "$out/plugin/bin/crew" "\$@"
    EOF
    chmod +x "$out/bin/crew"
    runHook postInstall
  '';
  dontFixup = true;
  passthru = { inherit release; };
  meta = {
    description = "crew: each drive's plan of bolts, its main level of Claude agents, and its bolts' work as Flume runs it";
    homepage = "https://github.com/boomdrivedev/crew";
    mainProgram = "crew";
    inherit platforms;
  };
}
