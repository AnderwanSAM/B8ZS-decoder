import socket
import threading
import pickle 

host = '127.0.0.1'
port = 3333

# Setting up and Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # make sur we can reuse the port later 
server.bind((host, port))

server.listen()

# Lists For Clients 
clients = []

# flag 
waiting=False

# default - to send messages to all clients 
def broadcast(message):
    for client in clients:
        client.send(message)


# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Receive  Message from a client 
            message = client.recv(1024).decode('ascii')
            if (message=='demande a envoyer'):
                waiting=True
                client.send('pret a recevoir'.encode('ascii'))
            elif (waiting): 
                #decode stuff 
                print("Decoding.....")
                print("Server side : Received " + message)
                decoded = decode(message)
                print("Decoded to :  " + decoded)
                print("Fin du decodage")
            else:
                print("Not ready to decode")

        except:
            # Removing And Closing Clients when something goes wrong  - the client left 
            index = clients.index(client)
            clients.remove(client)
            client.close()
            break


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        clients.append(client)
        client.send('Connected to server!'.encode('ascii'))
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def decode(s): 
    # find the length of the string 
    size=len(s)
    # flags
    inASequence=False 
    toIgnore=0
    # return value 
    result=""
    # decode 
    for i in range (size): 
        if (inASequence and toIgnore > 0): 
            # if we are in a sequence 
            # ignore this round
            toIgnore-=1
            continue 
        else : 
            if (s[i] =='0'):
                # check if we are preceding a sequence 
                # check if there are at least 8 numbers 
                if (  (i+7) > size ): 
                    result+="0"
                else : 
                    # check if the next 8 are a known sequence
                    next8 = s[i:(i+8)]
                    if (next8 == "000-+0+-"): 
                        result+="00000000"
                        toIgnore=7
                        inASequence=True
                    elif (next8 == "000+-0-+"): 
                        result+="00000000"
                        toIgnore=7
                        inASequence=True 
                    else :
                        # just a regular bit
                        result+="0"
            elif (s[i] == '+'): 
                # check if we are preceding a sequence 
                # check if there are at least 8 numbers 
                if (  (i+7) > size ): 
                    result+="1"
                else : 
                    # check if the next 8 are a known sequence
                    next8 = s[i:(i+8)]
                    if (next8 == "000-+0+-"): 
                        result+="00000000"
                        toIgnore=7
                        inASequence=True
                    elif (next8 == "000+-0-+"): 
                        result+="00000000"
                        toIgnore=7
                        inASequence=True 
                    else :
                        # just a regular bit
                        result+="1"
            elif (s[i] == '-'):
                # check if we are preceding a sequence 
                # check if there are at least 8 numbers 
                if (  (i+7) > size ): 
                    result+="1"
                else : 
                    # check if the next 8 are a known sequence
                    next8 = s[i:(i+8)]
                    if (next8 == "000-+0+-"): 
                        result+="00000000"
                        toIgnore=7
                        inASequence=True
                    elif (next8 == "000+-0-+"): 
                        result+="00000000"
                        toIgnore=7
                        inASequence=True 
                    else :
                        # just a regular bit
                        result+="1"
            else : 
                print("Invalid value detected")
    return result

receive()