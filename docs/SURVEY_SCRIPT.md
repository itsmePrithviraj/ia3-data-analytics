# Single survey form — ready to copy
**Title:** B.Tech Smartphone Usage Study

**Description:** We are conducting a Data Analytics course project about how B.Tech students estimate smartphone use. Please first estimate your usage, then check your phone's report for the same seven completed days. Participation is voluntary. We do not ask for your name, email, college or contact details. Individual responses will be kept by the project team for analysis; the course report will present aggregated results. You can stop before submitting. Because we do not collect an identifying code, we may be unable to locate your response for withdrawal after submission.

## Settings and flow
Use one form with sections. Turn off email collection, public response summaries and response editing after submission. Avoid sign-in requirements where possible; the form itself should not ask for an identifier. Do not enable a sign-in-based one-response restriction without reconsidering the participation wording.

A section break is an instruction aid, not a technical lock against going back. Do not claim that it prevents estimate editing. No form has been created or invitations sent automatically.

## Section 1 — participation
Use required Yes / No multiple choice. Branch No to the end, without proceeding to usage questions.
1. **Do you voluntarily agree to participate in this course project?** → `consent`
2. **Are you currently enrolled in a B.Tech programme?** → `btech_enrolled`
3. **Is this your first response to this study, including any pilot or trial response?** → `first_response`

## Section 2 — estimate before checking
Instruction: **Do not open Screen Time or Digital Wellbeing yet. Think about your own primary smartphone, including all activities counted by its usage report, during the seven completed days ending yesterday. Exclude tablets, laptops and other phones.**

4. **What was yesterday's date?** → `reference_end_date`
   Required short answer in YYYY-MM-DD. This is the final day of your reference period. Example: when the last day is 2026-10-17, the first is 2026-10-11.
5. **Before checking your phone's report, what do you estimate your average DAILY screen time was during those seven days?** → `estimated_daily_time`
   Required short answer: duration in H:MM. It is a daily average, not a weekly total or a clock time. Use hours and minutes, not decimal hours. Do not revise this estimate after checking.

The date example is illustrative; use yesterday on the actual day of responding. Do not put a suggested screen-time estimate into the question.

## Section 3 — phone-recorded daily totals
Now open the phone report. Record each completed date, oldest first. Count only this same primary phone. Enter durations as H:MM: for example, 1 hour 5 minutes is 1:05; 50 minutes is 0:50. These examples explain units, not typical usage.

- **iPhone:** Settings → Screen Time → See All App & Website Activity. Select this iPhone under Devices, use the daily view and navigate to the required dates. Do not copy an All Devices total.
- **Android:** Settings → Digital Wellbeing & parental controls → usage chart/dashboard. Navigate to the completed daily totals. Labels and history navigation vary by manufacturer.
- If the report cannot show the required history, do not invent a value. Leave that day blank and select No/Not sure for the final scope check.

6–12. Seven short-answer questions:
| Question | CSV heading |
|---|---|
| Day 1: screen time six days before your reference end date | day_1_time |
| Day 2: screen time five days before your reference end date | day_2_time |
| Day 3: screen time four days before your reference end date | day_3_time |
| Day 4: screen time three days before your reference end date | day_4_time |
| Day 5: screen time two days before your reference end date | day_5_time |
| Day 6: screen time one day before your reference end date | day_6_time |
| Day 7: screen time on your reference end date (yesterday) | day_7_time |

Allow blank daily entries so missing history is distinguishable from zero. The analysis excludes incomplete weeks and explains why. A genuine zero is 0:00. Do not request screenshots.

Optional short-answer pattern validation for estimate and nonblank daily values:
```text
^([01]?[0-9]|2[0-3]):[0-5][0-9]$|^24:00$
```
Use “matches” and the help message “Enter a duration from 0:00 to 24:00 in hours:minutes.” The Python importer also validates all durations.

## Section 4 — final checks
Required multiple choice: Yes / No / Not sure.
13. **Did you enter your estimate before viewing the phone's usage report today, and leave that estimate unchanged after checking?** → `estimate_before_check`
14. **Did you transcribe all seven correct completed dates from the same primary smartphone that you personally used throughout, without shared-phone use, a phone change, or combined-device totals?** → `record_scope_confirmed`

Only Yes to both is included in the primary analysis. An honest No is preferable to guessing.

## Invitation draft
> Hi! We are doing a B.Tech Data Analytics course project on estimated and phone-recorded smartphone use. If you are a B.Tech student and haven't already taken part, please fill this short form. You will need seven completed days of usage history on your primary phone. Please enter your estimate before opening the usage report. We don't ask for your name, email or college. Participation is voluntary. [Insert form link]

This draft is not sent automatically. Pilot the instructions first, especially access to older daily records.

## Export
Participants never enter IDs. Use the CSV headings shown above, or map the form's full question titles in `config/real.json`. See [real data guide](REAL_DATA_GUIDE.md). The template has headers only; every row will represent one response.

Official device guidance: [Apple Screen Time](https://support.apple.com/en-gb/guide/iphone/iphbfa595995/ios), [Google Digital Wellbeing](https://support.google.com/android/answer/9346420?hl=en-IN).
