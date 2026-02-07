---
description: Generate a structured feature design document
allowed-tools: ["Read", "Write", "Glob", "Grep", "AskUserQuestion"]
argument-hint: <description of the feature or change>
---

The user wants a design document for: **$ARGUMENTS**

Based on this description, suggest a short feature name (2-5 words, title-case) and use AskUserQuestion to get the user's approval before proceeding. Offer your suggestion as the recommended option with one alternative.

Once approved, use the feature name in the heading below and fill in each section using codebase context (via Glob, Grep, Read) and the user's description. For sections where you lack information, write a focused TODO rather than leaving the generic helper text. Delete any section that is clearly not applicable. Save the result to `docs/designs/YYYY-MM-design-[feature-name-kebab-case].md`.

---

***INSTRUCTIONS**: For each section below either replace the helper text with something real or delete the whole section. The result should be easily skimmable yet densely informative. This document isn’t a hoop to jump through, it's a chance to use your own work to enhance the technical education of your peers and an invitation for them to help you do better work.*

\[design doc\]

# Name of feature or change

Author: [Your name linked to your employee profile](https://example.com)
Status: draft
Current as of: January, 2000
Reviewers: [Person A](https://example.com), [Person B](https://example.com), etc.

[Overview](#overview)

[Terminology](#terminology)

[The system as it currently exists](#the-system-as-it-currently-exists)

[The problem we're solving](#the-problem-we're-solving)

[Goals](#goals)

[Non-Goals](#non-goals)

[Proposed Implementation](#proposed-implementation)

[Storage](#storage)

[Ownership](#ownership)

[Monitoring](#monitoring)

[Analytics](#analytics)

[Launch Plan](#launch-plan)

[Dependencies](#dependencies)

[Rollout](#rollout)

[Migrations](#migrations)

[Testing](#testing)

[Extensions](#extensions)

[Concerns](#concerns)

[Permissions and Security](#permissions-and-security)

[Usability](#usability)

[Risk and Abuse](#risk-and-abuse)

[Support](#support)

[Open Questions](#open-questions)

# Overview {#overview}

Brief description of the complete feature or change.
What's the point of this?
What's the cost of doing nothing?
Who cares about this?
Why do it now?
How do you feel about the tradeoffs being made here?

## Terminology {#terminology}

Any words not extremely obvious to anyone reading this document are:

*
*
*

## The system as it currently exists {#the-system-as-it-currently-exists}

This is a description of the current system, if any. What are the tradeoffs of the current design that no longer work for us?

## The problem we're solving {#the-problem-we're-solving}

What's wrong with the current system? Where does it or will it break down? Feel free to include charts and numbers but there's no need to prove the case if folks generally already agree.

## Goals {#goals}

The things we definitely want to be true are:

*
*
*

## Non-Goals {#non-goals}

The things that might be nice but are deliberately out of scope are:

*
*
*

# Proposed Implementation {#proposed-implementation}

What are you trying to build?

Add sections here on any APIs, datastores, or significant components that will be part of this design. When in doubt make at least one reference to each piece so commenters can ask for more detail on something that might affect them.

## Storage {#storage}

Where will data be stored?
Is this implementation write-heavy or read-heavy?
If it's write-only does it need a datastore or can it publish data to a pub-sub stream utility (like Kinesis or Kafka)?
If it's read-only can it use a read-only database replica?
How much data will there be?
What is the rough expected growth rate?
Is it tightly connected to existing data or fully separate?
What other systems will reference this data?

## Ownership {#ownership}

Which team will own this feature or system?
Which team's on call would wake up if all the running OS processes in which this feature exists die? (Make sure to invite that team to this document)
Who will care about the data?
Who in the company would be sad if this feature didn't ship?

## Monitoring {#monitoring}

On what web page can a person see whether the feature is healthy? What is "healthy" for this application?

The bare minimum metrics we'll need to always know the health of this feature or system are:

*
*
*

## Analytics {#analytics}

How is your data available in downstream analytics?
Is it in a shape that analysts can use?
Can it be used directly or must it go through an [ETL](http://datawarehouse4u.info/ETL-process.html)?
Are the records created by this feature immutable?
Are the records created by this feature deletable?
Does this remove any data that analysts currently depend on?

# Launch Plan {#launch-plan}

How are you planning to build this feature?

## Dependencies {#dependencies}

What are the upstream and downstream dependencies for this project?

## Rollout {#rollout}

How and when do you plan to build this feature?
How and when do you plan to deploy this feature?
When do we want to start writing data for any new tables?
Will it live behind a feature flag?
Does it require a feature announcement in-app?
Does it require product marketing support?

## Migrations {#migrations}

What, specifically, is the migration plan?
Does it require a backfill?

Describe the steps and attempt to show that if we abandon the project at any intermediate point that it'll be in a stable state until we come back to it. The migration plan should end with something like a \`DROP TABLE\` statement and the deletion of the previous code. If any portion of the old system must stay in place,
explain why this is necessary.

## Testing {#testing}

How will you test that the change or new system is correct?
How will it be tested in an ongoing way to detect regressions?

## Extensions {#extensions}

What are some nice-to-haves future improvements that are out of scope for this project?
What are some projects that are now possible after the launch of this feature?

# Concerns {#concerns}

What are some concerns you might have?

## Permissions and Security {#permissions-and-security}

Who can access this feature or system?
How do we guarantee the access is correctly limited?
In what situations might data leak to the wrong party?
Does this introduce any dependencies or new external surface area to our system that need to be audited? Is sensitive data always encrypted at rest?

## Usability {#usability}

Should this feature behave differently on mobile devices?

## Risk and Abuse {#risk-and-abuse}

What are some things hackers and malicious users can do to abuse this feature?
If we are moving money around, what is our financial risk?

## Support {#support}

Do we need to make any admin UI changes for this feature?
How is customer support expected to support this feature?

# Open Questions {#open-questions}

Is there something you know you don't know but maybe we need to figure out as a company?
Is there some point in the future where we'll be able to validate or reject the need for this work?
Is there an unsolved mystery that we'll have to work around?
