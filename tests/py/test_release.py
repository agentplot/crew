"""What a crew is where it runs, and the crew its host has installed (host-holds-and-updates "crew knows the release it
runs from", "A build's version is shown as a checkout's is", "crew names its command by the crew its host has
installed", "crew reads the crew its host has installed", "The launch digest reads crew's command as one word"): a
build's release file read field by field, its version shown, a root read as a checkout, a build or neither. That a
checkout reads itself through git, and that a start from a build records its release, is the session-start journey's
(t-session-hook)."""
import json
import subprocess

import pytest

import crew

COMMIT = "fcedc22e6df6380f1f640efac5f796416b1fb4c9"


def release(tmp_path, body):
    (tmp_path / "plugin").mkdir(parents=True, exist_ok=True)
    (tmp_path / crew.RELEASE).write_text(body if isinstance(body, str) else json.dumps(body))
    return tmp_path


class TestReleaseFile:
    def test_a_release_version_reads_as_its_tag(self):
        assert crew.release_version("0.44.1", COMMIT) == "v0.44.1"

    def test_an_untagged_version_reads_with_the_commits_first_seven_characters(self):
        assert crew.release_version("0-unstable-2026-11-08", COMMIT) == "0-unstable-2026-11-08+fcedc22"

    def test_a_file_naming_a_full_commit_and_a_version_reads_as_both(self):
        assert crew.release_read(json.dumps({"commit": COMMIT, "version": "0.44.1"})) == (
            {"commit": COMMIT, "version": "0.44.1"}, None)

    def test_a_file_whose_commit_is_not_forty_hexadecimal_characters_reads_as_no_release(self):
        for commit in ("fcedc22", COMMIT.upper(), COMMIT + "0", 42, None):
            assert crew.release_read(json.dumps({"commit": commit, "version": "0.44.1"})) == (
                None, "the release file names no commit")

    def test_a_file_with_no_version_reads_as_no_release(self):
        for version in ("", None, 3):
            assert crew.release_read(json.dumps({"commit": COMMIT, "version": version})) == (
                None, "the release file names no version")
        assert crew.release_read(json.dumps({"commit": COMMIT})) == (None, "the release file names no version")

    def test_a_file_that_is_not_json_or_no_object_reads_as_no_release(self):
        assert crew.release_read("commit = fcedc22") == (None, "the release file is not JSON")
        assert crew.release_read(json.dumps([COMMIT, "0.44.1"])) == (None, "the release file is not a JSON object")


class TestCrewRead:
    def test_a_build_with_a_release_file_and_no_git_reads_it(self, tmp_path):
        root = release(tmp_path, {"commit": COMMIT, "version": "0-unstable-2026-11-08"})
        assert crew.crew_read(root) == {"root": str(root), "commit": COMMIT, "version": "0-unstable-2026-11-08+fcedc22",
                                        "from": "release", "unread": None}
        assert crew.crew_version(root) == (COMMIT, "0-unstable-2026-11-08+fcedc22")

    def test_a_root_with_neither_git_nor_a_release_file_reads_nothing_and_says_so(self, tmp_path):
        got = crew.crew_read(tmp_path)
        assert (got["commit"], got["version"], got["from"]) == (None, None, None)
        assert "neither git nor a release file" in got["unread"] and crew.RELEASE in got["unread"]
        assert crew.crew_version(tmp_path) == (None, None)

    def test_a_release_file_crew_cannot_read_reads_nothing_and_says_what_it_lacks(self, tmp_path):
        root = release(tmp_path, {"commit": "fcedc22", "version": "0.44.1"})
        got = crew.crew_read(root)
        assert (got["commit"], got["version"], got["from"]) == (None, None, None)
        assert got["unread"].startswith("the release file names no commit")

    def test_crews_own_root_is_read_where_none_is_named(self, tmp_path, monkeypatch):
        root = release(tmp_path, {"commit": COMMIT, "version": "0.44.1"})
        monkeypatch.setattr(crew, "HOME", root)
        assert crew.crew_read()["version"] == "v0.44.1" and crew.crew_version() == (COMMIT, "v0.44.1")


