#TODO: Make a way to manually insert data (with only check if it makes sense (is efficient and will work))
#TODO: Rename number_of_words to number_of_blocks
from math import floor

import os

os.system("")

# if os.name != 'nt':
cyan = '\033[36m'
green = '\033[32m'
grey = '\033[37m'
# else:
#     cyan = ''
#     green = ''
#     grey = ''

def print_disk(number_of_words, word_length, disk_space, address_length, prefix=""):
    disk_img = "" + prefix
    blanks = disk_space-((word_length*number_of_words)+(address_length*number_of_words))
    for p in range(0, len(prefix)):
        blanks-=1
    for b in range(0,number_of_words):
        for a in range(0,address_length):
            disk_img+= cyan
            disk_img+="a"
        for w in range(0,word_length):
            disk_img+= green
            disk_img+="w"
    for blank in range(0,blanks):
        disk_img+=grey
        disk_img+="b"
    print("\n"+disk_img)

    print("\n\n[1] Generate new drive")
    print("[2] Exit")
    answer = input("> ")
    if answer == "1":
        run()
    elif answer == "2":
        quit(0)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    print("Simple HDD calculator")
    print("By: Wiktor Górecki (https://github.com/WiktorGorecki)")

def menu(error_message=""):
    if error_message:
        print(error_message)
    else:
        print()
    print()
    disk_space = int(input("Diskspace:     "))
    word_length = int(input("Size of word:  "))
    return disk_space, word_length

def run(error_message=""):
    disk_space, word_length = menu(error_message)
    number_of_words = floor(disk_space / word_length)

    calculated_number_of_words, calculated_address_length = calculateNoOfWordsThatFit(number_of_words, disk_space, word_length)
    print("\nCalculated parameters:")
    print("    Number of words: "+str(calculated_number_of_words))
    print("    Address length:  "+str(calculated_address_length))

    print("\n\n[1] Generate new drive")
    print("[2] Print the drive")
    print("[3] Exit")
    answer = input("> ")
    if answer=="1":
        run()
    elif answer=="2":
        print_disk(calculated_number_of_words, word_length, disk_space, calculated_address_length)
    elif answer=="3":
        quit(0)

def calculateNoOfWordsThatFit(number_of_words, disk_space, word_length):
    address_lenth=1
    while 1:
        max_address = address_lenth**2
        if max_address < number_of_words:
            address_lenth+=1

        # Check if disk will fit all the data
        used_bits = (address_lenth*number_of_words) + (word_length*number_of_words)
        while used_bits>disk_space:
            number_of_words-=1
            used_bits = (address_lenth * number_of_words) + (word_length * number_of_words)


        if max_address >= number_of_words:
            return number_of_words, address_lenth

    # rekurencyjnie!!!! bo inaczej nie dasz rady
    # jak się da zaadresować to sprawdź, czy jak się odejmie 1bit od adresu i doda 1 do pustego miejsca i zaadresuje puste miejsce, to czy sie bedzie dało zaadresowac na tylu adresach
    # adres adresowi adresem adresuje adres skurwysynu
    # kurwa mać masło maślane


logo()
run()