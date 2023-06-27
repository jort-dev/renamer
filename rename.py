# This function is called for EACH file. Return the new filename.
count = 0
def rename_file(filename, filename_base, filename_extension, file_path, folder_path, folder_name, file_index):
    global count
    count += 1
    return f"image{count}{filename_extension}"


# This function is called AFTER renaming ALL the files in ONE folder. Return the new folder name if you want it changed.
def rename_folder(folder_name, folder_path, parent_folder_name):
    return folder_name


"""
^^^^^^^^^^^^^^DOCUMENTATION / EXPLANATION for above functions^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The passed parameters are there for your convenience, and can be ignored.
Each function expects the new name to be returned. Return the same name to skip renaming.

def rename_file(filename, filename_base, filename_extension, file_path, folder_path, folder_name):
    This function gets called for all the files in one of your selected folders.
    Say you have selected one folder, C:/Pictures/family, containing three files: mama.jpg, papa.jpg, jort.jpg
    The first call to this function would be to rename the mama.jpg file. The parameters will be this:
        filename = mama.jpg
        filename_base = mama
        filename_extension = .jpg
        file_path = C:/Pictures/family/mama.jpg
        folder_path = C:/Pictures/family
        folder_name = family
        file_index = 0
    You return the new filename, for example family__mama.jpg. In the function you put: 
        return f"{folder_name}_{filename}
    Return the filename itself to not rename anything.
    The function is then called for the papa.jpg and jort.jpg file.
    After calling the rename_file function for all files in a folder, the rename_folder() function gets called:
    
def rename_folder(folder_name, folder_path, parent_folder_path):
    This function gets called after renaming all the files in one folder.
    Say the program just called the rename_file() function all the files in the C:/Pictures/family folder. 
    Then parameters will be this:
        folder_name = family
        folder_path = C:/Pictures/family
        parent_folder_name = Pictures
    You return the new filename, for example my_family. In the function you put:
        return f"my_{folder_name}"
    Return the folder name itself to not rename anything.
    

^^^^^^^^^^^^^^EXAMPLES^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Make the folder name the amount of files in each folder, put a number in front of all the files:
count = 0
def rename_file(filename, filename_base, filename_extension, file_path, folder_path, folder_name, file_index):
    global count
    count += 1
    return f"{count}_{filename}"


def rename_folder(folder_name, folder_path, parent_folder_name):
    global count
    new_folder_name = f"{folder_name}_{count}"
    count = 0
    return new_folder_name
    
    
For more examples, see the examples folder.
    
"""
