import os

import zmq
import requests
from dotenv import load_dotenv

load_dotenv()

OMDB_API_URL = "http://www.omdbapi.com/"
OMDB_API_KEY = os.getenv("OMDB_API_KEY")


def fetch_movie_poster(movie_title):
    """Fetches the poster URL of a movie from OMDb API."""
    params = {"t": movie_title, "apikey": OMDB_API_KEY}
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster", "Poster not found")
        else:
            return f"Error: {data.get('Error')}"
    return "Error: Failed to fetch from OMDb API"


def microservice():
    """ZeroMQ microservice that fetches movie poster URLs."""
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Microservice is running...")
    while True:
        movie_title = socket.recv_string()
        print(f"Received request for: {movie_title}")

        poster_url = fetch_movie_poster(movie_title)
        print(f"Sending response: {poster_url}")

        socket.send_string(poster_url)


if __name__ == "__main__":
    microservice()
