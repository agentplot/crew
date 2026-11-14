"""crew bolt new|order|drop|start on the plan (bolt-plan spec): each applied to a plan in memory, with the stages a drop
reads given; when a bolt lands (plan.land_refusal), started or not (plan.unheld_stages, plan.unheld_refusal,
plan.main_kit); and what a start appends, its base place's launch and then its pieces', reading no host
(crew-lands-each-bolt-through-flumes-base-place, Decision 3). The commits every write makes are the journey's
(t-journey-units and t-journey-land)."""
import base64
import pathlib

import pytest
from facts import FLEET, FactsWrite, apply, kept_by, known, plan_text, ran, units_of

import plan
import runner

KIT, BOARD = "switchboard-kit", "breadboard-kit"


def fresh():
    return FactsWrite(plan_text(bolts=[("tenant-environments", KIT, "swb-1"), ("console-pages", KIT, None), ("board-builds", BOARD, None)],
                                units=[("a-console-page", KIT, "console-pages", []), ("a-console-filter", KIT, "console-pages", ["a-console-page"]),
                                       ("lint-once", KIT, "tenant-environments", [])]))


def bolts(w):
    return [b.name() for b in w.plan.bolts()]


def run(w, *dos, stages=None):
    return apply(w, *dos, ctx=known(w, stages=stages))


def refusal(w, do, **kw):
    with pytest.raises(plan.Refusal) as e:
        run(w, do, **kw)
    return str(e.value)


class TestNew:
    def test_adds_a_bolt_last_or_before_one_named_with_its_sources(self):
        w = run(fresh(), 'bolt new apex-zones "Each apex is a zone." --repo switchboard-kit --before console-pages',
                'bolt new last-one "Last." --repo switchboard-kit --source books/x.md')
        assert bolts(w) == ["tenant-environments", "apex-zones", "console-pages", "board-builds", "last-one"]
        assert w.plan.bolt("last-one").all("Source") == ["books/x.md"]

    def test_refuses_a_name_the_plan_has(self):
        assert refusal(fresh(), 'bolt new console-pages "again" --repo switchboard-kit') == "wldn/main already has bolt console-pages"

    def test_a_kit_the_plan_does_not_name_enters_it_with_its_first_bolt(self):
        """Decision 3 of the-team-machinery-leaves: there is no registry of repositories in crew."""
        w = run(fresh(), 'bolt new rocs "x" --repo rocs-kit')
        assert w.plan.bolt("rocs").get("Repo") == "rocs-kit"

    def test_a_bolt_planned_to_stay_is_marked_in_the_plan(self):
        """bolt-plan "Planned to stay" (record 0067): --stays marks the bolt Stays: yes in the write that plans it, and
        a bolt planned without it carries no mark."""
        w = fresh()
        op = plan.op_bolt_new(known(w), plan.do_args("wldn", 'bolt new apex-zones "Each apex is a zone." --repo switchboard-kit --stays'))
        op.change(w)
        assert (w.plan.bolt("apex-zones").get("Stays"), op.act, op.on) == ("yes", "bolt.new", ["bolt/apex-zones"])
        w = run(w, 'bolt new last-one "Last." --repo switchboard-kit')
        assert w.plan.bolt("last-one").get("Stays") is None


def test_no_command_marks_a_bolt_to_stay_later():
    """bolt-plan "No mark later": crew has no command that marks a bolt planned or started already, so the mark is set
    ahead of time and never once the bolt is proven; a flag --stays on any other command is refused as crew's parser
    reads it, the plan unchanged."""
    w = fresh()
    before = w.plan.text()
    for do in ("bolt stay console-pages", "bolt order console-pages --first --stays", 'bolt drop console-pages "x" --stays',
               "unit order a-console-page --first --stays"):
        with pytest.raises(plan.Refusal):
            run(w, do)
    with pytest.raises(SystemExit):
        plan.parser().parse_args(["bolt", "stay", "console-pages"])
    assert w.plan.text() == before


def test_a_branch_from_before_the_mark_takes_it_at_its_next_write():
    """bolt-plan "A branch from before the mark and the holds": a plan whose Bolt descriptor predates the mark is read as
    it stands, and its next write brings its descriptor in step (plan.in_step), allowing Stays as crew's own does."""
    old = plan.HEADER.replace("%type: Stays enum yes\n", "").replace(" Path Stays\n", " Path\n")
    p = plan.Plan(old.replace("%rec: Unit", "Bolt: b\nRepo: switchboard-kit\nGoal: g\n\n%rec: Unit"))
    assert "%type: Stays" not in p.text() and p.bolt("b").get("Repo") == "switchboard-kit"
    assert plan.in_step(p) is True
    assert "%type: Stays enum yes" in p.text() and "%allowed: Bolt Repo Goal Source Path Stays" in p.text()
    assert plan.in_step(p) is False


