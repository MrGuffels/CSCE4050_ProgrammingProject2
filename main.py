import argparse
import hashlib
import os
import random

#Message Generation Length passed as a number. Returns a hex string
def genMessage(length):
    return hex(random.getrandbits(length))

#BadHash40(x) Message passed in as a hex string. Returns a hex string
def BadHash40(message):
    hexString = hashlib.sha256(bytes.fromhex(message)).hexdigest()
    return hexString[0:9]

def collisionCheck(value_pairs,badHash):
    for pair in value_pairs:
        old_message, old_badHash = pair
        if badHash == old_badHash:
            return True, pair
        else: return False


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

    #Start while Loop
    while True:

        #Call Message Generation
        message = genMessage(args.lhash)
        message_file.write(message)

        #Call BadHash40
        badHash = BadHash40(message)

        #Check for duplicate
        collision, member = collisionCheck(value_pairs,badHash)
        value_pairs.append((message,badHash))
        if collision == False:
            break

    #Output 2 original messages and collision on hash
    print ("First  message: "+member[0])
    print ("Second message: "+message)
    print ("Duplicate Hash: "+badHash)