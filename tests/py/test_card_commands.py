"""crew card read and crew's own cards (the rail-cards spec, briefs.16, record 0031): the decisions in
plugin/lib/cards.py, each on plain facts. The card a key names in the run record; what crew sets on a card; a git
remote as Pending You files by it; the area match_area chose, and the kit's
area to make; a tool's reply read as Pending You's CLI reads it, its refusal in Pending You's words, and the bridge's
own error; and what `crew card read` prints. Then the act that sends crew's own cards, plan.row_card_post,
row_card_change and row_card_close, on a stand-in for the bridge, the run record, a tell and an upload (record 0031):
what each sends and records, the line that adopts a card and whom it is told to, a card the user answered left as it
is unless what it asked changed since, a landing's head among it, and then followed by its new version under the key's
revision rather than changed, and each failure said and recorded. Then the port range a card's session starts
plannotator on, plan.session_env.
The bridge itself, and every command's wiring, are t-cards'."""
import json
import re

import pytest

import cards
import crew


def post(key, by, card, at="2026-10-12T10:00:00Z", **more):
    return dict(Act="card.post", Key=key, By=by, Card=card, At=at, **more)


def close(card, by="wldn-ops", **more):
    return dict(Act="card.close", Card=card, By=by, **more)


# --------------------------------------------------------------------------------------- the card a key names

def test_the_card_a_key_names_is_the_agents_newest_post_under_it():
    entries = [post("land/b1/abc1234", "wldn-ops", "req_a"),
               post("land/b1/abc1234", "wldn-ops", "req_b")]
    assert cards.card_under(entries, "land/b1/abc1234", "wldn-ops") == "req_b"


def test_a_closed_card_is_no_longer_held():
    entries = [post("land/b1/abc1234", "wldn-ops", "req_a"), close("req_a")]
    assert cards.card_under(entries, "land/b1/abc1234", "wldn-ops") is None


def test_another_agents_card_under_the_same_key_is_not_this_ones():
    entries = [post("land/b1/abc1234", "wldn-planner", "req_a")]
    assert cards.card_under(entries, "land/b1/abc1234", "wldn-ops") is None


def test_a_refused_post_or_close_holds_nothing_and_closes_nothing():
    entries = [post("land/b1/abc1234", "wldn-ops", "req_a"),
               post("land/b1/abc1234", "wldn-ops", None, Refused="Pending You refused post_request: x"),
               close("req_a", Refused="Pending You refused cancel_request: y")]
    assert cards.card_under(entries, "land/b1/abc1234", "wldn-ops") == "req_a"


def test_a_close_of_an_older_card_leaves_the_newer_held():
    entries = [post("land/b1/abc1234", "wldn-ops", "req_a"), post("land/b1/abc1234", "wldn-ops", "req_b"),
               close("req_a")]
    assert cards.card_under(entries, "land/b1/abc1234", "wldn-ops") == "req_b"


def test_crew_sets_the_key_the_session_and_the_area():
    card = {"kind": "choice", "title": "Which fix for v1?", "options": [{"id": "a", "label": "A"}, {"id": "b", "label": "B"}]}
    got = cards.post_args(card, "land/b1/abc1234", "wldn-ops", "chuck-herdr-alpha", "/w/places/v1", "prj_kit")
    assert got == dict(card, idempotencyKey="land/b1/abc1234", areaId="prj_kit",
                       session={"label": "wldn-ops", "machine": "chuck-herdr-alpha", "cwd": "/w/places/v1"})


# -------------------------------------------------------------------------------------------- where it goes

@pytest.mark.parametrize("url, remote", [
    ("https://github.com/WilldanGroup/switchboard-kit.git", "github.com/WilldanGroup/switchboard-kit"),
    ("git@github.com:afterthought/crew.git", "github.com/afterthought/crew"),
    ("ssh://git@github.com:22/afterthought/crew", "github.com/afterthought/crew"),
    ("https://github.com/afterthought/crew/", "github.com/afterthought/crew"),
    ("/Users/chuck/remotes/crew.git", None),
    ("", None)])
def test_a_remote_is_filed_by_its_host_and_repository(url, remote):
    assert cards.remote_of(url) == remote


def test_match_areas_first_suggestion_is_the_cards_area():
    assert cards.area_of({"decision": "use", "suggestions": [{"areaId": "prj_kit", "name": "switchboard-kit"},
                                                             {"areaId": "prj_other"}]}) == "prj_kit"


@pytest.mark.parametrize("matched", [
    {"decision": "create", "suggestions": [{"areaId": "prj_kit"}]},
    {"decision": "use", "suggestions": []},
    {"decision": "choose", "suggestions": [{"name": "no id"}]},
    {"decision": "use", "suggestions": [{"areaId": "kit"}]},
    {}])
def test_no_area_is_taken_when_match_area_says_create_or_names_none(matched):
    assert cards.area_of(matched) is None


def test_the_kits_area_is_made_under_its_key_in_the_drives_group():
    got = cards.create_area_args("github.com/WilldanGroup/switchboard-kit", "wldn", {"proposedTint": "sage"})
    assert got == {"idempotencyKey": "create-area:WilldanGroup/switchboard-kit", "name": "switchboard-kit",
                   "description": "What crew's agents ask about switchboard-kit.", "tint": "sage", "group": "wldn",
                   "repo": {"remote": "github.com/WilldanGroup/switchboard-kit"}}


def test_an_unknown_tint_is_sky():
    assert cards.create_area_args("github.com/a/b", "wldn", {"proposedTint": "teal"})["tint"] == "sky"


# --------------------------------------------------------------------------------------- reading a reply

def test_a_reply_is_its_structured_content():
    assert cards.reply_object({"structuredContent": {"requestId": "req_1"}, "content": [{"type": "text", "text": "{}"}]}) == {"requestId": "req_1"}


def test_a_reply_is_else_its_first_text_block_that_is_an_object():
    result = {"content": [{"type": "text", "text": "Posted."}, {"type": "text", "text": '{"requestId": "req_1"}'}]}
    assert cards.reply_object(result) == {"requestId": "req_1"}


@pytest.mark.parametrize("result", [{"content": [{"type": "text", "text": "[1]"}]}, {"content": []}, None, "text"])
def test_a_reply_with_no_object_is_none(result):
    assert cards.reply_object(result) is None


def test_a_refusal_is_pending_yous_words():
    result = {"content": [{"type": "text", "text": "Approve requests give their risk in approve.risk."}], "isError": True}
    assert cards.refused_by(result) == "Approve requests give their risk in approve.risk."


def test_a_long_refusal_is_cut_as_pending_yous_cli_cuts_it():
    assert len(cards.refused_by({"content": [{"type": "text", "text": "x" * 400}], "isError": True})) == 300


def test_a_result_not_marked_an_error_is_no_refusal():
    assert cards.refused_by({"content": [{"type": "text", "text": "Not found"}]}) is None


def test_a_refusal_with_no_words_says_so():
    assert cards.refused_by({"isError": True, "content": []}) == "Pending You refused it, and said nothing more"


def test_a_missing_sign_in_is_the_users_to_redo_never_npx():
    said = cards.bridge_said({"code": -32001, "message": "Claude Code on this computer isn’t signed in to Pending You "
                                                         "(https://www.pendingyou.com). Run: npx -y pendingyou@latest init"})
    assert said == ("this host can't ask through Pending You: Claude Code on this computer isn’t signed in to Pending "
                    "You (https://www.pendingyou.com). The user signs it in with pendingyou-signin")


def test_any_other_bridge_error_is_pending_you_unreached():
    assert cards.bridge_said({"code": -32000, "message": "Pending You (https://www.pendingyou.com) couldn’t be reached. "
                                                         "Check this computer’s connection, then try again."}) == \
        ("crew could not reach Pending You: Pending You (https://www.pendingyou.com) couldn’t be reached. "
         "Check this computer’s connection, then try again")


def test_a_reply_naming_no_card_is_refused_as_unread():
    with pytest.raises(crew.Refusal, match="Pending You's answer to post_request names no card"):
        cards.request_id({"status": "pending"}, "post_request")


def test_a_reply_with_no_version_is_refused():
    with pytest.raises(crew.Refusal, match="Pending You gave no version for req_1"):
        cards.version_of({"status": "answered", "version": True}, "req_1")


def test_not_found_is_a_lost_card():
    assert cards.lost("Not found: request:req_5de3dad46fba41068fba.")
    assert not cards.lost("Approve requests give their risk in approve.risk.")
    assert not cards.lost(None)


def test_a_lost_card_is_posted_again_under_its_key_by_the_rails_next_read():
    said = cards.lost_said("land/b1", "req_old", "Not found: request:req_old.")
    assert said.startswith("card req_old under land/b1 is lost to its owner (Pending You: \"Not found: request:req_old.\")")
    assert said.endswith("the rail's next read posts it again under its key, its summary saying an older copy is dead and "
                         "to dismiss it in the app")
    assert cards.lost_said("ask/wldn-ops/hold", "req_q", "Not found.").endswith(
        "Ask it again if it still matters, saying in it that an older copy is dead and to dismiss it in the app")


# ----------------------------------------------------------------------------------------- what read prints

def test_a_card_waiting_on_the_user():
    got = {"requestId": "req_1", "status": "pending", "turn": "you", "version": 1, "url": "https://www.pendingyou.com/app/r/req_1"}
    assert cards.answer_lines("land/b1/abc1234", "req_1", got) == [
        "card land/b1/abc1234: req_1, pending, waiting on the user", "  https://www.pendingyou.com/app/r/req_1"]


def test_an_answer_with_the_users_words():
    got = {"status": "answered", "turn": "agent", "answer": {"choiceIds": ["fix"], "note": {"text": "Both, please.", "via": "voice"}},
           "messages": [{"from": "you", "body": "And add a test."}, {"from": "you"}, "not a message"]}
    assert cards.answer_lines("land/b1/abc1234", "req_1", got) == [
        "card land/b1/abc1234: req_1, answered, your turn: the user has answered", "  picked: fix", "  note: Both, please.",
        "  you: And add a test."]


def test_an_approval_and_a_grouped_answer():
    got = {"status": "answered", "turn": "agent",
           "answer": {"approved": False, "answers": {"plan": {"approved": True}, "units-1": {"choiceIds": ["u1", "u2"]}}}}
    assert cards.answer_lines("proposal/4", "req_1", got)[1:] == ["  approved: no", "  plan: approved", "  units-1: u1, u2"]


def test_an_answer_is_shown_only_on_the_agents_turn():
    got = {"status": "pending", "turn": "you", "answer": {"choiceIds": ["fix"]}}
    assert cards.answer_lines("land/b1/abc1234", "req_1", got) == ["card land/b1/abc1234: req_1, pending, waiting on the user"]


def test_what_the_reply_leaves_out_is_left_out():
    assert cards.answer_lines("land/b1/abc1234", "req_1", {}) == ["card land/b1/abc1234: req_1"]


# ------------------------------------------------------------- the act that sends crew's own cards (record 0031)
# plan.row_card_post, row_card_change and row_card_close on a stand-in for what they reach: the bridge answers as
# Pending You would, and every emit, tell and upload is kept to be read. What each sends and records, and that a
# refusal, a host not signed in, an unread reply and a card not found are said and recorded and refuse nothing.
import plan  # noqa: E402


@pytest.fixture(autouse=True)
def kits(monkeypatch):
    """Each drive's kits as its plan and landings name them (plan.kits_read), with no branch read; and the rail's
    sweep reading no landing here (plan.reap_judged, the landing tests')."""
    monkeypatch.setattr(plan, "kits_read", lambda fleet, label: {"swancloud": ["crew"], "wldn": ["switchboard-kit"]}.get(label, []))
    monkeypatch.setattr(plan, "reap_judged", lambda fleet, label, landings: None)


WHERE = ("/kit/main", "github.com/WilldanGroup/switchboard-kit")
FACTS = dict(bolt="b1", kit="switchboard-kit", units=["v1"], chores=[], batches={"v1": 3}, head="abc1234", at=None, moved=0, pr=None)


class Py:
    """A stand-in for one session with Pending You: each tool answered from answers, a (got, words) pair, or a function
    of the tool's arguments giving one, as Pending You judges what it is sent, a Refusal raised when it is one; a
    session that can't open raises its refusal on entry."""

    def __init__(self, acts, answers, opening=None):
        self.acts, self.answers, self.opening = acts, answers, opening

    def __enter__(self):
        if self.opening:
            raise crew.Refusal(self.opening)
        return self

    def __exit__(self, *exc):
        pass

    def answer(self, tool, args):
        self.acts.calls.append((tool, args))
        got = self.answers.get(tool, ({"ok": True}, None))
        got = got(args) if callable(got) else got
        if isinstance(got, crew.Refusal):
            raise got
        return got

    def call(self, tool, args):
        got, words = self.answer(tool, args)
        if words is not None:
            raise crew.Refusal(f"Pending You refused {tool}: {words}")
        return got


class Acts:
    def __init__(self, answers=None, entries=(), caller="wldn-ops", opening=None, put=None):
        self.answers, self.held, self.who, self.opening, self.put_said = dict(answers or {}), list(entries), caller, opening, put
        self.calls, self.emitted, self.told, self.puts, self.names = [], [], [], [], []

    def bridge(self, name, later, held=None):
        self.names.append(name)
        return Py(self, self.answers, self.opening)

    def emit(self, label, act, on, **fields):
        self.emitted.append(dict(fields, Act=act, On=on, label=label))

    def entries(self, label):
        return self.held

    def tell(self, name, text):
        self.told.append((name, text))
        return True

    def put(self, url, data, kind):
        self.puts.append((url, len(data), kind))
        return self.put_said

    def session(self, label, key, facts):  # a landing card's reading, which crew starts before it builds the card
        return "http://chuck-herdr-alpha.ts.swancloud.net:19432"

    def end(self, label, key):  # no reading recorded on this host, so its close ends none
        return None

    def runner(self, label):  # no preview asked, so a batch card's close puts none away
        return [], {}

    def host(self):
        return "chuck-herdr-alpha"

    def caller(self):
        return self.who

    def kits(self, label):  # the kits the drive's teams build, which tell land/<kit> from land/<bolt>
        return ("switchboard-kit",)


MATCHED = {"decision": "use", "suggestions": [{"areaId": "prj_kit"}]}
POSTED = {"requestId": "req_c1", "url": "https://www.pendingyou.com/app/r/req_c1", "version": 1}


def act_post(acts):
    return plan.row_card_post(None, "wldn", "wldn-ops", cards.landing_card, FACTS, WHERE, acts)


