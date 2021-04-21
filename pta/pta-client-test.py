from socket import socket, AF_INET, SOCK_STREAM

# serverName = '127.0.0.1'
serverName = '127.0.0.1'
serverPort = 11550

apresented = False

while True:
    if not(apresented):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        # Conecta ao servidor
        clientSocket.connect((serverName, serverPort))

    # Recebe mensagem do usuario e envia ao servidor
    message = input('Digite uma frase: ')

    clientSocket.send(message.encode())

    modifiedMessage, addr = clientSocket.recvfrom(2048)

    print("Retorno do Servidor:", modifiedMessage.decode())

    try:
        msg = message.split(" ")[1]
        status = modifiedMessage.decode().split(" ")[1]

        if msg == "CUMP" and status == "OK":
            apresented = True
        elif msg == "TERM" and status == "OK":
            apresented = False
    except (IndexError):
        pass


clientSocket.close()
