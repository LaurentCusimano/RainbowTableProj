import random
import hashlib 
from multiprocessing import Pool
from hashlib import md5
import concurrent.futures
from datetime import datetime
import sys

NB_NOMBRE = 4
NB_LETTRE = 6
NB_WORD_GENERATED_PER_WORD_IN_DIC = 200
NB_REDUCE_FUNCTION_APPLIED = 4000
WORDLIST_FILE_NAME = "words_ccm.txt"
lines = []

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
        if(int(position) > (6 +j)):
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

def create_dictionary():
    f = open("dictionary_"+str(NB_REDUCE_FUNCTION_APPLIED)+ "_iter_"+str(NB_WORD_GENERATED_PER_WORD_IN_DIC)+"_nbwords"+".txt", "w")
    for line in words:
        for i in range(0,NB_WORD_GENERATED_PER_WORD_IN_DIC):
            f.write(put_numbers_in_word(gen_x_random_number(NB_NOMBRE),line.strip("\n")) + "\n")
    f.close()   
        
def create_rainbow_table():
    f = open("rainbow_table_"+str(NB_REDUCE_FUNCTION_APPLIED)+ "_iter_"+str(NB_WORD_GENERATED_PER_WORD_IN_DIC)+"_nbwords"+".txt", "w")
    lines = open("dictionary_"+str(NB_REDUCE_FUNCTION_APPLIED)+ "_iter_"+str(NB_WORD_GENERATED_PER_WORD_IN_DIC)+"_nbwords"+".txt", "w").readlines()
    hashed = ""
    i=0
    pourcentage=0
    for line in lines:
        line = line.strip("\n")
        hashed = str(md5(line.encode()).hexdigest())
        hashed = reduceV2(hashed,words)

        for i in range(0, NB_REDUCE_FUNCTION_APPLIED):
            hashed = str(md5(hashed.encode()).hexdigest())
            hashed = reduceV2(hashed,words)

        hashed = str(md5(hashed.encode()).hexdigest())
        f.write(line + ":" + hashed + "\n")
        hashed = ""

    f.close()


create_dictionary()
print("Dictionary created !")
print("nb_lines:",str(len(lines)))
print("should be :",str(NB_WORD_GENERATED_PER_WORD_IN_DIC * 30000))

create_rainbow_table()
print("rainbow table created !")
