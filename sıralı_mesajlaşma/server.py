import socket
import struct
import threading


class Client:
    def __init__(self, socket, addr, client_id):
        self.client_id = client_id
        self.socket = socket
        self.addr = addr


clients = []
turn_flag = True  # sıralamayı tutar. True ise 0. client / False ise 1. client

def handle_client(client_obj):
    global turn_flag
    while True:
        try:
            if turn_flag and client_obj.client_id == 0:
                client_obj.socket.sendall(struct.pack('B', 1) + "".encode('utf-8'))
                clients[1].socket.sendall(struct.pack('B', 0) + "".encode('utf-8'))
                data = client_obj.socket.recv(1024)
                if len(data) > 0:
                    # Check if we have at least 1 byte to unpack
                    flag = struct.unpack('B', data[:1])[0]  # Unpack needs a tuple, so index into it
                    message = data[1:].decode('utf-8')
                    if message and flag == 1:
                        print(f"Client {client_obj.client_id} mesaj gönderdi: {message}")
                        client_obj.socket.sendall(struct.pack('B', 0) + "".encode('utf-8'))
                        clients[1].socket.sendall(struct.pack('B', 1) + message.encode('utf-8'))
                        turn_flag = False

            elif not turn_flag and client_obj.client_id == 1:
                client_obj.socket.sendall(struct.pack('B', 1) + "".encode('utf-8'))
                clients[0].socket.sendall(struct.pack('B', 0) + "".encode('utf-8'))
                data = client_obj.socket.recv(1024)
                if len(data) > 0:
                    flag = struct.unpack('B', data[:1])[0]
                    message = data[1:].decode('utf-8')
                    if message and flag == 1:
                        print(f"Client {client_obj.client_id} mesaj gönderdi: {message}")
                        client_obj.socket.sendall(struct.pack('B', 0) + "".encode('utf-8'))
                        clients[0].socket.sendall(struct.pack('B', 1) + message.encode('utf-8'))
                        turn_flag = True
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_obj.socket.close()
    clients.remove(client_obj)


def start_server(host='192.168.1.101', port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)

    print(f"Server {host}:{port} adresinde dinliyor...")

    while True :
        client_socket, client_addr = server.accept()
        print(f"{client_addr} bağlandı.")
        client_id = len(clients)  # İlk bağlanan client id = 0, ikinci id = 1
        client_obj = Client(client_socket, client_addr, client_id)
        clients.append(client_obj)
        if len(clients) == 2:
            break

def start_handling():
    for client in clients:
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()


if __name__ == "__main__":
    start_server()
    start_handling()
