import os
import shutil
import subprocess


def create_directory(path, name):
    """Create directory with given path"""
    print("Create directory --> With path " + path + " With name " + name)
    os.mkdir(path)


def move_file(src_path, destination_path, create_folder_answer):
    """Move file from src to destination"""
    try:
        if create_folder_answer == "":
            print("Move file --> From src path --> ", src_path, " To destination --> ", destination_path)
            shutil.move(src_path, destination_path)
        else:
            print("Src path --> " + src_path)
            print("Destination path --> " + destination_path)
            print("Create folder answer --> " + create_folder_answer)
            final_destination_path = destination_path + "\\" + create_folder_answer
            create_directory(final_destination_path, create_folder_answer)
            print("Move file --> From src path --> ", src_path, " To destination --> ", final_destination_path)
            shutil.move(src_path, final_destination_path)

        open_directory(destination_path)
    except shutil.Error:
        print("Move file --> Error moving file.. Please try again..")


def open_directory(path):
    """Open directory in Windows Explorer"""
    program_name = 'explorer.exe'
    browser_path = os.path.join(os.getenv('WINDIR'), program_name)

    print("Open directory --> At path " + path + "With " + program_name)

    if os.path.isdir(path):
        subprocess.run([browser_path, path])


def handle_file(src_path,
                file_type,
                automatic_file_types,
                directory_dictionary,
                shortcuts,
                shortcuts_file_path):
    """Handle file based on file type"""
    print("Handle file --> automatic mode..")

    # Check if automatic file type
    if file_type in automatic_file_types:
        print("File type --> ", file_type, " In automatic file types..")
        folder_name = automatic_file_types[file_type]
        destination_path = directory_dictionary[folder_name]

        move_file(src_path, destination_path, "")
    else:
        # Open shortcuts file in notepad
        open_file_with_notepad(shortcuts_file_path)

        destination_path = get_destination_path(shortcuts, directory_dictionary)
        create_folder_answer = get_answer()

        move_file(src_path, destination_path, create_folder_answer)


def open_file_with_notepad(path):
    """Open file with given path"""
    program_name = "notepad.exe"

    print("Opening shortcuts at -->", path, "With", program_name)
    subprocess.Popen([program_name, path])


def get_destination_path(shortcuts, directory_dictionary):
    """Prompt user for destination path"""
    information_text = "Please enter destination folder >>> "
    error_text = "Chosen destination does not exist. Please enter a valid folder name or shortcut.."

    print("Get destination path --> Prompting destination path..")
    while True:
        # Get user input and change to uppercase values
        user_input = input(information_text).upper()
        print("Get destination path --> You entered: " + user_input)

        # Check if user input is a shortcut
        if user_input in shortcuts.keys():
            # User input is a shortcut, get destination path
            print("Get destination path --> Shortcut accepted..")
            folder_name = shortcuts[user_input]
            user_input = directory_dictionary[folder_name]
            break
        elif user_input in directory_dictionary.keys():
            # User input is a key in the directory dictionary, get destination path
            print("Get destination path --> Input accepted..")

            user_input = directory_dictionary[user_input]
            break
        else:
            print("Get destination path --> Input rejected: " + error_text)

    print("Get destination path --> Returning destination path --> " + user_input)
    return user_input


def get_answer():
    """Return name of new folder. Return empty string if cancelled"""
    information_text = "Would you like to create a folder for the file to reside in? Press enter if no >>> "
    error_text = "Folder name is too long. Please ensure file name is less than 255 characters.."
    max_folder_length = 255

    print("Get answer --> Prompting folder creation..")
    while True:
        user_input = str(input(information_text))
        print("Get answer --> You entered: " + user_input)

        # Check length of user input.
        if len(user_input) >= max_folder_length:
            print(error_text)
        else:
            print("Get answer --> Input accepted..")
            return user_input
