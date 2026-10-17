# Survey script — draft v0.1

This is ready-to-copy wording for discussion and pilot, not a deployed form. Keep the participant-facing title neutral; do not say that students underestimate usage before they respond. Test completion time in the pilot before quoting one in invitations.

## Invitation draft

> Hi! We are doing a Data Analytics coursework project about how B.Tech students estimate their smartphone use. Students from any college can participate. You will first estimate your average daily use, then check seven completed days in your phone's usage report. Please do not open that report before Part A. Participation is voluntary, and we do not ask for your name, email, registration number, app list or screenshots. Please participate only once. Your participant code is [CODE]. Start here: [PART A LINK].

Do not send this automatically. Share after pilot and protocol freeze. Supply one unique code to each person; the team keeps only the code's issued/used status, without a name/contact mapping in the dataset.

## Form settings

- Title: **B.Tech Student Smartphone Usage Study — Part A: Estimate**.
- Turn off email collection; do not request file uploads.
- No response summaries visible to participants.
- Disable editing after Part A submission.
- If sign-in is enabled for any reason, disclose it and do not promise fully anonymous collection. Prefer a configuration that does not require sign-in for this study.
- Keep separate Part A and Part B response exports; match by participant code.
- Use branch-to-end for nonconsent, not enrolled or already participated; do not request their usage details.
- Use form instructions rather than prefilled example answers that could anchor estimates.
- Mark optional questions explicitly. Preserve missing responses as missing.

## Part A: answer without opening the usage report

Intro:

> This coursework study compares an estimate with the screen time displayed by your primary smartphone. It covers the seven completed days ending yesterday. Include all use on that phone, including study and leisure; exclude other phones, tablets and computers. Results will be reported in aggregate. Participation is voluntary. You may stop before submitting. The project team and instructor may see the research data. We do not request direct identifiers. Keep your participant code to match the two parts; it can also identify your response if you contact the team before analysis is finalised. Please submit your estimate before checking your usage report.

Questions, in order:

1. **Do you voluntarily agree to take part and allow your answers to be used for this coursework study and its aggregate report?** Required choice: Yes / No. No → end.
2. **Are you currently enrolled in a B.Tech programme?** Required: Yes / No. No → end.
3. **Have you already participated in this study, including its pilot?** Required: Yes / No. Yes → end.
4. **Enter the participant code supplied with your invitation.** Required short text.
5. **What is today's date where you are?** Required date. This fixes the seven-day reference window.
6. **Which year of B.Tech are you currently in?** Required: 1 / 2 / 3 / 4 / 5 or above.
7. **College code, if supplied with your invitation.** Optional short text; allow undisclosed. Do not enter a personal registration number.
8. **Which operating system does your primary smartphone use?** Required: Android / iOS (iPhone) / Other.
9. **Before answering this form today, have you looked at a phone screen-time report showing any of the previous seven completed days?** Required: No / Yes / Not sure. Keep the answer; do not tell respondents which is preferred.
10. **Without opening your usage report now, estimate your average screen time per day on your primary smartphone over the seven completed days ending yesterday.** Two required numeric fields: Hours (0–24 integer); Additional minutes (0–59 integer). Explain that this is a daily average, not a seven-day total. Combined time must not exceed 24 hours.
11. **How often do you usually check your phone's screen-time report?** Optional: Never / Less than once a week / About weekly / Daily or almost daily / Prefer not to say.

Submission confirmation:

> Your estimate has now been saved. Please do not submit Part A again. Keep your participant code and the date you entered. Now open Part B: [LINK]. There you can check and enter your phone's recorded values. Use the seven days ending the day before your Part A date, even if you finish Part B later.

## Part B: read the recorded values

Title: **B.Tech Student Smartphone Usage Study — Part B: Phone Record**.

Intro:

> Complete Part A first. Now open your primary phone's usage report. Read the total screen time for each of the seven completed days in your reference window. Do not enter today's partial total or a combined report for several devices. If a record is unavailable, say so; do not guess. You do not need to send screenshots or app names.

Device guidance:

- Android: Settings → Digital Wellbeing (sometimes “Digital Wellbeing & parental controls”) → usage chart/dashboard. Find the dated daily screen-time totals. Menus differ between manufacturers; if previous days are unavailable, mark incomplete.
- iPhone: Settings → Screen Time → See All App & Website Activity → Devices → select this iPhone → Day; navigate to the required dates. Do not use “All Devices”.
- Use each date's total screen time, not a single app, battery usage or time since last charge.

Questions:

1. **Enter the same participant code used in Part A.** Required short text.
2. **Enter the last date of your reference period: the day before your Part A date.** Required date.
3. **Which report are you using?** Required: Android Digital Wellbeing / iPhone Screen Time / Other. For Other, optional description; team reviews compatibility before inclusion.
4. **Can you see a complete screen-time total for every one of the seven dates?** Required: Yes / No / Not sure. No/Not sure → submit incomplete response without forcing invented totals.
5. **Do these totals refer only to the same primary phone you estimated in Part A?** Required: Yes / No / Not sure. No/Not sure → end as scope not confirmed.
6. **Was this your personally used, unshared primary phone throughout all seven days, without switching to a replacement phone?** Required: Yes / No / Not sure. No/Not sure → end as scope not confirmed.
7. **Enter each daily total as hours:minutes, for example 2:07.** Seven required short-text fields. d1 = last date entered above; d2 = one day before d1; ...; d7 = six days before d1. If supported, show actual dates. Otherwise show the offsets explicitly and a clear calendar example unrelated to usage amounts. Accept 0:00–24:00, minute component 00–59, and only 24:00 when hours are 24.
8. **I copied these seven totals from the phone report rather than estimating them.** Required: Yes / No.

Final confirmation:

> Thank you. Your contribution is complete. Please do not submit another response. Keep your participant code in case you need to report a transcription mistake to the project team.

## Team pilot checklist

Try five volunteers before launching. Check Android/iPhone history access, date selection, time-entry format, correct single-device scope, saving Part A before viewing records, code matching and completion time. Ask which wording was confusing. Revise the draft once, record the revision and freeze the main-study questions. Pilot responses remain separate and are not reused.

## Export handoff

Export both forms as CSV; preserve originals in local `data/raw/`. Do not manually overwrite estimates with recorded values or delete problematic rows in the export. Record actual collection dates, questionnaire version and any protocol deviations. Bring both exports back to this project for joint validation and analysis.
