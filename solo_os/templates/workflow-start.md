# Solo OS — Workflow Start (Idea -> Roadmap -> Build Loop)

This is a small guided tour. It is meant to answer: **"What do I do next in Solo OS once `init` + `verify` are green?"**

## What you are trying to produce in GitHub

1) **Idea** (Kind: `Idea`, usually Status: `Todo` or `In Progress`, Stage: `Inbox`/`Today`/`This Week`)  
2) **Roadmap bet** (Kind: `Roadmap`, often Status: `Prioritized`/`In Progress`)  
3) **Build Loop** (Kind: `Build Loop`, with a real scope box + validation intent)

You can also skip directly to a Build Loop when execution is the main risk (Solo OS calls this a **direct-to-build-loop** path).

## Step A — Create your first issues (CLI-first, recommended)

**Prereq:** a valid `solo-os.yml` in your workspace root with `github.owner` + `github.project.number` configured (run `solo-os init` if needed).

### A1) Create an Idea (optional but common)

```bash
solo-os gh-create --repo <owner/name> --title "[Idea] <short name>" --from-template idea --kind Idea --status Todo --stage Inbox
```

### A2) Create a Roadmap bet (optional, but the “committed strategy” object)

```bash
solo-os gh-create --repo <owner/name> --title "[Roadmap] <short name>" --from-template roadmap --kind Roadmap --status Prioritized --stage "This Week"
```

### A3) Create a Build Loop (the bounded execution unit)

```bash
solo-os gh-create --repo <owner/name> --title "[Build Loop] <short name>" --from-template build-loop --kind "Build Loop" --status In Progress --stage Today
```

**Notes**
- `gh-create` creates the GitHub issue, adds it to your Solo OS Project (by default), and sets the Project fields.
- If you want a blank body, omit `--from-template` and provide `--body` or `--body-file` instead.
- Titles with `[Idea]`, `[Roadmap]`, `[Build Loop]` match Solo OS conventions, but the Project **Kind** field is what the tooling trusts most.

## Step B — Tighten the Build Loop before coding (Checkpoint A)

Once you have a Build Loop issue number:

```bash
solo-os bl-review --repo <owner/name> --issue <N>
```

This checks that the issue body matches the **canonical** Build Loop section headings and is not just boilerplate from the template.

## Step C — Your daily command loop (why Solo OS usually “clicks”)

```bash
solo-os daily-triage
solo-os gh-next
solo-os gh-brief --question active-work
```

## Optional — AI pack path (if you use Cursor/Claude Code)

If you’ve installed the packs:

```bash
solo-os install-commands
```

Then run the bundled slash-style prompts in this order (names only):
- `idea-triage`
- `roadmap-plan`
- `bl-create`
- `bl-execute` (drives `bl-review` and stops before merge)

## When you are stuck

- If commands look “empty,” you’re usually missing: **(a)** issues in the project, **(b)** `Kind/Status/Stage` set, or **(c)** a bad/missing `solo-os.yml` near your workspace root.
- If permissions fail, re-check the GitHub token’s **`project` scope** and that you can access the Project in the browser.