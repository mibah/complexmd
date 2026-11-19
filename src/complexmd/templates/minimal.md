# COMPLEX.md

**System:** <name of the simulator or library>
**Contract version:** 0.1.0
**Last reviewed:** not yet

Read this file completely before running any command. People can use it as a manual for
the same commands. Where something is not known, this file says `unknown`. If the software
and this file disagree, report it (see "Living contract").

## Purpose and scales

<What the model is for and not for; micro rules → macro observables; key assumptions; who decides what.>

## Canonical workflows

<The typical runs as command sequences: baseline, intervention vs. baseline, ensemble.>

## Discover

<Commands that list models, states, transitions, parameters (type, unit, range, default) and interventions.>

## Configure

<Configuration format, template command, validation command, fields with domain subtleties.>

## Run

<Run command; inputs are files only; seeds and ensembles; cost threshold for asking first.>

## Results

<Run directory layout with manifest, query commands, output format of each command.>

## Same commands for people and agents

<How a person replays and checks every agent step from the files.>

## Compose

<Which outputs feed other tools or models; compare only on equal definition and unit.>

## Conventions and limits

<Conventions and units, where the model is valid and where it fails, sources of uncertainty.>

## When the interface is not enough

You may read the source code or write your own script. Say first which capability is
missing, and record it under "Living contract" or in an issue. Repeated gaps should become
interface features.

## Human checkpoints

Stop and ask when the goal is unclear, a request falls outside "Conventions and limits", a
run exceeds the cost threshold, results look implausible or contradict another model, or this
contract seems wrong.

## Conformance

| Principle | Status | How |
| --- | --- | --- |
| Discoverability/Introspection | planned | |
| Declarative control | planned | |
| Statelessness | planned | |
| Structured, queryable output | planned | |
| Human-Agent parity | planned | |
| Composability | planned | |

Status: implemented, partial, planned, not-applicable. This table is a commitment; evidence
comes from review rounds.

## Living contract

This contract is tested and improved over time. An agent solves representative tasks using
only a plain-language request, this file and the interface. A second agent reviews the logs,
tool calls and outputs and proposes changes. A maintainer decides which changes to adopt.
Only after such a round may this file claim that <system> is ready for agents, and only for
the tasks that were tested.

### Revision log

#### YYYY-MM-DD · 0.1.0 · First version
- **Change:** <…>
- **Why:** <evidence: review round, recurring escalation, user report, interface change>
- **Approved by:** <name>
