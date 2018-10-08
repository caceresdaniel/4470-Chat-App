import select, socket, sys
import threading

# made socket class variable
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
currentIn = 0

class Server:
    peers = []

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
        listener()

    def handler(self,c,a):
        print("handler")
        while True:
            data = c.recv(1024)
            connections[currentIn].send(data)

    def run(self):
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            connections.append(c)


class Client:
    #host = socket.gethostname()
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Main problem: When we have to use the socket to connect, we can't use the inital socket we created when we started
# the chat.py app. I get a OSError. So we have to create a new socket to connect. The problem is we lose
# the port number associated with the old socket. Hence the new port number when the connection is establish.
# When u run the client app, run myport then do the connect. the port number is different.
# The prompt says:
# The output should display the IP address and the listening port of all the peers the process is connected to.
    def __init__(self, IPandPort):
        try:
            self.client_sock.connect(IPandPort)
        except WindowsError:
            print('Connect failed.')
            return
        print('The connection to peer ', self.client_sock.getpeername()[0], ' is successfully established kk')

        connections.append(self.client_sock)
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data)


def sendMsg(index, msg):
    i = index - 1
    global currentIn
    currentIn = i
    for x in range(len(connections)):
        if i == x:
            # connections[x].sendto(msg.encode('utf-8'),(connections[x].getpeername()[0], int(connections[x].getpeername()[1])))
            connections[x].send(bytes(msg, 'utf-8'))

def main(p):
    myServer = Server(int(p))
    myServer.run()
    listener()

def listener():
    validCommands = ['help', 'myip', 'myport', 'list', 'terminate', 'exit', 'connect', 'send']
    listener = input()
    listener = listener.lower()

    while(True):
        if(listener == 'help'):
            help()
            break
        elif(listener == 'myip'):
            myip()
            break
        elif(listener == 'myport'):
            myport()
            break
        elif ("connect" in listener):
            connect(listener)
            break
        elif(listener == 'list'):
            cList()
            break
        elif("send" in listener):
            send(listener)
            break
        elif(listener == 'terminate'):
            terminate()
            break
        elif(listener == 'exit'):
            exit()
        elif(listener not in validCommands):
            invalid()
            break

def help():
    print("\nmyip \n   display IP address")
    print("myport \n   display Port")
    print("connect \n   connects to a specific IP and Port, example format 'connect 192.0.0.0.1 2332'")
    print("list \n   lists all connected peers")
    print("send \n   sends a message to a selected connected peer, example format - 'send 2 hello how are you'")
    print("terminate \n   terminates a specified connection")
    print("exit \n   exits program")
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
    msg = sendInfo[2]
    sendMsg(index, msg)
    listener()


def terminate():
    print("not yet implemented")
    listener()

def invalid():
    print("Error Invalid command")
    listener()


if __name__ == "__main__":
    main(sys.argv[1])