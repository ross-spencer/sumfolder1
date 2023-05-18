"""Identify contents of folders and sub-folders and output hashes for
what we discover.
"""

import logging
import os
from pathlib import PureWindowsPath
from typing import Final, Union

from colorama import Fore, Style
from colorama import init as colorama_init

from .droidcsvhandler import DROIDCSVHandler
from .results import HashResult, QueryResult
from .storageobjects import File, Folder
from .utilities import _get_hash_obj, _sort_obj_list

colorama_init()

LOGFORMAT = (
    "%(asctime)-15s %(levelname)s: %(filename)s:%(lineno)s:%(funcName)s(): %(message)s"
)
DATEFORMAT = "%Y-%m-%d %H:%M:%S"

logging.addLevelName(
    logging.WARNING,
    f"{Fore.MAGENTA}{logging.getLevelName(logging.WARNING)}{Style.RESET_ALL}",
)
logging.addLevelName(
    logging.ERROR, f"{Fore.RED}{logging.getLevelName(logging.ERROR)}{Style.RESET_ALL}"
)
logging.addLevelName(
    logging.INFO, f"{Fore.GREEN}{logging.getLevelName(logging.INFO)}{Style.RESET_ALL}"
)

logging.basicConfig(format=LOGFORMAT, datefmt=DATEFORMAT, level="INFO")


class FolderException(Exception):
    """Exception to raise when there is a problem processing the given
    structures and folders.
    """


class MatchException(Exception):
    """Exception that indicates something isn't part of a given set."""


