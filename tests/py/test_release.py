"""What a crew is where it runs, and the crew its host has installed (host-holds-and-updates "crew knows the release it
runs from", "A build's version is shown as a checkout's is", "crew names its command by the crew its host has
installed", "crew reads the crew its host has installed", "The launch digest reads crew's command as one word"): a
build's release file read field by field, its version shown, a root read as a checkout, a build or neither. That a
checkout reads itself through git, and that a start from a build records its release, is the session-start journey's
(t-session-hook)."""
import json

import crew

COMMIT = "fcedc22e6df6380f1f640efac5f796416b1fb4c9"


def release(tmp_path, body):
    (tmp_path / "plugin").mkdir(exist_ok=True)
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
