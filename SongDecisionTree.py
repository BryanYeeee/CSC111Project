"""
A module that contains the SongDecisionTree class, which represents a decision tree with each level containing values
for a feature of the song's characteristics.
"""
from __future__ import annotations

import random
from typing import Any, Optional

class SongDecisionTree:
    """A decision tree with each level containing values for a feature of the song's characteristics

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[SongDecisionTree]

    def __init__(self, root: Optional[Any], subtrees: list[SongDecisionTree]) -> None:
        """Initialize a new SongDecisionTree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not None or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees


    def insert_song(self, items: list) -> None:
        """Insert the given items into this tree such that each item is the child of the item before it,
        and old subtrees are reused if the same root value is found.
        """
        if len(items) > 0:
            first_item = items[0]
            for subtree in self._subtrees:
                if subtree._root == first_item:
                    subtree.insert_song(items[1:])
                    return
            new_tree = create_tree(items)
            self._subtrees.append(new_tree)

    def find_related_songs(self, inputs: list) -> list:
        """
        Each input in the list is a value for a feature of the song's characteristics.
        Traverse through the tree by going down the path with the closest value to the first input.
        Return the leaf nodes when there are no more inputs.
        """
        if len(inputs) > 0:
            closest_tree = self._subtrees[random.randint(0, len(self._subtrees) - 1)]
            if not isinstance(closest_tree._root, str):
                for subtree in self._subtrees:
                    if abs(subtree._root - float(inputs[0])) < abs(closest_tree._root - float(inputs[0])):
                        closest_tree = subtree
            else:
                if inputs[0] in self._subtrees:
                    closest_tree = inputs[0]
            return closest_tree.find_related_songs(inputs[1:])
        else:
            return [cur_subtree._root for cur_subtree in self._subtrees]


def create_tree(items: list) -> Optional[SongDecisionTree]:
    """
    Given a list of items, create a decision tree using the first item as the root and the rest as subtrees.
    """
    if len(items) == 1:
        return SongDecisionTree(items[0], [])
    elif len(items) > 0:
        return SongDecisionTree(items[0], [create_tree(items[1:])])
    return None

