import socket
import threading


class Client:
    def __init__(self, socket, addr, client_id):
        self.client_id = client_id
        self.socket = socket
        self.addr = addr


clients = []
turn = 0  # İlk bağlanan client'ın mesaj gönderme sırası

# İstemci mesaj gönderme/alma işlemi
def handle_client(client_obj):
    global turn
    while True:
        try:
            # Sıranın kimde olduğunu client'a bildir
            for i, client in enumerate(clients):
                if i == turn:
                    client.send(b"your_turn")
                else:
                    client.send(b"wait")

            # Sırası gelen client mesaj atabilir
            if turn == client_obj.client_id:
                message = client_obj.socket.recv(1024)
                if message:
                    print(f"Client {client_obj.client_id + 1} mesaj gönderdi: {message.decode('utf-8')}")

                    # Diğer client'a mesajı gönder
                    for client in clients:
                        if client.client_id != client_obj.client_id:
                            client.send(message)

                    # Sıra diğer client'a geçiyor
                    turn = (turn + 1) % 2
                else:
                    break
        except:
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
