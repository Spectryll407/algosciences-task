import pytest
from pathlib import Path
from server import search

def test_linear_search(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello\nworld\n")
    assert search.linear_search("hello", file)
    assert not search.linear_search("foo", file)

def test_cached_search(tmp_path):
    file = tmp_path / "test.txt"
    file.write_text("hello\nworld\n")
    assert search.cached_set_search("world", file)
    assert not search.cached_set_search("nope", file)
