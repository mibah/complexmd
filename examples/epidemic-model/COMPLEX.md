# COMPLEX.md

> Illustrative example. The system described here is fictional; its commands do not exist.

**System:** EpiSim CLI (wrapping the fictional episim library 2.3)
**Contract version:** 0.2.0
**Last reviewed:** 2026-10-12

Read this file completely before running any command. People can use it as a manual for
the same commands. Where something is not known, this file says `unknown`. If the software
and this file disagree, report it (see "Living contract").

## Purpose and scales

- **Purpose:** compare interventions on age-structured compartmental epidemics (SIR, SEIR). Not for real-time forecasting.
- **Micro → macro:** per-person transition rates between compartments → prevalence, peak size and timing, attack rate.
- **Key assumptions:** homogeneous mixing within each age group (structural); contact matrix taken from a survey (empirical); constant rates over time (simplifying).
- **Roles:** the researcher sets goals, interprets results and signs off on conclusions; the agent plans, runs and reports.

## Canonical workflows

1. **Baseline:** `episim-cli template seir > base.yaml` → edit → `episim-cli validate base.yaml --json` → `episim-cli run base.yaml --out runs/base` → `episim-cli query runs/base summary --json`
2. **School closure vs. baseline:** `episim-cli run closure.yaml --out runs/closure` → `episim-cli compare runs/base runs/closure --json`
3. **Ensemble over seeds:** set `seeds: 200` in the config → `episim-cli run base.yaml --out runs/base-ens` → `episim-cli query runs/base-ens summary --json`
4. **Calibration of `beta`:** `episim-cli calibrate base.yaml --cases cases.csv --out runs/fit`

## Discover

| Question | Command |
| --- | --- |
| Which models, compartments and transitions exist? | `episim-cli describe --json` |
| Which parameters (type, unit, range, default)? | `episim-cli params --json` |
| Which interventions? | `episim-cli interventions --json` |

## Configure

- **Format:** YAML. **Start from:** `episim-cli template seir`
- **Validate before running:** `episim-cli validate base.yaml --json`
- **Fields that encode domain subtleties:**
  - `beta`: transmission probability per contact per day; `gamma`: recovery rate per day.
  - `contact_matrix`: path to a CSV with one row and column per age group.
  - Age groups are fixed: `0-17`, `18-64`, `65+`. `R0` is **not** a field: derive it with `episim-cli query runs/base r0 --json`.

## Run

- `episim-cli run base.yaml --out runs/base`
- Inputs are files only: no session, no hidden state, no required call order.
- **Randomness:** `seed` (integer) and `seeds` (number of replicates, default 1). **Ask first if:** `seeds` is above 500 or the horizon exceeds 3 years.

## Results

- **Output:** one directory per run with `manifest.json` (inputs, versions, seed, parent runs), `trajectories.parquet` and `summary.json`.
- **Queries:** `episim-cli query runs/base summary --json` for peak, attack rate and final state; `episim-cli compare runs/base runs/closure --json` for scenarios (single runs only).
- **Output of each command:**

  | Command | Output |
  | --- | --- |
  | `episim-cli validate` | JSON with `valid` and `errors[]` (`field`, `message`); exit code 1 if invalid |
  | `episim-cli run` | the path of the new run directory on the last line |
  | `episim-cli query` | JSON with `value`, `unit`, `definition`, `run` |
  | `episim-cli compare` | JSON with one `delta` per metric and both run paths |


## Same commands for people and agents

`episim-cli replay runs/base` prints the commands that produced a run, from its `manifest.json`.
A person can rerun them and compare the new `summary.json` with the old one.

## Compose

- The fictional `netsim` tool can read `trajectories.parquet` as a seeding profile; `manifest.json` lists `parents`.
- Compare models only on observables with the same definition and unit.

## Interventions

- `school_closure` (group `0-17`, `start_day`, `duration_days`) and `contact_reduction`: `intensity` is the share of contacts **removed** (0 to 1); 0.3 removes 30%.
- `vaccination` (`coverage` per age group, `start_day`, `efficacy`).
- Apply one intervention at a time first, then combinations. Always compare with a baseline that has the same seed and horizon.

## Conventions and limits

- **Conventions and units:** time in days; rates per day; prevalence as a fraction of the age group.
- **Valid for:** populations above 10,000 people, horizons up to 3 years. **Fails for:** small outbreaks, clustered contacts, changing behavior.
- **Uncertainty:** stochastic (replicates), parametric (`beta`, contact matrix); numerical `unknown`.

## Reporting

Cite the run directory and command for every number, state uncertainty and ensemble size,
say whether other models agree. Report peaks as value and day; tables list scenarios in rows
and metrics in columns; figures label axes with units.

## Worked examples

- Request: "How much does closing schools for 4 weeks reduce the peak?" → workflows 1 and 2 → `compare` delta of `peak_prevalence`, reported with ensemble spread.

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
| Discoverability/Introspection | implemented | `describe`, `params`, `interventions` |
| Declarative control | implemented | YAML config with `validate` |
| Statelessness | implemented | every command reads files only |
| Structured, queryable output | partial | no `compare` for ensembles |
| Human-Agent parity | implemented | same CLI, `replay` |
| Composability | planned | manifest parents exist; no second tool reads runs yet |

Status: implemented, partial, planned, not-applicable. This table is a commitment; evidence
comes from review rounds.

## Living contract

This contract is tested and improved over time. An agent solves representative tasks using
only a plain-language request, this file and the interface. A second agent reviews the logs,
tool calls and outputs and proposes changes. A maintainer decides which changes to adopt.
Only after such a round may this file claim that EpiSim CLI is ready for agents, and only for
the tasks that were tested.

### Revision log

#### 2026-10-12 · 0.2.0 · Intensity clarified
- **Change:** clarified that intensity is the share of contacts removed.
- **Why:** fictional review round: the runner read intensity as the share kept and reported a misleadingly small effect.
- **Approved by:** example maintainer (fictional)

#### 2026-09-03 · 0.1.0 · First version
- **Change:** first contract for EpiSim CLI.
- **Why:** new CLI layer over the library (fictional).
- **Approved by:** example maintainer (fictional)
