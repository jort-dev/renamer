#!/usr/bin/env python3
import argparse
import shutil

import webview
import os
from natsort import natsorted

parser = argparse.ArgumentParser(
    prog="Undo renames",
    description="Undo renaming done by the renamer tool",
    epilog="Created by Jort: github.com/jort-dev")
parser.add_argument("-t", "--test",
                    help="disables the actual moving of files",
                    action="store_true",
                    )
parser.add_argument("-v", "--verbose",
                    help="prints more messages about the process",
                    action="store_true",
                    )
parser.add_argument("-d", "--depth",
                    help="the depth of the folders to use. default is 0, just the files in the selected folders,"
                         " 1 is to undo the renaming of only the files within the folders of the selected folders, etc",
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


def get_last_history_file_path(folder_path):
    printt(f"Reading filenames from {folder_path}")
    filenames = []
    for filename in os.listdir(folder_path):
        if not (filename.startswith(".rename_history_") and filename.endswith(".txt")):
            continue
        filenames.append(filename)

    if len(filenames) == 0:
        quit(f"No history file found in {folder_path}")
    filenames = natsorted(filenames, key=lambda y: y.lower())  # sort items same as the file manager does
    last_history_file = filenames[-1]
    print(f"Using history file: {last_history_file}")
    history_file_path = os.path.join(folder_path, last_history_file)
    return history_file_path


def parse_history_file(history_file_path):
    with open(history_file_path) as file:
        lines = file.readlines()

    renames = []
    for line in lines:
        line = line.strip()
        rename = line.split("/")
        renames.append(rename)
    return renames


def undo_renames(folder_path, renames, history_file_path):
    folder_rename = renames[0]
    renamed_from_folder_named = folder_rename[0]
    renamed_to_folder_name = folder_rename[1]
    parent_folder_path = folder_path[:-len(renamed_to_folder_name)]
    old_folder_path = os.path.join(parent_folder_path, renamed_from_folder_named)

    printt(f"Undoing renames in {renamed_to_folder_name}")
    for rename in renames[1:]:
        from_file_path = os.path.join(folder_path, rename[1])
        to_file_path = os.path.join(folder_path, rename[0])
        if not args.test:
            shutil.move(from_file_path, to_file_path)

    printt(f"Deleting history file {history_file_path}")
    os.remove(history_file_path)
    if renamed_from_folder_named != renamed_to_folder_name:
        if not args.test:
            shutil.move(folder_path, old_folder_path)


def get_folder_paths():
    if not args.folder_paths or len(args.folder_paths) == 0:
        printt("No folders supplied as argument, launching folder picker")
        folder_paths = ask_folders()
        if not folder_paths:
            quit("You picked an invalid folder")

    else:
        folder_paths = args.folder_paths

    for folder_path in folder_paths:
        if not folder_path or not os.path.isdir(folder_path):
            quit("You picked an invalid folder")

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

    print(f"Undoing renaming items in folders: {folder_paths}")
    return folder_paths


print(f"Renaming undo program started")
folder_paths = get_folder_paths()
for folder_path in folder_paths:
    history_file_path = get_last_history_file_path(folder_path)
    renames = parse_history_file(history_file_path)
    undo_renames(folder_path, renames, history_file_path)
