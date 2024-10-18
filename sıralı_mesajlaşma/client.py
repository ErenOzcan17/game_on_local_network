import socket
import struct
import threading

turn_flag = True # sıralamayı tutar. True ise mevcut client ta
client_id = 0
#x değişkenini koyma sebebim client 2 olduğumuz durumda flag 0 geldiğinde sıranın karşıda olduğunu yazdıracak koşula girebilmek
first_message = False


def receive_messages(client_socket):
    global turn_flag
    global first_message
    global client_id
    while True:
        try:
            data = client_socket.recv(1024)
            if len(data) > 0:
                flag = struct.unpack('B', data[:1])[0]
                rec_message = data[1:].decode('utf-8')

                # bu koşulu koyma sebebim ilk bekletme mesajını atabilmek
                if flag == 0 and not first_message:
                    first_message = True
                    client_id = 1
                    print("client id = " + str(client_id))
                    print("Sıra diğer istemcide, lütfen bekleyin.")
                if flag == 1 and not first_message:
                    first_message = True
                    client_id = 0
                    print("client id = " + str(client_id))

                if flag == 1 and turn_flag:
                    turn_flag = False
                    print("gelen mesaj: {" + str(rec_message) + "}")
                    print("Sıra sizde, mesaj gönderebilirsiniz.")
                    send_message = input("Mesajınızı yazın: ")
                    client_socket.sendall(struct.pack('B', 1) + send_message.encode('utf-8'))
                elif flag == 0 and not turn_flag:
                    turn_flag = True
                    print("Sıra diğer istemcide, lütfen bekleyin.")


        except Exception as e:
            print(f"Error receiving message: {e}")
            break



def start_client(host='192.168.1.101', port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Mesajları almak için ayrı bir thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

if __name__ == "__main__":
    start_client()
