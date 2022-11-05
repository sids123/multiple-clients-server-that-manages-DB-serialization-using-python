import socket

def main():
    port = 2004
    BUFFER_SIZE = 2048
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("127.0.0.1", port))

    MESSAGE = ""

    MESSAGE = input("what do you want to do?\n")
    sock.send(MESSAGE.encode())

    while MESSAGE != "exit":
        read_or_write(sock)

        MESSAGE = input("what do you want to do?\n")
        sock.send(MESSAGE.encode())

    data = sock.recv(BUFFER_SIZE).decode()
    print(data)

    sock.close()

def read_or_write(sock):
    data = sock.recv(2048).decode()
    print(data)
    if data == "cannot connect to database now. try again later":
        return

    message = ""
    while True:
        message = input()
        sock.send(message.encode())
        if message == 'q':
            return
        try:
            data = sock.recv(2048).decode()
            print(data)
        except:
            None

if __name__ == "__main__":
    main()