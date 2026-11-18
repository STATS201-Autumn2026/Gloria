"""Rebuild the course dataset and audit from the pinned upstream TSV.

Packaging changes: normalized headers, stable IDs, explicit tie handling,
duplicate groups, and score-derived association labels. No summaries are edited.
Run with Python 3.10+; standard library only.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'source' / 'weibo_cluster_summaries.tsv'
COMMIT = 'f82076dc0c94498dfa88f8d387412b6b424a1c66'
BLOB = '233205a73674a0b9470eb6131f0d300f4312876c'
COUNTRIES = ['China', 'US', 'Russia', 'Ukraine']
SCORE_COLUMNS = ['China-based Domains PMI', 'US-based Domains PMI',
                 'Russian-based Domains PMI', 'Ukrainian-based Domains PMI']


def main():
    raw = SOURCE.read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if blob != BLOB:
        raise ValueError(f'Upstream TSV bytes do not match the pinned version: {blob}')
    with SOURCE.open(encoding='utf-8', newline='') as f:
        source_rows = list(csv.DictReader(f, delimiter='\t'))
    output = []
    summary_counts = Counter()
    labels = Counter()
    for i, row in enumerate(source_rows, start=1):
        if set(row) != {'Number of Weibos', 'Weibo Cluster Summary', *SCORE_COLUMNS}:
            raise ValueError(f'Unexpected columns at source row {i}')
        if any(row[k] is None or not row[k].strip() for k in row):
            raise ValueError(f'Missing field at source row {i}')
        scores = [float(row[k]) for k in SCORE_COLUMNS]
        text = row['Weibo Cluster Summary']
        summary_key = hashlib.sha256(text.strip().lower().encode()).hexdigest()
        summary_counts[summary_key] += 1
        winners = [c for c, score in zip(COUNTRIES, scores) if score == max(scores)]
        label = winners[0] if len(winners) == 1 else 'ambiguous'
        labels[label] += 1
        ranking = sorted(scores, reverse=True)
        output.append({
            'record_id': f'weibo_summary_{i:04d}',
            'source_row': i,
            'summary': text,
            'n_weibo': int(row['Number of Weibos']),
            'pmi_china': row[SCORE_COLUMNS[0]],
            'pmi_us': row[SCORE_COLUMNS[1]],
            'pmi_russia': row[SCORE_COLUMNS[2]],
            'pmi_ukraine': row[SCORE_COLUMNS[3]],
            'highest_score_ecosystem': label,
            'exact_tie': len(winners) > 1,
            'tied_ecosystems': '|'.join(winners) if len(winners) > 1 else '',
            'score_margin': ranking[0] - ranking[1],
            'summary_group_id': summary_key,
        })
    for row in output:
        row['duplicate_summary_count'] = summary_counts[row['summary_group_id']]
    dest = ROOT / 'data' / 'narrative_summaries.csv'
    dest.parent.mkdir(exist_ok=True)
    with dest.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)
    n_unique_max = len(output) - labels['ambiguous']
    audit = {
        'package_version': '1.0.0',
        'prepared_date': '2026-11-18',
        'upstream_repository': 'https://github.com/hanshanley/narrative-influence',
        'upstream_commit': COMMIT,
        'upstream_git_blob_sha1': blob,
        'upstream_sha256': hashlib.sha256(raw).hexdigest(),
        'processed_csv_sha256': hashlib.sha256(dest.read_bytes()).hexdigest(),
        'row_count': len(output),
        'missing_required_source_fields': 0,
        'unique_normalized_summaries': len(summary_counts),
        'duplicate_summary_groups': sum(v > 1 for v in summary_counts.values()),
        'exact_ties_for_highest_score': labels['ambiguous'],
        'score_margin_below_0_01_including_ties': sum(r['score_margin'] < 0.01 for r in output),
        'label_counts_including_ambiguous': dict(labels),
        'unique_maximum_rows': n_unique_max,
        'shares_percent_among_unique_maximum_rows': {
            c: round(100 * labels[c] / n_unique_max, 4) for c in COUNTRIES
        },
        'published_table_1_analysis_2_percent': {
            'China': 9.7, 'US': 18.3, 'Russia': 37.1, 'Ukraine': 35.0
        },
        'discrepancy_status': 'Unresolved. Public-release selection and score normalization may matter; no cause established.',
        'model_training_performed': False,
        'split_policy': 'One full split only; no train/test assignment has been made.'
    }
    (ROOT / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(audit, indent=2))


if __name__ == '__main__':
    main()
