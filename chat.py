import socket
import threading
import sys

def main(p):
    listener()

# Method that Listens for commands and calls the command that has been entered
def listener():
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
        elif("connect" in listener):
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
            print("unrecognized command")
            listener()

def serverinit():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    connections = []

    while True:
        c, a = sock.accept()
        # creates a new thread and passes the function that runs the thread
        cThread = threading.Thread(target = handler)
        # allows to close the program regardless if there are threads running
        cThread.daemon = True
        cThread.start()
        connections.append(c)

def handler(c, a):
    global connections
    while True:
        data = c.recv(1024)
        # this is when the message is sent 
        for connection in connections:
            connection.send(bytes(data))

        if not data:
            connetions.remove(c)
            c.close()
            break

# Method that lists all the commands available
def help():
    print("myip display IP address")
    print("myport display Port")
    print("connect connects to a specific IP and Port")
    print("list lists all connected peers")
    print("send sends a message to a selected connected peer")
    print("terminate terminates a specified connection")
    print("exit exits program")
    listener()

# Method that lists your IP address
def myip():
    hostname = socket.gethostname()
    global host
    host = socket.gethostbyname(hostname)
    print("The IP address is: ", host, "\n")
    listener()

# Method that lists your port
def myport():
    print("The program runs on port ", port)
    listener()

# Method that connects you to another user by sending an IP and Port
def connect(conString):
    # parse 
    print(conString)
    print("not yet implemented")
    listener()

# Method that Lists all peer connections
def cList():
    print("not yet implemented")
    listener()

# Method that sends a message to a specific peer
def send():
    print("not yet implemented")
    listener()

# Method that ends a connection to a peer
def terminate():
    print("not yet implemented")
    listener()

# This allows the program to start with an argument 
if __name__== "__main__":
    main(sys.argv[1])