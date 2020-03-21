import logging
import hashlib

log = logging.getLogger(__name__)

timestamp_format = "%Y-%m-%dT%H:%M:%SZ"


def sanitize(text):
    return str(text).lower().replace(" ", "-")


def calc_md5(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def remove_nones_from_string(string: str):
    if "None, " in string:
        string = string.replace("None, ", "")
    if ", None" in string:
        string = string.replace(", None", "")
    elif "None " in string:
        string = string.replace("None ", "")
    elif "None" in string:
        string = string.replace("None", "")
    return string


def remove_nones_from_list(list: list):
    return [x for x in list if x is not None]


def ensure_list_have_same_length(list1, list2, mode="cut beginning"):
    if mode == "cut beginning":
        diff = len(list1) - len(list2)
        if diff < 0:
            list2 = list2[abs(diff):]
        elif diff > 0:
            list1 = list1[diff:]
    return list1, list2
