# The HRIS Copilot Kit: plan

## 1. Purpose

**Promise to practitioners:** ready-to-use AI shortcuts for the HRIS jobs nobody else builds tools for, made by someone who has run Oracle HCM Cloud and Workday in production for 19 years.

**What it does for the brand:**
- Gives every newsletter issue something to download, which is what makes people subscribe and share.
- Turns expertise into a public, growing body of work that recruiters, conference organizers and clients can see.
- Shows the method behind the consulting offer: the free kit is generic; paid work tailors it to a client's configuration.

## 2. Name check before launch

"Copilot" is the name of Microsoft's AI assistant products. Using it in a product name could confuse people or draw a trademark objection. Decide before the first public release:

| Option | Note |
|---|---|
| The HRIS Copilot Kit | Strong recognition; trademark risk |
| The HRIS AI Kit | Plain and safe |
| The HRIS Shortcut Kit | Matches the "shortcuts" idea |
| The HR Tech Insider Kit | Ties directly to the newsletter |

Renaming before launch takes five minutes: change `name` and `slug` in `kit.config.json`, the README heading, and the repository name. After launch it breaks every shared link.

## 3. What goes in the kit

| Type | Best for | Build time |
|---|---|---|
| **Prompt card** | One-off analysis tasks | 1-2 hours |
| **Skill** | Repeatable procedures with a fixed output | Half a day |
| **Project template** | Ongoing jobs that need reference material | Half a day |
| **Tool** | Calculators and checkers people use on the site | 1-3 days |

Ratio to aim for: mostly prompt cards and skills; one tool per quarter as a flagship.

## 4. Repository

```
hris-copilot-kit/
├── kit/
│   ├── skills/<slug>/        SKILL.md, README.md, item.json, examples/
│   ├── prompts/<slug>/       prompt.md, item.json
│   ├── projects/<slug>/      instructions.md, README.md, item.json, reference/
│   └── tools/<slug>/         README.md, item.json
├── templates/                starting point for each type
├── scripts/
│   ├── new_item.py           scaffolds an item from a template
│   └── build.py              validates, packages zips, regenerates catalog
├── .github/workflows/
│   ├── validate.yml          runs on every push and pull request
│   └── release.yml           publishes downloads when you push a tag
├── catalog.json              machine-readable list of items (generated)
├── kit.config.json           name, repo and site settings
├── README.md                 public front page with the catalog table (generated section)
├── ROADMAP.md                this plan
├── CONTRIBUTING.md           how to add an item
└── CHANGELOG.md
```

## 5. Lifecycle of an item

1. **Idea.** From your own work, reader replies, or a GitHub issue using the request template.
2. **Scaffold.** `python scripts/new_item.py skill <slug> "<Title>"`
3. **Build.** Write the content; create synthetic examples labeled as fictional.
4. **Test.** Run it in Claude on the examples at least three times. Fix anything inconsistent.
5. **Validate.** `python scripts/build.py`, then commit.
6. **Pair with an issue.** The newsletter explains the problem; the item solves it.
7. **Release.** Tag `main` (`v2026.11.1`); GitHub publishes the zips.
8. **Link back.** Add the issue URL to `item.json` and cut a patch release.
9. **Maintain.** Bump the item's version when it changes and note it in the changelog.

## 6. Downloads and versioning

- **Every item is its own zip.** A skill zip uploads straight into Claude.
- **The whole kit is one zip** for people who want everything.
- **Stable links.** `https://github.com/rampreddym/hris-copilot-kit/releases/latest/download/<slug>.zip` always serves the newest version, so newsletter and site links never go stale.
- **Kit releases** use `vYEAR.MONTH.N`, for example `v2026.11.1`.
- **Items** use semantic versions in `item.json`: major for a changed output format, minor for new capability, patch for fixes.

## 7. Website (mittana.com/kit)

The site should read the catalog rather than store its own copy, so adding an item to the repo updates the site automatically.

