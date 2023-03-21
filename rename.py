"""
this function gets called for each filename to rename, return the new filename here
say you have picked the folder /home/jort/Pictures
the script calls this function for each image in the folder, for example portrait2.jpg
then the parameters will be:
- folder_path: /home/jort/Pictures
- base: portrait
- extension: .jpg
and you could return for example:
- portrait2_renamed.jpg
"""
def rename(folder_path, base, extension):
    new_filename = f"{base}_renamed{extension}"
    return new_filename