def crew_in(folder, body="#!/bin/sh\n"):
    """An executable crew in a folder, made where it is missing."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "crew").write_text(body)
    (folder / "crew").chmod(0o755)
    return folder


class TestInstalledCommand:
    PROFILE, SYSTEM = "/etc/profiles/per-user/chuck/bin", "/run/current-system/sw/bin"

    def test_a_checkout_names_its_own_command_whatever_its_path_holds(self):
        assert crew.installed_command("/workspace/crew/main", True, [self.PROFILE, self.SYSTEM]) == \
            "/workspace/crew/main/plugin/bin/crew"
        assert crew.installed_command("/workspace/crew/main", True, []) == "/workspace/crew/main/plugin/bin/crew"

    def test_a_build_passes_over_the_store_and_names_the_first_profiles_crew(self):
        home = "/nix/store/abc-crew-0.44.1"
        assert crew.installed_command(home, False, ["/nix/store/def-claude-code/bin", self.PROFILE]) == \
            "/etc/profiles/per-user/chuck/bin/crew"
        assert crew.installed_command(home, False, ["/nix/store/def-claude-code/bin", self.PROFILE, self.SYSTEM]) == \
            "/etc/profiles/per-user/chuck/bin/crew"
        assert crew.installed_command(home, False, ["/nix/store/def-claude-code/bin", self.SYSTEM]) == \
            "/run/current-system/sw/bin/crew"

    def test_a_build_with_only_store_folders_holding_crew_has_none_installed(self):
        assert crew.installed_command("/nix/store/abc-crew-0.44.1", False,
                                      ["/nix/store/def-claude-code/bin", "/nix/store/abc-crew-0.44.1/bin"]) is None
        assert crew.installed_command("/nix/store/abc-crew-0.44.1", False, []) is None

    def test_crew_command_reads_crews_path_and_names_the_builds_own_where_nothing_is_installed(self, tmp_path, monkeypatch):
        build, store = tmp_path / "store/abc-crew", tmp_path / "store"
        build.mkdir(parents=True)
        monkeypatch.setattr(crew, "HOME", build)
        monkeypatch.setattr(crew, "STORE", f"{store}/")
        shim = crew_in(store / "def-claude-code/bin")
        unrun = tmp_path / "unrun"
        unrun.mkdir()
        (unrun / "crew").write_text("#!/bin/sh\n")
        monkeypatch.setenv("PATH", f"{shim}:{unrun}:relative/bin")
        assert crew.crew_command() == str(build / "plugin/bin/crew")
        profile = crew_in(tmp_path / "profile/bin")
        monkeypatch.setenv("PATH", f"{shim}:{unrun}:{profile}")
        assert crew.crew_command() == str(profile / "crew")

    def test_crew_command_from_a_checkout_is_its_own(self, tmp_path, monkeypatch):
        (tmp_path / ".git").write_text("gitdir: /elsewhere\n")
        monkeypatch.setattr(crew, "HOME", tmp_path)
        monkeypatch.setenv("PATH", str(crew_in(tmp_path / "profile/bin")))
        assert crew.crew_command() == str(tmp_path / "plugin/bin/crew")


class Ran:
    """subprocess.run standing for the installed crew's `crew _release`: what it was asked, and its answer."""

    def __init__(self, stdout="", code=0, stderr="", late=False):
        self.stdout, self.code, self.stderr, self.late, self.asked = stdout, code, stderr, late, []

    def __call__(self, argv, **kw):
        self.asked.append((argv, kw.get("timeout")))
        if self.late:
            raise subprocess.TimeoutExpired(argv, kw.get("timeout"))
        return subprocess.CompletedProcess(argv, self.code, self.stdout, self.stderr)


class TestInstalled:
    @pytest.fixture
    def host(self, tmp_path, monkeypatch):
        """A build of crew in the store, its release file written, and a profile folder on crew's path."""
        build = release(tmp_path / "store/abc-crew", {"commit": COMMIT, "version": "0.44.1"})
        monkeypatch.setattr(crew, "HOME", build)
        monkeypatch.setattr(crew, "STORE", f"{tmp_path / 'store'}/")
        monkeypatch.setattr(crew, "ASKED", {})
        profile = tmp_path / "profile/bin"
        profile.mkdir(parents=True)
        monkeypatch.setenv("PATH", str(profile))
        return build, profile

    def test_an_installed_command_that_is_crews_own_is_read_with_no_process(self, host):
        build, profile = host
        crew_in(build / "bin")
        (profile / "crew").symlink_to(build / "bin/crew")
        assert crew.installed() == {"root": str(build), "commit": COMMIT, "version": "v0.44.1", "from": "release",
                                    "unread": None}

    def test_another_crews_answer_is_read_field_by_field_once_for_each_real_path(self, host, tmp_path, monkeypatch):
        build, profile = host
        other = crew_in(tmp_path / "store/xyz-crew/bin")
        (profile / "crew").symlink_to(other / "crew")
        said = {"root": str(tmp_path / "store/xyz-crew"), "commit": "2" * 40, "version": "v0.44.2", "from": "release",
                "unread": None}
        ran = Ran(json.dumps(said) + "\n")
        monkeypatch.setattr(subprocess, "run", ran)
        assert crew.installed() == said
        assert crew.installed() == said
        assert ran.asked == [(["bash", str(profile / "crew"), "_release"], crew.RELEASE_ASKED)] and crew.RELEASE_ASKED == 5
        (profile / "crew").unlink()
        (profile / "crew").symlink_to(crew_in(tmp_path / "store/uvw-crew/bin") / "crew")
        crew.installed()
        assert len(ran.asked) == 2

    @pytest.mark.parametrize("ran,why", [
        (Ran(json.dumps({"root": "/r", "version": "v0.44.2", "from": "release"})), "its answer names no commit"),
        (Ran("crew 0.44.2"), "its answer is not JSON"),
        (Ran("", code=2, stderr="crew: no such command\n"), "_release exited 2: crew: no such command"),
        (Ran(late=True), "did not answer crew _release within 5 seconds"),
        (Ran(json.dumps({"root": "/r", "commit": None, "version": None, "from": None, "unread": "neither git nor a release file"})),
         "it reads nothing of itself: neither git nor a release file"),
    ])
    def test_an_answer_late_failed_or_missing_a_field_is_unread_saying_why(self, host, tmp_path, monkeypatch, ran, why):
        build, profile = host
        (profile / "crew").symlink_to(crew_in(tmp_path / "store/xyz-crew/bin") / "crew")
        monkeypatch.setattr(subprocess, "run", ran)
        got = crew.installed()
        assert (got["commit"], got["version"], got["from"]) == (None, None, None)
        assert why in got["unread"] and str(profile / "crew") in got["unread"]

    def test_no_installed_command_is_unread_saying_no_folder_outside_the_store_has_a_crew(self, host, tmp_path, monkeypatch):
        monkeypatch.setenv("PATH", str(crew_in(tmp_path / "store/def-claude-code/bin")))
        assert crew.installed() == crew.unread_crew("no folder of crew's path outside the Nix store has a crew")
