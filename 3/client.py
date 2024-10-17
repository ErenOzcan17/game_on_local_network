import selectors
import socket
import struct
import sys

def client():
    host = '192.168.1.107'  # Sunucu IP adresi
    port = 9999

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    selector = selectors.DefaultSelector()
    selector.register(client_socket, selectors.EVENT_READ)

    print("Connected to the server. Waiting for messages...")

    try:
        while True:
            events = selector.select()
            for key, _ in events:
                if key.fileobj == client_socket:
                    data = client_socket.recv(1024)
                    if data:
                        handle_data(data)
                    else:
                        print("Connection closed by the server.")
                        client_socket.close()
                        sys.exit(0)
    except KeyboardInterrupt:
        print("Client exiting...")
    finally:
        client_socket.close()

def handle_data(data):
    flag1, flag2 = struct.unpack('BB', data[:2])
    message = data[2:].decode('utf-8')

    if flag1 == 0 and (flag2 == 0 or flag2 == 1):
        print(message)
    elif flag1 == 1 and flag2 == 1:
        # Hamle yapılır
        input("Lütfen hamle yapacağınız kareyi giriniz: ")
    elif flag1 == 1 and flag2 == 0:
        # Karşı hamle beklenir
        print("Karşı hamle bekleniyor.")

if __name__ == "__main__":
    client()
