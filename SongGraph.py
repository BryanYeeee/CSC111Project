"""CSC111 Project:

some stuffs

"""
from __future__ import annotations
import csv
import networkx as nx

class _Vertex:
    """A Vertex in a graph

    Instance Attributes:
        - vertex_id: Id of the vertex
        - name: Name of the song or artist
        - kind: type of vertex (either song or artist)
        - neighbours: neighbouring vertices mapped to the similarity score between them

    Representation Invariant:
        - self.kind in {'artist', 'song'}
    """
    vertex_id: str
    name: str
    kind: str
    neighbours: dict[_Vertex, float]

    def __init__(self, vertex_id: str, name: str, kind: str) -> None:
        """ Initialize a new vertex

        Preconditions:
            - self.kind in {"song", "artist"}
        """
        self.vertex_id = vertex_id
        self.name = name
        self.kind = kind
        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex"""
        return len(self.neighbours)

class SongGraph:
    """
    abcdefg
    """
    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph"""
        self._vertices = {}

    def add_vertex(self, vertex_id: str, name: str, kind: str) -> None:
        """Add a vertex

        Preconditions:
            - kind in {'artist', 'song'}
        """
        if vertex_id not in self._vertices:
            self._vertices[vertex_id] = _Vertex(vertex_id, name, kind)

    def has_vertex(self, vertex_id: str) -> bool:
        """Returns whether the graph contains a vertex with the given vertex_id"""
        return vertex_id in self._vertices

    def add_edge(self, vertex_id1: str, vertex_id2: str, score: float) -> None:
        """Add an edge with a score between the two vertices with the given vertex_ids in this graph.

        Raise a ValueError if vertex_id1 or vertex_id2 do not appear as vertices in this graph.

        Preconditions:
            - vertex_id1 != vertex_id2
        """
        if vertex_id1 in self._vertices and vertex_id2 in self._vertices:
            v1 = self._vertices[vertex_id1]
            v2 = self._vertices[vertex_id2]

            v1.neighbours[v2] = score
            v2.neighbours[v1] = score
        else:
            raise ValueError

    def adjacent(self, vertex_id1: str, vertex_id2: str) -> bool:
        """Return whether vertex_id1 and vertex_id2 are adjacent vertices in this graph.

        Return False if vertex_id1 or vertex_id2 do not appear as vertices in this graph.
        """
        if vertex_id1 in self._vertices and vertex_id2 in self._vertices:
            v1 = self._vertices[vertex_id1]
            return any(v2.vertex_id == vertex_id2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, vertex_id: str) -> set:
        """Return a set of the neighbours of the given vertex_id.

        Note that the *vertex_ids* are returned, not the _Vertex objects themselves.

        Raise a ValueError if vertex_id does not appear as a vertex in this graph.
        """
        if vertex_id in self._vertices:
            v = self._vertices[vertex_id]
            return {neighbour.vertex_id for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex vertex_ids in this graph.

        If kind != '', only return the vertex_ids of the given vertex kind.

        Preconditions:
            - kind in {'', 'artist', 'song'}
        """
        if kind != '':
            return {v.vertex_id for v in self._vertices.values() if v.kind == kind}
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
            graph_nx.add_node(v.vertex_id, kind=v.kind)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.vertex_id, kind=u.kind)

                if u.vertex_id in graph_nx.nodes:
                    graph_nx.add_edge(v.vertex_id, u.vertex_id)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx