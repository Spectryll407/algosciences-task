import time
import pandas as pd
import matplotlib.pyplot as plt
from server import search
from pathlib import Path

def benchmark(file: Path, queries: list[str]):
    methods = {
        "linear": search.linear_search,
        "cached": search.cached_set_search,
        # TODO: add mmap, bisect, regex, trie...
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
    queries = ["hello", "world", "foo", "bar"]
    df = benchmark(file, queries)
    print(df)
    df.plot(x="method", y="ms", kind="bar")
    plt.savefig("benchmarks/results.png")
