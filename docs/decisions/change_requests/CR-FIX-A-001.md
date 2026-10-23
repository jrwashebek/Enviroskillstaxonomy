# CR-FIX-A-001: Require named human reviewers before the career-ladder hypothesis is published as a finding

- **From:** Fix-A (AI agent, report editor, package fix pass) · **To:** CA (decider, ADR-0027 owner); project lead · **Date:** 2026-10-23 · **Type:** decision text change · **SemVer impact:** none (governance text)
- **Affects:** ADR-0027 §"Flagship report" bullet (publication rule for the career-ladder hypothesis, P-AS-14); flagship report §5; any brief or deck that repeats the rule
- **Evidence label:** J (raised by package review issue 3)

## Problem

ADR-0027 says the career-ladder hypothesis is "co-published with a nonpartisan partner only after IO and LM validation". IO and LM are AI agent roles. As written, the rule lets AI agents validate a hypothesis that AI agents drafted. Package review issue 3 (docs/review/package_review.md) calls this the first thing a journalist will write about, and proposes the fix below.

The report (draft 0.9.1, §5) now states the current rule as it stands, says it amounts to AI checking AI, and says a change has been requested. It does not claim the change has been made.

## Proposed change

Amend the ADR-0027 bullet to read:

> the career-ladder finding is presented as a hypothesis with its mechanism and evidence status. It is published as a finding only after named human reviewers (a qualified industrial-organizational psychologist and a labor economist) validate it, in addition to the IO and LM agent reviews, and it is then co-published with a nonpartisan partner (P-AS-14).

## After a decision

If accepted, the report's §5 sentence "A change has been requested … the decision is pending" becomes "Named human reviewers … must also validate it". If declined, the report keeps the current wording and its "AI checking AI" caveat.