def test_a_card_is_posted_in_its_owners_name_under_its_rows_key_filed_in_its_kit_and_recorded_on_its_row(capsys):
    acts = Acts({"match_area": (MATCHED, None), "post_request": (POSTED, None)})
    assert act_post(acts) == "req_c1"
    assert acts.names == ["wldn-ops"]
    assert [t for t, _ in acts.calls] == ["match_area", "post_request"]
    sent = acts.calls[1][1]
    assert (sent["idempotencyKey"], sent["areaId"], sent["session"]) == (
        "land/b1@wldn", "prj_kit", {"label": "wldn-ops", "machine": "chuck-herdr-alpha", "cwd": "/kit/main"})
    assert sent["approve"]["risk"] == "high"
    assert acts.emitted == [dict(Act="card.post", On=["bolt/b1"], by="wldn-ops", Card="req_c1", Key="land/b1", Head="abc1234",
                                 label="wldn")]
    assert capsys.readouterr().out == ("card land/b1: req_c1 https://www.pendingyou.com/app/r/req_c1\n"
                                       "call get_request (requestId req_c1, name wldn-ops)\n")
    assert acts.told == []


def test_a_card_raised_outside_its_owners_turn_is_told_to_its_owner_with_the_line_that_adopts_it(capsys):
    acts = Acts({"match_area": (MATCHED, None), "post_request": (POSTED, None)}, caller="chuck@chuck-herdr-alpha")
    act_post(acts)
    assert acts.told == [("wldn-ops", "Your card land/b1 is up for the user: call get_request (requestId req_c1, "
                                             "name wldn-ops), to hear their answer.")]
    assert "told wldn-ops: call get_request (requestId req_c1, name wldn-ops)" in capsys.readouterr().out


def test_the_first_card_in_a_kit_makes_its_area_under_the_kits_key_in_the_drives_group():
    acts = Acts({"match_area": ({"decision": "create", "proposedTint": "sage"}, None),
                 "create_area": ({"areaId": "prj_new"}, None), "post_request": (POSTED, None)})
    act_post(acts)
    made = acts.calls[1]
    assert made[0] == "create_area" and (made[1]["idempotencyKey"], made[1]["group"]) == ("create-area:WilldanGroup/switchboard-kit", "wldn")
    assert acts.calls[2][1]["areaId"] == "prj_new"


def test_pending_you_refusing_the_card_is_said_in_its_words_recorded_and_refuses_nothing_of_the_event(capsys):
    acts = Acts({"match_area": (MATCHED, None), "post_request": (None, "Approve requests give their risk in approve.risk.")})
    assert act_post(acts) is None
    assert acts.emitted == [dict(Act="card.post", On=["bolt/b1"], by="wldn-ops", Key="land/b1", label="wldn",
                                 refused="Pending You refused post_request: Approve requests give their risk in approve.risk.")]
    assert "card land/b1 not posted: Pending You refused post_request: Approve requests give their risk in approve.risk." in capsys.readouterr().err


def test_a_host_not_signed_in_is_said_and_recorded_and_the_event_stands(capsys):
    said = cards.bridge_said({"code": cards.SIGNED_OUT, "message": "Claude Code on this computer isn’t signed in to Pending You. Run: npx x"})
    acts = Acts(opening=f"{said}. {plan.CARD_LATER}")
    assert act_post(acts) is None
    assert "this computer isn’t signed in to Pending You" in acts.emitted[0]["refused"] and acts.calls == []
    assert "not posted: this host can't ask through Pending You" in capsys.readouterr().err


def test_a_reply_naming_no_card_is_recorded_as_unread_never_taken_as_empty():
    acts = Acts({"match_area": (MATCHED, None), "post_request": ({"status": "pending"}, None)})
    assert act_post(acts) is None
    assert acts.emitted[0]["refused"] == "Pending You's answer to post_request names no card: crew can't tell what it did"


def test_a_cards_picture_is_put_to_the_upload_url_its_post_returned_with_its_content_type(capsys):
    case = "One more unit."
    facts = dict(n=4, state="open", case=case, before=plan.Plan(PLAN), after=plan.Plan(PLAN_AFTER),
                 argvs=[plan.do_args("wldn", 'unit add g-one "One unit." --repo switchboard-kit')])
    up = dict(POSTED, uploads=[{"title": "The change, once approved", "uploadUrl": "https://up.example/p", "expiresAt": "x"}])
    acts = Acts({"match_area": (MATCHED, None), "post_request": (up, None)}, caller="wldn-planner")
    plan.row_card_post(None, "wldn", "wldn-planner", cards.proposal_card, facts, WHERE, acts)
    assert acts.puts and acts.puts[0][0] == "https://up.example/p" and acts.puts[0][2] == "image/png" and acts.puts[0][1] > 1000
    acts = Acts({"match_area": (MATCHED, None), "post_request": (POSTED, None)}, caller="wldn-planner")
    plan.row_card_post(None, "wldn", "wldn-planner", cards.proposal_card, facts, WHERE, acts)
    assert "its picture did not reach the card: Pending You gave no upload URL for it" in capsys.readouterr().err


HELD = [dict(Act="card.post", Key="land/b1", By="wldn-ops", Card="req_c1")]


def test_a_change_goes_to_the_owners_card_at_the_version_pending_you_reports_with_its_note(capsys):
    acts = Acts({"get_request": ({"status": "pending", "version": 3}, None), "update_request": ({"version": 4}, None)}, entries=HELD)
    assert plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, "Head is now abc1234", WHERE, acts) == "req_c1"
    tool, sent = acts.calls[1]
    assert tool == "update_request" and (sent["requestId"], sent["name"], sent["expectedVersion"], sent["changeNote"]) == (
        "req_c1", "wldn-ops", 3, "Head is now abc1234")
    assert "kind" not in sent and "idempotencyKey" not in sent
    assert acts.emitted == [dict(Act="card.update", On=["bolt/b1"], by="wldn-ops", Card="req_c1", Key="land/b1", Head="abc1234",
                                 label="wldn")]
    assert capsys.readouterr().out == "card land/b1: req_c1 changed, now version 4\n"


def test_a_change_that_finds_its_card_not_found_posts_it_again_saying_the_older_copy_is_dead():
    acts = Acts({"get_request": (None, "Not found: request:req_c1."), "match_area": (MATCHED, None),
                 "post_request": (dict(POSTED, requestId="req_c2"), None)}, entries=HELD)
    assert plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, "x note", WHERE, acts) == "req_c2"
    assert [(e["Act"], e.get("State"), e.get("Card")) for e in acts.emitted] == [("card.close", "lost", "req_c1"), ("card.post", None, "req_c2")]
    assert acts.calls[-1][1]["summary"].startswith(cards.DEAD)
    assert (acts.calls[-1][1]["idempotencyKey"], acts.emitted[-1]["Key"]) == ("land/b1@wldn:2", "land/b1")


ANSWERED = {"status": "answered", "turn": "agent", "version": 3}
MOVED = {"approved": "0123abc" + "0" * 33}  # the head the user approved, before the bolt's head moved to abc1234


def test_a_change_to_a_card_the_user_answered_asking_anew_acks_it_with_the_note_and_posts_the_new_version_following_it(capsys):
    acts = Acts({"get_request": (ANSWERED, None), "ack_answer": ({"version": 4}, None),
                 "match_area": (MATCHED, None), "post_request": (dict(POSTED, requestId="req_c2"), None)}, entries=HELD)
    assert plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, "Head is now abc1234", WHERE, acts,
                                anew=MOVED) == "req_c2"
    assert [t for t, _ in acts.calls] == ["get_request", "ack_answer", "match_area", "post_request"]
    assert acts.calls[1][1] == {"requestId": "req_c1", "name": "wldn-ops", "expectedVersion": 3, "outcome": "Head is now abc1234"}
    sent = acts.calls[3][1]
    assert (sent["idempotencyKey"], sent["follows"], sent["kind"]) == ("land/b1@wldn:2", "req_c1", "approve")
    opening, _, rest = sent["summary"].partition("\n\n")
    assert re.fullmatch(r"You answered the card before this one, by [0-9-]+ [0-9:]+ UTC: crew holds no record of what you "
                        r"answered\. Since then: head is now abc1234\.", opening)
    assert rest.startswith("Its head moved since your approval, from 0123abc to abc1234: approving this lands abc1234.")
    assert [(e["Act"], e.get("Card"), e["Key"], e.get("State"), e.get("Outcome"), e.get("Head")) for e in acts.emitted] == [
        ("card.close", "req_c1", "land/b1", "closed", plan.REVISED, None), ("card.post", "req_c2", "land/b1", None, None, "abc1234")]
    out = capsys.readouterr().out
    assert out.startswith("card land/b1: req_c1 closed, the user having answered it, and its new version follows it\n"
                          "card land/b1: req_c2 https://") and "call get_request (requestId req_c2, name wldn-ops)" in out
    after = HELD + [dict(Act="card.close", Card="req_c1", Key="land/b1", By="wldn-ops", State="closed"),
                    dict(Act="card.post", Key="land/b1", By="wldn-ops", Card="req_c2")]
    assert cards.card_under(after, "land/b1", "wldn-ops") == "req_c2"


def test_a_close_refused_on_a_card_the_user_answered_posts_nothing_and_is_recorded_as_the_change_refused(capsys):
    acts = Acts({"get_request": ({"status": "answered", "version": 3}, None), "ack_answer": (None, "Your latest message asks them something.")},
                entries=HELD)
    assert plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, "x note", WHERE, acts, anew=MOVED) is None
    assert [t for t, _ in acts.calls] == ["get_request", "ack_answer"]
    assert acts.emitted[0]["refused"] == ("Pending You refused the close of the card the user answered: "
                                          "Your latest message asks them something.")


@pytest.mark.parametrize("status, kind_changed, questions, anew, how", [
    ("pending", False, False, False, "change"), ("snoozed", False, False, False, "change"), ("pending", True, False, False, "follow"),
    ("pending", False, True, False, "follow"), ("snoozed", False, True, False, "follow"), ("pending", False, False, True, "change"),
    ("answered", False, False, False, "leave"), ("answered", False, True, False, "leave"), ("answered", False, False, True, "follow"),
    ("answered", True, False, False, "follow"), ("answered", False, True, True, "follow"),
    ("resolved", False, False, False, "leave"), ("closed", False, True, False, "leave"), ("resolved", False, False, True, "ended"),
    ("resolved", True, False, False, "ended"), ("cancelled", False, False, False, "ended"), ("expired", False, True, False, "ended")])
def test_a_card_waiting_on_the_user_is_changed_in_place_and_one_they_answered_is_left_unless_what_it_asks_changed(
        status, kind_changed, questions, anew, how):
    """record 0031 §1 and §3: a card the user has answered is final for what it asked, picked up or acked since or not;
    only its kind changed, or what it asks changed since (anew), follows it, or posts again once Pending You ended it;
    a waiting card is changed in place, or followed when its kind or its questions would not change in place."""
    assert cards.revision({"status": status, "version": 2}, kind_changed, questions, anew) == how


@pytest.mark.parametrize("status", ["answered", "resolved", "closed"])
@pytest.mark.parametrize("note", ["A yes now frees swb-1 for b2", "Its preview of abc1234 is up", "Its reading is at a new link"])
def test_a_change_to_a_card_the_user_answered_that_asks_nothing_anew_leaves_it_as_it_is(capsys, status, note):
    """A landing card the user approved, before ops lands it: a merge freeing the team's next bolt (teams.16), a
    preview's end and a reading's new link change what it offers, not what it asked, so it is neither acked, closed nor
    followed, nothing is recorded, and the approval goes on to ops (plan.16)."""
    acts = Acts({"get_request": (dict(ANSWERED, status=status), None)}, entries=HELD)
    assert plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, note, WHERE, acts) == "req_c1"
    assert [t for t, _ in acts.calls] == ["get_request"] and acts.emitted == [] and acts.told == []
    assert capsys.readouterr().out == "card land/b1: req_c1 is left as it is: the user has answered it\n"


def test_a_card_pending_you_ended_after_the_users_answer_asking_anew_is_recorded_closed_and_followed(capsys):
    """The owner acked the user's approval as it acted on it, so Pending You reads the card resolved; a merge then moved
    the head: the card is recorded closed as Pending You ended it, and the new card follows it, saying so."""
    acts = Acts({"get_request": (dict(ANSWERED, status="resolved"), None), "match_area": (MATCHED, None),
                 "post_request": (dict(POSTED, requestId="req_c2"), None)}, entries=HELD)
    assert plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, "Its head is now abc1234", WHERE, acts,
                                anew={"approved": ""}) == "req_c2"
    assert [t for t, _ in acts.calls] == ["get_request", "match_area", "post_request"]
    sent = acts.calls[2][1]
    assert sent["follows"] == "req_c1" and sent["summary"].startswith("You answered the card before this one, by ")
    assert sent["summary"].split("\n\n")[1].startswith(
        "Its head is now abc1234, and crew holds no record of the head you approved: approving this lands abc1234.")
    assert [(e["Act"], e.get("Card"), e.get("State"), e.get("Outcome")) for e in acts.emitted] == [
        ("card.close", "req_c1", "closed", plan.ENDED_ELSEWHERE), ("card.post", "req_c2", None, None)]


@pytest.mark.parametrize("entries, head, anew", [
    ([], "abc1234", None),
    ([post("land/b1", "wldn-ops", "req_c1", Head="abc1234")], "abc1234", None),
    ([post("land/b1", "wldn-ops", "req_c1", Head="0123abc")], "abc1234", {"approved": "0123abc"}),
    ([post("land/b1", "wldn-ops", "req_c1")], "abc1234", {"approved": ""}),
    ([post("land/b1", "wldn-ops", "req_c1", Head="0123abc"), dict(Act="card.update", Card="req_c1", Key="land/b1", Head="abc1234")],
     "abc1234", None),
    ([post("land/b1", "wldn-ops", "req_c1", Head="0123abc"),
      dict(Act="card.update", Card="req_c1", Key="land/b1", Head="abc1234", Refused="Pending You refused update_request: x")],
     "abc1234", {"approved": "0123abc"}),
    ([post("land/b1", "wldn-ops", "req_c0", Head="abc1234"), post("land/b1", "wldn-ops", "req_c1", Head="0123abc")],
     "abc1234", {"approved": "0123abc"})])
