"""CSC111 Project:

some stuffs

"""
from __future__ import annotations
import csv
from typing import Any
import networkx as nx

class _Vertex:
    """A Vertex in a graph

    Instance Attributes:
        -

    Representation Invariant:
        -
    """
    item: Any
    kind: str
    neighbours: dict[_Vertex, float]

    def __init__(self, item: Any, kind: str) -> None:
        """ Initialize a new vertex

        Preconditions:
            - kind in {"song", "artist"}
        """
        self.item = item
        self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex"""
        return len(self.neighbours)

class SongGraph:
    """
    abcdefg
    """
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph"""
        self._vertices = {}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex

        Preconditions:
            - kind in {'user', 'book'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def has_vertex(self, item: Any) -> bool:
        """Returns whether the graph contains a vertex with the given item"""
        return item in self._vertices

    def add_edge(self, item1: Any, item2: Any, score: float) -> None:
        """Add an edge with a score between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours[v2] = score
            v2.neighbours[v1] = score
        else:
            raise ValueError

    def adjacent(self, item1: Any, item2: Any) -> bool:
        """Return whether item1 and item2 are adjacent vertices in this graph.

        Return False if item1 or item2 do not appear as vertices in this graph.
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            return any(v2.item == item2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of the given vertex kind.

        Preconditions:
            - kind in {'', 'user', 'book'}
        """
        if kind != '':
            return {v.item for v in self._vertices.values() if v.kind == kind}
        else:
            return set(self._vertices.keys())

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.item, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.item, kind=u.kind)

                if u.item in graph_nx.nodes:
                    graph_nx.add_edge(v.item, u.item)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx