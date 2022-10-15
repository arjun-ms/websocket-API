import socket, threading
nickname = input("Enter your nickname: ")
host = '10.0.0.72'                                                      
port = 6677 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#connecting client to server
client.connect((host, port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break
        
def write():
    while True:
        message = '=> {}: {}'.format(nickname, input('')) 
        client.send(message.encode('ascii'))

#receiving multiple messages
receive_thread = threading.Thread(target=receive)               
receive_thread.start()
#sending messages
write_thread = threading.Thread(target=write)                   
write_thread.start()