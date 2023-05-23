"""
Get exifdata from files.
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
        for exif_key in exif_dict:
            for key in keys:
                if key in exif_key:
                    return exif_dict[exif_key]

        print(f"Metadata not found for {keys}")
        for exif_key, exif_value in exif_dict.items():
            print(f"{exif_key:50} : {exif_value}")
        print(f"Metadata not found for {keys}")


folder_path = "/home/jort/Pictures/rename_test"
for item_name in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item_name)
    if not os.path.isfile(item_path):
        continue
    value = get_exif_value(item_path, "Model")
    print(f"{item_name:40} Model: {value}")
