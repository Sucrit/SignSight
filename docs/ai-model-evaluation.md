# SignSight AI Model Evaluation

Evaluation date: 2026-06-09

This report summarizes the current testing and evaluation pass for the SignSight backend AI models. It covers the static landmark classifier, the gesture classifier artifact, and the available gesture archive dataset.

## Scope

Evaluated artifacts and data:

- Static landmark model: `backend/models/asl_landmarks_model.joblib`
- Static landmark approved records loaded by `load_approved_landmark_records()`
- Gesture model: `backend/models/asl_gesture_model.joblib`
- Gesture archive: `backend/gestures/archived_gesture_dataset/*.jsonl`

Not evaluated:

- Gesture V2 model, because `backend/models/asl_gesture_model_v2.joblib` was not present.
- Missing static letters with no approved samples.
- Live camera inference quality, lighting variation, signer diversity, or mobile-device runtime behavior.

## Commands Run

```bash
backend/.venv/bin/python backend/scripts/evaluate_landmark_confusions.py
backend/.venv/bin/python backend/scripts/benchmark_landmark_models.py
```

I also ran a one-off backend evaluation script to score the active model artifacts against the available approved/archive records.

## Static Landmark Classifier

### Active Model Coverage

The active static landmark model currently supports 18 labels:

```text
A, B, C, D, E, F, I, I_LOVE_YOU, M, N, O, R, S, T, U, V, W, Y
```

Approved records scored against the active model: `3650`

Per-label approved counts:

| Label | Count |
| --- | ---: |
| A | 189 |
| B | 212 |
| C | 239 |
| D | 63 |
| E | 147 |
| F | 203 |
| I | 176 |
| I_LOVE_YOU | 296 |
| M | 198 |
| N | 358 |
| O | 242 |
| R | 194 |
| S | 280 |
| T | 265 |
| U | 90 |
| V | 207 |
| W | 191 |
| Y | 100 |

### Active Model Apparent Accuracy

This is an apparent evaluation against available approved records, not a clean independent test set.

| Metric | Result |
| --- | ---: |
| Raw accuracy | 1.0000 |
| Rule-adjusted accuracy | 0.9992 |

The rule-adjusted pass slightly reduced apparent accuracy because the heuristic override changed a small number of otherwise correct predictions. The main observed effect was around the visually similar `C` and `O` family.

Per-label rule-adjusted apparent F1 scores:

| Label | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| A | 1.00 | 1.00 | 1.00 | 189 |
| B | 1.00 | 1.00 | 1.00 | 212 |
| C | 0.99 | 1.00 | 0.99 | 239 |
| D | 1.00 | 1.00 | 1.00 | 63 |
| E | 1.00 | 1.00 | 1.00 | 147 |
| F | 1.00 | 1.00 | 1.00 | 203 |
| I | 1.00 | 1.00 | 1.00 | 176 |
| I_LOVE_YOU | 1.00 | 1.00 | 1.00 | 296 |
| M | 1.00 | 1.00 | 1.00 | 198 |
| N | 1.00 | 1.00 | 1.00 | 358 |
| O | 1.00 | 0.99 | 0.99 | 242 |
| R | 1.00 | 1.00 | 1.00 | 194 |
| S | 1.00 | 1.00 | 1.00 | 280 |
| T | 1.00 | 1.00 | 1.00 | 265 |
| U | 1.00 | 1.00 | 1.00 | 90 |
| V | 1.00 | 1.00 | 1.00 | 207 |
| W | 1.00 | 1.00 | 1.00 | 191 |
| Y | 1.00 | 1.00 | 1.00 | 100 |

Summary F1:

| Average | F1 |
| --- | ---: |
| Macro average | 1.00 |
| Weighted average | 1.00 |

### Holdout Confusion Evaluation

`backend/scripts/evaluate_landmark_confusions.py` completed successfully.

Overall holdout accuracy:

| Metric | Result |
| --- | ---: |
| Raw holdout accuracy | 1.000 |
| Rule-adjusted holdout accuracy | 1.000 |

Focused confusion-family results:

| Family | Result |
| --- | ---: |
| I / Y | 1.000 |
| U / V / W | 1.000 |
| M / N / T / S / E | 1.000 |
| D / K / L | 1.000 for available D samples only |
| R / U | 1.000 |
| C / O / F | 1.000 |

Families with no samples:

- `G / H`
- `P / Q`

Important note: `D / K / L` only had `D` samples in the evaluated subset. `K` and `L` had no samples, so that family result does not prove K/L recognition quality.

### Landmark Benchmark Status

`backend/scripts/benchmark_landmark_models.py` did not run a full benchmark because the approved landmark dataset is incomplete for several required labels.

Blocked labels:

