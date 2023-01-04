"""Objects associated with sumfolder1 results."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class HashResult:
    """Results class for individual hashes."""

    name: str = None
    parent_folder: Path = None
    parent_folder_name: str = None
    containing_dirs: list = field(default_factory=list)

    def as_dict(self):
        """Request the hash result as a dict."""
        containing_dirs = [f"{folder}" for folder in self.containing_dirs]
        folder = f"{self.parent_folder}"
        if self.parent_folder:
            return {
                "name": self.name,
                "parent_folder": folder,
                "parent_folder_name": self.parent_folder_name,
                "containing_dirs": containing_dirs,
            }
        return {
            "name": self.name,
            "containing_dirs": containing_dirs,
        }


@dataclass
class QueryResult:
    """Results class for SumFolder1.

    {
        'query': {
            'search_hash': 'abdc1234',
            'found': True,
            'type': 'Directory',
            'results': [{
                'name': 'name',
                'containing_dirs': ["ccdc1234", "dcdc1234", "ecdc1234"]
            }]
        }
    }

    {
        "query": {
            "search_hash": "acdc1234",
            "found": true,
            "type": "File",
            "resulta": [{
                "name": "name",
                "parent_folder": "bcdc1234",
                "parent_folder_name": "somefolder1",
                "containing_dirs": ["ccdc1234", "dcdc1234", "ecdc1234"]
            }]
        }
    }

    """

    search_hash: str = None
    found: bool = False
    is_root: bool = False
    type_: str = None
    results: list[HashResult] = field(default_factory=list)

    def as_dict(self):
        """Request the query result as a dict."""
        results = []
        for result in self.results:
            results.append(result.as_dict())
        if self.is_root:
            return {
                "query": {
                    "search_hash": self.search_hash,
                    "found": self.found,
                    "type": self.type_,
                    "is_root": self.is_root,
                }
            }
        return {
            "query": {
                "search_hash": self.search_hash,
                "found": self.found,
                "type": self.type_,
                "results": results,
            }
        }
