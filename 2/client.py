import socket

# Sunucu ayarları
HOST = '192.168.1.101'  # localhost
PORT = 65432  # Kullanacağımız port


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            # Kullanıcıdan mesaj al
            message = input("Mesajınızı girin: ")
            s.sendall(message.encode('utf-8'))

            # Sunucudan yanıt al
            data = s.recv(1024)
            print('Sunucudan yanıt:', data.decode('utf-8'))


if __name__ == '__main__':
    start_client()