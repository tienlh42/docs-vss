# Reminder Rules

## Purpose

This document defines the reminder checks that should be reviewed regularly to keep project execution, task hygiene, and workload planning under control.

Reminder checks should focus on three areas:

* overdue tasks
* tasks that violate `General Rules`
* members whose weekly workload is below 100%

## Reminder Member Scope

Reminder checks should only apply to the following members:

* Dustin Nguyen
* Kantan Huynh - Head Office
* Ethan Vo
* James Huynh - Victoria School
* Scott Le - Victoria School
* Peter Duong - Victoria School
* Christina Pham
* Cielo Superticioso - Company Office

Tasks assigned only to members outside this scope should be excluded from reminder outputs.

Tasks without an assignee should still be included under `Unassigned` because they require ownership cleanup.

Overdue and General Rules violation reminders may be filtered by the selected folder/reporting scope. Weekly workload reminders must always scan the full workspace, even when the reminder report is generated for a selected folder.

## 1. Overdue Task Reminder

### Definition

A task is considered overdue when:

* it has a due date earlier than today
* it is not in a closed or completed status

### Reminder Output

The reminder should group overdue tasks by member/assignee.

Within each member group, list all overdue tasks and include:

Tasks without an assignee should be grouped under `Unassigned`.

* task name
* task URL
* assignee
* due date
* status
* parent Epic or Phase when available
* list or folder where the task belongs

### Recommended Action

For each overdue task, the assigned member should either:

* complete the task
* update the due date with a realistic new timeline
* explain the blocker in the task comment
* split the task if the scope is too large

## 2. General Rules Violation Reminder

### Definition

A task violates `General Rules` when it does not satisfy the baseline rules defined in the `General Rules` document.

Common violations include:

* missing assignee on execution-level tasks
* more than one assignee on a task
* missing due date on execution-level tasks
* missing time estimate on execution-level tasks
* time estimate greater than 16 hours
* description missing required sections
* task not written in English
* parent/reporting tasks incorrectly carrying execution fields such as direct assignee, due date, or time estimate

### Required Description Sections

Every task description should include:

* `Context`
* `Goal`
* `Solution`
* `Acceptance Criteria`

For compact display in ClickUp, use bold section labels:

```plain
**Context**
...

**Goal**
...

**Solution**
...

**Acceptance Criteria**
...
```

### Reminder Output

The reminder should group violating tasks by member/assignee.

Within each member group, list each violating task and include:

Tasks without an assignee should be grouped under `Unassigned`.

* task name
* task URL
* assignee
* violation type
* current value causing the violation
* suggested correction

### Recommended Action

The assigned member or project owner should fix the task setup before execution continues.

If the violation is structural, such as a task being too large or having multiple owners, the task should be split or reassigned before it is considered ready.

## 3. Weekly Workload Below 100% Reminder

### Definition

Weekly workload is calculated from the sum of time estimates on assigned execution-level tasks for each member within the target week across the entire workspace, not only one folder. This check includes both open and closed tasks because completed tasks still represent planned/consumed workload for that week.

A member is considered below 100% workload when their planned workload is below the expected weekly capacity.

Baseline weekly capacity:

* 40 hours = 100%
* recommended planning range: 40h to 44h

### Reminder Output

The reminder should scan all workspace tasks for the selected week, then list scoped members below 100% workload and include:

* member name
* planned hours
* workload percentage
* gap to 40 hours
* assigned task count
* suggested follow-up owner or project area when available

### Recommended Action

For members below 100%, project leads should review whether:

* the member genuinely has available capacity
* assigned work is missing time estimates
* upcoming work has not been created yet
* tasks are assigned to the wrong owner
* backlog items should be moved into the current week

The goal is not to fill capacity blindly, but to make planning gaps visible early.

## Report File Structure

Reminder reports should be split into separate files so each section can be refreshed independently:

* Overdue Task Reminder
* General Rules Violation Reminder
* Weekly Workload Below 100% Reminder

The combined report file may be kept as an index/summary only.

## Weekly Workload Display Format

Within the weekly workload reminder:

* group the report by member first
* group each member's task list by location
* do not repeat assignee or task ID inside task rows because the section is already grouped by assignee
* format dates as `dd/MM` when the date is in the current year, otherwise use `dd/MM/yy`
* use status icons instead of status text where possible

Recommended status legend:

* closed
* in progress
* open
* review/testing
* blocked/on hold

## Reminder Review Cadence

Recommended cadence:

* overdue tasks: daily
* General Rules violations: daily or before weekly planning
* workload below 100%: weekly, before the work week starts and during mid-week review

## Reminder Priority

Handle reminders in this order:

1. overdue tasks
2. General Rules violations
3. workload below 100%

Overdue tasks affect delivery immediately.

General Rules violations affect reporting accuracy and execution quality.

Workload gaps affect planning and capacity visibility.
