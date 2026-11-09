"""A host's hold and crew's updates reaching its agents (teams.19): which standing agent an update makes due a restart,
and why; what keeps a held host from being quiet; when a due agent may be restarted, how its exit ends crew's waits at
Claude Code's question, and what it is told; which
background work is one of crew's waits; the hold read from its file; which agents run on a host; and what the agents'
bands say of the crew they run and of the hold. That crew hold, go and update run on each host they name, end and bring
back the agents there, and that the hooks record a start's crew and hand a due agent its restart, is the hold journey's
(t-hold)."""
import json
import pathlib
import types

import pytest

import board
import crew
import hold
import transcript
from facts import FLEET

C1, C2 = "1" * 40, "2" * 40


@pytest.fixture(autouse=True)
def on_mac_studio(monkeypatch):
    monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
STARTED = {"session": "sid-1", "commit": C1, "version": "v0.12.1", "launch": "abc"}


def checkout(commit, version="v0.12.1"):
    """The crew a host has installed, a checkout at commit, as crew.installed reads it."""
    return {"root": "/workspace/crew/main", "commit": commit, "version": version, "from": "checkout", "unread": None}


def build(commit, version="v0.44.1"):
    """The crew a host has installed, a build whose release names commit, as crew.installed reads it."""
    return {"root": "/nix/store/abc-crew", "commit": commit, "version": version, "from": "release", "unread": None}


UNREAD = crew.unread_crew("/etc/profiles/per-user/chuck/bin/crew did not answer crew _release within 5 seconds")


