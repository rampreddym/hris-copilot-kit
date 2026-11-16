# AI Feature Governance Check

**Use it when:** a vendor release, demo or sales pitch asks you to turn on an AI feature in your HR system, and you need to decide whether to enable it, pilot it or leave it off.

**You need:** the vendor's description of the feature (release note, product page, demo notes) and a few facts about your organization. No employee data.

## The prompt

Copy everything in the box, then replace the [brackets].

```
You are an HR technology governance reviewer. Our HR system vendor wants us to enable the AI feature described below. Review it and produce the sections that follow, in order. Where the description doesn't give you a fact, do not assume it: add it to the vendor questions instead.

1. PLAIN-LANGUAGE SUMMARY: What the feature does, in three sentences a manager would understand.

2. DATA: Which employee data it appears to use. Whether data leaves our tenant or region. Whether our data trains the vendor's models. How long inputs and outputs are kept.

3. DECISION IMPACT: Does its output influence a decision about a person (hiring, pay, promotion, performance, scheduling, termination)? If yes, classify it as high-risk and list the kinds of legal obligations we should check with counsel for the countries below, such as bias audit, notice, consent or human review requirements. Name specific laws only if you are confident they apply, and tell us to verify their current status.

4. CONTROLS: Is it on by default? Can we limit it by country, population or role? Is there an audit log of AI suggestions and who accepted them? Can a human override every output? Can we switch it off without losing data?

5. RISK RATING: Low, Medium or High, with the two biggest reasons.

6. VENDOR QUESTIONS: The ten questions we must have answered in writing before enabling it, most important first.

7. RECOMMENDATION: Enable, Pilot with conditions, or Do not enable. If pilot, state the conditions and the success measure.

FEATURE DESCRIPTION:
[Paste the release note, product page text or demo notes]

OUR CONTEXT:
- HR system: [Oracle HCM Cloud / Workday / other]
- Countries where employees work: [list]
- Headcount: [approximate]
- Who would use the feature: [HR admins / managers / employees / candidates]
- Existing AI policy or committee: [yes, describe / no]
```

## What you get back
- A summary you can forward to your CHRO
- A risk rating with reasons
- The ten vendor questions to send before you commit
- A clear enable, pilot or decline recommendation

## Tips
- Run it once per feature, not once per release. Bundled features hide risk.
- Send the vendor questions in writing and keep the answers with your decision record.
- The legal section is a checklist for counsel, not legal advice.
