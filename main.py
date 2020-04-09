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

    #Start while Loop
    runs = 0
    while True:
        #File management for storing messages for use while testing. Resets each run.
        if os.path.exists("hash.data"):
            os.remove("hash.data")
        else : print ("The file doesn't exist")
        message_file = open("hash.data","w")
        runs += 1
        message_list=[]
        badHash_list=[]
        print ("Starting run: "+str(runs))

        counter = 0
        while counter < args.lhash: #Compile list of key and message pairs
            counter += 1
            message = genMessage()
            message_file.write(str(message))
            message_list.append(message)

            badHash = BadHash40(message)
            message_file.write(' | '+str(badHash)+'\n')
            badHash_list.append(badHash)

        message_file.close()

        seen = set()
        seen2 = []
        for badHash in badHash_list:
            if badHash in seen:
                seen2.append(badHash)
            else:
                seen.add(badHash)
        if seen2:
            break

    #Output 2 original messages and collision on hash
    print ("It took "+str(runs)+" runs of "+str(args.lhash)+" messages to find a collision.")

    message1_idx = badHash_list.index(seen2[0])
    message2_idx = badHash_list[(message1_idx+1):].index(seen2[0])+message1_idx+1

    print ("First  message: "+str(message_list[message1_idx]))
    print ("Second message: "+str(message_list[message2_idx]))
    print ("Duplicate Hash: 0x"+str(seen2[0]))