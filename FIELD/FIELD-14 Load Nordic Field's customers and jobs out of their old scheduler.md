---
key: FIELD-14
title: Load Nordic Field's customers and jobs out of their old scheduler
type: task
status: In progress
status_category: doing
priority: normal
assignee: '[[ola]]'
parent: "[[FIELD-1 Job scheduling]]"
labels: []
created: 2026-06-29T10:10:00Z
updated: 2026-07-02T10:20:00Z
aliases: []
tags: [customer/nordic-field]
sprint: "[[Sprint 2]]"
estimate: 3
---

Eleven hundred customers and about four thousand past jobs, exported from a scheduler the firm has used since 2014, in a file where the address is one column and the flat number is sometimes in it and sometimes in the note. Nothing about the pilot works until this has been done once against the real file.

## Acceptance

- [ ] Every customer in the export exists in Fieldnote with an address that finds them
- [ ] Past jobs keep their dates, so the last-visit line has something to say
- [ ] Rows the importer could not read are listed rather than dropped

## Comments
