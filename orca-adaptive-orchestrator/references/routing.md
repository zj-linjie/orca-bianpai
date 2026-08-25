# Capability Routing Policy

Read this reference when assigning or reassigning a Task. Runtime launch syntax and lifecycle recovery belong to the current Orca orchestration guide.

## Inventory contract

Use live evidence to describe each available combination:

- Runner and version;
- requested, launch, and Effective Model identities;
- supported launch constraints and effort;
- task-relative Capability Tier;
- evidence source, confidence, and current availability.

A Runner name is not a model or capability. An unresolved or ambiguous Effective Model cannot satisfy a locked assignment.

## Capability tiers

- **Flash**: bounded research, mechanical edits, local UI work, documentation, focused tests, and clearly specified fixes.
- **Pro**: architecture, cross-module reasoning, difficult debugging, complex state, concurrency, migrations, security-sensitive work, integration, and high-risk review.
- **Strong fallback**: a verified strong Codex model used for independent diagnosis or takeover after a Pro failure.

Risk, ambiguity, and reasoning coupling determine the minimum tier; apparent task size does not.

## Selection record

For every assignment record the Task requirement, chosen Runner/model, required and observed tier, evidence, constraints, rejected alternatives, selection reason, and fallback. Use Runner preferences only as tie-breakers between combinations that satisfy the same required tier: prefer OpenCode for mechanical implementation and focused tests, Claude for investigation and context-heavy coordination, and a verified Pro alias for complex implementation or high-risk review.

Launch receipts replace configuration estimates once a Worker starts. If requested and effective values differ materially, pause or re-route according to the approved constraints.

## Recovery policy

Preserve the previous attempt's deliverables, failure symptom, bounded output, tests, excluded hypotheses, and remaining Quality Gate.

- **Runner/tool/environment failure**: use a verified same-tier alternative unless the assignment is locked; otherwise pause for recovery or a Decision Gate.
- **Reasoning failure**: escalate Flash to Pro.
- **Pro failure**: Transfer to a verified strong fallback; pause when none is available.
- **Completed output failing validation**: create a Repair Task rather than treating it as a runtime retry.

One Task gets at most two automatic Dispatch attempts. Restate placement and Runner/model constraints on a replacement because Orca retry linkage does not imply policy inheritance.
