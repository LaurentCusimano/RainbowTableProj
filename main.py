import random
import hashlib 
from multiprocessing import Pool
from hashlib import md5
import concurrent.futures
from datetime import datetime

NB_NOMBRE = 4
NB_LETTRE = 6
NB_WORD_GENERATED_PER_WORD_IN_DIC = 200
NB_REDUCE_FUNCTION_APPLIED = 4000
WORDLIST_FILE_NAME = "words_ccm.txt"

words = open(WORDLIST_FILE_NAME, "r").readlines()

def gen_x_random_number(x):
    numbers = []
    for i in range(x):
        numbers.append(random.randint(0, 9))
    return numbers

def put_numbers_in_word(numbers,word):
    i = 0
    for number in numbers:
        place = random.randint(0,len(word) + i) 
        word = word[:place] + str(number) + word[place:]
        i += 1
    return word


def process(line):
    hashed = str(md5(line.encode()).hexdigest())
    i = NB_REDUCE_FUNCTION_APPLIED

    while i > 0:
        hashed = reduceV2(hashed,lines)
        hashed = str(md5(hashed.encode()).hexdigest())
        i-=1

    return [line,hashed]        
    
    
def reduceV2(hashed, Lines):
    number = get_number_of_a_string(hashed)
    if(len(str(number)) < 4 ):
        number += "0000"
    wordLine = int(number) % len(Lines)
    word = Lines[wordLine].strip('\n')
    j = 0
    for i in range(0, NB_NOMBRE):
        tempNumber = int(number[i])
        position = int(str(number)[len(str(number)) - i -1])
        if(int(position) > (6 + j )):
            position = int(position / 2)
        word = word[:position] + str(tempNumber) + word[position:]
        j += 1
    return word


def get_number_of_a_string(string):
    number = ""
    for element in range(0, len(string)):
            elem = string[element]
            if(elem.isdigit() ):
                number += elem

    return number


text = ""
password = ""
rainbowTable = {}

def findPassword(hashed):
    with open('words_ccm.txt', 'r') as f:
        words = f.readlines()

    f.close()

    with open('rainbow_table_4000_iterations_200_nbwords.txt', 'r') as f:
        for line in f:
            (key, val) = line.strip("\n").split(":")
            rainbowTable[key] = val

    f.close()

    keys_list = list(rainbowTable.keys())
    values_list = list(rainbowTable.values())

    inputHash = hashed.strip("\n")
    initialhash = inputHash

    for i in range(NB_REDUCE_FUNCTION_APPLIED+1):
        if inputHash not in values_list:
            key = reduceV2(inputHash, words)
            inputHash = str(md5(key.encode()).hexdigest())
        else:
            position = values_list.index(inputHash)
            key = keys_list[position]
            hashedkey = str(md5(key.encode()).hexdigest())
            password = key
            i=0

            while(hashedkey != initialhash and i <= NB_REDUCE_FUNCTION_APPLIED +1):
                i+=1
                password = reduceV2(hashedkey, words)
                hashedkey = str(md5(password.encode()).hexdigest())

            if(initialhash == hashedkey):
                print("password found!", initialhash,hashedkey, ":", password)
                return password
            else:
                key = reduceV2(inputHash, words)
                inputHash = str(md5(key.encode()).hexdigest())

    print("password not found !")



lines = open(WORDLIST_FILE_NAME, "r").readlines()

#create_dictionary()
#create_rainbow_table()

hashs_to_crack = open("test.txt", 'r')
hashs_to_crack = hashs_to_crack.readlines()

datas = []

#NB_REDUCE_FUNCTION_APPLIED += 1
#print(process("84721db2f2ad1c80d79baeabc5a039a7 "))
print(reduceV2("84721db2f2ad1c80d79baeabc5a309a6", lines))
#print(str(md5("a1b4a5n8ic".encode()).hexdigest()))

for htc in hashs_to_crack:
    passw = findPassword(htc)
    print(str(hashs_to_crack.index(htc) + 1)+ "/" + str(len(hashs_to_crack)))
    if(passw != None):
        datas.append([htc.strip("\n"),passw])

print(datas)



#if(passw != None):
#    print(passw)
#    print("hash of",passw, ":",str(md5(passw.encode()).hexdigest()))

