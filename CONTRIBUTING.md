# Adding to the kit

Every item lives in its own folder under `kit/<type>s/<slug>/` with an `item.json` describing it. The build script validates items, packages downloads and regenerates the catalog, so you never edit the catalog by hand.

## Add a new item

```bash
# 1. Scaffold from a template (types: skill, prompt, project, tool)
python scripts/new_item.py skill integration-error-explainer "Integration Error Explainer"

# 2. Write the content in kit/skills/integration-error-explainer/
#    and fill in summary, platforms and category in item.json

# 3. Test it in Claude with the synthetic examples in the item's examples/ folder

# 4. Validate, package and refresh the catalog
python scripts/build.py

# 5. Commit on a branch and merge
git checkout -b add/integration-error-explainer
git add -A && git commit -m "Add Integration Error Explainer skill"
```

## Publish a release

Releases are what the download links point to. Tag `main` after merging:

```bash
git tag v2026.11.1   # vYEAR.MONTH.N
git push origin v2026.11.1
```

GitHub Actions validates the kit, builds one zip per item plus the full kit, and attaches them and `catalog.json` to a GitHub Release. Download links of the form `releases/latest/download/<slug>.zip` always serve the newest version.

## Link it to the newsletter

When the issue that introduces an item is published, put its title and URL in the item's `item.json` under `newsletter`, run `python scripts/build.py` and cut a release.

## Before you merge: checklist

- [ ] Uses no real employee data; examples are synthetic and labeled as such
- [ ] Contains nothing from a current or past employer's configuration, documents or code
- [ ] Tested in Claude on the example inputs; output reviewed
- [ ] Skill `description` says when to use it, in under 1,024 characters
- [ ] Version bumped in `item.json` if the item changed (MAJOR.MINOR.PATCH)
- [ ] `python scripts/build.py --check` passes

## item.json fields

| Field | Example | Notes |
|---|---|---|
| `slug` | `release-note-triage` | Must match the folder name; lowercase and hyphens |
| `title` | `Release Note Triage` | Shown on the site and README |
| `type` | `skill` | `skill`, `prompt`, `project` or `tool`; must match the parent folder |
| `version` | `1.0.0` | Semantic versioning per item |
| `summary` | One sentence | What it does for the practitioner |
| `platforms` | `["Oracle HCM Cloud", "Workday"]` | Non-empty list |
| `category` | `Release management` | Used to group items on the site |
| `added` | `2026-11-16` | Date first published |
| `data_safety` | `No personal data needed` | What data the user must provide |
| `newsletter` | `{"title": "", "url": ""}` | Filled once the issue is out |
