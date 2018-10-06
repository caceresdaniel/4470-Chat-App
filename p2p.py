import select, socket, sys
import threading

# made socket class variable
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []


class Server:
    peers = []

    def __init__(self, port):
        host = socket.gethostname()
        sock.bind((host, port))
        sock.listen(1)
        iThread = threading.Thread(target=self.run)
        iThread.daemon = True
        iThread.start()
        print('server is running')
        listener()

    def handler(self,c,a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send((data))
            if not data:
                print('IP: ', str(a[0]) + '\nPort:' + str(a[1]), "disconnected")
                connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
                c, a = sock.accept()
                cThread = threading.Thread(target=self.handler, args=(c,a))
                cThread.daemon = True
                cThread.start()
                connections.append(c)
                print('IP: ', str(a[0]) + '\nPort:' + str(a[1]), "connected")





class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #host = socket.gethostname()

    # def sendMsg(self):
    #         while True:
    #             sock.send(bytes(input(""), 'utf-8'))


#Main problem: When we have to use the socket to connect, we can't use the inital socket we created when we started
#the chat.py app. I get a OSError. So we have to create a new socket to connect. The problem is we lose
#the port number associated with the old socket. Hence the new port number when the connection is establish.
#When u run the client app, run myport then do the connect. the port number is different.
#The prompt says:  The output should display the IP address and the listening port
# of all the peers the process is connected to.
    def __init__(self, IPandPort):
        print('client started')
        self.sock.connect(IPandPort)

        #This won't work but it should cuz its using the old port
        #sock.connect(IPandPort)

        #
        # while True:
        #         data = self.sock.recv(1024)
        #         if not data:
        #                 break
        #         print(data)


def main(p):
    myServer = Server(int(p))
    myServer.run()
    listener()

def listener():
    print("listener")
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
        elif(listener == 'send'):
            send()
            break
        elif(listener == 'terminate'):
            terminate()
            break
        elif(listener == 'exit'):
            exit()
        else:
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
    for x in connections:
        print(x)
    listener()


def send():
    print("not yet implemented")
    listener()


def terminate():
    print("not yet implemented")
    listener()


if __name__== "__main__":
    main(sys.argv[1])