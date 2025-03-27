"""
This module contains the RecommendationSystem class, which generates song recommendations 
based on inputs given by the user
"""
import random
from typing import Optional
from GenerateGraph import generate_song_graph, SEARCH_BAR_SPLITTER
from SongGraph import SongGraph
from SongDecisionTree import SongDecisionTree

DEFAULT_RECOMMENDATION_COUNT = 10
class RecommendationSystem:
    """
    Song recommendation system class to generate recommendations.

    Instance Attributes:
        - graph: SongGraph object that contains the song graph
        - song_list_names: a dictionary mapping song names to its vertex id in graph
        - tree: SongDecisionTree object that contains the decision tree
        - genres: a list of all the genres in graph
    """
    graph: SongGraph
    song_list_names: dict[str, str]
    tree: SongDecisionTree
    genres: list[str]

    def __init__(self):
        """
        Initialize the RecommendationSystem class and generate the song graph.
        """
        self.graph, self.song_list_names, self.tree, self.genres = generate_song_graph()

    def obtain_vertex_id(self, given_input: Optional[str | list]) -> Optional[str]:
        """
        If given a string formatted like "song_name<SEARCH_BAR_SPLITTER>artist_name", return the vertex_id of the song.
        If given a list of inputs, return the vertex_id of the song that is closest to the inputs.
        """
        if given_input is None:
            return None
        if isinstance(given_input, str):
            return self.song_list_names[given_input]
        else:
            options = self.tree.find_related_songs(given_input)
            print(options)
            return options[random.randint(0, len(options) - 1)]


    def generate_recommendations(self, given_input: Optional[str], n: int = DEFAULT_RECOMMENDATION_COUNT) -> list[str]:
        """
        Given a song name and artist, return a list of n tuples where the tuple is formatted like
        (song_name, artist_name, score).
        """
        if not given_input:
            return []
        vertex_id = self.obtain_vertex_id(given_input)
        shortest_distance = self.graph.find_shortest_distance(vertex_id, n)
        res = []
        for other_vertex_id, score in shortest_distance:
            vertex_details = self.graph.get_vertex_details(other_vertex_id)
            res.append((vertex_details['name'], '; '.join(vertex_details['artists']), score))
        return res

if __name__ == '__main__':
    vertex_id = "5SuOikwiRyPMVoIQDJUgSV"
    song = f'Comedy{SEARCH_BAR_SPLITTER}Gen Hoshino'
    sys = RecommendationSystem()
    recs = sys.generate_recommendations(song, 5)

    print(sys.graph.get_vertex_details(vertex_id))

    for neighbour_id in sys.graph.get_neighbours(vertex_id):
        print(sys.graph.get_neighbours(vertex_id)[neighbour_id])

    for rec in recs:
        print(rec)
    
    # inputs = [0.665,0.185,1,-13.852,1,0.0381,0.913,0.0,0.334,0.458,82.474,'acoustic'] # 1RZkqIEM5aV000fKgz9J46
    # inputs = [0.676,0.461,1,-6.746,0,0.143,0.0322,1.01e-06,0.358,0.715,87.917,'acoustic'] # 5SuOikwiRyPMVoIQDJUgSV
    inputs = [0.534,0.26,1,-12.406,1,0.0319,0.834,0.00405,0.102,0.151,113.877,'acoustic'] # 4ujYTGqbiV5xl97Pqoctq2
    sys.obtain_vertex_id(inputs)