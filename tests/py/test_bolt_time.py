"""A started bolt's age and who held its time (plan.20, record 0044; crew-board "Each minute of a bolt's life goes to
one holder" and "A held bolt's head line shows its age and who held its time"): the split, plan.bolt_time, a decision
of facts alone, each case a scenario of the crew-board delta; what it is split from, plan.bolt_facts, read from the run
record alone, from its entry that made the bolt's branch (Decision 11 of the-team-machinery-leaves); and a landing's
Age and Split, plan.landing_spent, from the same (crew-lands-each-bolt-through-flumes-base-place, Decision 7)."""
import datetime

from facts import START, at, plan_text

import plan

STARTED = datetime.datetime(2026, 10, 27, 11, 0, tzinfo=datetime.timezone.utc)


def t(minutes):
    """A time, minutes after the bolt's start."""
    return STARTED + datetime.timedelta(minutes=minutes)


def split(end, stages=(), submissions=(), cards=(), holds=()):
    return plan.bolt_time(STARTED, t(end), list(stages), list(submissions), list(cards), list(holds))


def shares(**minutes):
    return dict(dict.fromkeys(plan.HOLDERS, 0), **minutes)


# ------------------------------------------------------------------------------------------------ one holder a minute

def test_a_team_at_work():
    """Started three hours ago, a code stage ran two hours, a batch card holding its unit was open forty minutes with
    nothing running, and nothing held it twenty minutes."""
    got = split(180, stages=[{"start": t(0), "end": t(120), "merge": False, "what": "code on a"}],
                cards=[{"at": t(120), "until": t(160), "key": "batch/12"}])
    assert got["age"] == 180 and got["shares"] == shares(team=120, user=40, nobody=20)
    assert got["now"] == {"holder": "nobody", "what": None, "since": t(160)}


def test_a_merge_under_test():
    """a's merge #41 stood queued five minutes and under test twelve, while a's merge stage ran throughout."""
    merge = {"start": t(0), "end": None, "merge": True, "what": "merge on a"}
    queued = {"submitted": t(0), "started": None, "decided": None, "state": "queued", "what": "#41"}
    assert split(5, stages=[merge], submissions=[queued])["now"]["holder"] == "team"
    testing = dict(queued, started=t(5), state="testing")
    got = split(17, stages=[merge], submissions=[testing])
    assert got["shares"] == shares(team=5, kit=12)
    assert got["now"] == {"holder": "kit", "what": "#41", "since": t(5)}


def test_a_stage_beside_a_merge_under_test_is_the_teams():
    """c's code stage runs while a's merge #41 is under test."""
    got = split(30, stages=[{"start": t(10), "end": None, "merge": False, "what": "code on c"}],
                submissions=[{"submitted": t(0), "started": t(0), "decided": None, "state": "testing", "what": "#41"}])
    assert got["shares"] == shares(kit=10, team=20)
    assert got["now"] == {"holder": "team", "what": "code on c", "since": t(10)}


MERGE = {"start": t(0), "end": t(25), "merge": True, "what": "merge on a", "work": "unit/a"}


def test_a_decided_merge_with_its_checks_start():
    """#41, landed, was submitted at 14:00, its checks began at 14:05 as the follower saw while it stood, and it was
    decided at 14:17: 14:00 to 14:05 the team's, 14:05 to 14:17 the kit's, and no minute of it team-or-kit."""
    got = split(30, stages=[dict(MERGE, end=t(20))],
                submissions=[{"submitted": t(0), "started": t(5), "decided": t(17), "state": "landed", "what": "#41", "worktree": "unit/a"}])
    assert got["shares"] == shares(team=8, kit=12, nobody=10)


def test_a_decided_merge_whose_checks_start_is_not_kept_is_team_or_kit_though_its_merge_stage_ran():
    """#41, landed, submitted at 14:00 and decided at 14:17, its checks' start kept nowhere: 14:00 to 14:17 are
    team-or-kit, though a's merge stage ran throughout, and none of them the team's or the kit's."""
    got = split(30, stages=[MERGE], submissions=[{"submitted": t(3), "started": None, "decided": t(20), "state": "landed", "what": "#41",
                                                  "worktree": "unit/a"}])
    assert got["shares"] == shares(team=8, team_or_kit=17, nobody=5)


