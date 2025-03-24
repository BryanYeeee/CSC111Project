"""
some docstring bulshit
"""
import csv
import uuid
from SongGraph import _Vertex, SongGraph
from networkx_visual import visualize_graph

DATASET_NAME_1 = "datasets/kaggle_spotify_songs_1.csv"
DATASET_NAME_2 = "datasets/kaggle_spotify_songs_2.csv"

TESTING_LIMIT = 550


def generate_song_graph() -> SongGraph:
    """Generate some stuffs
    """
    g = SongGraph()
    max = TESTING_LIMIT

    with open(DATASET_NAME_1, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            g.add_vertex(row[1], 'song')
            for artist in row[2].split(";"):
                artist_id = uuid.uuid4()
                g.add_vertex(artist_id, 'artist')
                g.add_edge(row[1], artist_id)
            max = max-1
            if max ==TESTING_LIMIT/2:
                break

    with open(DATASET_NAME_2, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            g.add_vertex(row[0], 'song')
            artist_id = uuid.uuid4()
            g.add_vertex(artist_id, 'artist')
            g.add_edge(row[0], artist_id)
            max = max-1
            if max ==0:
                break

    return g


if __name__ == '__main__':
    g=generate_song_graph()
    print(len(g._vertices))
    visualize_graph(g)