class TestDue:
    def test_an_agent_whose_brief_model_effort_or_folders_changed_is_due(self):
        assert crew.update_due(STARTED, checkout(C1), "def", None) == (True, "its brief, model, effort or folders changed")
        assert crew.update_due(STARTED, UNREAD, "def", None) == (True, "its brief, model, effort or folders changed")

    def test_an_agent_whose_loaded_plugin_changed_is_due_and_one_whose_crew_code_alone_changed_is_not(self):
        assert crew.update_due(STARTED, checkout(C2), "abc", True) == (True, "crew's plugin changed")
        assert crew.update_due(STARTED, checkout(C2), "abc", False) == (False, None)

    def test_an_agent_on_crew_as_it_is_is_not_due(self):
        assert crew.update_due(STARTED, checkout(C1), "abc", None) == (False, None)

    def test_one_started_before_crew_kept_what_it_loaded_is_due(self):
        assert crew.update_due(dict(STARTED, commit=None, version=None, launch=None), checkout(C1), "abc", None) == (True, "it started before crew kept what an agent loads")
        assert crew.update_due(dict(STARTED, launch=None), checkout(C1), "abc", None)[0]

    def test_one_that_recorded_its_launch_and_no_commit_is_due_when_its_launch_changed(self):
        released = dict(STARTED, commit=None, version=None)
        assert crew.update_due(released, UNREAD, "def", None) == (True, "its brief, model, effort or folders changed")
        assert crew.update_due(released, checkout(C1), "def", None) == (True, "its brief, model, effort or folders changed")

    def test_one_that_recorded_its_launch_and_no_release_is_not_due_and_says_its_main_level_brought_up_again_restarts_it(self):
        released = dict(STARTED, commit=None, version=None)
        for now in (UNREAD, checkout(C1), build(C2)):
            due, why = crew.update_due(released, now, "abc", None)
            assert not due and why == crew.NO_COMMIT_SAID
        assert "can't tell whether its plugin changed since it started" in why and "recorded no release of crew's" in why
        assert "crew main down and crew main up restart it on the crew this host has installed" in why

    def test_crew_that_cannot_tell_whether_the_plugin_changed_restarts_nothing_and_says_so(self):
        assert crew.update_due(STARTED, checkout(C2), "abc", None) == (False, f"crew can't tell whether its plugin changed since {C1[:7]}")

    def test_an_installed_build_of_another_release_makes_its_agent_due(self):
        assert crew.update_due(STARTED, build(C2), "abc", None) == (True, "crew's release changed")

    def test_an_installed_build_of_the_release_it_started_on_does_not(self):
        assert crew.update_due(STARTED, build(C1), "abc", None) == (False, None)

    def test_an_installed_crew_crew_cannot_read_makes_none_due_and_says_why(self):
        assert crew.update_due(STARTED, UNREAD, "abc", None) == (False, "crew can't read the crew this host has installed: "
                                                                        "/etc/profiles/per-user/chuck/bin/crew did not answer crew _release within 5 seconds")
        none = crew.unread_crew(crew.NONE_INSTALLED)
        assert crew.update_due(STARTED, none, "abc", None) == (False, "crew can't read the crew this host has installed: "
                                                                      "no folder of crew's path outside the Nix store has a crew")

    def test_an_agent_with_no_recorded_start_is_never_due(self):
        assert crew.update_due(None, checkout(C1), "abc", True) == (False, None)

    def test_due_of_compares_what_a_session_loads_only_in_an_installed_checkout_in_its_own_root(self, monkeypatch):
        fleet = {"drives": {"wldn": {"label": "wldn", "machine": "mac-studio", "flume": {r: False for r in crew.KIND_ROLES}}}}
        compared = []
        monkeypatch.setattr(crew, "launch_now", lambda fleet, label, role: "abc")
        monkeypatch.setattr(crew, "loaded_changed", lambda was, now, root=None: compared.append((was, now, root)) or True)
        assert crew.due_of(fleet, "wldn-ops", STARTED, checkout(C2)) == (True, "crew's plugin changed", STARTED)
        assert compared == [(C1, C2, "/workspace/crew/main")]
        assert crew.due_of(fleet, "wldn-ops", STARTED, build(C2)) == (True, "crew's release changed", STARTED)
        assert crew.due_of(fleet, "wldn-ops", STARTED, checkout(C1)) == (False, None, STARTED)
        assert len(compared) == 1
        monkeypatch.setattr(crew, "installed", lambda: build(C2, "v0.44.2"))
        assert crew.due_of(fleet, "wldn-ops", STARTED) == (True, "crew's release changed", STARTED)

    def test_the_launch_digest_follows_the_model_effort_folders_and_brief_and_not_the_folders_order(self):
        l = {"model": "opus", "effort": "high", "dirs": ["/a", "/b"]}
        d = crew.launch_digest(l, "brief")
        assert d == crew.launch_digest(dict(l, dirs=["/b", "/a"]), "brief") and len(d) == 16
        assert len({d, crew.launch_digest(dict(l, model="sonnet"), "brief"), crew.launch_digest(dict(l, effort="max"), "brief"),
                    crew.launch_digest(dict(l, dirs=["/a"]), "brief"), crew.launch_digest(l, "brief, amended")}) == 5

    def test_the_launch_digest_reads_crews_own_path_in_the_brief_as_one_word(self, monkeypatch):
        # chuck-herdr-alpha, 2026-10-31: a start by the box's checkout named /workspace/crew/main/plugin/bin/crew in its
        # brief, the follower's release /nix/store/…-crew-0.38.7/plugin/bin/crew, and each read the other's start as due;
        # a brief now names the installed crew (crew_command), and every path a brief may name it by reads as <crew>
        l = {"model": "opus", "effort": "high", "dirs": ["/a"]}
        monkeypatch.setattr(crew, "crew_command", lambda: str(crew.HOME / "plugin/bin/crew"))
        monkeypatch.setattr(crew, "HOME", pathlib.Path("/workspace/crew/main"))
        checkout = crew.launch_digest(l, "run `/workspace/crew/main/plugin/bin/crew bolts`")
        monkeypatch.setattr(crew, "HOME", pathlib.Path("/nix/store/abc-crew-0.38.7"))
        release = crew.launch_digest(l, "run `/nix/store/abc-crew-0.38.7/plugin/bin/crew bolts`")
        assert checkout == release
        assert release != crew.launch_digest(l, "run `/nix/store/abc-crew-0.38.7/plugin/bin/crew status`")
        monkeypatch.setattr(crew, "crew_command", lambda: "/etc/profiles/per-user/chuck/bin/crew")
        assert release == crew.launch_digest(l, "run `/etc/profiles/per-user/chuck/bin/crew bolts`")


class Main:
    """A main level's session on its host as hold.kind_end reads and acts on it: whether its agent's exit is taken at
    once, later or never, and what was done."""

    def __init__(self, label, stopped=None, exits=True):
        self.label, self.stopped, self.exits, self.done = label, stopped, exits, []

    def agent_of(self, role):
        return f"{self.label}-{role}"

    def stop(self, role, ending=None, waits=False):
        self.done.append(f"{role} stopped" + (" with its waits" if waits else ""))
        return self.stopped

    def exited(self, role, looks):
        self.done.append(f"{role} watched")
        return self.exits

    def record(self, act, why, roles):
        self.done.append((act, why, roles))


