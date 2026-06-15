# General Rules

This document defines the baseline working rules for task setup, workload planning, and reporting consistency across projects in ClickUp.

All tasks must satisfy General Rules first. If a task belongs to the `Development` folder, it must satisfy General Rules first and then follow the additional rules defined in `Development Rules`.

## Task Size Rule

A single task must not exceed **16 hours** of estimated effort.

If the expected work exceeds 16 hours, the task should be split into multiple smaller tasks that each represent a clear deliverable or execution step.

This ensures:

* better progress tracking
* clearer ownership
* more accurate workload reporting
* improved sprint and milestone visibility

## Assignee Rule

Each task must have **only one assignee**.

The assignee represents the person primarily responsible for delivering the outcome of the task.

Other contributors should support through subtasks, comments, or linked deliverables rather than being assigned to the same task.

## Weekly Workload Rule

Weekly workload for each member is calculated based on the **sum of Time Estimates** across their assigned tasks.

The recommended total workload per member per week is:

**40h - 44h**

This range ensures:

* sustainable execution capacity
* realistic planning
* accurate timeline forecasting
* balanced resource allocation across projects

## Ticket Writing Rules

All tickets must be written in **English**.

Using AI to draft or improve ticket content is encouraged to ensure clarity, completeness, and consistency across teams.

Each ticket description must include the following sections:

* Context (*)
* Goal (*)
* Solution
* Acceptance Criteria

**Context** and **Goal** are mandatory.

Section intent:

* Context: background, problem statement, business situation, or current-state issue
* Goal: required outcome or objective that the ticket must achieve
* Solution: proposed approach or execution direction
* Acceptance Criteria: conditions that define completion

These rules apply to Epic, Phase, and task/subtask-level tickets whenever descriptions are used.

Descriptions must be clear enough for another team member, vendor, or reviewer to understand the task without additional explanation.

## OKR Field Rule

At the project level (tasks tagged **epic**), the custom field **OKR** is mandatory.

Allowed values:

* **Net-In**: work that directly supports business growth, conversion, enrollment, revenue contribution, or other business-driving initiatives.
* **Academic Excellence**: work that improves learning quality, teaching effectiveness, academic delivery, assessment quality, or student learning outcomes.
* **Operational Continuity**: work that ensures stable day-to-day operations, service continuity, platform reliability, support readiness, renewal readiness, and uninterrupted business or school processes.
* **Legal Compliance**: work that addresses legal, regulatory, contractual, policy, privacy, governance, or audit-related obligations to ensure compliance and risk control.

Behavior rules:

* Epic defines the OKR value
* Phase inherits the same OKR
* Task/subtask-level work inherits the same OKR

Child tasks must not use an OKR value that conflicts with their parent Epic.

## OKR Mapping Guideline

Use the following examples as a practical guide when choosing the correct OKR value.

### Net-In

Use **Net-In** for work that directly supports business growth, conversion, enrollment, revenue generation, or other growth-driving outcomes.

Typical examples:

* CRM implementation or optimization tied to presales or enrollment flow
* marketing consent flow that directly enables campaign execution
* website improvements that support lead generation or conversion
* new sales, admissions, or parent acquisition workflows

### Academic Excellence

Use **Academic Excellence** for work that improves teaching, learning, assessment, classroom delivery, academic operations, or student learning outcomes.

Typical examples:

* Google Classroom setup and improvement
* report card workflow improvements
* learning tools implementation
* AI pronunciation or learning-support applications
* systems or automations that improve academic delivery quality

### Operational Continuity

Use **Operational Continuity** for work that keeps operations running smoothly, maintains service availability, supports platform continuity, or ensures renewal and support readiness.

Typical examples:

* software or license renewals
* service continuity tasks for Mobile App, CRM, ERP, or admin systems
* infrastructure stability work
* support process setup
* vendor renewal coordination
* tasks that prevent interruption of normal school or business operations

