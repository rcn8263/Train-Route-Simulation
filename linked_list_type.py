""" 
file: linked_list_type.py
description: type definitions for mutable linked list construction
author: RIT CS
"""

from typing import Union
from dataclasses import dataclass
from node_types import MutableNode

@dataclass(frozen=False)
class LinkedList:
    """
    For mutable linked lists, we 'encapsulate' the list nodes in a wrapper
    class. This will allow functions that work with mutable lists to not
    worry about whether the list is empty or not. An empty list is still an
    instance of this LinkedList class; it's just that its head is None.
    The size of the list is stored here, too, as an example of the tradeoff
    between computing something every time you need it and using extra
    memory to store the value so that it does not have to be recomputed.
    """
    head: Union[MutableNode, None] = None
    size: int = 0
