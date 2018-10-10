import select, socket, sys
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []

#server class that creates a server for each client that is launched
#that way each client is a user
class Server:
    #init method that starts off the server
    def __init__(self, port):
        #getting the host name (IP) using sockets
        host = socket.gethostname()
        try:
            #setting the ip and port to a socket
            sock.bind((host, port))
        except WindowsError:
            print('Failed to create socket')
            exit()
        #enable the server to accept connections by using sock.listen
        sock.listen(1)
        #creating a thread for the run function
        iThread = threading.Thread(target=self.run)
        #setting a thread to a daemon allows it to shut down while there are still threads running 
        iThread.daemon = True
        iThread.start()
        listener()

    #this is the part of code where the server receives the message from the client
    def handler(self, c ,a):
        while True:
            #added try/except for when a client disconnects in a weird way
            try:
                data = c.recv(1024)
                print(data.decode("utf-8"))
            except socket.error:
                print('Peer ', c.getpeername()[0] ,' terminates the connection')
                if len(connections) > 0 and c in connections:
                    connections.remove(c)
                    c.close()
                return
            #checks to see if it receiving data from a socket if is not receiving data the socket is then removed and closed
            if not data:
                print('Peer ', c.getpeername()[0] ,' terminates the connection')
                if len(connections) > 0 and c in connections:
                    connections.remove(c)
                    c.close()
                break

    #function that accepts the connection from the client and adds the connection to the list of sockets
    def run(self):
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.handler, args=(c,a))
            cThread.daemon = True
            cThread.start()
            connections.append(c)
            print('The connection to peer ', c.getpeername()[0], ' is successfully established ')

#handles the client side of the program such as sending messages to the server, and connections
class Client:

    #this function initializes the client by creating a socket
    def __init__(self, IPandPort):
        client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print('Connecting...')
            #connects to the server and sends ip and port
            client_sock.connect(IPandPort)
        except WindowsError:
            print('Connection failed.')
            return
        print('The connection to peer ', client_sock.getpeername()[0], ' is successfully established ')
        cThread = threading.Thread(target=self.handler2, args=(client_sock,None))
        cThread.daemon = True
        cThread.start()
        connections.append(client_sock)

    #handler used to receive the message from the server and then sends to a specific client almost same as server handler
    def handler2(self, c, a):
        while True:
            try: 
                data = c.recv(1024)
            except socket.error:
                print('Peer ', c.getpeername()[0] ,' terminates the connection')
                if len(connections) > 0 and c in connections:
                    connections.remove(c)
                    c.close()
                return
            if not data:
                print('Peer ', c.getpeername()[0], ' terminate the connection')
                if len(connections) > 0 and c in connections:
                    connections.remove(c)
                    c.close()
                break
            print(data.decode("utf-8"))


#function that sends the message from a specific socket 
def sendMsg(index, message):
    i = index - 1
    connections[i].send(bytes(message, 'utf-8'))
    

#where the program first starts to run
#creates instance of the server and sends the port that was passed in as an argument and
#launches the server with that part, after server is launched, the listener is ran
def main(p):
    myServer = Server(int(p))
    myServer.run()
    listener()

#this function listens for user commands using simple if else statements 
def listener():
    validCommands = ['help', 'myip', 'myport', 'list', 'terminate', 'exit', 'connect', 'send']
    listener = input()
    listener = listener.lower()

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
        elif "terminate" in listener:
            terminate(listener)
            break
        elif listener == 'exit':
            #closes all peer connections when the exit command is given
            for c in connections:
                #shuts down the reading and writing side of the socket, shutdown is basically advisory to the socket at the other end that it is closing
                c.shutdown(socket.SHUT_RDWR)
                #finalizes the closing of the socket 
                c.close
            exit()
        elif listener not in validCommands:
            invalid()
            break

#lists the type of commands available 
def help():
    print("myip \n   display IP address")
    print("myport \n   display Port")
    print("connect \n   connects to a specific IP and Port \n   example format - 'connect 127.0.0.0.1 4545'")
    print("list \n   lists all connected peers")
    print("send \n   sends a message to a selected connected peer \n   example format - 'send 2 hello how are you doing'")
    print("terminate \n   terminates a specified connection")
    print("exit \n   exits the program")
    listener()

#grabs the host from the corresponding socket 
def myip():
    print("The IP address is: ", sock.getsockname()[0], "\n")
    listener()

#grabs the port from the corresponging port
def myport():
    print("The program runs on port ", sock.getsockname()[1])
    listener()

#first parses the string received then uses it with the class client to connect 
def connect(conString):
    socketInfo = conString.split(" ")
    client = Client((socketInfo[1], int(socketInfo[-1])))
    listener()

#lists all connections to and from the server using the list of sockets and a for loop
def cList():
    print('id: \t IP address \t Port No.')
    for x in range(len(connections)):
        print(x+1, '\t', connections[x].getpeername()[0], '\t',  connections[x].getpeername()[1])
    listener()

#grabs the string from the listener then parses it in to usable variables 
#then sends it to the function that sends the message to specified client
def send(senString):
    sendInfo = senString.split(" ", 2)
    index = int(sendInfo[1])
    msg = ''.join(sendInfo[2:])
    sendMsg(index, msg)
    listener()

#terminates specific peer connection by first splitting the string received into needed values
# it then shuts down both the reading and writing end of the specific socket, and then closes the 
#connection, finally removing the connection from the list of sockets.
def terminate(termString):
    termInfo = termString.split(" ")
    c = int(termInfo[1]) - 1
    connections[c].shutdown(socket.SHUT_RDWR)
    connections[c].close
    del connections[c]
    listener()

#just says invalid command when an invalid command was input in the program
def invalid():
    print("Error Invalid command")
    listener()

#this function allows the program to start with the port initialization
#the port is passed in when the program is first ran as an argument 
#and is then later used to initialize the server
if __name__ == "__main__":
    main(sys.argv[1])