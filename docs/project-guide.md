# Tile Cache
> Protect the home viewport from a one-use scan.
## Shop for the project
A map kiosk keeps returning to the same neighborhood. A flyover can evict every useful tile. A deterministic trace lets us count fetches on a laptop. I passed on a latency benchmark against a live map server because network weather would dominate the signal.
## Start with something people already use
cachetools 5.5.2 provides the LRU store. The controller owns tile values, recency, a 16-slot ceiling and a bounded history of 32 keys. The only model-written decision is whether a newly fetched tile deserves a slot. The distribution URL, exact version, digest and upstream license live in vendor/. The course application and its starting policy are new.
## Turn the tradeoff into a number
Count actual misses, including misses whose result is never cached. For each trace replay always-admit LRU and the candidate on the same request sequence. Compare sums, then enforce the separate control threshold.
With 16 slots, a scan longer than 16 can erase an entire working set. Repeated home keys and one-use flyover keys have different histories even when their tile bytes cost exactly the same to fetch.
## Try it locally
Open the repository in Cursor. Use Python 3.11 or newer from its terminal. No package install, dataset download or model account is needed to run the example.
`python3 check_example.py`
The worked trace visits eight home tiles, scans twenty new ones, then returns home. Ordinary LRU fetches 36 times and the selected admission policy fetches 28 times.
## Reserved tile fetches
Always admit 7384 · Selected 5627
---
# From objective to portfolio claim
## Write the contract first
A map kiosk repeatedly pans over a small area while visitors occasionally fly across hundreds of one-use tiles. The byte-identical tile loader already caches 16 entries with LRU. Implement admit(key, residents, recent). On a MISS return a bool indicating whether to admit the loaded tile. residents lists cached keys from least to most recently used. recent contains the last 32 REQUEST keys including hits, excluding the current request. There is no other persistent state. Admission at capacity evicts LRU. The cache controller alone serves values. Reduce aggregate cold tile fetches by at least 25% vs always-admit LRU on scan-and-return traces. On control traces (steady viewport and streaming unique tiles) keep aggregate fetches within 5% of LRU. Valid for hashable tile keys, no future access. Example pattern: revisit four home tiles repeatedly, scan 32 single-use tiles, revisit home.
## Plan with the model
Admitting every new tile lets a scan evict the neighborhood. Once the cache is full, consider admission only after repeat demand. Keep the loader and LRU eviction code intact so the agent cannot gain points by skipping a fetch or returning a different tile. A second design you could investigate follows.
Prefetch likely neighbor tiles. That might improve perceived latency but can increase bytes, so the current miss count would be the wrong primary score.
## Hand off one decision
In a clean copy of the starting policy, use Cursor Plan to name the edge case that could make a plausible patch fail. Save its reasoning as a short plan. Give a fresh Agent chat the objective, approved plan, editable function and a stopping budget. The experiment record links the exact inputs used here.
## Inspect the evidence
On 32 reserved scan-and-return traces the selected policy reduced fetches from 7,384 to 5,627, or 23.8%. It tied LRU at 6,651 control fetches. The frozen target was 25%. Retain the result as a measured prototype that missed its release gate. Plain runs passed 0/3, and plan-assisted runs passed 0/3. The unchanged application policy and the plain model are two different baselines.
`python3 verify.py` reproduces the saved outcomes. `python3 score.py` evaluates the selected candidate and exits 1 if it misses the target.
## Where the claim ends
A new neighborhood whose tiles recur only after more than 32 requests may keep missing. The trace generators cover a narrow pattern. The 23.8% figure is a fetch count, not a measured change in page-load time or network bytes. Collect consented, de-identified viewport traces or simulate slow neighborhood drift. Pre-register a guard on first visits to a new neighborhood. Keep this test panel sealed during the next design cycle.
~ [Repository, source code and second PDF](https://github.com/PatrickAllenCooper/course-tile-cache)   |   [Machine-readable results](https://github.com/PatrickAllenCooper/course-tile-cache/blob/main/research/results.json)
