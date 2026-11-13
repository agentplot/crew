# Design

## Context

**What the briefs say now.** The design agent's brief (`plugin/roles/design.md`) tells it to:
- record "something" whenever a design talk settles it (*Talking design with the user*), whatever kind of thing that is;
- quote the user's words in the record as their decision (*Decision records*, its first paragraph and its bullet *The user's own words*);
- quote any note the user added to an acceptance, and set a rejection "with the user's words" (bullets *Yes* and *No*);
- raise a card at its start for every proposed record or amendment that has none open, whatever it holds.

Nothing in the brief separates how a tool is built from what the plan holds.

**What it cost.**
- Sluice's record 0117 was amended on 2026-11-12 to freeze fixes on main until a rebuild and a redesign land, and the user was asked to accept that as a record. The user said that is not what a record is for (signal `2026-11-13-agentplot-planner-ca38ed28/01` on afterthought/crew-state `agentplot/main`).
- Crew's record 0060 was amended to carry a drive's queue. That amendment was taken out on the user's card (375083fb).
- The user does not want their own words going into records as the decision (signal `2026-11-13-agentplot-design-3d529768/01`, whose move challenges *Decision records*). Until the brief changes, agentplot-design follows the rule by its own reading.

**The rule.** `briefs.15`, as amended on 2026-11-13 (2b6422de), says:
- A record holds only how a tool is built or how it behaves.
- An order of work, a priority, a freeze, a schedule or a trial, which bolt or unit carries something, and how a one-off move, rename or carry-over is carried out belong to the plan. The design agent tells them to the planner, or to ops for a live system, and records none of them.
- A unit cites only records of architecture.
- A record states each decision in its own words. A decision the user settled has a deciders line naming where and when they settled it.

This change brings the briefs in line with that rule. No rule changes, so no page of `docs/architecture/` is edited (`docs.7`).

**The family.** Every tool's records are written by its drive's design agent, under this brief, so one brief change covers sluice's, Flume's and Boomdrive's records as well as crew's. No other tool writes decision records or holds a brief for them. The constitution skill, which any agent uses to start a kit's records, is crew's too.

**Area pages this change touches:**
- `briefs.md`: `briefs.4`, `briefs.5`, `briefs.11`, `briefs.15`.
- `tests.md`: `tests.6`, `tests.10`.
- `docs.md`: `docs.1`, `docs.7`.
- `core.md`: `roles.1`, `roles.3`, `roles.6`, `code.8`.

## Goals / Non-Goals

**Goals:**
- The design agent's brief says once what a record holds and where a plan matter goes, and each of its sections follows that.
- A record states each decision in its own words, and a decision the user settled has a deciders line naming where and when they settled it.
- The planner's brief has a unit cite only records of how a tool is built, and carries a plan matter in the plan.
- `tests/t-briefs.sh` pins each new rule with a phrase and refuses each old one (`tests.6`).

**Non-Goals:**
- A check in crew that refuses a record of a plan matter (Decision 5).
- Rewriting records already on a kit's main. Only a *proposed* record or amendment that holds a plan matter is taken out, when the design agent next starts (Decision 3). An accepted record stays as it is until the design agent amends it under the new brief.
- Any change to `crew record`, its card, or its transcript check.

## Decisions

### 1. The line is drawn once, in *Decision records*, and every other section follows it

*Decision records* opens with what a record holds and what belongs to the plan, in `briefs.15`'s own list:
- an order of work, a priority, a freeze, a schedule or a trial;
- which bolt or unit carries something;
- how a one-off move, rename or carry-over is carried out.

A plan matter is told to the planner, or to main-level ops when it moves a live system, with no record, no amendment and no card. The other sections point at this paragraph rather than repeat it:
- *Elaboration on main*: a record holds only how a tool is built or behaves.
- *Talking design with the user*: a talk that settles how a tool is built is recorded; one that settles a plan matter is told to the planner or ops.
- *Answering a design question*: a question about a plan matter is no design question, so nothing is recorded.
- *Queuing work*: `--source` names a record of how the tool is built.

Not taken: a section of its own for plan matters. The decision about whether to write a record is made in *Decision records*, so the line belongs there. A separate section would be one more place for the two to drift apart.

### 2. A plan matter the user settled reaches the planner as a signal of their words

The user's words are still kept, but in the place built for them. When the user settles a plan matter, the design agent:
- records their words as a signal, as *Talking design with the user* already has it do for "a need somewhere else";
- tells the planner, or ops, in one line naming that signal.

