"""Abstract syntax tree node definitions.

The nodes are plain dataclasses; the parser produces them and the compiler
consumes them.  Every node stores the source ``line`` so that diagnostics
point at real code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass
class Node:
    line: int = field(default=0, compare=False)


@dataclass
class Program(Node):
    statements: List[Node] = field(default_factory=list)


# --- expressions ---------------------------------------------------------
@dataclass
class Literal(Node):
    value: Any = None


@dataclass
class Name(Node):
    name: str = ""


@dataclass
class ListExpr(Node):
    items: List[Node] = field(default_factory=list)


@dataclass
class DictExpr(Node):
    """``{"कुंजी": मान, ...}`` — an ordered map literal."""

    keys: List[Node] = field(default_factory=list)
    values: List[Node] = field(default_factory=list)


@dataclass
class Slice(Node):
    """``x[start:stop]`` with either bound optional."""

    target: Optional[Node] = None
    start: Optional[Node] = None
    stop: Optional[Node] = None


@dataclass
class UnaryOp(Node):
    op: str = ""
    operand: Optional[Node] = None


@dataclass
class BinaryOp(Node):
    op: str = ""
    left: Optional[Node] = None
    right: Optional[Node] = None


@dataclass
class Compare(Node):
    op: str = ""
    left: Optional[Node] = None
    right: Optional[Node] = None


@dataclass
class Call(Node):
    callee: str = ""
    args: List[Node] = field(default_factory=list)


@dataclass
class Index(Node):
    target: Optional[Node] = None
    index: Optional[Node] = None


# --- statements ----------------------------------------------------------
@dataclass
class PrintStmt(Node):
    value: Optional[Node] = None


@dataclass
class ExprStmt(Node):
    value: Optional[Node] = None


@dataclass
class LetStmt(Node):
    name: str = ""
    value: Optional[Node] = None


@dataclass
class AssignStmt(Node):
    name: str = ""
    value: Optional[Node] = None
    op: str = "="


@dataclass
class IndexAssignStmt(Node):
    target: Optional[Node] = None
    index: Optional[Node] = None
    value: Optional[Node] = None


@dataclass
class SliceAssignStmt(Node):
    """``x[start:stop] = value`` — replace a slice of a list."""

    target: Optional[Node] = None
    start: Optional[Node] = None
    stop: Optional[Node] = None
    value: Optional[Node] = None


@dataclass
class IfStmt(Node):
    condition: Optional[Node] = None
    body: List[Node] = field(default_factory=list)
    orelse: List[Node] = field(default_factory=list)


@dataclass
class WhileStmt(Node):
    condition: Optional[Node] = None
    body: List[Node] = field(default_factory=list)


@dataclass
class FuncDef(Node):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[Node] = field(default_factory=list)


@dataclass
class TryStmt(Node):
    """``प्रयास … पकड़ नाम … अन्ततः … अन्त``.

    ``handler`` is empty when the user wrote only ``प्रयास``/``अन्ततः`` (the
    fault runs the ``final`` block and then keeps propagating).
    """

    body: List[Node] = field(default_factory=list)
    name: str = "त्रुटि"
    handler: List[Node] = field(default_factory=list)
    final: List[Node] = field(default_factory=list)


@dataclass
class ScopeDecl(Node):
    """``बाह्य नाम`` / ``वैश्विक नाम`` — bind a name in an enclosing scope."""

    kind: str = "nonlocal"      # "nonlocal" | "global"
    names: List[str] = field(default_factory=list)


@dataclass
class RaiseStmt(Node):
    """``उठाओ expr`` — raise a fault carrying a message."""

    value: Optional[Node] = None


@dataclass
class ReturnStmt(Node):
    value: Optional[Node] = None


@dataclass
class BreakStmt(Node):
    pass


@dataclass
class ContinueStmt(Node):
    pass


@dataclass
class PassStmt(Node):
    pass
