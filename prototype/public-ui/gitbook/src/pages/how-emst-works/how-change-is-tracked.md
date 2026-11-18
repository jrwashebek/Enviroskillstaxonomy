---
path: how-emst-works/how-change-is-tracked.md
title: How change is tracked
description: How EMST moves from a single signal to a watch item to a change indicator, so that a guess is never shown as a finding.
---

EMST tracks change in steps. Each step needs more evidence than the one before, so that a guess is never shown as a finding.

## 1. A signal is recorded

A signal is one piece of evidence that work may change. It might be a new tool, a new rule, a change in job postings or a report from someone who does the work. Each signal has a source, a date and a [source grade](page:how-to-read/source-grades.md). This release has {{signals}} signals, all on watch.

## 2. A watch item is opened

When signals suggest that a new kind of work or skill may be forming, EMST opens a watch item. {{lifecycleWatch}} Each watch item also names what would show it is not forming.

## 3. A change indicator moves

A signal counts toward a change in a role or a skill only when all of these are true:

- two independent kinds of evidence point the same way, such as job postings and observed use of a tool;
- the change lasts for two periods in a row, or for one period plus a recorded use of the tool at work;
- the signal links clearly to the role or skill, not just partly;
- the cause is named, so that a budget cut is not mistaken for the effect of AI;
- a named person has reviewed it.

No indicator may rest on one company's data alone.

## Where release {{release}} stands

This release checked {{changeTargets}} possible changes to roles and skills against that rule. {{changeMovedSentence}} Watch signals and watch items never count toward a change indicator.

Exposure to AI and automation is also pending. AI raters have made first passes for some tasks, but no group of practitioners has rated them, so the explorer shows “[Assessment pending](page:how-to-read/assessment-pending.md)”.

## Where to see it

[What's changing](explorer:/changing) in the explorer lists the signals, the watch items, the emerging roles and the laws and rules. [Anticipate change](page:by-need/anticipate-change.md) explains how to use it.
