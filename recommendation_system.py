"""
This module contains the RecommendationSystem class, which generates song recommendations
based on inputs given by the user
"""
import random
from typing import Optional
from generate_graph import generate_song_graph
from song_graph import SongGraph
from song_decision_tree import SongDecisionTree

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

    def __init__(self) -> None:
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
            return options[random.randint(0, len(options) - 1)]

    def get_similarity_score_count(self, vertex_ids: list[str], n: int) -> dict[tuple[str, str], list[float]]:
        """
        Given a list of vertex ids, find the top n songs that are similar to each vertex id.
        Return a dictionary where the keys are tuples of song names and artists, that were
        similar to the any of the given vertex ids, and the values are lists of 
        similarity scores between the given vertex ids and the song indicated by the key.
        """
        counter = {}
        for vertex_id in vertex_ids:
            shortest_distance = self.graph.find_shortest_distance(vertex_id, n)
            for other_vertex_id, score in shortest_distance:
                if other_vertex_id in vertex_ids:
                    continue
                vertex_details = self.graph.get_vertex_details(other_vertex_id)
                song_artist = (vertex_details['name'], '; '.join(vertex_details['artists']))
                if song_artist not in counter:
                    counter[song_artist] = []
                counter[song_artist].append(score)
        return counter

    def combine_similarity_score(self, counter: dict[tuple[str, str], list[float]],
                                 n: int) -> list[list[tuple[str, str, float]]]:
        """
        Given a dictionary where the key is a tuple of song names and artists,
        and the value is a list of similarity scores with that song, return a nested list where:
        - each sublist contains tuples of song names, artists, and the average similarity score
        - the first sublist contains songs that have n similarity scores
        - the second sublist contains songs that have n-1 similarity scores
        - ...
        - the last sublist contains songs that have 1 similarity score
        """
        ordered_list = [[] for _ in range(n)]
        for song_artist in counter:
            intersections = counter[song_artist]
            num_intersections = len(intersections)
            new_score = sum(intersections) / num_intersections
            ordered_list[n - num_intersections].append((song_artist[0], song_artist[1], new_score))
        return ordered_list

    def sort_and_format_scores(self, ordered_list: list[list[tuple[str, str, float]]], n: int) -> None:
        """
        Mutate the ordered list of songs to ensure that
        - Each sublist is sorted by the float value (similarity score) in ascending order
        - The similarity scores of all sublists are formatted to be relative to each other
        such that the scores are ordered in ascending order.
        
        The relative score is calculated multiplying the float value by the ratio of the
        previous non empty sublist's last song's (largest) score to the current sublist's first song's (smallest) score,
        to ensure that the scores are relative to each other.
        """
        i = 0
        num_songs = 0
        prev_last_val = None
        while i < len(ordered_list) and num_songs < n:
            if ordered_list[i] != []:
                cur_list = ordered_list[i]
                cur_list.sort(key=lambda x: x[-1])
                if prev_last_val:
                    ratio = prev_last_val / cur_list[0][-1]
                    ordered_list[i] = [(*cur_tuple[:-1], cur_tuple[-1] * ratio) for cur_tuple in cur_list]
                if num_songs + len(cur_list) > n:
                    ordered_list[i] = ordered_list[i][:n - num_songs]
                    num_songs += len(ordered_list[i])
                    break
                num_songs += len(ordered_list[i])
                prev_last_val = ordered_list[i][-1][-1]
            i += 1

    def generate_recommendations(self, given_input: Optional[list[str] | list],
                                 n: int = DEFAULT_RECOMMENDATION_COUNT) -> list[list[tuple[str, str, float]]]:
        """
        If given a list of strings, return a nested list where:
        - the first sublist contains a list of songs that are similar to every song in the input
        - ...
        - the last sublist contains a list of songs that are similar to one of the songs in the input
        - each sublist contains a list of tuples
        - each tuple contains the song name, artist name, and relative similarity score
        
        The relativity score is calculated by taking the average of the similarity scores between the 
        song and the songs in the given input. This relativity score is also multiplied by the ratio of the
        previous non empty sublist's last song's (largest) score to the current sublist's first song's (smallest) score,
        to ensure that the scores are relative to each other.
        
        If given a list of features, return a list of songs that are similar to the song with the given features.
        """
        if not given_input:
            return []
        if not all({isinstance(value, str) for value in given_input}):  # taking in a list of features
            vertex_ids = {self.obtain_vertex_id(given_input)}
            songs_to_check = 1
        else:
            vertex_ids = set(self.obtain_vertex_id(value) for value in given_input)
            songs_to_check = len(vertex_ids)

        counter = self.get_similarity_score_count(vertex_ids, n)
        ordered_list = self.combine_similarity_score(counter, songs_to_check)
        self.sort_and_format_scores(ordered_list, n)

        return ordered_list


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['random', 'song_graph', 'song_decision_tree', 'generate_graph'],
        'allowed-imports': [],
        'max-line-length': 120,
    })
