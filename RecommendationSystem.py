"""
This module contains the RecommendationSystem class, which generates song recommendations.
"""
from GenerateGraph import generate_song_graph
from SongGraph import SongGraph

SEARCH_BAR_SPLITTER = "｜"  # may need this as well in the file wherever the dictionary/list is generated


class RecommendationSystem:
    """
    Song recommendation system class to generate recommendations.

    Instance Attributes:
        - graph: SongGraph object that contains the song graph
        - song_list_names: a dictionary mapping song names to its vertex id in graph
    """
    graph: SongGraph
    song_list_names: dir[str: str]

    def __init__(self):
        """
        Initialize the RecommendationSystem class and generate the song graph.
        """
        self.graph, self.song_list_names = generate_song_graph()

    def obtain_vertex_id(self, given_input: str) -> str:
        """
        Given a string formatted like "song_name<SEARCH_BAR_SPLITTER>artist_name", return the vertex_id of the song.
        """
        song_name, artist_name = given_input.split(SEARCH_BAR_SPLITTER)
        return "5SuOikwiRyPMVoIQDJUgSV"
        # TODO: Find the vertex_id based on the song_name and artist_name

    def generate_recommendations(self, given_input: str, n: int) -> list[str, str, str]:
        """
        Given a song name and artist, return a list of n tuples where the tuple is formatted like
        (song_name, artist_name, score).
        """
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