class TestOrder:
    @pytest.mark.parametrize("how, order", [
        ("--first", ["board-builds", "tenant-environments", "console-pages"]),
        ("--before console-pages", ["tenant-environments", "board-builds", "console-pages"]),
        ("--last", ["tenant-environments", "console-pages", "board-builds"])])
    def test_moves_a_bolt(self, how, order):
        assert bolts(run(fresh(), f"bolt order board-builds {how}")) == order

    def test_a_bolt_never_goes_before_itself(self):
        assert refusal(fresh(), "bolt order console-pages --before console-pages") == "a bolt can't go before itself"


class TestDrop:
    def test_removes_a_bolt_and_its_units(self):
        w = run(fresh(), 'bolt drop console-pages "folded into the portal"')
        assert bolts(w) == ["tenant-environments", "board-builds"]
        assert [u.name() for u in w.plan.units()] == ["lint-once"]

    def test_requeue_queues_its_units_without_their_after(self):
        w = run(fresh(), 'bolt drop console-pages "folded into the portal" --requeue')
        assert units_of(w, repo=KIT) == ["a-console-page", "a-console-filter"]
        assert w.plan.unit("a-console-filter").all("After") == []

WHERE = "/kit/main/.config/sluice.toml"
POLICY = '[branches."bolt/*"]\nrequired = ["#check-full"]\nremote = "origin"\n'


class TestStart:
    """bolt-plan "crew bolt start requests a bolt's base place and then its pieces in one plan write" and bolt-teams "A start launches the bolt's base place before
    its pieces" (crew-lands-each-bolt-through-flumes-base-place, Decision 3): one plan write marks the bolt Path: flume
    and appends its base place's launch and then its pieces', reading no host and making no branch; refused, the plan
    unchanged and nothing requested, while no runner answers for the drive, and for a bolt started already, but one
    whose own launch the runner refused, which it launches anew (runner.restart). Its pieces' launches are the cross
    tests' (test_cross.py); its commit the cross journey's (t-journey-cross)."""
    HOST = "mac-studio"

    @pytest.fixture(autouse=True)
    def no_host(self, monkeypatch):
        """Every host read refused: a start reads none (drive-state "A bolt's start reads and runs nothing on any
        host")."""
        import crew

        def refused(*a, **k):
            raise AssertionError("a start reads no host")
        monkeypatch.setenv("CREW_AGENT", "chuck")
        monkeypatch.setattr(crew, "on_machine", refused)
        monkeypatch.setattr(plan, "host_run", refused)

    def write(self, requests="", refused=None, launched=None, held=()):
        """wldn's plan of fresh() with requests.rec holding requests (records' text), and its runner on deneb answering
        each request in refused, launched and held as facts.ran does."""
        w = fresh()
        w.files["requests.rec"] = runner.REQUESTS + requests
        reads = ran(label="wldn", refused=refused, held=held) if launched is None else ran(label="wldn", launched=launched, refused=refused, held=held)
        return FactsWrite(w.plan.text(), files=w.files, runners=reads)

    def requests(self, w):
        return [(r.get("Request"), r.get("Act"), r.get("Work"), r.get("Base"), r.get("Of"), r.get("Kind"))
                for r in plan.Plan(w.files["requests.rec"]).recs("Request")]

    def test_a_start_launches_the_base_place_then_its_pieces_in_one_write_reading_no_host(self):
        w = self.write()
        run(w, "bolt start console-pages")
        assert plan.started(w.plan.bolt("console-pages"))
        assert self.requests(w) == [
            ("1", "launch", "bolt/console-pages", "main", None, "crew/bolt"),
            ("2", "launch", "unit/a-console-page", "bolt/console-pages", None, "change"),
            ("3", "launch", "unit/a-console-filter", "bolt/console-pages", None, "change")]
        bolt, = [r for r in plan.Plan(w.files["requests.rec"]).recs("Request") if r.get("Work") == "bolt/console-pages"]
        assert (bolt.get("Name"), bolt.get("Repo"), bolt.get("Intent"), bolt.get("Recipient"), bolt.get("Brief"), bolt.all("After")) == (
            "console-pages", KIT, "wldn/console-pages", "wldn/ops", None, [])

    def test_a_start_where_the_main_level_host_keeps_no_checkout_of_the_kit_goes_on(self):
        w = self.write()
        fleet = kept_by(FLEET, "wldn", "/w", f"WilldanGroup/{BOARD}")
        apply(w, "bolt start console-pages", ctx=known(w, fleet=fleet))
        assert [r[2] for r in self.requests(w)] == ["bolt/console-pages", "unit/a-console-page", "unit/a-console-filter"]

    def test_a_drive_no_runner_answers_for_is_refused_and_nothing_is_requested(self):
        w = fresh()
        with pytest.raises(plan.Refusal) as e:
            run(w, "bolt start console-pages")
        assert str(e.value).startswith("no runner answers for wldn: its state repository holds no wldn/runner/<host>")
        assert not plan.started(w.plan.bolt("console-pages")) and "requests.rec" not in w.files

    def test_a_bolt_started_before_bolts_were_base_places_is_refused_as_started_already(self):
        w = self.write()
        assert refusal(w, "bolt start tenant-environments") == (
            "bolt tenant-environments is started already, before bolts were base places, and lands under the crew that started it")
        assert self.requests(w) == []

    BOLT = "\nRequest: 1\nAct: launch\nWork: bolt/console-pages\nRepo: switchboard-kit\nKind: crew/bolt\nName: console-pages\nBase: main\nPriority: 2\nIntent: wldn/console-pages\nRecipient: wldn/ops\nDate: 2026-11-08T12:00:00Z\nBy: chuck\n"
    PIECE = "\nRequest: 2\nAct: launch\nWork: unit/a-console-page\nRepo: switchboard-kit\nKind: change\nName: a-console-page\nBase: bolt/console-pages\nPriority: 2\nIntent: wldn/console-pages\nRecipient: wldn/planner\nBrief: Unit a-console-page.\nDate: 2026-11-08T12:00:00Z\nBy: chuck\n"

    def started_write(self, **answers):
        w = self.write(self.BOLT + self.PIECE, **answers)
        w.plan.bolt("console-pages").set("Path", "flume")
        return w

    def test_started_again_after_the_runner_refused_its_launch_it_drops_its_unlaunched_pieces_and_launches_anew(self):
        """bolt-teams "Started again": one write appends a drop of a's launch, then a launch of bolt/x and a launch of a
        after it, and a-console-filter, never launched, after them."""
        w = self.started_write(refused={1: "flume refused the launch: crew/bolt@1 is not locked on deneb"})
        run(w, "bolt start console-pages")
        assert self.requests(w)[2:] == [
            ("3", "drop", "unit/a-console-page", None, "2", None),
            ("4", "launch", "bolt/console-pages", "main", None, "crew/bolt"),
            ("5", "launch", "unit/a-console-page", "bolt/console-pages", None, "change"),
            ("6", "launch", "unit/a-console-filter", "bolt/console-pages", None, "change")]

    def test_a_bolt_started_to_stay_is_marked_in_the_start_write(self):
        """bolt-plan "Started to stay": the start's one write marks the bolt Path: flume and Stays: yes and requests its
        launches as any start does; a start run again after the runner refused its launch, nothing built then, marks
        it too, and a start without --stays marks nothing."""
        w = self.write()
        run(w, "bolt start console-pages --stays")
        b = w.plan.bolt("console-pages")
        assert (b.get("Path"), b.get("Stays")) == ("flume", "yes")
        assert [r[2] for r in self.requests(w)] == ["bolt/console-pages", "unit/a-console-page", "unit/a-console-filter"]
        w = self.started_write(refused={1: "flume refused the launch: crew/bolt@1 is not locked on deneb"})
        run(w, "bolt start console-pages --stays")
        assert w.plan.bolt("console-pages").get("Stays") == "yes"
        w = self.write()
        run(w, "bolt start console-pages")
        assert w.plan.bolt("console-pages").get("Stays") is None

    @pytest.mark.parametrize("answers", [{}, {"held": (1,)}, {"launched": {1: "flume-0.17.0/bolt-submitted"}}])
    def test_a_bolt_whose_launch_is_unanswered_held_or_launched_is_refused_as_started_already(self, answers):
        w = self.started_write(**answers)
        assert refusal(w, "bolt start console-pages") == "bolt console-pages is started already"
        assert len(self.requests(w)) == 2


