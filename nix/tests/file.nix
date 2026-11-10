# The crew-flake spec's file (record 0058, flake.2), over options.nix
# evaluated alone beside a system's `assertions`: deneb's drives, keyed by
# label, with their hosts and consoles (record 0064), render
# nix/tests/files/deneb.json byte for byte, their list in label order,
# with its kept repositories nix/tests/files/runner.json (record 0061),
# the version is crew's, and what crew refuses fails
# evaluation, by tryEval where the module system refuses it and by the
# assertions' messages where the module does.
t:
let
  inherit (t) lib;
  render = import ../modules/json.nix { inherit lib; };
  settings = import ./settings.nix;
  inherit (settings) deneb runner;
  pkgs = t.inputs.nixpkgs.legacyPackages.x86_64-linux;

  # options.nix enabled with `given` as its settings, beside the further
  # `modules`: its evaluation, and the config it gives.
  evaluation =
    modules: given:
    lib.evalModules {
      modules = modules ++ [
        (import ../modules/options.nix { inherit (t.outputs) packages; })
        {
          options.assertions = lib.mkOption {
            type = lib.types.listOf lib.types.unspecified;
            default = [ ];
          };
        }
        {
          _module.args = { inherit pkgs; };
          services.crew = {
            enable = true;
            host = "host-a";
            settings = given;
          };
        }
      ];
    };
  evaluated = modules: given: (evaluation modules given).config;

  textBeside = modules: given: render (evaluated modules given).services.crew.settings;
  text = textBeside [ ];
  # Whether `given` renders at all beside `modules`: false where evaluation
  # fails.
  rendersBeside =
    modules: given: (builtins.tryEval (builtins.seq (textBeside modules given) true)).success;
  renders = rendersBeside [ ];
  failuresBeside =
    modules: given:
    map (a: a.message) (lib.filter (a: !a.assertion) (evaluated modules given).assertions);
  failures = failuresBeside [ ];
  says = given: words: lib.hasInfix words (toString (failures given));

  pinned = builtins.readFile ./files/deneb.json;
  rendered = builtins.fromJSON (text deneb);

  # crew.py's VERSION line, read here on its own.
  crewVersion = lib.toInt (
    lib.head (builtins.match ".*\nVERSION = ([0-9]+)\n.*" (builtins.readFile ../../plugin/lib/crew.py))
  );

  # A module giving `drives`' keys, as another module gives a drive's
  # machine and state.
  giving = drives: { services.crew.settings.drives = drives; };
  # deneb's drives from two modules: the machine and state given, crew's
  # own keys the host's.
  split = [ (giving settings.given) ];
  own = {
    drives = settings.own;
    inherit (deneb) hosts consoles;
  };
  # agentplot's machine or state given, beside the host's every key.
  machineTwice = [ (giving { agentplot.machine = "deneb"; }) ];
  stateTwice = [ (giving { agentplot.state = "afterthought/crew-state"; }) ];
  # A drive given its machine and state, which the host names nowhere.
  extra = [
    (giving {
      extra = {
        machine = "deneb";
        state = "afterthought/crew-state";
      };
    })
  ];

  # deneb's drives with afterthought's changed by `change`.
  first =
    change:
    deneb
    // {
      drives = deneb.drives // {
        afterthought = change deneb.drives.afterthought;
      };
    };
  noState = first (p: removeAttrs p [ "state" ]);
  noMachine = first (p: removeAttrs p [ "machine" ]);
  noFolder = first (p: removeAttrs p [ "folder" ]);
  noRepos = first (p: removeAttrs p [ "repos" ]);
  noAccounts = first (p: removeAttrs p [ "accounts" ]);
  relativeFolder = first (p: p // { folder = "work/madswan"; });
  ownerlessRepo = first (p: p // { repos = [ "blueprints" ]; });
  noReviewer = first (p: p // { accounts = removeAttrs p.accounts [ "reviewer" ]; });
  dispatcherAccount = first (p: lib.recursiveUpdate p { accounts.dispatcher = "madswan"; });
  capitalAccount = first (p: lib.recursiveUpdate p { accounts.planner = "Madswan"; });

  # deneb's hosts, and deneb's entry among them changed by `change`.
  denebHost =
    change:
    deneb
    // {
      hosts = deneb.hosts // {
        deneb = change deneb.hosts.deneb;
      };
    };
  noHosts = removeAttrs deneb [ "hosts" ];
  macos = denebHost (h: h // { kind = "macos"; });
  home = denebHost (h: h // { home = "/Users/chuck"; });
  noSsh = denebHost (h: removeAttrs h [ "ssh" ]);
  noKind = denebHost (h: removeAttrs h [ "kind" ]);
  capitalHost = deneb // {
    hosts = deneb.hosts // {
      Deneb = deneb.hosts.deneb;
    };
  };
  # deneb's consoles, wldn's at a relative folder; and none.
  relativeConsole = deneb // {
    consoles = deneb.consoles // {
      wldn = "Code/clients/github_willdan";
    };
  };
  noConsoles = removeAttrs deneb [ "consoles" ];
  dispatcher = first (p: lib.recursiveUpdate p { runs.dispatcher = "standing"; });
  planner = runsPlanner: first (p: lib.recursiveUpdate p { runs.planner = runsPlanner; });
  # afterthought's batch setting by its former names, and out of range.
  formerReview = first (
    p:
    p
    // {
      review = {
        every = 5;
        hours = 4;
      };
    }
  );
  noChanges = first (p: lib.recursiveUpdate p { review.after_changes = 0; });
  noHours = first (p: lib.recursiveUpdate p { review.after_hours = 0; });

  # A drive's options, and those of its `runs` and its `review`, as the
  # module declares them for deneb's settings.
  driveOptions =
    ((evaluation [ ] deneb).options.services.crew.settings.type.getSubOptions [ ])
    .drives.type.nestedTypes.elemType.getSubOptions
      [ ];
  runsOptions = driveOptions.runs.type.getSubOptions [ ];
  reviewOptions = driveOptions.review.type.getSubOptions [ ];
  # Each description the module gives `runs`, `runs.planner`, `review` and
  # its keys, by the option's name.
  descriptions = {
    runs = driveOptions.runs.description;
    "runs.planner" = runsOptions.planner.description;
    review = driveOptions.review.description;
    "review.after_changes" = reviewOptions.after_changes.description;
    "review.after_hours" = reviewOptions.after_hours.description;
  };
  # Whether the description of `option` holds each of `words`.
  describes =
    option: words:
    lib.concatMap (
      word:
      t.expect (lib.hasInfix word
        descriptions.${option}
      ) "the description of ${option} has no ${word}: ${descriptions.${option}}"
    ) words;
  # madswan's drive with the label the host sets.
  labelled = deneb // {
    drives = deneb.drives // {
      madswan = deneb.drives.madswan // {
        label = "madswan";
      };
    };
  };
  # madswan's drive under a name crew does not accept.
  capital = deneb // {
    drives = removeAttrs deneb.drives [ "madswan" ] // {
      Madswan = deneb.drives.madswan;
    };
  };
  # deneb's drives as the file's list, each with its label.
  listed = deneb // {
    drives = lib.mapAttrsToList (label: d: d // { inherit label; }) deneb.drives;
  };
  none = deneb // {
    drives = { };
  };
  teams = deneb // {
    teams = [ ];
  };
  # deneb's drives under the version-5 file's key, with no `drives`.
  partitions = removeAttrs deneb [ "drives" ] // {
    partitions = deneb.drives;
  };

  # runner's settings with crew's kept repository changed by `change`, and
  # with a kept repository named `crew`, with no owner.
  crew =
    change:
    runner
    // {
      repositories = runner.repositories // {
        "agentplot/crew" = change runner.repositories."agentplot/crew";
      };
    };
  noCheckout = crew (e: removeAttrs e [ "checkout" ]);
  relative = crew (e: e // { dir = "repositories/agentplot/crew"; });
  view = crew (e: e // { view = "/Users/chuck/Code/boomdrive/agentplot/crew"; });
  ownerless = runner // {
    repositories = {
      crew = runner.repositories."agentplot/crew";
    };
  };
in
{
  "deneb's drives" =
    t.expect (renders deneb) "deneb's settings do not evaluate"
    ++ lib.optionals (renders deneb) (
      t.expect (
        text deneb == pinned
      ) "deneb's settings render ${text deneb}, not nix/tests/files/deneb.json"
      ++ t.expect (failures deneb == [ ]) "deneb's settings fail: ${toString (failures deneb)}"
      ++ t.expect (
        !(lib.head rendered.drives) ? roles
      ) "afterthought's drive, which gives no roles, renders a roles key"
      ++ t.expect (
        rendered ? hosts && rendered ? consoles && !(rendered ? repositories)
      ) "deneb's file renders without its hosts or consoles, or with repositories"
      ++
        t.expect
          (lib.all (
            d:
            d ? folder
            && d ? repos
            && d ? accounts
            && d ? runs
            && d ? review
            && !(d ? partition)
            && !(d ? flume)
            && !(d.review ? every)
            && !(d.review ? hours)
          ) rendered.drives)
          "a drive of deneb's file renders without its folder, repos, accounts, runs or review, or with a partition, a flume, an every or an hours"
      ++ t.expect (
        map (d: d.label) rendered.drives == [
          "afterthought"
          "agentplot"
          "madswan"
          "wldn"
        ]
      ) "the drives render as ${toString (map (d: d.label or null) rendered.drives)}, not in label order"
    );

  "deneb's drives from two modules" =
    t.expect (rendersBeside split own) "deneb's drives from two modules do not evaluate"
    ++ lib.optionals (rendersBeside split own) (
      t.expect (
        textBeside split own == pinned
      ) "deneb's drives from two modules render ${textBeside split own}, not nix/tests/files/deneb.json"
      ++ t.expect (
        failuresBeside split own == [ ]
      ) "deneb's drives from two modules fail: ${toString (failuresBeside split own)}"
    );

  "A machine written twice" =
    t.expect (!rendersBeside machineTwice deneb)
      "another module and the host's settings both give agentplot the machine deneb, and evaluation holds";

  "A state repository written twice" =
    t.expect (!rendersBeside stateTwice deneb)
      "another module and the host's settings both give agentplot the state afterthought/crew-state, and evaluation holds";

  "A drive given and not configured" = t.expect (
    !rendersBeside extra deneb
  ) "another module gives extra its machine and state, the host names no extra, and evaluation holds";

  "A runner host's kept repositories" =
    t.expect (renders runner) "runner's settings do not evaluate"
    ++ lib.optionals (renders runner) (
      t.expect (
        text runner == builtins.readFile ./files/runner.json
      ) "runner's settings render ${text runner}, not nix/tests/files/runner.json"
      ++ t.expect (failures runner == [ ]) "runner's settings fail: ${toString (failures runner)}"
    )
    ++ t.expect (
      renders deneb && !(rendered ? repositories) && !(lib.hasInfix "repositories" pinned)
    ) "deneb's file, which gives no repositories, has a repositories key";

  "An entry with no checkout" = t.expect (
    !renders noCheckout
  ) "a kept repository with no checkout evaluates";

  "A repository named with no owner" =
    t.expect (
      failures ownerless != [ ]
    ) "services.crew.settings.repositories names crew, and no assertion fails"
    ++
      lib.concatMap
        (
          words:
          t.expect (says ownerless words) "the failure names no ${words}: ${toString (failures ownerless)}"
        )
        [
          "services.crew.settings.repositories"
          "crew, which is no owner/name"
        ];

  "A key crew has no place for" = t.expect (!renders view) "a kept repository giving view evaluates";

  "The version is crew's" =
    t.expect (renders deneb && rendered.version == crewVersion)
      "the module writes version ${
        toString (rendered.version or null)
      }, not crew.py's ${toString crewVersion}"
    ++ t.expect (
      !renders (deneb // { version = 4; })
    ) "a host's settings set version 4, and evaluation holds";

  "A drive with no state repository" = t.expect (!renders noState) "a drive with no state evaluates";

  "A drive with no machine" = t.expect (!renders noMachine) "a drive with no machine evaluates";

  "A drive with no folder, repos or accounts" =
    t.expect (!renders noFolder) "a drive with no folder evaluates"
    ++ t.expect (!renders noRepos) "a drive with no repos evaluates"
    ++ t.expect (!renders noAccounts) "a drive with no accounts evaluates";

  "A relative folder" =
    t.expect (!renders relativeFolder) "a drive whose folder is work/madswan evaluates"
    ++ t.expect (!renders relative) "a kept repository whose dir is relative evaluates";

  "A repos entry with no owner" = t.expect (
    !renders ownerlessRepo
  ) "a drive whose repos names blueprints, with no owner, evaluates";

  "An account left out" =
    t.expect (!renders noReviewer) "a drive whose accounts gives no reviewer evaluates"
    ++ t.expect (!renders dispatcherAccount) "a drive whose accounts names dispatcher evaluates"
    ++ t.expect (!renders capitalAccount) "a drive whose planner's account is Madswan evaluates";

  "No hosts" =
    t.expect (
      !renders noHosts || failures noHosts != [ ]
    ) "settings giving deneb's drives and no hosts evaluate, and no assertion fails"
    ++ lib.optionals (renders noHosts) (
      lib.concatMap
        (
          words: t.expect (says noHosts words) "the failure names no ${words}: ${toString (failures noHosts)}"
        )
        [
          "services.crew.settings.hosts"
          "names no host"
        ]
    );

  "A kind crew does not read" = t.expect (!renders macos) "a host whose kind is macos evaluates";

  "A host's key crew has no place for" =
    t.expect (!renders home) "a host giving home beside its ssh and kind evaluates"
    ++ t.expect (!renders noSsh) "a host with no ssh evaluates"
    ++ t.expect (!renders noKind) "a host with no kind evaluates";

  "A host's name crew does not accept" =
    t.expect (
      failures capitalHost != [ ]
    ) "services.crew.settings.hosts names Deneb, and no assertion fails"
    ++
      lib.concatMap
        (
          words:
          t.expect (says capitalHost words) "the failure names no ${words}: ${toString (failures capitalHost)}"
        )
        [
          "services.crew.settings.hosts"
          "Deneb, which is no name crew accepts"
        ];

  "A relative console folder" = t.expect (
    !renders relativeConsole
  ) "services.crew.settings.consoles.wldn is Code/clients/github_willdan, and evaluation holds";

  "No consoles" =
    t.expect (renders noConsoles) "settings giving no consoles do not evaluate"
    ++ t.expect (
      renders noConsoles && !(builtins.fromJSON (text noConsoles) ? consoles)
    ) "settings giving no consoles render a consoles key";

  "A label the host sets" = t.expect (
    !renders labelled
  ) "the host's settings give madswan the label madswan, and evaluation holds";

  "A name crew does not accept" = t.expect (
    !renders capital
  ) "services.crew.settings.drives names Madswan, and evaluation holds";

  "Drives as a list" = t.expect (
    !renders listed
  ) "services.crew.settings.drives is a list of deneb's drives, and evaluation holds";

  "No drive" =
    t.expect (
      failures none != [ ]
    ) "services.crew.settings.drives names no drive, and no assertion fails"
    ++
      lib.concatMap
        (words: t.expect (says none words) "the failure names no ${words}: ${toString (failures none)}")
        [
          "services.crew.settings.drives"
          "names no drive"
        ];

  # With no `drives`, the drives are none, which the assertion fails.
  "Drives under `partitions`" = t.expect (
    !renders partitions || says partitions "services.crew.settings.drives names no drive"
  ) "services.crew.settings lists its drives under partitions with no drives, and evaluation holds";

  "A role crew has no kind for" =
    t.expect (!renders dispatcher) "a drive's runs names dispatcher, and evaluation holds"
    ++ t.expect (!renders (planner false)) "a drive's runs gives planner false, and evaluation holds"
    ++ t.expect (!renders (planner true)) "a drive's runs gives planner true, and evaluation holds"
    ++ t.expect (
      !renders (planner "always")
    ) "a drive's runs gives planner \"always\", and evaluation holds";

  "A batch setting by its former names" = t.expect (
    !renders formerReview
  ) "a drive's review gives every = 5 and hours = 4, and evaluation holds";

  "A batch setting out of range" =
    t.expect (!renders noChanges) "a drive's review gives after_changes = 0, and evaluation holds"
    ++ t.expect (!renders noHours) "a drive's review gives after_hours = 0, and evaluation holds";

  "The descriptions" =
    describes "runs" [
      ''"standing"''
      ''"on-demand"''
    ]
    ++ describes "runs.planner" [
      ''"standing"''
      ''"on-demand"''
    ]
    ++ describes "review.after_changes" [
      "changes"
      "at least 1"
    ]
    ++ describes "review.after_hours" [
      "hours"
      "above 0"
    ]
    ++ lib.concatLists (
      lib.mapAttrsToList (
        option: description:
        lib.concatMap
          (
            former:
            t.expect (
              !lib.hasInfix former description
            ) "the description of ${option} names ${former}: ${description}"
          )
          [
            "`flume`"
            "every ="
            "hours ="
          ]
      ) descriptions
    );

  "Teams" =
    t.expect (failures teams != [ ]) "services.crew.settings gives teams, and no assertion fails"
    ++
      lib.concatMap
        (words: t.expect (says teams words) "the failure says no ${words}: ${toString (failures teams)}")
        [
          "services.crew.settings.teams"
          "version ${toString crewVersion} has no place for teams"
        ];
}
