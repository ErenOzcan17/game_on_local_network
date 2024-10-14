import selectors
import socket
import struct


def client():
    host = '192.168.1.101'
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Selector oluştur
    selector = selectors.DefaultSelector()
    selector.register(client_socket, selectors.EVENT_READ)

    try:
        while True:
            # İstemci soketinden veriyi dinle
            events = selector.select()
            for key, _ in events:
                if key.fileobj is client_socket:
                    data = client_socket.recv(1024)
                    if not data:
                        print("Bağlantı kapandı.")
                        break
                    if handle_data(data):
                        break  # Handle_data döngüyü kırıyorsa, çık
    finally:
        selector.unregister(client_socket)
        client_socket.close()


def handle_data(data):
    flag1, flag2 = struct.unpack('BB', data[:2])
    message = data[2:].decode('utf-8')

    if flag1 == 0 and (flag2 == 0 or flag2 == 1):
        print(message)
    elif flag1 == 1 and flag2 == 1:
        # TODO: Hamle yapılır
        print("Hamle yapıldı.")
        return True  # Döngüyü kırmak için
    elif flag1 == 1 and flag2 == 0:
        # TODO: Karşı hamle beklenir
        print("Karşı hamle bekleniyor.")
        return True  # Döngüyü kırmak için

    return False


def chess_board(move):
    board = [
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " ", " ", " ", " "],
    ]
    print("  a  b  c  d  e  f  g  h")
    for i in range(8):
        print(8 - i, end=" ")
        for j in range(8):
            print(board[i][j], end=" ")
        print(8 - i)
    print("  a  b  c  d  e  f  g  h")


if __name__ == '__main__':
    client()
