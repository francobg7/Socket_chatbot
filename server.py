import socket
import select

HOST = 'localhost'
PORT = 12345

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor escuchando en {HOST}:{PORT}")

    sockets_list = [server_socket]
    clients = {}

    def broadcast_message(message, sender_socket):
        for client_socket in clients:
            if client_socket != sender_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except BrokenPipeError:
                    handle_disconnection(client_socket)

    def handle_disconnection(client_socket):
        print(f"Cliente {clients[client_socket]} desconectado")
        sockets_list.remove(client_socket)
        del clients[client_socket]
        client_socket.close()

    while True:
        readable, _, _ = select.select(sockets_list, [], [])

        for notified_socket in readable:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                sockets_list.append(client_socket)
                clients[client_socket] = client_address
                print(f"Cliente {client_address} conectado")
            else:
                try:
                    message = notified_socket.recv(1024).decode('utf-8')
                    if not message:
                        raise ConnectionResetError
                    print(f"Mensaje recibido de {clients[notified_socket]}: {message}")
                    broadcast_message(message, notified_socket)
                except (ConnectionResetError, BrokenPipeError):
                    handle_disconnection(notified_socket)

if __name__ == "__main__":
    main()
