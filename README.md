# The HRIS Copilot Kit

Ready-to-use AI shortcuts for HRIS and HR technology teams, built from 19 years of running Oracle HCM Cloud and Workday in production.

Each item solves one recurring HRIS job: triaging release notes, checking a vendor's AI feature, preparing a migration, writing test scripts. Download it, load it into Claude (or adapt it for another assistant), and use it the same day.

New items arrive with each issue of **The HR Tech Insider** newsletter by Ramprasad Reddy Mittana. Every item links to the issue that explains the problem behind it.

## What's in the kit

| Type | What it is | How to use it |
|---|---|---|
| **Skill** | A packaged procedure Claude follows whenever the task comes up | Download the zip, then upload it in Claude under Settings > Capabilities > Skills |
| **Prompt card** | One tested prompt with the inputs to paste in | Open `prompt.md`, copy the prompt, fill the brackets |
| **Project template** | Instructions plus reference files for one ongoing job | Create a Claude Project, paste `instructions.md`, upload the files |
| **Tool** | A small calculator or checker | Follow the item's README |

## Catalog

<!-- catalog:start -->
| Item | Type | Platforms | Introduced in | Download |
|---|---|---|---|---|
| **[Release Note Triage](kit/skills/release-note-triage)**<br>Turns an Oracle HCM or Workday release into an impact table, a regression test plan, opt-in decisions and a note for HR. | Skill | Oracle HCM Cloud, Workday | Coming soon | [zip](https://github.com/rampreddym/hris-copilot-kit/releases/latest/download/release-note-triage.zip) |
| **[AI Feature Governance Check](kit/prompts/ai-feature-governance-check)**<br>Decides whether to enable, pilot or decline a vendor's AI feature, with a risk rating and ten questions for the vendor. | Prompt card | Oracle HCM Cloud, Workday, Any HR system | Coming soon | [zip](https://github.com/rampreddym/hris-copilot-kit/releases/latest/download/ai-feature-governance-check.zip) |
<!-- catalog:end -->

**Download everything:** [hris-copilot-kit.zip](https://github.com/rampreddym/hris-copilot-kit/releases/latest/download/hris-copilot-kit.zip)

## Use it safely

- **Never paste real employee data** into an AI tool your company hasn't approved. Every item here works on configuration, release notes, logs or synthetic data.
- **Check your company's AI policy** before using any item at work.
- **Review the output.** These shortcuts speed up expert work; they don't replace the expert's sign-off.

## Request a shortcut

Have an HRIS task that eats your week? [Open a request](../../issues/new?template=shortcut-request.md).

## License

Content (skills, prompts, guides) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use and adapt it freely, with credit. Scripts are MIT licensed. See [LICENSE](LICENSE).

Not affiliated with or endorsed by Oracle, Workday, Microsoft or Anthropic. Product names are trademarks of their owners.
