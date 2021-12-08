NB_NOMBRE = 4
from hashlib import md5

def get_number_of_a_string(string):
    number = ""
    for element in range(0, len(string)):
            elem = string[element]
            if(elem.isdigit() ):
                number += elem

    return number


def reduction(hashed, Lines):
    number = get_number_of_a_string(hashed)
    if (len(str(number)) < 4):
        number += "0000"
    wordLine = int(number) % len(Lines)
    word = Lines[wordLine].strip('\n')
    j = 0
    for i in range(0, NB_NOMBRE):
        tempNumber = int(number[i])
        position = int(str(number)[len(str(number)) - i - 1])
        if (int(position) > (6 + j)):
            position = int(position / 2)
        word = word[:position] + str(tempNumber) + word[position:]
        j += 1
    return word


with open('words_ccm.txt', 'r') as f:
    words = f.readlines()

n = 10
text = ""
password = ""
rainbowTable = {}

with open('rainbow_table_esteban_laurent.txt', 'r') as f:
    for line in f:
        (key, val) = line.strip("\n").split(":")
        rainbowTable[key] = val

keys_list = list(rainbowTable.keys())
values_list = list(rainbowTable.values())

inputHash = "e9bba27dc9a6c843c6ab6a12fc8108e7"
initialhash = inputHash

for i in range(n+1):
    if inputHash not in values_list:
        print("input hash is not in known values")
        key = reduction(inputHash, words)
        inputHash = str(md5(key.encode()).hexdigest())
    else:
        break


if inputHash in values_list:
    position = values_list.index(inputHash)
    key = keys_list[position]

    hashedkey = str(md5(key.encode()).hexdigest())
    password = hashedkey
    print(password, initialhash)
    i=0
    while(hashedkey != initialhash and i<= n):
        i+=1
        password = reduction(hashedkey, words)
        hashedkey = str(md5(password.encode()).hexdigest())
        print(hashedkey, password, initialhash)

    if i==0:
        password = key
    print("password found!", password)

else:
    print("hash is not in list")

