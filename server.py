import socket
import threading

SERVER = "0.0.0.0"
PORT = 5555
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = []
nicknames = []
moves = {}

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            nickname, move = message.split(": ")
            moves[nickname] = move

            if len(moves) == 2:
                player1, move1 = list(moves.items())[0]
                player2, move2 = list(moves.items())[1]

                if move1 == move2:
                    result = f"{player1} and {player2} tied!"
                elif (move1 == "rock" and move2 == "scissors") or (move1 == "paper" and move2 == "rock") or (move1 == "scissors" and move2 == "paper"):
                    result = f"{player1} won!"
                else:
                    result = f"{player2} won!"

                broadcast(result.encode("utf-8"))
                moves.clear()
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

