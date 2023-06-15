import os
import importlib.util

os.system("")

CYAN = '\033[36m'
GREEN = '\033[32m'
GREY = '\033[37m'


def show_stats_menu(number_of_blocks, word_width, disk_space, address_width):
    answer = input("> ")
    if answer == "1":
        clear_screen()
        show_logo()
        run()
    elif answer == "2":
        show_disk(number_of_blocks, word_width, disk_space, address_width)
    elif answer == "3":
        quit(0)
    else:
        stats_menu_path = os.path.join("plugins", f"stats_menu_{answer}.py")
        if os.path.exists(stats_menu_path):
            run_plugin(stats_menu_path, number_of_blocks, word_width, disk_space, address_width)
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
    print("[3] Exit")
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
        run()
    elif answer == "2":
        show_stats(number_of_blocks, word_width, disk_space, address_width)
    elif answer == "3":
        quit(0)


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


def run_plugin(plugin_path, *args):
    plugin_name = os.path.splitext(os.path.basename(plugin_path))[0]
    spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.run(*args)


def run(error_message=""):
    disk_space, word_width = drive_input(error_message)
    number_of_blocks = disk_space // word_width

    calculated_number_of_blocks, calculated_address_width = calculate_fitting_blocks(number_of_blocks,
                                                                                     disk_space, word_width)
    print("\nCalculated parameters:")
    print("    Number of words: " + str(calculated_number_of_blocks))
    print("    Address width:  " + str(calculated_address_width))

    print("\n\n[1] Generate new drive")
    print("[2] Visualize the drive")
    print("[3] Drive statistics")
    print("[4] Exit")
    answer = input("> ")
    if answer == "1":
        run()
    elif answer == "2":
        show_disk(calculated_number_of_blocks, word_width, disk_space, calculated_address_width)
    elif answer == "3":
        show_stats(calculated_number_of_blocks, word_width, disk_space, calculated_address_width)
    elif answer == "4":
        quit(0)


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


def load_plugins():
    plugin_folder = "plugins"
    plugins = []
    if os.path.isdir(plugin_folder):
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py"):
                plugins.append(os.path.join(plugin_folder, filename))
    return plugins


def main_menu():
    clear_screen()
    show_logo()

    print("\n\n[1] Calculate a simple drive")
    print("[2] Plugins")
    print("[3] Exit")
    answer = input("> ")
    if answer == "1":
        run()
    elif answer == "2":
        plugins_menu()
    elif answer == "3":
        quit(0)
    else:
        main_menu()


def plugins_menu():
    # Load plugins
    plugins = load_plugins()
    if plugins:
        print("\nAvailable Plugins:")
        for i, plugin in enumerate(plugins, start=1):
            print(f"[{i}] {plugin}")
        print("Enter the number of the plugin to execute or press Enter to continue.")

        plugin_number = input("> ")
        if plugin_number:
            try:
                plugin_index = int(plugin_number) - 1
                selected_plugin = plugins[plugin_index]
                run_plugin(selected_plugin)
            except (ValueError, IndexError):
                print("Invalid plugin number. Continuing...")


def main():
    main_menu()


if __name__ == "__main__":
    main()
