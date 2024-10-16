import socket
import threading
import os


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)
    print("Server started")

    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()


def handle_client(client):
    while True:
        message = client.recv(1024).decode("utf-8")
        if message == "FILE":
            receive_file(client)
        elif message == "exit":
            client.close()
            break
        else:
            print(f"Client: {message}")

            response = input("Server: ")
            client.send(response.encode("utf-8"))


def receive_file(client):
    file_name = client.recv(1024).decode("utf-8")
    file_size = int(client.recv(1024).decode("utf-8"))

    with open(file_name, "wb") as file:
        while file_size > 0:
            data = client.recv(1024)
            file.write(data)
            file_size -= len(data)

    print(f"File {file_name} received")


start_server()
