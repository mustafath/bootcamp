# player.py
import socket
import threading

SERVER = "114.119.189.170"
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
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        message = f"{nickname}: {input('')}"
        client.send(message.encode("utf-8"))

if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()

