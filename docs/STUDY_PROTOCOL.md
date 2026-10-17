# Study protocol — draft v0.1, 17 October 2026

## Question and scope

Working title: **The Screen-Time Blind Spot: Estimated versus Phone-Recorded Screen Time among B.Tech Students**.

Primary question: Does the mean difference between phone-recorded and estimated average daily screen time differ from zero among the students recruited for this study?

Secondary descriptive questions: How large are individual absolute errors? What proportions underestimate, overestimate or closely match their records? How are estimated and recorded values related?

This is a cross-sectional paired measurement study, not an experiment or a before/after intervention. The device reference is transcribed by the participant. It is not an independent audit, a measure of all digital activity, or a diagnosis of addiction. We are not collecting GPA, health outcomes, private app lists or browsing histories.

## Population, observation and sample

- Intended population of interest: currently enrolled B.Tech students, from any college.
- Accessible sample: volunteer classmates and friends recruited through the team and their contacts. Describe it as convenience/referral sampling.
- Observation: one student with one estimate and one matching seven-day phone-recorded average.
- Target 100 valid pairs; practical minimum goal 60 valid pairs, comfortably above the student's 40–50 preference. These are feasibility targets, not a formal power calculation or guaranteed precision.
- Seek students from different colleges and study years where feasible; do not claim national representativeness or force artificial quotas after seeing results.
- Five pilot volunteers test usability, preferably including Android and iPhone. Exclude pilot records from the main analysis. Do not ask pilot participants to enter the main study again.
- Proposed collection cutoff: 23 October 2026, 21:00 IST, or 100 valid pairs, whichever comes first. Audit completeness during collection but do not inspect p-values to decide when to stop. If too few valid responses exist, report the shortfall and agree any extension before running inference.
- Suggested schedule: 17–18 Oct protocol/pilot/form setup; 18–23 Oct collection after protocol freeze; 24 Oct cleaning and EDA; 25 Oct CDA/report; 26 Oct final verification and submission by the student/team.

## Measurement window

Use the seven completed calendar days ending yesterday, relative to the date Part A is submitted in the participant's local calendar. Record that date and use the same window in Part B, even if Part B is completed later. Prefer completing both on the same day.

Example: Part A completed on 20 October covers 13–19 October inclusive. Today's partial usage is excluded. Use the student's primary smartphone only, for both estimate and records, including study and leisure use on that phone. Exclude laptops, tablets and secondary phones. Select the particular iPhone in Screen Time if reports combine devices.

Collect seven separate daily totals and calculate their mean in Python. This avoids mixing a partial current-week average, a previous calendar week and a rolling seven-day average. If any daily record is unavailable, do not guess it or replace it with zero. A weekly total is not substituted under this draft protocol.

## Prevent the estimate from being changed after checking

Use two short forms linked by a participant code. Part A saves the estimate; its submission confirmation links to Part B, where the participant opens the phone report. Disable editing submitted Part A responses. A single form split into sections usually still permits back-navigation, so it does not enforce this ordering by itself.

Each volunteer receives a unique non-identifying code from a shared team list (e.g. ST001). Assign codes once; do not store a code-to-name or code-to-phone-number list in the research dataset. The participant re-enters the same code in Part B. Invite each person only once; ask whether they have already participated. This does not prove anonymity against every possible linkage or prevent every duplicate; describe the actual collection method honestly.

Record whether a participant has already viewed a screen-time report covering any target days on the day of their estimate. Mark yes/unsure responses as pre-exposed; exclude them from the primary unprompted-estimation analysis and report their count. Earlier habitual checking is measured separately as optional context.

## Raw variable dictionary

| Field | Type / allowed values | Source and purpose |
|---|---|---|
| participant_id | Nominal ID, ST followed by digits | Join forms; never a numerical predictor |
| protocol_version | Text | Added by team, version used in collection |
| pilot | Boolean | Added by team; pilot records excluded |
| consent | Yes/No | Permission for coursework use and aggregate reporting |
| btech_enrolled | Yes/No | Eligibility |
| already_participated | Yes/No | Prevent repeated participation |
| estimate_date | Date, YYYY-MM-DD | Participant-local date, establishes window |
| part_a_timestamp | Timestamp | Automatic form export; preserve timezone metadata |
| study_year | Ordinal: 1/2/3/4/5+ | Descriptive sample profile |
| college_code | Nominal code or undisclosed | Optional, supplied by team; aggregate sample description |
| phone_os | Android/iOS/Other | Measurement context |
| checked_report_today | No/Yes/Unsure | Detect pre-exposure before estimate |
| estimated_hours | Integer 0–24 | Estimated daily average, hours component |
| estimated_minutes | Integer 0–59 | Estimated daily average, minutes component |
| checking_frequency | Never/Less than weekly/Weekly/Daily/Prefer not to say | Optional usual checking habit, descriptive only |
| part_b_timestamp | Timestamp | Confirm record entry followed estimate submission |
| reference_end_date | Date | Must equal estimate_date minus one day |
| recording_source | Android Digital Wellbeing/iPhone Screen Time/Other | Record measurement source; other method needs review |
| records_complete | Yes/No/Unsure | Whether all seven completed days are available |
| primary_phone_only | Yes/No/Unsure | Scope check: same phone, no combined device report |
| personally_used_same_phone | Yes/No/Unsure | Own primary phone throughout window, not shared/switched |
| d1_time ... d7_time | HH:MM strings | d1 = yesterday; d7 = seven days before estimate date |
| transcribed_from_report | Yes/No | Confirmation records were read, not guessed |

Hours/minutes must total between 0 and 1,440 per day. 24:00 is the only permitted time with hour 24. Zero may be real; unusual values are reviewed, not automatically replaced. No names, email addresses, registration numbers, screenshots or exact birth dates are requested. Disable email collection in form settings.

## Derived analysis variables

| Field | Definition |
|---|---|
| estimated_daily_minutes | 60 × estimated_hours + estimated_minutes |
| recorded_daily_minutes | Sum of seven converted daily totals / 7 |
| signed_error_minutes | recorded_daily_minutes − estimated_daily_minutes |
| absolute_error_minutes | Absolute value of signed_error_minutes |
| perception_group | Underestimate if error > 30; within 30 minutes if abs(error) ≤ 30; overestimate if error < −30 |
| inclusion_primary | Whether all prespecified primary-analysis criteria are satisfied |
| exclusion_reasons | All reasons a submitted pair is not included |

The 30-minute tolerance is a project-defined descriptive convention, not a validated clinical threshold. Preserve unrounded minutes for calculations; round only displayed results.

## Data custody and reproducibility

Keep original form exports unchanged locally. Derive a cleaned analysis file and an exclusions log. Two form exports are administrative inputs to one participant-level dataset. With 100 students and 700 daily entries, the primary test still has n = 100 paired observations.

Restrict raw form/export access to the project team and instructor as required. Publish code, methods and aggregate results in the private repository; do not automatically commit participant-level records. No data are collected or sent by this draft.

## Device references checked 17 October 2026

- [Apple: view Screen Time and select a device](https://support.apple.com/en-gb/guide/iphone/iphbfa595995/ios).
- [Google: Digital Wellbeing and screen-time charts](https://support.google.com/android/answer/9346420?hl=en-IN).

Interfaces vary. The pilot must confirm access to each previous day's total on the actual phones used. Enabling a tracker today cannot be assumed to recreate past usage.
