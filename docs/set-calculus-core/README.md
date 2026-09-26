# Set Calculus Core

This directory holds the canonical Set Calculus Core mathematical vocabulary and formal contracts.

## Core 0.1 canonical path

See [`CORE_0.1_PATH_INDEX.md`](CORE_0.1_PATH_INDEX.md) for the repository-wide Core 0.1 navigation index.

The path index maps the active Core formalizations, consistency evidence, provenance material, compatibility work, and required-but-missing release artifacts. `CORE_0.1_COMPLETENESS_CHECKLIST.md` remains the canonical pass/fail authority.

## Core-math boundary rule

Core Math does not contain scope boundaries unless the boundary is a universal barrier.

Scope boundaries are permitted in Applied Math.

Scope boundaries are not required in Applied Math unless the application defines them as a boundary.

Any universal barrier identified in Core Math requires special attention because it is an invalidating state to the core set ideology.

## Canonical primitives

The canonical definitions are maintained in `../philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md`. This README lists the Core primitive set without redefining those terms.

```text
Set
Member
Relationship
Identity
State
Transform
Resolution
Provenance
```

Canonical distinction:

```text
Identity != State
```

## Initial invariants

### Transform-produced properties

A property produced by a transform cannot automatically be projected backward onto its unresolved input.

```text
property(T(x)) does not imply property(x)
```

unless an explicit rule establishes that implication.

### Unresolved is not unknown

An unresolved state may contain constraints, relationships, provenance, and possible resolution paths even when it does not contain a unique final value.

```text
Unresolved != Unknown
```

### Provenance survives transformation

A resolution should retain enough trace to determine what admitted inputs, relationships, and transforms produced it.

### Explicit failure

The system should represent failure to resolve rather than silently inventing a value.

Candidate terminal or reportable states include:

- unresolved
- resolved
- reversible resolution
- closure
- logical failure

The exact vocabulary remains subject to formalization.

## Primitive-definition authority

The canonical terminology ledger is the definition authority for Core primitive names. Formal contract files may refine operational semantics without creating competing primitive definitions.

## Active formalizations

- `TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md` - trajectory admissibility, composition, boundary compatibility, representation structures, depth-indexed requirements, requirement entailment, and supported resolution depth.
- `TRANSFORM_SEMANTICS.md` - canonical A5 Transform contract covering applicability, input requirements, output guarantees, preservation, declared change, provenance, failure, composition, identity, reversibility, and closure-producing behavior.
- `STRUCTURAL_PROOF_RULES.md` - canonical A8 statuses and restrictions for weakening, contraction, exchange, cut, and substitution across provenance-bearing proof contexts.
- `RESOLUTION_TRANSITION_SEMANTICS.md` - canonical A9 public-state transition contract covering material cause, reclassification, supersession, reopening, and provenance-preserving transitions among UNRESOLVED, PARTIAL, VALID, and INVALID.
- `CLOSURE_REOPENING_ALGEBRA.md` - canonical A10 partial algebra for CLOSE, EXTEND, REOPEN, RECLOSE, epoch/receipt order, scoped closure, and provenance-preserving closure history.
- `RESOLUTION_CLOSURE_AND_REOPENING.md` - first-terminal-prefix closure, closure receipts, resolution epochs, evidence-driven reopening, protected residual conservation, and provenance-preserving reclosure.
- `ANCHOR_FOUNDATIONAL_SPACE.md` - minimal foundational resolution-space substrate, primitive objects, notation, reconciliation states, closure, provenance, and Anchor axioms.
- `RESOLUTION_TRANSITION_PROBLEM.md` - finite decision problem over an Anchor projection; canonical linear certificate bound and polynomial verifier establish bounded RTP membership in NP.
- `RTP_NP_HARDNESS_REDUCTION.md` - candidate polynomial-time many-one reduction from 3SAT to RTP, including construction, completeness/soundness argument, and explicit proof obligations.
- `RTP_ACTIVE_RELATIONAL_LEDGER.md` - canonical finite representation of active relational state; exact persistent Boolean-assignment representation; discharges PO-2.
- `RTP_SAT_ASSIGNMENT_INVARIANTS.md` - proves assignment exclusivity and assignment completeness for the 3SAT reduction; discharges PO-5 and PO-6.
- `RTP_SAT_CLAUSE_SOUNDNESS.md` - proves clause soundness, global no-bypass topology, and terminal reconciliation equivalence; discharges PO-7, PO-8, and PO-9.
- `RTP_SAT_RULE_COMPLEXITY.md` - proves `R_SAT` is a fixed seven-schema rule family and every primitive rule check is polynomial-time; discharges PO-3 and PO-4.
- `RTP_SAT_PROVENANCE_MONOTONICITY.md` - proves append-only verifier-derived provenance, assertion lineage retention, and anti-forgery/anti-erasure invariants; discharges PO-10.
- `RTP_CANONICAL_ENCODING_AND_SIZE_PROOFS.md` - freezes `RTP-ENC-v1`, proves the linear trajectory/certificate bounds and polynomial construction, discharges PO-1/PO-11/PO-12, and completes the NP-hardness/NP-completeness theorem.
- `artifacts/Resolution_Space_Framework.pdf` - preserved primary source artifact for the Anchor/RTP line; see `../provenance/PHOTONIC_MODEL_ANCHOR_LINEAGE.md` for project provenance.

- `RTP_CANONICAL_VERIFIER_REGISTRIES.md` - freezes `RTP-RULES-v1` and `RTP-BOUNDARIES-v1`, canonical predicates, version immutability, and a common `O(W^2)` primitive runtime bound.
- `RTP_VERIFIER_STATE_SIZE.md` - proves every canonical verifier state has size `O(N^2)` and derives a uniform conservative `O(N^5)` verifier bound for general RTP.

- `RTP_CERTIFICATE_CONSTANT_8.md` - gives the exact canonical certificate serialization and proves `|C| <= 8N^2` for every canonical instance, establishing `c_RTP = 8` without hidden asymptotic constants.


## Core consistency evidence

- `../audits/CORE_0.1_SPECIFICATION_AUDIT_A1_A4_A6_A7.md` - focused audit of A1-A4, A6, and A7, including repaired primitive, resolution-coordinate, six-witness, and trajectory gaps.
- `../../scripts/audit_core_specification_a1_a4_a6_a7.py` - executable validator for the audited specification gates.
- `../audits/CORE_0.1_G1_CONSISTENCY_AUDIT.md` - repository-wide G1 audit tying the historical three-state/five-witness material to the current six-witness/four-state Core and the closure/reopening layer.
- `../../scripts/audit_core_g1_consistency.py` - executable repository-wide G1 scanner used by `.github/workflows/core-g1-consistency-audit.yml`.