def test_a_merge_that_ended_before_the_follower_saw_it_is_team_or_kit_for_its_whole_run():
    """The follower started after a's merge stage of 13:50 to 14:20 and its submission were over: 13:50 to 14:20 are
    team-or-kit; a decision alone, the merge's own seen in the recent events, places no minute."""
    alone = {"submitted": None, "started": None, "decided": t(28), "state": None, "what": "#41", "worktree": "unit/a"}
    got = split(40, stages=[dict(MERGE, end=t(30))], submissions=[alone])
    assert got["shares"] == shares(team_or_kit=30, nobody=10)
    other = {"submitted": t(10), "started": t(12), "decided": t(15), "state": "landed", "what": "#40", "worktree": "unit/c"}
    assert split(40, stages=[dict(MERGE, end=t(30))], submissions=[other])["shares"] == shares(team_or_kit=27, kit=3, nobody=10), \
        "another unit's submission was taken for the merge's own"


def test_a_merge_stage_running_with_no_submission_held_is_the_teams():
    got = split(12, stages=[dict(MERGE, end=None)])
    assert got["shares"] == shares(team=12) and got["now"] == {"holder": "team", "what": "merge on a", "since": t(0)}


def test_a_standing_submission_testing_with_no_start_of_checks_is_team_or_kit_from_its_submit():
    got = split(20, submissions=[{"submitted": t(5), "started": None, "decided": None, "state": "testing", "what": "#9"}])
    assert got["shares"] == shares(nobody=5, team_or_kit=15) and got["now"] == {"holder": "team_or_kit", "what": "#9", "since": t(5)}


def test_minutes_that_cant_be_split_are_said_as_team_or_kit_with_why_once():
    """crew-board "Minutes that can't be split": twelve minutes of b's age were a decided merge's stay in sluice whose
    checks' start crew does not hold."""
    now = t(30)
    got = split(30, stages=[{"start": t(0), "end": t(10), "merge": False, "what": "code on a"}],
                submissions=[{"submitted": t(12), "started": None, "decided": t(24), "state": "landed", "what": "#41", "worktree": "unit/a"},
                             {"submitted": t(25), "started": None, "decided": None, "state": "testing", "what": "#42", "worktree": "unit/c"}])
    assert got["shares"] == shares(team=10, team_or_kit=17, nobody=3)
    since = f"{t(25).astimezone():%H:%M}"
    assert plan.time_said(got, now) == f"30m: team 10m, team or kit 17m, nobody 3m; team or kit since {since}, #42; team or kit: sluice keeps no start of its checks"
    assert plan.time_said(split(30, stages=[{"start": t(0), "end": t(10), "merge": False, "what": "code on a"}]), now).count("team or kit") == 0


def test_a_card_counts_only_while_nothing_moves_and_a_hold_only_while_no_one_else_holds():
    got = split(60, stages=[{"start": t(0), "end": t(20), "merge": False}],
                cards=[{"at": t(10), "until": t(40), "key": "land/crew"}],
                holds=[{"at": t(30), "until": None, "what": "its host deneb is held by chuck"}])
    assert got["shares"] == shares(team=20, user=20, hold=20)
    assert got["now"] == {"holder": "hold", "what": "its host deneb is held by chuck", "since": t(40)}


# ------------------------------------------------------------------------------------------------------------- nobody

def test_nobody_however_long_is_said_as_nobody_and_never_stalled():
    """Nothing of b has run, stood in sluice, had a card open or been held for seven minutes, then two: nobody holds it
    since the stage ended, and no word of a stall is said (teams.23 retires with the-team-machinery-leaves)."""
    for end in (27, 22):
        got = split(end, stages=[{"start": t(0), "end": t(20), "merge": False}])
        assert got["shares"] == shares(team=20, nobody=end - 20)
        assert got["now"] == {"holder": "nobody", "what": None, "since": t(20)} and "stalled" not in got
        assert plan.time_said(got, t(end)).endswith(f"; nobody since {t(20).astimezone():%H:%M}")


# ------------------------------------------------------------------------------------------------------- the edges

