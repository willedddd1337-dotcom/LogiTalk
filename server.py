
import socket as s
import threading

HOST = '0.0.0.0'
PORT = 8080

clients = []


def broadcast(data, exclude_socket=None):

    for client in clients:

        if client != exclude_socket:

            try:
                client.sendall(data)

            except:

                if client in clients:
                    clients.remove(client)


def handle_client(client_socket):

    while True:

        try:

            data = client_socket.recv(4096)

            if not data:
                break

            broadcast(
                data,
                exclude_socket=client_socket
            )

        except:
            break

    if client_socket in clients:
        clients.remove(client_socket)

    client_socket.close()


def main():

    server_socket = s.socket(
        s.AF_INET,
        s.SOCK_STREAM
    )

    server_socket.setsockopt(
        s.SOL_SOCKET,
        s.SO_REUSEADDR,
        1
    )

    server_socket.bind((HOST, PORT))

    server_socket.listen(5)

    print("server running...")

    while True:

        client_socket, addr = server_socket.accept()

        print(f"Connected: {addr}")

        clients.append(client_socket)

        t = threading.Thread(
            target=handle_client,
            args=(client_socket,)
        )

        t.start()


if __name__ == "__main__":
    main()