class TestKindEnd:
    """A main level's standing agent whose drive now runs its role as its kind is due an end, never a restart
    (design Decision 14; host-holds-and-updates "A standing agent of a role that now runs as its kind is ended at its
    next stop"): crew.end_due and crew.due_of read it from the teams file alone, crew update passes it over
    (hold.update_here), and crew _renew ends it once idle, its pane left and nothing started, never on a held host
    (hold.kind_end). That the Stop hook hands it over and crew _renew ends it through herdr is the hold journey's
    (t-hold)."""
    FLEET = {"drives": {"madswan": {"label": "madswan", "machine": "mac-studio",
                                                     "flume": dict({r: False for r in crew.KIND_ROLES}, planner="madswan-main", reviewer="madswan-main")}}}

    def test_a_main_level_agent_whose_role_runs_as_its_kind_is_due_an_end_and_one_that_stands_is_not(self):
        assert crew.end_due(self.FLEET, "madswan-planner") == crew.KIND_SAID
        assert crew.due_of(self.FLEET, "madswan-planner", STARTED, checkout(C1)) == (True, crew.KIND_SAID, STARTED)
        assert crew.end_due(self.FLEET, "madswan-design") is None
        assert crew.due_of(self.FLEET, "madswan-reviewer", STARTED, checkout(C1)) == (False, None, STARTED)

    def test_crew_update_passes_it_over_and_hands_any_other_due_agent_its_restart(self, monkeypatch, capsys):
        handed = []
        monkeypatch.setattr(crew, "held", lambda: None)
        monkeypatch.setattr(crew, "installed", lambda: checkout(C2, "v0.40.0"))
        monkeypatch.setattr(crew, "agents_here", lambda fleet, label=None: ["madswan-design", "madswan-planner"])
        monkeypatch.setattr(crew, "due_of", lambda fleet, name, now=None: (
            (True, crew.KIND_SAID, STARTED) if name == "madswan-planner" else (True, "crew's plugin changed", STARTED)))
        monkeypatch.setattr(hold, "hand", handed.append)
        hold.update_here(self.FLEET, types.SimpleNamespace(label=None))
        assert handed == ["madswan-design"]
        out = capsys.readouterr().out
        assert ("madswan-planner is passed over, never restarted: its role now runs as its kind, in Flume runs of its own; "
                "while it is up, the end of its next turn ends it, as crew main up madswan does") in out
        assert "madswan-design is due (crew's plugin changed): it is restarted on crew v0.40.0 once it is idle" in out

    @pytest.fixture
    def here(self, monkeypatch, tmp_path):
        monkeypatch.setattr(crew, "held", lambda: None)
        monkeypatch.setattr(hold, "RENEW", tmp_path / "renew")

    ENDED = ("agent.end", "main(madswan): end madswan-planner, which runs as its kind", ["planner"])

    def test_an_idle_agent_is_ended_its_pane_left_and_recorded(self, here, capsys):
        main = Main("madswan")
        hold.kind_end(self.FLEET, main, "planner")
        assert main.done == ["planner stopped with its waits", self.ENDED]
        assert ("madswan-planner is ended: its role now runs as its kind, in Flume runs of its own, so nothing starts it "
                "again; its pane is left") in capsys.readouterr().out

    def test_one_slow_to_exit_is_watched_and_one_that_never_exits_runs_on_still_due(self, here, capsys):
        slow = Main("madswan", stopped="madswan-planner did not exit")
        hold.kind_end(self.FLEET, slow, "planner")
        assert slow.done == ["planner stopped with its waits", "planner watched", self.ENDED]
        never = Main("madswan", stopped="madswan-planner did not exit", exits=False)
        hold.kind_end(self.FLEET, never, "planner")
        assert never.done == ["planner stopped with its waits", "planner watched"]
        assert "it runs on as it was, still due its end: the end of its next turn hands it back" in capsys.readouterr().err

    def test_one_gone_to_work_and_any_on_a_held_host_is_left(self, here, monkeypatch, capsys):
        working = Main("madswan", stopped=crew.working_said("madswan-planner"))
        hold.kind_end(self.FLEET, working, "planner")
        assert working.done == ["planner stopped with its waits"]
        monkeypatch.setattr(crew, "held", lambda: {"by": "chuck@mac-studio", "why": "herdr 0.9.6", "at": "2026-10-31T12:00Z"})
        held = Main("madswan")
        hold.kind_end(self.FLEET, held, "planner")
        assert held.done == []
        assert "mac-studio is held; crew go mac-studio hands madswan-planner its end" in capsys.readouterr().out


