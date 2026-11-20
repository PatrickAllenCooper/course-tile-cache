# Tile Cache

Protect the home viewport from a one-use scan. On 32 reserved scan-and-return traces the selected policy reduced fetches from 7,384 to 5,627, or 23.8%. It tied LRU at 6,651 control fetches. The frozen target was 25%. Retain the result as a measured prototype that missed its release gate.

[Project guide (PDF)](docs/project-guide.pdf) · [Experiment record (PDF)](docs/experiment-record.pdf) · [Every actual prompt and reply](runs/) · [Complete scores](research/results.json)

## Try it in Cursor’s terminal

Use Python 3.11+. No network, model key or dependency installation is required.

```sh
python3 check_example.py
python3 verify.py
python3 score.py
```

The last command exits 1 if the selected implementation misses the frozen target. The verification command succeeds when the recorded measurements reproduce, including a recorded miss.

## Study design

Three fresh plain model requests and three with a shared planning note. The examples use a bounded implementation protocol and synthetic inputs. Plain successes 0/3, assisted successes 0/3. See [the frozen contract](brain/objective.md), [selection protocol](brain/protocol.md), [upstream source and license](vendor/) and [recorded model runner](research/trials.py). The `study-start` tag fixes the starting code and evaluator. A fresh Cursor replication is described in the experiment record. For a new graded study choose a harder objective and reserve fresh cases.

## Contribution

The course materials and evaluation were prepared with AI assistance. The selected implementation is a saved foundation-model response. This repository adds a teaching application to a pinned external library. A new neighborhood whose tiles recur only after more than 32 requests may keep missing. The trace generators cover a narrow pattern. The 23.8% figure is a fetch count, not a measured change in page-load time or network bytes.
