"""Count tile fetches on a viewport trace. Supply tile IDs on the command line."""
from collections import deque
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "vendor"))
from cachetools import LRUCache
from candidate import admit


def play(keys, policy=admit, capacity=16):
    cache = LRUCache(maxsize=capacity)
    order = {}
    recent = deque(maxlen=2 * capacity)
    fetches = 0
    for key in keys:
        if key in cache:
            value = cache[key]
            del order[key]
            order[key] = None
        else:
            fetches += 1
            value = str(key).encode("utf8")
            decision = policy(key, tuple(order), tuple(recent))
            if type(decision) is not bool:
                raise ValueError("Admission must be boolean")
            if decision:
                if len(order) == capacity:
                    del order[next(iter(order))]
                cache[key] = value
                order[key] = None
        if value != str(key).encode("utf8") or len(cache) > capacity:
            raise AssertionError("Incorrect tile or capacity exceeded")
        recent.append(key)
    return fetches


if __name__ == "__main__":
    print(f"{play(sys.argv[1:])} fetches for {len(sys.argv)-1} requests")
