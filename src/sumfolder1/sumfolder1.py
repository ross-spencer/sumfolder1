"""Calculate checksums for the folders in a collection of objects using
an existing DROID report.

The script uses the principle of merkle trees to generate hashes of
directories recursively using the sums of the hashes of file objects
that are inside the given folders.

A Root node (Rn) hash is generated which encapsulates an entire
collection.

Different questions around the existence, or inclusion of files or
directories can be asked of a set once the initial tree is calculated.
"""

import argparse
import json
import logging
import sys
from typing import Final

from .referenceset import reference_set
from .sumfolders import SumFolders
from .version import _version

HASH_MD5: Final[str] = "md5"


def _print_version():
    """Print version information to stdout."""
    print(f"sumfolder1-v{_version}")
    sys.exit()


def _reference_set():
    """Return reference set CSV to stdout."""
    print(reference_set())
    sys.exit(0)


def _run_demo():
    """Create some demo output based on the reference set."""

    logging.info("Running a demo against the reference set...")
    sum_folders = SumFolders(HASH_MD5)
    sum_folders.sum_folders(reference_set(), as_str=True)

    folders = sum_folders.folders
    files = sum_folders.files

    tree = sum_folders.generate_tree(sum_folders.folders)

    demo = {}

    empty_file = "d41d8cd98f00b204e9800998ecf8427e"
    res = sum_folders.verify_hash(empty_file, folders, files)
    note = f"Empty file: '{empty_file}' appears twice in tree..."

    demo[empty_file] = {}
    demo[empty_file]["note"] = note
    demo[empty_file]["res"] = res.as_dict()

    empty_dir = "1ccb49edc4e873f1a8affd4bad5e9b90"
    res = sum_folders.verify_hash(empty_dir, folders, files)
    note = f"Empty dir: '{empty_dir}' appears twice in tree..."

    demo[empty_dir] = {}
    demo[empty_dir]["note"] = note
    demo[empty_dir]["res"] = res.as_dict()

    file_exists = "637a3fb7da1ab61d10e96336d9758416"
    res = sum_folders.verify_hash(file_exists, folders, files)
    note = f"Lone file: '{file_exists}' appears once in tree..."

    demo[file_exists] = {}
    demo[file_exists]["note"] = note
    demo[file_exists]["res"] = res.as_dict()

    file_doesnt_exist = "12345fb7da1ab61d10e96336d9758416"
    res = sum_folders.verify_hash(file_doesnt_exist, folders, files)
    note = f"Non-existent file: '{file_doesnt_exist}' appears zero times in tree..."

    demo[file_doesnt_exist] = {}
    demo[file_doesnt_exist]["note"] = note
    demo[file_doesnt_exist]["res"] = res.as_dict()

    root = "52b94608dc70813aa88dae01176dc73b"
    res = sum_folders.verify_hash(root, folders, files)
    note = f"Root is: '{root}'..."

    demo[root] = {}
    demo[root]["note"] = note
    demo[root]["res"] = res.as_dict()

    print(json.dumps(demo, indent=2))
    print("\n==== DEMO TREE OUTPUT TO STDERR ==\n", file=sys.stderr)
    print(tree, file=sys.stderr)


def main():
    """Primary entry point for the sumfolder1 module."""

    parser = argparse.ArgumentParser(
        description="Calculate checksums for folders in a collection of "
        "objects using a DROID format identification report"
    )
    parser.add_argument(
        "--csv", help="Single DROID CSV to read.", default=False, required=False
    )
    parser.add_argument(
        "--demo",
        help="Run demo queries and output a tree to demo.txt",
        default=False,
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "--ref",
        "--reference",
        help="Write reference set to stdout.",
        default=False,
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Return version information.",
        default=False,
        required=False,
        action="store_true",
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if args.version:
        _print_version()
    if not args.csv and not args.ref and not args.demo:
        parser.print_help()
        sys.exit(1)
    if args.ref:
        _reference_set()

    if args.csv:
        # MD5 default, but we can override this in future.
        sum_folders = SumFolders(HASH_MD5)
        sum_folders.sum_folders(args.csv)
        print(sum_folders.generate_tree(sum_folders.folders))

    if args.demo and not args.csv:
        _run_demo()
    elif args.demo:
        print("Demo should be called as a standalone argument", file=sys.stderr)


if __name__ == "__main__":
    main()
