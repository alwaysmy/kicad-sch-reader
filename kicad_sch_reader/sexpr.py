"""Minimal, dependency-free S-expression reader for KiCad files.

KiCad schematic/netlist files are s-expressions.  This module intentionally
does not model a generic Lisp type system: everything is either a ``str`` atom
or a ``list`` whose first element is the node head.  Quoted strings are
decoded once during tokenization so callers never need to strip quotes.
"""

from __future__ import annotations

from typing import Iterable, Iterator, List, Optional, Sequence, Union

Node = Union[str, List["Node"]]


def tokenize(text: str) -> List[str]:
    """Tokenize an s-expression source.

    Parentheses are tokens.  Quoted strings honour ``\\"``, ``\\\\``, ``\\n``,
    ``\\t``, ``\\r`` escapes and are returned decoded (without the surrounding
    quotes).  Bare atoms are returned as-is.
    """
    tokens: List[str] = []
    i = 0
    n = len(text)
    escapes = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}
    while i < n:
        c = text[i]
        if c.isspace():
            i += 1
            continue
        if c in "()":
            tokens.append(c)
            i += 1
            continue
        if c == '"':
            i += 1
            buf: List[str] = []
            while i < n:
                c = text[i]
                if c == "\\" and i + 1 < n:
                    nxt = text[i + 1]
                    buf.append(escapes.get(nxt, nxt))
                    i += 2
                    continue
                if c == '"':
                    i += 1
                    break
                buf.append(c)
                i += 1
            tokens.append("".join(buf))
            continue
        j = i
        while j < n and not text[j].isspace() and text[j] not in "()":
            j += 1
        tokens.append(text[i:j])
        i = j
    return tokens


def _parse_from(tokens: Sequence[str], pos: int) -> tuple[Node, int]:
    token = tokens[pos]
    if token != "(":
        return token, pos + 1
    pos += 1
    if pos >= len(tokens):
        raise ValueError("unterminated list")
    head = tokens[pos]
    pos += 1
    body: List[Node] = []
    while pos < len(tokens):
        token = tokens[pos]
        if token == ")":
            return [head] + body, pos + 1
        if token == "(":
            child, pos = _parse_from(tokens, pos)
            body.append(child)
        else:
            body.append(token)
            pos += 1
    raise ValueError("unterminated list")


def parse(text: str) -> List[Node]:
    """Parse an s-expression document containing zero or more top-level forms."""
    tokens = tokenize(text)
    forms: List[Node] = []
    pos = 0
    while pos < len(tokens):
        form, pos = _parse_from(tokens, pos)
        forms.append(form)
    return forms


def is_node(value: Node, name: Optional[str] = None) -> bool:
    if not isinstance(value, list) or not value:
        return False
    return name is None or value[0] == name


def head(value: Node) -> str:
    return str(value[0]) if isinstance(value, list) and value else ""


def children(node: Node, name: Optional[str] = None) -> Iterator[Node]:
    """Yield child nodes.  When *name* is given only matching heads are yielded."""
    if not isinstance(node, list):
        return
    for child in node[1:]:
        if isinstance(child, list) and child and (name is None or child[0] == name):
            yield child


def first(node: Node, name: str) -> Optional[Node]:
    """Return the first child node whose head is *name*, or ``None``."""
    for child in children(node, name):
        return child
    return None


def find_all(root: Iterable[Node], name: str) -> Iterator[Node]:
    """Yield every descendant (including *root*) whose head matches *name*."""
    stack = list(root)
    while stack:
        node = stack.pop(0)
        if not isinstance(node, list) or not node:
            continue
        if node[0] == name:
            yield node
        stack.extend(node[1:])


def atom_text(value: Node) -> str:
    """Return a node/atom as text (already unquoted by the tokenizer)."""
    return value if isinstance(value, str) else (head(value) if value else "")


def to_float(value: Node, default: float = 0.0) -> float:
    try:
        return float(atom_text(value))
    except (TypeError, ValueError):
        return default


def to_int(value: Node, default: int = 0) -> int:
    try:
        return int(float(atom_text(value)))
    except (TypeError, ValueError):
        return default


def xy(node: Node) -> tuple[float, float, float]:
    """Interpret an ``(at x y [rotation])`` node; missing fields default to 0."""
    x = to_float(node[1]) if len(node) > 1 else 0.0
    y = to_float(node[2]) if len(node) > 2 else 0.0
    r = to_float(node[3]) if len(node) > 3 else 0.0
    return x, y, r


def pair_xy(node: Node) -> tuple[float, float]:
    """Interpret an ``(xy x y)`` node."""
    return (to_float(node[1]), to_float(node[2])) if len(node) > 2 else (0.0, 0.0)


def prop(node: Node, name: str, default: str = "") -> str:
    """Return a ``(name value ...)`` child's value."""
    item = first(node, name)
    return atom_text(item[1]) if item is not None and len(item) > 1 else default
