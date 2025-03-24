"""
This module contains the RecommendationSystem class, which generates song recommendations.
"""
import heapq

from GenerateGraph import generate_song_graph
from SongGraph import SongGraph


class RecommendationSystem:
    """
    Song recommendation system class to generate recommendations.

    Instance Attributes:
        - graph: SongGraph object that contains the song graph
    """
    graph: SongGraph

    def __init__(self):
        """
        Initialize the RecommendationSystem class and generate the song graph.
        """
        self.graph = generate_song_graph()

    def generate_recommendation(self, orig_vertex_id: str, n: int) -> list[str]:
        """
        Given the id of a song in the graph, generate n song recommendations that
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
        return list([x[0] for x in res[:n]])



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