def test_a_card_asks_anew_only_once_the_head_moved_since_the_head_its_last_post_or_change_recorded(entries, head, anew):
    """The head a landing's or a deploy's card asks about is the one its last post or change done recorded, a refused
    change showing the user nothing; a card with none recorded, posted before crew recorded heads, asks anew, since
    crew can't tell which head the user approved (read.1)."""
    held = cards.card_under(entries, "land/b1", "wldn-ops")
    assert cards.head_anew(entries, held, head) == anew


STEP = dict(env="srv", n=1, text="restart crew's teams", doer="swancloud-ops", held=True, why=None, where=None, commands=[], done=None,
            consequences={"now": "It runs at once; no stage is working on srv now"})


def test_a_card_whose_kind_changed_is_withdrawn_while_it_waits_and_its_new_version_posted_following_it(capsys):
    """A step recorded again with an agent as its doer, held, where the user was: its `do` card becomes a choice,
    which update_request never changes (cards.CHANGED)."""
    acts = Acts({"get_request": ({"status": "pending", "version": 3}, None), "cancel_request": ({"version": 4}, None),
                 "match_area": (MATCHED, None), "post_request": (dict(POSTED, requestId="req_s2"), None)},
                entries=[post("op/srv/1", "swancloud-ops", "req_s1")], caller="swancloud-ops")
    note = "Recorded again: its doer and its hold changed"
    assert plan.row_card_change(None, "swancloud", "swancloud-ops", cards.step_card, STEP, note, WHERE, acts, kind_changed=True) == "req_s2"
    assert [t for t, _ in acts.calls] == ["get_request", "cancel_request", "match_area", "post_request"]
    assert acts.calls[1][1] == {"requestId": "req_s1", "name": "swancloud-ops", "reason": note}
    sent = acts.calls[3][1]
    assert (sent["idempotencyKey"], sent["follows"], sent["kind"]) == ("op/srv/1@swancloud:2", "req_s1", "choice")
    assert [(e["Act"], e.get("Card"), e.get("State"), e.get("Outcome")) for e in acts.emitted] == [
        ("card.close", "req_s1", "withdrawn", plan.RENEWED), ("card.post", "req_s2", None, None)]
    assert capsys.readouterr().out.startswith("card op/srv/1: req_s1 withdrawn, its kind having changed, and its new version follows it\n"
                                              "card op/srv/1: req_s2 https://")


def test_a_post_pending_you_answers_with_the_card_the_record_already_holds_open_is_recorded_once(capsys):
    """Read on mac-studio on 2026-10-18: two rail reads, from swancloud-ops's start and the design agent's, swept at
    once; each raised op/swancloud-srv/1's card, Pending You's idempotency gave both req_2a16bbe95cd841c58611, and the
    run record held two posts of it, at 15:24:51Z and 15:24:52Z. Here the other read's post is recorded while this
    one's is asked: this host's record holds nothing under the key until post_request is answered, then that post."""
    acts = Acts({"match_area": (MATCHED, None), "post_request": (POSTED, None)}, caller="chuck@chuck-herdr-alpha")
    acts.entries = lambda label: [post("land/b1", "wldn-ops", "req_c1")] if any(t == "post_request" for t, _ in acts.calls) else []
    assert act_post(acts) == "req_c1"
    assert acts.emitted == [] and acts.told == []
    assert capsys.readouterr().out == ("card land/b1: req_c1 https://www.pendingyou.com/app/r/req_c1, its post recorded already\n"
                                       "call get_request (requestId req_c1, name wldn-ops)\n")


# A step's card following its deploy's card, which swancloud-ops's run record still holds open (rail-cards: a post
# that follows an open card reads it).
DEPLOY_HELD = [post("deploy/srv", "swancloud-ops", "req_d1")]


def act_follow(get_request, entries=DEPLOY_HELD, follows="req_d1", since=None):
    acts = Acts({"match_area": (MATCHED, None), "post_request": (dict(POSTED, requestId="req_s1"), None), "get_request": get_request},
                entries=entries, caller="swancloud-ops")
    facts = dict(STEP, follows=follows) if follows else STEP
    return acts, plan.row_card_post(None, "swancloud", "swancloud-ops", cards.step_card, facts, WHERE, acts, since)


def test_a_post_following_a_card_pending_you_then_reports_resolved_records_the_post_and_then_that_card_closed(capsys):
    acts, card = act_follow(({"status": "resolved", "version": 4}, None))
    assert card == "req_s1"
    assert [t for t, _ in acts.calls] == ["match_area", "post_request", "get_request"]
    assert acts.calls[1][1]["follows"] == "req_d1" and acts.calls[2][1] == {"requestId": "req_d1", "name": "swancloud-ops"}
    assert [(e["Act"], e["On"], e["Card"], e["Key"], e.get("State"), e.get("Outcome")) for e in acts.emitted] == [
        ("card.post", ["env/srv"], "req_s1", "op/srv/1", None, None),
        ("card.close", ["env/srv"], "req_d1", "deploy/srv", "closed", plan.FOLLOWED)]
    assert capsys.readouterr().out.splitlines()[-1] == "card deploy/srv: req_d1 picked up in Pending You by req_s1, which follows it"
    assert cards.card_under(DEPLOY_HELD + [dict(e, By=e["by"]) for e in acts.emitted], "deploy/srv", "swancloud-ops") is None


@pytest.mark.parametrize("status", ["pending", "answered"])
def test_a_post_following_a_card_that_still_waits_or_is_answered_leaves_it_open(status):
    acts, card = act_follow(({"status": status, "turn": "agent", "version": 3}, None))
    assert card == "req_s1" and [t for t, _ in acts.calls] == ["match_area", "post_request", "get_request"]
    assert [e["Act"] for e in acts.emitted] == ["card.post"]


@pytest.mark.parametrize("get_request, why", [
    ((None, "Too many requests."), "Pending You refused get_request: Too many requests."),
    ((None, "Not found: request:req_d1."), "Pending You refused get_request: Not found: request:req_d1."),
    (crew.Refusal(f"Pending You did not answer get_request within 60 seconds. {plan.CARD_LATER}"),
     "Pending You did not answer get_request within 60 seconds.")])
def test_a_post_whose_read_of_the_card_it_follows_fails_stands_and_says_so(capsys, get_request, why):
    acts, card = act_follow(get_request)
    assert card == "req_s1" and [(e["Act"], e.get("refused")) for e in acts.emitted] == [("card.post", None)]
    assert capsys.readouterr().err == f"card deploy/srv: whether req_d1 was picked up can't be read: {why}\n"


@pytest.mark.parametrize("entries, follows", [
    (DEPLOY_HELD, None),
    (DEPLOY_HELD + [dict(Act="card.close", Card="req_d1", Key="deploy/srv", By="swancloud-ops", State="closed")], "req_d1"),
    ([post("deploy/srv", "wldn-ops", "req_d1")], "req_d1")])
def test_a_post_following_nothing_or_a_card_the_record_holds_closed_reads_nothing(entries, follows):
    acts, card = act_follow(({"status": "resolved", "version": 4}, None), entries, follows, ["The deploy ended, and this is its step 1"])
    assert card == "req_s1" and [t for t, _ in acts.calls] == ["match_area", "post_request"]
    assert [e["Act"] for e in acts.emitted] == ["card.post"]


def test_a_post_following_a_card_given_back_as_already_recorded_reads_nothing():
    acts = Acts({"match_area": (MATCHED, None), "post_request": (dict(POSTED, requestId="req_s1"), None)}, caller="swancloud-ops")
    acts.entries = lambda label: DEPLOY_HELD + ([post("op/srv/1", "swancloud-ops", "req_s1")]
                                                if any(t == "post_request" for t, _ in acts.calls) else [])
    plan.row_card_post(None, "swancloud", "swancloud-ops", cards.step_card, dict(STEP, follows="req_d1"), WHERE, acts)
    assert [t for t, _ in acts.calls] == ["match_area", "post_request"] and acts.emitted == []


# swancloud's after-deploy step of the-fleets-pendingyou-is-0-41-0, the Herdr re-sign-in, as deneb's op/deneb/20 held
# it on 2026-11-06: 370 characters and no command fields (signal 2026-11-06-swancloud-ops-bbe53808/01).
HERDR = ("Sign Herdr in to Pending You again on this host, so it holds the scope 0.41.0 asks for (`presence:focus`): run "
         "`pendingyou app login herdr` there, on the box over ssh (`ssh chuck-herdr-alpha pendingyou app login herdr`), and "
         "approve it in the browser or by code on the phone. Then `pendingyou herdr doctor` says \"Holding cards:\", not "
         "\"Sign Herdr in again to hold cards\".")
STEP_WORDS = "Keep each step’s words under 300 characters."  # post_request's refusal on deneb, 2026-11-06


def strict_post(args):
    """Pending You's post_request as deneb met it: a card whose action has a step of 300 characters or more refused in
    its words, any other posted."""
    if any(len(s["text"]) >= 300 for s in (args.get("action") or {}).get("steps") or []):
        return None, STEP_WORDS
    return dict(POSTED, requestId="req_s20"), None


MARKED_WORDS = "With questions, each question carries its own highStakes; leave the card’s highStakes out."  # as test_landings has it


def marked_post(args):
    """Pending You's post_request as the Willdan box and deneb met it (2026-11-10, 2026-11-11): a card of questions
    carrying highStakes, on the card or on any question, refused in its words, any other posted."""
    questions = args.get("questions") or []
    if questions and ("highStakes" in args or any("highStakes" in q for q in questions)):
        return None, MARKED_WORDS
    return dict(POSTED, requestId="req_d7"), None


def test_a_deploy_waiting_on_seven_steps_posts_one_list_of_five_boxes_and_nothing_is_refused():
    """rail-cards "Seven steps the deploy waits on, and Pending You refuses questions carrying highStakes": one list of
    five boxes carrying highStakes on the card posts, its form recorded boxes."""
    qs = [{"id": "q1", "kind": "multi", "options": []}, {"id": "q2", "kind": "multi", "options": []}]
    assert marked_post({"questions": [dict(qs[0], highStakes=True), qs[1]]}) == (None, MARKED_WORDS)
    assert marked_post({"questions": qs, "highStakes": True}) == (None, MARKED_WORDS)
    facts = dict(env="swancloud-srv", head="b" * 40, base="a" * 40, landings=[], notes=None, steps=[], before=[], after=[],
                 waited=[dict(n=str(i), text=f"step {i}", why=f"Why step {i}.", to="b" * 40, key=f"{i}" * 12, state="waiting")
                         for i in range(1, 8)])
    acts = Acts({"match_area": (MATCHED, None), "post_request": marked_post}, caller="swancloud-ops")
    assert plan.row_card_post(None, "swancloud", "swancloud-ops", cards.deploy_card, facts, WHERE, acts) == "req_d7"
    post = next(a for t, a in acts.calls if t == "post_request")
    assert (post["kind"], post["highStakes"], "questions" in post, len(post["options"])) == ("multi", True, False, 5)
    assert [(e["Act"], e.get("refused"), e.get("Card"), e.get("Form")) for e in acts.emitted] == [
        ("card.post", None, "req_d7", "boxes")]


def test_a_users_step_of_370_characters_with_no_commands_gets_its_card_its_words_whole():
    assert len(HERDR) == 370 and strict_post({"action": {"steps": [{"text": HERDR}]}}) == (None, STEP_WORDS)
    facts = dict(env="deneb", n=20, text=HERDR, doer="user", held=False, commands=[],
                 why="the scope is granted only by a sign-in the user approves (`agents.9`); no configuration makes it and no check can do it.")
    acts = Acts({"match_area": (MATCHED, None), "post_request": strict_post}, caller="swancloud-ops")
    assert plan.row_card_post(None, "swancloud", "swancloud-ops", cards.step_card, facts, WHERE, acts) == "req_s20"
    assert [(e["Act"], e.get("refused"), e.get("Card")) for e in acts.emitted] == [("card.post", None, "req_s20")]
    sent = next(a for t, a in acts.calls if t == "post_request")
    assert len(sent["title"]) <= cards.TITLE and all(len(s["text"]) <= cards.STEP for s in sent["action"]["steps"])
    assert sent["action"]["steps"] == [{"text": cards.prose(HERDR, cards.STEP)}]
    assert [(a["lang"], a["title"], a["lines"]) for a in sent["artifacts"]] == [("markdown", "The step", [HERDR])]


def test_a_steps_card_pending_you_still_refuses_is_recorded_refused_in_its_words_and_named_on_its_row():
    """A card refused for a bound crew does not know yet stays owed on the rail with Pending You's words (rail-cards "A
    row's card that Pending You refused is owed until it posts")."""
    acts = Acts({"match_area": (MATCHED, None), "post_request": (None, STEP_WORDS)}, caller="swancloud-ops")
    facts = dict(env="deneb", n=20, text="Sign Herdr in again", doer="user", held=False, commands=[])
    assert plan.row_card_post(None, "swancloud", "swancloud-ops", cards.step_card, facts, WHERE, acts) is None
    refused = [dict(e, Refused=e["refused"]) for e in acts.emitted]  # as the run record writes it
    assert plan.last_refusal(refused, "op/deneb/20") == f"Pending You refused post_request: {STEP_WORDS}"


POST, CLOSE = (lambda card, by="wldn-ops", key="land/b1": dict(Act="card.post", Key=key, By=by, Card=card),
               lambda card, state="closed": dict(Act="card.close", Card=card, State=state))


@pytest.mark.parametrize("entries, asked", [
    ([], "land/b1@wldn"),
    ([POST("req_1")], "land/b1@wldn"),
    ([POST("req_1"), POST("req_1")], "land/b1@wldn"),
    ([POST("req_1"), CLOSE("req_1", "declined")], "land/b1@wldn:2"),
    ([POST("req_1"), CLOSE("req_1"), POST("req_2")], "land/b1@wldn:2"),
    ([POST("req_1"), CLOSE("req_1"), POST("req_2"), CLOSE("req_2", "lost")], "land/b1@wldn:3"),
    ([POST("req_1", by="wldn-planner"), CLOSE("req_1")], "land/b1@wldn"),
    ([POST("req_1", key="land/b2"), CLOSE("req_1")], "land/b1@wldn"),
    ([dict(POST("req_1"), Refused="x"), CLOSE("req_1")], "land/b1@wldn")])
def test_a_card_is_posted_under_its_rows_key_and_after_a_closed_one_under_the_key_with_its_revision(entries, asked):
    assert cards.post_key(entries, "land/b1", "wldn-ops", "wldn") == asked