class TestLand:
    def land(self, stages, outside=(), of=None):
        return plan.land_refusal("console-pages", ["a-console-page", "a-console-filter"],
                                 of or (lambda u: {"stage": stages[u], "why": "its host did not answer"}), list(outside), "wldn")

    def test_lands_once_every_unit_has_landed_and_been_in_a_batch(self):
        assert self.land({"a-console-page": "landed", "a-console-filter": "landed"}) is None

    def test_a_unit_not_landed_on_main_refuses_it(self):
        assert self.land({"a-console-page": "landed", "a-console-filter": "merged"}) == "unit a-console-filter has not landed on main: it is merged"
        assert self.land({"a-console-page": "unknown", "a-console-filter": "landed"}) == (
            "cannot tell whether unit a-console-page has landed: its host did not answer")

    def test_the_landing_records_the_commit_main_holds_now(self):
        """plan.14, plan.18: the landing records the commit GitHub's main holds after the command's fetch, for a kit with
        an origin, and nothing is refused for the host's own main lagging it (plan.8); what can't be read refuses."""
        github, own = "c" * 40, "d" * 40
        assert plan.main_held("switchboard-kit", "chuck-herdr-alpha", f"ORIGIN=yes\nFETCHED=ok\nGITHUB={github}\nOWN={own}\n") == (github, None)
        for said in (f"{github} 0 1\n", "", "fatal: bad\n"):
            assert plan.main_held("switchboard-kit", "chuck-herdr-alpha", said) == (
                None, f"crew can't read what switchboard-kit's main on chuck-herdr-alpha holds: {said.strip() or 'nothing was said'}")

    def test_a_bolt_no_team_holds_lands_once_each_units_change_is_on_its_kits_main(self):
        planned = lambda u: {"stage": "ready"}
        of = plan.unheld_stages({"main": ["a-console-page", "a-console-filter"]}, None, planned)
        assert self.land({}, of=of) is None
        of = plan.unheld_stages({"main": ["a-console-page"]}, None, planned)
        assert self.land({}, of=of) == "unit a-console-filter has not landed on main: it is ready"
        of = plan.unheld_stages({"main": ["a-console-page", "a-console-filter"], "chores": []}, None, planned, ["a-console-filter"])
        assert self.land({}, of=of) == "chore a-console-filter has not landed on main: it is ready"
        of = plan.unheld_stages({"main": ["a-console-page"], "chores": ["a-console-filter"]}, None, planned, ["a-console-filter"])
        assert self.land({}, of=of) is None
        of = plan.unheld_stages(None, "chuck-herdr-alpha did not answer", planned)
        assert self.land({}, of=of) == "cannot tell whether unit a-console-page has landed: chuck-herdr-alpha did not answer"

    def test_a_bolt_never_started_is_read_in_the_checkout_the_main_level_host_keeps_of_its_kit(self):
        """The user's ruling of 2026-11-01: a bolt no runner took work of is read and landed on its drive's main-level host."""
        t = plan.main_kit(FLEET, "wldn", BOARD)
        assert (t["machine"], t["kit"]["main"]) == ("mac-studio", f"/w/{BOARD}/main")
        assert plan.unheld_refusal(FLEET, "console-pages", ["a-console-page"], KIT, t, "wldn") is None
        assert plan.unheld_refusal(FLEET, "console-pages", ["a-console-page"], "rocs-kit", None, "wldn") == (
            "bolt console-pages was never started, and wldn's main level runs on mac-studio, and the teams file keeps no rocs-kit there, "
            "so crew can't read its main; if it was renamed on its host, crew kit rename rocs-kit <new> names it so in the plan")
        assert plan.unheld_refusal(FLEET, "console-pages", [], KIT, t, "wldn") == (
            "bolt console-pages was never started and holds no units or chores, so nothing of it has landed")

    def test_a_change_no_batch_has_held_refuses_it(self):
        assert self.land({"a-console-page": "landed", "a-console-filter": "landed"}, ["a-console-page", "a-console-filter"]) == (
            "bolt console-pages lands only once every unit's latest change has been in a batch, and a-console-page or "
            "a-console-filter have not: a batch is due for them (crew review wldn)")


