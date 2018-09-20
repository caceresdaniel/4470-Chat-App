import socket
import sys

port = 0
host = ''

def listen(port):
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    c = None

    while True:
        if c is None:
            # Halts
            print('[Waiting for connection...]')
            c, addr = s.accept()
            print('Got connection from', addr)
        else:
            # Halts

            print('[Waiting for response...]')
            print(c.recv(1024))
            q = input("Enter something to this client: ")
            c.sendall(q.encode('utf-8'))
    menu()

def myip():
    hostname = socket.gethostname()
    global host
    host = socket.gethostbyname(hostname)
    print("The IP address is: ", host, "\n")
    menu()


def myport():
    #test = socket.getaddrinfo()
    global port
    print(port)
    #print("getaddr: ", test)
    menu()


def menu():

    if userinput == "help":
        print("help UNAVAILABLE\n")
        menu()

    elif userinput == "myip":
        myip()

    elif userinput == "myport":
        myport()

    elif userinput == "connect":
        print("connect UNAVAILABLE\n")
        menu()
    elif userinput == "list":
        print("list UNAVAILABLE\n")
        menu()
    elif userinput == "send":
        print("send UNAVAILABLE\n")
        menu()
    elif userinput == "terminate":
        print("terminate UNAVAILABLE\n")
        menu()
    elif userinput == "exit":
        sys.exit
    else:
        print("INVALID INPUT\nPlease Enter a Valid Input")
        menu()

def main():
    print("Welcome to Project #1")
    global port
    port = input("Please Enter A Port Number: ")
    port = int(port)
    listen(port)
    menu()

if __name__ == "__main__":
    main()