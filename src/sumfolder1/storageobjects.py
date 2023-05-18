"""Storage objects associated with sumfolder1."""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final

from .utilities import _get_hash_obj, _sort_obj_list


@dataclass
class Folder:
    """Folder class."""

    path: Path = None
    is_root: bool = False
    depth: int = None
    sub_dirs: list = field(default_factory=list)
    files: list = field(default_factory=list)
    hash_of_files: str = None
    hash_: str = None

    # Non-functional, tree-view helper.
    displayed: bool = False

    EMPTY_DIR: Final[str] = b"2600_EMPTY_DIRECTORY"  # pylint: disable=C0103

    def __repr__(self):
        """Create a string representation of this object."""
        try:
            return f"{self.path.name} ({self.hash_[:6]})"
        except TypeError:
            # Hash may not yet be available when this is called.
            return f"{self.path.name}"

    def hash_files(self, hash_func):
        """Calculate a single hash for files."""
        digest = _get_hash_obj(hash_func)
        if not self.files:
            self.hash_of_files = digest.hexdigest()
            return
        for file in self.files:
            digest.update(file.hash_.encode())
        self.hash_of_files = digest.hexdigest()

    def _hash_empty_directory(self, digest):
        """Return a hash for a completely empty directory."""
        digest.update(self.EMPTY_DIR)
        self.hash_ = digest.hexdigest()

    @staticmethod
    def _sort_directories(folders):
        """Sort directories by their hash values providing they have
        been calculated.

        NB. Hashes are a natural value to sort here. Previously a
        mechanic existed to generate a sort order, but this makes the
        heuristic less portable. Sorting by hash values (once
        calculated) makes this utility truly content based.
        """
        return _sort_obj_list(folders, "hash_", False)

    def hash_folders(self, hash_func) -> str:
        """Generate a single hash for folders."""
        digest = None
        digest = _get_hash_obj(hash_func)
        if not self.sub_dirs and not self.files:
            # There are no sub directories and no files. We have a
            # totally empty directory so return a hash for an empty
            # directory.
            self._hash_empty_directory(digest)
            return self.hash_
        hashes = []

        if not self.sub_dirs and self.hash_of_files:
            # We have an already calculated hash-set, we don't need to
            # do the work again.
            self.hash_ = self.hash_of_files
            return self.hash_

        # Otherwise, calculate everything in the directory again...
        #
        # Directories need to be sorted predictably to recalculate the
        # tree.
        sub_dirs = self._sort_directories(self.sub_dirs)

        for folder in sub_dirs:
            hashes.append(folder.hash_)
        for file in self.files:
            hashes.append(file.hash_)
        if self.is_root:
            logging.info("Root is calculated with: %s", hashes)
        for hash_ in hashes:
            digest.update(hash_.encode("utf-8"))
        self.hash_ = digest.hexdigest()
        return self.hash_


@dataclass
class File:
    """File class"""

    path: Path = None
    name: str = None
    parent: Folder = None
    hash_: str = None

    # Non-functional, tree-view helper.
    displayed: bool = False

    def __repr__(self):
        """Create a string representation of this object."""
        try:
            return f"{self.path.name} ({self.hash_[:6]})"
        except (TypeError, AttributeError):
            # Attributes may not be initialized when this is called.
            return f"{self.path.name}"