def test_the_shares_sum_to_the_age():
    """Pieces that are not whole minutes still give whole minutes that add up."""
    sec = datetime.timedelta(seconds=1)
    got = plan.bolt_time(STARTED, t(10) + 50 * sec, [{"start": t(0) + 20 * sec, "end": t(3) + 40 * sec, "merge": False}],
                         [{"submitted": t(4), "started": None, "decided": t(6) + 30 * sec, "state": "landed"},
                          {"submitted": t(6) + 40 * sec, "started": t(6) + 50 * sec, "decided": t(7) + 10 * sec, "state": "landed"}],
                         [{"at": t(7) + 20 * sec, "until": None, "key": "land/b"}], [])
    assert got["age"] == 10 and sum(got["shares"].values()) == 10 and got["shares"]["team_or_kit"] == 2


def test_a_stage_with_no_end_runs_to_the_end():
    got = split(45, stages=[{"start": t(15), "end": None, "merge": False, "what": "verify on a"}])
    assert got["shares"] == shares(nobody=15, team=30) and got["now"]["what"] == "verify on a"


def test_a_card_closed_before_the_start_is_left_out_and_one_open_across_it_counts_from_the_start():
    got = split(30, cards=[{"at": t(-60), "until": t(-10), "key": "batch/3"}, {"at": t(-5), "until": t(10), "key": "batch/4"}])
    assert got["shares"] == shares(user=10, nobody=20)


def test_a_submission_standing_not_under_test_is_the_teams():
    got = split(20, submissions=[{"submitted": t(5), "started": None, "decided": None, "state": "passed", "what": "#9"}])
    assert got["shares"] == shares(nobody=5, team=15)


def test_a_bolt_started_this_minute_is_nobodys():
    got = split(0)
    assert got == {"age": 0, "shares": shares(), "now": {"holder": "nobody", "what": None, "since": STARTED}}


# ------------------------------------------------------------------------------------- each holder from what crew keeps


PLAN = plan.Plan(plan_text(bolts=[("b", "switchboard-kit", True), ("o", "switchboard-kit", True)],
                           units=[("a", "switchboard-kit", "b", []), ("c", "switchboard-kit", "b", [], "chore"),
                                  ("x", "switchboard-kit", "o", [])]))


def e(act, minutes, *on, **fields):
    """A run-record entry, minutes after START, as record.parse reads one."""
    return dict({"Act": act, "At": at(minutes), "On": list(on)}, **fields)


def given(minutes=0):
    """The bolt's start, minutes after START."""
    return e("bolt.start", minutes, "bolt/b")


def facts_of(entries, unread=None):
    return plan.bolt_facts(entries, PLAN, "b", "wldn", "chuck-herdr-alpha", "switchboard-kit", unread)


def mins(m):
    return START + datetime.timedelta(minutes=m)


