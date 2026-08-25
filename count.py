#!/usr/bin/env python3
"""Parse formula.txt and count symbols from its abstract syntax tree."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


RESERVED = frozenset("()¬∧∃∈=")


@dataclass(frozen=True)
class Formula:
    kind: str
    parts: tuple[object, ...]


class ParseError(ValueError):
    """Raised when the input is not a formula in the declared grammar."""


def is_variable(char: str) -> bool:
    """Variables are single non-whitespace symbols not reserved by the grammar."""
    return len(char) == 1 and not char.isspace() and char not in RESERVED


def require(text: str, index: int, expected: str) -> int:
    if index >= len(text) or text[index] != expected:
        found = "end of input" if index >= len(text) else repr(text[index])
        raise ParseError(f"expected {expected!r} at offset {index}, found {found}")
    return index + 1


def parse_at(text: str, index: int = 0) -> tuple[Formula, int]:
    if index >= len(text):
        raise ParseError(f"expected a formula at offset {index}")

    char = text[index]

    # Existential formula: ∃v(phi)
    if char == "∃":
        if index + 1 >= len(text) or not is_variable(text[index + 1]):
            raise ParseError(f"expected a one-symbol variable at offset {index + 1}")
        variable = text[index + 1]
        cursor = require(text, index + 2, "(")
        child, cursor = parse_at(text, cursor)
        cursor = require(text, cursor, ")")
        return Formula("exists", (variable, child)), cursor

    # Parenthesized negation: (¬phi), or conjunction: (phi∧psi)
    if char == "(":
        if index + 1 < len(text) and text[index + 1] == "¬":
            child, cursor = parse_at(text, index + 2)
            cursor = require(text, cursor, ")")
            return Formula("not", (child,)), cursor

        left, cursor = parse_at(text, index + 1)
        cursor = require(text, cursor, "∧")
        right, cursor = parse_at(text, cursor)
        cursor = require(text, cursor, ")")
        return Formula("and", (left, right)), cursor

    # Atomic formula: v∈w or v=w
    if not is_variable(char):
        raise ParseError(f"expected a variable or formula constructor at offset {index}")
    if index + 2 >= len(text) or text[index + 1] not in "∈=":
        raise ParseError(f"expected ∈ or = after the variable at offset {index}")
    if not is_variable(text[index + 2]):
        raise ParseError(f"expected a one-symbol variable at offset {index + 2}")
    return Formula("atom", (char, text[index + 1], text[index + 2])), index + 3


def parse(text: str) -> Formula:
    if any(char.isspace() for char in text):
        raise ParseError("the canonical string must not contain whitespace")
    tree, cursor = parse_at(text)
    if cursor != len(text):
        raise ParseError(f"unexpected trailing input at offset {cursor}")
    return tree


def serialize(tree: Formula) -> str:
    if tree.kind == "atom":
        left, relation, right = tree.parts
        return f"{left}{relation}{right}"
    if tree.kind == "not":
        (child,) = tree.parts
        return f"(¬{serialize(child)})"
    if tree.kind == "and":
        left, right = tree.parts
        return f"({serialize(left)}∧{serialize(right)})"
    if tree.kind == "exists":
        variable, child = tree.parts
        return f"∃{variable}({serialize(child)})"
    raise AssertionError(f"unknown node kind: {tree.kind}")


def recursive_size(tree: Formula) -> int:
    """Count one symbol per variable, connective, relation, and parenthesis."""
    if tree.kind == "atom":
        return 3
    if tree.kind == "not":
        (child,) = tree.parts
        return 3 + recursive_size(child)  # (, ¬, )
    if tree.kind == "and":
        left, right = tree.parts
        return 3 + recursive_size(left) + recursive_size(right)  # (, ∧, )
    if tree.kind == "exists":
        _, child = tree.parts
        return 4 + recursive_size(child)  # ∃, variable, (, )
    raise AssertionError(f"unknown node kind: {tree.kind}")


def node_counts(tree: Formula) -> Counter[str]:
    counts = Counter([tree.kind])
    for part in tree.parts:
        if isinstance(part, Formula):
            counts.update(node_counts(part))
    return counts


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    default_formula = Path(__file__).with_name("formula.txt")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("formula", nargs="?", type=Path, default=default_formula)
    args = parser.parse_args()

    text = args.formula.read_text(encoding="utf-8").strip()
    tree = parse(text)
    canonical = serialize(tree)
    if canonical != text:
        raise ParseError("input parses but is not in canonical form")

    counts = node_counts(tree)
    contributions = {
        "atoms": counts["atom"] * 3,
        "conjunctions": counts["and"] * 3,
        "negations": counts["not"] * 3,
        "existentials": counts["exists"] * 4,
    }
    recursive = recursive_size(tree)

    print(f"formula: {text}")
    print(f"raw symbols: {len(text)}")
    print(f"recursive symbols: {recursive}")
    print("breakdown:")
    print(f"  atoms:        {counts['atom']:2} x 3 = {contributions['atoms']:2}")
    print(f"  conjunctions: {counts['and']:2} x 3 = {contributions['conjunctions']:2}")
    print(f"  negations:    {counts['not']:2} x 3 = {contributions['negations']:2}")
    print(f"  existentials: {counts['exists']:2} x 4 = {contributions['existentials']:2}")
    print(f"  total:                 {sum(contributions.values()):2}")
    print("canonical round-trip: ok")

    if len(text) != recursive or recursive != sum(contributions.values()):
        raise AssertionError("the raw, recursive, and component counts disagree")


if __name__ == "__main__":
    main()
