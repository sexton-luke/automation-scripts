import ast
import os


# Static functions
def generate_shortcut(start, step, name, shortcut_characters):
    """Return first letter of name as shortcut. If shortcut exists, return two, three, etc. letters as shortcut"""
    if name[start:step] in shortcut_characters:
        if step < len(name) - 1:
            print("Shortcut exists.. ")
            return generate_shortcut(start, step + 1, name, shortcut_characters)
    else:
        return name[:step].upper()


def print_dictionary_items(directory_paths):
    """Print each key, value of the dictionary"""
    print("Directory dictionary key value pairs..")
    for key, value in directory_paths.items():
        print("key value pair: {0}: {1}".format(key, value))


def write_shortcuts_to_file(shortcuts, path):
    """Write shortcuts to file located at root folder"""
    title = "File Sorter Shortcuts \n"
    write_create = 'w+'
    with open(path, write_create) as file:
        file.write(title)
        for key, value in shortcuts.items():
            file.write("\nShortcut: {0}\t Path: {1}".format(key, value))


def get_file_types_as_dictionary(file_name):
    """Retrieve contents of dictionary located in specified file"""
    read = 'r'
    with open(file_name, read) as file:
        contents = ast.literal_eval(file.read())

    return contents


def read_file_contents(file_name):
    """Retrieve contents of specified file"""
    read = 'r'
    with open(file_name, read) as file:
        contents = file.readline().split(',')

    return contents


AUTOMATIC_FILE_TYPES_FILE = 'text_files/automatic_file_types.txt'
FOLDER_NAMES_FILE = 'text_files/folder_names.txt'
SHORTCUTS_FILE_NAME = 'shortcuts.txt'
MODES = {'auto': 'AUTO', 'manual': 'MANUAL'}


class Settings:
    def __init__(self, mode, root_directory):
        """Setup root directory, folder names, and shortcuts based on given mode"""
        self.mode = mode
        self.root_directory = root_directory
        self.directory_paths = {}

        # Set directory paths based off mode
        if mode == MODES['auto']:  # Setup folder structures for partial automatic filing
            # Set directory paths
            self.automatic_file_types = get_file_types_as_dictionary(AUTOMATIC_FILE_TYPES_FILE)
            names = read_file_contents(FOLDER_NAMES_FILE)
            self.directory_paths = self.setup_directory_paths_with_specific_names(names)

        elif mode == MODES['manual']:
            # setup folder structure with user input required
            self.directory_paths = self.setup_all_directory_paths()

        print("Directory paths ->", self.directory_paths)
        print("Automatic file paths ->", self.automatic_file_types)

        # Setup shortcuts and write file to root directory
        self.shortcuts = self.get_shortcuts()
        self.shortcuts_file_path = root_directory + "\\" + SHORTCUTS_FILE_NAME
        write_shortcuts_to_file(self.shortcuts, self.shortcuts_file_path)

    # Getters
    def get_directory_paths(self):
        return self.directory_paths

    def get_automatic_file_types(self):
        return self.automatic_file_types

    def get_shortcuts_file_path(self):
        return self.shortcuts_file_path

    def get_mode(self):
        return self.mode

    # Class specific functions
    def is_mode_auto(self):
        """Return boolean value based on mode"""
        return self.mode == MODES['auto']

    def setup_all_directory_paths(self):
        """Manual: Return dictionary of {folder name: folder path} key value pairs for all folders under the root
        directory """
        dictionary = {}

        for root, directories, files in os.walk(self.root_directory, topdown=True):
            for directory in directories:
                # Change values to upper for error handling user input
                dictionary[directory] = os.path.join(root, directory)
        print_dictionary_items(dictionary)
        return dictionary

    def setup_directory_paths_with_specific_names(self, names):
        """Automatic: Return dictionary of {folder name: folder path} key value pairs applicable to folder names in
        given list """
        dictionary = {}

        for root, directories, files in os.walk(self.root_directory, topdown=True):
            for directory in directories:
                if directory in names:
                    # Change values to upper for error handling user input
                    dictionary[directory] = os.path.join(root, directory)
        print_dictionary_items(dictionary)

        return dictionary

    def get_shortcuts(self):
        """Generate unique folder name shortcuts for user input when manually sorting"""
        print("---- GENERATING SHORTCUTS ----")
        shortcut_characters = {}
        start = 0
        step = 1

        print("-- Directory Paths Dictionary --")
        for name in self.directory_paths.keys():
            print("Key name ->", name, "\nStart index ->", start, "\nStep index", step)
            shortcut = generate_shortcut(start, step, name, shortcut_characters)
            print("Shortcut generated ->", shortcut)
            if shortcut not in self.directory_paths.keys():
                shortcut_characters[shortcut] = name
            else:
                print("shortcut:", shortcut, "skipped as folder name exists with the same name as shortcut..")
        print("shortcuts ->", shortcut_characters)

        return shortcut_characters