class TestWhereABoltIsRead:
    """bolt-plan "crew reads a bolt at GitHub's copy where its policy names a remote, and else at the host's own" (plan.19, design Decision 1): GitHub's copy when the host holds
    it and the policy in it names a remote for the bolt, else the host's own branch, the only copy the host then has."""

    def test_githubs_copy_naming_a_remote_is_where_the_bolt_is_read(self):
        assert plan.gather.bolt_at("b", True, True, "origin") == "refs/remotes/origin/bolt/b"
        assert plan.gather.bolt_at("b", True, False, "origin") == "refs/remotes/origin/bolt/b"

    def test_a_bolt_kept_on_its_host_is_read_at_the_hosts_branch(self):
        """bolt-plan "A bolt kept on its host"."""
        assert plan.gather.bolt_at("b", True, True, None) == "refs/heads/bolt/b"

    def test_a_bolt_whose_github_copy_the_host_has_not_got_is_read_at_the_hosts(self):
        """bolt-plan "A bolt GitHub's copy of which this host has not got"."""
        assert plan.gather.bolt_at("b", False, True, None) == "refs/heads/bolt/b"
        assert plan.gather.bolt_at("b", False, False, None) is None
        assert plan.gather.bolt_at("b", True, False, None) is None

    def test_the_remote_a_policy_names_for_a_bolt(self):
        assert plan.gather.policy_remote(POLICY, "bolt/b") == "origin"
        specific = '[branches."*"]\nremote = "origin"\n[branches."bolt/*"]\nrequired = ["#check-full"]\n'
        assert plan.gather.policy_remote(specific, "bolt/b") is None
        assert plan.gather.policy_remote('[branches."main"]\nremote = "origin"\n', "bolt/b") is None
        assert plan.gather.policy_remote(None, "bolt/b") is None
        assert plan.gather.policy_remote("", "bolt/b") is None

    def test_a_policy_that_is_not_toml_raises(self):
        with pytest.raises(ValueError):
            plan.gather.policy_remote("[branches\n", "bolt/b")

    def test_kit_matches_branches_as_gather_does(self):
        assert plan.kit.branch_table is plan.gather.branch_table

    def test_a_started_bolt_whose_policy_crew_cant_read_is_unknown(self, monkeypatch):
        """bolt-plan "A policy crew can't read": nothing is read from the host's bolt/b in its place, so the bolt's state is
        unknown; its pieces read their stages from the runner's records, landed once main holds them."""
        from facts import crew_read, launched, madswan_fleet, ran
        monkeypatch.setenv("CREW_AGENT", "madswan-planner")
        why = ".config/sluice.toml at origin/bolt/b is not TOML, so crew can't read bolt b: Expected ']'"
        fleet = madswan_fleet()
        p, requests = launched(["b"], work=[("a", "b", [], "unit", []), ("done", "b", [], "unit", [])], fleet=fleet)
        unread = {"exists": False, "head": None, "head_at": None, "error": why}
        st = plan.Stages(fleet, p, crew_read(main=["done"], bolts={"b": unread}), runs={"madswan": (requests, ran({1: "code", 2: "landed"}))},
                         label="madswan")
        assert (st.of("a")["stage"], st.of("a")["worktree"]) == ("code", None)
        assert st.of("done")["stage"] == "landed"
        assert st.bolt_state(p.bolt("b")) == "unknown"


