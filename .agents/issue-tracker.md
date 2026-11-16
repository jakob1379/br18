# Issue tracker: Linear

Issues and specs for this repo live in Linear, workspace `jgalabs`. Use the Linear connector tools (`mcp__claude_ai_Linear__*`) for all operations. The `gh` CLI is not used for issues.

Every issue for this repo has:

- **Team**: `Jgalabs` (key `JGA`)
- **Repo label**: `br18` (in the single-select label group `repo`)
- **Project**: `Legoleze` for work under `legoleze/`. Work on the site clone has no project.

## Resuming after a break or a context compaction

The tracker is the memory. Before picking work, list the open issues (`list_issues` with team `JGA`, label `br18`, and state `backlog`, `unstarted` or `started`). Take the first `ready-for-agent` issue with no open blocker. When work on an issue stops, write where it stands as a comment on the issue before ending the turn.

Data gaps in the legoleze corpus are recorded in the `huller` list of `legoleze/dk-regulering/registry.yaml`, not as issues. An issue is work someone will do next.

## Conventions

- **Create an issue**: `save_issue` with `team: "JGA"`, `labels: ["br18", <triage label>, <category label>]`, `project: "Legoleze"` when it applies, and a Markdown `description`.
- **Read an issue**: `get_issue` with the identifier (`JGA-123`), then `list_comments` for the discussion. `get_issue` does not return comments.
- **List issues**: `list_issues` with `team: "JGA"`, `label: "br18"`, plus `project`, `state` or a second label query as needed.
- **Make an issue a sub-issue of a parent**: `save_issue` with `parentId`.
- **Blocking**: native relations. `save_issue` with `blockedBy: ["JGA-12"]` on the blocked issue. An issue is unblocked when every blocker is Done or Canceled.
- **Comment on an issue**: `save_comment`.
- **Apply / remove labels**: `save_issue` with `addLabels` / `removeLabels`. Never pass `labels` on an update: it replaces the whole set and drops `br18`.
- **Claim**: `save_issue` with `assignee: "me"` and `state: "In Progress"`.
- **Close**: comment with the explanation, then `save_issue` with `state: "Done"` (or `"Canceled"` for `wontfix`).

Category roles map to the labels that already exist: `bug` is `Bug`, `enhancement` is `Feature` (new behaviour) or `Improvement` (better behaviour).

## Pull requests as a triage surface

**PRs as a request surface: no.**

## When a skill says "publish to the issue tracker"

Create a Linear issue as in **Create an issue** above.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Map**: one issue labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. Create the label on first use.
- **Child ticket**: a sub-issue of the map (`parentId`). Labels: `wayfinder:<type>` (`research`/`prototype`/`grilling`/`task`).
- **Blocking**: see **Blocking** under Conventions.
- **Frontier query**: `list_issues` with `parentId` set to the map and an open state; drop any with an open blocker or an assignee; first in map order wins.
- **Claim**: see **Claim** under Conventions, the session's first write.
- **Resolve**: comment with the answer, set `state: "Done"`, then append a context pointer to the map's Decisions-so-far.
