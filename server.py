import socket, threading                                                
host = '192.168.152.199'                                                      
port = 7476                                                

#socket initialization
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#binding host and port to socket        
server.bind((host, port))                                              
server.listen()

clients = []
nicknames = []

def broadcast(message,connection):
    for client in clients:
        print(f"{client} == {connection}")
        if client!=connection:
            try:
                client.send(message)
            except:
                client.close()
 
                # if the link is broken, we remove the client
                client.remove(clients)
 

def handle(client):                                         
    while True:
        #recieving valid messages from client
        try: 
            message = client.recv(1024)
            broadcast(message,client)
        #removing clients
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'),0)
            nicknames.remove(nickname)
            break

def receive():
    print(f"Running on {host}:{port}")
    #accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))        
        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'),0)
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()