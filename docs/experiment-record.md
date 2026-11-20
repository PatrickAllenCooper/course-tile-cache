# Tile Cache experiment record
> The chain from a prompt to a patch to an independent decision.
## What was fixed before the runs
Study start c5762311dac8. The same task, example, starting function, requested model and 100-second implementation limit applied to all six runs. One extra planning call supplied the same note to the three assisted runs. Plain then assisted ran in each pair. One candidate per fresh chat. The author specified the policy interface, scorer and budget and supplied no mid-run coaching.
## What the model saw
Only the public task, original function and output instruction were delivered to the model. The assisted arm also received its saved plan. The scorer and final inputs stayed outside every implementation prompt. These are bounded text-in/code-out calls with a deterministic harness. Our authenticated Codex CLI supplied gpt-6.1-sol at low reasoning effort. The recorded trials did not run in Cursor. The same prompts can be used in Cursor.
## Read every prompt and response
[Open the prompt archive](https://github.com/PatrickAllenCooper/course-tile-cache/tree/main/runs). Start at 00-plan. Open prompt.txt for the exact request, reply.txt for the public response, call.json for elapsed seconds and reported usage. Each of the six implementation directories also preserves the extracted candidate.py. No follow-up prompts were issued. All decisions used the same base function. No gold answers or final scores were fed back.
## What planning added
> - Constraint: Use only the current key, LRU-ordered residents, and 32 prior requests; support arbitrary hashable keys without serving values or using future accesses. - Hypothesis: Admit while space remains. At capacity, admit only if the missed key appears in recent history. This lets repeated tiles enter while preventing one-use scans from evicting an established viewport. - Edge case: A new viewport revisited more than 32 requests apart may never qualify for admission at capacity. Also test partially filled caches and keys with unusual equality behavior. - Stopping check: Replay identical traces against always-admit LRU, counting every miss, including rejected admissions. Accept only if aggregate fetches fall at least 25% on scan-and-return traces and stay within 5% of LRU on both steady-viewport and unique-stream controls.
The planning call took 12.2 seconds, shared across three assisted attempts. Its cost is separate from the implementation figures. Provider billing per call was unavailable. No student credentials are needed to rescore.
---
# What actually changed
## Starting policy
> def admit(key, residents, recent): return True
## Selected change
The selected admission rule fills empty slots and admits a miss at capacity only when its key appears in recent request history. The controller still serves every requested tile and evicts using the same LRU policy. Read the complete [selected source](https://github.com/PatrickAllenCooper/course-tile-cache/blob/main/candidate.py) and compare it to [the original policy](https://github.com/PatrickAllenCooper/course-tile-cache/blob/main/baseline.py). The harness copied the selected model output verbatim after stripping any Markdown fence. The application, evaluator, dataset generation and package version stayed fixed through candidate selection.
## Why this particular candidate
We selected the earliest assisted candidate that passed development, then would have tried the earliest plain pass. All six generated modules were frozen at 1c7ebd314439 before the final panel ran. The selected run was 01-assisted. On 32 reserved scan-and-return traces the selected policy reduced fetches from 7,384 to 5,627, or 23.8%. It tied LRU at 6,651 control fetches. The frozen target was 25%. Retain the result as a measured prototype that missed its release gate.
## Every implementation trial
| Run | Seconds | Dev tile fetches | Final tile fetches | Verdict |
| --- | ---: | ---: | ---: | --- |
| 01-plain | 12.1 | 1,426 | 5,627 | MISS |
| 01-assisted | 8.3 | 1,426 | 5,627 | MISS |
| 02-plain | 24.9 | 1,426 | 5,627 | MISS |
| 02-assisted | 8.8 | 1,426 | 5,627 | MISS |
| 03-plain | 14.2 | 1,426 | 5,627 | MISS |
| 03-assisted | 5.8 | 1,426 | 5,627 | MISS |
## What the repetitions establish
The plain agent met the final target 0 times in three attempts. The assisted agent met it 0 times in three attempts. Input cases measure behavior; six calls are the units for comparing agents. The fixed order and single shared planning note limit any claim about planning in general. See [all scores and usage](https://github.com/PatrickAllenCooper/course-tile-cache/blob/main/research/results.json).
---
# Reproduce or extend the study
## Score a saved result
From the repo root, run `python3 verify.py`. This exercises a hand-checked example, compares the original and selected policies and replays all six development and final scores. To inspect one candidate independently run `python3 score.py runs/01-plain/candidate.py`. A failed target returns exit status 1 even when all checks ran as designed.
## Repeat one trial in Cursor
Make a new folder outside the published repository and open it in Cursor. Copy only baseline.py as candidate.py and the chosen run’s prompt.txt. Use a fresh chat and record the selected model, mode, date and time limit. Paste the full prompt. Save the returned module as candidate.py. Close the chat, copy that candidate back under a new name, and score it from the original repo. For a matched repeat, use identical settings and choose 01-plain or 01-assisted. Record provider differences. For a different model or native Cursor tools, label the result as a new condition.
## Use Plan and Goal for a larger project
In Plan mode ask for two designs and one cheap observation that would choose between them. Edit and save the plan. In Agent, or /goal in a Cursor CLI version that offers it, supply the measurable outcome, constraints, time and stop rule. Ask for a diff, development evidence and what remains unverified. Keep final evaluation under your control. These are instructions for extending this study. The six recorded implementation calls used a one-response budget.
## Reproduce the original runner
The optional `python3 research/trials.py NEW_RUN_DIR` uses the authenticated Codex CLI, the pinned model alias, and seven new calls; a provider subscription or access can be required. A free Cursor model is sufficient to study the method. All saved scoring works offline.
## A credible next claim
Collect consented, de-identified viewport traces or simulate slow neighborhood drift. Pre-register a guard on first visits to a new neighborhood. Keep this test panel sealed during the next design cycle. Before a new campaign, freeze fresh cases and move the evaluator outside the editable workspace. The public evidence here is available for inspection by anyone. Prior exposure removes its value as a blind test.