@pytest.mark.parametrize("key", ["batch/16", "proposal/16", "land/b1", "deploy/dev", "op/dev/1", "record/crew/0031"])
def test_each_drive_sends_its_rows_key_qualified_by_its_label_and_counts_its_revision_in_its_own_run_record(key):
    """briefs.16, read 2026-10-26 (signal 2026-10-26-swancloud-operator-4e81e687/01): madswan's batch 16 was given
    swancloud's batch 16 card, req_eafa10ee554b41edbce6, closed on 2026-10-22, since both main levels post under the
    host's one sign-in and both sent batch/16. Each of crew's six cards is sent under the row's key qualified by its
    drive's label, so two drives' rows of one key are two cards; the first part is still crew's, and each
    drive's revision is read from its own run record, a closed card of the other's under the key counting nothing."""
    by = "planner"
    swancloud = [POST("req_eafa10ee554b41edbce6", by=by, key=key), CLOSE("req_eafa10ee554b41edbce6")]
    sent = {"swancloud": cards.post_key(swancloud, key, by, "swancloud"), "madswan": cards.post_key([], key, by, "madswan")}
    assert sent == {"swancloud": f"{key}@swancloud:2", "madswan": f"{key}@madswan"}
    assert {plan.crews_key(k) for k in sent.values()} == {key.split("/")[0]}


@pytest.mark.parametrize("key, label, first, revised", [
    ("batch/7", "wldn", "batch/7@wldn", "batch/7@wldn:2"), ("land/a", "a", "land/a@a", "land/a@a:2"),
    ("x/1", "a", "x/1@a___", "x/1@a:2_"), ("deploy/dev", "wldn", "deploy/dev@wldn", "deploy/dev@wldn:2")])
def test_a_key_shorter_than_pending_you_takes_is_filled_out_to_eight_characters_the_same_on_every_post(key, label, first, revised):
    """rail-cards: a row's key shorter than Pending You takes. Read on mac-studio on 2026-10-19 (test D): crew could not
    post batch 7's card, the rail saying "card: batch/7, none open; its last post was refused: Pending You refused
    post_request: Some fields need fixing. idempotencyKey: Too small: expected string to have >=8 characters.", since
    batch/<n> under ten is seven characters. The drive's label makes every row's key long enough; a shorter one
    is still filled out at its end, the same on a retry and while its card is open."""
    by = "wldn-planner"
    held, closed = [POST("req_1", by=by, key=key)], [POST("req_1", by=by, key=key), CLOSE("req_1")]
    sent = [cards.post_key(e, key, by, label) for e in ([], [], held, closed)]
    assert sent == [first, first, first, revised] and all(len(k) >= cards.KEY_LEAST for k in sent)


def test_a_change_with_no_card_held_posts_it():
    acts = Acts({"match_area": (MATCHED, None), "post_request": (POSTED, None)})
    assert plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, "x note", WHERE, acts) == "req_c1"
    assert [t for t, _ in acts.calls] == ["match_area", "post_request"]


def test_a_close_acks_an_answered_card_with_its_outcome_and_withdraws_a_waiting_one_with_its_reason(capsys):
    acts = Acts({"get_request": ({"status": "answered", "version": 3}, None)}, entries=HELD)
    assert plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", outcome="Landed as #24 at 14:02", acts=acts) == "req_c1"
    assert acts.calls[1] == ("ack_answer", {"requestId": "req_c1", "name": "wldn-ops", "expectedVersion": 3, "outcome": "Landed as #24 at 14:02"})
    assert acts.emitted[0] == dict(Act="card.close", On=["bolt/b1"], by="wldn-ops", Card="req_c1", Key="land/b1", State="closed",
                                   Outcome="Landed as #24 at 14:02", label="wldn")
    acts = Acts({"get_request": ({"status": "pending", "version": 1}, None)}, entries=HELD)
    plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", reason="Held for a fix: the log is empty", acts=acts)
    assert acts.calls[1] == ("cancel_request", {"requestId": "req_c1", "name": "wldn-ops", "reason": "Held for a fix: the log is empty"})
    assert acts.emitted[0]["State"] == "withdrawn"
    assert capsys.readouterr().out.splitlines()[-1] == "card land/b1: req_c1 withdrawn"


def test_a_landing_on_the_users_words_sends_them_answered_here_and_records_the_outcome_without_them(capsys):
    """plan.16, main-level spec "The card closes with the user's words": a landing card still waiting closes as answered
    in the conversation, Pending You sent the user's words, the run record the outcome alone (record.3); one the user
    also tapped is acked with the words."""
    landed = plan.landed_words("c" * 40, "24")
    outcome, said = f"Landed on the user's word in wldn-ops's pane; {landed}", f'Landed on the user\'s word in wldn-ops\'s pane, "Land swb-1\'s bolt"; {landed}'
    acts = Acts({"get_request": ({"status": "pending", "version": 1}, None)}, entries=HELD)
    assert plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", outcome=outcome, acts=acts, said=said, here=True) == "req_c1"
    assert acts.calls[1] == ("cancel_request", {"requestId": "req_c1", "name": "wldn-ops", "reason": cards.cut(said, cards.OUTCOME),
                                                "answeredHere": True})
    assert acts.calls[1][1]["reason"].startswith('Landed on the user\'s word in wldn-ops\'s pane, "Land swb-1\'s bolt"; landed on')
    assert (acts.emitted[0]["State"], acts.emitted[0]["Outcome"]) == ("closed", outcome)
    assert "Land swb-1's bolt" not in repr(acts.emitted)
    assert capsys.readouterr().out.splitlines()[0] == "card land/b1: req_c1 closed"
    acts = Acts({"get_request": ({"status": "answered", "version": 3}, None)}, entries=HELD)
    plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", outcome=outcome, acts=acts, said=said, here=True)
    assert acts.calls[1][0] == "ack_answer" and "answeredHere" not in acts.calls[1][1]
    assert (acts.emitted[0]["State"], acts.emitted[0]["Outcome"]) == ("closed", outcome)


LONG = ("Applied: added " + ", ".join(f"the-unit-that-does-thing-{i}" for i in range(1, 9))
        + "; 3 other changes. Left out on your word: the-briefs-say-never-wt-submit-help.")


def test_a_close_cuts_its_outcome_and_its_reason_to_pending_yous_two_hundred_characters_and_records_them_whole():
    """Read on 2026-10-18: the planner's `crew plan answer 142 ...` applied the proposal and printed "card
    proposal/139 not closed: Pending You refused the close: Some fields need fixing. outcome: Too big: expected
    string to have <=200 characters.", the card left open. Pending You takes an outcome or a reason of 200 characters
    at most (cards.OUTCOME)."""
    assert len(LONG) > cards.OUTCOME
    held = [post("proposal/139", "wldn-planner", "req_p1")]
    acts = Acts({"get_request": ({"status": "answered", "turn": "agent", "version": 3}, None)}, entries=held, caller="wldn-planner")
    acts.end = lambda label, key: None  # a proposal's reading session, which this one has none of
    assert plan.row_card_close(None, "wldn", "wldn-planner", "proposal/139", outcome=LONG, acts=acts) == "req_p1"
    tool, sent = acts.calls[1]
    assert (tool, len(sent["outcome"]), sent["outcome"][-1]) == ("ack_answer", cards.OUTCOME, "…")
    assert LONG.startswith(sent["outcome"][:-1]) and acts.emitted[0]["Outcome"] == LONG
    acts = Acts({"get_request": ({"status": "pending", "version": 1}, None)}, entries=held, caller="wldn-planner")
    acts.end = lambda label, key: None
    plan.row_card_close(None, "wldn", "wldn-planner", "proposal/139", reason=LONG, acts=acts)
    tool, sent = acts.calls[1]
    assert (tool, len(sent["reason"]), acts.emitted[0]["Outcome"]) == ("cancel_request", cards.OUTCOME, LONG)
    short = cards.close_call({"status": "pending"}, "req_p1", "wldn-planner", reason="Dropped: not now")
    assert short[1]["reason"] == "Dropped: not now"


def test_the_close_of_a_card_the_user_answered_records_what_they_answered_in_crews_words_and_a_withdrawal_none():
    """rail-cards "An answered card's close records what the user answered from names alone": the landings card sent with land:y ticked,
    land:z cleared and a note; a deploy declined with "not tonight"; a card still waiting, withdrawn, records none."""
    sent = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y"], "note": "z after its fix"}}
    held = [post("land/crew", "swancloud-ops", "req_k1")]
    acts = Acts({"get_request": (sent, None)}, entries=held, caller="swancloud-ops")
    plan.row_card_close(None, "swancloud", "swancloud-ops", "land/crew", outcome="Asked of the runner as you ticked: y.", acts=acts,
                        offered=["land:y", "land:z"], Rows="1")
    assert (acts.emitted[0]["State"], acts.emitted[0]["Answer"], acts.emitted[0]["Rows"]) == ("closed", "ticked y, left z, with a note", "1")
    assert "after its fix" not in repr(acts.emitted)
    declined = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": False, "text": "not tonight"}}
    acts = Acts({"get_request": (declined, None)}, entries=[post("deploy/srv", "swancloud-ops", "req_d1")], caller="swancloud-ops")
    plan.row_card_close(None, "swancloud", "swancloud-ops", "deploy/srv", outcome="Declined", acts=acts)
    assert acts.emitted[0]["Answer"] == "declined, with a note" and "tonight" not in repr(acts.emitted)
    acts = Acts({"get_request": ({"status": "pending", "turn": "you", "version": 1}, None)}, entries=HELD)
    plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", reason="Held for a fix", acts=acts)
    assert acts.emitted[0]["State"] == "withdrawn" and "Answer" not in acts.emitted[0]


def test_a_card_closed_as_answered_in_its_owners_pane_records_the_pane_as_its_answer():
    landed = plan.landed_words("c" * 40, "24")
    outcome, said = f"Landed on the user's word in wldn-ops's pane; {landed}", f'Landed on the user\'s word in wldn-ops\'s pane, "Land swb-1\'s bolt"; {landed}'
    acts = Acts({"get_request": ({"status": "pending", "turn": "you", "version": 1}, None)}, entries=HELD)
    plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", outcome=outcome, acts=acts, said=said, here=True)
    assert (acts.emitted[0]["State"], acts.emitted[0]["Answer"]) == ("closed", "answered in wldn-ops's pane")


def test_a_card_followed_once_answered_records_the_answer_on_its_close_and_on_the_entries_its_new_card_follows(monkeypatch):
    acts = Acts({"get_request": (dict(ANSWERED, answer={"approved": True}), None), "ack_answer": ({"version": 4}, None),
                 "match_area": (MATCHED, None), "post_request": (dict(POSTED, requestId="req_c2"), None)}, entries=HELD)
    seen, posted = [], plan.card_posted
    monkeypatch.setattr(plan, "card_posted", lambda *a, **kw: seen.append(a[5]) or posted(*a, **kw))
    plan.row_card_change(None, "wldn", "wldn-ops", cards.landing_card, FACTS, "Head is now abc1234", WHERE, acts, anew=MOVED)
    close = acts.emitted[0]
    assert (close["Act"], close["State"], close["Answer"]) == ("card.close", "closed", "approved")
    (entries,) = seen
    assert {k: entries[-1][k] for k in ("Act", "Card", "State", "Answer")} == {"Act": "card.close", "Card": "req_c1", "State": "closed",
                                                                             "Answer": "approved"}
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", entries[-1]["At"])


class TestAnswerSeen:
    """rail-cards "crew records the user's answer the first time it reads it" (design Decision 1): plan.answer_seen, one
    card.answer per card, on its object in its owner's name, its Answer in crew's words."""
    APPROVED = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}

    def test_the_users_answer_is_recorded_once_on_the_rows_object_in_its_owners_name(self, capsys):
        held = [post("proposal/57", "wldn-planner", "req_57")]
        acts = Acts(entries=held, caller="wldn-planner")
        got = plan.answer_seen(acts, "wldn", "wldn-planner", "proposal/57", "req_57", self.APPROVED, held)
        (e,) = acts.emitted
        assert {k: e[k] for k in ("Act", "On", "by", "Card", "Key", "Answer")} == {
            "Act": "card.answer", "On": ["proposal/57"], "by": "wldn-planner", "Card": "req_57", "Key": "proposal/57", "Answer": "approved"}
        assert got == {"Card": "req_57", "Key": "proposal/57", "Answer": "approved"} and "Heads" not in e
        assert "req_57 was answered, approved" in capsys.readouterr().err
        again = Acts(entries=held + [dict(e, Act="card.answer")], caller="wldn-planner")
        assert plan.answer_seen(again, "wldn", "wldn-planner", "proposal/57", "req_57", self.APPROVED, again.held) is None
        assert again.emitted == []

    def test_a_refused_answer_entry_records_it_again_and_a_card_still_waiting_records_nothing(self):
        held = [post("proposal/57", "wldn-planner", "req_57"), dict(Act="card.answer", Card="req_57", Refused="x")]
        assert plan.answer_due(held, "req_57") and not plan.answer_due(held + [dict(Act="card.answer", Card="req_57")], "req_57")
        acts = Acts(entries=held, caller="wldn-planner")
        waiting = {"status": "pending", "turn": "you", "version": 1}
        assert plan.answer_seen(acts, "wldn", "wldn-planner", "proposal/57", "req_57", waiting, held) is None and acts.emitted == []

    def test_a_landings_cards_heads_are_the_bolts_ticked_at_the_heads_the_card_showed(self):
        held = [post("land/switchboard-kit", "wldn-ops", "req_e9", Heads="a@1111111 b@2222222")]
        got = {"status": "answered", "turn": "agent", "version": 2, "answer": {"choiceIds": ["land:a"]}}
        acts = Acts(entries=held)
        plan.answer_seen(acts, "wldn", "wldn-ops", "land/switchboard-kit", "req_e9", got, held,
                         heads=plan.card_heads("a@1111111 b@2222222"), offered=["land:a", "land:b"])
        (e,) = acts.emitted
        assert (e["On"], e["Answer"], e["Heads"]) == (["kit/switchboard-kit"], "ticked a, left b", "a@1111111")
        none = {"status": "answered", "turn": "agent", "version": 2, "answer": {"choiceIds": []}}
        acts = Acts(entries=held)
        plan.answer_seen(acts, "wldn", "wldn-ops", "land/switchboard-kit", "req_e9", none, held,
                         heads=plan.card_heads("a@1111111 b@2222222"), offered=["land:a", "land:b"])
        assert acts.emitted[0]["Answer"] == "ticked none, left a and b" and "Heads" not in acts.emitted[0]

    def test_a_questions_answer_is_on_its_asker(self):
        held = [post("ask/agentplot-design/sluice-who-claims", "agentplot-design", "req_q2")]
        acts = Acts(entries=held, caller="agentplot-design")
        got = {"status": "answered", "turn": "agent", "version": 2, "answer": {"choiceIds": ["a"]}}
        plan.answer_seen(acts, "wldn", "agentplot-design", "ask/agentplot-design/sluice-who-claims", "req_q2", got, held)
        (e,) = acts.emitted
        assert (e["On"], e["Card"], e["Key"], e["Answer"]) == (["agent/agentplot-design"], "req_q2", "ask/agentplot-design/sluice-who-claims", "picked a")

    def test_a_note_is_said_with_a_note_and_never_its_words(self):
        held = [post("proposal/57", "wldn-planner", "req_57")]
        acts = Acts(entries=held, caller="wldn-planner")
        got = dict(self.APPROVED, answer={"approved": True, "note": "but drop the third unit"})
        plan.answer_seen(acts, "wldn", "wldn-planner", "proposal/57", "req_57", got, held)
        assert acts.emitted[0]["Answer"] == "approved, with a note" and "third unit" not in repr(acts.emitted)


