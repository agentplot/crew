"""crew drive set <label> (drive-setup; design of crew-makes-a-new-drives-state): crew.drive_given for the drive its
flags give, read by plan.py's own parser as the command reads them, each flag left out, repeated or given a value crew
does not accept refused naming it; crew.teams_set and crew.teams_text for the file it writes, the drive's entry replaced
whole and the rest kept, in the bytes crew's module writes; crew.teams_step for what it does to the file as it stands;
and crew.drive_said for its answer. The command's wiring, its lock, its state and its entry, is t-drive-set's."""
import json
import pathlib

import pytest

import crew
import plan

FILES = pathlib.Path(__file__).resolve().parents[2] / "nix/tests/files"
MAC = "pats-mac"
FOLDER = "/Users/pat/.local/share/herdr/pat"
KEPT = ("/Users/pat/.local/share/boomdrive/repositories/pat/blueprints", "/Users/pat/Code/pat/blueprints")


def flags(label="pat", leave=(), **more):
    """A person's Mac's flags for crew drive set (Task notes 2.1): drive pat on pats-mac, its state pat/crew-state, its
    blueprints pat/blueprints, kept at the runner's container and view, every role on the account pat and standing,
    review 5 and 4, its console its folder. leave names flags left out; more gives a flag's words in place of these,
    a list of words, or a list of lists for a flag given several times."""
    given = {"--state": ["pat/crew-state"], "--blueprints": ["pat/blueprints"], "--machine": [MAC], "--session": ["pat"],
             "--folder": [FOLDER], "--repos": ["pat/blueprints"],
             "--accounts": [[r, "pat"] for r in crew.KIND_ROLES], "--flume": [[r, "false"] for r in crew.KIND_ROLES],
             "--review": ["5", "4"], "--hosts": [MAC, MAC, "darwin"], "--console": [FOLDER],
             "--repositories": ["pat/blueprints", *KEPT]}
    given.update({f"--{k}": v for k, v in more.items()})
    argv = ["drive", "set", label]
    for flag, words in given.items():
        if flag in leave or words is None:
            continue
        for w in (words if words and isinstance(words[0], list) else [words]):
            argv += [flag, *w]
    return argv


def parsed(argv):
    return plan.parser().parse_args(argv)


def given(here=MAC, **kw):
    return crew.drive_given(parsed(flags(**kw)), here)


