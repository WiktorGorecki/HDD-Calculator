import os
import importlib.util

from utils import run_plugin, load_plugins

os.system("")

CYAN = '\033[36m'
GREEN = '\033[32m'
GREY = '\033[37m'


def show_stats_menu(number_of_blocks, word_width, disk_space, address_width):
    answer = input("> ")
    if answer == "1":
        clear_screen()
        show_logo()
    elif answer == "2":
        show_disk(number_of_blocks, word_width, disk_space, address_width)
    elif answer == "3":
        quit(0)
    else:
        stats_menu_path = os.path.join("plugins", f"stats_menu_{answer}.py")
        if os.path.exists(stats_menu_path):
            run_plugin(stats_menu_path)
        else:
            show_stats_menu(number_of_blocks, word_width, disk_space, address_width)


def show_stats(number_of_blocks: int, word_width: int, disk_space: int, address_width: int):
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
    print("[2] Visualize the drive")
    print("[3] Back to the main menu")
    show_stats_menu(number_of_blocks, word_width, disk_space, address_width)


def show_disk(number_of_blocks: int, word_width: int, disk_space: int, address_width: int, prefix=""):
    counter = 0
    blanks = disk_space - ((word_width * number_of_blocks) + (address_width * number_of_blocks))
    print("\n Drive model:\n")
    print(prefix, end="")
    for p in range(len(prefix)):
        blanks -= 1
    for b in range(number_of_blocks):
        for a in range(address_width):
            print(CYAN + "a", end="")
            counter += 1
        for w in range(word_width):
            print(GREEN + "w", end="")
            counter += 1
    for _ in range(blanks):
        print(GREY + "u", end="")
        counter += 1
    if counter != disk_space:
        if counter > disk_space:
            print("Error: The disk visualization has more bits than the actual disk!!!")
        elif counter < disk_space:
            print("Error: The disk visualization has fewer bits than the actual disk!!!")
            print("You should count the drawn bits and check if it matches the number of address and word bits. "
                  "If yes, then you should probably add some blanks and call it a day")
        else:
            print("Error: The disk visualization doesn't contain a valid number of bits!!!")

    # Legend informing what each color represents
    print(CYAN + "\n\naddress")
    print(GREEN + "word")
    print(GREY + "unassigned")
    print('\x1b[0m')

    # Menu
    print("\n[1] Generate new drive")
    print("[2] Drive statistics")
    print("[3] Exit")
    answer = input("> ")
    if answer == "1":
        clear_screen()
        show_logo()
    elif answer == "2":
        show_stats(number_of_blocks, word_width, disk_space, address_width)
    elif answer == "3":
        quit(0)
    else:
        show_stats_menu(number_of_blocks, word_width, disk_space, address_width)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_logo():
    """
    Function that prints the name of the program and the name of the author.
    """
    print("Simple HDD calculator")
    print("By: Wiktor Górecki (https://github.com/WiktorGorecki)")


def get_number_input(msg: str):
    while True:
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
    disk_space = get_number_input("    Capacity :     ")
    word_width = get_number_input("    Size of word:  ")
    return disk_space, word_width


def main_menu():
    clear_screen()
    show_logo()

    print("\n\n[1] Plugins")
    print("[2] Exit")
    main_menu_answer = input("> ")
    if main_menu_answer == "1":
        plugins_menu()
    elif main_menu_answer == "2":
        quit(0)


def plugins_menu():
    plugins = load_plugins()

    print("\nChoose a plugin: ")
    for index, (plugin_path, display_name) in enumerate(plugins, start=1):
        print(f"[{index}] {display_name}")

    print("\n[0] Back")
    answer = input("> ")

    if answer == "0":
        main_menu()
    elif answer.isdigit() and 0 < int(answer) <= len(plugins):
        plugin_path, _ = plugins[int(answer) - 1]
        plugin_path += ".py"
        clear_screen()
        show_logo()
        run_plugin(plugin_path)
    else:
        plugins_menu()


if __name__ == "__main__":
    main_menu()
