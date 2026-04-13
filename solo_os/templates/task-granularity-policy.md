# Task Granularity Policy

Create a task only when at least one condition is true:

- expected work time > 30 minutes
- dependency/risk needs tracking
- context must survive interruptions
- explicit validation evidence is required

Do not create tasks for micro-steps under 30 minutes. Keep those steps in a parent task checklist.

## Done Criteria

A task is done only when evidence is linked:

- code proof (`github.com` issue/PR/commit), and/or
- decision/learning proof (canonical markdown doc)

## Archive Policy

- Archive stale completed tasks weekly
- keep one-line outcome before archive