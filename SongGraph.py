"""CSC111 Project:

some stuffs

"""
from __future__ import annotations
from typing import Any
import networkx as nx

SIMILARITY_WEIGHTING = {
    "genre": 2.0,
    "danceability": 1.5,
    "energy": 1.5,
    "valence": 1.2,
    "key": 1.0,
    "mode": 0.8,
    "tempo": 1.0,
    "loudness": 0.5,
    "speechiness": 0.3,
    "acousticness": 0.5,
    "instrumentalness": 0.7,
    "liveness": 0.4
}
# The max limit at which a similarity score can be in order to add an edge
SCORE_LIMIT = 2.25

class _Vertex:
    """A Vertex in a graph

    Instance Attributes:
        - vertex_id: Id of the vertex
        - name: Name of the song or artist
        - neighbours: neighbouring vertices mapped to the similarity score between them

    Representation Invariant:
        -
    """
    vertex_id: str
    track_name: str
    artists: set[str]
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    track_genre: str
    neighbours: dict[_Vertex, float]

    def __init__(
        self, vertex_id: str, name: str, artists: set[str],
        danceability: str, energy: str, key: str, loudness: str,
        mode: int, speechiness: str, acousticness: str,
        instrumentalness: str, liveness: str, valence: str,
        tempo: str, track_genre: str
    ) -> None:
        """ Initialize a new vertex
        """
        self.vertex_id = vertex_id
        self.name = name
        self.artists = artists
        self.danceability = float(danceability)
        self.energy = float(energy)
        self.key = int(key)
        self.loudness = float(loudness)
        self.mode = int(mode)
        self.speechiness = float(speechiness)
        self.acousticness = float(acousticness)
        self.instrumentalness = float(instrumentalness)
        self.liveness = float(liveness)
        self.valence = float(valence)
        self.tempo = float(tempo)
        self.track_genre = track_genre

        self.neighbours = {}

    def degree(self) -> int:
        """Return the degree of this vertex"""
        return len(self.neighbours)

    def get_similarity(self, other: _Vertex) -> float:
        """
        Calculates the similarit score of 2 vertices
        The formula used is ......
        """
        score = 0

        if self.track_genre == other.track_genre:
            score += SIMILARITY_WEIGHTING["genre"]

        numerical_features = [
            ("danceability", self.danceability, other.danceability, SIMILARITY_WEIGHTING["danceability"]),
            ("energy", self.energy, other.energy, SIMILARITY_WEIGHTING["energy"]),
            ("valence", self.valence, other.valence, SIMILARITY_WEIGHTING["valence"]),
            ("key", self.key, other.key, SIMILARITY_WEIGHTING["key"]),
            ("mode", self.mode, other.mode, SIMILARITY_WEIGHTING["mode"]),
            ("tempo", self.tempo, other.tempo, SIMILARITY_WEIGHTING["tempo"]),
            ("loudness", self.loudness, other.loudness, SIMILARITY_WEIGHTING["loudness"]),
            ("speechiness", self.speechiness, other.speechiness, SIMILARITY_WEIGHTING["speechiness"]),
            ("acousticness", self.acousticness, other.acousticness, SIMILARITY_WEIGHTING["acousticness"]),
            ("instrumentalness", self.instrumentalness, other.instrumentalness,
             SIMILARITY_WEIGHTING["instrumentalness"]),
            ("liveness", self.liveness, other.liveness, SIMILARITY_WEIGHTING["liveness"])
        ]

        for feature_name, val1, val2, weight in numerical_features:
            if feature_name == "tempo":
                tempo_diff = abs(val1 - val2) / max(val1, val2)
                score += weight * tempo_diff ** 2
            else:
                score += weight * (val1 - val2) ** 2

        return score