def test_a_followed_card_pending_you_picked_up_records_the_answer_its_reply_still_carries():
    acts, card = act_follow(({"status": "resolved", "version": 4, "answer": {"approved": True}}, None))
    assert [(e["Act"], e.get("Answer")) for e in acts.emitted] == [("card.post", None), ("card.close", "approved")]


# A record's card the user answered with a note, and the design agent's revision of the record after it (rail-cards
# "A follow-on card opens with one paragraph on the user's answer and what changed", "A follow-on with nothing changed is not posted").
DESIGN, RKEY = "swancloud-design", "record/crew/0019"
RECORD = dict(kit="crew", number=19, title="One card per thing", opening="A card asked again says what changed.", quoted=[],
              text="# 19. One card per thing\n\nBody.", alternatives=None)
ANSWERED_ON = [post(RKEY, DESIGN, "req_1", at="2026-10-23T13:10:04Z"),
               dict(Act="card.close", Key=RKEY, By=DESIGN, Card="req_1", State="closed", At="2026-10-23T14:02:41Z",
                    Answer="declined, with a note")]
OPENED = "You answered the card before this one, posted 2026-10-23 13:10 UTC, by 14:02 UTC: declined, with a note. Since then: "


def record_post(entries, since, follows="req_1"):
    acts = Acts({"match_area": (MATCHED, None), "post_request": (dict(POSTED, requestId="req_2"), None)}, entries=entries, caller=DESIGN)
    acts.kits = lambda label: ("crew",)
    b = cards.record_card(dict(RECORD, follows=follows))
    return acts, plan.card_posted(acts, "swancloud", DESIGN, b, WHERE, since=since)


def test_a_post_following_a_card_the_user_answered_opens_with_what_they_answered_and_what_changed_and_follows_it():
    acts, card = record_post(ANSWERED_ON, ["Revised at 4be21c0: docs(adr): 0019 takes the user's note"])
    assert card == "req_2"
    sent = acts.calls[-1][1]
    said = OPENED + "revised at 4be21c0: docs(adr): 0019 takes the user's note."
    assert sent["summary"].startswith(said + "\n\nA card asked again says what changed.")
    assert sent["context"]["background"].startswith(said) and sent["follows"] == "req_1"
    assert [(e["Act"], e.get("Card"), e.get("State")) for e in acts.emitted] == [("card.post", "req_2", None)]


@pytest.mark.parametrize("since", [None, []])
def test_a_post_following_a_card_the_user_answered_with_nothing_changed_is_recorded_standing_and_not_posted(capsys, since):
    acts, card = record_post(ANSWERED_ON, since)
    assert card is None and acts.calls == [] and acts.names == []
    words = "Not posted: nothing has changed since the user answered req_1 by 2026-10-23 14:02 UTC, so their answer stands"
    assert acts.emitted == [dict(Act="card.post", On=["record/crew/0019"], by=DESIGN, refused=words, Card="req_1", Key=RKEY,
                                 State="stands", label="swancloud")]
    assert capsys.readouterr().err == f"card {RKEY}: {words}\n"
    stood = ANSWERED_ON + [dict(acts.emitted[0], By=DESIGN, Refused=words)]
    assert cards.card_under(stood, RKEY, DESIGN) is None and plan.last_refusal(stood, RKEY) == words


def test_a_later_post_with_something_changed_follows_the_card_whose_answer_stands():
    stood = ANSWERED_ON + [dict(Act="card.post", Key=RKEY, By=DESIGN, Card="req_1", State="stands", Refused="Not posted: …")]
    acts, card = record_post(stood, ["Revised at 9c0ffee: docs(adr): 0019 names the key"], follows=None)
    sent = acts.calls[-1][1]
    assert card == "req_2" and sent["follows"] == "req_1" and sent["summary"].startswith(OPENED + "revised at 9c0ffee")
    assert sent["idempotencyKey"] == "record/crew/0019@swancloud:2"


def test_a_post_following_no_card_the_user_answered_is_posted_as_built():
    acts, card = record_post([], None, follows=None)
    sent = acts.calls[-1][1]
    assert sent["summary"] == cards.record_card(RECORD)["card"]["summary"] and "follows" not in sent
    acts = Acts({"match_area": (MATCHED, None), "post_request": (POSTED, None)})
    act_post(acts)
    assert acts.calls[-1][1]["summary"] == cards.landing_card(FACTS)["card"]["summary"]


def test_a_change_with_no_card_held_hands_what_changed_to_the_post_it_makes():
    """The record's card was withheld once, its answer standing: the change holds no card, and posts the next revision
    following req_1, saying what changed, or withholds it again when the event gives nothing changed."""
    stood = ANSWERED_ON + [dict(Act="card.post", Key=RKEY, By=DESIGN, Card="req_1", State="stands", Refused="Not posted: …")]
    acts = Acts({"match_area": (MATCHED, None), "post_request": (dict(POSTED, requestId="req_2"), None)}, entries=stood, caller=DESIGN)
    acts.kits = lambda label: ("crew",)
    assert plan.row_card_change(None, "swancloud", DESIGN, cards.record_card, RECORD, "Revised at 4be21c0: x", WHERE, acts,
                                since=["Revised at 4be21c0: x"]) == "req_2"
    assert acts.calls[-1][1]["summary"].startswith(OPENED + "revised at 4be21c0: x.") and acts.calls[-1][1]["follows"] == "req_1"
    acts = Acts(entries=stood, caller=DESIGN)
    acts.kits = lambda label: ("crew",)
    assert plan.row_card_change(None, "swancloud", DESIGN, cards.record_card, RECORD, "x", WHERE, acts, since=[]) is None
    assert acts.calls == [] and acts.emitted[0]["State"] == "stands"


@pytest.mark.parametrize("since", [None, []])
def test_a_card_following_one_the_user_answered_that_pending_you_no_longer_finds_is_posted_again_never_withheld(since):
    """rail-cards "A row's card lost to its owner is posted again": the card that followed req_1 is lost to its owner,
    and its copy is the row's card the user can no longer reach, no follow-on with nothing changed: posted again
    following req_1, opening with what the user answered and the change's note when the event gives nothing changed."""
    held = ANSWERED_ON + [post(RKEY, DESIGN, "req_2", at="2026-10-23T15:00:00Z")]
    acts = Acts({"get_request": (None, "Not found: request:req_2."), "match_area": (MATCHED, None),
                 "post_request": (dict(POSTED, requestId="req_3"), None)}, entries=held, caller=DESIGN)
    acts.kits = lambda label: ("crew",)
    assert plan.row_card_change(None, "swancloud", DESIGN, cards.record_card, dict(RECORD, follows="req_1"), "Raised again", WHERE, acts,
                                since=since) == "req_3"
    assert [(e["Act"], e.get("Card"), e.get("State")) for e in acts.emitted] == [("card.close", "req_2", "lost"), ("card.post", "req_3", None)]
    sent = acts.calls[-1][1]
    assert sent["follows"] == "req_1" and sent["summary"].startswith(OPENED + "raised again.\n\n" + cards.DEAD)


def test_a_close_pending_you_does_not_find_is_recorded_lost_and_a_refused_one_recorded_refused():
    acts = Acts({"get_request": (None, "Not found: request:req_c1.")}, entries=HELD)
    assert plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", outcome="x", acts=acts) is None
    assert [(e["Act"], e["State"]) for e in acts.emitted] == [("card.close", "lost")]
    acts = Acts({"get_request": ({"status": "pending", "version": 1}, None), "cancel_request": (None, "Too many requests.")}, entries=HELD)
    assert plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", reason="x", acts=acts) is None
    assert acts.emitted[0]["refused"] == "Pending You refused the close: Too many requests."


def test_a_close_with_no_card_held_closes_nothing_and_says_so(capsys):
    acts = Acts()
    assert plan.row_card_close(None, "wldn", "wldn-ops", "land/b1", outcome="x", acts=acts) is None
    assert acts.calls == [] and acts.emitted == []
    assert capsys.readouterr().out == "card land/b1: wldn-ops holds none open on this host, so none is closed\n"


PLAN = "%rec: Bolt\n%key: Bolt\n\n%rec: Unit\n%key: Unit\n"
PLAN_AFTER = PLAN + "\nUnit: g-one\nRepo: switchboard-kit\nIntent: One unit.\n"


# ------------------------------------------------------------------------------------ the port a session takes
# plan.session_env: the environment a card's session starts plannotator in, so it takes the first free port of a
# range wherever crew runs (card-sessions), read against plannotator 0.28.26's reading of PLANNOTATOR_PORT.

def test_a_session_with_no_port_named_takes_crews_range():
    assert plan.session_env({})["PLANNOTATOR_PORT"] == "19432-19451" == plan.CARD_PORTS


def test_a_range_the_environment_names_is_kept():
    assert plan.session_env({"PLANNOTATOR_PORT": "19440-19460"})["PLANNOTATOR_PORT"] == "19440-19460"


@pytest.mark.parametrize("named", ["19432", "abc", "19451-19432", "0-10", "19432-70000", ""])
def test_one_port_or_one_plannotator_cant_read_gives_crews_range(named):
    assert plan.session_env({"PLANNOTATOR_PORT": named})["PLANNOTATOR_PORT"] == "19432-19451"


@pytest.mark.parametrize("environ", [{}, {"PLANNOTATOR_PORT": "19440-19460"},
                                     {"PLANNOTATOR_REMOTE": "0", "PLANNOTATOR_SKIP_BROWSER_OPEN": "0"}])
def test_every_session_is_remote_and_opens_no_browser(environ):
    env = plan.session_env(environ)
    assert env["PLANNOTATOR_REMOTE"] == "1" and env["PLANNOTATOR_SKIP_BROWSER_OPEN"] == "1"


def test_the_rest_of_the_environment_passes_through_and_the_one_given_is_not_changed():
    environ = {"PLANNOTATOR_URL_HOST": "auto", "PATH": "/bin", "PLANNOTATOR_PORT": "19432"}
    env = plan.session_env(environ)
    assert env["PLANNOTATOR_URL_HOST"] == "auto" and env["PATH"] == "/bin"
    assert environ == {"PLANNOTATOR_URL_HOST": "auto", "PATH": "/bin", "PLANNOTATOR_PORT": "19432"}


# --------------------------------------------------------------------------------- a session's end, swept
# plan.end_session, and crew card read on a batch whose card's close ends its session: the key's folder swept whether
# or not the drive's cards folder for it exists, a folder another end swept first, as the card hook's crew card end
# or the rail's sweep may while this one reads plannotator's list, swept as empty and never raised.

class TestSessionEnd:
    S = {"pid": 42, "document": "/c/00-summary.md", "url": "http://chuck-herdr-alpha.ts.swancloud.net:19432",
         "started": "2026-10-23T10:00:00Z"}

    def recorded(self, monkeypatch, tmp_path, key):
        """The key's session recorded under the drive's cards folder, and another end sweeping its folder while
        this one reads plannotator's list, which still lists the session, whose pid has gone by its signal."""
        d = tmp_path / "wldn" / key
        d.mkdir(parents=True)
        (d / "session.json").write_text(json.dumps(self.S))
        (tmp_path / "wldn" / "proposal").mkdir()  # another key's folder, so the drive's stays

        def listed():
            for f in d.iterdir():
                f.unlink()
            d.rmdir()
            return {42: {"target": self.S["document"]}}, None

        def kill(pid, sig):
            raise ProcessLookupError(pid)
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        monkeypatch.setattr(plan, "plannotator_sessions", listed)
        monkeypatch.setattr(plan.os, "kill", kill)
        return d

    def test_a_folder_swept_by_another_end_meanwhile_is_swept_as_empty_and_its_end_said(self, monkeypatch, tmp_path):
        d = self.recorded(monkeypatch, tmp_path, "batch/3")
        assert plan.end_session("wldn", "batch/3") == ("batch/3's session had already ended, and batch/3 is forgotten", False)
        assert not d.parent.exists() and (tmp_path / "wldn" / "proposal").is_dir()

    def test_a_key_with_no_folder_ends_nothing_and_makes_none(self, monkeypatch, tmp_path):
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        assert plan.end_session("wldn", "proposal/9") == ("no session was running for proposal/9", False)
        assert not (tmp_path / "wldn").exists()

    def test_a_batchs_read_closes_its_card_and_returns_though_another_end_swept_its_folder(self, monkeypatch, tmp_path, capsys):
        d = self.recorded(monkeypatch, tmp_path, "batch/3")
        sent = {"status": "answered", "turn": "agent", "version": 2, "answer": {"note": {"text": "Read."}}}
        acts = Acts({"get_request": (sent, None)}, [post("batch/3", "wldn-planner", "req_b3", On=["batch/3"])])
        acts.end = lambda label, key: plan.end_session(label, key)[0]
        fleet = {"drives": {"wldn": {"label": "wldn", "machine": "chuck-herdr-alpha"}}, "hosts": {}}
        plan.batch_card_read(fleet, "wldn", "batch/3", "wldn-planner", acts=acts)
        assert [e["Act"] for e in acts.emitted] == ["card.close"]
        assert capsys.readouterr().out.splitlines() == [
            "batch/3: sent back on its card, with a note:", "Read.", "card batch/3: req_b3 closed",
            "batch/3's session had already ended, and batch/3 is forgotten"]
        assert not d.parent.exists()


# --------------------------------------------------------------------------------------------- crew card wait, gone

