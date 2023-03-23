#!/usr/bin/env python3
"""
iterate all the folders
keep track which files are in each folder
for each folder, call the rename file function, and then the folder rename function
keep track of the renames
rename all files, then all folders
]


"""
import argparse
import os
import pathlib
import shutil
import time

import webview
from natsort import natsorted

import rename

print(f"Rename program started")
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
print(args)


def printt(*argss, **kwargs):
    if args.verbose:
        to_print = " ".join(map(str, argss))
        print(to_print, **kwargs)


def determine_renames(folder_path, filenames):
    printt(f"Determining to what the files are going to be renamed")
    renames = []
    for filename in filenames:
        file_path = os.path.join(folder_path, filename)
        filename_base = pathlib.Path(file_path).stem
        filename_extension = pathlib.Path(file_path).suffix
        new_filename = rename.rename_file(folder_path, filename, filename_base,
                                          filename_extension)  # separate function for easier configuration
        printt(f"{filename} -> {new_filename}")
        if filename == new_filename:
            printt(f"Filename not changed, ignoring.")
            continue
        new_file_path = os.path.join(folder_path, new_filename)
        renames.append([file_path, new_file_path])
    printt(f"All {len(renames)} determined")
    return renames


def validate_renames(renames):
    printt(f"Validating the paths to what the files are going to be renamed")
    used_paths = []
    for rename in renames:
        old = rename[0]
        if not os.path.isfile(old):
            quit(f"Cannot rename, not a file: {old}")
        new = rename[1]
        if os.path.exists(new):
            quit(f"Cannot rename: existing path: {new}")
        if new in used_paths:
            quit(f"Cannot rename: duplicate renamed file, files must have unique filenames: {new}")
        used_paths.append(new)

    printt(f"All renames are valid")


def save_rename_history(folder_path, renames):
    printt(f"Saving the renaming history")
    # use / as separator because its the only visible illegal filename character
    # https://stackoverflow.com/questions/1976007/what-characters-are-forbidden-in-windows-and-linux-directory-names
    # save the filename only and not the full path case cluttered and in case folder gets moved
    runtime_timestamp = time.strftime("%Y%m%d_%H%M%S")
    rename_history_filename = f"rename_history_{runtime_timestamp}.txt"
    with open(os.path.join(folder_path, rename_history_filename), "w") as history_file:
        for rename in renames:
            old_filename = pathlib.Path(rename[0]).name
            new_filename = pathlib.Path(rename[1]).name
            history_file.write(f"{old_filename}/{new_filename}\n")
    printt(f"Saved rename history as {rename_history_filename}")


def apply_renames(renames):
    printt(f"Renaming the files")
    applied_renames = []  # in case the renaming proces throws exceptions so we can undo partial process
    for rename in renames:
        try:
            from_path = rename[0]
            to_path = rename[1]
            printt(f"{from_path} -> {to_path}")
            if not args.test:
                shutil.move(from_path, to_path)
            applied_renames.append(rename)
        except:
            print(f"A rename has failed: {rename}. WARNING: Not all files have been renamed.")
    printt(f"Done renaming")
    return applied_renames


def read_filenames(folder_path):
    printt(f"Reading filenames from {folder_path}")
    filenames = []
    for filename in os.listdir(folder_path):
        filename_path = os.path.join(folder_path, filename)
        if not os.path.isfile(filename_path):
            # skip non-file items like folders
            continue
        if filename.startswith("rename_history_") and filename.endswith(".txt"):
            printt(f"Skipping backup file {filename}")
            continue
        if args.ignore_hidden and filename.startswith("."):
            printt(f"Ignoring hidden file {filename}")
            continue
        filenames.append(filename)

    filenames = natsorted(filenames, key=lambda y: y.lower())  # sort items same as the file manager does
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


def get_folder_paths():
    if not args.folder_paths or len(args.folder_paths) == 0:
        printt("No folders supplied as argument, launching folder picker")
        folder_paths = ask_folders()
        if not folder_paths:
            quit("You picked an invalid folder")

        for folder_path in folder_paths:
            if not folder_path or not os.path.isdir(folder_path):
                quit("You picked an invalid folder")
    else:
        folder_paths = args.folder_paths

    # recursively retrieve all the folders within the folders until the defined depth
    for depth in range(1, args.depth + 1):
        printt(f"Scanning depth level {depth}")
        parent_folder_paths = folder_paths
        folder_paths = []
        for folder_path in parent_folder_paths:
            for item in os.listdir(folder_path):
                if os.path.isdir(os.path.join(folder_path, item)):
                    folder_paths.append(item)

    folder_paths = [os.path.abspath(folder_path) for folder_path in folder_paths]
    print(f"Renaming items in folders: {folder_paths}")
    return folder_paths


folder_paths = get_folder_paths()
for folder_path in folder_paths:
    filenames = read_filenames(folder_path)
    renames = determine_renames(folder_path, filenames)
    validate_renames(renames)
    applied_renames = apply_renames(renames)
    # rename folder here todo
    save_rename_history(folder_path, applied_renames)
print(f"Rename program finished")
