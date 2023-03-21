import webview
import os
import natsort
from natsort import natsorted

debug = True  # enable more printed messages, disables the actual renaming of files


def printt(*args, **kwargs):
    if debug:
        to_print = " ".join(map(str, args))
        print(to_print, **kwargs)

def ask_folder():
    dir_path = None

    def open_file_dialog(w):
        nonlocal dir_path
        try:
            dir_path = w.create_file_dialog(webview.FOLDER_DIALOG, directory=os.getcwd())[0]
        except TypeError:
            pass  # user exited file dialog without picking
        finally:
            w.destroy()

    window = webview.create_window("", hidden=True)
    webview.start(open_file_dialog, window)
    return dir_path


def get_last_history_file(folder_path):
    printt(f"Reading filenames from {folder_path}")
    filenames = []
    for filename in os.listdir(folder_path):
        if not (filename.startswith("rename_history_") and filename.endswith(".txt")):
            continue
        filenames.append(filename)

    if len(filenames) == 0:
        quit(f"No history file found in {folder_path}")
    filenames = natsorted(filenames, key=lambda y: y.lower())  # sort items same as the file manager does
    latest_history_file = filenames[-1]
    print(f"Using history file: {latest_history_file}")
    return latest_history_file


print(f"Renaming undo program started")
folder_path = ask_folder()