class TestDriveGiven:
    """drive-setup, "Every key is a flag, with no default", "A flag crew does not accept is refused before anything is
    read" and "The flags agree before anything is read" (design, Decision 2)."""

    def refused(self, said, here=MAC, **kw):
        with pytest.raises(crew.Refusal) as e:
            given(here, **kw)
        assert said in str(e.value), str(e.value)
        assert str(e.value).startswith("crew drive set ") and str(e.value).endswith("nothing was read or written")
        return str(e.value)

    def test_a_persons_mac(self):
        """drive-setup, A person's Mac: every key from its flag, the review whole numbers, no roles where none given."""
        g = given()
        assert g["drive"] == {
            "label": "pat", "blueprints": ["pat/blueprints"], "state": "pat/crew-state", "machine": MAC, "session": "pat",
            "folder": FOLDER, "repos": ["pat/blueprints"], "accounts": {r: "pat" for r in crew.KIND_ROLES},
            "flume": {r: False for r in crew.KIND_ROLES}, "review": {"every": 5, "hours": 4}}
        assert g["hosts"] == {MAC: {"ssh": MAC, "kind": "darwin"}} and g["console"] == FOLDER
        assert g["repositories"] == {"pat/blueprints": {"dir": KEPT[0], "checkout": KEPT[1]}}

    def test_the_optional_flags_left_out_give_no_console_no_kept_repository_and_no_roles(self):
        g = given(leave=("--console", "--repositories", "--roles"))
        assert g["console"] is None and g["repositories"] == {} and "roles" not in g["drive"]

    def test_several_blueprints_repos_hosts_and_streams_and_a_roles_override(self):
        g = given(blueprints=[["pat/blueprints"], ["pat/notes"]], repos=[["pat/app"], ["pat/blueprints"], ["pat/notes"]],
                  hosts=[[MAC, MAC, "darwin"], ["box-1", "box-1.tail", "nixos"]],
                  flume=[[r, "pat-work" if r == "planner" else "false"] for r in crew.KIND_ROLES],
                  roles=[["planner", "effort", "max"], ["planner", "session", "pat-2"], ["main-ops", "model", "claude-opus-5-5"]],
                  review=["3", "1.5"])
        d = g["drive"]
        assert d["blueprints"] == ["pat/blueprints", "pat/notes"] and d["repos"] == ["pat/app", "pat/blueprints", "pat/notes"]
        assert d["flume"]["planner"] == "pat-work" and d["flume"]["ops"] is False
        assert d["roles"] == {"planner": {"effort": "max", "session": "pat-2"}, "main-ops": {"model": "claude-opus-5-5"}}
        assert d["review"] == {"every": 3, "hours": 1.5} and set(g["hosts"]) == {MAC, "box-1"}

    def test_hours_given_as_a_whole_number_with_a_point_is_whole(self):
        assert given(review=["5", "4.0"])["drive"]["review"] == {"every": 5, "hours": 4}
        assert type(given(review=["5", "4.0"])["drive"]["review"]["hours"]) is int

    @pytest.mark.parametrize("flag", ["--state", "--blueprints", "--machine", "--session", "--folder", "--repos", "--accounts",
                                      "--flume", "--review", "--hosts"])
    def test_each_required_flag_left_out_is_refused_naming_it(self, flag):
        """drive-setup, A flag left out: every flag of a key crew requires, and --hosts, is required."""
        self.refused(f"crew drive set pat: {flag} is required", leave=(flag,))

    @pytest.mark.parametrize("flag, words", [("state", [["pat/crew-state"], ["pat/other-state"]]), ("machine", [[MAC], [MAC]]),
                                             ("session", [["pat"], ["pat-2"]]), ("folder", [[FOLDER], ["/elsewhere"]]),
                                             ("review", [["5", "4"], ["5", "4"]]), ("console", [[FOLDER], [FOLDER]])])
    def test_a_flag_given_past_its_count_is_refused_naming_it(self, flag, words):
        self.refused(f"--{flag} is given 2 times, and it is given once", **{flag: words})

    @pytest.mark.parametrize("flag", ["accounts", "flume"])
    def test_a_role_left_out_named_twice_or_unknown_is_refused_naming_the_flag_and_the_role(self, flag):
        """drive-setup, An account left out: refused naming --accounts and the reviewer."""
        value = "pat" if flag == "accounts" else "false"
        others = [[r, value] for r in crew.KIND_ROLES if r != "reviewer"]
        self.refused(f"--{flag} leaves out the reviewer: it is given once for each role", **{flag: others})
        self.refused(f"--{flag} names the planner twice", **{flag: others + [["reviewer", value], ["planner", value]]})
        self.refused(f"--{flag} names dispatcher, which is no main-level role", **{flag: others + [["dispatcher", value]]})
        self.refused(f"--{flag} names main-ops, which is no main-level role", **{flag: others + [["main-ops", value]]})

    def test_an_account_crew_does_not_accept_is_refused(self):
        self.refused("--accounts gives the ops \"Pat Smith\", which is no Claude account's name crew accepts",
                     accounts=[[r, "Pat Smith" if r == "ops" else "pat"] for r in crew.KIND_ROLES])

    @pytest.mark.parametrize("value", ["true", "False", "Pat Work", ""])
    def test_a_flume_setting_that_is_no_streams_name_is_refused(self, value):
        self.refused(f"--flume gives the planner {json.dumps(value)}, which is false or the name of a Flume stream",
                     flume=[[r, value if r == "planner" else "false"] for r in crew.KIND_ROLES])

    @pytest.mark.parametrize("review, said", [(["0", "4"], "--review gives \"0\" changes a batch"),
                                              (["five", "4"], "--review gives \"five\" changes a batch"),
                                              (["2.5", "4"], "--review gives \"2.5\" changes a batch"),
                                              (["5", "0"], "--review gives \"0\" hours a batch, and that is a number above 0"),
                                              (["5", "-1"], "--review gives \"-1\" hours"), (["5", "inf"], "--review gives \"inf\" hours")])
    def test_a_review_crew_does_not_read_is_refused(self, review, said):
        self.refused(said, review=review)

    def test_a_host_named_wrongly_is_refused(self):
        self.refused("--hosts gives pats-mac the kind \"macos\", which is darwin or nixos", hosts=[MAC, MAC, "macos"])
        self.refused("--hosts names \"Pats-Mac\", which is no host's name crew accepts", hosts=["Pats-Mac", MAC, "darwin"])
        self.refused("--hosts names pats-mac twice", hosts=[[MAC, MAC, "darwin"], [MAC, "other", "darwin"]])
        self.refused("--hosts gives pats-mac no ssh name", hosts=[MAC, "", "darwin"])

    @pytest.mark.parametrize("flag, value", [("folder", "work/pat"), ("console", "herdr/pat")])
    def test_a_relative_folder_or_console_is_refused(self, flag, value):
        self.refused(f"--{flag} is an absolute path, not {json.dumps(value)}", **{flag: [value]})

    def test_a_relative_kept_folder_or_checkout_is_refused(self):
        self.refused("--repositories is an absolute path, not \"repositories/pat/blueprints\"",
                     repositories=["pat/blueprints", "repositories/pat/blueprints", KEPT[1]])
        self.refused("--repositories names \"blueprints\", which is no <owner>/<name>", repositories=["blueprints", *KEPT])

    def test_an_address_that_is_none_or_a_label_crew_does_not_accept_is_refused(self):
        self.refused("--state names \"crew-state\", which is no <owner>/<name>", state=["crew-state"])
        self.refused("--repos names \"pat/blueprints extra\", which is no <owner>/<name>", repos=["pat/blueprints extra"])
        with pytest.raises(crew.Refusal, match="a drive's label is lowercase words with dashes, not \"Pat\""):
            given(label="Pat")

    def test_a_roles_override_crew_has_no_place_for_is_refused(self):
        self.refused("--roles names conductor, which crew has no definition for", roles=["conductor", "effort", "max"])
        self.refused("--roles sets planner's \"account\"", roles=["planner", "account", "ia"])
        self.refused("--roles sets planner's effort to \"extreme\", which is no effort level", roles=["planner", "effort", "extreme"])
        self.refused("--roles sets planner's effort twice", roles=[["planner", "effort", "max"], ["planner", "effort", "high"]])

    def test_a_first_blueprints_repo_not_among_repos_is_refused(self):
        """drive-setup, A blueprints repo it does not keep: refused naming pat/blueprints and --repos."""
        said = self.refused("--blueprints names pat/blueprints first", repos=["pat/app"], leave=("--repositories",))
        assert "--repos does not name it" in said

    def test_a_machine_not_among_hosts_is_refused(self):
        self.refused("--machine is box-1, which --hosts does not name", machine=["box-1"], leave=("--repositories",))

    def test_a_kept_address_not_among_repos_is_refused(self):
        self.refused("--repositories names pat/app, which --repos does not", repositories=[["pat/blueprints", *KEPT], ["pat/app", *KEPT]])

    def test_kept_repositories_of_another_host_are_refused(self):
        """drive-setup, Kept repositories of another host: --machine box-1, run on pats-mac."""
        self.refused("--repositories names the kept repositories of the host crew drive set runs on, pats-mac, and the drive's "
                     "machine is box-1", machine=["box-1"], hosts=[[MAC, MAC, "darwin"], ["box-1", "box-1", "nixos"]])
        assert given(leave=("--repositories",), machine=["box-1"], hosts=[["box-1", "box-1", "nixos"]])["drive"]["machine"] == "box-1"


