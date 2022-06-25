import socket
import threading
import pickle

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 3333))

canSend=True 

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
        if (canSend):
            message = '{}'.format(input(''))
            toSend = encode(message)
            print("Your message as been encoded as " + toSend + " and sent")
            client.send(toSend.encode('ascii'))
        else : 
            print("The server cannot decode your message. but feel free to type :)")
            message = '{}'.format(input(''))
            toSend = encode(message)

def encode(s):
    # find the length of the string 
    size = len(s)
    # flags 
    wasLow = True
    inASequence=False
    toIgnore=0
    # return value 
    result =""
    for i in range(size) : 
        if (int(s[i]) == 1): 
            if (wasLow):
                #this time should be high 
                result+="+"
                wasLow=False
            else: 
                #It was not low, so this time it should be low
                result+="-"
                wasLow=True 
        elif(int(s[i]) == 0 ): 
            # check if there are enough numbers in a range of 8
            # if we are in a sequence, then 8 rounds have been applied, continue
            if (inASequence and toIgnore>0): 
                toIgnore-=1
                continue 
            else : 
                # check the length
                # print(i)
                if (  (i+7) > size  ): 
                    result+="0"
                else : 
                    # check how many of them are zero 
                    next8 = s[i:(i+8)]
                    # if the eight of them are 0
                    if (next8.count('0') == 8): 
                        # Apply the corresponding sequence
                        inASequence=True
                        toIgnore=7
                        # if the previous was low 
                        if (wasLow): 
                            # apply the sequence for negative
                            result+="000-+0+-"
                            wasLow=True
                        else : 
                            # apply the sequence for positive 
                            result+="000+-0-+"
                            wasLow=False
                    else : 
                        # simply add 0
                        result+="0"  
        else: 
            # invalid value 
            print("Invalid value detected")
    # print(result)
    return result


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()