class TestCardWaitGone:
    """card-sessions "The old wait run": crew keeps no process waiting on a card or its reading (teams.24), so crew card
    wait is refused at once, naming crew card read <key>, and reads, starts and leaves nothing."""

    @pytest.mark.parametrize("key", ["batch/3", "land/y", "proposal/4", "land/switchboard-kit"])
    def test_the_old_wait_is_refused_at_once_naming_the_read_and_starts_nothing(self, key, monkeypatch, tmp_path):
        import argparse
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        monkeypatch.setattr(plan.subprocess, "Popen", lambda *a, **k: pytest.fail("crew card wait started a process"))
        with pytest.raises(crew.Refusal, match=f"^crew card wait is gone: crew keeps no process waiting on a card or its "
                                               f"reading. Run crew card read {re.escape(key)} when"):
            plan.card_wait(None, argparse.Namespace(key=key, unit=None, label="wldn", sub="wait"))
        assert list(tmp_path.iterdir()) == []

    def test_the_wait_its_wait_constants_and_the_readings_it_started_are_gone(self):
        for name in ("batch_wait", "land_start", "land_unstarted", "batch_unstarted", "CARD_POLL", "CARD_READ"):
            assert not hasattr(plan, name), name


# ------------------------------------------------------------------------------- a sent reading, at the refresh
# plan.readings_due and the sweep's acts on it (card-sessions "The rail's refresh tells a reading's owner once that the
# user sent it"; review-batches "The session approved", "Notes sent while the planner is down").

NOTES = ("annotated", "1. x1: say what a zone is.", 1)


def test_a_sent_reading_is_told_once_a_wordless_batch_recorded_and_nothing_else_acted_on():
    assert plan.readings_due([("land/y", NOTES, False), ("batch/3", NOTES, False), ("proposal/4", ("approved", None, 0), False),
                              ("batch/4", ("approved", None, 0), False), ("batch/5", ("approved", "Fine.", 0), False)]) == [
        ("land/y", "tell"), ("batch/3", "tell"), ("proposal/4", "tell"), ("batch/4", "record"), ("batch/5", "tell")]
    assert plan.readings_due([("land/y", NOTES, True), ("proposal/4", ("dismissed", None, None), False), ("batch/3", None, False)]) == []


def test_only_a_live_keys_reading_with_a_result_is_read_and_a_mark_is_seen(tmp_path):
    for key, result, told in (("land/y", {"decision": "annotated", "feedback": "x"}, False),
                              ("batch/3", {"decision": "approved"}, True), ("land/gone", {"decision": "approved"}, False),
                              ("batch/4-1/u1", {"decision": "approved"}, False), ("proposal/4", None, False)):
        d = tmp_path / key
        d.mkdir(parents=True)
        if result:
            (d / "result.json").write_text(json.dumps(result))
        if told:
            (d / "told.json").write_text("{}")
    live = {"land/y", "batch/3", "batch/4-1", "proposal/4"}
    assert plan.readings_sent(tmp_path, live, []) == [("batch/3", ("approved", None, None), True), ("land/y", ("annotated", "x", None), False)]
    assert plan.readings_sent(tmp_path, live, ["batch/"]) == [("land/y", ("annotated", "x", None), False)]


def test_a_reading_read_before_any_refresh_leaves_it_nothing_to_tell(tmp_path):
    """card-sessions "Read before the refresh": crew card read sets the decision aside, or ends the batch's reading."""
    d = tmp_path / "land/y"
    d.mkdir(parents=True)
    (d / "session.json").write_text(json.dumps({"pid": 42, "document": "/c/00-y.md", "url": "http://x:19432", "started": "2026-10-23T10:00:00Z"}))
    (d / "result.json").write_text(json.dumps({"decision": "annotated", "feedback": "x"}))
    plan.reading_decided(d, ("annotated", "x", None))
    assert plan.readings_sent(tmp_path, {"land/y"}, []) == []


def test_a_told_mark_goes_with_the_reading_it_marked_so_the_next_one_is_told_of_again(tmp_path):
    """card-sessions "A landing's reading sent": crew card read sets the reading aside and its told mark with it, and a
    new session the user then sends is told of once more."""
    d = tmp_path / "land/y"
    d.mkdir(parents=True)
    (d / "session.json").write_text(json.dumps({"pid": 42, "document": "/c/00-y.md", "url": "http://x:19432", "started": "2026-10-23T10:00:00Z"}))
    (d / "result.json").write_text(json.dumps({"decision": "annotated", "feedback": "x"}))
    (d / "told.json").write_text("{}")
    assert plan.readings_sent(tmp_path, {"land/y"}, []) == [("land/y", ("annotated", "x", None), True)]
    plan.reading_decided(d, ("annotated", "x", None))
    assert not (d / "told.json").exists()
    (d / "result.json").write_text(json.dumps({"decision": "approved"}))
    assert plan.readings_due(plan.readings_sent(tmp_path, {"land/y"}, [])) == [("land/y", "tell")]
    (d / "told.json").write_text("{}")
    plan.untold(d)
    plan.untold(d)
    assert not (d / "told.json").exists()


class TestSweptReading:
    FLEET = {"drives": {"wldn": {"label": "wldn", "machine": "chuck-herdr-alpha"}}, "hosts": {}}
    # Where the bolt's work runs, as the runner that took it reported (plan.land_held).
    AT = {"label": "wldn", "machine": "chuck-herdr-alpha", "stream": "wldn"}

    def sweep(self, monkeypatch, tmp_path, acts, key, result, live=None):
        import argparse
        import io
        d = tmp_path / "wldn" / key
        d.mkdir(parents=True)
        (d / "result.json").write_text(json.dumps(result))
        monkeypatch.setattr(plan, "CARDS", tmp_path)
        monkeypatch.setattr(plan, "land_held", lambda fleet, label, bolt: (None, plan.Rec("Bolt", [("Bolt", bolt)]), self.AT))
        monkeypatch.setattr(plan.sys, "stdin", io.StringIO(json.dumps({"live": live or [key], "blind": []})))
        plan.card_sweep(self.FLEET, argparse.Namespace(key=None, unit=None, label="wldn"), acts)
        return d

    def test_a_landings_reading_sent_is_told_to_main_level_ops_once_with_none_of_the_users_words(self, monkeypatch, tmp_path, capsys):
        """card-sessions "A landing's reading sent"."""
        acts = Acts()
        d = self.sweep(monkeypatch, tmp_path, acts, "land/y", {"decision": "annotated", "feedback": "this drops the retry"})
        assert acts.told == [("wldn-ops", "The user sent land/y's reading. Run crew card read land/y for what they sent.")]
        assert json.loads(capsys.readouterr().out) == [dict(key="land/y", unit=None, ended=False, sent=True,
                                                            said="the user sent its reading, and wldn-ops was told to run crew card read land/y")]
        assert json.loads((d / "told.json").read_text())["told"] == "wldn-ops"
        import argparse
        import io
        monkeypatch.setattr(plan.sys, "stdin", io.StringIO(json.dumps({"live": ["land/y"], "blind": []})))
        plan.card_sweep(self.FLEET, argparse.Namespace(key=None, unit=None, label="wldn"), acts)
        assert len(acts.told) == 1 and json.loads(capsys.readouterr().out) == []

    def test_a_tell_that_fails_leaves_the_reading_untold_for_the_next_refresh(self, monkeypatch, tmp_path, capsys):
        """card-sessions "The owner is down"; review-batches "Notes sent while the planner is down"."""
        acts = Acts()

        def down(name, text):
            print(f"could not tell {name} on chuck-herdr-alpha: it is not up", file=plan.sys.stderr)
            return False
        acts.tell = down
        d = self.sweep(monkeypatch, tmp_path, acts, "batch/3", {"decision": "annotated", "feedback": "1. x", "annotationCount": 1})
        assert json.loads(capsys.readouterr().out)[0]["said"] == (
            "the user sent its reading, and crew could not tell wldn-planner: could not tell wldn-planner on chuck-herdr-alpha: "
            "it is not up; the next refresh tells it")
        assert not (d / "told.json").exists() and acts.emitted == []

    def test_a_reading_closed_with_no_decision_tells_nobody(self, monkeypatch, tmp_path, capsys):
        """card-sessions "Closed with no decision"."""
        acts = Acts()
        self.sweep(monkeypatch, tmp_path, acts, "proposal/4", {"decision": "dismissed"})
        assert acts.told == [] and json.loads(capsys.readouterr().out) == []

    def test_a_reading_of_a_key_no_live_row_holds_tells_nobody(self, monkeypatch, tmp_path, capsys):
        acts = Acts()
        self.sweep(monkeypatch, tmp_path, acts, "land/y", {"decision": "approved"}, live=["land/z"])
        assert acts.told == []

    def test_a_batch_approved_with_no_words_is_recorded_read_and_its_card_closed_read_no_notes(self, monkeypatch, tmp_path, capsys):
        """review-batches "The session approved", and "Sent with no card on the main level's host"."""
        acts = Acts({"get_request": ({"status": "pending", "turn": "you", "version": 1}, None)},
                    [post("batch/3", "wldn-planner", "req_b3", On=["batch/3"])])
        self.sweep(monkeypatch, tmp_path, acts, "batch/3", {"decision": "approved", "annotationCount": 0})
        assert [(e["Act"], e.get("Outcome")) for e in acts.emitted] == [("card.close", "Read; no notes")]
        assert acts.told == []
        assert json.loads(capsys.readouterr().out)[0]["said"] == (
            "the user approved its reading with no notes, so crew recorded it read, Read; no notes: card batch/3: req_b3 withdrawn")
        acts = Acts()
        self.sweep(monkeypatch, tmp_path / "none", acts, "batch/3", {"decision": "approved", "annotationCount": 0})
        assert [(e["Act"], e.get("Outcome"), e.get("by")) for e in acts.emitted] == [("batch.close", "Read; no notes", "wldn-planner")]

    def test_a_batch_approved_with_no_words_whose_card_holds_a_note_is_told_to_the_planner(self, monkeypatch, tmp_path, capsys):
        tapped = {"status": "answered", "turn": "agent", "version": 2, "answer": {"note": {"text": "x1: name the host."}}}
        acts = Acts({"get_request": (tapped, None)}, [post("batch/3", "wldn-planner", "req_b3", On=["batch/3"])])
        self.sweep(monkeypatch, tmp_path, acts, "batch/3", {"decision": "approved", "annotationCount": 0})
        assert acts.emitted == [] and [n for n, _ in acts.told] == ["wldn-planner"]


# ------------------------------------------------------------------------- crew card read of a kit's landings card

def test_a_sent_landings_card_reads_the_ticked_bolts_in_its_order_and_the_submit_that_lands_them():
    """rail-cards "Landing approved": a and c ticked, b cleared."""
    heads = plan.card_heads("a@abc1234 b@abc1234 c@def5678")
    got = {"status": "answered", "turn": "agent", "answer": {"choiceIds": ["land:c", "land:a"], "note": {"text": "c first"}}}
    assert plan.landing_lines("swancloud", got, heads) == [
        "  to land, in the card's order: a and c", "  a: no land is posted for it yet: crew's next raise of the card posts it", "  c: no land is posted for it yet: crew's next raise of the card posts it"]
    assert "  note: c first" in cards.answer_lines("land/crew", "req_k1", got)


def test_a_sent_landings_card_reads_each_land_crew_posted_with_its_request_and_no_command():
    """rail-cards "The landings card's read prints the lands crew posted", "Two bolts sent": a and c ticked, b cleared,
    crew's raise posting a's land as request 57 and c's as 58 (crew-lands-each-bolt-through-flumes-base-place,
    Decision 10): each with its request, and no crew bolt submit or any command."""
    heads = plan.card_heads("a@abc1234 b@abc1234 c@def5678")
    got = {"status": "answered", "turn": "agent", "answer": {"choiceIds": ["land:c", "land:a"]}}
    entries = [dict(Act="bolt.submit", On=["bolt/a"], Card="req_k1", Head="abc1234", Request="57", Outcome="asked"),
               dict(Act="bolt.submit", On=["bolt/c"], Card="req_k1", Head="def5678", Request="58", Outcome="asked")]
    said = plan.landing_lines("swancloud", got, heads, posted={plan.row_name(p["work"]): p["request"] for p in plan.lands_posted(entries)})
    assert said == ["  to land, in the card's order: a and c", "  a: asked of the runner to land, request 57",
                    "  c: asked of the runner to land, request 58"]
    assert not [l for l in said if "crew " in l or "submit" in l]
    assert plan.row_name("fix/main/crew/red") == "main--red" and plan.row_name("bolt/a") == "a"


def test_a_land_posted_on_an_earlier_send_is_named_with_its_request():
    """rail-cards "The landings card's read prints the lands crew posted", from an earlier send: z, which an earlier
    send still lands, its land posted as request 41 on that card's send, comes first, named with its request."""
    heads = plan.card_heads("a@abc1234")
    got = {"status": "answered", "turn": "agent", "answer": {"approved": True}}
    entries = [dict(Act="bolt.submit", On=["bolt/z"], Card="req_k0", Head="0a1b2c3", Request="41", Outcome="asked")]
    said = plan.landing_lines("swancloud", got, heads, ["z"], posted={plan.row_name(p["work"]): p["request"] for p in plan.lands_posted(entries)})
    assert said == ["  to land on the user's send of an earlier card: z", "  to land, in the card's order: a",
                    "  z: asked of the runner to land, request 41",
                    "  a: no land is posted for it yet: crew's next raise of the card posts it"]


def test_a_lone_row_approved_lands_it_and_a_send_ticking_none_lands_nothing():
    one = plan.card_heads("y@abc1234")
    approved = {"status": "answered", "turn": "agent", "answer": {"approved": True}}
    assert plan.landing_lines("wldn", approved, one)[-1] == "  y: no land is posted for it yet: crew's next raise of the card posts it"
    none = {"status": "answered", "turn": "agent", "answer": {"choiceIds": []}}
    assert plan.landing_lines("wldn", none, one) == ["  no bolt ticked: nothing lands"]
    assert plan.landing_lines("wldn", {"status": "pending", "turn": "you"}, one) == []


def test_a_bolt_ticked_that_the_record_holds_taking_main_first_is_left_out_of_the_submit_its_send_standing():
    """rail-cards "Ticked after being left": z takes main first, y lands."""
    heads = plan.card_heads("y@abc1234 z@abc1234")
    got = {"status": "answered", "turn": "agent", "answer": {"choiceIds": ["land:y", "land:z"]}}
    assert plan.landing_lines("swancloud", got, heads, main_first={"z"}) == [
        "  to land, in the card's order: y",
        "  z takes main first until a fix taking main in moves its head, and the user's send stands for it",
        "  y: no land is posted for it yet: crew's next raise of the card posts it"]
    assert plan.landing_lines("swancloud", got, heads, main_first={"y", "z"})[-1] == (
        "  z takes main first until a fix taking main in moves its head, and the user's send stands for it")


