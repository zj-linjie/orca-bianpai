# Route by effective model and use supervised Orca lifecycle

The explicit orchestrator will choose capability from the Effective Model resolved through the Runner's current configuration, rather than inferring capability from a Runner name such as Claude Code or OpenCode. Coordinated work will use Orca Run, Task, and Dispatch lifecycle state because failure transfer, questions, dependency waves, and completion evidence require durable supervision; ordinary full handoff is reserved for requests where the original agent will stop monitoring.
