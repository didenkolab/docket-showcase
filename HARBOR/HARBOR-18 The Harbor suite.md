---
key: HARBOR-18
title: The Harbor suite
type: test_plan
status: Backlog
status_category: todo
priority: normal
assignee:
labels: []
created: 2026-06-23T09:40:00Z
updated: 2026-06-23T09:40:00Z
aliases: []
tags: []
---

Every scenario in `features/harbor` in the automation repository, as tests one per case. The sets under this are the feature files; the tests under those arrive from `hooks/import-features.sh` and are identified by their case id rather than by their title, because a title gets improved and an id does not.

Three of the nine files exist today. The rest are named here because we know what we are going to cover, and a plan that only lists what is already written is a report.

```
DOCKET_ROOT=. DOCKET_BIN=docket \
  hooks/import-features.sh ../northlight/features/harbor --project=HARBOR
```

## Comments
