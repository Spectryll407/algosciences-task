from pathlib import Path
import mmap
import bisect
import re


def linear_search(query: str, file_path: Path) -> bool:
    """Naive scan of file, line by line."""
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == query:
                return True
    return False


def cached_set_search(query: str, file_path: Path) -> bool:
    """Load file once into memory (as a set)."""
    cache_attr = "_cache"
    cache_path_attr = "_cached_path"

    if (not hasattr(cached_set_search, cache_attr) or
        getattr(cached_set_search, cache_path_attr, None) != file_path):
        with file_path.open("r", encoding="utf-8") as f:
            cached_set_search._cache = {line.strip() for line in f}
        cached_set_search._cached_path = file_path

    return query in cached_set_search._cache


def mmap_search(query: str, file_path: Path) -> bool:
    """Use memory-mapped file for fast lookup (handles Windows newlines)."""
    with file_path.open("r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        # try both LF and CRLF endings
        patterns = [
            f"{query}\n".encode("utf-8"),
            f"{query}\r\n".encode("utf-8"),
        ]
        found = any(mm.find(p) != -1 for p in patterns)
        mm.close()
        return found

def binary_search(query: str, file_path: Path) -> bool:
    """Binary search in sorted file (requires sorted data)."""
    if not hasattr(binary_search, "_cache"):
        with file_path.open("r", encoding="utf-8") as f:
            binary_search._cache = sorted(line.strip() for line in f)
    idx = bisect.bisect_left(binary_search._cache, query)
    return idx < len(binary_search._cache) and binary_search._cache[idx] == query


def regex_search(query: str, file_path: Path) -> bool:
    """Regex full-line match."""
    pattern = re.compile(rf"^{re.escape(query)}$")
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if pattern.match(line.strip()):
                return True
    return False
