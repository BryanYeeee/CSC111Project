"""
This module would find song properties such as genre, danceability, energy, tempo, artists, etc. for a song that is not
included in the CSV Spotify datasets.
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

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
    """
    song_input = song_input.strip().replace(" ", "+")
    search_url = PARENT_URL + "/search?query=" + song_input
    page = requests.get(search_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    links = soup.find_all("td", class_="table_img", limit=5)

    # Links to first 5 songs found on the page
    return [PARENT_URL + quote(td.find("a")["href"]) for td in links]


def get_song_properties(song_page_url: str) -> dict:
    """
    Gets properties of a song by scraping the song page URL on songdata.io.

    Preconditions:
        - song_page_url: A valid URL from songdata.io that points to a specific song's page.
    """

    page = requests.get(song_page_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Scraping track_name and artists
    try:
        song_id = re.search(r'/track/([a-zA-Z0-9]+)', song_page_url).group(1)
        col12 = soup.find("div", class_="col-12 text-center")
        col12_div = col12.find_all("div")
    except:
        print("Something went wrong with finding the song id")

    try:
        track_name, artists = col12_div[0].text, col12_div[1].text
    except:
        print("Something went wrong with finding the track name or artist names")
    artists = set(artists.split(", "))

    # Scraping tempo and mode
    try:
        tempo = re.search(r"BPM(\d+)", col12_div[4].text.replace('\n', '')).group(1)
        mode = 1 if "major" in col12_div[5].text.lower() else 0
        camelot = re.search(r"Camelot(.+)", col12_div[6].text.replace('\n', '')).group(1)
        key = CAMELOT_TO_KEY[camelot]
    except:
        print("Something went wrong with finding the tempo, mode, or key")

    # Scraping danceability, energy, loudness, speechiness, acousticness, instrumentalness, liveness, and valence
    grid = soup.find_all("div", class_="col-6-lg-12")
    div_text = ''
    for div in grid:
        if div.text:
            div_text += div.text
    div_text = div_text.replace("\n", ' ')

    try:
        danceability = int(re.search(r"Danceability (\d+)", div_text).group(1)) / 100
        energy = int(re.search(r"Energy (\d+)", div_text).group(1)) / 100
        loudness = re.search(r"Loudness ([-.\d]+)", div_text).group(1)
        speechiness = int(re.search(r"Speechiness (\d+)", div_text).group(1)) / 100
        acousticness = int(re.search(r"Acousticness (\d+)", div_text).group(1)) / 100
        instrumentalness = int(re.search(r"Instrumentalness (\d+)", div_text).group(1)) / 100
        liveness = int(re.search(r"Liveness (\d+)", div_text).group(1)) / 100
        valence = int(re.search(r"Valence (\d+)", div_text).group(1)) / 100
    except:
        print("Something went wrong with finding the danceability, "
              "energy, loudness, speechiness, acousticness, instrumentalness, liveness, or valence")

    try:
        return {"song_id": song_id, "track_name": track_name, "artists": artists, "danceability": danceability,
                "energy": energy, "key": key, "loudness": loudness, "mode": mode, "speechiness": speechiness,
                "acousticness": acousticness, "instrumentalness": instrumentalness, "liveness": liveness,
                "valence": valence,
                "tempo": tempo}
    except:
        return {}
