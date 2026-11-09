# services.crew, the options both modules share (record 0058, flake.2),
# given the flake's own `packages`: crew's package, the flake's own for the
# host's system unless the host gives its own; `host`, this host as
# `hostname -s` names it, which is no key of the file; and `settings`,
# crew's teams file, each key named as the file names it, free-form JSON
# with what crew.load requires declared for its type and with no default
# (code.5), so a key the module does not declare passes to the file and
# crew judges it (RFC 42); `drives`, keyed by each drive's label, which
# json.nix writes as the file's list in label order, each with its herdr
# session's `folder`, the `repos` it keeps and the Claude account each of
# its roles runs under (`accounts`); `hosts`, each host crew reaches or
# reads, exactly its `ssh` name and its `kind` (record 0064); `consoles`,
# the drives whose console this host opens, each with its folder;
# `repositories`, the host's kept repositories (record 0061), each exactly
# an absolute `dir` and `checkout`. Which keys agree with which (a
# machine with no host, a blueprints repo not kept, two accounts in one
# session) is crew's to judge at load. `version` is crew's own, read from
# plugin/lib/crew.py, and no host sets it.
{ packages }:
{
  config,
  lib,
  pkgs,
  ...
}:
let
  inherit (lib) mkOption types;
  cfg = config.services.crew;
  json = (pkgs.formats.json { }).type;

  inherit (pkgs.stdenv.hostPlatform) system;
  set =
    packages.${system}
      or (throw "crew's flake gives no packages for ${system}: it gives ${lib.concatStringsSep ", " (builtins.attrNames packages)}");

  # The teams file's version crew reads, from crew.py's line
  # `VERSION = <n>`: one source, so the module and the crew of one commit
  # never name two versions.
  versions = lib.filter (m: m != null) (
    map (builtins.match "VERSION = ([0-9]+)") (
      lib.splitString "\n" (builtins.readFile ../../plugin/lib/crew.py)
    )
  );
  version =
    if versions == [ ] then
      throw "services.crew: crew's plugin/lib/crew.py has no line `VERSION = <n>`, the teams file's version crew reads"
    else
      lib.toInt (lib.head (lib.head versions));

  # A name crew mints or accepts (code.4), a GitHub repository, and an
  # absolute path.
  crewName = types.strMatching "[a-z0-9][a-z0-9-]*";
  repository = types.strMatching "[^/[:space:]]+/[^/[:space:]]+";
  absolute = types.strMatching "/.*";

  # crew.py's KIND_ROLES, MAIN_ROLES and EFFORTS.
  kindRoles = [
    "design"
    "planner"
    "reviewer"
    "ops"
    "operator"
  ];
  mainRoles = [
    "design"
    "planner"
    "main-ops"
    "operator"
    "reviewer"
  ];
  efforts = [
    "low"
    "medium"
    "high"
    "xhigh"
    "max"
  ];

  # A list or attribute set the host gives, even where empty: the module
  # system gives such a type's empty value to an option no definition
  # sets, which here is a key crew requires, so it has none.
  required = type: type // { emptyValue = { }; };

  unset =
    type: description:
    mkOption {
      type = types.nullOr type;
      default = null;
      inherit description;
    };

  review = types.submodule {
    options = {
      every = mkOption {
        type = types.ints.positive;
        description = "How many of the drive's constructed changes make a batch.";
      };
      hours = mkOption {
        type = types.addCheck types.number (n: n > 0) // {
          name = "positiveNumber";
          description = "positive number";
        };
        description = "How many hours make a batch due.";
      };
    };
  };

  # Every role of KIND_ROLES, and no other: false while it stands, or the
  # name of the Flume stream its runs run in on the main level's host.
  flume = types.submodule {
    options = lib.genAttrs kindRoles (
      role:
      mkOption {
        type = types.either (types.enum [ false ]) crewName;
        description = "The ${role}'s Flume setting: false while it stands, or the name of the Flume stream its runs run in.";
      }
    );
  };

  # The kinds of host crew reads (crew.py's HOST_KINDS).
  hostKinds = [
    "darwin"
    "nixos"
  ];
  # A host crew reaches or reads (record 0064): exactly its ssh name and
  # its kind, with no default and no other key, since the submodule
  # declares no free-form type.
  host = types.submodule {
    options = {
      ssh = mkOption {
        type = types.nonEmptyStr;
        description = "The name ssh reaches the host by.";
      };
      kind = mkOption {
        type = types.enum hostKinds;
        description = "The host's kind, darwin or nixos: whether it is a Mac is all crew reads of it.";
      };
    };
  };

  # Every role of KIND_ROLES, and no other, with the Claude account it
  # runs under, with no default.
  accounts = types.submodule {
    options = lib.genAttrs kindRoles (
      role:
      mkOption {
        type = crewName;
        description = "The Claude account the ${role} runs under.";
      }
    );
  };

  role = types.submodule {
    options = {
      model = unset types.nonEmptyStr "The model the role runs on, over its definition's.";
      effort = unset (types.enum efforts) "The effort the role runs at, over its definition's.";
      session = unset types.nonEmptyStr "The herdr session of the main level's machine the role runs in.";
    };
  };

  # A drive, under its label's name in services.crew.settings.drives.
  drive = types.submodule (
    { name, ... }:
    {
      freeformType = json;
      options = {
        label = mkOption {
          type = crewName;
          default = name;
          readOnly = true;
          description = "The drive's label, its name under services.crew.settings.drives, which names its main level and its state branch `<label>/main`; no host sets it.";
        };
        blueprints = mkOption {
          type = types.nonEmptyListOf repository;
          description = "The drive's blueprints repositories, each `owner/name`, the first the one its main level works in.";
        };
        state = mkOption {
          type = types.unique {
            message = "A drive's state repository is written once: where another module gives it, the host's configuration writes it nowhere else in services.crew.settings, and each place that writes it is named below.";
          } repository;
          description = "The drive's state repository, `owner/name`, whose branch `<label>/main` holds its plan and run record; written once, by the host's settings or by another module that gives it by the drive's label.";
        };
        machine = mkOption {
          type = types.unique {
            message = "A drive's machine is written once: where another module gives it, the host's configuration writes it nowhere else in services.crew.settings, and each place that writes it is named below.";
          } crewName;
          description = "The host its main level runs on, as `hostname -s` names it; written once, by the host's settings or by another module that gives it by the drive's label.";
        };
        session = mkOption {
          type = types.nonEmptyStr;
          description = "The herdr session its main level runs in.";
        };
        folder = mkOption {
          type = absolute;
          description = "The absolute folder of its herdr session on its machine, which keeps the repositories its `repos` lists, each at `<folder>/<name>`.";
        };
        repos = mkOption {
          type = required (types.listOf repository);
          description = "The repositories its folder keeps on its machine, each by its address, `owner/name`; none where a host's `repositories` names them.";
        };
        accounts = mkOption {
          type = accounts;
          description = "The Claude account each of its main-level roles runs under.";
        };
        review = mkOption {
          type = review;
          description = "The drive's batch setting: a batch is due every `every` changes or every `hours` hours.";
        };
        flume = mkOption {
          type = flume;
          description = "The Flume setting of each of its main-level roles.";
        };
        roles = unset (types.submodule {
          options = lib.genAttrs mainRoles (main: unset role "The ${main}'s model, effort or session.");
        }) "Each main-level role's model, effort or session, over its definition's; none where unset.";
      };
    }
  );

  # A kept repository of this host (record 0061): exactly the folder crew
  # names as the kit's, where worktrees are cut, and the working tree it
  # names as the kit's checkout, each an absolute path with no default, and
  # no other key, since the submodule declares no free-form type.
  kept = types.submodule {
    options = {
      dir = mkOption {
        type = absolute;
        description = "The repository's folder, an absolute path, which crew names as the kit's and where worktrees are cut: the runner's container on a runner host.";
      };
      checkout = mkOption {
        type = absolute;
        description = "The repository's checkout, an absolute path, the working tree crew names as the kit's main checkout: the runner's view on a runner host.";
      };
    };
  };

  # Each kept repository's key is its address, `owner/name`.
  addresses =
    if cfg.settings.repositories == null then [ ] else builtins.attrNames cfg.settings.repositories;
  unaddressed = lib.filter (r: builtins.match "[^/[:space:]]+/[^/[:space:]]+" r == null) addresses;
  # Each host's key is a name crew accepts, as `hostname -s` names it.
  unnamed = lib.filter (h: builtins.match "[a-z0-9][a-z0-9-]*" h == null) (
    builtins.attrNames cfg.settings.hosts
  );
