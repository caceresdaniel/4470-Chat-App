import select, socket, sys
import threading

listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peers = []

# server class that creates a server for each client that is launched
# that way each client is a user
class Server:
    # init method that starts off the server
    def __init__(self, port):
        # getting the host name (IP) using sockets
        host = socket.gethostname()
        try:
            # setting the ip and port to a socket
            listening_socket.bind((host, port))
        except WindowsError:
            print('Failed to create socket')
            exit()
        # enable the server to accept connections by using sock.listen
        listening_socket.listen(1)
        # creating a thread for the run function
        listening_thread = threading.Thread(target=self.run)
        # setting a thread to a daemon allows it to shut down while there are still threads running
        listening_thread.daemon = True
        listening_thread.start()
        menu()

    # function that accepts the connection from the client and adds the connection to the list of sockets
    def run(self):
        while True:
            connection, address = listening_socket.accept()
            connection_thread = threading.Thread(target=self.connection_handler, args=(connection,))
            connection_thread.daemon = True
            connection_thread.start()
            peers.append(connection)
            print('The connection to peer ', connection.getpeername()[0], ' is successfully established ')

    # this is the part of code where the server receives the message from the client
    def connection_handler(self, connection):
        while True:
            # added try/except for when a client disconnects in a weird way
            try:
                data = connection.recv(1024)
                print('Message received from ', connection.getpeername()[0])
                print('Sender’s Port: <', connection.getpeername()[1], '>')
                print('Message: ', data.decode("utf-8"))
            except socket.error:
                print('Peer ', connection.getpeername()[0], ' terminates the connection')
                if len(peers) > 0 and connection in peers:
                    peers.remove(connection)
                    connection.close()
                return
            # checks to see if it receiving data from a socket if is not receiving data the socket is then removed and closed
            if not data:
                print('Peer ', connection.getpeername()[0], ' terminates the connection')
                if len(peers) > 0 and connection in peers:
                    peers.remove(connection)
                    connection.close()
                break


# handles the client side of the program such as sending messages to the server, and connections
class Client:

    # this function initializes the client by creating a socket
    def __init__(self, ip_port):
        connecting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print('Connecting...')
            # connects to the server and sends ip and port
            connecting_socket.connect(ip_port)
        except WindowsError:
            print('Connection failed.')
            return
        print('The connection to peer ', connecting_socket.getpeername()[0], ' is successfully established ')
        client_thread = threading.Thread(target=self.connection_handler, args=(connecting_socket,))
        client_thread.daemon = True
        client_thread.start()
        peers.append(connecting_socket)

    # handler used to receive the message from the server and then sends to a specific client
    # almost same as server handler
    def connection_handler(self, connection):
        while True:
            try: 
                data = connection.recv(1024)
            except socket.error:
                print('Peer ', connection.getpeername()[0], ' terminates the connection')
                if len(peers) > 0 and connection in peers:
                    peers.remove(connection)
                    connection.close()
                return
            if not data:
                print('Peer ', connection.getpeername()[0], ' terminate the connection')
                if len(peers) > 0 and connection in peers:
                    peers.remove(connection)
                    connection.close()
                break
            print('Message received from ', connection.getpeername()[0])
            print('Sender’s Port: <', connection.getpeername()[1], '>')
            print('Message: ', data.decode("utf-8"))


# function that sends the message from a specific socket
def sendMsg(index, message):
    i = index - 1
    print("Message sent to ", peers[i].getpeername()[0])
    peers[i].send(bytes(message, 'utf-8'))
    

# where the program first starts to run
# creates instance of the server and sends the port that was passed in as an argument and
# launches the server with that part, after server is launched, the listener is ran
def main(p):
    myServer = Server(int(p))
    myServer.run()
    menu()

# this function listens for user commands using simple if else statements
def menu():
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
            connection_list()
            break
        elif "send" in listener:
            send(listener)
            break
        elif "terminate" in listener:
            terminate(listener)
            break
        elif listener == 'exit':
            # closes all peer connections when the exit command is given
            for c in peers:
                # shuts down the reading and writing side of the socket, shutdown is basically advisory to the socket at the other end that it is closing
                c.shutdown(socket.SHUT_RDWR)
                # finalizes the closing of the socket
                c.close
            exit()
        elif listener not in validCommands:
            invalid()
            break

# lists the type of commands available
def help():
    print("myip... \n   display IP address")
    print("myport... \n   display Port")
    print("connect... \n   connects to a specific IP and Port \n   example format - 'connect 127.0.0.0.1 4545'")
    print("list... \n   lists all connected peers")
    print("send... \n   sends a message to a selected connected peer \n   example format - 'send 2 hello how are you doing'")
    print("terminate... \n   terminates a specified connection")
    print("exit... \n   exits the program")
    menu()

# grabs the host from the corresponding socket
def myip():
    print("The IP address is: ", listening_socket.getsockname()[0])
    menu()

# grabs the port from the corresponding port
def myport():
    print("The program runs on port ", listening_socket.getsockname()[1])
    menu()

# first parses the string received then uses it with the class client to connect
def connect(conString):
    myip = listening_socket.getsockname()[0]
    socketInfo = conString.split(" ")
    ip = socketInfo[1]
    ipexists = False
    for p in peers:
        if ip == p.getpeername()[0]:
            ipexists = True
    if len(peers) > 2:
        print("Peer limit reached")
    elif myip == ip:
        print("Can not connect to your self please check the IP you wish to connect to")
    elif ipexists == True:
        print('Connection already exists can not reconnect to same connection')
    else:
        Client((socketInfo[1], int(socketInfo[-1])))
    menu()

# lists all connections to and from the server using the list of sockets and a for loop
def connection_list():
    print('id: \t IP address \t Port No.')
    for x in range(len(peers)):
        print(x + 1, '\t', peers[x].getpeername()[0], '\t', peers[x].getpeername()[1])
    menu()

# grabs the string from the listener then parses it in to usable variables
# then sends it to the function that sends the message to specified client
def send(senString):
    sendInfo = senString.split(" ", 2)
    index = int(sendInfo[1])
    if (int(sendInfo[1]) <= len(peers)) and index != 0:
        msg = ''.join(sendInfo[2:])
        sendMsg(index, msg)
        menu()
    else:
        print("This peer does not exist please use the list function to properly find a peer to send a message too")
        menu()

# terminates specific peer connection by first splitting the string received into needed values
# it then shuts down both the reading and writing end of the specific socket, and then closes the 
# connection, finally removing the connection from the list of sockets.
def terminate(termString):
    termInfo = termString.split(" ")
    c = int(termInfo[1]) - 1
    if (int(termInfo[1]) <= len(peers)) and termInfo[1] != 0:
        peers[c].shutdown(socket.SHUT_RDWR)
        peers[c].close
        del peers[c]
        menu()
    else:
        print("This peer does not exist please use the list function to properly find a peer to terminate")
        menu()

# just says invalid command when an invalid command was input in the program
def invalid():
    print("Error Invalid command")
    menu()

# this function allows the program to start with the port initialization
# the port is passed in when the program is first ran as an argument
# and is then later used to initialize the server
if __name__ == "__main__":
    main(sys.argv[1])