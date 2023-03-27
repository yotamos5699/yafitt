
import socket
import datetime


def initiateHost(host):
    if host:
        return host
    return socket.gethostbyname(socket.gethostname())


def getStreamType(s_type):
    if s_type:
        return s_type
    return socket.SOCK_STREAM


class Socket:
    def __init__(self, port, host=None, STREAM_TYPE=None):
        self.starting_time = datetime.datetime.now()
        self.host = initiateHost(host)
        self.port = port
        self.address = (self.host, self.port)
        self.server = socket.socket(
            socket.AF_INET, getStreamType(socket.SOCK_STREAM))
        self.server.bind(self.address)

    def __str__(self):
        return 'address:' + str(self.address)

    def object(self):
        return {
            "host": self.host,

        }

    def initServer(self):
        return self.socket.bind(self.address)

    def run_time(self):
        now = datetime.datetime.now()
        return self.starting_time-now