class TestStanding:
    @pytest.mark.parametrize("name, role", [
        ("wldn-design", ("wldn", "design")), ("wldn-planner", ("wldn", "planner")), ("wldn-ops", ("wldn", "ops")),
        ("wldn-operator", ("wldn", "operator")), ("swb-1-conductor", None), ("swb-1-ops", None),
        ("wldn-dispatch-chuck-herdr-alpha", None), ("swb-1-unit-2", None), ("wldn-reviewer", None), ("nobody", None)])
    def test_only_a_main_levels_standing_agent_is_restarted_for_an_update(self, name, role):
        assert crew.standing_role(FLEET, name) == role

    def test_the_agents_on_a_host_are_its_main_levels(self, monkeypatch):
        fleet = {"drives": {"swancloud": {"machine": "deneb"}, "madswan": {"machine": "mac-studio"}}}
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        assert crew.agents_here(fleet) == ["swancloud-design", "swancloud-planner", "swancloud-ops", "swancloud-operator"]
        assert crew.agents_here(fleet, "madswan") == []


class TestStarts:
    def test_the_newest_session_of_each_agent_is_its_start(self, tmp_path, monkeypatch):
        monkeypatch.setattr(crew, "SESSIONS", tmp_path)
        (tmp_path / "old").write_text("CREW_AGENT=wldn-ops\nCREW_COMMIT=" + C1 + "\n")
        (tmp_path / "new").write_text(f"CREW_AGENT=wldn-ops\nCREW_COMMIT={C2}\nCREW_VERSION=v0.13.0\nCREW_LAUNCH=abc\n")
        (tmp_path / "other").write_text("CREW_AGENT=wldn-design\n")
        import os
        os.utime(tmp_path / "old", (1, 1))
        assert crew.start_of("wldn-ops") == {"session": "new", "commit": C2, "version": "v0.13.0", "launch": "abc"}
        assert crew.start_of("wldn-design") == {"session": "other", "commit": None, "version": None, "launch": None}
        assert crew.start_of("wldn-planner") is None


class TestHeld:
    def test_a_host_with_no_hold_file_is_not_held_and_one_crew_cannot_read_is(self, tmp_path, monkeypatch):
        monkeypatch.setattr(crew, "HOLD", tmp_path / "hold")
        assert crew.held() is None
        (tmp_path / "hold").write_text(json.dumps({"by": "fleet-releases", "why": "herdr 0.9.6", "at": "2026-10-21T03:00Z", "now": False}))
        assert crew.held()["why"] == "herdr 0.9.6"
        (tmp_path / "hold").write_text("{")
        assert crew.held() == {"by": "?", "why": f"crew can't read its hold file {tmp_path / 'hold'}", "at": None}

    def test_a_start_refused_by_a_hold_names_who_held_it_since_when_why_and_what_lifts_it(self):
        h = {"by": "fleet-releases", "why": "herdr 0.9.6", "at": "2026-10-21T03:00Z"}
        assert crew.held_said("deneb", h) == ("deneb is held by fleet-releases since 2026-10-21T03:00Z: herdr 0.9.6. "
                                              "crew starts no agent there until crew go deneb")


