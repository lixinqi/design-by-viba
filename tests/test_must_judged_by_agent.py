"""must_judged_by_agent: which rules an agent judges, which a program judges.

The rule set's trait answers true when an agent must judge a rule, false when
`must_judged_by_agent_impl` lists it as a program's. The test reads the table out
of `must_judged_by_agent_impl.viba.md`, then asks the trait about every rule in
`rules.viba.md` three ways: the leaf type, the variant payload as `Rule` spells
it (the leaf plus its hint — one type, now that a hint block is the product's
unit), and the implementation directly. It also asks a few types outside the
rule set: none is in the table, so every one defaults to true.

    VIBA_ROOT=../viba python3 tests/test_must_judged_by_agent.py
"""

import os
import re
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VIBA_ROOT = Path(os.environ.get("VIBA_ROOT", str(REPO.parent / "viba"))).resolve()
sys.path.insert(0, str(VIBA_ROOT))
sys.path.insert(0, str(VIBA_ROOT / "tests"))

from interpreter_support import Host, is_ok, value_of
from viba import markdown
from viba.interpret import interpret

PASS = 0
FAIL = 0


def check(ok: bool, label: str) -> None:
    global PASS, FAIL
    if ok:
        PASS += 1
    else:
        FAIL += 1
        print(f"FAIL: {label}")


def rules_of():
    """(type name, the hint `Rule` spells on that variant) for every rule."""
    body = dict(markdown.files_of((REPO / "rules.viba.md").read_text()))["types.viba"]
    return re.findall(r"^  \| \$\w+ \((\w+) \* \{ (.*?) \}\)$", body, re.M)


def table_of():
    """The rule types `must_judged_by_agent_impl` answers false for."""
    text = (REPO / "must_judged_by_agent_impl.viba.md").read_text()
    return re.findall(r"^pattern rules\.(\w+)$", text, re.M)


def ask(expr: str, label: str, want: bool) -> None:
    """One question, asked from a design of its own."""
    with tempfile.TemporaryDirectory(prefix="design-by-viba-") as scratch:
        source = (
            "import must_judged_by_agent_impl as table\n"
            "import rule_tools.trait as tools\n"
            "import rules.types as rules\n\n"
            "__decl__ = Any <- $env Env\n\n"
            f"__impl__ = {expr}\n"
        )
        path = Path(scratch) / "ask.viba"
        path.write_text(source)
        result = interpret(str(path), Host().environ(
            viba_path=os.pathsep.join([str(REPO), scratch])))
        got = value_of(result) if is_ok(result) else None
        check(got is want, f"{label} -> {want}: {got!r}")


def run() -> int:
    rules = rules_of()
    table = table_of()
    names = [name for name, _ in rules]

    check(len(rules) == 55, f"55 rules in Rule: {len(rules)}")
    check(len(table) == 19, f"19 rules in the table: {len(table)}")
    check(len(set(names)) == len(names), "one entry per rule type")
    check(set(table) <= set(names), f"table names are rule types: {set(table) - set(names)}")

    for name, hint in rules:
        want = name not in table
        ask(f"tools.must_judged_by_agent[rules.{name}]", f"leaf {name}", want)
        ask(f"tools.must_judged_by_agent[rules.{name} * {{ {hint} }}]",
            f"payload {name}", want)
        ask(f"table[rules.{name}].value", f"impl {name}", want)

    for source in ("int", "str", "list[int]", "rules.Rule", "rules.Finding",
                   "rules.Position"):
        ask(f"tools.must_judged_by_agent[{source}]", f"default {source}", True)

    print(f"must_judged_by_agent: {PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(run())
