"""
A module that contains the SongDecisionTree class, which represents a decision tree with each level containing values
for a feature of the song's characteristics.
"""
from __future__ import annotations

import random
from typing import Any, Optional


def organize_levels(danceability: Any, energy: Any, key: Any, loudness: Any, mode: Any, speechiness: Any,
                    acousticness: Any, instrumentalness: Any, liveness: Any, valence: Any,
                    tempo: Any, genre: Any) -> list:
    """
    Organize the song characteristics into a list based on the weights of each feature.
    The value of the weights can be seen in SongGraph.py
    """
    return [genre, danceability, energy, valence, key, tempo, instrumentalness, mode, acousticness, loudness, liveness,
            speechiness]


NODES_PER_LEVEL = organize_levels(
    [x * 0.1 for x in range(0, 11)],
    [x * 0.1 for x in range(0, 11)],
    list(range(0, 12)),
    list(range(-10, 0)),
    [0, 1],
    [x * 0.01 for x in range(0, 11)],
    [x * 0.1 for x in range(7)],
    [x * 0.1 for x in range(0, 4)],
    [x * 0.1 for x in range(0, 5)],
    [x * 0.1 for x in range(0, 11)],
    [x * 10 for x in range(0, 24)],
    [
        'World-music', 'Country', 'Industrial', 'Trance', 'Club', 'Goth', 'Piano',
        'Comedy', 'Techno', 'Honky-tonk', 'Edm', 'Show-tunes', 'Happy', 'Pagode',
        'Children', 'Malay', 'Party', 'German', 'Indie', 'Sleep', 'Songwriter', 'Sad',
        'Dubstep', 'Disney', 'Jazz', 'Grindcore', 'New-age', 'Salsa', 'Study', 'Latino',
        'Grunge', 'J-dance', 'Rock', 'Emo', 'Classical', 'Dance', 'Turkish', 'Drum-and-bass',
        'Indian', 'Samba', 'Idm', 'Mpb', 'Hip-hop', 'Latin', 'Soul', 'Alternative', 'Electro',
        'French', 'Spanish', 'Punk', 'Tango', 'Funk', 'Chill', 'R-n-b', 'Breakbeat', 'Forro',
        'British', 'Metal', 'Bluegrass', 'Guitar', 'Sertanejo', 'Iranian', 'Anime', 'Brazil',
        'J-idol', 'Folk', 'Hardstyle', 'Dub', 'Gospel', 'Groove', 'Disco', 'Trip-hop', 'Opera',
        'Blues', 'Hardcore', 'Electronic', 'Reggae', 'Dancehall', 'Swedish', 'Ambient', 'Afrobeat',
        'Kids', 'Acoustic', 'Garage', 'House', 'Pop', 'Ska', 'Romance'
    ]
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
        if len(inputs) > 0:
            closest_tree = self._subtrees[random.randint(0, len(self._subtrees) - 1)]
            for subtree in self._subtrees:
                if not isinstance(closest_tree._root, str):
                    if abs(subtree._root - float(inputs[0])) < abs(closest_tree._root - float(inputs[0])):
                        closest_tree = subtree
                elif subtree._root == inputs[0]:
                    return subtree.find_related_songs(inputs[1:])
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


def round_values(inputs: list) -> list:
    """
    Given a list of inputs, round each numerical input to the closest value according to the NODES_PER_LEVEL list.
    """
    res = []
    for i in range(len(inputs)):
        if not isinstance(inputs[i], str):
            closest_val = NODES_PER_LEVEL[i][random.randint(0, len(NODES_PER_LEVEL[i]) - 1)]

            if not isinstance(NODES_PER_LEVEL[i][0], str):
                for opt in NODES_PER_LEVEL[i]:
                    if abs(opt - float(inputs[i])) < abs(opt - float(inputs[i])):
                        closest_val = opt
            elif inputs[i] in NODES_PER_LEVEL[i]:
                closest_val = inputs[i]
            res.append(closest_val)
        else:
            res.append(inputs[i])
    return res
