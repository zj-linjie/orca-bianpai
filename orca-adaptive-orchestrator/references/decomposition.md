# Decomposition and PR Units

Use this reference while producing the Execution Manifest and when a material scope discovery requires replanning.

## Keep or split

Keep one Worker when the objective is small, tightly coupled, or likely to require concurrent edits to the same files. Split only when at least two candidate Tasks each have:

- a meaningful and complete outcome;
- explicit acceptance criteria;
- identifiable read/write ownership;
- an independently explainable deliverable;
- no frequent coordination with another concurrent Task.

Do not split adjacent files, repeated steps of one refactor, or one debugging loop merely to increase parallelism. Prefer two or three concurrent Workers; four is the default hard ceiling.

## Construct the Task graph

For every candidate Task, record inputs, outputs, dependencies, owned paths or components, Quality Gate, risk, and expected PR Unit. Build a conflict graph before a dependency graph:

- Overlapping implementation ownership prevents concurrent execution.
- Read-only investigation or review may share a checkout with an implementation Worker when it cannot mutate files.
- Every concurrently active implementation PR Unit needs its own approved checkout/worktree and branch. If isolation is unavailable, serialize those Tasks even when their file ownership does not overlap.
- A fresh Worker does not imply a new worktree.

Group dependency-ready, conflict-free Tasks into Waves. Create a prerequisite PR Unit for shared contracts, migrations, or foundational types that block other work. Keep dependency chains no deeper than three or four levels. Use Orca `new-top-level` semantics with the repository default base for independent PR Units; use child/stacked placement only for genuine dependency, and state the actual Git base separately from Orca lineage.

## Define PR Units

A PR Unit has one purpose, one implementation owner, independent validation, and a clear rollback story. Use review burden and semantic cohesion rather than line-count limits. One Task may include several coherent commits, but one implementation Task must not write multiple unrelated PR Units.

The implementation Worker owns commits for its PR Unit. Reviewers report findings without editing that branch. A failed review creates one bounded Repair Task and transfers current implementation ownership to its Worker only after the original Worker settles; the previous owner must not continue editing. An Integration Task checks consistency, dependency order, coverage, and conflict risk across PR Units; it does not merge, cherry-pick, rewrite history, or become a catch-all editor unless the Manifest or validated force-dispatch constraints explicitly grant that bounded ownership.

## Risk and Quality Gates

Always define observable acceptance criteria. A Worker's success report is evidence, not acceptance.

Require an independent review at the same or stronger Capability Tier for authentication, authorization, security, data migrations, concurrency, public APIs, cross-module refactors, and Pro-tier implementation. Ordinary Flash-tier work may rely on focused tests and repository checks when its risk is low.

When tests already fail on the untouched baseline, preserve reproducible evidence and distinguish the baseline failure from regressions. Fix unrelated baseline problems only when they block the approved Quality Gate or the user expands scope.

## Dirty checkout

Relevant uncommitted changes create a Decision Gate before execution. Offer only safe choices:

1. keep the work in the current checkout with one implementation Worker, exiting force dispatch for ordinary direct execution when applicable;
2. let the user establish a clean commit or another explicit base;
3. replan around a different, already available baseline.

Never automatically stash, commit, discard, or copy the user's changes.