class TestWhenABoltIsFetched:
    """bolt-plan "A bolt on GitHub is fetched where a decision rests on it" (plan.18, plan.19, design Decision 3): crew
    bolts asks each kit's GitHub fetched first; every other read fetches nothing. b is started, its work running on box,
    where the runner that took it reported the kit in /kit/main (plan.bolt_at)."""
    FLEET = {"drives": {"wldn": {"label": "wldn", "machine": "mac-studio"}}}
    KIT_READ = {"ok": True, "main": [], "chores": [], "places": {}, "chore_places": {}, "fixes": [],
                "bolts": {"b": {"exists": True, "at": "origin/bolt/b", "changes": [], "archived": [], "open": {}, "chores": [],
                                "head": "d" * 40, "head_at": "2026-10-23T09:00:00Z"}}}

    WHERE = {"label": "wldn", "machine": "box", "stream": "wldn", "kit": {"main": "/kit/main", "dir": "/kit/main", "name": KIT, "repo": KIT}}

    def asked(self, monkeypatch, kept=None):
        asks = []
        monkeypatch.setattr(plan, "READ", plan.Reading())
        monkeypatch.setattr(plan, "runner_facts", lambda fleet, label: ([], {}))
        monkeypatch.setattr(plan, "rail_runs", lambda found: {"wldn": ([], {})})
        monkeypatch.setattr(plan, "bolt_at", lambda fleet, label, b, run=None: self.WHERE if plan.started(b) else None)
        monkeypatch.setattr(plan, "drive_entries", lambda fleet, label: [])  # the run record crew bolts reads its landings from
        if kept:
            plan.READ.keep_kits("box", kept)

        def gathered(fleet, host, req):
            asks.append(req)
            return {k["main"]: self.KIT_READ for k in req["kits"]}, None
        monkeypatch.setattr(plan, "gathered", gathered)
        return asks

    def plan(self):
        return plan.Plan(plan_text(bolts=[("b", KIT, "swb-1")], units=[("a", KIT, "b", [])]))

    def test_crew_bolts_asks_each_kit_fetched(self, monkeypatch):
        """bolt-plan "crew bolts after a landing elsewhere"."""
        import argparse
        asks = self.asked(monkeypatch)
        p = self.plan()
        monkeypatch.setattr(plan, "plans", lambda fleet, labels, errors: [("wldn", "o/state", "f" * 40, p)])
        with pytest.raises(SystemExit) as e:
            plan.bolts_view(self.FLEET, argparse.Namespace(label="wldn", bolt=None, json=True))
        assert e.value.code == 0
        assert [[k.get("fetch") for k in a["kits"]] for a in asks] == [[True]]

    def test_crew_bolts_asks_no_fetch_in_the_runners_clone(self, monkeypatch):
        """drive-state "crew fetches nothing in the runner's clone": box's teams file names the kit's repository, whose
        container is the folder its runner reported, so crew bolts asks it read as the runner last fetched it."""
        asks = self.asked(monkeypatch)
        fleet = dict(self.FLEET, repositories={"host": "box", "named": {KIT: {"dir": "/kit/main", "checkout": "/v/kit"}}})
        plan.stages_for(fleet, "wldn", self.plan(), self.plan().bolts(), fetch=True)
        assert [[k.get("fetch") for k in a["kits"]] for a in asks] == [[False]]
        other = dict(self.FLEET, repositories={"host": "deneb", "named": {KIT: {"dir": "/kit/main", "checkout": "/v/kit"}}})
        asks.clear()
        plan.stages_for(other, "wldn", self.plan(), self.plan().bolts(), fetch=True)
        assert [[k.get("fetch") for k in a["kits"]] for a in asks] == [[True]]

    def test_a_read_on_every_team_read_fetches_nothing(self, monkeypatch):
        """bolt-plan "The board does not fetch"."""
        asks = self.asked(monkeypatch)
        plan.stages_for(self.FLEET, "wldn", self.plan(), self.plan().bolts())
        assert [("fetch" in a or any("fetch" in k for k in a["kits"])) for a in asks] == [False]

    def test_a_fetching_survey_is_asked_though_the_command_has_read_the_kit(self, monkeypatch):
        asks = self.asked(monkeypatch, kept={"/kit/main": self.KIT_READ})
        plan.stages_for(self.FLEET, "wldn", self.plan(), self.plan().bolts())
        assert asks == []
        st = plan.stages_for(self.FLEET, "wldn", self.plan(), self.plan().bolts(), fetch=True)
        assert [[k.get("fetch") for k in a["kits"]] for a in asks] == [[True]]
        assert st.kit(self.plan().bolt("b"))[0]["bolts"]["b"]["at"] == "origin/bolt/b"

    def test_a_fetch_that_fails_reads_the_kit_unknown_with_gits_words(self, monkeypatch):
        """bolt-plan "A fetch that fails"."""
        self.asked(monkeypatch)
        why = "cannot fetch /kit/main from GitHub: fatal: unable to access 'https://github.com/o/k/': Could not resolve host"
        monkeypatch.setattr(plan, "gathered", lambda fleet, host, req: ({"/kit/main": {"ok": False, "error": why}}, None))
        st = plan.stages_for(self.FLEET, "wldn", self.plan(), self.plan().bolts(), fetch=True)
        assert st.kit(self.plan().bolt("b")) == (None, f"box: {why}")
        assert st.bolt_state(self.plan().bolt("b")) == "unknown"


