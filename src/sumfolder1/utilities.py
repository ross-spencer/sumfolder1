"""Convenience functions used across sumfolder1."""

import hashlib
import operator


def _sort_obj_list(list_: list, key: str, reverse: bool) -> list:
    """Sort the given list of objects by the given attribute."""
    return sorted(list_, key=operator.attrgetter(key), reverse=reverse)


def _get_hash_obj(hash_func="md5"):
    """Return a hash object to the caller."""
    hash_func = hash_func.lower()
    hash_objs = {
        "md5": hashlib.md5(),
        "sha256": hashlib.sha256(),
        "blake": hashlib.blake2b(),
    }
    return hash_objs.get(hash_func, hashlib.md5())
