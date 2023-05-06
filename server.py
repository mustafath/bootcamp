# server.py
import socket
import threading

SERVER = "localhost"
PORT = 5555
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat!".encode("utf-8"))
            break

def receive():
    while True:
        client, addr = server.accept()
        print(f"Connected with {addr}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of client is {nickname}!")
        broadcast(f"{nickname} joined the chat!".encode("utf-8"))
        client.send("Connected to the server!".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    print("Server started...")
    server.listen()
    receive()

