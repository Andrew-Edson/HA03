import socket
import os


# Starts client and connects to server
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 12345))
    print("Client connected")

    while True:

        message = input(
            "Enter Message (Input 'FILE' to send a file) (Input 'exit' to disconnect)\n"
        )

        if message == "FILE":
            send_file(client)
        elif message == "exit":
            client.send("exit".encode("utf-8"))
            break
        else:
            client.send(message.encode("utf-8"))
            response = client.recv(1024).decode("utf-8")
            if response == "FILE":
                recieve_file(client)
            print(f"Server: {response}")


# Sends file to server
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


# Receives file from server
def recieve_file(client):
    file_name = client.recv(1024).decode("utf-8")
    file_size = int(client.recv(1024).decode("utf-8"))

    with open(f"client_files\{file_name}", "wb") as file:
        while file_size > 0:
            data = client.recv(1024)
            file.write(data)
            file_size -= len(data)

    print(f"File {file_name} received")


# Starts client
start_client()