This keeps three things true:
- `roles.6`: a message names the record to read and carries no fact to act on blindly.
- `briefs.15`: the user's words are kept, but not in a decision record. A signal is no decision record.
- The planner routes signals already (`--signal` on a proposal's `unit add` and `chore add`), so a plan matter reaches the plan by the path it already has.

A plan matter that the design agent finds itself, in a question or a reading, needs no signal: its tell names what brought it.

Not taken: a tell carrying the user's words with no signal. The words would live only in a message, which `briefs.15`'s details rule out ("a decision that lives only in a message").

### 3. A proposed record or amendment of a plan matter raises no card at the start

At its start the design agent runs `crew record … --proposed` for each proposed record or amendment on its kits' main that has no card open. Under the new brief, one that holds only a plan matter raises no card. The design agent:
- takes it out of the kit's main in a commit, submitted through sluice as any record is (`state.3`);
- tells the planner or ops, as Decision 2 says.

This is what was done by hand for record 0060's amendment (375083fb). Without it, the start loop would put the next such amendment to the user as a record, which `briefs.15`'s details rule out ("a card asking the user to accept one").

Only a proposed record or amendment is taken out, since the user has not accepted it. An accepted record that holds a plan matter changes only when the design agent amends it, which then goes through *Decision records* as any amendment does.

### 4. A record states each decision in its own words

Each place the brief quotes the user into a record now states the decision in the record's own words:

| Where in the brief | Now |
|---|---|
| A decision the user settled (first paragraph and the bullet *The user's own words*, retitled *What the user settled*) | The deciders line names the user and where and when they settled it, quoting none of their words |
| *Yes* bullet | The user's note is stated in the record's own words |
| *No* bullet | The record says why the user said no, in its own words, and where they said it |
| A choice of the user's alone | The record says where the user gave their yes, in the pane or on its card |

`crew record --settled-in-pane --excerpt` still takes the user's yes word for word. Those words are the evidence crew reads in the design agent's transcript as the user's (`signals.5`), and crew records that check by naming the transcript record, never the words (main-level "A record's card is raised unless it was settled in the pane"). The brief says so, so the agent does not take the excerpt as wording for the record.

Not taken: a record that quotes the user only in its *Context*. The user asked for none of their words in records (signal `3d529768/01`). A *Context* section that quotes them would just move the quote somewhere else.

### 5. No check refuses a record of a plan matter

`roles.3` asks for a check when an agent breaks a rule its brief already states. Until this change, the brief said the opposite. So this change only corrects the brief.

A later check could look only at a record's words, its title, deciders line or decision, to tell how a tool is built from what the plan holds. The family's principle 16 rules that out: no check reads Markdown (agentplot/blueprints `design/principles.md`, as `docs.7`'s details cite it). If the design agent writes a plan matter into a record under the new brief, the place to catch it is the user's answer on the record's card, or the reviewer's reading. A check of crew's would have to read the record's prose to do it.

Not taken: a refusal in `crew record` based on words in a record's title.

### 6. The planner's brief carries the other half

A plan matter now arrives at the planner, so the planner's brief says what to do with it:
- **The intent paragraph**: `--source` names only records of how a tool is built or behaves.
- **A new paragraph after it**: a plan matter, whoever settles it, the user included, is carried in the plan, by a proposal where it changes the plan. The planner never asks the design agent for a record of one and never cites one as a unit's source.

Main-level ops's brief is not changed. It already takes every live system, and the design agent's tell names the signal behind it. Not taken: a sentence in `main-ops.md` naming carry-overs. It would add nothing ops does not already do with a tell about a live system.

### 7. The constitution skill says the same of a kit's records

`plugin/skills/constitution/SKILL.md` has an agent start a kit's `docs/adr/` in MADR form, with a `decision-makers` field. One sentence after its MADR line says:
- a record holds only how the kit is built or behaves;
- it states each decision in its own words, its `decision-makers` naming who settled it without quoting them;
- a plan matter gets no record.

`tests/t-docs.sh` pins it. That test already reads `plugin/skills/`.

### 8. Fixtures keep their records

`tests/t-cards.sh` and `tests/py/test_cards.py` hold fixture records whose deciders line quotes "no fleet". Crew reads a record's status and puts the record whole on its card, and reads nothing of its deciders line. So those fixtures prove nothing about the rule this change concerns, and rewriting them changes no outcome. They are left as they are.

### Rules relied on

- `briefs.15`: the rule this change brings the briefs to.
- `briefs.5`: an intent names the outcome and the records that govern it. Here those are records of how a tool is built.
- `briefs.4`, `briefs.11`: a record's card is crew's, raised through `crew record`. Its form is unchanged.
- `roles.1`: the plan changes only by a proposal the user approves, so a plan matter reaches the plan through the planner.
- `roles.3`: a check follows a broken rule the brief already stated. None did (Decision 5).
- `roles.6`: a tell names the record behind it. Here that record is the signal (Decision 2).
- `signals.5`: the excerpt is crew's evidence of the user's yes.
- `docs.1`, `docs.7`: records and rules are the design agent's. This change edits neither.
- `tests.6`: every rule a brief carries is pinned in `t-briefs.sh`.
- `tests.10`: neither test reads a new path, so `tests/moon.yml` is unchanged.
- `code.8`: no modelled shape changes.

### Departures

- From `openspec/config.yaml`'s tasks rule that the last task runs `tests/suite --affected`: this change has no such task. The stage's brief gives the verify stage the repository's whole checks, after every task, and has no task check every part the change touches. Each task names its one test instead.

## Risks / Trade-offs

- **[A decision is both architecture and a plan matter]**, such as a freeze that also changes how a merge queue behaves → the brief records the architecture and tells the planner the plan matter. Each half goes where it belongs, and the record does not say when its work happens.
- **[The design agent strips a plan matter that is actually architecture]** → the user sees the planner's proposal or ops's step and can say so. A missing record can be written later at no cost, while a plan matter put to the user as a record has already cost them a card.

## Migration Plan

None. A design agent loads its brief at its start (`teams.19`), so the new words reach each drive's design agent at its next start after the landing reaches its host. Proposed records of a plan matter are taken out then (Decision 3).

## After deploy

None. Each rule here is a phrase `tests/t-briefs.sh` or `tests/t-docs.sh` checks, and nothing waits on a host or on the user.

## Task notes

**1.1** `plugin/roles/design.md`, *Decision records*. Add a new first paragraph before "Every decision record you write":

> A decision record holds only how a tool is built or how it behaves. An order of work, a priority, a freeze on fixes, a schedule or a trial, which bolt or unit carries something, and how a one-off move, rename or carry-over is carried out are the plan's, whoever settles them, the user included: tell each to `{{PLANNER}}` in one line with `{{TEAM_CMD}} tell`, or to `{{MAIN_OPS}}` when it moves a live system, naming the signal of the user's words when they settled it, as *Talking design with the user* says, and write no record or amendment of it and raise no card for it. A unit you queue cites only records of how a tool is built or behaves.

In `tests/t-briefs.sh`, in the block headed "A decision record is settled by whose decision it is", pin these phrases of the design brief:
- "A decision record holds only how a tool is built or how it behaves"
- "which bolt or unit carries something, and how a one-off move, rename or carry-over is carried out are the plan's, whoever settles them, the user included"
- "or to \`wldn-ops\` when it moves a live system, naming the signal of the user's words when they settled it"
- "write no record or amendment of it and raise no card for it"
- "A unit you queue cites only records of how a tool is built or behaves"

Extend the block's opening comment to say so (`briefs.15` as amended 2026-11-13).

**1.2** `plugin/roles/design.md`, *Decision records*.

The paragraph that now opens "Every decision record you write" becomes:

> Every decision record you write, and every amendment you make to one, states each of its decisions in its own words, never the user's words quoted as the decision, and says which of its decisions is whose, and each is settled its own way. What the user settled, in this pane or relayed by the operator, is theirs: state it in the record's own words, its deciders line naming the user and where and when they settled it, proposed until the user has seen it as a record, …

The rest of that sentence is unchanged. Further on in the paragraph, "and the record says so" becomes "and the record says where they gave it".

The bullets:
- **The user's own words.** Retitle it **What the user settled.** Its first clause becomes: "Where the user settled something, the record states it in its own words and its deciders line names the user and where and when they settled it, quoting none of their words;" The rest of the bullet is unchanged.
- **Yes.** "quoting any note they added in their own words" becomes "stating any note they added in the record's own words".
- **No.** "set \`status: rejected\` with the user's words" becomes "set \`status: rejected\` with why, in the record's own words, and where the user said no".

In the second paragraph, after "quoting their yes whole, with the record's number when they named it", add: "; those words are crew's evidence and go into no record".

In `tests/t-briefs.sh`'s same block:
- Replace the pin "record it with those words quoted as its deciders" with "state it in the record's own words, its deciders line naming the user and where and when they settled it".
- Replace "the record's deciders line quotes those words as the user's decision" with "its deciders line names the user and where and when they settled it, quoting none of their words".
- Replace "and the record says so" with "and the record says where they gave it".
- Replace "set \`status: rejected\` with the user's words" with "set \`status: rejected\` with why, in the record's own words, and where the user said no".
- Pin "states each of its decisions in its own words, never the user's words quoted as the decision", "stating any note they added in the record's own words" and "those words are crew's evidence and go into no record".
- Add a `lacks` for each old phrase: "record it with those words quoted as its deciders", "quotes those words as the user's decision", "quoting any note they added in their own words" and "with the user's words, and take out".

**1.3** `plugin/roles/design.md`, *Decision records*, the paragraph "At your start". After "unless the user settled it in the pane or it says it waits on another record's answer.", add:

> A proposed record or amendment that holds only a plan matter gets no card: take it out of the kit's main in a commit, submitted as any record is, and tell the planner, or ops for a live system, as above.

Pin "A proposed record or amendment that holds only a plan matter gets no card" and "take it out of the kit's main in a commit, submitted as any record is" in `tests/t-briefs.sh`'s same block.

**1.4** `plugin/roles/design.md`, the other sections:

- **Elaboration on main**, the paragraph's last sentence becomes: "A record holds only how a tool is built or behaves, states each decision in its own words and says whose each of its decisions is, and a choice of the user's alone in it is proposed until they accept it, as *Decision records* says."
- **Talking design with the user**, its first paragraph becomes:

  > The user comes to this pane to think a design through with you. When the talk settles how a tool is built or how it behaves, record it and commit: the record states the decision in its own words, is told to them by number and commit, and goes to them on a card only for a choice that is theirs alone, as *Decision records* says. If it changes what a bolt in flight should build, tell the planner in one line. When the talk settles an order of work, a priority, a freeze, a schedule or a carry-over, it is the plan's: record the user's words as a signal, as below, tell `{{PLANNER}}`, or `{{MAIN_OPS}}` for a live system, in one line naming the signal, and write no decision record of it.

- **Answering a design question**, after its first paragraph's last sentence, add: "A question of an order of work, a priority, a freeze, a schedule or a carry-over is no design question: tell whoever brought it that it is the plan's, `{{PLANNER}}`'s or, for a live system, `{{MAIN_OPS}}`'s, and record nothing."
- **Queuing work**: `--source <the page or decision record it comes from>` becomes `--source <the page or decision record of how the tool is built that it comes from>`.

In `tests/t-briefs.sh`, in the block that pins "quotes the user's words as their decision" for the design brief (the one ending "names a rule-decided choice, accepts a record only on the user's yes and queues nothing before"):
- Replace that pin with "the record states the decision in its own words, is told to them by number and commit".
- Pin "When the talk settles an order of work, a priority, a freeze, a schedule or a carry-over, it is the plan's", "in one line naming the signal, and write no decision record of it", "A record holds only how a tool is built or behaves, states each decision in its own words", "is no design question: tell whoever brought it that it is the plan's, \`wldn-planner\`'s or, for a live system, \`wldn-ops\`'s, and record nothing" and "decision record of how the tool is built that it comes from".
- Add a `lacks` for "quotes the user's words as their decision".

**2.1** `plugin/roles/planner.md`, *Proposals*:
- The paragraph **An intent names the outcome and the records that govern it**: after "name the records with \`--source\`", add ", only records of how a tool is built or behaves".
- After that paragraph, add:

  > **An order of work, a priority, a freeze, a schedule or a carry-over is the plan's**, whoever settles it, the user included: the design agent tells it to you, naming the signal of the user's words when they settled it, and writes no decision record of it. Carry it in the plan, by a proposal where it changes the plan, and never ask the design agent for a decision record of it or cite one as a unit's source.

Pin in `tests/t-briefs.sh`, in the planner block that pins "An intent names the outcome and the records that govern it": "name the records with \`--source\`, only records of how a tool is built or behaves", "**An order of work, a priority, a freeze, a schedule or a carry-over is the plan's**", "Carry it in the plan, by a proposal where it changes the plan" and "never ask the design agent for a decision record of it or cite one as a unit's source".

**3.1** `plugin/skills/constitution/SKILL.md`, §3, after the line "ADRs use MADR: … \`0001-record-architecture-decisions.md\` starts the folder.", add:

> A record holds only how the kit is built or behaves, each decision stated in the record's own words and its \`decision-makers\` naming who settled it, never quoting them; an order of work, a priority, a freeze or a carry-over is a plan's and gets no record.

In `tests/t-docs.sh`, read the skill (`$CREW/plugin/skills/constitution/SKILL.md`) and pin "A record holds only how the kit is built or behaves" and "an order of work, a priority, a freeze or a carry-over is a plan's and gets no record". Use a comment that names `briefs.15`, and an `ok` line saying so. The test's `# Reads:` line already names `plugin/skills/`.
