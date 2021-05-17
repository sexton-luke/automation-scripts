from watchdog.events import FileSystemEventHandler

import handler_functions


class WatchDirectory(FileSystemEventHandler):
    def __init__(self, automatic_file_types, directory_dictionary, shortcuts, shortcuts_file_path):
        self.automatic_file_types = automatic_file_types
        self.directory_dictionary = directory_dictionary
        self.shortcuts = shortcuts
        self.shortcuts_file_path = shortcuts_file_path

    def on_created(self, event):
        """Handle file type based on settings mode"""
        rfind_error_code = -1
        src_path = event.src_path

        print("WatchDirectory() -> ", src_path, event.event_type)

        last_period_index = src_path.rfind('.')  # rfind() return index of last occurring specified value

        print("WatchDirectory() last period found at index ->", last_period_index)

        if last_period_index != rfind_error_code:
            # Get file type: substring from range [last period : end of string]
            file_type = src_path[last_period_index:]

            print("WatchDirectory() file type ->", file_type, "length ->", str(len(file_type)))

            handler_functions.handle_file(src_path,
                                          file_type,
                                          self.automatic_file_types,
                                          self.directory_dictionary,
                                          self.shortcuts,
                                          self.shortcuts_file_path)
