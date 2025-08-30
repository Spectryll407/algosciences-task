from pathlib import Path

def linear_search(query: str, file_path: Path) -> bool:
    """Naive scan of file, line by line."""
    with file_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip() == query:
                return True
    return False

def cached_set_search(query: str, file_path: Path) -> bool:
    """Load file once into memory (as a set)."""
    if not hasattr(cached_set_search, "_cache"):
        with file_path.open("r", encoding="utf-8") as f:
            cached_set_search._cache = {line.strip() for line in f}
    return query in cached_set_search._cache

# later: mmap_search, bisect_search, regex_search, trie_search...
