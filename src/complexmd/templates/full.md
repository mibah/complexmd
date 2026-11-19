# COMPLEX.md

**System:** <name of the simulator or library>
**Contract version:** 0.1.0
**Last reviewed:** not yet

Read this file completely before running any command. People can use it as a manual for
the same commands. Where something is not known, this file says `unknown`. If the software
and this file disagree, report it (see "Living contract").

## Purpose and scales

- **Purpose:** <what the model is for; what it must not be used for>
- **Micro → macro:** <entities and local rules> → <collective observables of interest>
- **Key assumptions:** <assumption> (structural | empirical | simplifying)
- **Roles:** the researcher sets goals, interprets results and signs off on conclusions; the agent plans, runs and reports.

## Canonical workflows

1. **Baseline:** `<cmd> describe` → `<cmd> template` → edit → `<cmd> validate` → `<cmd> run` → `<cmd> query`
2. **Intervention vs. baseline:** <commands>
3. **Ensemble / sweep:** <commands>
4. <further workflows, e.g. calibration | none>

## Discover

| Question | Command |
| --- | --- |
| Which models, states and transitions exist? | `<cmd> describe --json` |
| Which parameters (type, unit, range, default)? | `<cmd> params --json` |
| Which interventions? | `<cmd> interventions --json` |

Take this from the commands, not from the source code.

## Configure

- **Format:** YAML. **Start from:** `<cmd> template`
- **Validate before running:** `<cmd> validate <config.yaml> --json`
- **Fields that encode domain subtleties:** <field: meaning, unit>

## Run

- `<cmd> run <config.yaml> --out <dir>`
- Inputs are files only: no session, no hidden state, no required call order.
- **Randomness:** <seed and ensemble fields>. **Ask first if:** <cost threshold>.

## Results

- **Output:** one directory per run with `manifest.json` (inputs, versions, seed, parent runs) and <data files>.
- **Queries:** `<cmd> query <run> <metric> --json` for <summary, final state, peaks>; `<cmd> compare <run> <run>` for scenarios.
- **Output of each command:**

  | Command | Output |
  | --- | --- |
  | `<cmd> validate` | <e.g. JSON with `valid` and `errors[]` (`field`, `message`); exit code> |
  | `<cmd> run` | <e.g. path of the new run directory> |
  | `<cmd> query` | <e.g. JSON with `value`, `unit`, `definition`, `run`> |

- Use queries instead of loading raw output.

## Same commands for people and agents

<How a person replays every agent step from the run directories, e.g. `<cmd> replay <run>`.>

## Compose

- <Which outputs other tools or models accept as inputs.>
- Compare models only on observables with the same definition and unit.

## Interventions

- <Target, timing, intensity, sequence. Every intervention result is compared with a matching baseline.>

## Conventions and limits

- **Conventions and units:** <…>
- **Valid for:** <…>  **Fails for:** <…>
- **Uncertainty:** <stochastic | parametric | numerical | unknown>

## Reporting

Cite the run directory and command for every number, state uncertainty and ensemble size,
say whether other models agree. <Table and figure conventions.>

## Worked examples

- <path>: <request> → <commands> → <outputs>

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