- **Source:** `https://github.com/rampreddym/hris-copilot-kit/releases/latest/download/catalog.json`
- **Page layout:** filter chips by category and platform; one card per item with title, type, summary, platforms, Download button, and "Read the issue" link; a "Download the full kit" button; an email signup for kit updates.

Prompt for Lovable:

> Add a /kit page that fetches https://github.com/rampreddym/hris-copilot-kit/releases/latest/download/catalog.json at load time and renders one card per entry in `items`: title, a type badge, summary, platforms as tags, a Download button linking to `download`, and a "Read the issue" link to `newsletter.url` when it is not empty. Add filter chips for `category` and `platforms`. Add a "Download the full kit" button linking to `full_kit_download`, and show `version` and `item_count` in the header. Show a friendly message if the fetch fails.

Check that the fetch works from the browser once the first release exists; if GitHub's redirect blocks it, serve `catalog.json` from the repository's raw URL instead.

## 8. Newsletter and LinkedIn loop

| Channel | What happens |
|---|---|
| Newsletter issue | Explains one problem; ends with "Download the shortcut" |
| LinkedIn post | 60-second screen recording of the shortcut doing the job |
| LinkedIn comment | Link to the download |
| Kit item README | Links back to the issue |
| Site /kit page | Every item, with subscribe prompt |
| GitHub | Stars and watchers get release notifications |

## 9. First 12 items

One per weekly issue. The first two are already in the repo.

| # | Item | Type | Category |
|---|---|---|---|
| 1 | Release Note Triage | Skill | Release management |
| 2 | AI Feature Governance Check | Prompt card | AI governance |
| 3 | Integration Error Explainer | Skill | Integrations |
| 4 | Pre-Migration Data Audit | Skill | Data quality |
| 5 | HR Case Tier Router | Project template | Service delivery |
| 6 | Security Role SoD Reviewer | Skill | Security |
| 7 | Vendor Demo Scorecard | Prompt card | Selection |
| 8 | Test Script Generator | Skill | Testing |
| 9 | CHRO Translation | Prompt card | Communication |
| 10 | Year-End Readiness Checklist | Project template | Payroll and compensation |
| 11 | HCM Migration Risk Calculator | Tool | Migration (quarterly flagship) |
| 12 | Business Requirements to Configuration Workbook | Skill | Implementation |

Keep a running backlog in GitHub issues labeled `request` and `idea`.

## 10. Measures

| Measure | Where | 90-day target |
|---|---|---|
| Downloads per item | GitHub Release asset counts | 100+ for the best item |
| Repository stars | GitHub | 250 |
| Newsletter subscribers from the kit | Site signup source | Track from launch |
| Inbound requests | Issues and LinkedIn messages | 10 ideas from readers |

Download counts: `gh api repos/rampreddym/hris-copilot-kit/releases --jq '.[].assets[] | "\(.name) \(.download_count)"'`

## 11. Guardrails

- **Synthetic data only.** Every example is invented and labeled as fictional.
- **Nothing from an employer.** No configurations, documents, code or screenshots from NSF or any past employer. Build from general patterns and vendor-public information.
- **No legal advice.** Compliance content points to counsel and tells users to verify current law.
- **Credit and license.** Content under CC BY 4.0 so others can reuse it with credit, which spreads your name; scripts under MIT.
- **Not affiliated.** The README states the kit isn't endorsed by Oracle, Workday, Microsoft or Anthropic.
- **Review before merge.** Use the checklist in CONTRIBUTING.md.

## 12. Launch checklist

- [ ] Decide the final name (section 2)
- [ ] Create the empty GitHub repository and push this code
- [ ] Push tag `v2026.11.1` and confirm the release has 2 item zips, the full kit zip and catalog.json
- [ ] Download each zip and test the skill upload in Claude
- [ ] Build the /kit page on mittana.com
- [ ] Publish the newsletter issue that introduces Release Note Triage
- [ ] Add the issue link to the item, run the build, release `v2026.11.2`
- [ ] LinkedIn launch post with a screen recording
