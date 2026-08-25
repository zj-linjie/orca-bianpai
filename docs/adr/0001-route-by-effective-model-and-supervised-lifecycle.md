# Route by effective model and delegate lifecycle to Orca

The adaptive orchestrator is a Policy Layer. It chooses Task boundaries, capability, Quality Gates, and bounded recovery from the Effective Model and repository evidence rather than inferring capability from a Runner name.

Orca's version-matched guides remain the single source of truth for repository/worktree operations and Run, Task, Dispatch, Worker, message, receipt, and cleanup semantics. The Policy Layer records decisions against Orca IDs but does not reproduce or replace that lifecycle.
