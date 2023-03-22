import shutil

import webview
import os
from natsort import natsorted

debug = True  # enable more printed messages, disables the actual renaming of files
test = True  # enable test folder


def printt(*args, **kwargs):
    if debug:
        to_print = " ".join(map(str, args))
        print(to_print, **kwargs)


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


def get_last_history_file_path(folder_path):
    printt(f"Reading filenames from {folder_path}")
    filenames = []
    for filename in os.listdir(folder_path):
        if not (filename.startswith("rename_history_") and filename.endswith(".txt")):
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


def undo_renames(folder_path, renames):
    for rename in renames:
        from_file_path = os.path.join(folder_path, rename[1])
        to_file_path = os.path.join(folder_path, rename[0])
        shutil.move(from_file_path, to_file_path)

def delete_history_file(history_file_path):
    printt(f"Deleting history file {history_file_path}")
    os.remove(history_file_path)


print(f"Renaming undo program started")
folder_path = ask_folder()
history_file_path = get_last_history_file_path(folder_path)
renames = parse_history_file(history_file_path)
undo_renames(folder_path, renames)
delete_history_file(history_file_path)
