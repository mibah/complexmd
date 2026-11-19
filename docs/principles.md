# Principles and their place in COMPLEX.md

COMPLEX.md follows one source: Cattuto & Vespignani, *Computational models of complex systems
meet AI agents*, npj Complexity (2026), <https://doi.org/10.1038/s44260-026-00102-1>
(CC BY 4.0). This page paraphrases the paper, says where each idea lives in a COMPLEX.md, and
marks what this project adds.

## 1. The paper in short

The Perspective argues that complex systems science suits AI agents well: the gap between
micro rules and macro behavior is bridged by simulation, and the most useful work perturbs
systems across a large space of interventions. Most simulators were built for people in scripts
and notebooks, so an agent has to read source code, write throwaway programs and wade through
large outputs. The authors propose six design principles for an agent-friendly interface, a
dedicated contract file (conventionally `AGENT.md`) that announces the interface to the agent,
and a continuous cycle in which one agent works with the contract and a second reviews the
result. As a worked case they wrap the Epydemix epidemic-modeling library
(<https://github.com/epistorm/epydemix/tree/agent-framework>). Throughout, the human researcher
keeps scientific intent and epistemic responsibility.

Origin codes used below: **K** = the paper names this as contract content; **P** = the paper
asks for it elsewhere (principles, role of the human, escalation, living document) but does
not assign it to the contract; **C** = COMPLEXmd addition, not from the paper.

## 2. The six principles

The names are the paper's and are used unchanged everywhere in this project.

### Discoverability/Introspection
- **Paper:** A model answers structured queries about itself: its structure, its parameters
  with the values they may take, its components, states and transitions, and the interventions
  it offers. Nobody should need to read source code for this. A parameter registry is the
  typical device.
- **In COMPLEX.md:** *Discover* (and *Interventions* for the intervention catalog).
- **Check for authors:** Can an agent list every parameter with its range without opening a source file?

### Declarative control
- **Paper:** The agent steers the simulator with self-contained, validatable configuration
  artifacts (JSON or YAML) instead of sequences of imperative calls. Domain subtleties belong
  in configuration fields.
- **In COMPLEX.md:** *Configure*.
- **Check for authors:** Can an agent produce and validate a complete run description without writing code?

### Statelessness
- **Paper:** Every operation is a self-contained function of its inputs (config, saved
  outputs). Session state, in-memory objects and call-order constraints are hostile to agents.
- **In COMPLEX.md:** *Run*.
- **Check for authors:** Does each command work from files alone, in any order, after a restart?

### Structured, queryable output
- **Paper:** Results go to the filesystem in a self-describing format, and query tools answer
  targeted questions (statistics, final state, scenario comparison) so the agent need not load
  full trajectories.
- **In COMPLEX.md:** *Results*.
- **Check for authors:** Can an agent get the peak of a run as a small JSON answer without parsing raw output?

### Human-Agent parity
- **Paper:** The interface is equally legible and operable by a person and an agent. A CLI
  that takes YAML and returns JSON fits; a person can replay an agent's commands in a terminal.
- **In COMPLEX.md:** *Same commands for people and agents*.
- **Check for authors:** Can a researcher reproduce every agent step from the files and commands alone?

### Composability
- **Paper:** Tools that share filesystem-backed artifacts can be chained; output bundles carry
  a manifest that records their parent, so provenance and multi-model pipelines are traceable
  from files.
- **In COMPLEX.md:** *Compose*.
- **Check for authors:** Does a run's manifest say which runs and inputs it came from?

## 3. Other statements of the paper

| Statement | Section in COMPLEX.md |
| --- | --- |
| The agent contract: a file read at the start that documents discovery, configuration format, output files, query commands and domain conventions | the file as a whole |
| The contract is a living document, improved by agent-on-agent review | Living contract, Revision log |
| Leaving the interface (reading source, writing scripts) stays possible; frequent escalation reveals gaps | When the interface is not enough |
| The interface is an additive layer; existing code keeps working | Conformance (`How` column) |
| The human is responsible for scientific conclusions; confidently wrong results are a risk | Purpose and scales, Human checkpoints |
| A model is agent-ready only after it solves representative tasks from a plain request and the contract | Living contract |
| Shared conventions and community benchmarks are the path forward | Roadmap in the README |
| Micro-macro gap and exploration of the intervention space | Purpose and scales, Interventions |

## 4. COMPLEXmd additions

Not from the paper and never attributed to its authors:

- **Assumption typology** (structural, empirical, simplifying): makes the limits of a model visible at a glance.
- **Cost threshold in Run:** gives the agent a concrete point at which to ask first.
- **Comparison rule in Compose:** results are comparable only with equal definition and unit.
- **Concrete stop list in Human checkpoints:** turns the paper's call for human oversight into testable triggers.
- **Conformance table:** lets a project state, per principle, how far it has come, since the paper says principles can be adopted one by one.
- **Revision log format and mandatory human approval:** the paper allows the reviewer agent to apply changes itself; this project requires a maintainer to approve each substantive change.
- **`unknown` instead of guessing:** gaps are named, not filled.
- **The name `COMPLEX.md`** instead of `AGENT.md`, and the `complexmd check` structure checker.

## 5. Section overview

| Section | Required? | Content | Origin |
| --- | --- | --- | --- |
| Purpose and scales | yes | what the model is for and not for; micro rules → macro observables; key assumptions; roles | contract content required elsewhere in the paper (assumption typology: COMPLEXmd addition) |
| Canonical workflows | yes | typical runs as command sequences | contract content named in the paper |
| Discover | yes | commands for models, states, transitions, parameters, interventions | contract content named in the paper |
| Configure | yes | format, template, validation, domain subtleties as fields | contract content named in the paper |
| Run | yes | run command, files only, seeds, ensembles, cost threshold | contract content named in the paper (cost threshold: COMPLEXmd addition) |
| Results | yes | run directory with manifest, output of each command, query commands | contract content named in the paper |
| Same commands for people and agents | yes | replaying agent steps from files | required elsewhere in the paper |
| Compose | yes | outputs as inputs, provenance via parents | required elsewhere in the paper (comparison rule: COMPLEXmd addition) |
| Interventions | recommended | target, timing, intensity, order; compare with a matching baseline | required elsewhere in the paper |
| Conventions and limits | yes | conventions, units, validity, failure cases, uncertainty | contract content named in the paper (conventions) and required elsewhere (knowing where a model fails) |
| Reporting | recommended | cite run and command, state uncertainty, table and figure conventions | contract content named in the paper |
| Worked examples | recommended | request → commands → outputs | contract content named in the paper |
| When the interface is not enough | yes | escalation is allowed, announced and recorded | required elsewhere in the paper |
| Human checkpoints | yes | when the agent stops and asks | required elsewhere in the paper (concrete stop list: COMPLEXmd addition) |
| Conformance | yes | per principle: implemented, partial, planned, not-applicable | COMPLEXmd addition (derived from the paper) |
| Living contract + Revision log | yes | testing, improving, readiness, version history | required elsewhere in the paper (log format and human approval: COMPLEXmd addition) |

## 6. What COMPLEXmd does not implement

The six principles are properties of a model's interface. Each model project has to implement
them itself, for example with a thin CLI layer around existing code. COMPLEX.md documents the
principles and makes the claim checkable in structure, but it does not implement them.
