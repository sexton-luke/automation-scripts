"""
Title: File Sorter
Author: Luke Sexton
GitHub: https://github.com/valentina-valentine

File Sorter sorts file types based on chosen folder name under a root path.
* Options to customize for inputting
"""

# Import modules
import os
import time

from watchdog.observers import Observer

from settings import MODES
from settings import Settings
from watch_directory import WatchDirectory


def directory_exists(path):
    """Check desired path exists on the operating system"""
    return os.path.exists(path)


def get_root_directory():
    """Return root path from user input if exists"""
    information_text = "Please enter the root directory path >>> "
    error_text = "Directory does not exist. Please try again.."

    print("Prompting root directory..")
    while True:
        user_input = input(information_text)
        if directory_exists(user_input):
            return user_input
        else:
            print(error_text)


if __name__ == '__main__':
    # Get root directory path
    # root_directory = "enter path here.."
    root_directory = get_root_directory()
    print("Root directory ->", root_directory)

    try:
        if directory_exists(root_directory):
            # Initialize Settings with mode and root directory
            print("Initializing Settings class with mode ->", MODES['auto'])
            settings = Settings(MODES['auto'], root_directory)

            automatic_file_types = settings.get_automatic_file_types()
            directory_dictionary = settings.get_directory_paths()
            shortcuts = settings.get_shortcuts()
            shortcuts_file_path = settings.get_shortcuts_file_path()

            print("automatic file types ->", automatic_file_types,
                  "\ndirectory dictionary ->", directory_dictionary,
                  "\nshortcuts ->", shortcuts,
                  "\nshortcuts file path ->", shortcuts_file_path)

            # Initialize event handler
            print("Initializing event handler -> WatchDirectory()..")
            event_handler = WatchDirectory(automatic_file_types, directory_dictionary, shortcuts, shortcuts_file_path)

            # Initialize Observer
            observer = Observer()
            observer.schedule(event_handler, root_directory, recursive=False)
            observer.start()
            print("Observer has started..")

            try:  # Run until cancelled
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
                print("Observer has stopped..")
            observer.join()
    except TypeError:
        print("User closed program.. Goodbye..")
