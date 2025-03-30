"""
A module that contains the SongDecisionTree class, which represents a decision tree with each level containing values
for a feature of the song's characteristics.
"""
from __future__ import annotations

import random
from typing import Any, Optional


def organize_levels(levels: dict) -> list:
    """
    Given a dictionary of song characteristics and their respective values,
    organize the song characteristics into a list based on the weights of each feature
    (The characteristic corresponding to the larger weight occurs first in the list).
    
    The value of the weights can be seen in SongGraph.py
    
    Preconditions:
    - "genre" in levels
    - "danceability" in levels
    - "energy" in levels
    - "valence" in levels
    - "key" in levels
    - "tempo" in levels
    - "instrumentalness" in levels
    - "mode" in levels
    - "acousticness" in levels
    - "loudness" in levels
    - "liveness" in levels
    - "speechiness" in levels
    """
    return [levels.get("genre"), levels.get("danceability"), levels.get("energy"),
            levels.get("valence"), levels.get("key"), levels.get("tempo"),
            levels.get("instrumentalness"), levels.get("mode"), levels.get("acousticness"),
            levels.get("loudness"), levels.get("liveness"), levels.get("speechiness")]


NODES_PER_LEVEL = organize_levels(
    {
        "danceability": [x * 0.1 for x in range(0, 11)],
        "energy": [x * 0.1 for x in range(0, 11)],
        "key": list(range(0, 12)),
        "loudness": list(range(-10, 0)),
        "mode": [0, 1],
        "speechiness": [x * 0.01 for x in range(0, 11)],
        "acousticness": [x * 0.1 for x in range(7)],
        "instrumentalness": [x * 0.1 for x in range(0, 4)],
        "liveness": [x * 0.1 for x in range(0, 5)],
        "valence": [x * 0.1 for x in range(0, 11)],
        "tempo": [x * 10 for x in range(0, 24)],
        "genre": [
            'world-music', 'country', 'industrial', 'trance', 'club', 'goth', 'piano',
            'comedy', 'techno', 'honky-tonk', 'edm', 'show-tunes', 'happy', 'pagode',
            'children', 'malay', 'party', 'german', 'indie', 'sleep', 'songwriter', 'sad',
            'dubstep', 'disney', 'jazz', 'grindcore', 'new-age', 'salsa', 'study', 'latino',
            'grunge', 'j-dance', 'rock', 'emo', 'classical', 'dance', 'turkish', 'drum-and-bass',
            'indian', 'samba', 'idm', 'mpb', 'hip-hop', 'latin', 'soul', 'alternative', 'electro',
            'french', 'spanish', 'punk', 'tango', 'funk', 'chill', 'r-n-b', 'breakbeat', 'forro',
            'british', 'metal', 'bluegrass', 'guitar', 'sertanejo', 'iranian', 'anime', 'brazil',
            'j-idol', 'folk', 'hardstyle', 'dub', 'gospel', 'groove', 'disco', 'trip-hop', 'opera',
            'blues', 'hardcore', 'electronic', 'reggae', 'dancehall', 'swedish', 'ambient', 'afrobeat',
            'kids', 'acoustic', 'garage', 'house', 'pop', 'ska', 'romance'
        ]
    }
)


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
        if len(inputs) == 0:
            return [cur_subtree._root for cur_subtree in self._subtrees]
        closest_tree = self._subtrees[random.randint(0, len(self._subtrees) - 1)]
        for subtree in self._subtrees:
            if not isinstance(subtree._root, str):
                if abs(subtree._root - float(inputs[0])) < abs(closest_tree._root - float(inputs[0])):
                    closest_tree = subtree
            elif subtree._root == inputs[0]:
                return subtree.find_related_songs(inputs[1:])
        return closest_tree.find_related_songs(inputs[1:])


def create_tree(items: list) -> Optional[SongDecisionTree]:
    """
    Given a list of items, create a decision tree using the first item as the root and the rest as subtrees.
    """
    if len(items) == 1:
        return SongDecisionTree(items[0], [])
    elif len(items) > 0:
        return SongDecisionTree(items[0], [create_tree(items[1:])])
    return None


def check_closest_val(cur_val: float | int, new_val: float | int, comparing_value: float | int) -> float | int:
    """
    Given a current value, a new value, and a comparing value,
    return the value that is closest to the comparing value.
    """
    if abs(new_val - float(comparing_value)) < abs(cur_val - float(comparing_value)):
        return new_val
    return cur_val


def round_values(inputs: list) -> list:
    """
    Given a list of inputs, round each numerical input to the closest value according to the NODES_PER_LEVEL list.
    """
    res = []
    for i in range(len(inputs)):
        closest_val = NODES_PER_LEVEL[i][random.randint(0, len(NODES_PER_LEVEL[i]) - 1)]

        if not isinstance(NODES_PER_LEVEL[i][0], str):
            for opt in NODES_PER_LEVEL[i]:
                closest_val = check_closest_val(closest_val, opt, inputs[i])
        elif inputs[i] in NODES_PER_LEVEL[i]:
            closest_val = inputs[i]
        res.append(closest_val)
    return res


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['random'],
        'allowed-imports': [],
        'max-line-length': 120,
    })
