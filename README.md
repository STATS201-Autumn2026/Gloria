---
pretty_name: Across the Firewall - Weibo Narrative Summaries (Course Edition)
language:
- en
license: apache-2.0
task_categories:
- text-classification
size_categories:
- 1K<n<10K
tags:
- social-science
- media-narratives
- weibo
- replication
- synthetic-summaries
configs:
- config_name: default
  data_files:
  - split: full
    path: data/narrative_summaries.csv
---

# Across the Firewall: Weibo Narrative Summaries - Course Edition

Version **1.0.0**, prepared **November 18, 2026**.

This is an independently prepared course-use derivative of the public replication materials for **Hans W. A. Hanley, Yingdan Lu, and Jennifer Pan (2025), "Across the firewall: Foreign media's role in shaping Chinese social media narratives on the Russo-Ukrainian War," PNAS 122(1), e2420607122**. It is not an official release by the paper's authors and does not imply their endorsement.

- [Published paper](https://doi.org/10.1073/pnas.2420607122)
- [Original research repository](https://github.com/hanshanley/narrative-influence)
- [Pinned source revision](https://github.com/hanshanley/narrative-influence/tree/f82076dc0c94498dfa88f8d387412b6b424a1c66)
- [Original dataset documentation](https://github.com/hanshanley/narrative-influence/blob/f82076dc0c94498dfa88f8d387412b6b424a1c66/weibo_clusters_statistics_summaries/readme.md)

## What this dataset contains

The complete public TSV at the pinned revision contains **2,147 narrative-cluster records**. Each record includes an **English AI-generated summary**, a count of Weibo posts, and four media-ecosystem association scores. The upstream documentation describes the scores as normalized PMI values and the summaries as generated with LLaMa 3.1. The original paper reports Llama 3-generated summaries.

The underlying study concerns Chinese Weibo posts about the Russia-Ukraine war. It analyzes relevant Weibo posts from February 1 to April 19, 2022, and news articles from January 1 to June 1, 2022. These are study-level coverage dates, not timestamps supplied for every row in this release.

**This package does not contain original Chinese Weibo post text, individual user records, article full texts, or the study's 8.26 million news articles.** The language of the released summaries is English, so the metadata uses `en`. The original study reports 2,183 narratives; the public TSV contains a selected set of 2,147 records. The exact relationship between release selection, normalized scores, and the published aggregate results requires further verification.

## Files

| File | Contents |
|---|---|
| `data/narrative_summaries.csv` | Viewer-ready CSV with all 2,147 source records and documented derived fields |
| `source/weibo_cluster_summaries.tsv` | Byte-for-byte copy of the pinned upstream data file |
| `source/UPSTREAM_README.md` | Upstream explanation of the released summaries and association scores |
| `source/UPSTREAM_REPOSITORY_README.md` | Upstream repository documentation and attribution |
| `build_dataset.py` | Standard-library Python script that rebuilds the CSV and audit |
| `audit.json` | Reproducible counts, hashes, tie checks, and distribution comparison |
| `LICENSE` | Upstream Apache License 2.0 |
| `NOTICE` | Attribution and packaging-change notice |

## Record definition and fields

The observation unit is **one released narrative cluster**, not one post or article. All original rows are retained in original order; the source summary wording is unchanged.

| Field | Type | Definition |
|---|---|---|
| `record_id` | string | Stable ID within this pinned edition, generated from source row order; not an original author-supplied cluster ID |
| `source_row` | integer | One-based data-row number in the upstream TSV, excluding its header |
| `summary` | string | Original English AI-generated narrative summary |
| `n_weibo` | integer | Upstream `Number of Weibos` value |
| `pmi_china` | float | Released `China-based Domains PMI` value |
| `pmi_us` | float | Released `US-based Domains PMI` value |
| `pmi_russia` | float | Released `Russian-based Domains PMI` value |
| `pmi_ukraine` | float | Released `Ukrainian-based Domains PMI` value |
| `highest_score_ecosystem` | string | Highest of the four released scores: China, US, Russia, Ukraine; `ambiguous` for an exact tie |
| `exact_tie` | boolean | Whether two or more ecosystems share the maximum score |
| `tied_ecosystems` | string or null | Pipe-separated winners for tied records; empty CSV cell otherwise |
| `score_margin` | float | Largest minus second-largest released score; zero for an exact tie |
| `summary_group_id` | string | SHA-256 of the summary after trimming surrounding whitespace and lowercasing; groups exact normalized duplicates |
| `duplicate_summary_count` | integer | Number of records sharing the same normalized summary |

The scores are association measures, not probabilities. Negative values are valid. Labels derived here are **computational proxies**, not human-verified source, stance, truthfulness, or influence labels. A narrative associated with Russia-based websites is not necessarily pro-Russian or originally authored in Russia.

## Preparation and changes

Prepared with ChatGPT assistance for dataset organization, deterministic transformation code, documentation, and data-quality checks. This packaging does not claim original authorship of the underlying records or of the PNAS research. No new narrative summaries were generated during packaging.

Changes from the upstream TSV:

1. Convert tab-separated records to UTF-8 CSV and normalize column names.
2. Add stable row IDs, exact-duplicate group IDs, and duplicate counts.
3. Compute the maximum-score ecosystem, explicit tie indicators, and score margins.
4. Preserve all 2,147 rows, including ambiguous and duplicated summaries.
5. Add dataset documentation, provenance, and a reproducible audit.

No missing values were imputed. No model was trained. No training, validation, or test split was assigned. `full` is the complete collection, not a recommended training split.

## Audit findings

| Check | Result |
|---|---:|
| Source records | 2,147 |
| Records missing any of the six source fields | 0 |
| Distinct summaries after trimming/lowercasing | 2,146 |
| Exact duplicate-summary groups | 1 |
| Records tied for highest score | 14 |
| Records with score margin below 0.01, including ties | 258 |
| Records with a unique highest score | 2,133 |

The 0.01 margin threshold is an exploratory sensitivity flag, not a validated confidence threshold.

| Highest-score ecosystem | Records excluding ties | Share excluding ties | Paper Table 1, Analysis 2 |
|---|---:|---:|---:|
| China | 411 | 19.3% | 9.7% |
| US | 85 | 4.0% | 18.3% |
| Russia | 808 | 37.9% | 37.1% |
| Ukraine | 829 | 38.9% | 35.0% |

There are also 14 records labeled `ambiguous`. Rounding can make shares sum to slightly more than 100%.

**The simple maximum of the released normalized scores does not reproduce the paper's Table 1 distribution.** Release selection and normalization may contribute; the cause has not been established. This package preserves the values without correction and labels the derived outcome explicitly. It must not be described as a successful replication of the published table.

## Intended course use and evaluation

A possible question is: Can narrative-summary text predict the ecosystem with the highest released association score?

Use only `summary` as the text-model input. The four association scores, `highest_score_ecosystem`, `exact_tie`, `tied_ecosystems`, and `score_margin` reveal information about the target and must not be input features for that task. The count and identifier fields should also be excluded from a text-only model.

For a primary four-class analysis, exclude the 14 exact ties, report the exclusion, and investigate near-ties in a sensitivity analysis. Keep records with the same `summary_group_id` in the same split. That ID only detects normalized exact duplicates: inspect paraphrases and event-related summaries before treating different clusters as independent.

Compare a majority-class baseline with TF-IDF plus logistic regression. Fit vocabulary and tune parameters on training data only. Evaluate on held-out groups using macro-F1, per-class recall, and a confusion matrix. The small US-associated class makes overall accuracy alone misleading. Preserve the split assignment and random seed in the project's code repository.

## Limitations and appropriate interpretation

- Summaries are generated by a language model; they may omit context, simplify a narrative, or express bias. They are not human-verified transcriptions.
- Summaries report narratives present in a corpus. Some describe false, disputed, or propagandistic claims. Their inclusion is not an endorsement or factual verification.
- Analysis concerns this selected early-2022 war-related release and does not establish population-wide patterns in Chinese media or Weibo.
- The source file lacks individual timestamps, source article/post texts, and user-level observations. It cannot by itself establish narrative origin or causal diffusion.
- The derived labels reproduce a rule applied to released scores, not independently observed ground truth. Model performance measures agreement with that rule.
- Normalized-score interpretation and the discrepancy from published aggregates remain open validation issues.
- Do not use these data to infer the political views of individual people.

## Provenance and reproducibility

- Original authors: Hans W. A. Hanley, Yingdan Lu, Jennifer Pan.
- Repository: `hanshanley/narrative-influence`.
- Pinned commit: `f82076dc0c94498dfa88f8d387412b6b424a1c66`.
- Source path: `weibo_clusters_statistics_summaries/weibo_cluster_summaries.tsv`.
- Original Git blob SHA-1: `233205a73674a0b9470eb6131f0d300f4312876c`.
- SHA-256 checksums and audit statistics: `audit.json`.

Rebuild from the bundled source using Python 3.10 or later:

```bash
python build_dataset.py
```

The script verifies the original Git blob hash and regenerates the CSV and audit. It uses only the Python standard library. Preserve the CRLF line endings of the original TSV when copying or editing repository files.

To load after uploading this folder to a Hugging Face dataset repository, replace the example repository ID below with the actual account/repository name:

```python
from datasets import load_dataset
dataset = load_dataset("YOUR_USERNAME/weibo-narrative-summaries", split="full")
```

For a submitted assignment, record both the source commit above and the exact commit of this Hugging Face repository that you used. A course requiring an organization-owned dataset may additionally require an organization copy.

## License and attribution

The upstream repository is distributed under **Apache License 2.0**, reproduced in `LICENSE`. This derivative retains that license and credits the original authors in `NOTICE`. Copyright 2024 The Board of Trustees of The Leland Stanford Junior University, as stated in the upstream repository. This package does not redistribute the original article corpus or the paper PDF, and it does not extend the repository license to those separate materials.

## Citation

Hanley, Hans W. A., Yingdan Lu, and Jennifer Pan. 2025. "Across the Firewall: Foreign Media's Role in Shaping Chinese Social Media Narratives on the Russo-Ukrainian War." *Proceedings of the National Academy of Sciences* 122 (1): e2420607122. https://doi.org/10.1073/pnas.2420607122.

```bibtex
@article{hanley2025firewall,
  author = {Hanley, Hans W. A. and Lu, Yingdan and Pan, Jennifer},
  title = {Across the firewall: Foreign media's role in shaping Chinese social media narratives on the Russo-Ukrainian War},
  journal = {Proceedings of the National Academy of Sciences},
  year = {2025},
  volume = {122},
  number = {1},
  pages = {e2420607122},
  doi = {10.1073/pnas.2420607122}
}
```

Also identify this course edition and its exact Hugging Face revision when using its derived fields.
