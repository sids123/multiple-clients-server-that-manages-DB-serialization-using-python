import pickle
import socket
from threading import Thread

class database():
    def __init__(self):
        self.database_dict = {}
        pickle.dump(self.database_dict, open("database.p", "wb"))

    def read(self, key=""):
        self.database_dict = pickle.load(open("database.p", "rb"))
        info = ""
        if key == "":
            info = str(self.database_dict)
        else:
            info = str(self.database_dict[key])
        pickle.dump(self.database_dict, open("database.p", "wb"))
        return info

    def write(self, key, value):
        self.database_dict = pickle.load(open("database.p", "rb"))
        self.database_dict[key] = value
        pickle.dump(self.database_dict, open("database.p", "wb"))

class databse_synchronized(database):
    def __init__(self):
        self.d = database()
        self.users = [False, 0]


    def read(self, sock):
        if self.users[1]  == 10 or self.users[0] == True:
            sock.send("cannot connect to database now. try again later".encode())
        else:
            sock.send("access granted".encode())
            self.users[1] += 1
            data = sock.recv(1024).decode()
            while data != 'q':
                if data == "all":
                    sock.send(self.d.read().encode())
                else:
                    sock.send(self.d.read(key=data).encode())
                data = sock.recv(1024).decode()
            self.users[1] -= 1

    def write(self, sock):
        if self.users[0] == True or self.users[1] > 0:
            sock.send("cannot connect to database now. try again later".encode())
        else:
            sock.send("access granted".encode())
            self.users[0] = True
            data = sock.recv(1024).decode()
            data = data.split()
            while data[0] != 'q':
                self.d.write(key=data[0], value=data[1])
                sock.send("database changed successfully".encode())
                data = sock.recv(1024).decode()
                data = data.split()
            self.users[0] = False

class ClientThread(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn

    def run(self):
        data = self.conn.recv(1024).decode()
        while data != "exit":
            if data == "read":
                db.read(self.conn)
            else:
                db.write(self.conn)
            data = self.conn.recv(1024).decode()
        self.conn.send("bye bye".encode())
        self.conn.close()

global db
db = databse_synchronized()

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind(("127.0.0.1", 2004))

while True:
    tcpServer.listen()

    (conn, (ip, port)) = tcpServer.accept()
    new_client = ClientThread(ip, port, conn)
    new_client.start()