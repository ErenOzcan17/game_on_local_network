import socket
import struct
import threading

class Client:
    def __init__(self, socket, addr, client_id):
        self.client_id = client_id
        self.socket = socket
        self.addr = addr

clients = []
turn_flag = True  # True if it's client 0's turn, False for client 1
board = [' ' for _ in range(9)]  # 3x3 Tic-Tac-Toe board

def handle_client(client_obj):
    global turn_flag
    while True:
        try:
            if turn_flag and client_obj.client_id == 0:
                client_obj.socket.sendall(struct.pack('B', 1) + b'Your turn')
                data = client_obj.socket.recv(1024)
                if len(data) > 0:
                    move = struct.unpack('I', data[:4])[0]
                    board[move] = 'X'  # Client 0 is 'X'
                    clients[1].socket.sendall(struct.pack('B', 0) + struct.pack('I', move))
                    turn_flag = False

            elif not turn_flag and client_obj.client_id == 1:
                client_obj.socket.sendall(struct.pack('B', 1) + b'Your turn')
                data = client_obj.socket.recv(1024)
                if len(data) > 0:
                    move = struct.unpack('I', data[:4])[0]
                    board[move] = 'O'  # Client 1 is 'O'
                    clients[0].socket.sendall(struct.pack('B', 0) + struct.pack('I', move))
                    turn_flag = True
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_obj.socket.close()
    clients.remove(client_obj)


def get_local_ip():
    # Bağlantı oluşturup IP adresini bul
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        ip_address = "IP adresi bulunamadı"
    finally:
        s.close()
    return ip_address


def start_server(host=get_local_ip(), port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)

    print(f"Server {host}:{port} is listening...")

    while True:
        client_socket, client_addr = server.accept()
        print(f"{client_addr} connected.")
        client_id = len(clients)  # First client id = 0, second id = 1
        client_obj = Client(client_socket, client_addr, client_id)
        clients.append(client_obj)
        if len(clients) == 2:
            break

    for client in clients:
        client_thread = threading.Thread(target=handle_client, args=(client,))
        client_thread.start()


if __name__ == "__main__":
    start_server()
