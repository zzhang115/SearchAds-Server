# Search Ads · Data Preparation & Retrieval

**Python data normalization · Java search components · Reproducible tests**

A historical search-advertising project with a newly hardened, standalone data-cleaning entry point. The Python component demonstrates a practical delivery workflow: validate records, preserve business values, produce valid JSONL, and prove behavior with regression tests.

## Try the verified component

Requires Python 3.10+; no packages, network access, credentials or payment required. From the repository root:

```sh
python3 click_log_data/CleanData/cleanData.py --input examples/ads.sample.jsonl --output cleaned-demo.jsonl
python3 -m unittest discover -s tests -v
```

The demo uses **synthetic records**, not customer data. Expected result: two output records. Choose a new output filename when rerunning; existing files are intentionally protected.

## What the cleaner guarantees

- Normalizes title punctuation/spacing, lowercases queries, and adds deduplicated title keywords.
- Preserves IDs, prices, booleans, nulls and additional fields. It never invents replacement prices.
- Serializes with the JSON encoder, including Unicode and escaped characters.
- Processes one input line at a time; skips blank lines, stops on invalid records with a line number.
- Publishes only a complete result; errors do not leave a partial output or overwrite an existing file.

Input: one JSON object per line. `title`, `query`, and `brand` must be strings; optional `keyWords` must be an array of strings. This is normalization, not a comprehensive advertising schema validator. Atomic publication uses same-directory hard links; filesystems without hard-link support fail safely.

## Repository map

| Area | Purpose | Verification boundary |
| --- | --- | --- |
| `click_log_data/CleanData/cleanData.py` | Deterministic JSONL normalization | Local CLI and unit tests |
| `click_log_data/CTR/`, `Features/`, `Word2Vec/` | Historical modeling experiments | Not revalidated |
| `src/ads/`, `src/query/`, `src/server/` | Java selection, query and servlet components | Not revalidated |
| `tests/`, `examples/` | Regression tests and synthetic sample | Safe offline entry point |

## Modernization notes

The old cleaner ran during import, used fixed paths, randomized prices and attempted JSON conversion with quote replacement. The current CLI intentionally changes that behavior: explicit paths, deterministic values, no import side effects, and proper serialization. Workflows relying on the old ID offsets or random-price generation need a separate synthetic-data generator; those transformations are no longer performed implicitly.

## Scope & responsible use

This repository is a portfolio/learning project, not a deployed advertising service. Passing cleaner tests does not establish model quality, production scalability or a working end-to-end server. Historical crawlers and datasets are not required for the demo and should not be run against third-party services without checking permission and current terms.

Modernization changes were prepared with AI assistance. No client outcomes, performance numbers, or commercial deployments are claimed. No new license is asserted for historical code or bundled data.
