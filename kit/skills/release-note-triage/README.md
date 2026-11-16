# Release Note Triage

**What it does:** Reads an Oracle HCM Cloud or Workday release and tells you what changes for your configuration, what to regression test, which opt-in features to turn on, which AI features need a governance review, and what to tell HR.

**Install:** Download `release-note-triage.zip` from the [latest release](../../../../releases/latest) and upload it in Claude under Settings > Capabilities > Skills.

**Set up once:** Fill in `profile-template.md` with your configuration and keep it for every release.

**Try it:** Attach both files in `examples/` and ask: "Triage this release for us."

**You get:** a three-sentence CHRO summary, an impact table sorted by risk, a regression test plan, opt-in recommendations, a list of AI features needing review, deprecations, a draft note to HR business partners, and questions for the vendor.

**Data you need:** release notes and a configuration profile. No employee data.
