# The living contract

A COMPLEX.md is a hypothesis about what an agent needs to know. The paper this project follows
(Cattuto & Vespignani, 2026) proposes testing such a contract with agents, the way usability
testing exposes problems in a human interface. This page describes one practical way to do it.
The prompts and the maintainer-approval rule are COMPLEXmd's own wording and additions.

## 1. The cycle

1. Choose tasks.
2. Agent A solves them using only the request, `COMPLEX.md` and the model's interface.
3. Agent B reviews A's logs, tool calls and outputs.
4. B proposes changes to the contract and flags gaps in the interface.
5. A maintainer decides which proposals to adopt.
6. Adopted changes get a revision-log entry, and the contract version goes up.

## 2. Choosing tasks

Pick 5 to 10 tasks, worded the way researchers would ask. Cover:

- discovering what the model can do;
- running a baseline;
- an intervention compared with a baseline;
- an ensemble, reported with its spread;
- a comparison with another model;
- one request outside the model's validity, where the agent should ask instead of answering.

## 3. When to run a round

- after a new software version;
- when agents keep escalating beyond the interface;
- after user reports;
- when you switch to a different agent model.

## 4. Prompts

````markdown
**Runner prompt**
You are operating <system>. Read COMPLEX.md completely, then complete the task below using
only the commands it documents. Do not read source code unless COMPLEX.md's section
"When the interface is not enough" applies; if you do, say why first. Keep a log of every
command with its output. Finish with a short report that follows the "Reporting" section.
Task: <task>
````

````markdown
**Reviewer prompt**
You are reviewing another agent's work with <system>. You get COMPLEX.md, the agent's log of
commands and outputs, and its run directories. You do not get the expected answer. Check
whether the work followed the contract and whether its conclusions are supported by the
files. List each finding with: where it occurs (log line or run), its kind (ambiguous
contract, missing information, wrong information, interface gap, agent error, unsupported
claim), why it matters, and a concrete wording change for COMPLEX.md if one would help.
````

## 5. Deciding and recording

The maintainer adopts or rejects each proposal. Each adopted change gets a revision-log entry
with its evidence, and the version is raised. A readiness sentence, if you write one, names the
round and the tasks that were tested. Without a real round there is no such sentence.

## 6. Good practice

- Start the reviewer in a fresh session, without the runner's context.
- Where possible, use a different model as reviewer, or have a person spot-check.
- Keep the logs and results of each round in the model project, for example in `reviews/2026-11-19/`.

## 7. The convention itself

Changes to COMPLEXmd go through issues (`convention-change`) and are listed in
[CHANGELOG.md](../CHANGELOG.md).
