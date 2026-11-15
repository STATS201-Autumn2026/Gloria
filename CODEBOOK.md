# Codebook

## Fields present in the aligned metadata pilot

| Field | Rule |
| --- | --- |
| source_record_id, sample_type | Original source identifier and merger/penalty type; together unique within the source snapshots. |
| case_id, case_family_id, case_identity_verified | Case linkage fields; IDs blank and verification 0 until reviewed. |
| case_title, source_url | Original title and penalty notice URL; merger URL restoration remains pending. |
| date_raw, date_raw_type | Unmodified receiveTime for mergers or announcement_date for penalties. |
| decision_date_raw | Penalty signed date, when available. |
| publication_date_verified, date_verified | Blank date and flag 0 until first official release is verified. |
| primary_industry_raw, primary_industry | Raw coding and candidate aligned coding, with unclassified industry blank in the latter. |
| has_platform_firm_raw, has_SOE_raw, has_foreign_firm_raw | Original 0/1 coding, where 0 may only mean no positive evidence. |
| corresponding evidence_status fields | Original positive, no_positive_evidence or negative_all_parties_evidenced status. |
| corresponding verified_candidate fields | 1 for positive evidence, 0 for all-party negative evidence, blank otherwise; still subject to independent review. |
| violation_type, merger_structure | Type-specific coding; inapplicable fields blank. |
| fine_amount_wan, fine_observed_subtotal_wan | Source penalty total and verified subtotal, in CNY 10,000. Incomplete totals stay missing. |
| is_large_fine_raw, is_large_fine_observed | Preserve the original rule; the observed-only version is missing for missing/inapplicable fines. |
| deal_value_wan_raw, deal_value_status | Recorded merger value in CNY 10,000 and evidence type; comparability must be checked. |
| law_period_raw | Penalty decision calendar-period indicator, not an exogenous instrument or validated law-applicability measure. |
| media_report_raw | Original label if known; blank for all supplied cases. |
| media_post_30, media_same_day, prior_case_media_90 | Empty until case-specific Wisenews searches and time windows are verified. |
| search_complete, window_complete | Search flag 0; full-window flag blank until news coverage is checked. |
| source_review_sample_flag | Existing review selection flag; does not establish review completion. |

## Additional fields for the final merged study

| Field | Coding rule |
| --- | --- |
| investigation_start_date, decision_date, publication_date | Distinct dates with source citations and confidence flags. Do not replace a missing investigation date with the decision date. |
| preinvestigation_media_90 | Case-specific coverage in the 90 calendar days strictly before confirmed investigation start. Only applicable to the enforcement-direction extension. |
| prior_case_media_90 | Case-specific coverage in days -90 to -1 before t0; timing descriptor, not proof of pre-investigation coverage. |
| media_same_day | Day-0 reporting retained separately because ordering within the day may be unknown. |
| firm_visibility_pre | Non-case firm mentions before t0, measured over a fixed period; distinguish this from case-specific reporting. |
| violation_type | Penalties only: monopoly_agreement, abuse_of_dominance, unlawful_concentration, other. Use the principal legal basis; document tie-breaking for multiple violations. Missing/not applicable for ordinary merger notifications. |
| fine_amount_wan | Case-level sum of nonduplicated monetary fines in CNY 10,000. Keep confiscated gains separate. Explicit 'each' amounts must be multiplied by the named penalized parties. Missing is not zero. |
| is_large_fine | Optional penalty-only sensitivity: strictly above observed penalty-case median = 1, at/below = 0, unknown = missing; calculate the median on training data for prediction. Prefer continuous log(1+fine_amount_wan) if measurement supports it. |
| penalty_missing | Separately flag a missing penalty amount where the variable is applicable. |
| official_prominence | Presence of a press briefing or prominent release recorded at t0. Potential mechanism variable; do not mechanically control it away in every model. |
| litigation_pre_t0 | Case-related litigation verified to predate t0; later Faxin litigation is a possible outcome or mechanism, not a baseline control. |
| search_log | Query strings, firm aliases, time span, outlet universe, retrieval date, candidate IDs and match decisions. Keep licensed full text outside public repositories. |

Parent-company and ultimate-controller rules must be the same in both case types. Preserve the supplied foreign-involvement rule, including Hong Kong, Macao and Taiwan and its exclusion of mainland-controlled offshore vehicles based solely on location. Report a control-based sensitivity analysis. The SOE flag covers Chinese state control; foreign state firms do not automatically qualify. Align industries using the same existing taxonomy; code the affected market or transaction target rather than automatically assigning the diversified parent's industry.
