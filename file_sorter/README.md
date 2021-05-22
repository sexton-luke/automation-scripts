# File Sorter

File sorter sorts files based on user input of folder name within a specified root path.

## [IMPORTANT] - Setup automatic file types and folder names
- [x] Default mode: AUTO
- [ ] Please ensure you open and configure the following files:
```
text_files/automatic_file_types.txt
text_files/folder_names.txt
```
- [ ] If you do not wish to be prompted for the root path, change the following in `main.py` to:
```
root_directory = get_root_directory()  # Line 41 >>> Comment out if using specific root path
# root_directory = "enter path here.." # Line 42 >>> Uncomment and enter specific root path
```

## Modes
### _AUTO_
In AUTO mode, files dragged into a watched directory will be automatically filed by the dictionary specified in `text_files/automatic_file_types.txt`.

### _MANUAL_
In MANUAL mode, files dragged into a watched directory will always require user input by either **_shortcut_** or **_folder name_**.
