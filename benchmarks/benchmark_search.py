import time
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from server import search


def benchmark(file: Path, queries: list[str]):
    methods = {
        "linear": search.linear_search,
        "cached_set": search.cached_set_search,
        "mmap": search.mmap_search,
        "binary": search.binary_search,
        "regex": search.regex_search,
    }

    results = []
    for name, func in methods.items():
        start = time.perf_counter()
        for q in queries:
            func(q, file)
        elapsed = (time.perf_counter() - start) * 1000
        results.append({"method": name, "ms": elapsed})
    return pd.DataFrame(results)


if __name__ == "__main__":
    file = Path("tests/data/small_sample.txt")
    queries = ["hello", "world", "foobar", "notfound"]

    df = benchmark(file, queries)
    print(df)

    ax = df.plot(x="method", y="ms", kind="bar", legend=False, title="Search Performance")
    ax.set_ylabel("Time (ms)")
    plt.tight_layout()
    plt.savefig("benchmarks/results.png")