def lab_flags(**more):
    """A second drive, lab, on the same host."""
    return dict(dict(state=["lab/crew-state"], blueprints=["lab/blueprints"], repos=["lab/blueprints"], session=["lab"],
                     folder=["/Users/pat/lab"], console=["/Users/pat/lab"], repositories=None), **more)


class TestSettable:
    """drive-setup, A part of another shape (a-drive-set-mends-what-it-replaces, Decision 3): crew.settable refuses a
    teams file's data whose parts crew drive set could not keep beside the drive, naming the key."""

    def refused(self, data, said):
        with pytest.raises(crew.Refusal) as e:
            crew.settable(data)
        assert said in str(e.value), str(e.value)

    def test_absent_and_null_parts_pass(self):
        assert crew.settable({"version": 6}) is None
        assert crew.settable({"version": 6, "drives": None, "hosts": None, "consoles": None, "repositories": None}) is None

    @pytest.mark.parametrize("drives", [{}, "pat"])
    def test_drives_that_are_no_list_are_refused(self, drives):
        self.refused({"version": 6, "drives": drives}, "'drives' lists each drive as an object, not ")

    def test_a_drive_that_is_no_object_is_refused(self):
        self.refused({"version": 6, "drives": ["pat"]}, "'drives' lists \"pat\", which is no drive's object")

    @pytest.mark.parametrize("key, value", [("hosts", []), ("consoles", []), ("repositories", "x")])
    def test_hosts_consoles_or_repositories_that_are_no_object_are_refused(self, key, value):
        self.refused({"version": 6, key: value}, f"'{key}' is an object, not ")


