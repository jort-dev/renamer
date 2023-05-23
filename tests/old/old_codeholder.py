from PIL import Image
from PIL.ExifTags import TAGS


def get_exif_value_from_image(tag_key, image_path=None, image=None):
    if image_path:
        image = Image.open(image_path)
    if not image:
        print(f"No image supplied to find tag '{tag_key}' in")
        return

    exif_dict = {
        "filename": image.filename,
        "size": image.size,
        "height": image.height,
        "width": image.width,
        "format": image.format,
        "mode": image.mode,
        "animated": getattr(image, "is_animated", False),
        "frames": getattr(image, "n_frames", 1)
    }
    exif_data = image.getexif()
    for tag_id in exif_data:
        tag = TAGS.get(tag_id, tag_id)
        data = exif_data.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        exif_dict[tag] = data
    if tag_key not in exif_dict:
        print(f"Tag '{tag_key}' not found following metadata:")
        for tag in exif_dict:
            print(f"{tag:25}: {exif_dict[tag]}")
        print(f"Tag '{tag_key}' not found in above metadata.")
        return
    return exif_dict[tag_key]