class TestCrewBoltsCrossed:
    """crew bolts, text and JSON, reads a piece's stage from the runner's records and says the host and stream it runs
    in as that runner reported (Decisions 8 and 14 of teams-cross-to-flume-as-their-bolts-land; bolt-plan "A started
    bolt's work reads its stage from the runner's records"; the user's ruling of 2026-11-01): x is started, its work taken
    by deneb's runner in stream madswan, its a in code and b after a held; y is planned, not started."""

    @pytest.fixture(autouse=True)
    def writer(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "madswan-dispatch-deneb")

    def data(self, runners, bolt=None):
        from facts import crew_read, launched, madswan_fleet
        fleet = madswan_fleet()
        p, requests = launched(["x"], work=[("a", "x", [], "unit", []), ("b", "x", ["a"], "unit", []), ("y1", "y", [], "unit", [])],
                               fleet=fleet, planned=["y"])
        return plan.bolts_data(fleet, ["madswan"], [("madswan", "afterthought/crew-state", "abcdef1" + "0" * 33, p)],
                               crew_read(bolts={"x": {}, "y": {}}), {}, bolt, runs={"madswan": (requests, runners)})

    def bolts(self, d):
        return {b["bolt"]: b for b in d["drives"][0]["plans"][0]["bolts"]}

    def test_a_bolts_json_gives_its_host_and_stream_and_each_pieces_runner_stage(self):
        from facts import ran
        x = self.bolts(self.data(ran({1: "code"}, held=[2])))["x"]
        assert (x["given"], x["host"], x["stream"]) == ("flume", "deneb", "madswan")
        assert [(u["unit"], u["stage"], u["tasks"], u["worktree"]) for u in x["units"]] == [("a", "code", (6, 26), None),
                                                                                           ("b", "waiting", None, None)]
        assert x["units"][1]["flume"] == {"stage": "waiting", "after": ["unit/a"]}

    def test_crew_bolts_says_a_landing_the_runner_reports_and_writes_nothing(self, monkeypatch):
        """bolt-teams "crew bolts reads it" (state.4): x's land posted, the runner's report has its base place landed at
        a7c3e9f and no read has recorded it; crew bolts says x landed at that commit and writes and records nothing."""
        import runner
        from facts import crew_read, launched, madswan_fleet, ran
        monkeypatch.setattr(plan, "write", lambda *a, **k: pytest.fail("crew bolts made a plan write"))
        monkeypatch.setattr(plan.record, "emit", lambda *a, **k: pytest.fail("crew bolts recorded an entry"))
        fleet = madswan_fleet()
        p, requests = launched(["x"], work=[("a", "x", [], "unit", [])], fleet=fleet)
        base = runner.launch_of(requests, "bolt/x").get("Request")
        m = runner.next_request(requests)
        requests = requests + [plan.Rec("Request", runner.request_fields(m, "land", "bolt/x", {"Of": base}, "2026-11-08T12:00:00Z",
                                                                         "madswan-ops"))]
        reads = ran({1: "landed", base: "flume-0.17.0/bolt-landed"}, unplaced={m: "-"})
        d = plan.bolts_data(fleet, ["madswan"], [("madswan", "afterthought/crew-state", "abcdef1" + "0" * 33, p)],
                            crew_read(bolts={"x": {}}), {}, None, runs={"madswan": (requests, reads)})
        assert self.bolts(d)["x"]["landing"]["outcome"] == "landed"
        assert "landed at a7c3e9f" in plan.bolts_text(d)

    def test_the_text_names_a_crossed_teams_stream_and_each_pieces_stage_and_place(self):
        """bolt-plan "A unit in code" and "A dependent waits"."""
        from facts import ran
        out = plan.bolts_text(self.data(ran({1: "code"}, held=[2]))).splitlines()
        assert "x  crew  @ deneb, in Flume stream madswan  active" in out
        assert f"  {'a':<40} {'code 6/26':<12} flume/change--teams-cross-to-flume-as-their-bolts-land" in out
        assert f"  {'b':<40} {'waiting':<12}   on a" in out

    def test_a_runner_crew_cant_read_is_named_and_its_work_reads_unknown(self):
        """bolt-plan "The runner's host is silent": deneb's runner can't be read, and then no runner answers at all."""
        import runner
        why = "deneb's runner can't be read: madswan/runner/deneb at 5e1f0c2: recfix refused it"
        d = self.data({"deneb": runner.host_read("madswan", "deneb", "5e1f0c2a" + "0" * 32, {}, {"runner.rec": "recfix refused it"})})
        assert {u["stage"] for u in self.bolts(d)["x"]["units"]} == {"unknown"}
        assert d["runners_unread"] == {"deneb's runner": why}
        assert plan.bolts_text(d).splitlines()[-1] == (
            f"deneb's runner can't be read ({why}): the stages of the work crossed to Flume there are unknown")
        none = "no runner answers for madswan: its state repository holds no madswan/runner/<host>"
        assert self.data({})["runners_unread"] == {"madswan's runners": none}

    def test_a_bolt_whose_place_the_runner_has_carried_no_status_of_runs_on_that_runners_host(self):
        """drive-state "A place not carried yet": deneb's runner took a's launch, held it with its claim's words, a naming
        no After, and then launched it at its place with no status of it carried yet; x's head line names deneb, never
        that where it runs can't be told, and a reads launching, with the runner's words while it holds the launch,
        never held for its After work (the signal of 2026-11-07, request 88 of afterthought)."""
        from facts import ran
        claim = "claimed by deneb's runner; launching once no other runner has claimed it"
        d = self.data(ran(held={1: claim, 2: None}))
        x = self.bolts(d)["x"]
        assert (x["host"], x["stream"]) == ("deneb", None)
        assert x["units"][0]["flume"] == {"stage": "launching", "words": claim}
        out = plan.bolts_text(d).splitlines()
        assert any(line.startswith("x  crew  @ deneb  ") for line in out) and "where it runs can't be told" not in "\n".join(out)
        assert f"  {'a':<40} {'launching':<12}   held by the runner: {claim}" in out
        assert f"  {'b':<40} {'waiting':<12}   on a" in out
        d = self.data(ran(unplaced={1: "/places/change--a"}, held=[2]))
        assert self.bolts(d)["x"]["host"] == "deneb" and "where it runs can't be told" not in plan.bolts_text(d)

    def test_a_stop_short_whose_agent_flume_0_17_keeps_open_is_on_its_line_and_its_bolt_runs_on_its_host(self):
        """bolt-plan "A stop-short whose agent is kept open": the runner carries flume 0.17.0's status of a's place,
        its code ended short needing an answer with its agent kept open (tests/py/flume-0.17.0/kept-open.json)."""
        from facts import ran
        d = self.data(ran({1: "flume-0.17.0/kept-open"}, held=[2]))
        assert (self.bolts(d)["x"]["host"], self.bolts(d)["x"]["stream"]) == ("deneb", "madswan")
        assert (f"  {'a':<40} {'needs':<12} flume/change--the-flake-configures-each-tool-by-its-own-module  asks at code: The code "
                "stage of the-flake-configures-each-tool-by-its-own-module cannot start:") in plan.bolts_text(d)

    @pytest.mark.parametrize("fixture, at, words", [
        ("past-bound", "code", "the submission conflicted with its base: [sluice] #24 conflicts on bolt/sluice-runs-one-host-process"),
        ("submission-refused", "its submission", "the merge queue refused the submission: sluice refused the submission:")])
    def test_a_place_waiting_on_its_caller_is_on_its_line_at_what_it_waits_to_retry(self, fixture, at, words):
        """bolt-plan "A place past its bound" and "A submission that waits on its retry": the runner carries flume
        0.17.0's status of a's place, its verify delivered and its submission in conflict past its kind's bound, or
        refused by the merge queue (tests/py/flume-0.17.0/); crew bolts reads a waiting on its caller at the stage it
        waits to retry, or its submission, with Flume's words, never at verify."""
        from facts import ran
        d = self.data(ran({1: f"flume-0.17.0/{fixture}"}, held=[2]))
        assert self.bolts(d)["x"]["units"][0]["flume"]["stage"] == "waits"
        line = next(line for line in plan.bolts_text(d).splitlines() if line.startswith(f"  {'a':<40} "))
        assert line.startswith(f"  {'a':<40} {'waits':<12} flume/change--pull-requests-are-queued-on-the-forge  "
                               f"waits on its caller at {at}: {words}")
        assert "verify" not in line

    def test_a_bolt_whose_places_the_runner_holds_ended_reads_each_unit_merged(self):
        """bolt-plan "A landing held for the runner": Flume landed x's a and b on x and tidied their places, holding each
        record for the runner, which carries them as their status (tests/py/flume-0.20.0/landed-held.json), a at
        1111111 and b at 2222222, x's head b's landing; y, started, runs on deneb. crew bolts reads x at deneb, in the stream
        the held records name, waiting to land, each of a and b merged on a line naming its place, and no line saying a
        landing on its bolt names it."""
        from facts import crew_read, launched, madswan_fleet, ran
        fleet = madswan_fleet()
        p, requests = launched(["x", "y"], work=[("a", "x", [], "unit", []), ("b", "x", ["a"], "unit", []), ("y1", "y", [], "unit", [])],
                               fleet=fleet)
        runners = ran({1: "flume-0.20.0/landed-held", 2: "flume-0.20.0/landed-held", 3: "code"}, commits={1: "1" * 40, 2: "2" * 40})
        d = plan.bolts_data(fleet, ["madswan"], [("madswan", "afterthought/crew-state", "abcdef1" + "0" * 33, p)],
                            crew_read(bolts={"x": {"head": "2" * 40}, "y": {}}), {}, runs={"madswan": (requests, runners)})
        out = plan.bolts_text(d).splitlines()
        assert "x  crew  @ deneb, in Flume stream madswan  waits" in out, out
        place = "flume/change--crew-runs-from-its-own-file-alone"
        for u in "ab":
            assert any(line.startswith(f"  {u:<40} {'merged':<12} {place}") for line in out), out
        assert not any("landed on its bolt" in line or "can't be told" in line for line in out)

    def test_a_question_and_sluices_words_are_on_the_pieces_line(self):
        """bolt-plan "A construct that asked" and "Sent back by sluice"."""
        from facts import ran
        out = plan.bolts_text(self.data(ran({1: "stopped-short", 2: "sent-back"})))
        assert f"  {'a':<40} {'needs':<12} flume/change--agent-mode-is-a-layered-setting  asks at code: Head 118ec46 is ready" in out
        assert "code 26/26   flume/change--teams-cross-to-flume-as-their-bolts-land  sent back by sluice: check-full failed" in out


