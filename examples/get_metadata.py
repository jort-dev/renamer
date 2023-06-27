"""
Get exifdata from files, like the used phone or a creation timestamp.
"""
import os
from datetime import datetime

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


def ms_to_timestamp(ms):
    return datetime.fromtimestamp(ms / 1000.0)


def mtime_stamp(file_path):
    timestamp = os.path.getmtime(file_path)
    timestamp = datetime.fromtimestamp(timestamp)
    return timestamp.strftime("%Y%m%d_%H%M%S")


def get_timestamp(file_path):
    # returns the first timestamp found in the metadata, otherwise the file modification date
    # returns: YYYYMMDD_HHMMSS
    try:
        timestamp = get_exif_value(file_path, "CreateDate", "Date")  # "Date" is the fallback, it matches a lot
        timestamp = timestamp.replace(":", "").replace(" ", "_")
        timestamp = timestamp.split("+", 1)[0]  # remove timezone stuff if its there
        if "0000" in timestamp:
            timestamp = mtime_stamp(file_path)
        return timestamp
    except:
        return mtime_stamp(file_path)


"""
Example:
I used the following code to show the used camera and timestamp for a set of mixed photos.

from examples.get_metadata import *
# This function is called for EACH file. Return the new filename.
def rename_file(filename, filename_base, filename_extension, file_path, folder_path, folder_name, file_index):
    if "PXL" in filename:
        model = "pixel"
    elif "IMG" in filename:
        model = "iphone"
    elif "00" in filename or "DSC" in filename:
        model = "sony"
    else:
        model = "panasonic"

    try:
        timestamp = get_timestamp(file_path)
        new = f"{timestamp}_{model}{filename_extension}"
    except:
        new = f"IDK_{model}{filename_extension}"
    print(f"{filename} -> {new}")
    return new
"""