class TestQuiet:
    def test_a_host_is_quiet_once_nothing_of_crews_works_there(self):
        assert hold.busy_said([{"name": "swancloud-design", "status": "idle", "asking": False, "own": [], "unread": None}], 0) == []

    def test_what_still_works_is_said_each_its_own_way(self):
        facts = [{"name": "swancloud-design", "status": "working", "asking": False, "own": [], "unread": None},
                 {"name": "swancloud-operator", "status": "blocked", "asking": False, "own": [], "unread": None},
                 {"name": "swancloud-planner", "status": "idle", "asking": True, "own": [], "unread": None},
                 {"name": "swancloud-ops", "status": "idle", "asking": False, "own": ["wt submit main"], "unread": None},
                 {"name": "swancloud-reviewer", "status": "idle", "asking": False, "own": None, "unread": "herdr names no session for it"}]
        assert hold.busy_said(facts, 2) == [
            "swancloud-design is working", "swancloud-operator waits on a question to you in its pane",
            "swancloud-planner waits on a question to you in its pane",
            "swancloud-ops runs 1 background task of its own: wt submit main",
            "crew can't tell what swancloud-reviewer is doing: herdr names no session for it", "2 of crew's tests are running"]

    @pytest.mark.parametrize("command, wait", [
        ("crew unit wait a-unit --timeout 3600000", True), ("crew chore wait c", True), ("crew card wait batch/3", True),
        ("crew fix crw-4 f --wait", True), ("cd /x && crew review swancloud --wait --timeout 60000", True),
        ("bash /x/plugin/bin/crew unit wait u", True), ("crew bolt submit b", False), ("wt submit main", False),
        ("sleep 600; echo wait", False), (None, False)])
    def test_only_crews_waits_are_background_work_a_restart_may_end(self, command, wait):
        # crew card wait is gone (teams.24), and one still running from before is still read as crew's.
        assert hold.crew_wait(command) is wait


