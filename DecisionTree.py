"""
"""
from __future__ import annotations

import csv
import random
from typing import Any, Optional

from GenerateGraph import filter_genre

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


    def insert_sequence(self, items: list) -> None:
        # !! Edit docstring (exercise 2 template)
        """Insert the given items into this tree. 

        The inserted items form a chain of descendants, where:
            - items[0] is a child of this tree's root
            - items[1] is a child of items[0]
            - items[2] is a child of items[1]
            - etc.

        Do nothing if items is empty.

        The root of this chain (i.e. items[0]) should be added as a new subtree within this tree, as long as items[0]
        does not already exist as a child of the current root node. That is, create a new subtree for it
        and append it to this tree's existing list of subtrees.

        If items[0] is already a child of this tree's root, instead recurse into that existing subtree rather
        than create a new subtree with items[0]. If there are multiple occurrences of items[0] within this tree's
        children, pick the left-most subtree with root value items[0] to recurse into.
        """
        if len(items) > 0:
            first_item = items[0]
            for subtree in self._subtrees:
                if subtree._root == first_item:
                    subtree.insert_sequence(items[1:])
                    return
            new_tree = create_tree(items)
            self._subtrees.append(new_tree)

    def traverse_tree(self, inputs: list) -> list:
        """
        Traverse through the tree by going to the subtree with the closest value to the first input.
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
            return closest_tree.traverse_tree(inputs[1:])
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

def build_decision_tree() -> SongDecisionTree:
    """Build a decision tree.
    """
    tree = SongDecisionTree('', [])  # The start of a decision tree
    count = 0
    with open('datasets/kaggle_spotify_songs_1.csv') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skip the header row
        
        for row in reader:
            count += 1

            values = [row[8], row[9], row[10],
                row[11], row[12], row[13], row[14], row[15], row[16],
                row[17], row[18]]
            values = list(map(float, values))
            values.append(filter_genre(row[20]))
            values.append(row[1])
            tree.insert_sequence(values)

            if count == 10: # limit
                return tree
    return tree


if __name__ == '__main__':
    decision_tree = build_decision_tree()
    inputs = [0.665,0.185,1,-13.852,1,0.0381,0.913,0.0,0.334,0.458,82.474,'acoustic'] # 1RZkqIEM5aV000fKgz9J46
    # inputs = [0.676,0.461,1,-6.746,0,0.143,0.0322,1.01e-06,0.358,0.715,87.917,'acoustic'] # 5SuOikwiRyPMVoIQDJUgSV
    inputs = [0.534,0.26,1,-12.406,1,0.0319,0.834,0.00405,0.102,0.151,113.877,'acoustic'] # 4ujYTGqbiV5xl97Pqoctq2

    print(inputs)
        
    results = decision_tree.traverse_tree(inputs)
    print(results)
