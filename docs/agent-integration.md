# Pointing agents at COMPLEX.md

## 1. Why a pointer is needed

Agents read what their configuration points to. A `COMPLEX.md` that nobody references stays
unread, and the contract does its job only if it is in the agent's context from the start.

## 2. Claude Code

Claude Code does not load `COMPLEX.md` by itself. Import it from `CLAUDE.md`:

```markdown
@COMPLEX.md
```

The import places the file in context at the start of each session. You may add one sentence
about escalation, for example that the agent must say so before leaving the documented commands.

## 3. Other agents (`AGENTS.md`)

Add this to `AGENTS.md`:

```markdown
This project ships an agent contract in `COMPLEX.md`. Read it completely before you operate
the model, use the commands it documents, and follow its rules for escalation and human
checkpoints.
```

## 4. Optional `AGENT.md`

The paper calls the contract `AGENT.md`. For tools that look for that name, add a file with one
line that points to `COMPLEX.md`, and keep all content in `COMPLEX.md`.

## 5. Limits

A file cannot force an agent to follow it. What counts is the test in
[living-contract.md](living-contract.md): whether an agent, given only a request and the
contract, does the work correctly.
