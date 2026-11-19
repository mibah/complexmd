# COMPLEX.md specification (convention v0.1)

The key words MUST, MUST NOT, SHOULD and MAY are used as in RFC 2119.

## 1. Scope

This convention defines the name, location, structure, checkable rules and versioning of a
`COMPLEX.md` file. It does not constrain how the model itself is built.

## 2. File

- A model project MUST name the file `COMPLEX.md` and SHOULD place it in the project root.
- In a monorepo, each tool SHOULD have its own `COMPLEX.md` in its own folder.
- The file MUST be UTF-8 and SHOULD be CommonMark. It MUST NOT use front matter.

## 3. Header lines

Directly under the title the file MUST contain:

- `**System:**` followed by a non-empty name.
- `**Contract version:**` as SemVer (`MAJOR.MINOR.PATCH`).
- `**Last reviewed:**` as a date `YYYY-MM-DD` or `not yet`.

## 4. Sections

Sections are H2 headings. The set below is defined in [principles.md](principles.md), which also
gives the origin of each row (K, P or C: the paper names it as contract content, requires it
elsewhere, or it is a COMPLEXmd addition).

| Section | Level | Origin |
| --- | --- | --- |
| Purpose and scales | MUST | P (assumption typology: C) |
| Canonical workflows | MUST | K |
| Discover | MUST | K |
| Configure | MUST | K |
| Run | MUST | K (cost threshold: C) |
| Results | MUST | K |
| Same commands for people and agents | MUST | P |
| Compose | MUST | P (comparison rule: C) |
| Interventions | SHOULD | P |
| Conventions and limits | MUST | K + P |
| Reporting | SHOULD | K |
| Worked examples | SHOULD | K |
| When the interface is not enough | MUST | P |
| Human checkpoints | MUST | P (stop list: C) |
| Conformance | MUST | C |
| Living contract | MUST | P (log format, approval: C) |

The order above is RECOMMENDED. Additional sections MAY be added. The value `unknown` is valid
anywhere and is preferred to a guess.

## 5. Conformance table

The Conformance section MUST contain a table with one row for each of the six principles named
in the paper: Discoverability/Introspection, Declarative control, Statelessness, Structured,
queryable output, Human-Agent parity, Composability. Status MUST be `implemented`, `partial`,
`planned` or `not-applicable`. `not-applicable` MUST be justified in the `How` column;
`implemented` SHOULD say how.

## 6. Revision log

`### Revision log` under Living contract MUST have at least one entry:
`#### YYYY-MM-DD · X.Y.Z · Title`, followed by the fields `Change`, `Why` and `Approved by`.
Each substantive change MUST be approved by a maintainer. The newest entry's version SHOULD
equal the `Contract version`. A file MAY claim readiness for agents only after a review round,
and only for the tasks tested.

## 7. Versioning

The contract version changes MAJOR for incompatible changes to the model's commands, fields or
formats, MINOR for additions, PATCH for clarifications. The version of this convention is 0.1;
changes are listed in [CHANGELOG.md](../CHANGELOG.md).

## 8. Relation to the paper

COMPLEX.md implements the contract that Cattuto & Vespignani call `AGENT.md`. A project MAY add
an `AGENT.md` that only points to `COMPLEX.md`.

## 9. What `complexmd check` verifies

Only structure. It does not run the model or test whether the interface works.

| Code | Level | Rule |
| --- | --- | --- |
| CX001 | error | file missing or not readable as UTF-8 (exit code 2) |
| CX010 | error | a MUST section is missing |
| CX011 | warning | a SHOULD section is missing |
| CX012 | warning | a section appears twice |
| CX020 | error | `**System:**` line missing or empty |
| CX021 | error | `**Contract version:**` missing or not SemVer |
| CX022 | error | `**Last reviewed:**` missing, or neither a valid `YYYY-MM-DD` date nor `not yet` |
| CX030 | error | no table in Conformance |
| CX031 | error | a principle is missing from the table, or an unknown row exists |
| CX032 | error | status is not one of the four values |
| CX033 | error | `not-applicable` without a reason in `How` |
| CX034 | warning | `implemented` without an entry in `How` |
| CX040 | error | Revision log has no entry |
| CX041 | warning | entry heading does not match `#### YYYY-MM-DD · X.Y.Z · Title` |
| CX042 | warning | newest entry's version differs from `Contract version` |
| CX050 | warning | unresolved placeholder `<…>` or `YYYY-MM-DD` |
| CX060 | warning | more than 6000 words (`--max-words` changes the limit) |
