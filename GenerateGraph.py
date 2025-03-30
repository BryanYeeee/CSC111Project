"""
This module processes csv dataset files to generate the necessary objects to be used by the recommendation system
"""
import csv
from SongGraph import SongGraph
from SongDecisionTree import SongDecisionTree, organize_levels, round_values

DEFAULT_ORDER = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                 "instrumentalness", "liveness", "valence", "tempo", "genre"]

DATASET_NAME_1 = "datasets/kaggle_spotify_songs_1.csv"
DATASET_NAME_2 = "datasets/kaggle_spotify_songs_2.csv"
FILE_LENGTH_1 = 113999
FILE_LENGTH_2 = 32833
SONG_LIMIT_1 = 6000
SONG_LIMIT_2 = 4000
INTERVAL = 1

BASE_GENRES = {"pop", "rock", "techno", "metal", "house", "reggae", "songwriter", "rap"}
SAME_GENRES = {"rap": "hip-hop", "r&b": "r-n-b"}

SEARCH_BAR_SPLITTER = "｜"


def filter_genre(genre: str) -> str:
    """
    Given a genre, filter it to a base or common genre if possible.
    """
    for base_genre in BASE_GENRES:
        if base_genre in genre:
            genre = base_genre
    if genre in SAME_GENRES:
        return SAME_GENRES[genre]
    return genre


def add_to_objects(vertex_id: str, name: str, artists: set[str],
                   danceability: str, energy: str, key: str, loudness: str,
                   mode: str, speechiness: str, acousticness: str,
                   instrumentalness: str, liveness: str, valence: str,
                   tempo: str, genre: str,
                   songs_added: set,
                   new_graph: SongGraph,
                   song_list_names: dict[str, str],
                   new_tree: SongDecisionTree,
                   limit: int) -> str:
    """
    Add a song to the graph and tree if it has not been added yet.
    Also add it to the dictionary of song names and artists.
    """
    song_name = name + SEARCH_BAR_SPLITTER + artists
    if song_name.lower() not in songs_added:
        artists = set(artists.split(";"))
        genre = filter_genre(genre)
        new_graph.add_vertex(
            vertex_id, name, artists, danceability, energy, key, loudness, mode, speechiness, acousticness,
            instrumentalness, liveness, valence, tempo, genre)
        songs_added.add(song_name.lower())
        song_list_names[song_name] = vertex_id

        if limit % INTERVAL == 0:
            values = [danceability, energy, key, loudness, mode, speechiness, acousticness,
                      instrumentalness, liveness, valence, tempo]
            values = list(map(float, values))

            new_tree.insert_song(round_values(organize_levels(*values, genre)) + [vertex_id])
    return genre.capitalize()


def generate_song_graph() -> tuple[SongGraph, dict[str, str], SongDecisionTree]:
    """
    Generates a SongGraph, dictionary mapping song and artists to track id, and SongDecisionTree
    by reading two CSV datasets containing Spotify song data.
    Each song in the dataset is added as a vertex in the graph with its properties like
    genre, danceability, energy, tempo, artists, etc.
    """
    new_graph = SongGraph()
    new_tree = SongDecisionTree('', [])
    song_list_names = {}
    songs_added = set()
    limit = 0
    total = 0
    genres = set()

    print("start")
    with open(DATASET_NAME_1, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        reader = list(reader)
        while limit < len(reader):
            row = reader[limit]
            genres.add(add_to_objects(row[1], row[4], row[2], row[8], row[9], row[10], row[11], row[12], row[13],
                                      row[14], row[15], row[16], row[17], row[18],
                                      row[20], songs_added, new_graph, song_list_names, new_tree, limit))
            if limit % 1000 == 0:
                print(limit)
            limit += FILE_LENGTH_1 // SONG_LIMIT_1
            total += 1
    print("first file done")

    limit = 0

    with open(DATASET_NAME_2, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        reader = list(reader)
        while limit < len(reader):
            row = reader[limit]
            genres.add(add_to_objects(
                row[0], row[1], row[2], row[11], row[12], row[13],
                row[14], row[15], row[16], row[17], row[18], row[19],
                row[20], row[21], row[9], songs_added, new_graph, song_list_names, new_tree, limit
            ))
            if limit % 1000 == 0:
                print(limit)
            limit += FILE_LENGTH_2 // SONG_LIMIT_2
            total += 1
    print(total)

    return new_graph, song_list_names, new_tree, genres


if __name__ == '__main__':
    # TODO: Comment out, used for testing
    g, songs = generate_song_graph()
    print(g.get_vertex_details("7ujx3NYtwO2LkmKGz59mXp"))
    print(g.get_vertex_details("4OSEE9iEHADmTSCpxl87GJ"))
    # visualize_graph(g)

    print(songs)
