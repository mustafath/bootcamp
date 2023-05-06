import socket
import threading

SERVER = "119.8.174.146"
PORT = 5555
ADDR = (SERVER, PORT)

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                print(message)
                if "won!" in message or "tied!" in message:
                    write()
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    move = input("Enter your move (rock/paper/scissors): ").lower()
    message = f"{nickname}: {move}"
    client.send(message.encode("utf-8"))

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