class TestSubmit:
    """bolt-teams "A bolt lands on the user's send alone, carried to the runner as a land" (crew-lands-each-bolt-through-
    flumes-base-place, Decision 1): crew bolt submit is kept as a word and refuses at once, with any arguments, before
    it reads anything, naming the card's send as the way."""

    @pytest.mark.parametrize("args", [[], ["y"], ["y", "z", "--label", "wldn"], ["y", "--excerpt", "Land y."]])
    def test_it_refuses_with_any_arguments_before_anything_is_read(self, monkeypatch, args):
        import crew

        def unread(*a, **k):
            raise AssertionError("a refused submit reads nothing")
        for name in ("locate", "default_label", "drive_entries", "plan_of", "runner_facts"):
            monkeypatch.setattr(plan, name, unread)
        monkeypatch.setattr(crew, "on_machine", unread)
        a = plan.parser().parse_args(["bolt", "submit", *args])
        with pytest.raises(plan.Refusal) as e:
            plan.bolt_submit(FLEET, a)
        who = {0: "a bolt lands on the user's send of its row on its kit's", 1: "y lands on the user's send of its row on its kit's",
               2: "y and z land on the user's send of their rows on their kit's"}[len(a.bolt)]
        assert str(e.value) == plan.submit_refused(a.bolt) == (
            f"crew bolt submit lands nothing: {who} landings card, which crew carries to the runner as a land")

    def test_its_refusal_records_no_act(self):
        assert ("bolt", "submit") not in plan.ACTS


