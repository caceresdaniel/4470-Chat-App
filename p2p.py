import select, socket, sys
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []


class Server:
    def __init__(self, port):
        host = socket.gethostname()
        try:
            sock.bind((host, port))
        except WindowsError:
            print('Failed to create socket')
            exit()
        sock.listen(1)
        iThread = threading.Thread(target=self.run)
        iThread.daemon = True
        iThread.start()
        print('server is running')
        listener()

    def handler(self, c ,a):
        while True:
            data = c.recv(1024)
            print(data.decode("utf-8"))

    def run(self):
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            connections.append(c)
            print('The connection to peer ', c.getpeername()[0], ' is successfully established ')


class Client:

    def handler2(self, c, a):
        while True:
            data = c.recv(1024)
            print(data.decode("utf-8"))

    def __init__(self, IPandPort):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print('Connecting...')
            client_sock.connect(IPandPort)
        except WindowsError:
            print('Connect failed.')
            return
        print('client started')
        print('The connection to peer ', client_sock.getpeername()[0], ' is successfully established ')
        cThread = threading.Thread(target=self.handler2, args=(client_sock,None))
        cThread.daemon = True
        cThread.start()
        connections.append(client_sock)



def sendMsg(index, message):
    connections[index].send(bytes(message, 'utf-8'))


def main(p):
    myServer = Server(int(p))
    myServer.run()
    listener()

def invalid():
    print("Error Invalid command")
    listener()

def listener():
    print("listener")
    listener = input()
    listener = listener.lower()
    validCommands = ['help', 'myip', 'myport', 'list', 'terminate', 'exit', 'connect', 'send']

    while(True):
        if listener == 'help':
            help()
            break
        elif listener == 'myip':
            myip()
            break
        elif listener == 'myport':
            myport()
            break
        elif "connect" in listener:
            connect(listener)
            break
        elif listener == 'list':
            cList()
            break
        elif "send" in listener:
            send(listener)
            break
        elif listener == 'terminate':
            terminate()
            break
        elif listener == 'exit':
            exit()
        elif listener not in validCommands:
            invalid()
            break


def help():
    print("myip display IP address")
    print("myport display Port")
    print("connect connects to a specific IP and Port")
    print("list lists all connected peers")
    print("send sends a message to a selected connected peer")
    print("terminate terminates a specified connection")
    print("exit exits program")
    listener()


def myip():
    hostname = socket.gethostname()
    host = socket.gethostbyname(hostname)
    print("The IP address is: ", sock.getsockname()[0], "\n")
    listener()


def myport():
    print("The program runs on port ", sock.getsockname()[1])
    listener()


def connect(conString):
    # parse
    socketInfo = conString.split(" ")
    client = Client((socketInfo[1], int(socketInfo[-1])))
    listener()


def cList():
    print('id: \t IP address \t Port No.')
    for x in range(len(connections)):
        print(x+1, '\t', connections[x].getpeername()[0], '\t',  connections[x].getpeername()[1])
    listener()


def send(senString):
    sendInfo = senString.split(" ", 2)
    index = int(sendInfo[1])
    msg = ''.join(sendInfo[2:])
    sendMsg(index, msg)
    listener()


def terminate():
    print("not yet implemented")
    listener()


if __name__ == "__main__":
    main(sys.argv[1])