class SumFolders:
    """Encapsulates data structures and other functionality required to
    create our Merkle/Radix/Patricia tree enabling folder verification
    using cryptographic techniques.
    """

    TYPE_FOLDER: Final[str] = "Directory"
    TYPE_FILE: Final[str] = "File"

    def __init__(self, hash_func: str = "md5"):
        """SumFolders constructor."""

        self.hash_func = hash_func

        # Icons used to generate visual tree representation.
        self.folder_icon = "📁"
        self.file_icon = "📄"
        if os.name == "nt":
            self.folder_icon = "□"
            self.file_icon = "◌"

        # Flag that indicates whether or not we want to create a Root
        # Node (Rn) of if one is already available and we don't need to.
        self.given_root = False

        # Root Node (Path) that contains information about the Root
        # Node.
        self.root_folder = None

        # Variables to hold computed folders and files information.
        self.folders = None
        self.files = None

        # Functionality in this class depends on the merkle tree being
        # generated. Provide a defensive option that makes this clear
        # to the caller.
        self.merkle_generated = False

        # Used in tests to prove the consistency of results.
        self.root_folder_hash = None

    @staticmethod
    def _add_folder(folders: list[Folder], path: str) -> Folder:
        # Given a path, match an existing folder to it. If there isn't
        # a match, raise a FolderException as there isn't a lot more
        # that we can do here.
        for folder in folders:
            if path == folder.path:
                return folder
        raise FolderException("Containing folder hasn't been created")

    @staticmethod
    def _create_root(min_depth: int) -> Folder:
        """Create a root folder for this collection."""
        root = Folder()
        root.depth = min_depth - 1
        root.is_root = True
        root.path = PureWindowsPath("/merkle_collection_root")
        return root

    def generate_lists(
        self, droid_list: list[dict], csv_hash: str, make_root_node: bool = False
    ) -> Union[list[Folder], list[File]]:
        """Extract information about our folders and files and some of
        their relationships.
        """
        folders = []
        files = []
        min_depth = 1000
        override_root = False

        for idx, row in enumerate(droid_list, 1):
            path = PureWindowsPath(row["FILE_PATH"])
            type_ = row["TYPE"]
            hash_ = row[csv_hash]
            root = False
            # A root node (Rn) that sits above all other folders and
            # files needs to exist to provide a collection hash. This
            # ideally comes from the report and is identified currently
            # as row 1 or 2 without a parent_id. If it doesn't exist we
            # create an artificial Rn to capture the set's overall hash.
            if idx == 1 and not make_root_node:
                # DROID seems to output rows 1 or 2 as the first row ID
                # these days. This maybe a bug in DROID, but it's not
                # super important. The best version of this that we've
                # hit upon is to act when parent is empty and it's of
                # type folder.
                if row["PARENT_ID"] == "" and type_ == "Folder":
                    root = True
                    self.given_root = True
            if type_ == "Folder":
                folder = Folder()
                folder.path = path
                folder.is_root = root
                folder.depth = len(path.parts)
                min_depth = min(folder.depth, min_depth)
                folders.append(folder)
            elif type_ in ("File", "Container"):
                file = File()
                file.path = path
                file.name = path.name
                file.hash_ = hash_
                try:
                    file.parent = self._add_folder(folders, path.parent)
                except FolderException:
                    pass
                files.append(file)
            else:
                raise ValueError(f"Unexpected type in report: {type_}")
        if self.given_root is False and not override_root:
            root = self._create_root(min_depth)
            folders.insert(0, root)
        files = _sort_obj_list(files, "hash_", False)
        return folders, files

    @staticmethod
    def add_to_subs(needle: Folder, haystack: list[Folder]) -> None:
        """Add directory to subs."""
        for folder in haystack:
            if not str(needle.path).startswith(str(folder.path)):
                continue
            if needle.depth - folder.depth == 1:
                folder.sub_dirs.append(needle)

    @staticmethod
    def add_file(file: File, folders: list[Folder]) -> None:
        """Add file to directories."""
        for folder in folders:
            try:
                if file.parent.path == folder.path:
                    folder.files.append(file)
                    break
            except AttributeError:
                folders[0].files.append(file)
                break

    def create_relationships(
        self, folders: list[Folder], files: list[File]
    ) -> list[Folder]:
        """Create the relationships in the tree."""
        sorted_folders = _sort_obj_list(folders, "depth", False)
        root_dir = None
        for idx, folder in enumerate(sorted_folders):
            if idx == 0 and folder.is_root is not True:
                pass
                # need to create a "collection folder"
                # raise ValueError("Root should be our first directory but it is not")
            if idx == 0:
                root_dir = folder
                continue
            if folder.depth - root_dir.depth == 1:
                root_dir.sub_dirs.append(folder)
                continue
            self.add_to_subs(folder, folders[1:])
        for file in files:
            self.add_file(file, folders)
        assert folders[0].is_root
        # Ensure that files at Rn+1 have root as their parent.
        for file in folders[0].files:
            file.parent = folders[0]
        return folders

    def _print_tree_files(self, files: list[File], padding: str) -> str:
        """Print files out in the tree."""
        file_str = ""
        for file in files:
            color_hash = f"{Fore.YELLOW}{file.hash_}{Style.RESET_ALL}"
            file_str = f"{file_str}{padding}   {self.file_icon} {file.path.name} {color_hash}\n"
            file.displayed = True
        return file_str

    def generate_tree(
        self,
        folders: list[Folder],
        _tree: str = "",
        root_dir_depth: int = 0,
        print_files: bool = True,
    ) -> None:
        """Create a visual representation of the given DROID report."""
        if not self.merkle_generated:
            raise FolderException(
                "Merkle tree needs to be generated before calling generate_tree(...)"
            )
        sorted_folders = _sort_obj_list(folders, "depth", False)
        space = ""
        for idx, folder in enumerate(sorted_folders):
            if idx == 0 and root_dir_depth == 0:
                root_dir_depth = folder.depth
            space = " " * ((folder.depth - root_dir_depth) * 3)
            if not folder.displayed:
                color_hash = f"{Fore.GREEN}{folder.hash_[:]}{Style.RESET_ALL}"
                _tree = f"{_tree}{space}{self.folder_icon} {folder.path.name} {color_hash}\n"
                if print_files:
                    file_str = self._print_tree_files(folder.files, space)
                    _tree = f"{_tree}{file_str}"
                folder.displayed = True
            if folder.sub_dirs:
                _tree = self.generate_tree(
                    folder.sub_dirs, _tree=_tree, root_dir_depth=root_dir_depth
                )
        return _tree

    def generate_merkle(self, folders: list[Folder]) -> None:
        """Create a merkle tree from the given DROID report."""
        sorted_folders = _sort_obj_list(folders, "depth", True)
        root = None
        for idx, folder in enumerate(sorted_folders):
            if len(sorted_folders) == 1:
                # We only have one folder so it has to be root so we
                # don't have to work anything else out.
                root = sorted_folders[0]
            elif idx == 0 and folder.is_root is True:
                raise ValueError("Root should not be the first element in this list")
            if folder.is_root:
                root = folder
            folder.hash_folders(self.hash_func)
        self.root_folder_hash = root.hash_
        self.merkle_generated = True

    def _check_folder(self, hash_: str, folders: list[Folder]) -> list[Folder]:
        """Given a hash to check against, find a list of folders that
        match that hash. Alternatively if there is no match return an
        exception for the caller to handle.
        """
        folder_matches = [folder for folder in folders if folder.hash_ == hash_]
        try:
            _ = folder_matches[0]
        except IndexError as err:
            raise MatchException("Folder not matched") from err
        if len(folder_matches) > 1:
            logging.info(
                "Folder with hash %s is a duplicate entry and appears multiple times in the tree"
            )
        matches = []
        for folder in folder_matches:
            folder.hash_folders(self.hash_func)
            assert hash_ == folder.hash_, "recalculation of folder hash failed"
            name = folder.path.name
            path = folder
            matches.append({"name": name, "path": path})
        logging.info("Folder: %s %s", path.depth, hash_)
        return matches

    def _check_files(self, hash_: str, files: list[File]) -> list[File]:
        """Given a hash to check against, find a list of files that
        match that hash. Alternatively if there is no match return an
        exception for the caller to handle.
        """
        file_matches = [file for file in files if file.hash_ == hash_]
        try:
            _ = file_matches[0]
        except IndexError as err:
            raise MatchException("File not matched") from err
        matches = []
        for file in file_matches:
            folder_hash = file.parent.hash_
            file.parent.hash_folders(self.hash_func)
            assert (
                folder_hash == file.parent.hash_
            ), "recalculation of parent should be identical"
            name = file.name
            path = file.parent
            matches.append({"name": name, "path": path})
        return matches

    def get_active_tree(self, container: Folder, folders: list[Folder]) -> list[Folder]:
        """Retrieve the anticipated active-tree for the search hash. I.e.
        all folder hashes from search hash up to root node (Rn.
        """
        tmp_active_tree = []
        tmp_active_tree.append(container)
        for folder in folders:
            subs = [sub_dir.hash_ for sub_dir in folder.sub_dirs]
            sub_depth = False
            for sub_dir in folder.sub_dirs:
                if container.depth != sub_dir.depth:
                    # If we have matched at the wrong depth then we are
                    # matching a false-positive. At the very least we
                    # need a match at depth. Given the need for more
                    # data, we will also need to match on name, but there
                    # is no additional value in that currently.
                    continue
                sub_depth = True
            if container.hash_ in subs and sub_depth is True:
                tmp_active_tree.append(folder)
                container = folder
        active_tree = []
        for folder in tmp_active_tree:
            # Recalculate the hashes by way of affirming their correctness.
            folder.hash_folders(self.hash_func)
            active_tree.append(folder)
        return active_tree

    def verify_hash(
        self, hash_: str, folders: list[Folder], files: list[File]
    ) -> QueryResult:
        """Verify a hash's existence, or non-existence against a
        dataset.

        Process:

            * Walk tree back from container dir. ✔️
            * Find all containing folders and recalculate (H1). ✔️
            * Find Rn+1 (folders directly before Rn) (H2). ✔️
            * Look for crossover between H1 and H2. ✔️
            * Sum all at Rn+1 (including files). ✔️
            * Report set of all folders discovered (H1). ✔️

        FIXME: R0912: Too many branches (15/12) (too-many-branches)
        FIXME: R0915: Too many statements (71/50) (too-many-statements)
        """
        is_root = False
        if hash_ == self.root_folder_hash:
            is_root = True
        search_hash = hash_
        logging.info("Looking for: %s", search_hash)
        folder = None
        is_file = True
        query_result = QueryResult()
        query_result.search_hash = search_hash
        try:
            matches = self._check_folder(hash_, folders)
            is_file = False
        except MatchException:
            try:
                matches = self._check_files(hash_, files)
            except MatchException:
                return query_result
        type_ = self.TYPE_FILE
        if not is_file:
            type_ = self.TYPE_FOLDER
        query_result.found = True
        query_result.type_: str = type_
        for match_ex in matches:
            folders = _sort_obj_list(folders, "depth", False)
            match = match_ex["path"]
            hash_result = HashResult()
            hash_result.name = match_ex["name"]
            if type_ == self.TYPE_FILE:
                hash_result.parent_folder = match
                hash_result.parent_folder_name = match.path.name
            logging.info("Container hash: %s, type: (%s)", match.hash_, type_)
            if not folders[0].is_root:
                raise FolderException("Expecting root as first in set")
            if is_root:
                root_hash = folders[0].hash_folders(self.hash_func)
                assert root_hash == self.root_folder_hash
                query_result.found = True
                query_result.is_root = True
                return query_result
            root_group = folders[0].depth
            root_files = [file.hash_ for file in folders[0].files]
            logging.info("Root group: %s", root_group)
            logging.info("Root files %s", root_files)
            folders = _sort_obj_list(folders, "depth", True)
            folder_depths = []
            for folder in folders:
                if folder.depth == root_group:
                    continue
                folder_depths.append(folder.depth)
            require = min(folder_depths)
            logging.info("Rn+1 depth: %s (out of: %s)", require, folder_depths)
            # Root node hashes minus 1 (H1).
            rn_m1_hashes = [
                folder.hash_ for folder in folders if folder.depth == require
            ]
            # Sort checksums alphabetically so that they are consistently
            # added together, i.e. this ensures that they are added by content
            # and no additional data needs adding to the objects, e.g. such
            # as sort order in a previous version of this code.
            rn_m1_hashes.sort()
            # Active-tree (H2).
            active_tree_folders = self.get_active_tree(match, folders)
            active_tree_hashes = [folder.hash_ for folder in active_tree_folders]
            logging.info("Rn+1 hashes: %s", rn_m1_hashes)
            logging.info("Identified active-tree: %s", active_tree_hashes)
            if search_hash in root_files:
                digest = _get_hash_obj(self.hash_func)
                rn1 = rn_m1_hashes + root_files
                for item in rn1:
                    digest.update(item.encode())
                calculated = digest.hexdigest()
                if calculated != self.root_folder_hash:
                    raise FolderException(
                        f"Root hashes do not match: want: {self.root_folder_hash} have: {calculated}"
                    )
                for hashes in active_tree_hashes:
                    hash_result.containing_dirs.append(hashes)
                query_result.results.append(hash_result)
                continue
            # We have two sets of hashes. We have the hashes at Rn+1 (H1)
            # and we have the collection of hashes (re-calculated) from the
            # containing folder up the tree (H2).
            #
            # Given this, ensure that one folder in H2 exists in H1. This
            # tells us that we have the container's active-tree calculated
            # correctly.
            #
            # The intersection simply needs to be greater than one, to
            # show that there is overlap between the two sets.
            folders_intersection = set(active_tree_hashes).intersection(rn_m1_hashes)
            assert (
                len(folders_intersection) >= 1
            ), f"Intersection length: {len(folders_intersection)}"
            # Finally calculate the hashes at Rn+1 and ensure that they
            # match the previously calculated Rn.
            all_hashes = rn_m1_hashes + root_files
            logging.info("Recalculating with all hashes %s", all_hashes)
            final_compute = _get_hash_obj(self.hash_func)
            for hashes in all_hashes:
                final_compute.update(hashes.encode())
            final_computed = final_compute.hexdigest()
            assert (
                final_computed == self.root_folder_hash
            ), f"final_computed: ({final_computed}) doesn't equal expected: ({self.root_folder_hash})"
            assert self.root_folder_hash in active_tree_hashes
            try:
                active_tree_hashes.remove(search_hash)
            except ValueError:
                pass
            for hashes in active_tree_hashes:
                hash_result.containing_dirs.append(hashes)
            query_result.results.append(hash_result)
        return query_result

    def sum_folders(
        self, droid_csv: str, make_root_node: bool = False, as_str: bool = False
    ):
        """The primary function of the SumFolders Class is to generate
        a Merkle/Radix tree of the information in a DROID report and
        generate hashes for folders which do not inherently have them.
        This is all done here...
        """
        droidcsv = DROIDCSVHandler()
        if as_str:
            droid_list = droidcsv.read_droid_csv_from_string(droid_csv)
        else:
            droid_list = droidcsv.read_droid_csv_from_file(droid_csv)
        folders, files = self.generate_lists(droid_list, droidcsv.hash, make_root_node)
        folders = self.create_relationships(folders, files)
        self.generate_merkle(folders)
        self.folders = folders
        self.files = files