class SongGraph:
    """
    abcdefg
    """
    _vertices: dict[str, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph"""
        self._vertices = {}

    def add_vertex(
        self, vertex_id: str, name: str, artists: set[str],
        danceability: str, energy: str, key: str, loudness: str,
        mode: str, speechiness: str, acousticness: str,
        instrumentalness: str, liveness: str, valence: str,
        tempo: str, track_genre: str
    ) -> None:
        """Add a vertex

        Preconditions:
            -
        """
        if vertex_id not in self._vertices:
            self._vertices[vertex_id] = _Vertex(
                vertex_id, name, artists,
                danceability, energy, key, loudness,
                mode, speechiness, acousticness,
                instrumentalness, liveness, valence,
                tempo, track_genre)
            self.generate_edges(vertex_id)

    def generate_edges(self, vertex_id1: str) -> None:
        """Add edges to this vertex based on the similarity score of other vertices

        Preconditions:
            - vertex_id1 in self._vertices
        """
        v1 = self._vertices[vertex_id1]
        for vertex_id2 in self._vertices:
            if vertex_id1 != vertex_id2:
                score = v1.get_similarity(self._vertices[vertex_id2])
                if score < SCORE_LIMIT:
                    self.add_edge(vertex_id1, vertex_id2, score)

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

    def has_vertex(self, vertex_id: str) -> bool:
        """Returns whether the graph contains a vertex with the given vertex_id"""
        return vertex_id in self._vertices

    def adjacent(self, vertex_id1: str, vertex_id2: str) -> bool:
        """Return whether vertex_id1 and vertex_id2 are adjacent vertices in this graph.

        Return False if vertex_id1 or vertex_id2 do not appear as vertices in this graph.
        """
        if vertex_id1 in self._vertices and vertex_id2 in self._vertices:
            v1 = self._vertices[vertex_id1]
            return any(v2.vertex_id == vertex_id2 for v2 in v1.neighbours)
        else:
            return False

    def get_neighbours(self, vertex_id: str) -> dict[str, float]:
        """Return a dictionary of the neighbours to similarity score of the given vertex_id.

        Raise a ValueError if vertex_id does not appear as a vertex in this graph.
        """
        if vertex_id in self._vertices:
            v = self._vertices[vertex_id]
            return {neighbour.vertex_id: v.neighbours[neighbour] for neighbour in v.neighbours}
        else:
            raise ValueError

    def get_all_vertices(self) -> set:
        """Return a set of all vertex vertex_ids in this graph.
        """
        return set(self._vertices.keys())

    def get_vertex_details(self, vertex_id: str) -> dict[str, Any]:
        """
        Given a vertex_id id, return the details of the vertex
        """
        vertex = self._vertices[vertex_id]
        return {
            'name': vertex.name,
            'artists': vertex.artists,
            'danceability': vertex.danceability,
            'energy': vertex.energy,
            'key': vertex.key,
            'loudness': vertex.loudness,
            'mode': vertex.mode,
            'speechiness': vertex.speechiness,
            'acousticness': vertex.acousticness,
            'instrumentalness': vertex.instrumentalness,
            'liveness': vertex.liveness,
            'valence': vertex.valence,
            'tempo': vertex.tempo,
            'track_genre': vertex.track_genre
        }

    def get_average_edges(self) -> float:
        """Returns the average number of edges per vertex.
        Used to decide a value for the SCORE_LIMIT constant
        """
        return sum(len(self._vertices[vid].neighbours) for vid in self._vertices)/(len(self._vertices))

    def to_networkx(self, max_vertices: int = 5000) -> nx.Graph:
        """Convert this graph into a networkx Graph.

        max_vertices specifies the maximum number of vertices that can appear in the graph.
        (This is necessary to limit the visualization output for large graphs.)

        Note that this method is provided for you, and you shouldn't change it.
        """
        graph_nx = nx.Graph()
        for v in self._vertices.values():
            graph_nx.add_node(v.vertex_id)

            for u in v.neighbours:
                if graph_nx.number_of_nodes() < max_vertices:
                    graph_nx.add_node(u.vertex_id)

                if u.vertex_id in graph_nx.nodes:
                    graph_nx.add_edge(v.vertex_id, u.vertex_id)

            if graph_nx.number_of_nodes() >= max_vertices:
                break

        return graph_nx
