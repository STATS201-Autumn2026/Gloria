---
language:
- zh
- en
size_categories:
- n<1K
pretty_name: Chinese Antitrust Case Metadata Readiness Pilot
---

# Dataset card

## Purpose and status

A prepared 40-row metadata preview for checking case metadata, with 20 merger records and 20 penalty announcement records. This is a readiness pilot, not a labeled media benchmark. It has not been published to GitHub or Hugging Face. Media outcomes, unique case identities and first public release dates require verification.

## Sources and versions

The source merger table is `merger_case_audit.csv`, with 2,608 rows, SHA-256 `b15414beee6a0cb267b2f719e4d95826073b1b97b396b89d7f063df6d6ba1331`. The source penalty table is `penalty_audit.csv`, with 57 announcement rows representing 249 attachment records, SHA-256 `5cc824cbaee6a9ea8b35c7b8ba3afc6311cc23eb478715bb8c3d106022f026f8`.

Both were supplied with coding summaries and scripts. They originate from SAMR notices and penalty decisions and contain automated rules and recorded manual amendments. Selection flags do not prove completion of independent review. Penalty source URLs are retained. Merger notice URLs must be restored from the source collection before a final research release. No source document text is included in this small CSV.

## Unit and coverage

One row is a source record, not yet a verified unique antitrust case. `source_record_id` and `sample_type` identify the source. `case_id` and `case_family_id` remain blank until a proceeding-level crosswalk is checked. The full merger `receiveTime` range is August 18, 2022 to November 11, 2026. Recorded penalty announcement dates span May 7, 2024 to September 28, 2026; exact observed decision dates span January 17, 2022 to July 25, 2026, with one additional decision known only by month. These clocks are not equivalent. No claim of nationally complete enforcement coverage is made.

## Preparation

`combined_pilot.py` preserves original flags and dates, recognizes NA tokens, and constructs consistent columns. An ownership status of `positive` maps to verified-candidate 1; `negative_all_parties_evidenced` maps to 0; absence of positive evidence maps to missing. These remain candidates for independent checking. The raw missing-fine-to-zero rule is retained as `is_large_fine_raw`; `is_large_fine_observed` is blank for missing/inapplicable fines. Amount units follow the supplied coding rules (CNY 10,000), subject to validation. Fines are not merger values.

The sample takes the 20 lowest SHA-256 hashes of `pilot-v2|sample_type|source_record_id` within each type. This balanced demonstration release is not a probability sample for population coverage rates and must not replace the full research sample for regression. The 40-row release and 2,665-row aligned candidate table can both be reproduced locally.

## Variables and missingness

See `CODEBOOK.md`. Load IDs as strings. `date_raw_type` identifies the source clock. `publication_date_verified`, case IDs, `media_post_30`, same-day and prior-media fields are blank. `search_complete=0`, `date_verified=0` and `case_identity_verified=0` mark unfinished verification. Unknown never means a negative media outcome. News matching requires aliases, a fixed outlet universe, retrieval logs and explicit case-link adjudication.

## Access and reuse

Review preview. External redistribution permissions and the appropriate dataset license remain to be verified; no open-content license is asserted. Publish only approved derived metadata. Wisenews full text, Faxin judgments and raw penalty decisions are excluded. Database access does not establish redistribution rights. Before publication, identify the approved terms, restore source URLs and confirm reviewer access.

## Validation and known limitations

There are 0 recorded media labels across both source tables. Among merger records, 675 main industries are unclassified and only 15 transaction amounts are present. Among penalties, 56 fines are present and 1 is missing. Twenty-five penalty records share 2024-05-07 as their recorded announcement date; the median recorded announcement-decision gap is 226.5 days across 56 complete date pairs. This establishes neither a true disclosure delay nor a website migration. Verify original releases before assigning t0.

No logit has been estimated. Repeated merger titles are review candidates, not automatic duplicates. Independently recode a stratified sample of at least 10% of final case-news matches, including negative and uncertain labels, report disagreement and precision/recall against adjudicated matches, and verify ownership absences. The existing 261 merger and 6 penalty review flags indicate selection only.

## Reproducibility links

Course Hugging Face namespace: `DKU-STATS201-Autumn2026`. Exact dataset repository and commit remain pending.

Course GitHub repository: https://github.com/STATS201-Autumn2026/Gloria. Record the full checked-out commit SHA with `git rev-parse HEAD`.

Add the exact Hugging Face dataset URL and revision when it is published. Source digests above identify the input snapshots; they are not Git commit IDs.
