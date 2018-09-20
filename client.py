
import socket

s = socket.socket()
host = socket.gethostname()
port = 4747

s.connect((host, port))
print ('Connected to', host)

while True:
    z = input("Enter something for the server: ")
    s.sendall(z.encode('utf-8'))
    # Halts
    print ('[Waiting for response...]')
    print (s.recv(1024))