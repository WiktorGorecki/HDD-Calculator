import os
from math import floor

from ..main import drive_input


def run():
    disk_space, word_width = drive_input()
    number_of_blocks = floor(disk_space / word_width)
    calculated_number_of_blocks, calculated_address_width = calculate_fitting_blocks(number_of_blocks,
                                                                                     disk_space, word_width)
    print("\nCalculated parameters:")
    print("    Number of words: " + str(calculated_number_of_blocks))
    print("    Address width:  " + str(calculated_address_width))

    # Return the calculated parameters
    return calculated_number_of_blocks, word_width, disk_space, calculated_address_width


def calculate_fitting_blocks(number_of_blocks: int, disk_space: int, word_width: int):
    """
    Calculates the maximum number of blocks that fit on the specified drive.
    :param number_of_blocks: Number of blocks of data that the disk will store.
    :param disk_space: Number of unassigned bits that the program will assign.
    :param word_width: Number of bits that one block will store.
    :return: Number of words, Width of the address in a block.
    """
    address_width = 1
    while True:
        max_address = address_width ** 2
        if max_address < number_of_blocks:
            address_width += 1

        # Check if the disk will fit all the data
        used_bits = (address_width * number_of_blocks) + (word_width * number_of_blocks)
        while used_bits > disk_space:
            number_of_blocks -= 1
            used_bits = (address_width * number_of_blocks) + (word_width * number_of_blocks)

        if max_address >= number_of_blocks:
            return number_of_blocks, address_width
