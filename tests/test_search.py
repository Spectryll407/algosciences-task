import pytest
from pathlib import Path
from server import search


@pytest.fixture
def sample_file(tmp_path: Path):
    file = tmp_path / "sample.txt"
    file.write_text("hello\nworld\nfoobar\n")
    return file


def test_linear_search(sample_file):
    assert search.linear_search("hello", sample_file)
    assert search.linear_search("world", sample_file)
    assert not search.linear_search("python", sample_file)


def test_cached_set_search(sample_file):
    assert search.cached_set_search("foobar", sample_file)
    assert not search.cached_set_search("missing", sample_file)


def test_mmap_search(sample_file):
    assert search.mmap_search("hello", sample_file)
    assert not search.mmap_search("nope", sample_file)


def test_binary_search(sample_file):
    # File must be sorted for binary search
    sorted_file = sample_file.parent / "sorted.txt"
    sorted_file.write_text("alpha\nfoobar\nhello\nworld\n")
    assert search.binary_search("foobar", sorted_file)
    assert not search.binary_search("zzz", sorted_file)


def test_regex_search(sample_file):
    assert search.regex_search("world", sample_file)
    assert not search.regex_search("worl", sample_file)  # partial should not match
