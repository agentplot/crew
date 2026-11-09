"""Nothing of crew's runs a tool for a bolt (crew-lands-each-bolt-through-flumes-base-place, Decision 1; record 0056
point 1): in every command crew's code runs, read from its source and never from a docstring or a comment, no sluice
command, `wt submit`, `wt merge`, `wt remove`, `gh` or `read-tree` is found, in any function, since a card's preview is
asked of the runner too (a-cards-preview-is-asked-of-the-runner, Decision 9), so a new caller of sluice fails this
case. A command crew runs is each argument list a function hands a runner, subprocess, crew.on_machine, host_run,
gather.run, kit_git or crew_argv, and each script constant of the module handed one, bare or through a wrapper, its
value a string the module builds from literals and other such constants. plugin/bin/crew is read line by line, its
comments left out. That no stub logs such a call on a bolt's run is t-journey-land's."""
import ast
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
MODULES = ["plugin/lib/plan.py", "plugin/lib/gather.py", "plugin/lib/kit.py", "plugin/lib/board.py", "plugin/lib/runner.py"]
# A tool named as a command in a script: sluice or gh as a command word, wt with submit, merge or remove among its words
# before the command ends, or git's read-tree.
TOOL = re.compile(r"(?:^|[\s;|&(`$\"'])(?:sluice(?=\s|$)|gh(?=\s|$)|wt\b[^\n;|&]*\b(?:submit|merge|remove)\b)|read-tree\b")
# The calls crew runs a command through, each by the name it is called by.
RUNNERS = {"run", "Popen", "check_output", "check_call", "call", "on_machine", "host_run", "kit_git", "crew_argv"}


def constants(tree):
    """Each module-level string constant, built from literals and other such constants by +."""
    out = {}

    def value(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        if isinstance(node, ast.Name) and node.id in out:
            return out[node.id]
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            a, b = value(node.left), value(node.right)
            return a + b if a is not None and b is not None else None
        return None
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            v = value(n.value)
            if v is not None:
                out[n.targets[0].id] = v
    return out


def literal(node):
    """A list or tuple element's text: a string, or an f-string's literal parts with each value as {}."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(str(v.value) if isinstance(v, ast.Constant) else "{}" for v in node.values)
    return None


def words(seq):
    """A list's or tuple's literal words, in order, each value not a literal left out."""
    return [w for w in (literal(e) for e in seq.elts) if w is not None]


def runs_tool(ws):
    """Whether a command's words run a tool for a bolt: sluice or gh as its program, wt with submit, merge or remove
    among its words, read-tree among them, or a script among them that names one (TOOL)."""
    if not ws:
        return False
    return (ws[0] in ("sluice", "gh") or (ws[0] == "wt" and bool({"submit", "merge", "remove"} & set(ws))) or "read-tree" in ws
            or any(TOOL.search(w) for w in ws if "\n" in w or " " in w))


def run_strings(path):
    """Each command a module's functions run, as (the function, its words): each argument list it hands a runner
    (RUNNERS), and each script constant handed one, as one word."""
    tree = ast.parse((ROOT / path).read_text())
    consts = constants(tree)
    out = []
    for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        for n in ast.walk(fn):
            if not (isinstance(n, ast.Call) and (getattr(n.func, "id", None) or getattr(n.func, "attr", None)) in RUNNERS):
                continue
            for a in n.args:
                if isinstance(a, (ast.List, ast.Tuple)):
                    out.append((fn.name, words(a)))
                for m in ast.walk(a):  # a script constant handed it, bare or through a wrapper such as fetch_told
                    if isinstance(m, ast.Name) and m.id in consts:
                        out.append((fn.name, [consts[m.id]]))
    return out


@pytest.mark.parametrize("path", MODULES)
def test_no_function_of_a_module_runs_a_tool_for_a_bolt(path):
    found = sorted({(fn, " ".join(ws)[:80]) for fn, ws in run_strings(path) if runs_tool(ws)})
    assert found == [], f"{path} runs a tool for a bolt: {found}"


def test_the_crew_command_runs_no_tool_for_a_bolt():
    lines = [(i, l) for i, l in enumerate((ROOT / "plugin/bin/crew").read_text().splitlines(), 1) if not l.lstrip().startswith("#")]
    found = [(i, l.strip()) for i, l in lines if TOOL.search(l.split(" # ")[0])]
    assert found == [], found


def test_a_new_caller_of_sluice_would_be_found(tmp_path):
    """The case reads what it should: a function running sluice, wt's remove or git's read-tree from a list, or a
    script naming one, is found, a preview function's among them; a file's name or words about sluice are not."""
    landing = "sluice " + "submit main --no-wait --json"  # spelled apart, as a tool's guard reads commands it is shown
    src = (f'X = "cd \\"$1\\" && {landing}"\n'
           'WORDS = "the merge queue is sluice\'s, and its file .config/sluice.toml"\n'
           "def submit(): host_run(fleet, h, fetch_told(fleet, h, main, X), main)\n"
           "def land(): subprocess.run(['sluice', 'branch', 'delete'])\n"
           "def tidy(): subprocess.run(['wt', '-C', main, 'remove', path])\n"
           "def level(): kit_git(fleet, t, main, ['git', 'read-tree', '-m', '-u', 'HEAD'])\n"
           "def said(): print(WORDS, ['sluice', 'gh'])\n"
           "def card_preview(): subprocess.run(['sluice', 'preview', branch, revision, '--json'])\n")
    (tmp_path / "case.py").write_text(src)
    got = run_strings(tmp_path / "case.py")  # an absolute path, which ROOT / it leaves as it is
    assert sorted(fn for fn, ws in got if runs_tool(ws)) == ["card_preview", "land", "level", "submit", "tidy"], got
