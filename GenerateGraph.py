"""
This module processes csv dataset files to generate a SongGraph to be used by the recommendation system
"""
import csv
from SongGraph import SongGraph
from networkx_visual import visualize_graph

DATASET_NAME_1 = "datasets/kaggle_spotify_songs_1.csv"
DATASET_NAME_2 = "datasets/kaggle_spotify_songs_2.csv"
SONG_LIMIT_1 = 1
SONG_LIMIT_2 = 4000

BASE_GENRES = {"pop", "rock", "techno", "metal", "house", "reggae", "songwriter"}
SAME_GENRES = {"rap": "hip-hop", "r&b": "r-n-b"}

SEARCH_BAR_SPLITTER = "｜"  # may need this as well in the file wherever the dictionary/list is generated


def filter_genre(genre: str) -> str:
    """
    Given a genre, filter it to a base or common genre if possible.
    """
    if genre in SAME_GENRES:
        return SAME_GENRES[genre]
    for base_genre in BASE_GENRES:
        if base_genre in genre:
            return base_genre
    return genre


def generate_song_graph() -> (SongGraph, dict[str: str]):
    """
    Generates a SongGraph by reading two CSV datasets containing Spotify song data.
    Each song in the dataset is added as a vertex in the graph with its properties like
    genre, danceability, energy, tempo, artists, etc.
    """
    new_graph = SongGraph()
    song_list_names = {}
    songs_added = set()
    limit = SONG_LIMIT_1

    print("start")
    with open(DATASET_NAME_1, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            song_name = row[4] + SEARCH_BAR_SPLITTER + row[2]
            if song_name.lower() not in songs_added:
                artists = set(row[2].split(";"))
                new_graph.add_vertex(
                    row[1], row[4], artists, row[8], row[9], row[10],
                    row[11], row[12], row[13], row[14], row[15], row[16],
                    row[17], row[18], filter_genre(row[20]))
                songs_added.add(song_name.lower())
                song_list_names[song_name] = row[1]
                limit = limit - 1
                if limit % 1000 == 0:
                    print(limit)
                if limit == 0:
                    break
    print("first file done")

    limit = SONG_LIMIT_2

    with open(DATASET_NAME_2, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            song_name = row[1] + SEARCH_BAR_SPLITTER + row[2]
            if song_name.lower() not in songs_added:
                new_graph.add_vertex(
                    row[0], row[1], {row[2]}, row[11], row[12], row[13],
                    row[14], row[15], row[16], row[17], row[18], row[19],
                    row[20], row[21], filter_genre(row[9]))
                songs_added.add(song_name.lower())
                song_list_names[song_name] = row[0]
                limit = limit - 1
                if limit % 1000 == 0:
                    print(limit)
                if limit == 0:
                    break
    return new_graph, song_list_names


if __name__ == '__main__':
    # TODO: Comment out, used for testing
    g, songs = generate_song_graph()
    print(g.get_vertex_details("7ujx3NYtwO2LkmKGz59mXp"))
    print(g.get_vertex_details("4OSEE9iEHADmTSCpxl87GJ"))
    # visualize_graph(g)

    print(songs)
