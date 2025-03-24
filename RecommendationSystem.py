"""
This module contains the RecommendationSystem class, which generates song recommendations.
"""
import heapq

from GenerateGraph import generate_song_graph
from SongGraph import SongGraph


SEARCH_BAR_SPLITTER = " | " # may need this as well in the file wherever the dictionary/list is generated
class RecommendationSystem:
    """
    Song recommendation system class to generate recommendations.

    Instance Attributes:
        - graph: SongGraph object that contains the song graph
    """
    graph: SongGraph
    song_list_names: list[str]

    def __init__(self):
        """
        Initialize the RecommendationSystem class and generate the song graph.
        """
        self.graph = generate_song_graph() # ** Maybe have this return the song_list_names + a dictionary with vertex_id as the key
        self.song_list_names = [f'Comedy{SEARCH_BAR_SPLITTER}Gen Hoshino']
        
    def obtain_vertex_id(self, given_input: str) -> str:
        """
        Given a string formatted like "song_name<SEARCH_BAR_SPLITTER>artist_name", return the vertex_id of the song.
        """
        song_name, artist_name = given_input.split(SEARCH_BAR_SPLITTER)
        return "5SuOikwiRyPMVoIQDJUgSV"
        # TODO: Find the vertex_id based on the song_name and artist_name

    def find_shortest_distance(self, orig_vertex_id: str, n: int) -> list[str, float]:
        """
        Given the id of a song in the graph, find n other songs that
        are similar to the song and return their vertex_ids in a list.

        Preconditions:
            - orig_vertex_id in self.graph._vertices
            - n > 0
        """
        shortest_distance = {orig_vertex_id: 0}

        queue = [(0.0, orig_vertex_id)]
        visited = set()
        while queue and len(shortest_distance) + 1 < n:
            score, vertex_id = heapq.heappop(queue)
            visited.add(vertex_id)
            neighbours = self.graph.get_neighbours(vertex_id)
            for neighbour in neighbours:
                neighbour_score = neighbours[neighbour]
                if neighbour not in shortest_distance:
                    shortest_distance[neighbour] = float('inf')
                shortest_distance[neighbour] = min(shortest_distance[neighbour], score + neighbour_score)

                if neighbour not in visited:
                    heapq.heappush(queue, (score + neighbour_score, neighbour))
        del shortest_distance[orig_vertex_id]
        res = [(key, shortest_distance[key]) for key in shortest_distance]
        res.sort(key=lambda x: x[1])
        print(res)
        return res[:n]

    def generate_recommendations(self, given_input: str, n: int) -> list[str, str, str]:
        """
        Given a song name and artist, return a list of n tuples where the tuple is formatted like 
        (song_name, artist_name, score).
        """
        vertex_id = self.obtain_vertex_id(given_input)
        shortest_distance = self.find_shortest_distance(vertex_id, n)
        res = []
        for other_vertex_id, score in shortest_distance:
            vertex_details = self.graph.get_vertex_details(other_vertex_id)
            res.append((vertex_details['name'], '; '.join(vertex_details['artists']), score))
        return res

if __name__ == '__main__':
    vertex_id = "5SuOikwiRyPMVoIQDJUgSV"
    sys = RecommendationSystem()
    recs = sys.generate_recommendation(vertex_id, 5)

    print(sys.graph.get_vertex_details(vertex_id))

    for neighbour_id in sys.graph.get_neighbours(vertex_id):
        print(sys.graph.get_neighbours(vertex_id)[neighbour_id])

    for rec_id in recs:
        print(sys.graph.get_vertex_details(rec_id)['name'])
        # print(sys.graph.get_vertex_details(rec_id))
        print(sys.graph.get_neighbours(vertex_id)[rec_id])
