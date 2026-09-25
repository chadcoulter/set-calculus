# Core 0.1 Specification Audit: A1-A4, A6, A7

**Branch:** `core-specification-audit`  
**Scope:** A1, A2, A3, A4, A6, A7 against the current Core  
**Disposition:** gaps repaired where found; A3 and A7 required no mathematical change

## Findings

### A1 Canonical primitive vocabulary

**Gap found and repaired.**

The Core README still described the primitive names as candidates and omitted Identity from its primitive list. The canonical terminology ledger lacked rows for Set, Member, Relationship, and Identity.

The repair:

- makes the terminology ledger the definition authority;
- defines all eight Core primitives exactly once in that ledger;
- adds Identity to the canonical primitive set;
- makes `Identity != State` explicit at the Core entry point.

### A2 Three-axis resolution state and four public states

**Gap found and repaired.**

The current Core already had:

- `rho=<P,N,C>`;
- the product partial order;
- join, meet, and incomparability;
- the four public states;
- independent decisive-positive and decisive-negative proof conditions.

The missing item was deterministic construction semantics for the normalized coordinates.

The repair defines obligation-level `Pos(o)`, `Neg(o)`, and `Done(o)`, then constructs:

```text
P = (sum Pos(o)) / |O|
N = (sum Neg(o)) / |O|
C = (sum Done(o)) / |O|
```

for nonempty material-obligation set `O`, with an explicit vacuous profile rule.

Positive and negative support may coexist, preserving conflict rather than cancelling it.

### A3 Independent decisive closure

**No mathematical gap found.**

The current Core explicitly defines:

```text
DecisivePositive != !DecisiveNegative
DecisiveNegative != !DecisivePositive
D+ -> positive closure
D- -> negative closure
```

Constructive Positive Closure has no negative-exhaustion premise, and overlapping decisive closures produce a scoped conflict object.

### A4 Six typed boundary witnesses

**Gap found and repaired.**

Identity had an active typed payload, but the detailed payload schemas and validation logic for State, Context, Authority, Invariant, and Provenance remained only in historical five-witness sections.

The repair adds active canonical payloads for all six witness types, a six-type witness envelope, four-state witness validation, and six-witness aggregate boundary validation.

### A6 Trajectory and boundary semantics

**Gap found and repaired.**

The current four-state composition operator and six-witness checkpoint existed, but the canonical trajectory concatenation law still had to be reconstructed across later corrective sections.

The repair adds one current law:

```text
Adm4(pi1 + pi2 | C,A)
=
Adm4(pi1 | C,A)
tensorA
ValidateBoundary6(E_B6(pi1,pi2 | C,A))
tensorA
Adm4(pi2 | C,A)
```

where `tensorA` denotes the existing four-valued admissibility operator.

This explicitly preserves known positive structure in PARTIAL trajectories.

### A7 Tie-break sequent calculus

**No mathematical gap found.**

The current Core already defines:

- admissible-rule formation;
- scope, dependency, provenance, supersession, and specificity precedence;
- maximal-rule selection;
- positive, negative, partial, and unresolved conflict conclusions;
- preservation of losing rules and witnesses in provenance;
- the canonical `Gamma ; Q |-Omega kappa` sequent interface.

## Validation rule

The executable specification audit validates the repaired active Core definitions.

The repository-wide G1 strict scan remains a separate required validation and must report zero `REVIEW_REQUIRED` findings so historical three-state/five-witness material cannot silently become active again.

## Gate disposition

The machine-readable checklist may mark A1, A2, A3, A4, A6, and A7 as `pass` when both:

```text
specification audit = PASS
G1 strict audit = PASS
```

The human gate checkboxes remain under the named maintainer's authority.
