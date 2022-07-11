import socket
from _thread import *


class Channel:
    def __init__(self, connection, receive_callback):
        self.__alive = True
        self.__connection = connection
        self.__file = self.__connection.makefile(mode='rw')
        self.receive_callback = receive_callback
        start_new_thread(self.__loop, ())

    def close(self):
        self.send('close')
        self.__connection.close()
        self.__alive = False

    def is_alive(self):
        return self.__alive

    def __loop(self):
        while self.__alive:
            try:
                data = self.__file.readline().split('\n')[0]
            except ConnectionResetError:
                pass
            if data == 'close':
                self.__connection.close()
                self.__connection = None
                self.__file = None
                self.__alive = False
            elif data == '':
                pass
            else:
                self.receive_callback(data)

    def send(self, string):
        if type(string) is str:
            self.__file.write(string + '\n')
            self.__file.flush()

            return True
        else:
            return False


class Server:

    def __init__(self, ip, port, backlog, connection_callback):
        self.listeningSocket = socket.socket()
        self.listeningSocket.bind((ip, port))
        self.listeningSocket.listen(backlog)
        self.connection_callback = connection_callback
        self.alive = True
        start_new_thread(self.__loop, ())

    def keep_alive(self):
        while self.alive:
            pass

    def __loop(self):
        while self.alive:
            connection = self.listeningSocket.accept()[0]
            self.connection_callback(connection)

    def close(self):
        self.alive = False
        self.listeningSocket.close()


class Client(Channel):
    def __init__(self, ip, port, receive_callback):
        self.connection = socket.socket()
        self.connection.connect((ip, port))
        super().__init__(self.connection, receive_callback)
