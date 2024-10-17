import socket
import struct


def client():
    host = '10.138.135.133'
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        data = client_socket.recv(1024)
        flag1, flag2 = struct.unpack('BB', data[:2])
        message = data[2:].decode('utf-8')

        if flag1 == 0 and (flag2 == 0 or flag2 == 1):
            print(message)
        elif flag1 == 1 and flag2 == 1:
            # TODO: Hamle yapılır
            print("Hamle yapıldı.")
        elif flag1 == 1 and flag2 == 0:
            # TODO: Karşı hamle beklenir
            print("Karşı hamle bekleniyor.")


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
