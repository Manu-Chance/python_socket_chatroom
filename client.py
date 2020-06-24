import socket
import select
import errno
import sys

HEADER = 10

IP = '127.0.0.1'
PORT = 5555
ADDR = IP, PORT

my_username = input("Username:> ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(ADDR)
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username}:> ")

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message) :< {HEADER}}".encode('utf-8')
        client_socket.send(message_header + message)
    
    try:
        while True:
            username_header = client_socket.recv(HEADER)
            if not len(username_header):
                print("[CONNECTION CLOSED]")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} :> {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('reading error', str(e))
            sys.exit()
        continue



    except Exception as e:
        print('General error', str(e))