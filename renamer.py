#!/usr/bin/env python3
"""
EDIT THE rename.py SCRIPT, NOT THIS

this script:
 - iterate all the folders
 - keep track which files are in each folder
 - for each folder, call the rename file function, and then the folder rename function
 - keep track of the renames
 - rename all files, then all folders
"""
class RenamerException(Exception):
    """Custom exception class for Renamer errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

try:
    import time
    import traceback
    import rename  # PROGRAM THE RENAMES HERE
    import re

    import argparse
    import os
    import pathlib
    import shutil
    import tkinter as tk
    from tkinter import filedialog

    parser = argparse.ArgumentParser(
        prog="Renamer",
        description="Rename files with Python code",
        epilog="Created by Jort: github.com/jort-dev")
    parser.add_argument("-t", "--test",
                        help="disables the actual moving of files",
                        action="store_true",
                        )
    parser.add_argument("-v", "--verbose",
                        help="prints more messages about the process",
                        action="store_true",
                        )
    parser.add_argument("-w", "--hide-warnings",
                        help="hide warnings about uninstalled packages",
                        action="store_true",
                        )
    parser.add_argument("-i", "--ignore-hidden",
                        help="ignore hidden files starting with a dot. "
                             "the hidden .rename_history_TIMESTAMP.txt file is already ignored",
                        action="store_true",
                        )
    parser.add_argument("-d", "--depth",
                        help="the depth of the folders to use. default is 0, just the files in the selected folders,"
                             " 1 is to rename only the files within the folders of the selected folders, etc",
                        type=int,
                        default=0
                        )
    parser.add_argument("folder_paths",
                        nargs=argparse.REMAINDER,
                        help="the path to the folder(s) containing the files to rename",
                        )
    args = parser.parse_args()


    def printt(*argss, **kwargs):
        if args.verbose:
            to_print = " ".join(map(str, argss))
            print(to_print, **kwargs)


    printt(f"Rename program started with arguments: {args}")

    # dont require natsort to be installed
    try:
        from natsort import os_sorted

        NATSORT_AVAILABLE = True
    except ImportError:
        if not args.hide_warnings:
            print(
                f"Warning: 'natsort' not installed, files will not be iterated the same way your file explorer shows them sorted by name")
        NATSORT_AVAILABLE = False

    # dont require webview to be installed
    try:
        import webview

        WEBVIEW_AVAILABLE = True
    except ImportError:
        if not args.hide_warnings:
            print(f"Warning: 'webview' not installed, you will not be able to select multiple folders")
        WEBVIEW_AVAILABLE = False


    def determine_renames(folder_path, filenames):
        printt(f"Determining to what the files are going to be renamed")
        renames = []
        folder_name = os.path.basename(folder_path)
        parent_folder_path = folder_path[:-len(folder_name)]
        # -1 to remove the trailing / which makes basename return empty string
        parent_folder_name = os.path.basename(folder_path[:-len(os.path.basename(folder_path)) - 1])
        file_index = 0  # for tracking and preventing double filenames
        amount_of_files = len(filenames)
        print()  # progress bar reset
        for filename in filenames:
            print(f"Renaming file {file_index} / {amount_of_files}: {filename}", end="\r")
            file_path = os.path.join(folder_path, filename)
            filename_base = pathlib.Path(file_path).stem
            filename_extension = pathlib.Path(file_path).suffix
            printt(f"Asking rename for {filename} with parameters "
                   f"{filename=}, {filename_base=}, {filename_extension=}, {file_path=}, {folder_path=}, {folder_name=}")
            new_filename = rename.rename_file(
                filename=filename,
                filename_base=filename_base,
                filename_extension=filename_extension,
                file_path=file_path,
                folder_path=folder_path,
                folder_name=folder_name,
                file_index=file_index,
            )
            printt(f"{filename} -> {new_filename}")
            if filename == new_filename:
                printt(f"Filename not changed, ignoring.")
                continue
            new_file_path = os.path.join(folder_path, new_filename)
            renames.append([file_path, new_file_path])
            file_index += 1

        print()  # progress bar reset
        print()  # progress bar reset

        printt(f"All {len(renames)} file renames determined, "
               f"asking folder rename with parameters {folder_name=}, {folder_path=}, {parent_folder_name=}")
        folder_name_renamed = rename.rename_folder(
            folder_name=folder_name,
            folder_path=folder_path,
            parent_folder_name=parent_folder_name,
        )
        renamed_folder_path = os.path.join(parent_folder_path, folder_name_renamed)
        folder_rename = [folder_path, renamed_folder_path]
        printt(f"Folder rename: {folder_path} -> {renamed_folder_path}")
        renames.insert(0, folder_rename)
        return renames


    def validate_renames(all_renames):
        printt(f"Validating the renames")
        for renames in all_renames:
            folder_rename = renames[0]
            folder_from = folder_rename[0]
            folder_to = folder_rename[1]
            printt(f"Validating renames for {folder_from}")
            if folder_from != folder_to:  # if we are renaming the folder, check if destination path is available
                if os.path.exists(folder_to):
                    raise RenamerException(f"Cannot rename: folder rename is existing path: {folder_to}")

            used_renames = []
            for rename in renames[1:]:
                old = rename[0]
                if not os.path.isfile(old):
                    raise RenamerException(f"Cannot rename, not a file: {old}")
                new = rename[1]
                if os.path.exists(new):
                    raise RenamerException(f"Cannot rename: existing path: {old} -> {new}")
                for used_rename in used_renames:
                    if used_rename[1] == new:
                        raise RenamerException(f"Cannot rename: duplicate renamed file, files must have unique filenames: "
                             f"can't rename {old} to {new} because {used_rename[0]} is already being renamed to it. Consider including the 'file_index' parameter in your new filename.")
                used_renames.append(rename)

        printt(f"All renames are valid")


    def save_rename_history(all_renames):
        printt(f"Saving the renaming history")
        # use / as separator because its the only visible illegal filename character
        # https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
        # save the filename only and not the full path case cluttered and in case folder gets moved
        runtime_timestamp = time.strftime("%Y%m%d_%H%M%S")
        rename_history_filename = f".rename_history_{runtime_timestamp}.txt"
        printt(f"Saving rename history files as {rename_history_filename}")
        for renames in all_renames:
            folder_rename = renames[0]
            folder_from = folder_rename[0]
            folder_to = folder_rename[1]
            append = ""
            if folder_from != folder_to:
                append = f" (was {folder_from})"
            printt(f"Saving renames for {folder_to}{append}")

            with open(os.path.join(folder_to, rename_history_filename), "w") as history_file:
                old_foldername = pathlib.Path(folder_from).name
                new_foldername = pathlib.Path(folder_to).name
                history_file.write(f"{old_foldername}/{new_foldername}\n")

                for rename in renames[1:]:
                    # the first rename is the folder rename
                    old_filename = pathlib.Path(rename[0]).name
                    new_filename = pathlib.Path(rename[1]).name
                    history_file.write(f"{old_filename}/{new_filename}\n")


    def apply_renames(all_renames):
        printt(f"Renaming the files")
        all_applied_renames = []  # in case the renaming proces throws exceptions so we can undo partial process
        for renames in all_renames:
            applied_renames = []
            folder_rename = renames[0]
            folder_from = folder_rename[0]
            folder_to = folder_rename[1]
            printt(f"Renaming files in {folder_from}")
            applied_renames.append(folder_rename)  # always save because the first line should always be the folder rename
            for rename in renames[1:]:
                try:
                    from_path = rename[0]
                    to_path = rename[1]
                    printt(f"File {from_path} -> {to_path}")
                    if not args.test:
                        shutil.move(from_path, to_path)
                        pass
                    applied_renames.append(rename)
                except:
                    print(f"A rename has failed: {rename}. WARNING: Not all files have been renamed.")

            if folder_from != folder_to:
                printt(f"Folder: {folder_from} -> {folder_to}")
                if not args.test:
                    shutil.move(folder_from, folder_to)
                    pass
            else:
                printt("No folder rename specified")
            all_applied_renames.append(applied_renames)
        printt(f"Done renaming")
        return all_applied_renames


    def natural_sort_key(s):
        """A custom natural sort key function for fallback sorting."""
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


    def sort_items(items):
        """Sort items using natsort if available, otherwise use a custom method."""
        if NATSORT_AVAILABLE:
            return os_sorted(items)
        else:
            return sorted(items, key=natural_sort_key)


    def read_filenames(folder_path):
        printt(f"Reading filenames from {folder_path}")
        filenames = []
        for filename in os.listdir(folder_path):
            filename_path = os.path.join(folder_path, filename)
            if not os.path.isfile(filename_path):
                # skip non-file items like folders
                continue
            if filename.startswith(".rename_history_") and filename.endswith(".txt"):
                printt(f"Skipping backup file {filename}")
                continue
            if args.ignore_hidden and filename.startswith("."):
                printt(f"Ignoring hidden file {filename}")
                continue
            filenames.append(filename)

        filenames = sort_items(filenames)  # sort items same as the file manager does if available
        printt(f"Read {len(filenames)} filenames")
        return filenames


    def ask_folders():
        # returns None if no folder is choosen, otherwise a list of paths
        dir_paths = None

        def open_file_dialog(w):
            nonlocal dir_paths
            try:
                dir_paths = w.create_file_dialog(dialog_type=webview.FOLDER_DIALOG,
                                                 allow_multiple=True,
                                                 directory=os.getcwd()
                                                 )
            except TypeError:
                pass  # user exited file dialog without picking
            finally:
                w.destroy()

        printt(f"Launching folder picker")
        window = webview.create_window("", hidden=True)
        webview.start(open_file_dialog, window)
        printt(f"You picked these folders: {dir_paths}")
        return dir_paths


    def ask_folder():
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory()
        if not folder_path:  # no path is empty string
            return None
        return [folder_path]


    def get_folder_paths():
        if not args.folder_paths or len(args.folder_paths) == 0:
            printt("No folders supplied as argument, launching folder picker")
            if WEBVIEW_AVAILABLE:
                folder_paths = ask_folders()
            else:
                folder_paths = ask_folder()
            if not folder_paths:
                raise RenamerException("No folder picked")

        else:
            folder_paths = args.folder_paths

        for folder_path in folder_paths:
            if not folder_path or not os.path.isdir(folder_path):
                raise RenamerException("You picked an invalid folder")

        # sanitize trailing slashes
        folder_paths = [os.path.normpath(folder_path) for folder_path in folder_paths]

        # recursively retrieve all the folders within the folders until the defined depth
        for depth in range(1, args.depth + 1):
            printt(f"Scanning depth level {depth}")
            parent_folder_paths = folder_paths
            folder_paths = []
            for folder_path in parent_folder_paths:
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        folder_paths.append(item_path)
            printt(f"Found {len(folder_paths)} items at depth {depth}: {folder_paths}")

        if len(folder_paths) == 0:
            raise RenamerException(f"No folders found at this depth level. Try lowering it.")
        print(f"Renaming items in folders: {folder_paths}")
        return folder_paths


    folder_paths = get_folder_paths()
    all_folders_renames = []
    for folder_path in folder_paths:
        filenames = read_filenames(folder_path)
        renames = determine_renames(folder_path, filenames)
        all_folders_renames.append(renames)

    validate_renames(all_folders_renames)
    all_applied_renames = apply_renames(all_folders_renames)
    save_rename_history(all_applied_renames)
except KeyboardInterrupt:
    quit("Stopped")
except RenamerException as e:
    print(f"Renamer error: {e}")
except Exception as e:
    traceback.print_exc()
    print(f"Unexpected error renaming: {e}")

print(f"Rename script finished, this window can be closed")
while True:
    try:
        time.sleep(0.01)
    except KeyboardInterrupt:
        quit("Stopped")
