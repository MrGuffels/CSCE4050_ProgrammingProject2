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
                        help='Length of hash input/output list', default=100000)

    args = parser.parse_args()

    #Start while Loop
    runs = 0
    while True:
        #File management for storing messages for use while testing. Resets each run.
        if os.path.exists("hash.data"):
            os.remove("hash.data")
        else : print ("The file doesn't exist")
        message_file = open("hash.data","w")   
        runs += 1
        value_pairs = {}
        counter = 0
        print ("Starting run: "+str(runs))
        while counter < args.lhash:
            counter += 1

            #Call Message Generation
            message = genMessage()
            message_file.write(str(message))

            #Call BadHash40
            badHash = BadHash40(message)
            message_file.write(' | '+str(badHash)+'\n')

            #Check for duplicate
            collision = collisionCheck(value_pairs,badHash)
            if collision == True:
                break
            else:
                value_pairs[badHash] = message
        message_file.close()
        if collision == True:
            break

    #Output 2 original messages and collision on hash
    print ("It took "+str(runs)+" runs of "+str(args.lhash)+" messages to find a collision.")
    print ("First  message: "+str(value_pairs[badHash]))
    print ("Second message: "+str(message))
    print ("Duplicate Hash: 0x"+str(badHash))