class TestTeamsSet:
    """drive-setup, "The drive's facts are replaced and the rest of the file is kept", "A kept repository stays while a
    drive of the host keeps it" and "The file is written as crew's module writes it" (design, Decisions 3, 4 and 10;
    a-drive-set-mends-what-it-replaces, Decisions 3 and 4)."""

    def set(self, data, here=MAC, **kw):
        return crew.teams_set(data, given(here, **kw), here)

    def test_a_new_file_from_no_file(self):
        data, changed = self.set(None)
        assert data == {"version": crew.VERSION, "drives": [given()["drive"]], "hosts": {MAC: {"ssh": MAC, "kind": "darwin"}},
                        "consoles": {"pat": FOLDER}, "repositories": {"pat/blueprints": {"dir": KEPT[0], "checkout": KEPT[1]}}}
        assert changed == ["drives.pat", f"hosts.{MAC}", "consoles.pat", "repositories.pat/blueprints"]
        assert crew.fleet_of(data, MAC)["drives"]["pat"]["checkout"] == KEPT[1]

    def test_a_second_drive_is_added_and_the_first_kept_byte_for_byte(self):
        """drive-setup, A second drive: the file names lab and pat, pat's entry as it was."""
        first, _ = self.set(None)
        data, changed = self.set(first, label="lab", **lab_flags())
        assert [d["label"] for d in data["drives"]] == ["lab", "pat"]
        assert crew.teams_text(data["drives"][1]) == crew.teams_text(first["drives"][0])
        assert data["consoles"] == {"lab": "/Users/pat/lab", "pat": FOLDER} and data["repositories"] == first["repositories"]
        assert changed == ["drives.lab", "consoles.lab"]

    def test_the_drives_entry_is_replaced_whole_a_roles_override_no_longer_given_gone(self):
        """drive-setup, A role's override no longer given: the file's pat has no roles."""
        first, _ = self.set(None, roles=["planner", "effort", "max"])
        assert first["drives"][0]["roles"] == {"planner": {"effort": "max"}}
        data, changed = self.set(first, session=["pat-2"])
        assert "roles" not in data["drives"][0] and data["drives"][0]["session"] == "pat-2"
        assert changed == ["drives.pat.roles", "drives.pat.session"]

    def test_a_host_is_added_and_one_replaced_and_another_kept(self):
        first, _ = self.set(None, hosts=[[MAC, MAC, "darwin"], ["box-1", "box-1", "nixos"]])
        data, changed = self.set(first, hosts=[[MAC, "pats-mac.tail", "darwin"], ["box-2", "box-2", "nixos"]])
        assert data["hosts"] == {MAC: {"ssh": "pats-mac.tail", "kind": "darwin"}, "box-1": {"ssh": "box-1", "kind": "nixos"},
                                 "box-2": {"ssh": "box-2", "kind": "nixos"}}
        assert changed == ["hosts.box-2", f"hosts.{MAC}"]

    def test_a_console_is_set_and_one_removed_consoles_left_out_when_empty(self):
        first, _ = self.set(None, leave=("--console",))
        assert "consoles" not in first
        data, changed = self.set(first, console=["/Users/pat/elsewhere"])
        assert data["consoles"] == {"pat": "/Users/pat/elsewhere"} and changed == ["consoles.pat"]
        data, changed = self.set(data, leave=("--console",))
        assert "consoles" not in data and changed == ["consoles.pat"]

    def test_a_repository_removed_from_the_drive_leaves_repositories(self):
        """drive-setup, A repository removed from the drive: no other drive of the host lists pat/app."""
        first, _ = self.set(None, repos=[["pat/app"], ["pat/blueprints"]],
                            repositories=[["pat/app", "/r/pat/app", "/v/pat/app"], ["pat/blueprints", *KEPT]])
        data, changed = self.set(first, repos=["pat/blueprints"])
        assert data["drives"][0]["repos"] == ["pat/blueprints"] and set(data["repositories"]) == {"pat/blueprints"}
        assert changed == ["drives.pat.repos", "repositories.pat/app"]
        data, _ = self.set(data, leave=("--repositories",))
        assert "repositories" not in data

    def test_a_repository_another_drive_of_the_host_keeps_stays(self):
        """drive-setup, A repository another drive keeps: pat and lab both run on this host and list pat/app."""
        first, _ = self.set(None, repos=[["pat/app"], ["pat/blueprints"]],
                            repositories=[["pat/app", "/r/pat/app", "/v/pat/app"], ["pat/blueprints", *KEPT]])
        both, _ = self.set(first, label="lab", **lab_flags(repos=[["lab/blueprints"], ["pat/app"]]))
        data, _ = self.set(both, repos=["pat/blueprints"])
        assert data["repositories"]["pat/app"] == {"dir": "/r/pat/app", "checkout": "/v/pat/app"}

    def test_a_repository_a_drive_of_another_host_lists_does_not_keep_it(self):
        first, _ = self.set(None, repos=[["pat/app"], ["pat/blueprints"]],
                            repositories=[["pat/app", "/r/pat/app", "/v/pat/app"], ["pat/blueprints", *KEPT]],
                            hosts=[[MAC, MAC, "darwin"], ["box-1", "box-1", "nixos"]])
        both, _ = self.set(first, label="lab", **lab_flags(repos=[["lab/blueprints"], ["pat/app"]], machine=["box-1"],
                                                                hosts=["box-1", "box-1", "nixos"], console=None))
        data, _ = self.set(both, repos=["pat/blueprints"], hosts=[[MAC, MAC, "darwin"]])
        assert set(data["repositories"]) == {"pat/blueprints"}

    def test_a_given_kept_repository_replaces_the_files(self):
        first, _ = self.set(None)
        data, changed = self.set(first, repositories=["pat/blueprints", "/r/elsewhere", KEPT[1]])
        assert data["repositories"] == {"pat/blueprints": {"dir": "/r/elsewhere", "checkout": KEPT[1]}}
        assert changed == ["repositories.pat/blueprints"]

    def test_an_unknown_top_level_key_is_kept_and_the_version_is_crews(self):
        first, _ = self.set(None)
        data, changed = self.set(dict(first, note={"by": "hand"}), session=["pat-2"])
        assert data["note"] == {"by": "hand"} and data["version"] == crew.VERSION and changed == ["drives.pat.session"]

    def test_the_drives_are_written_in_the_order_of_their_labels(self):
        data, _ = self.set(None)
        for label in ("zed", "abc", "pat-2"):
            data, _ = self.set(data, label=label, **lab_flags(state=[f"{label}/crew-state"], console=None))
        assert [d["label"] for d in data["drives"]] == ["abc", "pat", "pat-2", "zed"]

    def test_the_same_flags_change_nothing(self):
        first, _ = self.set(None)
        data, changed = self.set(json.loads(crew.teams_text(first)))
        assert changed == [] and crew.teams_text(data) == crew.teams_text(first)

    def test_a_drive_listed_twice_is_written_once_and_named_whole(self):
        """drive-setup, The drive listed twice: pat once, as the flags give it, and drives.pat changed."""
        first, _ = self.set(None)
        data, changed = self.set(json.loads(crew.teams_text(dict(first, drives=first["drives"] * 2))))
        assert crew.teams_text(data) == crew.teams_text(first) and changed == ["drives.pat"]

    def test_other_drives_of_any_shape_are_kept_as_the_file_holds_them(self):
        """A drive with no label and one whose repos is no list, both on this host: set with no traceback, the
        labelled drives in the order of their labels, then the other, each as the file held it."""
        first, _ = self.set(None)
        nameless = {"machine": MAC, "repos": ["pat/blueprints", {"by": "hand"}]}
        lab = {"label": "lab", "machine": MAC, "repos": 7}
        data, changed = self.set(dict(first, drives=first["drives"] + [nameless, lab]))
        assert data["drives"] == [lab, given()["drive"], nameless] and changed == []

    @pytest.mark.parametrize("name", ["deneb.json", "runner.json"])
    def test_the_module_files_are_written_again_byte_for_byte(self, name):
        """drive-setup, deneb's file: the pinned files of crew's module, read as bytes, written again as they are."""
        raw = (FILES / name).read_bytes()
        assert crew.teams_text(json.loads(raw)).encode() == raw

    def test_the_text_has_its_keys_sorted_no_space_and_no_newline(self):
        assert crew.teams_text({"b": [1, {"d": False, "c": "é"}], "a": 1}) == '{"a":1,"b":[1,{"c":"é","d":false}]}'


