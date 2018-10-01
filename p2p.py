import select, socket, sys
import threading

class Server:
    connections = []
    peers = []
    host = socket.gethostname()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handler(self):
        self.sock.listen(1)
        c,a = self.sock.accept()
        print(str(a[0]) + ':' + str(a[1]), "connected")
        print(a)
        print(c)
        # while True:
        #     data = c.recv(1024)
        #     for connection in self.connections:
        #         connection.send((data))
        #     if not data:
        #         print(str(a[0]) + ':' + str(a[1]), "disconnected")
        #         self.connections.remove(c)
        #         c.close()
        #         break

    def __init__(self, port):
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = socket.gethostname()

        self.sock.bind((host, port))

        #sock.listen(1)
        print("Server running...")
        iThread = threading.Thread(target=self.handler)
        iThread.daemon = True
        iThread.start()
        listener()



# class Client:
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     host = socket.gethostname()
#
#
#     def sendMsg(self):
#             while True:
#                 self.sock.send(bytes(input(""), 'utf-8'))
#
#     def __init__(self, port):
#             self.sock.connect((host, port))
#
#             iThread = threading.Thread(target=self.sendMsg)
#             iThread.daemon = True
#             iThread.start()
#
#             while True:
#                     data = self.sock.recv(1024)
#                     if not data:
#                             break
#                     print(data)
def main(p):
    myServer = Server(int(p))
    #sock = socket.socket()
    #host = socket.gethostname()
    #global port
    #port = int(p)
    #sock.bind((host,port))
    #sock.listen(5)
    #connection = None

    listener()

def listener():
    print("listener")
    ex = True
    listener = input()
    listener = listener.lower()

    while(ex):
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


def listener2():
    ex = True
    listener = input()
    listener = listener.lower()

    while(ex):
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
    global host
    host = socket.gethostbyname(hostname)
    print("The IP address is: ", host, "\n")
    listener()

def myport():
    print("The program runs on port ")
    listener()

def connect(conString):
    # parse
    socketInfo = conString.split(" ")
    #print('IP: ',socketInfo[1:2], ' Port: ', socketInfo[-1])
    ip = socketInfo[1]
    #print('type:')
    #print(type(ip))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socketInfo[1], int(socketInfo[-1])))
    s.sendall(bytes('IM INSIDE!', 'utf-8'))
    #print('connected? ', s)
    listener()

def cList():
    print("not yet implemented")
    listener()

def send():
    print("not yet implemented")
    listener()

def terminate():
    print("not yet implemented")
    listener()

if __name__== "__main__":
    main(sys.argv[1])