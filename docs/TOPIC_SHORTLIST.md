# Topic shortlist

Historical shortlist, superseded by the student's selection of the screen-time study on 17 October 2026. See `STUDY_PROTOCOL.md` for the selected project. The recommendations below describe the earlier selection stage.

Publisher pages checked on 17 October 2026. Counts below are publisher-reported observations, not independently verified counts from downloaded files. All four pages identify CC BY 4.0 licensing; retain source attribution if any are used in future work.

## 1. Complaints and later telecom churn — recommended overall

[UCI Iranian Churn](https://archive.ics.uci.edu/dataset/563/iranian+churn+dataset) · [DOI](https://doi.org/10.24432/C5JW3Z)

- 3,150 observations; one row represents a customer of an Iranian telecom company.
- Includes complaint status, call failures, usage, subscription length, tariff and churn. Predictor measurements aggregate the first nine months; churn is recorded at month 12.
- Question: Is complaint status associated with later customer churn?
- Proposed CDA: chi-square independence on complaint × churn counts, subject to expected-count and independence checks. Report group churn rates and their difference. Consider Fisher's exact test if a 2×2 table is sparse.
- Limit: one company's observational sample cannot establish that complaints cause churn.

## 2. Grain shape in two rice varieties — distinctive subject

[UCI Rice (Cammeo and Osmancik)](https://archive.ics.uci.edu/dataset/545/rice+cammeo+and+osmancik) · [DOI](https://doi.org/10.24432/C5MW4Z)

- 3,810 observations; one row is a grain measured from an image, with seven shape features and its variety label.
- Question: Does mean major-axis length differ between the two varieties?
- Proposed CDA: Welch independent two-sample t-test, after checking distributions and whether the collection design supports independence. Show a mean difference with a confidence interval.
- Optional EDA: area/perimeter correlation; PCA only if it adds a useful explanation.
- Limits: image-based measurements require unit checking; grains from shared batches may be dependent. Inspect collection details before generalizing to varieties broadly.

## 3. Visitor type and online purchases — accessible business story

[UCI Online Shoppers Purchasing Intention](https://www.archive.ics.uci.edu/dataset/468/online%20shoppers%20purchasing%20intention%20dataset) · [DOI](https://doi.org/10.24432/C5F88Q)

- 12,330 sessions, selected so each belongs to a different user.
- Contains visitor type, browsing activity, timing and a purchase indicator.
- Question: Is visitor type associated with whether a session ends in a purchase?
- Proposed CDA: chi-square independence; inspect category sizes and expected counts first.
- EDA: conversion proportions, visit durations and page counts.
- Limits: categories may be unbalanced; purchase is not revenue amount. Any predictive extension must assess when variables become available and avoid outcome leakage.

## 4. Weather and public-bike demand — strong visual potential

[UCI Seoul Bike Sharing Demand](https://archive.ics.uci.edu/dataset/560/seoul+bike+sharing+demand) · [DOI](https://doi.org/10.24432/C5F62R)

- 8,760 observations; one row is an hour with bike rentals, weather and calendar information.
- Question: How does rental demand vary with rain and season?
- EDA: hourly profiles, weather relationships and seasonal distributions.
- CDA needs a dependence-aware design. Consecutive hours are not automatically independent; daily aggregation alone does not solve serial dependence. Ordinary t-tests or ANOVA require additional justification.
- Limits: season, time and operating status can confound comparisons. This is the most involved option for a short report.

## Choice guidance

Choose telecom for a manageable, interpretable EDA/CDA project. Choose rice if an unusual subject and a numeric mean comparison are more appealing. Choose online shopping for an intuitive digital-business question. Choose bikes if willing to spend more time on temporal dependence.

These are proposed questions and methods, not findings. We will validate the selected data and design before committing to a test.
