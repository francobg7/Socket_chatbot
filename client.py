import socket
import threading

HOST = 'localhost'
PORT = 12345

def recibir_mensaje(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except ConnectionAbortedError:
            break

def enviar_mensaje(client_socket, user):
    while True:
        message = input()
        if message.lower() == 'salir':
            break
        full_message = f"{user}: {message}"
        client_socket.send(full_message.encode('utf-8'))

def main():
    user = input("Ingresa tu nombre de usuario: ")  # Solicitar nombre de usuario
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    receive_thread = threading.Thread(target=recibir_mensaje, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=enviar_mensaje, args=(client_socket, user))
    send_thread.start()

    send_thread.join()
    client_socket.close()

if __name__ == "__main__":
    main()
