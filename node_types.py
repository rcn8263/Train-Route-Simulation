""" 
file: node_types.py
description: type definitions for immutable and mutable linked sequences
author: RIT CS
"""

from typing import Any, Union
from dataclasses import dataclass


@dataclass(frozen=True)
class FrozenNode:
    """
    An immutable link node containing a value and a link to the next node
    """
    value: Any
    next: Union['FrozenNode', None]


@dataclass(frozen=False)
class MutableNode:
    """
    A mutable link node containing a value and a link to the next node
    """
    value: Any
    next: Union['MutableNode', None]