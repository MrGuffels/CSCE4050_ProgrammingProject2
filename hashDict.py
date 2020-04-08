import argparse
import hashlib
import os
import random

#Message Generation Returns a hex string
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
                        help='Length of hash input/output list', default=10000)

    args = parser.parse_args()

    #File management for storing messages for use while testing
    if os.path.exists("message_file.txt"):
        os.remove("message_file.txt")
    else : print ("The file doesn't exist")
    message_file = open("message_file.txt","w")
    message_file.write('                              Message                              | Hash Values\n')
    value_pairs = {}
    counter = 0

    #Start while Loop

    while True:
        #Progress Check
        counter += 1
        if counter % 10000 == 0:
            print ("Tests Done: "+str(counter))

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

    #Output 2 original messages and collision on hash
    print ("First  message: "+str(value_pairs[badHash]))
    print ("Second message: "+str(message))
    print ("Duplicate Hash: 0x"+str(badHash))