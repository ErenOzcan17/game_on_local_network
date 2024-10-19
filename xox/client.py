import socket
import struct
import threading
import tkinter as tk
from tkinter import messagebox

turn_flag = True  # True if it's this client's turn
client_id = None
first_message = False
board = [' ' for _ in range(9)]  # 3x3 Tic-Tac-Toe board

def receive_messages(client_socket):
    global turn_flag, client_id
    while True:
        try:
            data = client_socket.recv(1024)
            if len(data) > 0:
                flag = struct.unpack('B', data[:1])[0]
                if flag == 0:  # Other client's move
                    move = struct.unpack('I', data[1:5])[0]
                    board[move] = 'O' if client_id == 0 else 'X'
                    update_board()
                    turn_flag = True
                elif flag == 1:  # Your turn
                    turn_flag = True
                    print("Your turn!")
        except Exception as e:
            print(f"Error receiving message: {e}")
            client_socket.close()
            break

def send_move(move):
    global turn_flag
    if turn_flag and board[move] == ' ':
        board[move] = 'X' if client_id == 0 else 'O'
        update_board()
        client_socket.sendall(struct.pack('I', move))
        turn_flag = False

def update_board():
    for i, val in enumerate(board):
        buttons[i].config(text=val)
    if check_winner():
        messagebox.showinfo("Game Over", f"Player {board[0]} wins!")
        reset_board()
    elif ' ' not in board:
        messagebox.showinfo("Game Over", "It's a draw!")
        reset_board()

def check_winner():
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                     (0, 3, 6), (1, 4, 7), (2, 5, 8),
                     (0, 4, 8), (2, 4, 6)]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] != ' ':
            return True
    return False

def reset_board():
    global board
    board = [' ' for _ in range(9)]
    update_board()

def create_buttons():
    for i in range(9):
        button = tk.Button(root, text=' ', font=('Arial', 24), width=5, height=2,
                           command=lambda i=i: send_move(i))
        button.grid(row=i//3, column=i%3)
        buttons.append(button)

def start_client(host, port=5555):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()


def listen_broadcast(port):
    # Broadcast mesajlarını dinlemek için bir UDP soketi oluştur
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Broadcast mesajlarını almak için soketi bağla
    sock.bind(("", port))

    print(f"Broadcast mesajlarını dinliyor... (Port: {port})")

    while True:
        # Gelen mesajları al
        data, addr = sock.recvfrom(1024)
        print(f"Broadcast mesajı alındı socket başlatılıyor")
        if data.decode('utf-8') == "Eren12345":
            start_client(addr[0])
            break

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    buttons = []
    create_buttons()
    listen_broadcast(5000)
    root.mainloop()
