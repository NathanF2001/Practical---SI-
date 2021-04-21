from socket import *
import os

serverPort = 11550
# Cria o Socket TCP (SOCK_STREAM) para rede IPv4 (AF_INET)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
# Socket fica ouvindo conexoes. O valor 1 indica que uma conexao pode ficar na fila
serverSocket.listen(1)

print("Servidor pronto para receber mensagens. Digite Ctrl+C para terminar.")


def load_users():
    cur_path = os.path.dirname(__file__)

    file_users = open(f"{cur_path}/pta-server/users.txt", 'r')
    users_string = file_users.read()
    list_users = users_string.split('\n')
    list_users = list_users[:-1]

    return list_users


def valid_user(user, list_users):
    return user in list_users


def LIST():
    cur_path = os.path.dirname(__file__)

    list_files = os.listdir(f"{cur_path}/pta-server/files")
    return list_files


def PEGAR(name):
    cur_path = os.path.dirname(__file__)

    file_users = open(f"{cur_path}/pta-server/files/{name}", 'rb')
    bytes_file = file_users.read()
    size = os.stat(f"{cur_path}/pta-server/files/{name}").st_size

    return bytes_file, size

    # Variáveis utilizadas no servidor


list_users = load_users()

apresented = False

while 1:
    try:

        # Cria um socket para tratar a conexao do cliente
        if not(apresented):

            connectionSocket, addr = serverSocket.accept()

        msg = connectionSocket.recv(1024).decode()

        # Caso comando seja
        if msg == "exit":
            break

        try:
            capitalizedMsg = msg.lower()
            msg_list = capitalizedMsg.split(" ")
            if len(msg_list) < 2:
                Seq_num = -1
                raise IndexError
            elif len(msg_list) == 2:
                if msg_list[1] in ["cump", "pega"]:
                    raise ValueError
                Seq_num, command = msg_list
            elif len(msg_list) == 3:
                Seq_num, command, args = msg_list
            else:
                Seq_num = -1
                raise IndexError
            if apresented:
                if command == "list":
                    list_files = LIST()
                    returnMsg = Seq_num + " ARQS " + \
                        f"{len(list_files)} " + ",".join(list_files)
                elif command == "pega":
                    bytes_file, size_file = PEGAR(args)
                    returnMsg = f"{Seq_num} ARQ {size_file} {bytes_file}"
                elif command == "term":
                    returnMsg = f"{Seq_num} OK"
                    apresented = False
            else:
                if command != "cump":
                    raise ValueError

                isverified = valid_user(args, list_users)

                if isverified:
                    apresented = True
                    returnMsg = f"{Seq_num} OK"
                else:
                    raise ValueError
        except (ValueError, IndexError, FileNotFoundError):
            returnMsg = f"{Seq_num} NOK"

        connectionSocket.send(returnMsg.encode())

        if not(apresented):
            connectionSocket.close()

    except (KeyboardInterrupt, SystemExit):
        print("Ctrl+C pressed")
        break

serverSocket.shutdown(SHUT_RDWR)
serverSocket.close()
