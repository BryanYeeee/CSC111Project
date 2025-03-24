"""
some docstring bulshit
"""
import csv
from SongGraph import SongGraph
from networkx_visual import visualize_graph

DATASET_NAME_1 = "datasets/kaggle_spotify_songs_1.csv"
DATASET_NAME_2 = "datasets/kaggle_spotify_songs_2.csv"

TESTING_LIMIT = 550

def generate_song_graph() -> SongGraph:
    """
    Generate some stuffs
    """
    new_graph = SongGraph()
    limit = TESTING_LIMIT

    with open(DATASET_NAME_1, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            artists = row[2].split(";")
            new_graph.add_vertex(
                row[1], row[4], artists, row[8], row[9], row[10], 
                row[11], row[12], row[13], row[14], row[15], row[16], 
                row[17], row[18], row[20])
            limit = limit - 1
            if limit == TESTING_LIMIT/2:
                break

    with open(DATASET_NAME_2, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            new_graph.add_vertex(
                row[0], row[1], row[2], row[11], row[12], row[13], 
                row[14], row[15], row[16], row[17], row[18], row[19], 
                row[20], row[21], row[9])

            limit = limit - 1
            if limit == 0:
                break

    return new_graph


if __name__ == '__main__':
    g=generate_song_graph()
    print(len(g._vertices))
    visualize_graph(g)