class TestDropOfAStartedBolt:
    """bolt-plan "A bolt is created and dropped through crew" and bolt-teams "A bolt's drop drops its base place last"
    (crew-lands-each-bolt-through-flumes-base-place, Decision 8): the drop's own commit drops each piece's launch and
    then the bolt's, and the drop asks nothing of sluice or any host for its branch, sweeping only what its units made
    where its work ran."""

    def started(self):
        w = TestStart().write(TestStart.BOLT + TestStart.PIECE)
        w.plan.bolt("console-pages").set("Path", "flume")
        return w

    def test_its_commit_drops_the_pieces_and_then_the_base_place(self, monkeypatch):
        monkeypatch.setenv("CREW_AGENT", "chuck")
        w = self.started()
        run(w, 'bolt drop console-pages "Not now."')
        rs = plan.Plan(w.files["requests.rec"]).recs("Request")
        assert [(r.get("Act"), r.get("Work"), r.get("Of")) for r in rs[2:]] == [("drop", "unit/a-console-page", "2"),
                                                                                 ("drop", "bolt/console-pages", "1")]

    def test_after_it_nothing_is_asked_of_any_host(self, monkeypatch, capsys):
        """bolt-plan "The drop's host does not answer": what follows the drop's write reaches no host, and says nothing
        of the branch of a bolt with a base place, which Flume tidies."""
        import crew
        monkeypatch.setenv("CREW_AGENT", "chuck")
        monkeypatch.setattr(crew, "on_machine", lambda *a, **k: pytest.fail(f"the drop reached a host: {a[1:]}"))
        monkeypatch.setattr(plan, "host_run", lambda *a, **k: pytest.fail(f"the drop reached a host: {a[1:]}"))
        w = self.started()
        op = plan.op_bolt_drop(known(w), plan.do_args("wldn", 'bolt drop console-pages "Not now."'))
        op.change(w)
        op.after("WilldanGroup/crew-state", "a" * 40)
        assert capsys.readouterr().out == ""
