# Execution Manifest

Show this Manifest before any Orca Run, Task, Worker, worktree, branch, commit, or other mutation. In direct-execution mode, show it immediately before starting.

## Required format

```md
# Execution Manifest

Objective: <one sentence>
Mode: <default-confirm | plan-only | direct-execution>
Orca: <fixed executable and runtime version/readiness>
Repository: <managed selector, or unmanaged path in plan-only mode; current ref; clean/dirty state>
Overrides: <every user override or none>
Concurrency: <maximum and planned peak>

## Waves

### Wave 1

| Task | Outcome and Quality Gate | Ownership | Runner → Effective Model | Tier / effort | Placement | PR Unit | Failure path |
|---|---|---|---|---|---|---|---|
| T1 | ... | read: ...; write: ... | ... | ... | ... | ... | ... |

Dependencies: <Task edges and stacked bases, or none; distinguish Orca lineage from Git base>

## Reviews and integration

<required independent reviews, Repair policy, and Integration Task>

## Git and publication

<base refs, branch/commit authority, PR order, and whether remote publication is unauthorized or explicitly authorized>

## Decision Gates

<dirty checkout, ambiguity, unavailable models, external effects, or none>

## Rationale

<why this is the smallest safe decomposition and why each tier/Runner fits>
```

## Authorization wording

For default-confirm mode, end with a precise statement of the local effects confirmation will authorize. State separately that destructive changes, history rewrites, force pushes, deployment, remote PR publication, and unlisted scope remain unauthorized.

For plan-only mode, label every PR Unit as proposed, state that it is a prospective local branch/review boundary rather than an existing remote PR, confirm that no Orca or repository mutations were performed, and stop.

For direct-execution mode, state which explicit phrase authorized immediate local execution, then proceed only with listed effects.
