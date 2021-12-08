import random
import hashlib
NB_NOMBRE = 4
NB_LETTRE = 6
NB_WORD_GENERATED_PER_WORD_IN_DIC = 3000
NB_REDUCE_FUNCTION_APPLIED = 1000
WORDLIST_FILE_NAME = "words_ccm.txt"

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

def create_dictionary():
    f = open("wordlist_generatedv2.txt", "w")
    dic = open(WORDLIST_FILE_NAME, 'r')
    lines = dic.readlines()
    for line in lines:
        for i in range(0,NB_WORD_GENERATED_PER_WORD_IN_DIC):
            f.write(put_numbers_in_word(gen_x_random_number(NB_NOMBRE),line.strip("\n")) + "\n")
    f.close()

create_dictionary()