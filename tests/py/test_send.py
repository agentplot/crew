"""crew send (briefs.10, record 0035, the operator-agent spec "A send reaches the operator of the drive it names, marked as a tell",
the run-record spec "A send that reaches its operator appends one entry naming the sender and the operator"): crew.send_door for where a
send goes, from the teams file alone, and crew.send for what it types and records. That the command reaches the
operator's pane on its host is the main level's journey's (t-journey-main)."""
import re

import pytest

import crew
import facts
import record

FLEET = {**facts.FLEET, "drives": {**facts.FLEET["drives"],
                                       "swancloud": {"label": "swancloud", "machine": "mac-studio"}}}
HERE = "mac-studio"
WAY_ON = (f". A drive another host runs is sent to from here once {crew.TEAMS} on {HERE} names it, as the host's "
          "configuration writes it, never by crew send run on that host over ssh; nothing was sent")


class TestDoor:
    """A drive's label resolves to its operator; nothing else is placed."""

    def test_a_drive_goes_to_its_operator_by_its_label(self):
        assert crew.send_door(FLEET, "wldn", "user@mac-studio", HERE) == ("wldn", "wldn-operator")

    @pytest.mark.parametrize("name", ["swb-1", "swb-2", "crw-5"])
    def test_a_teams_name_from_before_teams_left_is_refused_naming_the_drives(self, name):
        """operator-agent "A name crew does not know"."""
        with pytest.raises(crew.Refusal, match=rf"^crew send sends to a drive by its label, not '{name}': drives swancloud wldn"
                                               rf"{re.escape(WAY_ON)}$"):
            crew.send_door(FLEET, name, "swancloud-planner", HERE)

    def test_an_agents_name_is_refused_naming_the_drives(self):
        with pytest.raises(crew.Refusal, match=r"crew send sends to a drive by its label, not 'wldn-planner': "
                                               rf"drives swancloud wldn{re.escape(WAY_ON)}$"):
            crew.send_door(FLEET, "wldn-planner", "swancloud-planner", HERE)

    def test_an_unknown_name_is_refused(self):
        with pytest.raises(crew.Refusal, match="not 'nosuch'"):
            crew.send_door(FLEET, "nosuch", None, HERE)

    def test_the_door_sending_to_its_own_label_is_refused(self):
        with pytest.raises(crew.Refusal, match=r"you are wldn's door: carry it on with `crew tell <agent>`"):
            crew.send_door(FLEET, "wldn", "wldn-operator", HERE)

    def test_another_drives_operator_may_send(self):
        assert crew.send_door(FLEET, "wldn", "swancloud-operator", HERE) == ("wldn", "wldn-operator")

    def test_a_drive_this_hosts_file_does_not_name_is_refused_naming_the_way_on(self):
        """operator-agent "A drive the host's teams file does not name" (record 0068): the refusal names the drives
        the file names, the file on this host, and that a drive another host runs is sent to once that file names
        it, never by crew send run on that host over ssh."""
        fleet = {**facts.FLEET, "drives": {"wldn": facts.FLEET["drives"]["wldn"]}}
        with pytest.raises(crew.Refusal) as e:
            crew.send_door(fleet, "afterthought", "wldn-planner", "chuck-herdr-alpha")
        said = str(e.value)
        for words in ("not 'afterthought': drives wldn.", f"{crew.TEAMS} on chuck-herdr-alpha names it",
                      "never by crew send run on that host over ssh", "nothing was sent"):
            assert words in said


class TestSend:
    """A send is a tell to the door, the addressee before the text, and one `send` entry in the receiving drive's
    record holding its length and never its text; a send that typed nothing records nothing."""

    @pytest.fixture
    def acts(self, monkeypatch):
        told, emitted, sent = [], [], {"ok": True}
        monkeypatch.setenv("CREW_AGENT", "swancloud-planner")
        monkeypatch.setattr(crew, "this_host", lambda: HERE)
        monkeypatch.setattr(crew, "tell", lambda fleet, name, text, **kw: told.append((name, text, kw)) or sent["ok"])
        monkeypatch.setattr(record, "emit", lambda label, act, on=(), **f: emitted.append((label, act, list(on), f)))
        return told, emitted, sent

    def test_a_delivered_send_is_a_tell_to_the_door_and_one_send_entry(self, acts):
        told, emitted, _ = acts
        text = "The zone check fails on tenants with no region"
        assert crew.send(FLEET, "wldn", text) is True
        assert told == [("wldn-operator", f"(sent to wldn) {text}", {"record": False, "sender": "swancloud-planner", "ask": "send", "reading": None})]
        assert emitted == [("wldn", "send", ["agent/wldn-operator"], {"why": "send wldn", "Chars": 46})]
        assert text not in repr(emitted)

    def test_a_send_that_typed_nothing_records_nothing(self, acts):
        told, emitted, sent = acts
        sent["ok"] = False
        assert crew.send(FLEET, "wldn", "hello") is False
        assert len(told) == 1 and emitted == []

    def test_a_send_whose_entry_is_kept_still_reports_it_sent(self, acts, monkeypatch):
        """run-record "A refused push": the send is typed into its operator and its entry's push is refused,
        record.emit answering None with the entry kept on this host (record.2, pinned by test_record.py); the send
        stands, reported made (record 0068)."""
        told, emitted, _ = acts
        monkeypatch.setattr(record, "emit", lambda label, act, on=(), **f: emitted.append((label, act)) and None)
        assert crew.send(FLEET, "wldn", "hello") is True
        assert emitted == [("wldn", "send")] and len(told) == 1

    def test_a_refused_send_types_and_records_nothing(self, acts):
        told, emitted, _ = acts
        with pytest.raises(crew.Refusal):
            crew.send(FLEET, "swb-1", "hello")
        assert told == [] and emitted == []
