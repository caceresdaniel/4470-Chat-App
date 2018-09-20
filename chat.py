import socket
import sys

def main(p):

    sock = socket.socket() 
    host = socket.gethostname() 
    global port
    port = int(p)
    sock.bind((host,port))
    sock.listen(5)
    connection = None

    listener()

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
        elif(listener == 'connect'):
            connect()
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
    print("The program runs on port ", port)
    listener()

def connect():
    print("not yet implemented")
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