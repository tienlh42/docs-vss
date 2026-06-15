# Development Task Rules

## Purpose

This document defines the additional task-structure rules for the `Development` folder in ClickUp.

`Development Rules` is a supplemental layer on top of `General Rules`, not a replacement.

Any task inside the `Development` folder must satisfy `General Rules` first. After that, it must also satisfy the additional structure and reporting rules defined in this document.

## Folder Structure

The structure is:

`Folder (Development) -> List -> Epic -> Phase (Milestone) -> Task/Subtask`

### 1. List level

Each List should represent one of these two cases:

* A system or product area, for example `Mobile App`, `Websites`, `Power School`, or `ClickUp`
* A major standalone project, for example `Data Privacy`

This means the List is the main reporting bucket at portfolio level inside the `Development` folder.

### 2. Epic level

Inside each List, work should be grouped under top-level tasks tagged `epic`.

An `Epic` is treated as the project level for reporting. It can represent:

* A project inside a system
* A major feature stream
* A compliance or transformation initiative
* A backlog bucket if work is not yet structured into an active project

Examples already used in the folder:

* `Epic: Phase 3 (Photo Privacy + Deeplink)` in `Mobile App`
* `Epic: DPIA & TIA for ClickUp` in `Data Privacy`
* `Epic: CRM Presales Flow` in `Data Privacy`
* `Epic: Backlog` in multiple Lists

### 3. Phase level

Under each Epic, create child tasks tagged `phase`.

A `Phase` is treated as a milestone/reporting stage under the Epic. Every Epic should be broken into phases that match the real delivery path of that work.

Typical phase names may include:

* `BRD`
* `Vendor Proposal`
* `Planning`
* `Development`
* `Testing`
* `UAT`
* `Deployment`
* `Documentation`
* `Review & Approval`
* `Implementation & Monitoring`

The exact phase names can vary by project type. The rule is not to force one template for all work, but to make sure each Epic is broken into meaningful milestone stages that can be reported clearly.

## Task Structure Under Each Phase

Each Phase must contain concrete tasks or subtasks. Depending on the nature of the project, there are two accepted patterns.

### Pattern A: Direct tasks under the Phase

Use this when the phase is straightforward and the tasks can be tracked directly.

Example:

* `Phase: BRD`
* `BRD (Photo Privacy . Deeplink)`
* `Share BRD draft with stakeholder, collect feedback`
* `Stakeholder signs off on BRD`

This pattern is recommended for software delivery, outsource execution, feature development, and other linear implementation work.

### Pattern B: Workstream/grouping tasks under the Phase, then subtasks inside

Use this when the phase is document-heavy, compliance-heavy, or contains multiple workstreams that need to be grouped first.

Example:

* `Phase: Documentation`
* `Policy & Regulations`
* `Training & HR`
* `Core Assessment Documents`
* `Vendor & Legal`

Then each grouping task contains the detailed subtasks under it.

This pattern is recommended for projects like data privacy, governance, legal/compliance, policy rollout, or any initiative where one phase contains several document packages.

## General Setup Rules

When creating new work in `Development`, follow these rules:

1. Choose the correct List first.

Put the work in the List for the owning system or the major project area.

2. Create or reuse the correct Epic.

If the work belongs to an existing project stream, add it under that Epic.

If it is a new project stream, create a new top-level task and tag it `epic`.

3. Break the Epic into Phases.

Every reportable Epic should have milestone child tasks tagged `phase`.

4. Add concrete tasks or subtasks under each Phase.

Do not leave a phase empty.

Each phase should show the actual outputs, approvals, or execution tasks needed to finish that stage.

5. Keep the structure practical.

If a phase only needs a few direct tasks, use them directly.

If a phase contains many related work items across categories, create grouping tasks first.

6. Keep reporting levels clean.

The expected reporting levels are:

`List` = system / major project bucket

`Epic` = project level

`Phase` = milestone level

Task/Subtask = execution/output level

## Ticket Writing Rules

All tickets in the `Development` folder must be logged in English.

Using AI to draft or improve ticket content is encouraged, especially to make wording clearer, more complete, and easier to report across teams.

Each ticket description must include the following sections:

* `Context` `(*)`
* `Goal` `(*)`
* `Solution`
* `Acceptance Criteria`

`Context` and `Goal` are mandatory for every ticket.

The expected intent of each section is:

* `Context`: background, problem statement, business situation, or current-state issue
* `Goal`: the required outcome or objective that the ticket must achieve
* `Solution`: proposed approach, implementation direction, or expected execution path
* `Acceptance Criteria`: conditions that define when the ticket can be considered complete

This rule applies to Epic, Phase, and task/subtask-level tickets whenever a description is used. Descriptions should be written clearly enough that another team member, vendor, or reviewer can understand the purpose and expected outcome without additional explanation.

## Assignee, Due Date, and Time Estimate Rule

Tasks tagged `epic` and `phase` must not have `Assignee`, `Due Date`, or `Time Estimate` set directly on the task itself.

These three fields are treated as rollup fields at the Epic and Phase level. Their effective values are derived from the task/subtask-level child work underneath. Setting them directly on the Epic or Phase creates conflicting signals with the underlying work and pollutes workload, timeline, and capacity reporting.

The intended behavior is:

* `Assignee` on an `Epic` or `Phase` is left empty. Ownership at the reporting level is visible through the union of assignees on the underlying tasks/subtasks.
* `Due Date` on an `Epic` or `Phase` is left empty. The effective due date is the latest due date among the child tasks/subtasks; for an `Epic` it is the latest phase due date.
* `Time Estimate` on an `Epic` or `Phase` is left empty. The total effort is the sum of the time estimates on the underlying tasks/subtasks.

Task/subtask-level work continues to follow the standard rules: one assignee per task, a realistic due date, and a time estimate that reflects expected effort.

## How To Decide the Right Shape

Use a software delivery style when the work moves through implementation stages such as requirements, planning, development, testing, UAT, and deployment.

Use a compliance or documentation style when the work is driven by document packages, governance domains, legal review, training, or sign-off gates.

In both cases, the important rule is the same:

* The Epic must be reportable as a project
* The Phases must be reportable as milestones
* The lowest-level tasks or subtasks must represent real execution items or actions

## Minimum Standard for Any New Epic

Before considering a new Epic properly set up, it should have:

* the correct List
* one top-level task tagged `epic`
* a clear set of child tasks tagged `phase`
* tasks or subtasks defined under each active phase

If work has not been structured yet, it can temporarily stay in `Epic: Backlog`, but before active execution starts it should be reorganized into the correct Epic and Phase structure.

## Reporting Intent

This structure exists so reporting can happen consistently at two main levels:

* Epic level: project progress
* Phase level: milestone progress

Tasks and subtasks exist to support execution and to make phase progress evidence-based, but the primary reporting layers remain `Epic` and `Phase`.
