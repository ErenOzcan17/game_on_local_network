import select
import socket
import struct

def server():
    host = get_local_ip()
    port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print(f"Server running on {host}:{port}")

    # 1. kullanıcı
    connection1, address1 = server_socket.accept()
    print(f"New client connected from {address1}")
    connection1.sendall(struct.pack('BB', 0, 0) + "Waiting for other user...".encode('utf-8'))

    # 2. kullanıcı
    connection2, address2 = server_socket.accept()
    print(f"New client connected from {address2}")

    print("Game is starting...")
    connection1.sendall(struct.pack('BB', 0, 0) + "Welcome to the game! First move is yours...".encode('utf-8'))
    connection2.sendall(struct.pack('BB', 0, 0) + "Welcome to the game! Waiting for rival's first move...".encode('utf-8'))

    connection1.sendall(struct.pack('BB', 1, 1) + "".encode('utf-8'))

    connections = [connection1, connection2]
    while True:
        # Veri alınabilir bağlantıları kontrol et
        read_sockets, _, _ = select.select(connections, [], [])

        for sock in read_sockets:
            if sock == connection1:
                handle_client_message(sock, connection2)

            elif sock == connection2:
                handle_client_message(sock, connection1)


def handle_client_message(sock, target_sock):
    data = sock.recv(1024)
    if data:
        target_sock.sendall(data)
    else:
        print(f"Connection closed: {sock.getpeername()}")
        sock.close()


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

if __name__ == "__main__":
    server()