class TestTeamsStep:
    """drive-setup, "The file it would write is checked before it is written", "Run again with the same answers, it
    changes nothing", "Where Nix links the teams file, nothing is written there", "A teams file crew cannot read at all
    is moved aside once" and "A teams file at crew's own version is written where the set mends it" (design, Decisions
    5, 7 and 8; a-drive-set-loses-no-drive-and-no-record, Decision 2; a-drive-set-mends-what-it-replaces, Decisions 1 to
    3): the step from plain facts, nothing read or written by it."""

    KEPT = ("crew drive set sets only drive pat's entry and the hosts, console and kept repositories its flags give, and moves "
            "aside only a file crew cannot read at all, so /Users/pat/.config/crew/teams.json and every drive it names are left "
            "as they are, and nothing was written")

    @pytest.fixture(autouse=True)
    def teams(self, monkeypatch):
        monkeypatch.setattr(crew, "TEAMS", pathlib.Path("/Users/pat/.config/crew/teams.json"))

    def step(self, text=None, linked=False, target=None, aside_taken=False, here=MAC, **kw):
        return crew.teams_step({"linked": linked, "target": target, "text": text, "aside_taken": aside_taken,
                                "given": given(here, **kw), "here": here})

    def refused(self, said, **kw):
        with pytest.raises(crew.Refusal) as e:
            self.step(**kw)
        assert said in str(e.value), str(e.value)
        return str(e.value)

    def written(self, **kw):
        return crew.teams_text(crew.teams_set(None, given(**kw), MAC)[0])

    def test_no_file_is_written_new(self):
        step = self.step()
        assert step == {"step": "write", "text": self.written(), "changed": ["drives.pat", f"hosts.{MAC}", "consoles.pat",
                                                                               "repositories.pat/blueprints"]}

    def test_the_file_the_same_flags_wrote_is_left(self):
        """drive-setup, Set twice: the same flags on the file they wrote write nothing."""
        assert self.step(text=self.written()) == {"step": "unchanged"}

    def test_a_file_that_loads_has_the_drive_set_in_it(self):
        step = self.step(text=self.written(), session=["pat-2"])
        assert step["step"] == "write" and step["changed"] == ["drives.pat.session"]
        assert json.loads(step["text"])["drives"][0]["session"] == "pat-2"

    def test_a_file_respaced_by_hand_is_written_and_changes_no_key(self):
        step = self.step(text=json.dumps(json.loads(self.written()), indent=2))
        assert step == {"step": "write", "text": self.written(), "changed": []}

    @pytest.mark.parametrize("text, reason", [
        ('{"version":5,"partitions":[]}', "teams.json is version 5, and crew reads only version 6"),
        ("not json", "teams.json is no JSON (Expecting value"),
        (b"\xff\xfe{}", "teams.json is no JSON ("),
        ('{}', "teams.json is version null, and crew reads only version 6"),
        ('[]', "not a teams file's object")])
    def test_a_file_crew_cannot_read_at_all_is_moved_aside_with_its_reason(self, text, reason):
        """drive-setup, A file at version 5 and A file that is no JSON: moved aside, named with why crew cannot read it,
        and the file written new."""
        step = self.step(text=text)
        assert step["step"] == "aside" and reason in step["reason"]
        assert step["text"] == self.written() and step["changed"][0] == "drives.pat"

    def both(self, relative=None):
        """A version-6 file naming lab and pat, as crew drive set wrote it, the folder of the drive relative names then
        made relative by a hand, or none."""
        lab = crew.teams_set(None, given(label="lab", **lab_flags()), MAC)[0]
        data = crew.teams_set(lab, given(), MAC)[0]
        assert [d["label"] for d in data["drives"]] == ["lab", "pat"]
        for d in data["drives"]:
            if d["label"] == relative:
                d["folder"] = d["folder"].lstrip("/")
        return crew.teams_text(data)

    @pytest.mark.parametrize("aside_taken", [False, True])
    def test_a_file_at_crews_own_version_that_fails_a_check_is_refused_and_never_moved_aside(self, aside_taken):
        """drive-setup, One wrong field beside another drive: refused naming lab's folder and the check, the file and
        every drive it names left as they are, and nothing written, whether or not the aside is taken (record 0065,
        points 6 and 8; a-drive-set-mends-what-it-replaces, Decision 2)."""
        said = self.refused("", text=self.both("lab"), aside_taken=aside_taken)
        assert said.startswith("the teams file crew drive set would write is refused: drive lab in "
                               "/Users/pat/.config/crew/teams.json: 'folder' is the absolute folder of its herdr session on "
                               "pats-mac, not \"Users/pat/lab\""), said
        assert said.endswith(self.KEPT)
        assert ": regenerate /Users/pat/.config/crew/teams.json from crew's own module, services.crew, crew drive set, or the " \
               "machine's configuration that writes it. crew drive set sets only" in said
        assert "cannot load" not in said and "is taken" not in said

    def test_a_file_that_lists_no_drives_is_written(self):
        """drive-setup, A file that lists no drives: the drive set in it, nothing moved aside."""
        step = self.step(text='{"version":6,"drives":[],"hosts":{}}')
        assert step["step"] == "write" and step["text"] == self.written() and step["changed"][0] == "drives.pat"

    def test_a_file_that_lists_teams_is_refused(self):
        """drive-setup, A file that lists teams: the set keeps its teams, so the file it would write fails the check."""
        said = self.refused("/Users/pat/.config/crew/teams.json lists teams, which version 6 has no place for",
                            text='{"version":6,"teams":[]}')
        assert said.startswith("the teams file crew drive set would write is refused: ") and said.endswith(self.KEPT)

    def test_a_fault_in_the_drives_own_entry_is_mended(self):
        """drive-setup, A fault in the drive's own entry: pat's folder relative, and --folder gives it absolute."""
        step = self.step(text=self.both("pat"))
        assert step == {"step": "write", "text": self.both(), "changed": ["drives.pat.folder"]}

    def test_a_fault_in_a_host_the_flags_name_is_mended(self):
        """drive-setup, A fault in a host the flags name: pats-mac's kind macos, and --hosts gives it darwin."""
        data = json.loads(self.written())
        data["hosts"][MAC]["kind"] = "macos"
        step = self.step(text=crew.teams_text(data))
        assert step == {"step": "write", "text": self.written(), "changed": [f"hosts.{MAC}"]}

    def test_the_drive_listed_twice_is_written_once(self):
        """drive-setup, The drive listed twice: pat once, as the flags give it."""
        data = json.loads(self.written())
        data["drives"] *= 2
        step = self.step(text=crew.teams_text(data))
        assert step == {"step": "write", "text": self.written(), "changed": ["drives.pat"]}

    def test_a_part_of_another_shape_is_refused(self):
        """drive-setup, A part of another shape: hosts a list, refused naming hosts, nothing written."""
        said = self.refused("", text='{"version":6,"hosts":[]}')
        assert said.startswith("/Users/pat/.config/crew/teams.json is at crew's version 6, and crew drive set cannot keep what it "
                               "holds beside drive pat: /Users/pat/.config/crew/teams.json: 'hosts' is an object, not []"), said
        assert said.endswith(self.KEPT)

    def test_an_aside_already_taken_is_refused_naming_both_paths(self):
        """drive-setup, An aside already taken: both files left, nothing written."""
        said = self.refused("/Users/pat/.config/crew/teams.json is a file crew cannot load (", text='{"version":5}', aside_taken=True)
        assert "/Users/pat/.config/crew/teams.json.before-drive-set, where crew drive set moves such a file once, is taken" in said
        assert said.endswith("both are left as they are, and nothing was written")

    def test_an_aside_taken_is_no_matter_for_a_file_that_loads(self):
        assert self.step(text=self.written(), aside_taken=True) == {"step": "unchanged"}

    def test_a_link_whose_file_names_the_drive_as_given_writes_nothing_and_goes_on(self):
        """drive-setup, The drive Nix already names."""
        target = "/nix/store/abc-crew-teams.json"
        assert self.step(text=self.written(), linked=True, target=target) == {"step": "linked", "target": target}

    def test_a_link_whose_file_names_no_drive_pat_is_refused_naming_its_settings(self):
        """drive-setup, A drive Nix does not name: refused naming services.crew.settings.drives.pat, nothing made."""
        lab = self.written(label="lab", **lab_flags())
        said = self.refused("/Users/pat/.config/crew/teams.json is a link to /nix/store/abc-crew-teams.json, which crew's "
                            "module writes, and crew drive set writes nothing there", text=lab, linked=True,
                            target="/nix/store/abc-crew-teams.json")
        assert "does not name drive pat as given, drives.pat, consoles.pat, repositories.pat/blueprints differing or missing" in said
        assert "services.crew.settings.drives.pat" in said and said.endswith("nothing was made")

    def test_a_link_whose_file_gives_another_repos_and_no_console_is_refused_naming_the_keys(self):
        other = self.written(repos=[["pat/app"], ["pat/blueprints"]], leave=("--console",))
        said = self.refused("does not name drive pat as given, drives.pat.repos, consoles.pat differing or missing", text=other,
                            linked=True, target="/nix/store/abc-crew-teams.json")
        assert "services.crew.settings.drives.pat" in said

    def test_a_link_crew_cannot_read_or_load_is_refused(self):
        self.refused("crew cannot read the file it links to", linked=True, target="/nix/store/gone")
        said = self.refused("crew cannot load the file it links to (/Users/pat/.config/crew/teams.json is version 5", text='{"version":5}',
                            linked=True, target="/nix/store/old")
        assert "services.crew.settings.drives.pat" in said

    def test_a_file_crew_would_refuse_is_refused_in_its_words_with_nothing_written(self):
        """drive-setup, Two accounts in one session: --session pat, the planner on ia and every other role on pat."""
        said = self.refused("the teams file crew drive set would write is refused: drive pat's ",
                            accounts=[[r, "ia" if r == "planner" else "pat"] for r in crew.KIND_ROLES])
        assert "run in session pat under ia and pat, and a herdr session runs under one account" in said
        assert said.endswith("Nothing was written.")
        said = self.refused("the teams file crew drive set would write is refused", text=self.written(),
                            accounts=[[r, "ia" if r == "planner" else "pat"] for r in crew.KIND_ROLES])
        assert "run in session pat under ia and pat, and a herdr session runs under one account" in said
        assert said.endswith(self.KEPT)


