from hashlib import md5

NB_NOMBRE = 4
NB_REDUCE_FUNCTION_APPLIED = 10
WORDLIST_FILE_NAME = "words_ccm.txt"
dic = open(WORDLIST_FILE_NAME, 'r')
lines = dic.readlines()

def get_number_of_a_string(string):
    number = ""
    for element in range(0, len(string)):
            elem = string[element]
            if(elem.isdigit() ):
                number += elem

    return number

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

def create_rainbow_table():
    f = open("rainbow_table_esteban_laurent.txt", "w")
    dic = open("wordlist_generatedv2.txt", 'r')
    words = open("words_ccm.txt", "r").readlines()
    lines = dic.readlines()
    hashed = ""
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

create_rainbow_table()

