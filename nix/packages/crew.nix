# crew's package (record 0058, flake.1): crew is bash and Python the host
# runs, so nothing compiles. Its source is the tree's plugin/ alone, so no
# other file of the tree changes its path, copied to $out/plugin unpatched,
# as the fleet's is; and $out/bin/crew, a wrapper that puts jq, Python 3.13,
# the hosts' minor (code.1), and recutils (state.1) first on its PATH and
# runs the plugin's own bin/crew. A wrapper, never a link: plugin/bin/crew
# finds its root from its own path unresolved. git, herdr, wt and openspec
# stay the host's.
{
  lib,
  stdenvNoCC,
  runtimeShell,
  jq,
  python313,
  recutils,
  version,
  platforms,
}:
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
  meta = {
    description = "crew: each partition's plan of bolts, its main level of Claude agents, and its bolts' work as Flume runs it";
    homepage = "https://github.com/agentplot/crew";
    mainProgram = "crew";
    inherit platforms;
  };
}
