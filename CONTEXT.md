# Orca Adaptive Orchestration Skill

This context defines the Policy Layer language used to analyze, decompose, route, verify, and recover adaptive work through Orca. Orca owns the runtime meanings and lifecycle of Run, Task, Dispatch, Worker, terminals, and worktrees; the definitions below only describe how policy decisions refer to those objects.

## Language

**Coordinator**:
The primary agent that plans the work, assigns ownership, supervises outcomes, and presents decisions to the user.
_Avoid_: Main worker, scheduler

**Worker**:
An agent session that owns one bounded Task and reports its outcome to the Coordinator.
_Avoid_: Sub-agent, child agent

**Runner**:
The agent CLI environment used by a Worker, such as Claude Code or OpenCode; it does not identify the underlying model provider or capability.
_Avoid_: Model, provider

**Effective Model**:
The underlying model selected after Runner aliases and local provider configuration are resolved.
_Avoid_: Agent, Runner

**Capability Tier**:
A task-relative classification used to match an Effective Model to the required reasoning and implementation difficulty.
_Avoid_: Agent tier, effort

**Quality Gate**:
The acceptance boundary a Task must satisfy before its outcome is accepted, independent of what the Worker reports.
_Avoid_: Worker success, test command

**Capability Escalation**:
Moving an unsettled Task to a stronger Capability Tier because its reasoning demands exceeded the previous tier.
_Avoid_: Runner switch, retry

**Run**:
One supervised orchestration objective and the durable coordination boundary for its Tasks and messages.
_Avoid_: Session, job

**Task**:
A bounded unit of work with explicit ownership, dependencies, acceptance criteria, and an expected deliverable.
_Avoid_: Prompt, assignment

**Wave**:
A set of dependency-ready Tasks that may run concurrently without conflicting ownership.
_Avoid_: Batch, phase

**Integration Task**:
A Pro-tier Task that checks consistency, dependency order, test coverage, and conflicts across multiple PR Units.
_Avoid_: Merge Task, final Worker

**Repair Task**:
A bounded follow-up Task created when a completed deliverable fails its Quality Gate.
_Avoid_: Retry, Transfer

**Dispatch**:
One attempt to assign a Task to a specific Worker under the Coordinator's supervision.
_Avoid_: Task, launch

**Execution Manifest**:
The user-visible plan shown before work starts, including Tasks, dependencies, Worker choices, isolation, reasoning effort, and intended PR Units.
_Avoid_: Plan, preview

**Decision Gate**:
A pause that requires the user's choice because proceeding would expand scope, authority, risk, or the agreed recovery budget.
_Avoid_: Worker question, confirmation

**PR Unit**:
A coherent, independently reviewable change boundary represented by its own branch and commits; remote publication requires explicit authorization.
_Avoid_: Task, patch

**Transfer**:
A new Dispatch that gives an unsettled Task to another Worker while preserving the previous attempt's evidence and constraints.
_Avoid_: Retry, handoff

**Full Handoff**:
An ownership transfer after which the original agent stops supervising the work.
_Avoid_: Transfer, Dispatch
