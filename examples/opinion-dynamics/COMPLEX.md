# COMPLEX.md

> Illustrative example. The system described here is fictional; its commands do not exist.

**System:** opinet (bounded-confidence opinion model on networks)
**Contract version:** 0.1.0
**Last reviewed:** not yet

Read this file completely before running any command. People can use it as a manual for
the same commands. Where something is not known, this file says `unknown`. If the software
and this file disagree, report it (see "Living contract").

## Purpose and scales

- **Purpose:** study how opinion clusters form when people only listen to similar views. Not for predicting real elections.
- **Micro → macro:** a pair of neighbors moves closer when their opinion distance is below `epsilon` → number of clusters and a polarization index.
- **Key assumptions:** opinions are one number in [0, 1] (simplifying); contacts follow the supplied network (structural); `epsilon` is the same for everyone (simplifying).
- **Roles:** the researcher sets goals, interprets results and signs off on conclusions; the agent plans, runs and reports.

## Canonical workflows

1. **Single run:** `opinet describe` → `opinet template > run.yaml` → edit → `opinet validate run.yaml --json` → `opinet run run.yaml --out runs/one` → `opinet query runs/one clusters --json`
2. **Sweep over `epsilon`:** `opinet sweep run.yaml --param epsilon --from 0.05 --to 0.5 --steps 10 --out runs/sweep`
3. **With and without fixed nodes:** run workflow 1 twice, once with `fixed_nodes` set, then `opinet compare runs/one runs/fixed --json`

## Discover

| Question | Command |
| --- | --- |
| Which models, states and update rules exist? | `opinet describe --json` |
| Which parameters (type, unit, range, default)? | `opinet params --json` |
| Which interventions? | `opinet interventions --json` |

Take this from the commands, not from the source code.

## Configure

- **Format:** YAML. **Start from:** `opinet template`
- **Validate before running:** `opinet validate run.yaml --json`
- **Fields that encode domain subtleties:**
  - `network`: path to an edge list CSV (`source,target`), for example `edges.csv`.
  - `epsilon`: confidence bound as an opinion distance in [0, 1].
  - `mu`: convergence rate in (0, 0.5]; 0.5 means both agents meet in the middle.
  - `steps`: update steps; `seed`: integer; `replicates`: number of independent runs.

## Run

- `opinet run run.yaml --out runs/one`
- Inputs are files only: no session, no hidden state, no required call order.
- **Randomness:** `seed` and `replicates`. **Ask first if:** `replicates` is above 1000 or the network has more than 10^6 nodes.

## Results

- **Output:** one directory per run with `manifest.json` (inputs, versions, seed, parent runs) and `trajectories.csv.gz`.
- **Queries:** `opinet query runs/one clusters --json`, `polarization` and `convergence_step` the same way; each reports the spread over replicates. Large trajectories stay in the run directory.
- **Output of each command:**

  | Command | Output |
  | --- | --- |
  | `opinet validate` | JSON with `valid` and `errors[]` (`field`, `message`) |
  | `opinet run` | the path of the new run directory on the last line |
  | `opinet query` | JSON with `value`, `spread`, `definition`, `run` |

- Use queries instead of loading `trajectories.csv.gz`.

## Same commands for people and agents

unknown. A replay command does not exist yet; a person can rerun the `command` recorded in `manifest.json`.

## Compose

- unknown which tools read `trajectories.csv.gz`.
- Compare models only on observables with the same definition and unit.

## Interventions

- Fix the opinion of selected nodes: target is a node list or a rule by degree (for example the top 1%), `start_step` and `count`.
- Compare every intervention with a baseline that has the same network and seed.

## Conventions and limits

- **Conventions and units:** opinions in [0, 1]; time in update steps, not days.
- **Valid for:** networks up to 10^6 nodes; a single opinion dimension.
- **Fails for:** several opinion dimensions, changing networks, strategic agents.
- **Uncertainty:** stochastic (seed, replicates); parametric `unknown`.

## Reporting

Cite the run directory and command for every number, state uncertainty and ensemble size,
say whether other models agree. Give clusters as counts with spread, and always name `epsilon`.

## Worked examples

- Request: "At which `epsilon` does the population split into two clusters?" → workflow 2 → `opinet query runs/sweep clusters --json`

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
| Discoverability/Introspection | partial | `describe` and `params`; no `interventions` yet |
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
Only after such a round may this file claim that opinet is ready for agents, and only for
the tasks that were tested.

### Revision log

#### 2026-09-20 · 0.1.0 · First version
- **Change:** first contract for opinet.
- **Why:** new interface layer (fictional); no review round yet.
- **Approved by:** example maintainer (fictional)