| Label | Approved Samples |
| --- | ---: |
| G | 0 |
| H | 0 |
| K | 0 |
| L | 0 |
| P | 0 |
| Q | 0 |
| X | 0 |

The benchmark requires at least 10 approved samples per label, so the current dataset is not ready for full alphabet benchmarking.

## Gesture Classifier

### Service Dataset Availability

The gesture service loader reads files from:

```text
backend/gestures/{LABEL}.jsonl
```

Current top-level service gesture files: none.

Available gesture samples are stored in:

```text
backend/gestures/archived_gesture_dataset/
```

This means the current training service will not automatically use the archived gesture captures unless they are migrated or the loader is intentionally extended.

### Gesture Archive Coverage

Official labels found in the archive: `10`

Archive records scored: `527`

| Label | Count |
| --- | ---: |
| GOODBYE | 6 |
| HELLO | 82 |
| HELP | 37 |
| J | 41 |
| NO | 54 |
| PLEASE | 34 |
| SORRY | 44 |
| THANK_YOU | 95 |
| WHERE | 49 |
| YES | 85 |

Missing official gesture labels:

- `WHAT`
- `Z`

The archive also contains a non-official label, `PAKYU`, which is not part of `GESTURE_LABELS` and was excluded from the evaluation.

### Active Gesture Model Apparent Accuracy

The active gesture model supports the same 10 archive labels listed above.

This is an apparent evaluation on the archive and may include training data, so it is not a clean generalization estimate.

| Metric | Result |
| --- | ---: |
| Records scored | 527 |
| Apparent accuracy | 0.9734 |
| Macro F1 | 0.97 |
| Weighted F1 | 0.97 |

Lowest or notable per-class F1 scores:

| Label | F1 |
| --- | ---: |
| HELP | 0.94 |
| PLEASE | 0.94 |
| SORRY | 0.95 |
| HELLO | 0.97 |
| YES | 0.97 |

### Gesture Archive Holdout Retrain

I retrained a gesture classifier using the same SVC configuration used by the backend and evaluated a stratified 80/20 split of the archive.

| Metric | Result |
| --- | ---: |
| Train records | 421 |
| Test records | 106 |
| Holdout accuracy | 0.9528 |
| Macro F1 | 0.95 |
| Weighted F1 | 0.95 |

Per-label holdout F1:

| Label | F1 |
| --- | ---: |
| GOODBYE | 1.00 |
| HELLO | 0.97 |
| HELP | 0.86 |
| J | 0.94 |
| NO | 0.96 |
| PLEASE | 0.93 |
| SORRY | 0.94 |
| THANK_YOU | 1.00 |
| WHERE | 0.95 |
| YES | 0.94 |

Main holdout confusions:

- `HELP` confused with `YES`
- `SORRY` confused with `PLEASE`
- `WHERE` confused with `NO`
- `HELLO` confused with `J`
- `YES` confused with `HELP`

## Interpretation

The current models are promising on the available local data, especially for the labels already represented in the training sets. However, the results should not be treated as production-grade proof yet.

Main reasons:

- Static landmark evaluation has missing labels, so full alphabet performance is unknown.
- Several static confusion families report perfect results because one or more labels have no samples.
- The active landmark model apparent score is likely optimistic because it evaluates against available approved records rather than a separately collected test set.
- The full landmark benchmark is blocked by missing approved samples for `G`, `H`, `K`, `L`, `P`, `Q`, and `X`.
- Gesture archive results are strong, but the archive is not currently in the service loader path.
- Gesture classes are incomplete because `WHAT` and `Z` are missing.
- `GOODBYE` has only 6 archive samples, so its perfect score is not statistically meaningful.

## Recommendations

1. Add at least 10 approved static samples for `G`, `H`, `K`, `L`, `P`, `Q`, and `X` so the benchmark script can run.
2. Prefer a much higher target for production readiness: balanced samples across left/right hands, multiple signers, multiple devices, and varied lighting.
3. Migrate reviewed gesture archive records into `backend/gestures/{LABEL}.jsonl` or update the service loader if the archive is intended to remain the canonical source.
4. Add `WHAT` and `Z` gesture samples before claiming full configured gesture-label support.
5. Create a signer-holdout evaluation once enough signer metadata exists. Row-stratified splits can overestimate quality when captures come from the same signer/session.
6. Save confusion matrices and classification reports as machine-readable artifacts during CI or release evaluation.
7. Keep the rule-adjusted landmark accuracy separate from raw model accuracy so heuristic overrides can be audited independently.

## Release Readiness Summary

Current status: useful prototype model, not fully production validated.

The strongest current model area is recognition for existing static landmark labels and the archived 10-label gesture set. The biggest blockers are incomplete label coverage, lack of full benchmark eligibility, and the mismatch between the gesture service loader path and the available archived gesture data.
