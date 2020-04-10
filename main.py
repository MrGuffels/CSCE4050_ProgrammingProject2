import argparse
import hashlib
import os
import random

#Message Generation Length passed as a number. Returns a hex string
def genMessage():
    message = hex(random.getrandbits(256))[2:]
    while (len(message) != 64):
        message = '0'+message
    return '0x'+message

#BadHash40(x) Message passed in as a hex string. Returns a hex string
def BadHash40(message):
    hexString = hashlib.sha256(bytes.fromhex(message[2:])).hexdigest()
    return hexString[:10]

def collisionCheck(value_pairs,badHash):
    if not value_pairs:
        return False
    if badHash in value_pairs:
        return True


#Runtime
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Executes the birthday attack against the BadHash40 hash function')
    parser.add_argument('-lhash', type=int,
                        help='Length of hash input/output list', default=1000000)

    args = parser.parse_args()

    #Start while True Loop
    runs = 0
    while True:
        #File management for storing messages for use while testing. Resets each run.
        if os.path.exists("hash.data"):
            os.remove("hash.data")
        else : print ("The file doesn't exist")
        message_file = open("hash.data","w")

        message_list=[] #Create empty lists for storing the message and hashes
        badHash_list=[]

        runs += 1   #run counter for visual clarity
        print ("Starting run: "+str(runs))

        counter = 0 #message counter for list size

        while counter < args.lhash: #Compile list of key and message pairs
            counter += 1
            message = genMessage()
            message_file.write(str(message))    #Write message to file
            message_list.append(message)        #Add message to list

            badHash = BadHash40(message)
            message_file.write(' | '+str(badHash)+'\n') #Write hash to file
            badHash_list.append(badHash)        #Add hash to list

        message_file.close()        #Close file writing

        seen = set()    #Duplicate testing
        seen2 = []
        for badHash in badHash_list:    #Loop through hashes in list
            if badHash in seen:         #If hash in set already
                seen2.append(badHash)   #Add to duplicate set
            else:  
                seen.add(badHash)       #Add to unique set
        if seen2:       #If duplicate set has elements, break
            break

    #Output 2 original messages and collision on hash
    print ("It took "+str(runs)+" runs of "+str(args.lhash)+" messages to find a collision.")

    message1_idx = badHash_list.index(seen2[0])     #Find index to print message that matches badHash
    message2_idx = badHash_list[(message1_idx+1):].index(seen2[0])+message1_idx+1       #Find second index to print second message that matches badHash

    print ("First  message: "+str(message_list[message1_idx]))  #Print all the values
    print ("Second message: "+str(message_list[message2_idx]))
    print ("Duplicate Hash: 0x"+str(seen2[0]))