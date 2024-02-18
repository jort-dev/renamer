import os
import re

try:
    from natsort import os_sorted

    NATSORT_AVAILABLE = True
except ImportError:
    NATSORT_AVAILABLE = False


def natural_sort_key(s):
    """A custom natural sort key function for fallback sorting."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]


def sort_items(items):
    """Sort items using natsort if available, otherwise use a custom method."""
    if NATSORT_AVAILABLE:
        return os_sorted(items)
    else:
        return sorted(items, key=natural_sort_key)


# Specify the directory
directory = 'C:\\Users\\Jort\\Downloads'

# List all files and directories in the specified directory
items = os.listdir(directory)

# Sort the list of files and directories
sorted_items = sort_items(items)

# Print the sorted list of files and directories
for item in sorted_items:
    print(item)
