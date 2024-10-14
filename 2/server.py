import socket
import threading

HOST = '192.168.1.101'  # localhost
PORT = 65432  # Kullanacağımız port

# Mesaj sırasını tutacak değişken
current_user = 0
messages = []


def handle_client(conn, addr):
    global current_user

    print(f'Bağlantı sağlandı: {addr}')
    while True:
        # Kullanıcının mesajını al
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode('utf-8')

        # Mesajı kaydet
        messages.append(message)
        print(f'Kullanıcı {addr} mesaj gönderdi: {message}')

        # Sıra değiştirme
        current_user = 1 - current_user

        # Diğer kullanıcıya mesajı gönder
        conn.sendall(f'Mesaj: {message}'.encode('utf-8'))
        print(f'Mesaj {addr} adresine gönderildi.')

    conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Sunucu başlatıldı {HOST}:{PORT}')

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == '__main__':
    start_server()
