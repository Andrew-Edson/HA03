import socket
import threading
import os


# Starts server and binds to socket 12345
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 12345))
    server.listen(5)
    print("Server started")

    # Accepts client connections and starts a new thread for each client
    while True:
        client, addr = server.accept()
        print(f"Connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()


# Handles client messages and file transfers
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

            response = input("Server Response (Input 'FILE' to send a file)\n")
            if response == "FILE":
                send_file(client)
            else:
                client.send(response.encode("utf-8"))


# Receives file from client
def receive_file(client):
    file_name = client.recv(1024).decode("utf-8")
    file_size = int(client.recv(1024).decode("utf-8"))

    with open(f"server_files\{file_name}", "wb") as file:
        while file_size > 0:
            data = client.recv(1024)
            file.write(data)
            file_size -= len(data)

    print(f"File {file_name} received")


# Sends file to client
def send_file(client):
    file_path = input("Enter file path: ")

    if os.path.exists(file_path):

        client.send("FILE".encode("utf-8"))
        file_name = os.path.basename(file_path)
        client.send(file_name.encode("utf-8"))
        file_size = os.path.getsize(file_path)
        client.send(str(file_size).encode("utf-8"))

        with open(file_path, "rb") as file:
            while file_size > 0:
                data = file.read(1024)
                client.send(data)
                file_size -= len(data)

        print(f"File {file_name} sent")
    else:
        print("File not found")


# Starts server
start_server()
