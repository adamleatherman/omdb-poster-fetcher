import zmq


def main_program():
    """ZeroMQ main program that requests movie poster URLs."""
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    while True:
        movie_title = input(
            "Enter a movie title (or 'exit' to quit): "
        ).strip()
        if movie_title.lower() == "exit":
            break

        socket.send_string(movie_title)
        print(f"Request sent for: {movie_title}")

        poster_url = socket.recv_string()
        print(f"Poster URL: {poster_url}")


if __name__ == "__main__":
    main_program()
