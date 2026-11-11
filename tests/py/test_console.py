"""The console's tabs (the operator-agent spec, The console opens with its shell alone and The console keeps the tabs it
has open): plan.console_tabs on the tabs named, the tabs the console's panes file records with whether herdr still has
each pane, and who follows on the host; and plan.console_asked on the words after the label. That crew console up opens
what the decision names is the main journey's (t-journey-main)."""
import pytest

from crew import Refusal

import crew
import plan


def tabs(asked=(), recorded=None, follower="job"):
    return plan.console_tabs(set(asked), recorded or {}, follower)


def test_a_first_up_while_the_hosts_job_follows_opens_the_shell_tab_alone():
    assert tabs() == (["shell"], [], [])


def test_a_first_up_while_no_one_follows_opens_the_shell_and_the_rail_tab_whose_loop_follows():
    assert tabs(follower="none") == (["shell", "rail"], [], [])


def test_a_rail_tab_following_is_no_job_so_the_rail_tab_opens():
    assert tabs(follower="tab") == (["shell", "rail"], [], [])


def test_a_follower_crew_cant_read_is_no_job_so_the_rail_tab_opens():
    assert tabs(follower="unknown") == (["shell", "rail"], [], [])


def test_the_rail_named_while_the_job_follows_opens_beside_the_shell():
    assert tabs(["rail"]) == (["shell", "rail"], [], [])


def test_tabs_named_open_in_the_order_flow_rail_board_after_the_shell():
    assert tabs(["board", "flow", "rail"]) == (["shell", "flow", "rail", "board"], [], [])


def test_a_second_up_keeps_every_open_tab_and_opens_nothing():
    assert tabs(recorded={"shell": True, "rail": True}) == ([], ["shell", "rail"], [])
    assert tabs(recorded={"shell": True, "flow": True, "rail": True, "board": True}) == ([], ["shell", "flow", "rail", "board"], [])


def test_a_console_opened_before_its_shell_tab_keeps_its_tabs_and_gains_the_shell():
    assert tabs(recorded={"flow": True, "rail": True, "board": True}) == (["shell"], ["flow", "rail", "board"], [])


def test_a_board_tab_the_user_closed_is_forgotten_and_not_opened_again():
    assert tabs(recorded={"shell": True, "board": False}) == ([], ["shell"], ["board"])


def test_a_closed_tab_named_again_is_opened_again():
    assert tabs(["board"], {"shell": True, "board": False}) == (["board"], ["shell"], [])


def test_a_closed_rail_tab_opens_again_while_no_job_follows_and_is_forgotten_while_one_does():
    assert tabs(recorded={"shell": True, "rail": False}, follower="none") == (["rail"], ["shell"], [])
    assert tabs(recorded={"shell": True, "rail": False}) == ([], ["shell"], ["rail"])


def test_a_shell_tab_the_user_closed_opens_again():
    assert tabs(recorded={"shell": False, "rail": True}) == (["shell"], ["rail"], [])


def test_the_words_after_the_label_are_the_tabs_in_any_order():
    assert plan.console_asked([]) == set()
    assert plan.console_asked(["board", "flow"]) == {"flow", "board"}


@pytest.mark.parametrize("words, said", [(["page"], "crew console up opens the tabs flow, rail and board; there is no tab page"),
                                         (["shell"], "crew console up opens the tabs flow, rail and board; there is no tab shell"),
                                         (["rail", "rail"], "crew console up names the rail tab twice")])
def test_a_word_that_is_no_tab_or_a_tab_named_twice_is_refused(words, said):
    with pytest.raises(Refusal, match=said):
        plan.console_asked(words)


def test_the_tabs_are_the_words_after_the_label_and_none_when_none_is_named():
    assert plan.parser().parse_args(["_console", "up", "wldn"]).tabs == []
    assert plan.parser().parse_args(["_console", "up", "wldn", "board", "rail"]).tabs == ["board", "rail"]


class TestTheHostsConsoles:
    """operator-agent, A host opens the consoles its teams file names: crew console up opens a drive's console only on
    a host whose `consoles` names it, in the herdr session named for the label, its tabs in the folder given
    (crew.standing, crew.operator_session; record 0064)."""
    WILLDAN = "/Users/chuck/Code/clients/github_willdan"
    FLEET = {"drives": {"wldn": {"label": "wldn", "machine": "chuck-herdr-alpha", "session": "wldn-2"}},
             "hosts": {"deneb": {"ssh": "deneb", "kind": "darwin"}, "chuck-herdr-alpha": {"ssh": "chuck-herdr-alpha", "kind": "nixos"}},
             "consoles": {"wldn": WILLDAN}}

    def test_a_console_the_host_names_opens_in_its_session_and_folder(self, monkeypatch):
        """A console the host names: deneb opens wldn's console, whose main level runs on chuck-herdr-alpha, in deneb's
        wldn session, its tabs in the folder `consoles` gives."""
        monkeypatch.setattr(crew, "this_host", lambda: "deneb")
        c = crew.standing(self.FLEET, "console", "wldn")
        assert (c.kind, c.session, c.cwd, c.machine, c.host, c.standing) == ("console", "wldn", self.WILLDAN, "deneb", "deneb", ())

    def test_a_console_the_host_does_not_name_is_refused_with_nothing_opened(self, monkeypatch):
        """A console the host does not name: mac-studio's teams file gives no `consoles`."""
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        with pytest.raises(Refusal, match="^mac-studio's teams file names no console of wldn in 'consoles', so no console of "
                                          "wldn opens here$"):
            crew.standing(dict(self.FLEET, consoles={}), "console", "wldn")
