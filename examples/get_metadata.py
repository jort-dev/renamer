"""
Get exifdata from files, like the used phone or a creation timestamp.
"""
import os

from exiftool import ExifToolHelper


def get_exif_value(path, *keys):
    """
    *keys:
    Check all the exif data of the item, if the exif key contains one of the *keys, return the value.
    Useful if you want get the camera model for videos and photos:
    For photos the camera model is stored in EXIF:Model
    For videos the camera model is stored in XML:DeviceModelName
    so as the *keys argument, you can either pass:
    "EXIF:Model", "XML:DeviceModelName"
    or
    "Model"
    As both keys contain "Model"
    """
    for exif_dict in ExifToolHelper().get_metadata(path):
        for key in keys:  # iterate keys first, so that first listed keys are grabbed first
            for exif_key in exif_dict:
                if key in exif_key:
                    return exif_dict[exif_key]

        for exif_key, exif_value in exif_dict.items():
            print(f"{exif_key:50} : {exif_value}")
        print(f"In above metadata, no key containing {keys} was found for {path}")


folder_path = "/home/jort/Pictures/rename_test"
for item_name in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item_name)
    if not os.path.isfile(item_path):
        continue
    model = get_exif_value(item_path, "Model")
    timestamp = get_exif_value(item_path, "CDate")
    timestamp = timestamp.replace(":", "").replace(" ", "_")
    print(f"{item_name:40} Model: {model:20} Creation: {timestamp}")

"""
Example:
I used the following code to show the used camera and timestamp for a set of mixed photos.
from exiftool import ExifToolHelper
def rename_file(filename, filename_base, filename_extension, file_path, folder_path, folder_name, file_index):
    if "PXL" in filename: # my pixel does not have a model number with videos
        model = "Pixel 7"
    elif "000" in filename: # same for my camera
        model = "DSC-RX100M5"
    else:
        model = get_exif_value(file_path, "Model")

    timestamp = get_exif_value(file_path, "CreateDate", "Date")  # "Date" is the fallback, it matches a lot
    timestamp = timestamp.replace(":", "").replace(" ", "_")
    if model == "DSC-RX100M5":
        model = "jort_cam"
    elif model == "Pixel 7":
        model = "jort_phone"
    elif model == "OnePlus":
        model = "others_phone"
    return f"{timestamp}_{model}_item{file_index}{filename_extension.lower()}"
"""