<p align="center">
  <img
   width="786"
   height="204"
   alt="Logo for sumfolder1"
   src="https://raw.githubusercontent.com/ross-spencer/sumfolder1/main/logo/sumfolder1.png">
</p>

sumfolder1 is a utility for use within the archival and digital preservation
community to generate checksums for file system directories, and to generate
an overall "collection" checksum for a given set of files.

* [Why?](#why)
  * [Archival questions](#archival-questions)
  * [Structural questions](#structural-questions)
  * [Forensics questions](#forensics-questions)
* [How?](#how)
  * [Reference set](#reference-set)
  * [Reference implementation](#reference-implementation)
  * [Merkle trees](#merkle-trees)
  * [Terminology](#terminology)
  * [New folder attributes](#new-folder-attributes)
  * [Sensitivity](#sensitivity)
* [DROID](#droid)
  * [DROID in Siegfried](#droid-in-siegfried)
  * [DROID as an inspiration](#droid-as-an-inspiration)
  * [Writing about sumfolder1](#writing-about-sumfolder1)
* [Installation](#installation)
* [Usage](#usage)
  * [Demo output](#demo-output)
  * [Use with a DROID csv](#use-with-a-droid-csv)
  * [Outputting the reference CSV](#outputting-the-reference-csv)
* [License](#license)

## Why?

Conventionally, checksums exist for files, they do not exist for directories.
They have no payload that can be summed together to calculate a digest/checksum.

If it were possible to create checksums for folders or a global checksum for a
collection of objects, it would become possible to ask the following:

### Archival questions

* What is the collection checksum for a given set of files and folders?
* What is the checksum for a given folder?
* Given a collection of objects online, am I looking at an authentic listing?
* Have I downloaded a collection in its entirety?

### Structural questions

* Is file/folder hash(x) included in the collection set?
* Is file/folder hash(y) (non-existent) part of the entire set?
* Is file hash(x) part of folder(y) where the collection has arbitrary depth?
* Where are duplicate checksums located within a collection?

### Forensics questions

* Has a digital object been removed from the collection?
* Did the collection contain at least one empty directory?

## How?

Given a set of file paths and existing checksums it is possible to compute a
checksum for a folder by creating a checksum of the given checksums.

Given checksum 1) `7c1f9f9a4d0ce9a72ee63f37a1b7f694` and checksum 2)
`aececec0bc3f515039aec9e60c413cd3` an MD5 can be computed as:
`82f9e9a4305714fffdd7932783980cbc`.

We can see this illustrated for a small collection as follows:

```text
📁 folder_1 82f9e9a4305714fffdd7932783980cbc
    📄 checksum_1 7c1f9f9a4d0ce9a72ee63f37a1b7f694
    📄 checksum_2 aececec0bc3f515039aec9e60c413cd3
```

If we follow this approach through an entire directory structure we can create
checksums for all sub-directories and for the collection as a whole.
### Reference set

A reference set is provided with this repository: [reference set](reference/collection.7z).

We can iterate through the directory tree to create sets of directory checksums
and a collection checksum: `52b94608dc70813aa88dae01176dc73b`.

The reference set then looks as follows:

```text
📁 collection 93778c524035d5d3e429a2fe43b7700a
   📄 file_0001 14118ff9ad0344decb37960809b2f17a
   📄 file_0000 8cfda2609b880a553759cd6200823f3b
   📄 file_0002 a4501ee1a5c711ea9db78a800a24e830
   📁 sub_dir_1 82301616d7e24f474dbe21de93af0a34
      📄 file_empty d41d8cd98f00b204e9800998ecf8427e
      📄 file_0003 dc7f828c5fe622925181d06edada350f
      📄 file_0004 e3d90a4bf14a9b355f0e69ba08df522d
      📁 sub_1_dir_1 1c7ba27edf1356d097a3f568032430c2
         📄 file_0005 637a3fb7da1ab61d10e96336d9758416
   📁 sub_dir_2 1ccb49edc4e873f1a8affd4bad5e9b90
   📁 sub_dir_3 2a60541cede91a36e9dc5bab7a97dd6e
      📁 sub_3_empty_1 db9d848b4f83ff3cb3faa4df0a59e3e1
         📁 sub_3_empty_2 1ccb49edc4e873f1a8affd4bad5e9b90
   📁 sub_dir_4 272d45767d534335163f220c1d40e559
      📄 file_0006 2b43227486ec8744cd5d4c955d269743
      📄 file_0007 c5a1973a70e08bf1eee13b8090f790ad
      📄 file_0008 fdffe4dd2d39c7d9986dbf5c6ec5ad39
   📁 sub_dir_5 d818d29b75f89a9b5d8d1c5a4c70dbbb
      📁 sub_5_dir_1 82f9e9a4305714fffdd7932783980cbc
         📄 file_0009 7c1f9f9a4d0ce9a72ee63f37a1b7f694
         📄 file_0010 aececec0bc3f515039aec9e60c413cd3
   📁 sub_dir_6 74be16979710d4c4e7c6647856088456
      📄 file_empty d41d8cd98f00b204e9800998ecf8427e

```

### Reference implementation

The reference implementation for sumfolder1 does the following:

From the lowest sub-directory in the tree:

1. Check for sub-directories and add the checksums for these to a hash digest in
alphabetical order by checksum.
1. For files in the directory add these to the hash digest in alphabetical order
by checksum.
1. Create a digest for the list of checksums.

Repeat, processing each folder backwards up to the top level.

> NB. If a folder is completely empty it is assigned a constant value
chosen in the code: `2600_EMPTY_DIRECTORY`. This evaluates to an MD5 value of
`1ccb49edc4e873f1a8affd4bad5e9b90`.

### Merkle trees

The concept I have used here is based on Merkle trees and a loose understanding
of techniques used in the block-chain and in the source control system GitHub.

A good video summary of Merkle trees can be found on YouTube:

* [Gaurav Sen on Merkle Trees][merkle-1]

And a Python tutorial I found useful in starting this work:

* [Dan Nolan on Merkle Trees][merkle-2]

The technique required for a directory tree is a little more convoluted than
that of a Merkle tree which uses binary nodes and evaluates checksums from left
to right. I believe the implementation used for sumfolder1 is more closely
aligned to that of a "Radix Tree" or "Patricia Tree", however, this is to be
explored more.

> NB. A merkle tree can be used in its context for performance; sumfolder1 does
not yet have a performance use-case.

### Terminology

The reference implementation introduces some terminology that helps with
understanding the approach:

* Active-tree: the side of a directory tree that we're querying about a given
hash.
* Non-active-tree: the tree at root node (Rn+1) that do not contain the digital
object that we're querying.
* Root-node (Rn): the name of the top-level node, i.e. collection folder. This
is either artificially created for a set of directories all at the same level,
or exists as a function of the given collection set.

### New folder attributes

Folder objects need to be given additional attributes to enable the algorithm
to work.

* Folder-depth, so directories can be grouped and distinguished from
one-another by level in the hierarchy.
* Hash, the goal of this tool is to enable a hash to be calculated for
an entire collection.

### Sensitivity

I am trying to make this code as portable as possible, i.e. while it works with
DROID-style reports today, it might also work with other checksum-based outputs
tomorrow. Additionally, to be able to compare folder structures, this utility
may also work with DROID-style reports later on in a transfer workflow; at which
point, folders and files may have been renamed, but their content remains
consistent.

To calculate a single folder checksum we currently do the following:

* If there are folders in the directory, order their hashes alphabetically
and add to a list.
* File checksums are then ordered alphabetically and added to the end of the
list.
* The checksums are then summed together to create a new folder-level checksum.

## DROID

sumfolder1 uses the DROID format identification report to generate folder level
checksums.

DROID can be found at The National Archives UK website:

* [DROID @ The National Archives][droid-1]

### DROID in Siegfried

sumfolder1 can also be used with DROID compatible reports created by Siegfried
using a command such as follows:

```bash
sf --hash=md5 --droid <collection_folder>
```

### DROID as an inspiration

File format reports provide a means of statically analyzing collections of
digital objects. A DROID report satisfies the pre-conditions required to create
reliable folder- and collection-level checksums for digital collections:

* A collection is static, i.e. unlikely to change.
* Digital objects within the collection have checksums.

> NB: A collection need not be static to be analyzed but it is not the primary
use-case of this utility.

More information about the different uses for a file-format identification
report can be found in my paper in the Code4Lib journal.

* [Fractal in detail: What information is in a file format identification report?][code4lib-1]

### Writing about sumfolder1

I wrote a blog describing the utility on the OPF website.

* [What is the checksum of a directory?][opf-1]

[opf-1]: https://openpreservation.org/blogs/what-is-the-checksum-of-a-directory/?q=1

## Installation

sumfolder1 is available on pypi and can be installed as follows:

```bash
pip install -U sumfolder1
```

## Usage

sumfolder1 has the following usage instructions:

```text
usage: sumfolder1.py [-h] [--csv CSV] [--demo] [--ref] [-v]

Calculate checksums for folders in a collection of objects using a DROID format
identification report

options:
  -h, --help          show this help message and exit
  --csv CSV           Single DROID CSV to read.
  --demo              Run demo queries and output a tree to demo.txt
  --ref, --reference  Write reference set to stdout.
  -v, --version       Return version information.
```

### Demo output

sumfolder1's demo output can be invoked as follows:

```bash
python sumfolder1 --demo
```

JSON will be output to `stdout` describing a handful of queries generated using
the reference collection.

An visualization of the collection tree will be output (for demo purposes) to
`stderr`.

### Use with a DROID csv

Given a DROID csv the tool can be invoked as follows:

```bash
python sumfolder1 --csv <droid_csv_file>
```

### Outputting the reference CSV

A reference CSV can be output to `stdout`. Ideally it is piped to some other
file using a command such as follows:

```bash
python sumfolder1 --ref > <output_file>
```

## License

This work is license using: GNU GENERAL PUBLIC LICENSE Version 3.

[droid-1]: https://www.nationalarchives.gov.uk/information-management/manage-information/preserving-digital-records/droid/
[code4lib-1]: https://www.nationalarchives.gov.uk/information-management/manage-information/preserving-digital-records/droid/
[merkle-1]: https://www.youtube.com/watch?v=qHMLy5JjbjQ
[merkle-2]: https://medium.com/building-blocks-on-the-chain/learn-merkle-trees-by-programming-your-own-4f0438d40063
