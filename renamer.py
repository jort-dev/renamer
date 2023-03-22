#!/usr/bin/env python3
"""
- determine the new filenames
- check if any new filename already exists, if yes, abort all
- rename all
- save the history
"""

import os
import pathlib
import shutil
import sys
import time

import webview
from natsort import natsorted

import rename

debug = False  # enable more printed messages, disables the actual renaming of files
test = True  # enable testing parameters like the test folder


def printt(*args, **kwargs):
    if debug:
        to_print = " ".join(map(str, args))
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
            if not debug:
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
        filenames.append(filename)

    filenames = natsorted(filenames, key=lambda y: y.lower())  # sort items same as the file manager does
    printt(f"Read {len(filenames)} filenames")
    return filenames


def ask_folder():
    dir_path = None

    def open_file_dialog(w):
        nonlocal dir_path
        try:
            if test:
                dir_path = w.create_file_dialog(webview.FOLDER_DIALOG, directory="/home/jort/rename_test")[0]
            else:
                dir_path = w.create_file_dialog(webview.FOLDER_DIALOG, directory=os.getcwd())[0]
        except TypeError:
            pass  # user exited file dialog without picking
        finally:
            w.destroy()

    window = webview.create_window("", hidden=True)
    webview.start(open_file_dialog, window)
    return dir_path


def get_folder_path():
    folder_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not folder_path:
        printt("No path supplied as argument, launching folder picker")
        folder_path = ask_folder()
        if not folder_path or not os.path.isdir(folder_path):
            quit("You picked an invalid folder")

    folder_path = os.path.abspath(folder_path)
    print(f"Renaming items in {folder_path}")
    return folder_path


print(f"Rename program started")
folder_path = get_folder_path()
filenames = read_filenames(folder_path)
renames = determine_renames(folder_path, filenames)
validate_renames(renames)
applied_renames = apply_renames(renames)
save_rename_history(folder_path, applied_renames)
print(f"Done")
