import argparse
import hashlib
import os
import random

#Message Generation Length passed as a number. Returns a hex string
def genMessage(length):
    message = hex(random.getrandbits(length))[2:]
    while (len(message) != 64):
        message = '0'+message
    return '0x'+message

#BadHash40(x) Message passed in as a hex string. Returns a hex string
def BadHash40(message):
    hexString = hashlib.sha256(bytes.fromhex(message[2:])).hexdigest()
    return hexString[0:9]

def collisionCheck(value_pairs,badHash):
    if not value_pairs:
        return False, (None,None)
    for pair in value_pairs:
        old_message, old_badHash = pair
        if badHash == old_badHash:
            return True, pair
    return False, (None,None)

#Runtime
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Executes the birthday attack against the BadHash40 hash function')
    parser.add_argument('-lhash', type=int,
                        help='Length of hash input and output in bits', default=256)

    args = parser.parse_args()

    #File management for storing messages for use while testing
    if os.path.exists("message_file.txt"):
        os.remove("message_file.txt")
    else : print ("The file doesn't exist")
    message_file = open("message_file.txt","w")
    value_pairs = []
    counter = 0

    #Start while Loop

    while True:
        #Progress Check
        counter += 1
        if counter % 10000 == 0:
            print ("Tests Done: "+str(counter))

        #Call Message Generation
        message,rand_bit = genMessage(args.lhash)
        message_file.write(str(message)+'\n')

        #Call BadHash40
        badHash = BadHash40(message)

        #Check for duplicate
        collision, member = collisionCheck(value_pairs,badHash)
        value_pairs.append((message,badHash))
        if collision == True:
            break

    #Output 2 original messages and collision on hash
    print ("First  message: "+str(member[0]))
    print ("Second message: "+str(message))
    print ("Duplicate Hash: 0x"+str(badHash))