def test_the_start_is_the_newest_and_its_stages_pair_with_their_ends():
    """An older crew's give of b, a start of it refused, and its start."""
    entries = [e("bolt.give", -500, "bolt/b", "team/swb-1"), e("bolt.start", -100, "bolt/b", Refused="its host is held"), given(0),
               e("stage.start", 5, "stage/a/code", "unit/a", "agent/swb-1-unit-1"),
               e("stage.start", 6, "stage/c/code", "chore/c", "agent/swb-1-unit-2"),
               e("stage.end", 30, "stage/a/code", "unit/a", "agent/swb-1-unit-1"),
               e("stage.start", 40, "stage/x/code", "unit/x", "agent/swb-2-unit-1"),
               e("fix.start", 50, "fix/b/take-main", "bolt/b", "agent/swb-1-unit-3"),
               e("stage.end", 55, "fix/b/take-main", "agent/swb-1-unit-3"),
               e("fix.merge", 56, "fix/b/take-main", "bolt/b", "agent/swb-1-unit-3"),
               e("stage.start", 57, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("stage.end", 70, "stage/a/merge", "unit/a", "agent/swb-1-unit-1")]
    got = facts_of(entries)
    assert got["start"] == mins(0)
    assert got["stages"] == [
        {"start": mins(5), "end": mins(30), "merge": False, "what": "code on a", "work": "unit/a"},
        {"start": mins(6), "end": None, "merge": False, "what": "code on chore c", "work": "chore/c"},
        {"start": mins(50), "end": mins(55), "merge": False, "what": "fix fix/b/take-main", "work": "fix/b/take-main"},
        {"start": mins(56), "end": None, "merge": True, "what": "merge of fix/b/take-main", "work": "fix/b/take-main"},
        {"start": mins(57), "end": mins(70), "merge": True, "what": "merge on a", "work": "unit/a"}]


def test_the_users_card():
    """Every unit of b has merged, nothing runs, and its kit's landings card has been open for an hour."""
    entries = [given(0), e("stage.start", 0, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("stage.end", 60, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("card.post", 30, "bolt/o", Card="req_1", Key="land/switchboard-kit", By="wldn-ops"),
               e("card.close", 30, Card="req_1", Key="land/switchboard-kit", State="closed"),
               e("card.post", 60, Card="req_2", Key="land/switchboard-kit", By="wldn-ops")]
    got = plan.time_at(facts_of(entries), mins(120))
    assert got["shares"]["user"] == 60 and got["shares"]["team_or_kit"] == 60, "a merge with no submit held was counted the team's"
    assert got["now"] == {"holder": "user", "what": "land/switchboard-kit", "since": mins(60)}


def test_a_main_level_question_about_something_else_is_no_card_of_the_bolts():
    """crew-board "A main-level question about something else": agentplot-design's question, its post naming the asker
    alone, is none of b's, nor is any question of a main-level role's that names neither b nor its work (design
    Decision 8); a question whose post names b's work is b's."""
    entries = [given(0),
               e("card.post", 10, "agent/wldn-design", Card="req_3", Key="ask/wldn-design/sluice-who-claims", By="wldn-design"),
               e("card.post", 12, "agent/wldn-planner", Card="req_4", Key=None, By="wldn-planner"),
               e("card.post", 14, "agent/wldn-ops", "unit/a", Card="req_5", Key="ask/wldn-ops/a-zone", By="wldn-ops")]
    got = facts_of(entries)
    assert [(c["key"], c["at"]) for c in got["cards"]] == [("ask/wldn-ops/a-zone", mins(14))]


def test_a_cards_span_ends_at_the_users_answer_or_its_close_whichever_is_first():
    """A batch card holding a, posted at 2 and answered at 20, closed at 50; a proposal's naming b, closed at 30 with no
    answer recorded; the answer of a copy lost to its owner reached nobody, so the copy posted again waits anew."""
    entries = [given(0), e("review.batch", 1, Batch="12", Units="a:b@abc1234"),
               e("card.post", 2, "batch/12", Card="req_b12", Key="batch/12", By="wldn-planner"),
               e("card.answer", 20, "batch/12", Card="req_b12", Key="batch/12", Answer="answered with a note"),
               e("card.answer", 25, "batch/12", Card="req_b12", Key="batch/12", Answer="again"),
               e("card.close", 50, Card="req_b12", Key="batch/12", State="closed"),
               e("plan.propose", 3, "proposal/7", "bolt/b"),
               e("card.post", 4, "proposal/7", Card="req_p7", Key="proposal/7", By="wldn-planner"),
               e("card.close", 30, Card="req_p7", Key="proposal/7", State="closed"),
               e("card.post", 5, Card="req_l1", Key="land/b", By="wldn-ops"),
               e("card.answer", 6, Card="req_l1", Key="land/b", Answer="approved"),
               e("card.close", 7, Card="req_l1", Key="land/b", State="lost"),
               e("card.post", 8, Card="req_l2", Key="land/b", By="wldn-ops")]
    got = {c["key"]: (c["at"], c["until"]) for c in facts_of(entries)["cards"]}
    assert got == {"batch/12": (mins(2), mins(20)), "proposal/7": (mins(4), mins(30)), "land/b": (mins(5), None)}


def test_the_user_answered_the_landings_card():
    """crew-board "The user answered the landings card": b's kit's card posted at 14:00 (here 0) with b among its rows,
    answered at 14:40, ops not yet submitting b: 14:00 to 14:40 the user's, nobody's after, and the user holds b no
    more."""
    entries = [given(-30), e("stage.start", -20, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("stage.end", -10, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("card.post", 0, "kit/switchboard-kit", Card="req_e9", Key="land/switchboard-kit", By="wldn-ops", Heads="b@abc1234 o@def5678"),
               e("card.answer", 40, "kit/switchboard-kit", Card="req_e9", Key="land/switchboard-kit", Answer="ticked b", Heads="b@abc1234")]
    facts = facts_of(entries)
    assert [(c["at"], c["until"]) for c in facts["cards"]] == [(mins(0), mins(40))]
    got = plan.time_at(facts, mins(70))
    assert got["shares"]["user"] == 40 and got["now"]["holder"] == "nobody"


def test_a_landings_card_that_no_longer_carries_the_bolt():
    """crew-board "A landings card that no longer carries the bolt": changed at 15:00 (here 60) to rows that no longer
    name b; an older post recorded with no Heads names every bolt, as before crew recorded heads; none counts before
    b's last merge ends."""
    merged = [given(-30), e("stage.start", -20, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
              e("stage.end", -10, "stage/a/merge", "unit/a", "agent/swb-1-unit-1")]
    card = [e("card.post", 0, Card="req_e9", Key="land/switchboard-kit", By="wldn-ops", Heads="b@abc1234 o@def5678"),
            e("card.update", 60, Card="req_e9", Key="land/switchboard-kit", By="wldn-ops", Heads="o@def5678"),
            e("card.update", 90, Card="req_e9", Key="land/switchboard-kit", By="wldn-ops", Heads="o@def5678 b@1111111")]
    assert [(c["at"], c["until"]) for c in facts_of(merged + card)["cards"]] == [(mins(0), mins(60)), (mins(90), None)]
    bare = [e("card.post", -20, Card="req_e1", Key="land/switchboard-kit", By="wldn-ops")]
    assert [(c["at"], c["until"]) for c in facts_of(merged + bare)["cards"]] == [(mins(-10), None)]
    assert facts_of(merged[:1] + card)["cards"] == []


def test_a_held_host():
    """Nothing of b runs and no card of it is open, while the host its work runs on was held at 14:02 and not let go."""
    entries = [given(0), e("host.hold", 10, "host/chuck-herdr-alpha", By="chuck"), e("host.go", 20, "host/chuck-herdr-alpha", By="chuck"),
               e("host.hold", 30, "host/mac-studio", By="chuck"), e("host.hold", 40, "host/chuck-herdr-alpha", By="chuck")]
    got = plan.time_at(facts_of(entries), mins(50))
    assert got["shares"]["hold"] == 20 and got["shares"]["nobody"] == 30
    assert got["now"] == {"holder": "hold", "what": "its host chuck-herdr-alpha is held by chuck", "since": mins(40)}


def test_a_batch_card_a_proposal_card_and_a_card_whose_post_names_the_work_are_the_bolts():
    entries = [given(0), e("review.batch", 1, Batch="12", Units="a:b@abc1234 x:o@def5678"),
               e("review.batch", 1, Batch="13", Units="x:o@def5678"),
               e("card.post", 2, "batch/12", Card="req_b12", Key="batch/12", By="wldn-planner"),
               e("card.post", 2, "batch/13", Card="req_b13", Key="batch/13", By="wldn-planner"),
               e("plan.propose", 3, "proposal/7", "unit/a", "bolt/b"), e("plan.propose", 4, "proposal/8", "unit/x"),
               e("plan.propose", 5, "proposal/9", "unit/x", "proposal/8"), e("plan.propose", 5, "proposal/10", "unit/y", "proposal/7"),
               e("card.post", 6, "proposal/7", Card="req_p7", Key="proposal/7", By="wldn-planner"),
               e("card.post", 6, "proposal/8", Card="req_p8", Key="proposal/8", By="wldn-planner"),
               e("card.post", 7, "unit/a", Card="req_r", Key="record/switchboard-kit/0012", By="wldn-design")]
    assert sorted(c["key"] for c in facts_of(entries)["cards"]) == ["batch/12", "proposal/7", "record/switchboard-kit/0012"]


def test_a_card_lost_to_its_owner_and_posted_again_counts_as_one_open_card():
    entries = [given(0), e("card.post", 10, Card="req_1", Key="land/b", By="wldn-ops"),
               e("card.close", 20, Card="req_1", Key="land/b", State="lost"),
               e("card.post", 25, Card="req_2", Key="land/b", By="wldn-ops"),
               e("card.close", 40, Card="req_2", Key="land/b", State="closed")]
    assert [(c["at"], c["until"]) for c in facts_of(entries)["cards"]] == [(mins(10), mins(40))]


def test_the_kits_landings_card_counts_from_the_bolts_last_merge():
    entries = [given(0), e("card.post", 5, Card="req_1", Key="land/switchboard-kit", By="wldn-ops"),
               e("stage.start", 10, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("stage.end", 30, "stage/a/merge", "unit/a", "agent/swb-1-unit-1")]
    assert [c["at"] for c in facts_of(entries)["cards"]] == [mins(30)]
    assert facts_of(entries[:2])["cards"] == []


def test_no_submission_is_the_bolts_time_whatever_the_record_names():
    """crew-board "A submission the runner reports" and run-record "No record of sluice's is read": a submit an older
    crew queued naming #52, and the land crew posted for b, place no minute; the runner's report carries no time of a
    submission (crew-lands-each-bolt-through-flumes-base-place, Decision 7)."""
    entries = [given(0), e("bolt.submit", 30, "bolt/b", Outcome="queued", Submission="52"),
               e("bolt.submit", 40, "bolt/b", Outcome="asked", Request="57", Card="req_1", Head="abc1234")]
    assert facts_of(entries)["submissions"] == []


def spent(entries, end):
    return plan.landing_spent(entries, PLAN, PLAN.bolt("b"), "wldn", "switchboard-kit", mins(end))


def test_a_landing_records_the_age_and_split_its_head_line_gives():
    """run-record "A bolt lands": b started 6h 10m before its landing is recorded, its work holding it 3h 45m, the
    user 2h 05m and nobody 20m."""
    entries = [given(0), e("stage.start", 0, "stage/a/code", "unit/a", "agent/swb-1-unit-1"),
               e("stage.end", 225, "stage/a/code", "unit/a", "agent/swb-1-unit-1"),
               e("card.post", 225, Card="req_l1", Key="land/b", By="wldn-ops"),
               e("card.answer", 350, Card="req_l1", Key="land/b", Answer="approved")]
    assert spent(entries, 370) == {"Age": "370", "Split": "team 225, kit 0, team-or-kit 0, user 125, hold 0, nobody 20"}


def test_a_landing_by_pull_request_places_none_of_its_minutes_on_the_kit():
    """crew-board "A landing by pull request" and run-record "No record of sluice's is read": b's base place landed
    after its submission #52 from pull/9 stood under test, and its unit a's #41 stood seventeen minutes; none of it is
    the kit's, and the split sums to the age."""
    entries = [given(0), e("stage.start", 0, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("stage.end", 20, "stage/a/merge", "unit/a", "agent/swb-1-unit-1"),
               e("bolt.submit", 30, "bolt/b", Outcome="asked", Request="57"),
               e("bolt.submit", 31, "bolt/b", Outcome="submitted", Submission="52")]
    got = spent(entries, 60)
    split = dict((h, int(m)) for h, m in (x.rsplit(" ", 1) for x in got["Split"].split(", ")))
    assert got["Age"] == "60" and split["kit"] == 0 and sum(split.values()) == 60


def test_a_landing_whose_start_cant_be_read_carries_no_age_or_split():
    """run-record "The start can't be read": the record holds no start of b."""
    assert spent([e("bolt.start", 0, "bolt/o")], 30) == {}


def test_an_older_crews_give_is_the_start_where_the_record_holds_no_start():
    assert facts_of([e("bolt.give", 0, "bolt/b", "team/swb-1")])["start"] == mins(0)


def test_a_start_that_cant_be_read_is_said_and_shows_no_share():
    """The run record holds no start of b, nor an older crew's give of it, in the days the board reads."""
    got = plan.time_at(facts_of([e("bolt.start", 0, "bolt/o"), e("bolt.give", 0, "bolt/o", "team/swb-2")]), mins(10))
    assert got == {"unknown": "its age can't be told: the run record of the last 60 days holds no start of it"}


def test_a_record_that_cant_be_read_is_said():
    got = facts_of([given(0)], unread={"wldn/main of WilldanGroup/crew-state": "fetch failed"})
    assert got == {"unknown": "its age can't be told: wldn/main of WilldanGroup/crew-state could not be read (fetch failed)"}