def test_a_ticked_bolt_that_landed_or_left_the_plan_is_said_and_left_out_of_the_submit():
    """rail-cards "The landings card's read prints the lands crew posted", read again after part of the send landed:
    z landed on the send and w left the plan, so the read names y's land alone."""
    heads = plan.card_heads("y@abc1234 z@abc1234 w@abc1234")
    got = {"status": "answered", "turn": "agent", "answer": {"choiceIds": ["land:y", "land:z", "land:w"]}}
    assert plan.landing_lines("swancloud", got, heads, gone={"z": "landed", "w": "left the plan"}) == [
        "  to land, in the card's order: y",
        "  z landed since the card was posted, so it is no bolt to land",
        "  w left the plan since the card was posted, so it is no bolt to land",
        "  y: no land is posted for it yet: crew's next raise of the card posts it"]
    assert plan.landing_lines("swancloud", got, heads, gone={"y": "landed", "z": "landed", "w": "landed"})[-1] == (
        "  w landed since the card was posted, so it is no bolt to land")


class TestTickedGone:
    """What the read of a sent landings card leaves out of the submit: each ticked bolt the run record holds landed since
    the card's first entry, by sluice's landing or crew's close, or that the plan no longer holds (plan.landed_since,
    plan.ticked_gone)."""
    POSTED = post("land/crew", "swancloud-ops", "req_k1", at="2026-10-31T10:00:00Z", Heads="y@abc1234 z@abc1234")

    def test_a_bolt_sluice_landed_or_crew_closed_since_the_post_is_landed(self):
        entries = [self.POSTED,
                   dict(Act="bolt.submit", On=["bolt/z"], Outcome="landed", At="2026-10-31T10:05:00Z"),
                   dict(Act="bolt.land", On=["bolt/w"], At="2026-10-31T10:06:00Z")]
        assert plan.landed_since(entries, "req_k1") == {"z", "w"}

    def test_a_landing_before_the_post_a_refused_one_and_a_queued_one_are_not(self):
        entries = [dict(Act="bolt.land", On=["bolt/z"], At="2026-10-30T09:00:00Z"), self.POSTED,
                   dict(Act="bolt.submit", On=["bolt/y"], Refused="a conflict on README.md", At="2026-10-31T10:05:00Z"),
                   dict(Act="bolt.submit", On=["bolt/y"], Outcome="queued", At="2026-10-31T10:04:00Z"),
                   dict(Act="bolt.land", On=["bolt/w"], Refused="w has not landed", At="2026-10-31T10:06:00Z")]
        assert plan.landed_since(entries, "req_k1") == set()

    def test_a_card_the_record_holds_no_entry_of_has_nothing_landed_since(self):
        assert plan.landed_since([dict(Act="bolt.land", On=["bolt/z"], At="2026-10-31T10:06:00Z")], "req_k1") == set()

    def test_landed_and_gone_from_the_plan_are_told_apart(self):
        assert plan.ticked_gone(["y", "z", "w"], {"y", "z"}, {"z"}) == {"z": "landed", "w": "left the plan"}
        assert plan.ticked_gone(None, {"y"}, set()) == {} and plan.ticked_gone(["y"], {"y"}, set()) == {}


class ReadSent:
    """crew card read land/crew as swancloud-ops on the drive's main machine, holding req_k1 under it, with the
    user's send (got) read from Pending You; the kit's card raised in its stead, the raise adding what it records (told)
    to this host's run record."""
    FLEET = {"drives": {"swancloud": {"label": "swancloud", "machine": "mac-studio"}}}

    PLAN = "%rec: Bolt\n\nBolt: y\nRepo: crew\n\nBolt: z\nRepo: crew\n\n%rec: Unit\n\n"

    def __init__(self, monkeypatch, got, told=(), branch=(), held=PLAN, now=None):
        import argparse
        self.entries = [post("land/crew", "swancloud-ops", "req_k1", Heads="y@abc1234 z@abc1234")]
        self.raised, self.calls, self.worked, self.emitted = [], [], [], []
        acts = self

        class Bridge(Py):
            def __init__(self, name, later, held=None):
                Py.__init__(self, acts, {"get_request": (got, None)})

        def raised(fleet, label, kit, note=None, pane=None):
            print("card land/crew: req_k1 is left as it is, the user having answered it")
            self.raised.append(kit)
            self.entries += list(told)
        def emit(label, act, on, **fields):  # this host's run record, the read's own acts among it
            self.emitted.append(dict(fields, Act=act, On=on))
            self.entries.append(dict(fields, Act=act, On=on, By=fields.get("by")))
        monkeypatch.setattr(cards, "Bridge", Bridge)
        monkeypatch.setattr(plan.record, "emit", emit)
        monkeypatch.setattr(cards, "host_entries", lambda record, label, host: list(self.entries))
        monkeypatch.setattr(plan, "card_asker", lambda fleet, a: ("swancloud", "swancloud-ops"))
        monkeypatch.setattr(crew, "this_host", lambda: "mac-studio")
        monkeypatch.setattr(plan, "land_hand", raised)
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: list(branch))
        monkeypatch.setattr(plan, "plan_of", lambda fleet, label: held and plan.Plan(held))

        def work(fleet, label, kit, moves):  # each bolt's head now where it lives, at the head the card showed unless now
            self.worked.append(moves)
            return {b: dict(head=(now or {}).get(b, sent), gained=[], lost=[], why=None) for b, (sent, _) in moves.items()}
        monkeypatch.setattr(plan, "bolt_work", work)
        self.run = lambda json=False: plan.card_read(self.FLEET, argparse.Namespace(key="land/crew", label=None, json=json, sub="read"))


TICKED = {"status": "answered", "turn": "agent", "version": 3, "answer": {"choiceIds": ["land:y", "land:z"]}}
Z_HELD = dict(Act="forecast", On=["bolt/z"], Heads="bolt/z@abc1234 main@e4f5a6b", Paths="README.md", Reached="held")


def test_reading_a_sent_landings_card_raises_it_first_and_leaves_a_bolt_taking_main_first_out_of_the_submit(monkeypatch, capsys):
    """rail-cards "A row taking main first is offered to land again once proven with no conflict": the raise records z held, on this host, and
    the read gives y alone to land."""
    read = ReadSent(monkeypatch, TICKED, told=[Z_HELD])
    read.run()
    out, err = capsys.readouterr()
    assert read.raised == ["crew"] and "is left as it is" in err and "is left as it is" not in out
    assert out.splitlines()[-3:] == [
        "  to land, in the card's order: y",
        "  z takes main first until a fix taking main in moves its head, and the user's send stands for it",
        "  y: no land is posted for it yet: crew's next raise of the card posts it"]


def test_a_ticked_bolt_whose_take_main_fix_moved_it_since_its_conflict_lands_on_the_send(monkeypatch, capsys):
    """rail-cards "A ticked bolt taking main in lands on its send once it reads proven at a new head": z's conflict is recorded at the head the card
    showed, abc1234, and its take-main fix has moved it to def5678, with no conflict recorded there."""
    read = ReadSent(monkeypatch, TICKED, told=[Z_HELD], now={"z": "def5678" + "0" * 33})
    read.run()
    assert read.worked == [{"z": ("abc1234", None)}]
    assert capsys.readouterr().out.splitlines()[-3:] == [
        "  to land, in the card's order: y and z", "  y: no land is posted for it yet: crew's next raise of the card posts it",
        "  z: no land is posted for it yet: crew's next raise of the card posts it"]
    again = ReadSent(monkeypatch, TICKED, told=[Z_HELD, dict(Z_HELD, Heads="bolt/z@def5678 main@9999999")],
                     now={"z": "def5678" + "0" * 33})
    again.run()
    assert capsys.readouterr().out.splitlines()[-1] == "  y: no land is posted for it yet: crew's next raise of the card posts it"


def test_a_conflict_a_wait_recorded_on_the_branch_leaves_the_bolt_out_too(monkeypatch, capsys):
    read = ReadSent(monkeypatch, TICKED, branch=[dict(Z_HELD, Reached="wait", Id="e-1")])
    read.run()
    assert capsys.readouterr().out.splitlines()[-1] == "  y: no land is posted for it yet: crew's next raise of the card posts it"


def test_a_ticked_bolt_with_no_conflict_lands_as_any_and_the_json_answer_is_left_clean(monkeypatch, capsys):
    """rail-cards "Ticked and clean"."""
    read = ReadSent(monkeypatch, TICKED)
    read.run()
    assert capsys.readouterr().out.splitlines()[-1] == "  z: no land is posted for it yet: crew's next raise of the card posts it"
    read.run(json=True)
    out, err = capsys.readouterr()
    assert json.loads(out) == TICKED and "is left as it is" in err


def test_a_send_read_again_after_part_of_it_landed_gives_the_rest_alone_to_land(monkeypatch, capsys):
    """rail-cards "The landings card's read prints the lands crew posted", read again after part of the send landed: y
    landed, closed and gone from the plan, the answered card still open; the read names z alone to land, crew's next
    raise posting its land, and y as landed, naming no land of a bolt that landed."""
    landed = [dict(Act="bolt.submit", On=["bolt/y"], Outcome="landed", At="2026-10-12T10:05:00Z", Id="e-2"),
              dict(Act="bolt.land", On=["bolt/y"], At="2026-10-12T10:05:30Z", Id="e-3")]
    read = ReadSent(monkeypatch, TICKED, branch=landed, held="%rec: Bolt\n\nBolt: z\nRepo: crew\n\n%rec: Unit\n\n")
    read.run()
    assert capsys.readouterr().out.splitlines()[-3:] == [
        "  to land, in the card's order: z",
        "  y landed since the card was posted, so it is no bolt to land",
        "  z: no land is posted for it yet: crew's next raise of the card posts it"]


def test_a_bolt_sluice_landed_that_is_not_closed_yet_is_no_bolt_to_land_either(monkeypatch, capsys):
    read = ReadSent(monkeypatch, TICKED, told=[dict(Act="bolt.submit", On=["bolt/y"], Outcome="landed", At="2026-10-12T10:05:00Z")])
    read.run()
    assert capsys.readouterr().out.splitlines()[-1] == "  z: no land is posted for it yet: crew's next raise of the card posts it"


def test_a_plan_that_cant_be_read_refuses_the_read_of_what_the_send_lands(monkeypatch, capsys):
    read = ReadSent(monkeypatch, TICKED, held=None)
    with pytest.raises(crew.Refusal, match="swancloud/main could not be read, so which bolts land/crew's send still lands can't be told"):
        read.run()


def test_a_card_still_waiting_on_the_user_is_not_raised(monkeypatch, capsys):
    read = ReadSent(monkeypatch, {"status": "pending", "turn": "you", "version": 2})
    read.run()
    assert read.raised == [] and read.emitted == []


def test_reading_a_sent_landings_card_records_the_users_answer_once_before_its_raise(monkeypatch, capsys):
    """rail-cards "crew records the user's answer the first time it reads it": crew card read is one of the three acts."""
    read = ReadSent(monkeypatch, TICKED)
    read.run()
    assert [(e["Act"], e["On"], e["by"], e["Card"], e["Answer"], e["Heads"]) for e in read.emitted] == [
        ("card.answer", ["kit/crew"], "swancloud-ops", "req_k1", "ticked y and z", "y@abc1234 z@abc1234")]
    read.run()
    assert len(read.emitted) == 1


def test_reading_an_answered_proposal_card_records_its_answer(monkeypatch, tmp_path, capsys):
    entries = [post("proposal/57", "wldn-planner", "req_57")]
    got = {"status": "answered", "turn": "agent", "version": 3, "answer": {"approved": True}}
    acts = Acts(entries=entries, caller="wldn-planner")

    class Bridge(Py):
        def __init__(self, name, later, held=None):
            Py.__init__(self, acts, {"get_request": (got, None)})
    monkeypatch.setattr(cards, "Bridge", Bridge)
    monkeypatch.setattr(cards, "host_entries", lambda record, label, host: list(entries))
    monkeypatch.setattr(plan, "card_asker", lambda fleet, a: ("wldn", "wldn-planner"))
    monkeypatch.setattr(crew, "this_host", lambda: "chuck-herdr-alpha")
    monkeypatch.setattr(plan, "CARDS", tmp_path)
    plan.card_read({}, argparse.Namespace(key="proposal/57", label=None, json=False, sub="read"), acts)
    assert [(e["Act"], e["On"], e["Card"], e["Key"], e["Answer"]) for e in acts.emitted] == [
        ("card.answer", ["proposal/57"], "req_57", "proposal/57", "approved")]
    assert capsys.readouterr().out.splitlines()[0] == "card proposal/57: req_57, answered, your turn: the user has answered"


# ------------------------------------------------------------ crew card preview, on the user's words (record 0043)
# rail-cards "The user asks for a preview by writing on the card", "crew card preview asks the runner by one request, running nothing
# of sluice's" and "A preview is put away on the user's done and when its row leaves the landings card": the
# owner's command on the main machine writes one request for the runner on the host where the thing's work runs, and
# runs nothing there (Decision 6 of a-cards-preview-is-asked-of-the-runner).

import argparse  # noqa: E402
import io  # noqa: E402

from facts import FactsWrite, reviewed  # noqa: E402
import runner  # noqa: E402

PKIT = {"name": "crew", "repo": "agentplot/crew", "main": "/crew/main", "dir": "/crew"}
PFLEET = {"drives": {"swancloud": {"label": "swancloud", "machine": "deneb"}}, "hosts": {}}
# Where crew's started bolts run, as the runner that took their work reported (plan.land_held, plan.batch_unit_at).
PAT = {"label": "swancloud", "machine": "deneb", "stream": "swancloud", "kit": PKIT}
PHEAD = "abc1234" + "0" * 33
CARD = [post("land/crew", "swancloud-ops", "req_k1", Heads="y@abc1234 z@def5678 x@1234567")]
DEMO = '{"name": "demo", "kind": "preview", "branch": "unit/a", "revision": "abc1234"}'
ROW = {"bolt": "y", "box": True, "why": None, "facts": {"head": PHEAD, "kit": "crew"}}
UP = {"name": "crew-y", "branch": "bolt/y", "revision": PHEAD, "state": "up", "addresses": {"web": "http://deneb:4310"}}
LAUNCHED = plan.Rec("Request", runner.request_fields(1, "launch", "unit/a", dict(
    Repo="crew", Kind="change", Name="a", Base="bolt/x", Priority=1, Intent="swancloud/x", Recipient="swancloud/planner",
    Brief="Build a."), "2026-11-08T11:00:00Z", "swancloud-dispatch"))