class TestRenew:
    def test_the_hand_of_a_restart_runs_crew_renew_through_the_installed_crew(self, tmp_path, monkeypatch):
        # The Stop hook of a session that loaded an older build runs that build's hold.hand: the restart it hands is the
        # installed crew's, so the agent comes back on crew as the host has it now.
        ran = []
        monkeypatch.setattr(crew, "crew_command", lambda: "/etc/profiles/per-user/chuck/bin/crew")
        monkeypatch.setattr(hold, "RENEW", tmp_path / "renew")
        monkeypatch.setattr(hold.subprocess, "Popen", lambda argv, **kw: ran.append(argv))
        hold.hand("wldn-ops")
        assert ran == [["bash", "/etc/profiles/per-user/chuck/bin/crew", "_renew", "wldn-ops"]]
        assert (tmp_path / "renew/wldn-ops.log").exists()

    def test_a_due_agent_is_restarted_only_once_it_is_idle_with_nothing_of_its_own_running(self):
        assert hold.renew_ready("idle", False, None, []) == (True, None)
        assert hold.renew_ready("done", False, None, []) == (True, None)
        assert hold.renew_ready("working", False, None, []) == (False, "it is working")
        assert hold.renew_ready("idle", True, None, []) == (False, "it waits on a question to you in its pane")
        assert hold.renew_ready("blocked", False, None, []) == (False, "it waits on a question to you in its pane")
        assert hold.renew_ready("idle", False, None, ["wt submit main"]) == (False, "it runs background work of its own: wt submit main")
        assert hold.renew_ready(None, False, None, []) == (False, "it is not up")
        assert hold.renew_ready("idle", False, "no transcript", []) == (False, "crew can't tell what it is doing: no transcript")

    def test_an_agent_not_up_is_started_with_no_stop_only_when_an_earlier_restarts_keys_ended_it(self):
        # swancloud-operator and fwn-1-conductor exited within a minute of their restarts giving up on deneb, and their
        # panes stood as shells for nine hours (signal 2026-10-23-chuck-mac-studio-8d53f475/01).
        assert hold.renew_exited(False, None, "sid-1", "sid-1", False) == (True, None)

    def test_an_agent_no_restart_gave_up_on_is_not_up_and_left_to_crew_revive(self):
        assert hold.renew_exited(False, None, None, "sid-1", False) == (False, "it is not up")
        assert hold.renew_exited(False, None, "", "sid-1", False) == (False, "it is not up")

    def test_a_mark_of_another_session_is_stale_and_read_as_not_up(self):
        assert hold.renew_exited(False, None, "sid-0", "sid-1", False) == (False, "it is not up")
        assert hold.renew_exited(False, None, "sid-1", None, False) == (False, "it is not up")

    def test_a_pane_herdr_lists_an_agent_in_is_not_started_over(self):
        assert hold.renew_exited(True, None, "sid-1", "sid-1", False) == (False, "it is not up")

    def test_a_restarts_mark_names_the_session_its_exit_was_typed_into_and_a_stale_one_goes_as_it_is_read(self, tmp_path, monkeypatch):
        monkeypatch.setattr(hold, "RENEW", tmp_path)
        mark = tmp_path / "wldn-ops.exiting"
        assert hold.marked_exit("wldn-ops", "sid-1") is None
        mark.write_text("sid-1\n")
        assert hold.marked_exit("wldn-ops", "sid-1") == "sid-1" and mark.exists()
        assert hold.marked_exit("wldn-ops", "sid-2") == "sid-1" and not mark.exists()
        assert hold.EXITING * 5 == 600

    def test_an_agent_taken_down_stays_down(self):
        assert hold.renew_exited(False, None, "sid-1", "sid-1", True) == (False, "it was taken down; it stays down")

    def test_a_pane_crew_cannot_read_starts_nothing_and_says_why(self):
        assert hold.renew_exited(None, "herdr lists no pane w1:p2, which crew keeps for wldn-ops", "sid-1", "sid-1", False) == (
            False, "crew can't tell whether its pane holds it: herdr lists no pane w1:p2, which crew keeps for wldn-ops")

    def test_a_restarted_agent_is_told_the_crew_it_started_on_the_one_it_runs_now_and_what_changed(self):
        said = hold.renew_notice("v0.12.1", "v0.13.0", ["feat(teams): a host is held", "fix(board): x"])
        assert said.startswith("crew restarted you on crew v0.13.0 (you started on v0.12.1), so your brief and crew's plugin are as they now stand. "
                               "What changed: feat(teams): a host is held; fix(board): x.")
        assert "start again any wait you still need" in said
        assert hold.renew_notice(None, None, []).startswith("crew restarted you on crew as it now is, so")

    def test_claude_codes_question_at_an_exit_with_background_work_is_read_from_the_panes_screen(self):
        assert crew.exit_asks(EXIT_SCREEN)
        assert not crew.exit_asks("❯ \n  ? for shortcuts")
        assert not crew.exit_asks(" Exiting worktree session\n ❯ 1. Keep worktree")
        assert not crew.exit_asks("") and not crew.exit_asks(None)

    def test_a_restart_ends_crews_waits_at_the_exits_question_and_any_other_stop_leaves_it_asked(self, tmp_path, monkeypatch):
        # swc-3's and swc-4's conductors, restarted at a give beside their bolts waiting to land, stopped at the question
        # on their landing-card waits and read as blocked (signal 2026-10-22-swancloud-dispatch-deneb-bddc208d/01).
        monkeypatch.setattr(crew, "nap", lambda seconds: None)
        for waits in (True, False):
            agents = crew.Agents(None, "main", "swancloud", "swancloud", "swancloud", tmp_path / str(waits), ("ops",), "/w", None)
            agents.herdr = Exiting()
            agents.ensure()
            agents.put("panes", "ops", "w8:p1")
            why = agents.stop("ops", waits=waits)
            enters = [a for a in agents.herdr.acts if a[:2] == ("agent", "send-keys")]
            if waits:
                assert why is None and agents.ended == ["ops"]
                assert enters == [("agent", "send-keys", "w8:p1", "enter")]
            else:
                assert why == "swancloud-ops did not exit (busy or waiting on the user); it was left running"
                assert enters == [] and agents.herdr.state == "blocked"

    def lingering(self, tmp_path, monkeypatch, reads):
        monkeypatch.setattr(crew, "nap", lambda seconds: None)
        agents = crew.Agents(None, "main", "swancloud", "swancloud", "swancloud", tmp_path, None, "/w", None)
        agents.herdr = Lingering(reads)
        agents.ensure()
        agents.put("panes", "operator", "w2:p3")
        return agents

    def test_an_agent_slow_to_exit_is_watched_after_its_stop_gives_up_and_ended_once_it_goes(self, tmp_path, monkeypatch):
        # swancloud-operator exited within a minute of its restart giving up on deneb (signal 2026-10-23-chuck-mac-studio-8d53f475/01).
        agents = self.lingering(tmp_path, monkeypatch, STOP_LOOKS + 3)
        assert agents.stop("operator", waits=True) == "swancloud-operator did not exit (busy or waiting on the user); it was left running"
        assert agents.ended == []
        typed = list(agents.herdr.acts)
        assert agents.exited("operator", 10) is True
        assert agents.ended == ["operator"] and agents.herdr.reads == STOP_LOOKS + 3
        assert agents.herdr.acts == typed

    def test_an_agent_that_never_exits_is_left_running_with_nothing_more_typed_to_it(self, tmp_path, monkeypatch):
        agents = self.lingering(tmp_path, monkeypatch, None)
        assert agents.stop("operator", waits=True)
        typed = list(agents.herdr.acts)
        assert agents.exited("operator", 10) is False
        assert agents.ended == [] and agents.herdr.state == "idle"
        assert agents.herdr.acts == typed


