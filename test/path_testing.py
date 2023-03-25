import os

folder_path = os.getcwd()


def get_parent_folder_name(folder_path):
    return os.path.basename(folder_path[:-len(os.path.basename(folder_path)) - 1])  # -1 to remove the trailing /


print(folder_path)
print(get_parent_folder_name(folder_path))
