# Solo OS — Getting Started (First-Time User Guide)

Solo OS is a **GitHub Projects V2** operating layer for **solo builders and small teams** who want a repeatable path from **idea → roadmap bet → build loop → shipped learning** — with daily focus tools on top of live GitHub state.

This guide is the same text printed by:

```bash
solo-os onboarding
```

## 1) The mental model (what you are doing)

- **Source of truth:** GitHub Projects + Issues, not a pile of private markdown “status boards”.
- **Structure via fields (defaults):** `Kind`, `Status`, `Stage`.
- **Kinds:** `Idea`, `Roadmap`, `Build Loop`.
- **Stages (time focus):** `Inbox`, `Today`, `This Week`, `Waiting` (WIP and stage rules are designed to keep focus sane).
- **Optional accelerators:** install Solo OS **skills / commands / agents** to standardize how an AI helps you *write and operate* the workflow (GitHub is still the source of truth).

If this sounds heavy: **Tier 1** value is just “I know what to do today” once items exist. Everything else is adoption layers.

## 2) Prereqs (one-time)

You need:
- `git`, `python`, `pipx`, and GitHub CLI `gh`
- a GitHub token with the **`project` scope** (Projects v2)
- a GitHub organization/user that owns a **Projects (v2) project** you can access

Solo OS bootstraps:
- a workspace-level config file: `solo-os.yml`
- required Project **single-select fields** and **options** (best-effort)

## 3) Install Solo OS (recommended)

```bash
pipx install git+https://github.com/ScoopedOutStudios/solo-os.git
```

(If you are developing from a local checkout, `pipx install -e .` is fine.)

## 4) One-time auth check

```bash
gh auth login
gh auth refresh --scopes project
gh auth status
```

If `verify` says your token is missing the `project` scope, refresh scopes before you fight mysterious permission errors.

## 5) Initialize a workspace (creates/aligns a GitHub Project + fields)

From the folder you want to treat as your **workspace root** (it can contain multiple repos):

```bash
solo-os init
solo-os verify
```

What `init` is doing, in human terms:
- **Pick/creates a GitHub Project (v2)**
- **Ensure required project fields** exist (`Kind`, `Status`, `Stage`) with the expected options
- **Write `solo-os.yml`**, which tells Solo OS which repos belong to the workspace
- **Print “recommended views”** you can create in GitHub’s UI (Solo OS does not auto-create these views)

### Empty project is normal
If the GitHub Project has no issues **added to the project** yet, most CLI “planning” commands will look empty. That is expected. Add issues to the project, then set the fields.

## 6) Your first 15 minutes: create 1–3 real items in GitHub

Solo OS works best if you have at least:
- 1 `Idea` in `Inbox` or `Todo` (or `In Progress` if you are actively exploring)
- 1 `Roadmap` bet in `Prioritized` / `In Progress` (optional, but it’s the “committed strategy” object)
- 1 `Build Loop` in `Today` or `This Week` (optional, but it’s the “bounded execution” object)

### 6.1) Create a structured issue (CLI-first path)

Solo OS ships issue body templates you can use directly:

- **Idea body:** `solo-os build-loop-template --kind idea` (prints the Idea template; yes, the flag name is shared)
- **Roadmap body:** `solo-os build-loop-template --kind roadmap`
- **Build Loop body:** `solo-os build-loop-template --kind build-loop`

Create the GitHub issue and add it to your Solo OS project, then set `Kind/Status/Stage`:

```bash
solo-os gh-create --repo <owner/name> --title "[Idea] <short name>" --from-template idea --kind Idea --status Todo --stage Inbox
solo-os gh-create --repo <owner/name> --title "[Roadmap] <short name>" --from-template roadmap --kind Roadmap --status Prioritized --stage "This Week"
solo-os gh-create --repo <owner/name> --title "[Build Loop] <short name>" --from-template build-loop --kind "Build Loop" --status In Progress --stage Today
```

If you are unsure which repo a piece of work belongs to, start with the repo where the code will change; Solo OS is workspace-level, so you can add more repos later.

### 6.2) Promote an Idea → Roadmap (when ready)

If an Idea graduates into a committed bet, promote it (this rewrites the title prefix and updates the Project fields):

```bash
solo-os gh-promote --repo <owner/name> --issue <N> --kind Roadmap --status Prioritized
```

(You can also create a new Roadmap issue and link the Idea in the body under **Parent Linkage** — pick whichever traceability you want.)

## 7) The daily loop (this is the “punch line” for Tier 1)

Run:

```bash
solo-os daily-triage
solo-os gh-next
solo-os gh-brief --question active-work
```

What you should get:
- A stage-oriented review (`daily-triage`)
- A “what should I do next?” shortlist (`gh-next`)
- A narrative brief (`gh-brief`) for common questions

## 8) Build loop discipline (Checkpoint A first)

The fastest way to get execution discipline is:
- use the canonical Build Loop body template
- run Checkpoint A review:

```bash
solo-os bl-review --repo <owner/name> --issue <N>
```

Solo OS focuses on **Checkpoint A readiness** in the core CLI. Checkpoints B/C are primarily **governance and execution practice**; treat them as contract + habits, not magic automation, unless you add tooling around them.

## 9) Optional: install AI “operating system packs”

If you use Cursor, Claude Code, or similar:

```bash
solo-os install-skills
solo-os install-commands
solo-os install-agents
```

Then start with a simple story:
- `idea-triage` → decide Go/Park/Kill and capture assumptions
- `roadmap-plan` → create a real Roadmap bet
- `bl-create` → create a Build Loop with explicit scope + non-goals
- `bl-execute` → drive execution and stop before merge for human approval

If you want a guided “do the next right thing” tour:

```bash
solo-os workflow-start
```

## 10) If something feels “broken”

- **`verify` fails on project fields:** rerun `solo-os init` to repair/align project fields, then `solo-os verify` again
- **CLI output looks empty:** you probably have issues that are not **on the project**, or the project fields are not set
- **Permission errors on Projects:** re-check `gh auth` scopes, and confirm you can access the Project as an org member/user (admin requirements vary)
- **You want a strategy doc:** that belongs in `docs/` (or your product docs) — it is *not* a tracked Solo OS “workflow object”

## 11) Where to read next in this repository

- `docs/workflow-spec.md` (canonical semantics: Kind/Status/Stage, lifecycles)
- `docs/governance/build-loop-and-release-rhythm.md` (what “good” looks like in execution + release)
- `README.md` (install + command list + system overview)