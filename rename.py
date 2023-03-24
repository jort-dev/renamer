count = 0


def rename_file(folder_path, filename, base, extension):
    global count
    count += 1
    return f"renamed_image_{count}{extension}"


def rename_folder(parent_folder_path, folder_name):
    global count
    new_folder_name = f"{folder_name}_{count}"
    count = 0
    return new_folder_name



"""
Documentation / examples:
this function gets called for each filename to rename, return the new filename here
say you have picked the folder /home/jort/Pictures
the script calls this function for each image in the folder, for example portrait2.jpg
then the parameters will be:
- folder_path: /home/jort/Pictures
- base: portrait
- extension: .jpg
and you could return for example:
- portrait2_renamed.jpg


Examples:
get the folder name
folder_name = folder_path.split("/")[-1]




Rename folder
gets called after all the files in that folder have been renamed, maybe you want to include the amount of files / timestamp range or whatever

"""