EXIT_SCREEN = """ Background work is running
 The following will stop when you exit:

 crew card wait land/the-bolt
 ❯ 1. Exit and stop tasks
   2. Move to background and exit
   3. Stay
"""


class Exiting:
    """herdr's side of a Claude Code session told /exit while a background task of its own runs: the question shows and
    the agent reads blocked, Enter on the question's first option ends it, and Ctrl+C leaves it asked."""

    def __init__(self):
        self.state, self.acts = "idle", []

    def status(self, pane, fresh=False):
        return self.state

    def run(self, *args):
        self.acts.append(args)
        out = ""
        if args[:2] == ("agent", "prompt") and args[3] == "/exit":
            self.state = "blocked"
        elif args[:2] == ("pane", "read"):
            out = EXIT_SCREEN if self.state == "blocked" else ""
        elif args[:2] == ("agent", "send-keys") and args[3:] == ("enter",) and self.state == "blocked":
            self.state = None
        return types.SimpleNamespace(returncode=0, stdout=out, stderr="")


# How many times a stop reads an agent afresh before it gives up: once a second for 30 seconds, and once after Ctrl+C.
STOP_LOOKS = 31


class Lingering:
    """herdr's side of a Claude Code session slow to exit: told /exit and Ctrl+C it stays up and idle, and herdr reads it
    gone only after `reads` fresh reads of it in all, never when reads is None."""

    def __init__(self, reads):
        self.state, self.acts, self.told, self.reads, self.gone_at = "idle", [], False, 0, reads

    def status(self, pane, fresh=False):
        if fresh and self.told:
            self.reads += 1
            if self.gone_at is not None and self.reads >= self.gone_at:
                self.state = None
        return self.state

    def run(self, *args):
        self.acts.append(args)
        if args[:2] == ("agent", "prompt") and args[3] == "/exit":
            self.told = True
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")


class TestHosts:
    def test_all_is_every_main_levels_host_and_one_named_must_be_a_host(self):
        fleet = {"drives": {"l": {"machine": "mac-studio"}, "m": {"machine": "deneb"}},
                 "hosts": {"deneb": {}, "box": {}, "mac-studio": {}, "macbook-pro": {}}}
        assert hold.hosts_named(fleet, "--all") == ["deneb", "mac-studio"]
        assert hold.hosts_named(fleet, "macbook-pro") == ["macbook-pro"]
        with pytest.raises(crew.Refusal, match="nowhere is no host of the fleet's hosts file. hosts: box deneb mac-studio macbook-pro"):
            hold.hosts_named(fleet, "nowhere")


class TestTranscript:
    def test_each_background_tasks_command_is_read_from_the_call_that_started_it(self, tmp_path):
        rows = [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "tu1", "name": "Bash",
                                                                "input": {"command": "crew unit wait u", "run_in_background": True}}]}},
                {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "tu1"}]}, "toolUseResult": {"backgroundTaskId": "b1"}},
                {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "tu2", "name": "Bash", "input": {"command": "wt submit main"}}]}},
                {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "tu2"}]}, "toolUseResult": {"backgroundTaskId": "b2"}},
                {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "gone"}]}, "toolUseResult": {"backgroundTaskId": "b3"}}]
        path = tmp_path / "s.jsonl"
        path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        assert transcript.started_commands(path) == {"b1": "crew unit wait u", "b2": "wt submit main", "b3": None}
        assert transcript.started_commands(tmp_path / "none.jsonl") is None


