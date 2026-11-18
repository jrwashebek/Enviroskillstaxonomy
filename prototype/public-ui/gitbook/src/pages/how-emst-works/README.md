---
path: how-emst-works/README.md
title: How EMST is put together
description: The kinds of record in EMST, from roles and tasks to competencies, employer versions, modules, signals and links to other systems.
---

EMST is built from a few kinds of record that link to each other. Roles and tasks come first: they say what the work is. The other records hang from them.

## Roles and tasks

A role profile describes a kind of job, such as a forester or an environmental permit writer. Each role lists tasks: short statements of the work, such as inspecting a site or writing a permit condition. This release has {{roles}} roles and {{tasks}} tasks.

Roles come in three depths: {{rolesFull}} full profiles, {{rolesLower}} earlier drafts at lower depth, and {{rolesEmerging}} emerging roles that are only ideas so far. [What EMST covers](page:start-here/what-emst-covers/README.md) says more about each depth.

## Competencies

A competency is a skill or a body of knowledge behind a set of tasks. Each one links to the tasks it supports. This release has {{comps}}:

- {{compsPractice}} practice competencies, for doing a kind of work;
- {{compsTransversal}} transversal competencies, which apply across all kinds of environmental work, such as working safely or working with the public and partners;
- {{compsKnowledge}} knowledge areas.

Each competency has draft levels. The levels are described by indicators: things you could see a person do at that level. This release has {{indicators}} indicators. The levels are explore only, because no expert panel has placed them yet.

## Employer versions

The same role can look different at a federal agency and at a small nonprofit. So each role can have a version for each kind of employer that has it: {{actorList}}. This release has {{variants}} employer versions. A version says how the work, the rules and the setting differ.

## Job families and subject modules

- A **job family** groups roles that do similar work, such as wildland fire management. There are {{families}}, and a role can be in more than one.
- A **subject module** groups related subsectors, such as air quality. There are {{modules}} subject modules, plus core practice that every module shares.

## Signals and instruments

**Signals** are signs that the work may change, such as a new tool or a change in job postings. **Instruments** are the laws, rules, court decisions and other documents that shape the work. [How change is tracked](page:how-emst-works/how-change-is-tracked.md)

## Links to other systems

EMST links its records to other ways of describing jobs: O\*NET, ESCO, OPM job series and state job classes. This release has {{series}} OPM series records and {{stateClasses}} state job class records. AI agents suggested every link, and no person has reviewed them. [Links to other systems](page:how-to-read/links-to-other-systems.md)

## Tools and credentials

EMST also lists {{tools}} tools and {{credentials}} credentials, linked to the work they are used for.

## IDs and releases

Each record has an ID, such as emst:core/ROL-ZJFCC09. IDs are candidates until version 2.0.0, so they may still change. Always cite the release with the ID. Each release is built from the [GitHub repository]({{repo}}) and must pass eight checks before anyone outside the project may rely on it. [Release status](page:release/status.md)
