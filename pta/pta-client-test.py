from socket import socket, AF_INET, SOCK_STREAM

# serverName = '127.0.0.1'
serverName = '127.0.0.1'
serverPort = 11550
clientSocket = socket(AF_INET, SOCK_STREAM)

# Conecta ao servidor
clientSocket.connect((serverName, serverPort))
cnt = 0
# Recebe mensagem do usuario e envia ao servidor
message = input('Digite uma frase: ')
print(message.encode())
clientSocket.send(message.encode())


modifiedMessage, addr = clientSocket.recvfrom(4096)

print("Retorno do Servidor:", modifiedMessage.decode())

clientSocket.close()
