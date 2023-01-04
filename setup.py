"""Setuptools for sumfolder1"""

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

version = {}
with open("src/sumfolder1/version.py", encoding="UTF-8") as fp:
    exec(fp.read(), version)  # pylint: disable=W0122

setup(
    name="sumfolder1",
    version=version.get("_version"),
    description="Checksums for folders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ross-spencer/sumfolder1",
    author="Ross Spencer",
    author_email="all.along.the.watchtower2001+github@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Other Audience",
        "Topic :: System :: Archiving",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    install_requires=[
        "colorama==0.4.6",
    ],
    keywords="digital-preservation, collection-analysis, checksums, merkle-tree",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9, <4",
    entry_points={"console_scripts": ["sumfolder1=sumfolder1.sumfolder1:main"]},
    project_urls={
        "Bug Reports": "https://github.com/ross-spencer/sumfolder1/issues",
        "Source": "https://github.com/ross-spencer/sumfolder1",
    },
)
