# TODO: Make a way to manually insert data (with only check if it makes sense (is efficient and will work))
# TODO: Move blanks from functions to place before it's call
from math import floor

import os

os.system("")

cyan = '\033[36m'
green = '\033[32m'
grey = '\033[37m'


def stats_menu(number_of_blocks, word_width, disk_space, address_width):
    answer = input("> ")
    if answer == "1":
        clear_screen()
        logo()
        run()
    elif answer == "2":
        print_disk(number_of_blocks, word_width, disk_space, address_width)
    elif answer == "3":
        quit(0)
    else:
        stats_menu(number_of_blocks, word_width, disk_space, address_width)


def stats(number_of_blocks: int, word_width: int, disk_space: int, address_width: int):
    blanks = disk_space - ((word_width * number_of_blocks) + (address_width * number_of_blocks))

    # Printing the stats
    print("Stats of the drive: ")
    print("\n  Effective capacity: " + str(number_of_blocks * word_width) + "b")
    print("\n  Assigned space: " + str(round(((disk_space - blanks) / disk_space) * 100)) + "%")
    print("    - Addresses: " + str(round(((address_width * number_of_blocks) / disk_space) * 100)) + "%")
    print("    - Words: " + str(round(((word_width * number_of_blocks / disk_space) * 100))) + "%")
    print("  Unassigned space: " + str(round((blanks / disk_space) * 100)) + "%")

    # Menu
    print("\n\n[1] Generate new drive")
    print("[2] Visualise the drive")
    print("[3] Exit")
    stats_menu(number_of_blocks, word_width, disk_space, address_width)


def print_disk(number_of_blocks: int, word_width: int, disk_space: int, address_width: int, prefix=""):
    counter = 0
    blanks = disk_space - ((word_width * number_of_blocks) + (address_width * number_of_blocks))
    print("\n Drive model:\n")
    print(prefix, end="")
    for p in range(0, len(prefix)):
        blanks -= 1
    for b in range(0, number_of_blocks):
        for a in range(0, address_width):
            print(cyan + "a", end="")
            counter += 1
        for w in range(0, word_width):
            print(green + "w", end="")
            counter += 1
    for blank in range(0, blanks):
        print(grey + "u", end="")
        counter += 1
    if counter != disk_space:
        if counter > disk_space:
            print("Error: The disk visualisation has more bits than the actual disk!!!")
        elif counter < disk_space:
            print("Error: The disk visualisation has less bits than the actual disk!!!")
            print("You should count the drawn bits and check if it matches number of address and word bits. If yes, "
                  "then you should probably add some blanks, and call it a day")
        else:
            print("Error: The disk visualisation doesn't contain valid number of bits!!!")

    # Legend informing what does each colour represent
    print(cyan + "\n\naddress")
    print(green + "word")
    print(grey + "unassigned")
    print('\x1b[0m')

    # Menu
    print("\n[1] Generate new drive")
    print("[2] Drive statistics")
    print("[3] Exit")
    answer = input("> ")
    if answer == "1":
        clear_screen()
        logo()
        run()
    elif answer == "2":
        stats(number_of_blocks, word_width, disk_space, address_width)
    elif answer == "3":
        quit(0)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def logo():
    """
    Function that prints name of the program and name of the author.
    """
    print("Simple HDD calculator")
    print("By: Wiktor Górecki (https://github.com/WiktorGorecki)")


def number_input(msg: str):
    while 1:
        try:
            result = int(input(msg))
            break
        except ValueError:
            print("Error: NaN")
    return result


def drive_input(error_message=""):
    if error_message:
        print(error_message)
    else:
        print()
    print()
    print("Specify drive properties:")
    disk_space = number_input("    Capacity :     ")
    word_width = number_input("    Size of word:  ")
    return disk_space, word_width


def run(error_message=""):
    disk_space, word_width = drive_input(error_message)
    number_of_blocks = floor(disk_space / word_width)

    calculated_number_of_blocks, calculated_address_width = calculate_number_of_fitting_blocks(number_of_blocks,
                                                                                               disk_space, word_width)
    print("\nCalculated parameters:")
    print("    Number of words: " + str(calculated_number_of_blocks))
    print("    Address width:  " + str(calculated_address_width))

    print("\n\n[1] Generate new drive")
    print("[2] Visualise the drive")
    print("[3] Drive statistics")
    print("[4] Exit")
    answer = input("> ")
    if answer == "1":
        run()
    elif answer == "2":
        print_disk(calculated_number_of_blocks, word_width, disk_space, calculated_address_width)
    elif answer == "3":
        stats(calculated_number_of_blocks, word_width, disk_space, calculated_address_width, )
    elif answer == "4":
        quit(0)


def calculate_number_of_fitting_blocks(number_of_blocks: int, disk_space: int, word_width: int):
    """
    Calculates maximum number of blocks that fit on specified drive
    :param number_of_blocks: Number of blocks of data that the disk will store
    :param disk_space: Number of unassigned bits that the program will assign
    :param word_width: Number of bits that one block will store
    :return: Number of words, Width of the address in a block
    """
    address_width = 1
    while 1:
        max_address = address_width ** 2
        if max_address < number_of_blocks:
            address_width += 1

        # Check if disk will fit all the data
        used_bits = (address_width * number_of_blocks) + (word_width * number_of_blocks)
        while used_bits > disk_space:
            number_of_blocks -= 1
            used_bits = (address_width * number_of_blocks) + (word_width * number_of_blocks)

        if max_address >= number_of_blocks:
            return number_of_blocks, address_width


logo()
run()
