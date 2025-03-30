"""
This module would find song properties such as genre, danceability, energy, tempo, artists, etc. for a song that is not
included in the CSV Spotify datasets.
"""
from urllib.parse import quote
import re
import requests
from bs4 import BeautifulSoup
import generate_graph

PARENT_URL = "https://songdata.io"
CAMELOT_TO_KEY = {
    "1A": 8, "1B": 11, "2A": 3, "2B": 6,
    "3A": 10, "3B": 3, "4A": 5, "4B": 8,
    "5A": 0, "5B": 3, "6A": 7, "6B": 10,
    "7A": 2, "7B": 5, "8A": 9, "8B": 0,
    "9A": 4, "9B": 7, "10A": 11, "10B": 2,
    "11A": 6, "11B": 9, "12A": 1, "12B": 4}


def get_song_links(song_input: str) -> list:
    """
    Returns first 5 links on songdata.io by searching the website based on the song_input
    Returns empty list if nothing found

    >>> links = get_song_links("Bohemian Rhapsody")
    >>> links[0]
    'https://songdata.io/track/6l8GvAyoUZwWDgF1e4822w/Bohemian%20Rhapsody-by-Queen'
    >>> links[4]
    'https://songdata.io/track/2OWOkkAQv7KFlScZymrfZ4/Bohemian%20Rhapsody-by-Rockabye%20Baby%21'
    """
    song_input = song_input.strip().replace(" ", "+")
    search_url = PARENT_URL + "/search?query=" + song_input
    page = requests.get(search_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all("td", class_="table_img", limit=5)

    return [PARENT_URL + quote(td.find("a")["href"]) for td in links]


def get_song_properties(song_page_url: str) -> dict:
    """
    Gets properties of a song by scraping the song page URL on songdata.io.

    Preconditions:
        - song_page_url: A valid URL from songdata.io that points to a specific song's page.
    >>> properties = get_song_properties("https://songdata.io/track/1lOe9qE0vR9zwWQAOk6CoO/Ransom-by-Lil-Tecca")
    >>> properties['song_id']
    '1lOe9qE0vR9zwWQAOk6CoO'
    >>> properties['loudness']
    -6.257
    >>> properties['tempo']
    180
    >>> properties['track_genre']
    'hip-hop'
    """

    properties = {"song_id": "", "track_name": "", "artists": [], "danceability": 0.0, "energy": 0.0, "key": 0,
                  "loudness": 0.0, "mode": 0, "speechiness": 0.0, "acousticness": 0.0, "instrumentalness": 0.0,
                  "liveness": 0.0, "valence": 0.0, "tempo": 0, "track_genre": ""}

    page = requests.get(song_page_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Scraping track_name, artists, and track genre
    try:
        col12 = soup.find("div", class_="col-12 text-center")
        col12_div = col12.find_all("div")
    except AttributeError:
        return {}

    try:
        properties["song_id"] = re.search(r'/track/([a-zA-Z0-9]+)', song_page_url).group(1)
        properties["track_name"], artists = get_title_artist(song_page_url)
        properties["artists"] = artists.split(", ")
        properties["track_genre"] = get_song_genre(properties["track_name"], properties["artists"][0])

    except AttributeError:
        return {}

    # Scraping tempo and mode
    try:
        properties["tempo"] = int(re.search(r"BPM(\d+)", col12_div[4].text.replace('\n', '')).group(1))
        properties["mode"] = 1 if "major" in col12_div[5].text.lower() else 0
        camelot = re.search(r"Camelot(.+)", col12_div[6].text.replace('\n', '')).group(1)
        properties["key"] = CAMELOT_TO_KEY[camelot]
    except AttributeError:
        return {}

    # Scraping danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, and valence
    grid = soup.find_all("div", class_="col-6-lg-12")
    div_text = ''
    for div in grid:
        if div.text:
            div_text += div.text
    div_text = div_text.replace("\n", ' ')

    try:
        properties["danceability"] = int(re.search(r"Danceability (\d+)", div_text).group(1)) / 100
        properties["energy"] = int(re.search(r"Energy (\d+)", div_text).group(1)) / 100
        properties["loudness"] = float(re.search(r"Loudness ([-.\d]+)", div_text).group(1))
        properties["speechiness"] = int(re.search(r"Speechiness (\d+)", div_text).group(1)) / 100
        properties["acousticness"] = int(re.search(r"Acousticness (\d+)", div_text).group(1)) / 100
        properties["instrumentalness"] = int(re.search(r"Instrumentalness (\d+)", div_text).group(1)) / 100
        properties["liveness"] = int(re.search(r"Liveness (\d+)", div_text).group(1)) / 100
        properties["valence"] = int(re.search(r"Valence (\d+)", div_text).group(1)) / 100
    except AttributeError:
        return {}

    return properties


def get_song_genre(song_name: str, artist: str) -> str:
    """
    Return's the song genre, bsed on the song_name and artist arguments
    by webscraping a wikipedia page, or returns an empty string if the page or genre isn't found.
    The genre is filtered by the funciton in GenerateGraph
    >>> get_song_genre("I Love It", "Icona Pop")
    'pop'
    >>> get_song_genre("Gangsta's Paradise", "Coolio")
    'hip-hop'
    """
    clean_name = re.sub(r"\s*(feat\.?|ft\.?).*", "", song_name, flags=re.IGNORECASE).strip()
    api_url = (f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="
               f"{quote(clean_name + " " + artist)}%20song&format=json")
    data = requests.get(api_url).json()

    if data["query"]["search"]:
        page_title = quote(data["query"]["search"][0]["title"])
        page_url = f"https://en.wikipedia.org/wiki/{page_title}"
        song_data_page = requests.get(page_url)
        genre_soup = BeautifulSoup(song_data_page.text, "html.parser")
        try:
            genre_row = genre_soup.find("th", string="Genre")
            genre = genre_row.find_next_sibling("td").text
            genre = genre.strip().split("\n")[0].lower()
            return generate_graph.filter_genre(genre)
        except AttributeError:
            return ''
    return ''


def get_title_artist(song_page_url: str) -> tuple[str, str]:
    """
    Gets the title and artist of a song by scraping a songdata.io url link
    Precondition:
        - song_page_url: A valid URL from songdata.io that points to a specific song's page.

    >>> get_title_artist("https://songdata.io/track/3eekarcy7kvN4yt5ZFzltW/HIGHEST-IN-THE-ROOM-by-Travis-Scott")
    ('HIGHEST IN THE ROOM', 'Travis Scott')
    """
    page = requests.get(song_page_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Scraping track_name and artists
    col12 = soup.find("div", class_="col-12 text-center")
    col12_div = col12.find_all("div")

    track_name, artists = col12_div[0].text, col12_div[1].text
    return track_name, artists


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['requests', 'bs4', 'generate_graph', 're', 'urllib.parse'],
        'max-line-length': 120,
    })
