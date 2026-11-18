---
description: "The kinds of record in EMST, from roles and tasks to competencies, employer versions, modules, signals and links to other systems."
---

# How EMST is put together

{% hint style="info" %}
Draft release 2.0.0-rc.1. Drafted by AI agents, not yet reviewed by people. [What this means](../how-to-read/drafted-by-ai-agents.md)
{% endhint %}

EMST is built from a few kinds of record that link to each other. Roles and tasks come first: they say what the work is. The other records hang from them.

## Roles and tasks

A role profile describes a kind of job, such as a forester or an environmental permit writer. Each role lists tasks: short statements of the work, such as inspecting a site or writing a permit condition. This release has 37 roles and 1,317 tasks.

Roles come in three depths: 13 full profiles, 18 earlier drafts at lower depth, and 6 emerging roles that are only ideas so far. [What EMST covers](../start-here/what-emst-covers/README.md) says more about each depth.

## Competencies

A competency is a skill or a body of knowledge behind a set of tasks. Each one links to the tasks it supports. This release has 223:

- 196 practice competencies, for doing a kind of work;
- 18 transversal competencies, which apply across all kinds of environmental work, such as working safely or working with the public and partners;
- 9 knowledge areas.

Each competency has draft levels. The levels are described by indicators: things you could see a person do at that level. This release has 1,699 indicators. The levels are explore only, because no expert panel has placed them yet.

## Employer versions

The same role can look different at a federal agency and at a small nonprofit. So each role can have a version for each kind of employer that has it: federal government; state government; local government; nonprofit and nongovernmental organizations; the private sector; and academic and research institutions. This release has 140 employer versions. A version says how the work, the rules and the setting differ.

## Job families and subject modules

- A **job family** groups roles that do similar work, such as wildland fire management. There are 17, and a role can be in more than one.
- A **subject module** groups related subsectors, such as air quality. There are 19 subject modules, plus core practice that every module shares.

## Signals and instruments

**Signals** are signs that the work may change, such as a new tool or a change in job postings. **Instruments** are the laws, rules, court decisions and other documents that shape the work. [How change is tracked](how-change-is-tracked.md)

## Links to other systems

EMST links its records to other ways of describing jobs: O\*NET, ESCO, OPM job series and state job classes. This release has 79 OPM series records and 38 state job class records. AI agents suggested every link, and no person has reviewed them. [Links to other systems](../how-to-read/links-to-other-systems.md)

## Tools and credentials

EMST also lists 99 tools and 96 credentials, linked to the work they are used for.

## IDs and releases

Each record has an ID, such as emst:core/ROL-ZJFCC09. IDs are candidates until version 2.0.0, so they may still change. Always cite the release with the ID. Each release is built from the [GitHub repository](https://github.com/jrwashebek/Enviroskillstaxonomy) and must pass eight checks before anyone outside the project may rely on it. [Release status](../release/status.md)

---

Built from EMST release 2.0.0-rc.1, 25 October 2026. [Report a problem with this page](https://github.com/jrwashebek/Enviroskillstaxonomy/issues) on GitHub (free account needed). An independent open project. Not a government website. Text: CC BY 4.0. Data: CC0 1.0.
