import socket
import threading


# localhost for local testing, and any random free port
HOST = '127.0.0.1'
PORT = 5001

# creating socket object using (IPv4 + TCP)
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


#Binding the socket
server_socket.bind((HOST, PORT))

# Listening connections
server_socket.listen()
print(f'[*] Server listening on {HOST}:{PORT}')

clients = []
client_usernames = {}
# Sending message so that all clients can see it (broadcasting)
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except socket.error as err:
                print(str(err))
                client.close()
                clients.remove(client)

# Function to handle newly connected clients
def handle_clients(client_socket, address):
    username = client_socket.recv(1024).decode()
    clients.append(client_socket)
    client_usernames[client_socket] = username
    print(f'[+] New connection {address} with username - {username}')

    while True:
        try:
            message = client_socket.recv(2048)
            if not message:
                break # Client disconnected
            print(f'{username}: {message.decode()}')
            broadcast(message, client_socket)
        except socket.error as err:
            print(str(err))
            print(f'[-] {address} Disconnected')
            if client_socket in clients:
                clients.remove(client_socket)
            client_usernames.pop(client_socket, None)  # Also remove from username dict safely
            client_socket.close()


def start_server():
    print('[SERVER STARTED AND ACCEPTING CLIENTS]')
    while True:
        client_socket, address = server_socket.accept()
        thread = threading.Thread(target=handle_clients, args=(client_socket, address))
        thread.start()
        print(f'\n[ACTIVE CONNECTIONS] {threading.active_count() - 1}')     # -1 as a thread is created for server itself

if __name__ == '__main__':
    start_server()