class TestBands:
    HERE = {"host": "deneb", "version": "v0.13.0", "held": None,
            "agents": {"wldn-planner": {"version": "v0.12.1", "due": True}, "wldn-operator": {"version": "v0.13.0", "due": False},
                       "wldn-ops": {"version": None, "due": True}}}

    def test_each_agent_says_the_crew_it_started_on_and_the_one_it_takes_at_its_next_stop(self):
        assert board.crew_said({"version": "v0.12.1", "due": False}, "v0.13.0") == "crew v0.12.1"
        assert board.crew_said({"version": "v0.12.1", "due": True}, "v0.13.0") == "crew v0.12.1 → v0.13.0 at its next stop"
        assert board.crew_said({"version": None, "due": True}, None) == "an older crew → crew as it now is at its next stop"

    def test_a_due_agents_band_shows_the_release_the_host_has_installed(self, monkeypatch):
        # The planner started on a build whose release names 0.44.1; the host has since installed one naming 0.44.2.
        fleet = {"drives": {"wldn": {"label": "wldn", "machine": "mac-studio", "flume": {r: False for r in crew.KIND_ROLES}}}}
        start = dict(STARTED, version="v0.44.1")
        monkeypatch.setattr(crew, "installed", lambda: build(C2, "v0.44.2"))
        monkeypatch.setattr(crew, "starts", lambda: {"wldn-planner": start})
        monkeypatch.setattr(crew, "agents_here", lambda fleet, label=None: ["wldn-planner"])
        monkeypatch.setattr(crew, "held", lambda: None)
        monkeypatch.setattr(crew, "launch_now", lambda fleet, label, role: start["launch"])
        here = board.here_read(fleet, "wldn")
        assert here == {"host": "mac-studio", "version": "v0.44.2", "held": None,
                        "agents": {"wldn-planner": {"version": "v0.44.1", "due": True}}}
        assert board.crew_said(here["agents"]["wldn-planner"], here["version"]).endswith("crew v0.44.1 → v0.44.2 at its next stop")

    def test_a_band_ends_its_first_line_with_its_crew_and_one_with_no_recorded_start_is_drawn_as_it_is(self):
        """Each main-level role here with a recorded start (crew.agents_here); no team agent or dispatcher has a band
        (Decision 11 of the-team-machinery-leaves)."""
        from test_board import data
        v = board.agent_views(dict(data(), here=self.HERE))["views"]
        first = "".join(s for s, _ in v["wldn-planner"][0])
        assert first.endswith("  crew v0.12.1 → v0.13.0 at its next stop")
        assert v["wldn-operator"][0][-1] == ("crew v0.13.0", "dim")
        assert "".join(s for s, _ in v["wldn-ops"][0]).endswith("an older crew → v0.13.0 at its next stop")
        assert v["wldn-design"] == board.agent_views(data())["views"]["wldn-design"]
        assert sorted(v) == ["wldn-design", "wldn-operator", "wldn-ops", "wldn-planner"]

    def test_every_band_on_a_held_host_opens_with_the_hold(self):
        from test_board import data
        h = {"by": "fleet-releases", "why": "herdr 0.9.6", "at": "2026-10-21T03:00Z"}
        v = board.agent_views(dict(data(), here=dict(self.HERE, held=h)))["views"]
        line = [("deneb is held", "bold"), (" by fleet-releases since 2026-10-21T03:00Z: herdr 0.9.6. Start nothing new; crew go deneb lifts it", None)]
        assert all(lines[0] == line for lines in v.values())


class TestGoOpensTheConsoles:
    """operator-agent, Consoles after a hold: crew go lifts the host's hold and opens again the consoles of the drives
    its teams file's `consoles` names, and no other drive's (hold.go, board.labels_here; record 0064)."""

    def test_go_opens_the_consoles_consoles_names_and_no_other(self, monkeypatch, tmp_path, capsys):
        import argparse
        import plan
        import record
        fleet = dict(FLEET, drives=dict(FLEET["drives"], agentplot={"label": "agentplot", "machine": "deneb"},
                                        madswan={"label": "madswan", "machine": "deneb"}),
                     consoles={"agentplot": "/p", "wldn": "/w"})
        opened = []
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        monkeypatch.setattr(crew, "held", lambda: {"by": "chuck"})
        monkeypatch.setattr(crew, "HOLD", tmp_path / "hold.json")
        monkeypatch.setattr(crew, "agents_here", lambda fleet, label=None: [])
        monkeypatch.setattr(record, "emit", lambda *a, **k: None)
        monkeypatch.setattr(plan, "revive_cmd", lambda fleet, a: None)
        monkeypatch.setattr(hold, "tell_each", lambda fleet, names, text: None)
        monkeypatch.setattr(hold, "update_here", lambda fleet, a: None)
        monkeypatch.setattr(plan, "console_cmd", lambda fleet, a: opened.append((a.act, a.label)))
        hold.go(fleet, argparse.Namespace())
        assert opened == [("up", "wldn"), ("up", "agentplot")]
        assert "deneb is no longer held" in capsys.readouterr().out
