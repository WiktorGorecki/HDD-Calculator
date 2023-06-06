# TODO: Make a way to manually insert data (with only check if it makes sense (is efficient and will work))
# TODO: Rename number_of_words to number_of_blocks
# TODO: Move blanks from functions to place before it's call
from math import floor

import os

os.system("")

cyan = '\033[36m'
green = '\033[32m'
grey = '\033[37m'


def stats(number_of_words: int, word_length: int, disk_space: int, address_length: int):
    blanks = disk_space - ((word_length * number_of_words) + (address_length * number_of_words))
    print("Stats of the drive: ")
    print("\n  Effective capacity: "+str(number_of_words*word_length)+"b")
    print("\n  Assigned space: " + str(round(((disk_space - blanks) / disk_space) * 100)) + "%")
    print("    - Addresses: " + str(round(((address_length * number_of_words) / disk_space) * 100)) + "%")
    print("    - Words: " + str(round(((word_length * number_of_words / disk_space) * 100))) + "%")
    print("  Unassigned space: " + str(round((blanks / disk_space) * 100)) + "%")

    print("\n\n[1] Generate new drive")
    print("[2] Visualise the drive")
    print("[3] Exit")
    answer = input("> ")
    if answer == "1":
        clear_screen()
        logo()
        run()
    elif answer == "2":
        print_disk(number_of_words, word_length, disk_space, address_length)
    elif answer == "3":
        quit(0)


def print_disk(number_of_words: int, word_length: int, disk_space: int, address_length: int, prefix=""):
    counter = 0
    disk_img = "" + prefix
    blanks = disk_space - ((word_length * number_of_words) + (address_length * number_of_words))
    print("\n Drive model:\n")
    print(prefix, end="")
    for p in range(0, len(prefix)):
        blanks -= 1
    for b in range(0, number_of_words):
        for a in range(0, address_length):
            # disk_img += cyan
            # disk_img += "a"
            print(cyan+"a", end="")
            counter += 1
        for w in range(0, word_length):
            # disk_img += green
            # disk_img += "w"
            print(green+"w", end="")
            counter += 1
    for blank in range(0, blanks):
        # disk_img += grey
        # disk_img += "u"
        print(grey+"u", end="")
        counter += 1
    if counter != disk_space:
        print("An error occurred!!!")
    #print("\n" + disk_img)
    print(cyan+"\n\naddress")
    print(green+"word")
    print(grey+"unassigned")
    print('\x1b[0m')

    print("\n[1] Generate new drive")
    print("[2] Drive statistics")
    print("[3] Exit")
    answer = input("> ")
    if answer == "1":
        clear_screen()
        logo()
        run()
    elif answer == "2":
        stats(number_of_words, word_length, disk_space, address_length)
    elif answer == "3":
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
    print("Specify drive properties:")
    disk_space = int(input("    Capacity :     "))
    word_length = int(input("    Size of word:  "))
    return disk_space, word_length


def run(error_message=""):
    disk_space, word_length = menu(error_message)
    number_of_words = floor(disk_space / word_length)

    calculated_number_of_words, calculated_address_length = calculateNoOfWordsThatFit(number_of_words, disk_space,
                                                                                      word_length)
    print("\nCalculated parameters:")
    print("    Number of words: " + str(calculated_number_of_words))
    print("    Address length:  " + str(calculated_address_length))

    print("\n\n[1] Generate new drive")
    print("[2] Visualise the drive")
    print("[3] Drive statistics")
    print("[4] Exit")
    answer = input("> ")
    if answer == "1":
        run()
    elif answer == "2":
        print_disk(calculated_number_of_words, word_length, disk_space, calculated_address_length)
    elif answer == "3":
        stats(calculated_number_of_words, word_length, disk_space, calculated_address_length, )
    elif answer == "4":
        quit(0)


def calculateNoOfWordsThatFit(number_of_words, disk_space, word_length):
    address_length = 1
    while 1:
        max_address = address_length ** 2
        if max_address < number_of_words:
            address_length += 1

        # Check if disk will fit all the data
        used_bits = (address_length * number_of_words) + (word_length * number_of_words)
        while used_bits > disk_space:
            number_of_words -= 1
            used_bits = (address_length * number_of_words) + (word_length * number_of_words)

        if max_address >= number_of_words:
            return number_of_words, address_length


logo()
run()