in
{
  options.services.crew = {
    enable = lib.mkEnableOption "crew's teams file, linked for the user who runs crew, and crew in the system profile";

    package = mkOption {
      type = types.package;
      default = set.crew;
      defaultText = lib.literalExpression "crew.packages.\${pkgs.stdenv.hostPlatform.system}.crew";
      description = "crew: the flake's, or a host's own laid out the same, `plugin/` and `bin/crew`.";
    };

    host = mkOption {
      type = crewName;
      example = "deneb";
      description = "This host, as `hostname -s` names it and the drives' `machine` names a host. It is no key of the file: crew reads its host from `hostname -s`.";
    };

    settings = mkOption {
      type = types.submodule {
        freeformType = json;
        options = {
          version = mkOption {
            type = types.int;
            default = version;
            readOnly = true;
            description = "The teams file's version, crew's own, read from plugin/lib/crew.py; no host sets it.";
          };
          drives = mkOption {
            type = types.attrsOf drive;
            description = "Every drive, by its label, with its `machine`.";
          };
          hosts = mkOption {
            type = types.attrsOf host;
            description = "Each host crew reaches or reads, by its name as `hostname -s` gives it, with its `ssh` name and its `kind`; every drive's `machine` among them.";
          };
          consoles = unset (types.attrsOf absolute) "The drives whose console this host opens, each by its label, with the absolute folder its console's tabs open in; none where unset, and the file then names none.";
          repositories = unset (types.attrsOf kept) "The repositories this host keeps, each by its address, `owner/name`, with its `dir` and its `checkout`, which crew names on this host as the kit's folder and checkout; none where unset, and the file then names none.";
        };
      };
      description = "crew's teams file, `~/.config/crew/teams.json`, each key named as the file names it, rendered at evaluation.";
    };
  };

  config = lib.mkIf cfg.enable {
    assertions = [
      {
        assertion = cfg.settings.drives != { };
        message = "services.crew.settings.drives names no drive: crew's teams file lists every drive, by its label.";
      }
      {
        assertion = unaddressed == [ ];
        message = "services.crew.settings.repositories names ${lib.concatStringsSep ", " unaddressed}, which is no owner/name: each kept repository is named by its address.";
      }
      {
        assertion = cfg.settings.hosts != { };
        message = "services.crew.settings.hosts names no host: crew's teams file names each host crew reaches or reads, every drive's machine among them, with its ssh name and kind.";
      }
      {
        assertion = unnamed == [ ];
        message = "services.crew.settings.hosts names ${lib.concatStringsSep ", " unnamed}, which is no name crew accepts: each host is named as `hostname -s` gives it.";
      }
      {
        assertion = !(cfg.settings ? teams);
        message = "services.crew.settings.teams is set, and crew's teams file at version ${toString version} has no place for teams: crew runs no team.";
      }
    ];
  };
}
