import socket
import threading
import pickle

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 3333))

canSend=False 

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            print(message)
            if message == 'Connected to server!':
                client.send('demande a envoyer'.encode('ascii'))
            elif (message == 'pret a recevoir'): 
                canSend=True
                print("The server is ready to decode your message")
            else:
                print(message)
            print(message)
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        message = '{}'.format(input(''))
        client.send(message.encode('ascii'))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()