def preview_rec(n, work="bolt/y", revision=PHEAD, done=False, branch=None):
    """A preview request as crew card preview writes it."""
    return plan.Rec("Request", runner.request_fields(n, "preview", work, runner.preview_fields(
        "deneb", "crew", branch or ("bolt/y" if work == "bolt/y" else "unit/a"), revision, done), "2026-11-08T12:00:00Z", "swancloud-ops"))


def deneb_read(previews="", answers=""):
    """deneb's runner as crew reads it, with these answers and previews."""
    files = {"runner.rec": plan.Plan(runner.RUNNER + "\nHost: deneb\nVersion: 0.6.0\nSince: 2026-11-08T11:00:00Z\n"),
             "answers.rec": plan.Plan(runner.ANSWERS + answers), "previews.rec": plan.Plan(runner.PREVIEWS + previews)}
    return {"deneb": runner.host_read("swancloud", "deneb", "5e1f0c2a" + "0" * 32, files, {})}


def done_up(n):
    return f"\nRequest: {n}\nOutcome: done\nText: {json.dumps(UP)}\nStatus: {json.dumps(UP)}\nListed: yes\nAt: 2026-11-08T12:03:00Z\n"


class PreviewActs:
    """What crew card preview reaches on the main machine: who asks, this host, its run record, the kits, the
    drive's requests and runners, a landings row read as the raise reads it, and a unit's made lines; and where it
    hands the command on, to the main machine (forward), each recorded."""

    def __init__(self, caller="swancloud-ops", host="deneb", entries=CARD, requests=(), runners=None, row=ROW, lines=None):
        self.who, self.here, self.held, self.forwarded = caller, host, list(entries), []
        self.requests, self.runners, self.row, self.lines, self.rows, self.made_on = list(requests), runners or deneb_read(), row, lines, [], []

    def caller(self):
        return self.who

    def host(self):
        return self.here

    def entries(self, label):
        return self.held

    def kits(self, label):
        return ("crew",)

    def forward(self, host, args):
        self.forwarded.append((host, args))

    def runner(self, label):
        return list(self.requests), dict(self.runners)

    def land_row(self, label, bolt, host):
        self.rows.append((bolt, host))
        return (self.row, None) if self.row else (None, "deneb did not answer")

    def made(self, label, host, units):
        self.made_on.append((host, list(units)))
        return {"made": {u: self.lines or [] for u in units}}


def asked(key, thing, done=False):
    return argparse.Namespace(key=key, thing=thing, done=done, label="swancloud")


class TestCardPreview:
    @pytest.fixture(autouse=True)
    def held(self, monkeypatch):
        """The plan's bolts and where their work runs; each plan write applied to requests.rec as the acts hold it, at a
        tip holding them; and each card change's note kept. crew holds no call of sluice's to reach
        (test_no_tool_for_a_bolt.py)."""
        monkeypatch.setenv("CREW_AGENT", "swancloud-ops")
        monkeypatch.setattr(plan, "land_held", lambda fleet, label, bolt: (None, plan.Rec("Bolt", [("Bolt", bolt), ("Repo", "crew")]), PAT))
        monkeypatch.setattr(plan, "batch_unit_at", lambda fleet, label, bolt, unit: PAT)
        self.writes, self.notes = [], []
        monkeypatch.setattr(plan, "preview_changed", lambda fleet, label, key, note: self.notes.append((key, note)))
        monkeypatch.setattr(plan, "write", self.write)

    def write(self, fleet, label, change, subject, act=None, on=(), fields=None, **more):
        acts = self.acts
        text = runner.REQUESTS + "".join("\n" + "\n".join(r.lines()) + "\n" for r in acts.requests)
        w = FactsWrite("%rec: Bolt\n%key: Bolt\n", files={"requests.rec": text}, runners=acts.runners, label=label)
        change(w)
        new = plan.Plan(w.files["requests.rec"]).recs("Request")[len(acts.requests):]
        acts.requests += new
        self.writes.append(dict(subject=subject, act=act, on=list(on), fields=fields, requests=[dict(r.fields) for r in new]))

    def run(self, acts, *args, **kw):
        self.acts = acts
        return plan.card_preview(PFLEET, asked(*args, **kw), acts)

    def test_ops_ask_writes_one_preview_naming_its_host_work_kit_branch_and_head(self, capsys):
        """rail-cards "Asked", drive-state "A preview of a landings row's bolt": the row read afresh, as the raise
        reads it, on the host whose runner took its work; sluice never run."""
        acts = PreviewActs()
        self.run(acts, "land/crew", "y")
        assert acts.rows == [("y", "deneb")]
        assert [(w["subject"], w["act"], w["on"], w["fields"]) for w in self.writes] == [
            ("plan(card): preview of y asked from land/crew", "card.preview", ["bolt/y"], {"Key": "land/crew", "State": "asked"})]
        assert self.writes[0]["requests"] == [{"Request": "1", "Act": "preview", "Host": "deneb", "Work": "bolt/y", "Repo": "crew",
                                               "Branch": "bolt/y", "Revision": PHEAD, "Date": self.writes[0]["requests"][0]["Date"],
                                               "By": "swancloud-ops"}]
        assert self.notes == [("land/crew", "y: Its preview of abc1234 is asked of the runner on deneb")]
        assert capsys.readouterr().out == "request 1: y: Its preview of abc1234 is asked of the runner on deneb\n"

    def test_asked_twice_while_the_runner_reports_it_up_writes_nothing(self, capsys):
        """rail-cards "Asked twice"."""
        acts = PreviewActs(requests=[preview_rec(1)], runners=deneb_read(previews=done_up(1)))
        self.run(acts, "land/crew", "y")
        assert self.writes == [] and self.notes == []
        assert capsys.readouterr().out == ("crew's ask of y's preview of abc1234 stands, as request 1, so none is written: "
                                           "y: Its preview of abc1234 is up: web http://deneb:4310\n")

    def test_asked_again_after_a_refusal_writes_a_second(self):
        """rail-cards "Asked again after a refusal"."""
        words = "its Act preview, which crew's implementation does not read"
        acts = PreviewActs(requests=[preview_rec(1)], runners=deneb_read(answers=f"\nRequest: 1\nOutcome: refused\nWords: {words}\nAt: 2026-11-08T12:01:00Z\n"))
        self.run(acts, "land/crew", "y")
        assert [r["Request"] for w in self.writes for r in w["requests"]] == ["2"]
        assert self.notes[-1] == ("land/crew", "y: Its preview of abc1234 is asked of the runner on deneb")

    def test_done_writes_the_done_and_with_none_standing_writes_nothing(self, capsys):
        """rail-cards "The user is done" and "Done with none asked": no row read for it."""
        acts = PreviewActs(requests=[preview_rec(1)], runners=deneb_read(previews=done_up(1)), row=None)
        self.run(acts, "land/crew", "y", done=True)
        assert [(w["subject"], w["fields"]) for w in self.writes] == [
            ("plan(card): preview of y put away from land/crew", {"Key": "land/crew", "State": "done"})]
        assert [(r["Request"], r["Host"], r["Work"], r["Repo"], r["Branch"], r["Revision"], r["Done"]) for r in self.writes[0]["requests"]] == [
            ("2", "deneb", "bolt/y", "crew", "bolt/y", PHEAD, "yes")]
        assert self.notes == [("land/crew", "y: Its preview of abc1234 is put away")] and acts.rows == []
        capsys.readouterr()
        self.run(acts, "land/crew", "y", done=True)
        assert len(self.writes) == 1 and len(self.notes) == 1
        assert capsys.readouterr().out == "crew asked for no preview of y that stands, from land/crew or another card, so nothing is put away\n"

    def test_a_batch_lines_ask_names_its_unit_and_the_lines_branch_and_revision(self):
        acts = PreviewActs(caller="swancloud-planner", entries=[reviewed(7, [("a", "x", "aaa1")])], requests=[LAUNCHED],
                           lines=[["code", [DEMO]]])
        self.run(acts, "batch/7", "a/demo")
        assert acts.made_on == [("deneb", ["a"])]
        assert [(r["Work"], r["Host"], r["Repo"], r["Branch"], r["Revision"]) for r in self.writes[0]["requests"]] == [
            ("unit/a", "deneb", "crew", "unit/a", "abc1234")]
        assert self.notes == [("batch/7", "a/demo: Its preview of abc1234 is asked of the runner on deneb")]
        with pytest.raises(plan.Refusal, match="batch/7 carries no a/spike to bring up: it carries a/demo"):
            self.run(acts, "batch/7", "a/spike")
        with pytest.raises(plan.Refusal, match="batch/7 carries no b to bring up: it carries a"):
            self.run(acts, "batch/7", "b/demo")
        with pytest.raises(plan.Refusal, match="a batch's line is named <unit>/<name>"):
            self.run(acts, "batch/7", "a")
        with pytest.raises(plan.Refusal, match="holds no batch 8"):
            self.run(acts, "batch/8", "a/demo")
        assert len(self.writes) == 1

    def test_a_thing_the_card_does_not_carry_is_refused_writing_nothing(self):
        """rail-cards "A thing the card does not carry"."""
        with pytest.raises(plan.Refusal, match="land/crew carries no w to bring up: it carries x, y and z$"):
            self.run(PreviewActs(), "land/crew", "w")
        with pytest.raises(plan.Refusal, match="land/crew carries no y to bring up: it carries nothing that must run"):
            self.run(PreviewActs(entries=()), "land/crew", "y")
        with pytest.raises(plan.Refusal, match="land/crew's row y can't land now, so its preview is not asked: held for a fix"):
            self.run(PreviewActs(row={"bolt": "y", "why": "held for a fix: gap (fix/y/gap)"}), "land/crew", "y")
        with pytest.raises(plan.Refusal, match="proposal/3 carries nothing crew brings up"):
            self.run(PreviewActs(), "proposal/3", "y")
        assert self.writes == [] and self.notes == []

    def test_anyone_but_the_owner_is_refused_writing_nothing(self):
        """rail-cards "Asked by anyone but the owner"."""
        with pytest.raises(plan.Refusal, match="land/crew is swancloud-ops's card: swancloud-ops brings up what it carries"):
            self.run(PreviewActs(caller="swancloud-design"), "land/crew", "y")
        with pytest.raises(plan.Refusal, match="batch/7 is swancloud-planner's card"):
            self.run(PreviewActs(caller="swancloud-ops"), "batch/7", "a/demo")
        assert self.writes == [] and self.notes == []

    def test_off_the_main_machine_it_runs_there(self):
        acts = PreviewActs(host="mac-studio")
        self.run(acts, "land/crew", "y", done=True)
        assert acts.forwarded == [("deneb", ["card", "preview", "land/crew", "y", "--done", "--label", "swancloud"])]
        assert self.writes == [] and acts.rows == []

    def test_card_preview_is_a_command_that_writes_a_request_for_ops_and_the_planner(self):
        """roles.1: the role table names every command that writes a request."""
        assert plan.REQUESTERS["card preview"] == ("main-ops", "planner")
        assert plan.ACTS[("card", "preview")] == "card.preview"


# --------------------------------------------------------------------- a card's change, as Pending You's notice names it
# plan.card_ask, what crew _answered makes of a change on a card that `pendingyou watch` hands it (design Decision 5 of
# roles-run-as-flume-kinds): an ask of the role whose run the card's asker is, keyed by the card's request and version,
# reading nothing else of the card; and board.answers_watched, whether the host's follower runs that notice at all.
import board  # noqa: E402

STANDS = {r: "standing" for r in crew.KIND_ROLES}
KFLEET = {"drives": {"madswan": {"label": "madswan", "machine": "deneb", "runs": dict(STANDS, planner="on-demand", ops="on-demand")},
                         "wldn": {"label": "wldn", "machine": "chuck-herdr-alpha", "runs": STANDS}}}


def test_a_change_on_a_runs_card_asks_its_role_by_the_cards_request_and_version():
    """role-runs "A card's answer, an opening and a batch are asks": a deploy approved from the phone."""
    assert plan.card_ask(KFLEET, "madswan-ops", "req_eafa10ee554b41edbce6", "3", "answer_ready") == dict(
        label="madswan", role="ops", names="card/req_eafa10ee554b41edbce6", key="card/req_eafa10ee554b41edbce6/3",
        words="the user answered it")


def test_a_later_change_on_the_card_is_keyed_apart_and_says_what_came():
    first = plan.card_ask(KFLEET, "madswan-planner", "req_1", "3", "answer_ready")
    later = plan.card_ask(KFLEET, "madswan-planner", "req_1", "4", "message_ready")
    assert (first["key"], later["key"]) == ("card/req_1/3", "card/req_1/4")
    assert later["words"] == "a message came on it"
    assert plan.card_ask(KFLEET, "madswan-planner", "req_1", "5", "")["words"] == "Pending You's notice named it with no event"


@pytest.mark.parametrize("name", ["wldn-planner", "madswan-design", "crw-1-conductor", "chuck@deneb", "madswan", "", None])
def test_a_card_in_any_other_name_asks_nothing(name):
    """role-runs "A standing agent's card": a standing role's, a team's agent's and the user's own stay the wake mod's."""
    assert plan.card_ask(KFLEET, name, "req_1", "3", "answer_ready") is None


@pytest.mark.parametrize("card, version", [("", "3"), ("req_a b", "3"), ("card/x", "3"), ("req_1", ""), ("req_1", "v3"), ("req_1", None)])
def test_a_notice_crew_cannot_read_is_refused(card, version):
    with pytest.raises(crew.Refusal):
        plan.card_ask(KFLEET, "madswan-planner", card, version, "answer_ready")


def test_the_follower_hears_the_notice_only_where_a_role_whose_main_level_is_here_runs_as_its_kind():
    """role-runs "The follower hears Pending You's notice while a role here runs as its kind"."""
    assert board.answers_watched(KFLEET, "deneb")
    assert not board.answers_watched(KFLEET, "chuck-herdr-alpha")
    assert not board.answers_watched(KFLEET, "mac-studio")
    assert not board.answers_watched({"drives": {"madswan": dict(KFLEET["drives"]["madswan"], runs=STANDS)}}, "deneb")


def test_the_notice_runs_crew_answered_through_pending_yous_watch():
    argv = board.notice_argv()
    assert argv[:3] == ["pendingyou", "watch", "--"] and argv[-2:] == [str(crew.HOME / "plugin/bin/crew"), "_answered"]