### Legal Compliance

Use **Legal Compliance** for work that is primarily driven by legal, policy, privacy, governance, regulatory, contractual, or audit requirements.

Typical examples:

* DPIA, TIA, or privacy compliance documentation
* legal review workflows
* consent governance and policy alignment
* contract or regulatory readiness tasks
* compliance-driven data handling or approval requirements

### Decision Rule

If a task appears to fit more than one OKR, choose the OKR based on the **primary business intent** of the Epic.

Examples:

* A data privacy task that supports marketing still belongs to **Legal Compliance** if the main driver is regulatory/privacy compliance.
* A system enhancement used by teachers belongs to **Academic Excellence** if the main outcome is better teaching or learning.
* A renewal task belongs to **Operational Continuity** if the main purpose is to avoid service interruption.
* A CRM workflow belongs to **Net-In** if the main purpose is acquisition, conversion, or business growth.

The Epic should define the OKR source, and all child tasks should inherit that same intent.

## Assignee, Due Date, and Time Estimate Rule (Epic and Phase Level)

Tasks tagged **epic** and **phase** must not have the following fields set directly:

* Assignee
* Due Date
* Time Estimate

These fields function as rollups derived from task/subtask-level child work.

Correct behavior:

* Epic and Phase Assignee remain empty
* Epic and Phase Due Date remain empty
* Epic and Phase Time Estimate remain empty

Task/subtask-level work must include:

* one assignee
* a realistic due date
* a time estimate aligned with expected effort

This ensures workload accuracy and prevents reporting conflicts across timelines and capacity planning.

## Time Estimate Sizing Guideline

To keep planning and workload reporting consistent across teams, task estimates should follow a simple sizing model.

Recommended sizing bands:

* **1h**: a very small task with a clear outcome, such as a quick update, small fix, brief review, or short coordination step
* **2h**: a small task that requires focused work but remains limited in scope
* **4h**: a medium task that can usually be completed within half a working day
* **8h**: a large task that represents roughly one full working day of focused execution
* **16h**: the maximum recommended size for a single task, used only when the work is still one clear deliverable and cannot be split further without losing practical meaning

Sizing guidance:

* Prefer smaller, outcome-based tasks over broad activity-based tasks
* If a task feels unclear or hard to estimate, split it before assigning a Time Estimate
* If a task is likely to exceed **16h**, it must be broken down into multiple smaller tasks
* Estimates should reflect expected effort, not calendar duration
* Use the same sizing logic across task/subtask-level work to improve workload balancing and weekly planning

Examples:

* `1h`: update ticket content, review a vendor comment, confirm a stakeholder decision
* `2h`: prepare a draft note, validate a small requirement set, conduct a focused review session
* `4h`: write a BRD section, complete a testing cycle for a small scope, configure a simple workflow
* `8h`: implement a self-contained feature component, produce a full document package draft, complete one substantial execution block
* `16h`: complete a large but still clearly bounded deliverable that should remain under one owner

This guideline supports more reliable sprint planning, cleaner reporting, and fairer workload distribution across team members.

## Parent Task Rollup Rule

For any parent task that contains subtasks, the parent-level **Time Estimate**, **Due Date**, and **Status** must be treated as rolled-up fields derived from the full set of subtasks underneath it.

This means:

* The effective **Time Estimate** of the parent task should reflect the sum of the Time Estimates across all relevant subtasks.
* The effective **Due Date** of the parent task should reflect the appropriate rolled-up timeline from its subtasks, typically based on the latest required due date among the child tasks.
* The effective **Status** of the parent task should reflect the real progress state of its subtasks rather than being managed independently from the child work.

The purpose of this rule is to ensure that parent tasks represent the actual state of execution underneath them and do not create conflicting reporting signals.

This rule applies to any structured parent task that is used to group execution work through subtasks, including milestone and project grouping layers where applicable.
