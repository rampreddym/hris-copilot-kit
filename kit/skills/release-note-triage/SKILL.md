---
name: release-note-triage
description: Triage Oracle HCM Cloud or Workday release notes against an organization's HRIS configuration. Use when an HRIS or HR technology team pastes or attaches quarterly or biannual release notes, a "what's new" document, readiness material or a feature list and wants to know what affects them, what to regression test, which opt-in features to switch on, which AI features need a governance review, and what to tell HR.
---

# Release Note Triage

Turn a vendor release into decisions: what changes for us, what we test, what we switch on, and who needs to know.

## Inputs

1. **Release notes.** Pasted text, an attached PDF or spreadsheet, or a feature list.
2. **Configuration profile.** Modules live, countries, integrations, notable customizations, security model. A template is in `profile-template.md`. If no profile is given, ask for it once. If the user wants to proceed anyway, mark every applicability judgment "Confirm" rather than guessing.
3. **Calendar (optional).** Upcoming events such as open enrollment, year-end, a compensation cycle or a go-live, so release timing collisions can be flagged.

## Procedure

1. **Inventory.** Turn every feature in the notes into a row: module, feature name exactly as written, and delivery mode. Use the vendor's own labels for delivery mode and map them to one of: *On by default*, *Opt-in*, *Needs setup*, *Deprecation or removal*.
2. **Applicability.** Compare each row to the profile. A feature in a module the organization does not use is *Not applicable*. If the profile doesn't say, mark *Confirm*.
3. **Impact rating.** Rate applicable rows:
   - **High:** on-by-default change to a live module that touches pay, absence balances, security or role access, integrations, web services or APIs, or employee-facing screens; any deprecation of something in use.
   - **Medium:** on-by-default change to back-office screens or reports; opt-in features with clear value.
   - **Low:** cosmetic changes, documentation, opt-in features with no current need.
4. **AI features.** List separately every feature that uses generative AI, machine learning or recommendations. For each, record whether it is on by default, what employee data it appears to use, and whether it influences decisions about people. Recommend a governance review before enabling any that do.
5. **Deprecations.** List removed or deprecated features with their stated dates and the replacement, if named.
6. **Timing.** If a calendar was provided, flag releases that land within two weeks of a critical event.

## Output

Produce these sections in order:

1. **CHRO summary.** No more than three sentences: how many high-impact changes, the one decision leadership needs to make, and the biggest risk.
2. **Impact table.** Feature | Module | Delivery mode | Applies? | Impact | Why it matters here | Action | Suggested owner. Sort High first. Omit *Not applicable* rows from the table and give their count in one line.
3. **Regression test plan.** For every High and Medium row: test case, steps, expected result. Order by risk: integrations and payroll first, then security, then employee-facing, then the rest.
4. **Opt-in recommendations.** Switch on now / Evaluate in a test environment / Leave off, each with a one-line reason.
5. **AI features needing review.** The list from step 4.
6. **Deprecations.** The list from step 5.
7. **HR communication draft.** A short note to HR business partners about changes employees or managers will see. Plain language, no product jargon.
8. **Questions for the vendor.** Anything the notes leave unclear.

## Rules

- Quote feature names exactly as they appear in the notes. Never describe behavior the notes don't state; list it under questions for the vendor.
- Never assume a module is live. Use *Confirm* when the profile is silent.
- This task never needs employee personal data. Do not ask for it, and if some appears in the inputs, don't repeat it.
- If the notes are too long to cover in one pass, work module by module, say which modules are done, and offer to continue.
