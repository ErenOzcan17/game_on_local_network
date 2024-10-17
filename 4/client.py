import socket
import threading

turn_flag = False  # İstemci sırasını belirleyecek bayrak

# Diğer client'tan gelen mesajları alma
def receive_messages(client_socket):
    global turn_flag
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "your_turn" and turn_flag == False:
                turn_flag = True
                print("Sıra sizde, mesaj gönderebilirsiniz.")
            if message == "wait" and turn_flag == True:
                turn_flag = False
                print("Sıra diğer istemcide, lütfen bekleyin.")

        except:
            break

# Client'ın başlatılması
def start_client(host='192.168.1.101', port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Mesajları almak için ayrı bir thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Mesaj gönderme işlemi
    while True:
        if turn_flag:
            try:
                message = input("Mesajınızı yazın: ")
                client_socket.send(message.encode('utf-8'))
            except:
                break

if __name__ == "__main__":
    start_client()