class TestStateUnmade:
    """drive-setup, "A state not made is finished by the same command again" (design, Decision 4): the words of a
    refusal once the teams file names the drive as given."""

    @pytest.fixture(autouse=True)
    def teams(self, monkeypatch):
        monkeypatch.setattr(crew, "TEAMS", pathlib.Path("/Users/pat/.config/crew/teams.json"))

    @pytest.mark.parametrize("ending", ["", ".", ".\n"])
    def test_a_refused_push_names_the_file_the_drive_the_words_and_the_command_again(self, ending):
        words = "the push of pat/main to pat/crew-state failed: refused for the test"
        assert crew.state_unmade("pat", words + ending) == (
            "/Users/pat/.config/crew/teams.json names drive pat as given, and its state was not made: the push of pat/main to "
            "pat/crew-state failed: refused for the test. crew drive set pat run again with the same flags makes it.")


class TestDriveSaid:
    """drive-setup, "Its answer is plain or JSON" (design, Decision 12): a line for a moved file, one for the teams
    file and one for the state, or one JSON object, from what was done."""

    FILE = "/Users/pat/.config/crew/teams.json"
    TIP = "0123456789abcdef0123456789abcdef01234567"
    MADE = {"repository": "pat/crew-state", "branch": "pat/main", "tip": TIP, "outcome": "made",
            "did": ["started an empty plan", "added moves.rec with 0 moves of pat/blueprints"]}
    EXISTS = {"repository": "pat/crew-state", "branch": "pat/main", "tip": TIP, "outcome": "exists", "did": []}

    def done(self, state, **teams):
        return {"label": "pat", "teams": dict({"file": self.FILE}, **teams), "state": state}

    def test_a_new_drive_in_plain_lines(self):
        said = crew.drive_said(self.done(self.MADE, outcome="written", changed=["drives.pat", "hosts.pats-mac", "consoles.pat"]), False)
        assert said.split("\n") == [
            f"{self.FILE}: drive pat set, changing drives.pat, hosts.pats-mac, consoles.pat",
            "pat/main of pat/crew-state 0123456: started an empty plan; added moves.rec with 0 moves of pat/blueprints"]

    def test_a_new_drive_as_one_json_object(self):
        """drive-setup, Setup reads the answer: teams.outcome written, state.outcome made."""
        said = crew.drive_said(self.done(self.MADE, outcome="written", changed=["drives.pat"]), True)
        assert "\n" not in said
        assert json.loads(said) == {"label": "pat",
                                    "teams": {"file": self.FILE, "outcome": "written", "aside": None, "changed": ["drives.pat"]},
                                    "state": self.MADE}

    def test_run_again_it_says_unchanged_and_exists(self):
        """drive-setup, Set twice: it says unchanged and exists."""
        done = self.done(self.EXISTS, outcome="unchanged")
        assert crew.drive_said(done, False).split("\n") == [f"{self.FILE} names drive pat as given: nothing written",
                                                            "pat/main of pat/crew-state exists, at 0123456: nothing to do"]
        said = json.loads(crew.drive_said(done, True))
        assert (said["teams"]["outcome"], said["teams"]["changed"], said["state"]["outcome"]) == ("unchanged", [], "exists")

    def test_a_link_says_it_is_crews_modules_and_names_its_target(self):
        done = self.done(dict(self.MADE, outcome="finished", did=["added moves.rec with 0 moves of pat/blueprints"]),
                         outcome="linked", target="/nix/store/abc-crew-teams.json")
        assert crew.drive_said(done, False).split("\n")[0] == (
            f"{self.FILE} is a link to /nix/store/abc-crew-teams.json, which crew's module writes: nothing written there, and it "
            "names drive pat as given")
        said = json.loads(crew.drive_said(done, True))
        assert said["teams"]["outcome"] == "linked" and said["state"]["outcome"] == "finished"

    def test_a_file_moved_aside_is_named_first_with_why(self):
        done = self.done(self.MADE, outcome="written", changed=["drives.pat"], aside=f"{self.FILE}.before-drive-set",
                         reason=f"{self.FILE} is version 5, and crew reads only version 6.")
        lines = crew.drive_said(done, False).split("\n")
        assert lines[0] == (f"{self.FILE} moved to {self.FILE}.before-drive-set: crew could not load it: {self.FILE} is version 5, "
                            "and crew reads only version 6.")
        assert len(lines) == 3
        assert json.loads(crew.drive_said(done, True))["teams"]["aside"] == f"{self.FILE}.before-drive-set"

    def test_a_rewrite_that_changes_no_key_says_so(self):
        said = crew.drive_said(self.done(self.EXISTS, outcome="written", changed=[]), False)
        assert said.split("\n")[0] == f"{self.FILE}: drive pat set, no key changed"
