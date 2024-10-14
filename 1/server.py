import socket
import struct


def server():
    host = get_local_ip()
    port = 9999

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)

    print(f"Server running on {host}:{port}")

    # 1. kullanici
    connection1, address1 = server_socket.accept()
    print(f"New client is connected from {address1}")
    connection1.sendall(struct.pack('BB', 0, 0) + "Waiting for other user...".encode('utf-8'))

    # 2. kullanici
    connection2, address2 = server_socket.accept()
    print(f"New client is connected from {address2}")

    print("Game is starting...")
    connection1.sendall(struct.pack('BB', 0, 0) + "Welcome to the game! First move is yours...".encode('utf-8'))
    connection2.sendall(struct.pack('BB', 0, 0) + "Welcome to the game! Waiting for rival first move...".encode('utf-8'))

    while True:
        connection1.sendall(struct.pack('BB', 1, 1) + "".encode('utf-8'))

        # İlk iki byte bayraklar olarak alınır
        flag1, flag2 = struct.unpack('BB', data[:2])  # İki bayrak
        # Geri kalan kısım metin olarak yorumlanır
        message = data[2:].decode('utf-8')


def get_local_ip():
    # Bağlantı oluşturup IP adresini bul
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Sahte bir bağlantı aç, internet erişimi gerekmez
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        ip_address = "IP adresi bulunamadı"
    finally:
        s.close()

    return ip_address





if __name__ == '__main__':
    server()
