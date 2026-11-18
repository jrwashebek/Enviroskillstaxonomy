---
description: "How EMST moves from a single signal to a watch item to a change indicator, so that a guess is never shown as a finding."
---

# How change is tracked

{% hint style="info" %}
Draft release 2.0.0-rc.1. Drafted by AI agents, not yet reviewed by people. [What this means](../how-to-read/drafted-by-ai-agents.md)
{% endhint %}

EMST tracks change in steps. Each step needs more evidence than the one before, so that a guess is never shown as a finding.

## 1. A signal is recorded

A signal is one piece of evidence that work may change. It might be a new tool, a new rule, a change in job postings or a report from someone who does the work. Each signal has a source, a date and a [source grade](../how-to-read/source-grades.md). This release has 107 signals, all on watch.

## 2. A watch item is opened

When signals suggest that a new kind of work or skill may be forming, EMST opens a watch item. Something may be starting in this work, but it is not yet shown to exist across the sector. It is dropped if no new evidence comes in by its review date. Each watch item also names what would show it is not forming.

## 3. A change indicator moves

A signal counts toward a change in a role or a skill only when all of these are true:

- two independent kinds of evidence point the same way, such as job postings and observed use of a tool;
- the change lasts for two periods in a row, or for one period plus a recorded use of the tool at work;
- the signal links clearly to the role or skill, not just partly;
- the cause is named, so that a budget cut is not mistaken for the effect of AI;
- a named person has reviewed it.

No indicator may rest on one company's data alone.

## Where release 2.0.0-rc.1 stands

This release checked 210 possible changes to roles and skills against that rule. None met it. Watch signals and watch items never count toward a change indicator.

Exposure to AI and automation is also pending. AI raters have made first passes for some tasks, but no group of practitioners has rated them, so the explorer shows “[Assessment pending](../how-to-read/assessment-pending.md)”.

## Where to see it

What's changing in the explorer lists the signals, the watch items, the emerging roles and the laws and rules. [Anticipate change](../by-need/anticipate-change.md) explains how to use it.

---

The EMST explorer is not online yet. Names of explorer pages and records on this page will become links when it is. Until then, the records are in the release files on [GitHub](https://github.com/jrwashebek/Enviroskillstaxonomy).

Built from EMST release 2.0.0-rc.1, 25 October 2026. [Report a problem with this page](https://github.com/jrwashebek/Enviroskillstaxonomy/issues) on GitHub (free account needed). An independent open project. Not a government website. Text: CC BY 4.0. Data: CC0 1.0.
