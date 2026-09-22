# Triadic Compute Model — State Machine

## 1. Purpose

This document defines the state machine for the Triadic Compute Model.

The model operates as a repeated relational resolution cycle:

```text
Input State
  -> 29-Coordinate Resolution Pass
  -> Triadic Projection
  -> Admissibility Check
  -> Enough Boundary Test
  -> Resolved State
  -> Feedback
  -> Next Input State
```

The 29 resolver coordinates are required parts of the state machine.

---

# 2. Core State Machine

```text
S_n
  ↓
R29(S_n, G_n)
  ↓
Pτ(A_n, T_n)
  ↓
ADM(B_n, G_n)
  ↓
ENOUGH(B_n, G_n)
  ↓
S_n+1
```

Where:

```text
S_n     = current world/model state
G_n     = active continuation goal
R29     = complete 29-coordinate resolution pass
A_n     = source / possibility state
T_n     = active projection axis / relevance relation
B_n     = resolved image
ADM     = admissibility evaluation
ENOUGH  = Enough Boundary termination test
S_n+1   = accepted next state
```

---

# 3. State Definition

```text
TriadicState {
    id
    step
    model_space
    active_goal
    active_frontier
    coordinate_results[29]
    current_partition
    dangling_distinctions
    resolved_image
    admissibility
    enough_status
    provenance
    diagnostics
}
```

---

# 4. Input State

The input state is the complete model available to the resolver at step n.

```text
InputState := {
    Ω_n: ModelSpace,
    G_n: Goal,
    P_n: PartitionState,
    F_n: Frontier,
    D_n: DanglingSet,
    Prov_n: ProvenanceGraph
}
```

The model begins with:

```text
A_n := Ω_n
```

The source vector is therefore not a scalar input. It is the current possibility/model state presented to the resolver.

---

# 5. Active Goal

The resolver operates relative to an active continuation goal:

```text
G_n
```

The goal determines relevance.

```text
Relevant(x) := can x change the continuation selected by G_n?
```

The Prime Resolver aligns all resolver layers to the current G_n.

---

# 6. Required 29-Coordinate Resolution Pass

Every resolution cycle executes all 29 coordinate domains.

```text
R29(S_n, G_n)
```

produces:

```text
CoordinateResult[1..29]
```

The required groups are:

```text
1–4   Physical Primitives
5–9   Conservation Laws
10–14 Quantum / Information Laws
15–19 Logical Relations
20–24 Lattice Navigation
25–28 Persistence Laws
29    Prime Resolver
```

No coordinate is optional.

---

# 7. Coordinate Result

Each resolver coordinate emits:

```text
CoordinateResult {
    coordinate_id
    input_projection
    relevant_relations
    resolved_relations
    unresolved_relations
    contradictions
    dangling_relations
    admissibility_evidence
    provenance
}
```

Each result must preserve the relation between:

```text
source state
resolver coordinate
goal G
resolved distinction
```

---

# 8. Resolution Pass Semantics

The 29-coordinate pass evaluates the current state in parallel conceptually:

```text
Ω_n
 ├─ R1
 ├─ R2
 ├─ ...
 ├─ R28
 └─ R29
```

The combined result is:

```text
R_n := merge(CoordinateResult[1..29])
```

Merge does not mean destructive overwrite.

It means construction of a combined relational view preserving each coordinate's provenance.

---

# 9. Partition Lattice Update

The resolver operates over the current partition lattice:

```text
Π(Ω_n)
```

Coordinate results may:

```text
refine a partition
collapse equivalent distinctions
retain unresolved distinctions
reopen a prior locality
preserve dangling distinctions
```

The updated partition state is:

```text
P'_n := update_partition(P_n, R_n, G_n)
```

Resolution seeks the coarsest partition sufficient for the active continuation.

---

# 10. Dangling State

Distinctions that are irrelevant to G_n are not destroyed.

They enter:

```text
D_n
```

or remain there.

```text
Dangling(x) :=
    unresolved_or_unneeded(x)
    AND
    not currently capable of changing G_n
```

Dangling distinctions remain provenance-addressable.

A context or goal change may reopen them.

---

# 11. Triadic Projection

The atomic projection is:

```text
τ = [A, T, B]
```

For step n:

```text
τ_n = [A_n, T_n, B_n]
```

Where:

```text
A_n = current source / possibility state
T_n = projection axis selected from the 29-coordinate resolved relation set
B_n = projected resolved image
```

Projection function:

```text
project(A_n, T_n, G_n)
    -> B_n
```

---

# 12. Projection Axis

The projection axis is not independent of the resolution pass.

```text
T_n := derive_projection_axis(
    CoordinateResult[1..29],
    G_n
)
```

The Prime Resolver constrains T_n to align with G_n.

---

# 13. Projection Outcome

Projection may yield:

```text
SINGULAR
DANGLING
UNRESOLVED
CONTRADICTORY
```

Interpretation:

```text
SINGULAR       = one admissible relevant continuation image
DANGLING       = no active relevant image; distinction retained
UNRESOLVED     = insufficient resolution
CONTRADICTORY  = coordinate results cannot yet be reconciled
```

Only a singular admissible result can become a terminal Enough-Boundary output.

---

# 14. Admissibility Check

Every projected result B_n is evaluated before acceptance.

```text
ADM(B_n, T_n, Ω_n, G_n)
```

Core admissibility structure:

```text
Adm_G(T, Ω)
    =
P_subject
∧ P_relation
∧ P_viability
∧ P_provenance
```

The result is:

```text
AdmissibilityResult {
    subject_valid
    relation_valid
    viable
    provenance_preserved
    accepted
    reasons
}
```

---

# 15. Admissibility Failure

If admissibility fails:

```text
ADM == false
```

then:

```text
B_n is not committed as next state
```

The state becomes:

```text
SAFE_DANGLING
```

or returns to resolution:

```text
REOPEN_LOCALITY
```

depending on the failure reason.

No transform may create acceptance through provenance destruction.

---

# 16. Enough Boundary

The Enough Boundary determines whether further resolution can change the relevant continuation.

```text
Enough(B_n, G_n)
```

is true when:

```text
all distinctions capable of changing the relevant continuation
have been resolved sufficiently for G_n
```

Formal working condition:

```text
Enough(B_n, G_n) :=
    admissible(B_n)
    AND
    no unresolved relevant distinction remains
```

---

# 17. Enough Boundary Result

```text
EnoughResult :=
    ENOUGH
  | NOT_ENOUGH
  | REOPEN
```

---

# 18. NOT_ENOUGH Transition

If:

```text
Enough == NOT_ENOUGH
```

then:

```text
active frontier expands or changes
dangling distinctions may be reconsidered
partition navigation continues
29-coordinate pass repeats
```

State transition:

```text
RESOLVING
    -> RESOLVING
```

---

# 19. REOPEN Transition

If a previously dangling distinction becomes relevant:

```text
context change
OR
goal change
OR
new relation
```

then:

```text
D_n -> active frontier
```

State:

```text
REOPEN_LOCALITY
```

followed by another full 29-coordinate pass.

---

# 20. ENOUGH Transition

If:

```text
ADM == true
AND
Enough == ENOUGH
```

then:

```text
B_n is accepted
```

and becomes:

```text
S_n+1
```

---

# 21. Feedback

Accepted output becomes the next source state.

```text
B_n -> A_n+1
```

or:

```text
S_n+1 := commit(B_n)
```

Feedback preserves:

```text
prior state identity
transition provenance
resolver evidence
partition history
dangling set
goal history
```

---

# 22. Next-State Construction

```text
S_n+1 := {
    Ω_n+1 = incorporate(B_n)
    G_n+1 = next_goal(G_n, B_n)
    P_n+1 = P'_n
    F_n+1 = next_frontier(B_n)
    D_n+1 = retained_dangling
    Prov_n+1 = Prov_n + resolution_trace
}
```

The next goal may remain unchanged.

---

# 23. State Machine States

```text
INITIAL
RESOLVING
PROJECTING
ADMISSIBILITY_CHECK
SAFE_DANGLING
REOPEN_LOCALITY
ENOUGH_CHECK
RESOLVED
FEEDBACK
INVALID
```

---

# 24. State Machine Transitions

```text
INITIAL
  -> RESOLVING

RESOLVING
  -> PROJECTING

PROJECTING
  -> ADMISSIBILITY_CHECK

ADMISSIBILITY_CHECK
  -> SAFE_DANGLING       if inadmissible
  -> ENOUGH_CHECK        if admissible

SAFE_DANGLING
  -> REOPEN_LOCALITY     if relevant distinction emerges
  -> RESOLVING           if alternate admissible path exists

ENOUGH_CHECK
  -> RESOLVED            if ENOUGH
  -> RESOLVING           if NOT_ENOUGH
  -> REOPEN_LOCALITY     if reopened distinction required

REOPEN_LOCALITY
  -> RESOLVING

RESOLVED
  -> FEEDBACK

FEEDBACK
  -> RESOLVING           for next step
```

---

# 25. Core Execution Loop

```text
resolve_step(S_n):

    G_n = S_n.active_goal

    coordinate_results =
        resolve_all_29(S_n, G_n)

    partition =
        update_partition(
            S_n.current_partition,
            coordinate_results,
            G_n
        )

    T_n =
        derive_projection_axis(
            coordinate_results,
            G_n
        )

    B_n =
        project(
            S_n.model_space,
            T_n,
            G_n
        )

    admissibility =
        check_admissibility(
            B_n,
            T_n,
            S_n.model_space,
            G_n
        )

    if not admissibility.accepted:
        return safe_dangling_or_reopen(
            S_n,
            B_n,
            admissibility
        )

    enough =
        test_enough_boundary(
            B_n,
            coordinate_results,
            partition,
            G_n
        )

    if enough == REOPEN:
        return reopen_locality(S_n)

    if enough == NOT_ENOUGH:
        return continue_resolution(S_n)

    return commit_next_state(
        S_n,
        B_n,
        coordinate_results,
        partition,
        admissibility
    )
```

---

# 26. Provenance Contract

Every transition must retain:

```text
input state
goal
coordinate results
projection axis
triad
admissibility result
partition transition
Enough Boundary decision
output state
```

Minimum trace:

```text
ResolutionTrace {
    step
    source_state
    goal
    coordinate_results[29]
    projection_axis
    triad
    admissibility
    enough_decision
    resulting_state
}
```

---

# 27. Invariant Preservation

The state machine must preserve:

```text
identity continuity
temporal continuity
causal provenance
required conservation relations
information provenance
admissibility
partition lineage
dangling-state recoverability
```

Any result that violates a required invariant may not become the accepted next state.

---

# 28. Resolver Completeness Rule

A resolution pass is structurally complete only if:

```text
count(CoordinateResult) == 29
```

Missing coordinate:

```text
=> INVALID resolution pass
```

The runtime must not silently treat an absent coordinate as neutral.

---

# 29. Prime Resolver Rule

Coordinate 29 operates as gatekeeper.

It must verify that:

```text
all coordinate results are interpreted relative to G
projection axis T remains aligned with G
admissibility is not bypassed
provenance remains intact
```

A failed Prime Resolver result prevents commit.

---

# 30. Termination Rule

A resolution step terminates only when:

```text
29-coordinate pass complete
AND
projection result singular
AND
admissibility accepted
AND
Enough Boundary reached
```

Otherwise resolution continues, reopens, or enters safe dangling state.

---

# 31. Feedback Rule

The model is iterative:

```text
S0
 -> S1
 -> S2
 -> ...
```

Each resolved output becomes the input possibility state for the next cycle.

This creates a persistent relational world model rather than independent one-shot resolutions.

---

# 32. Canonical Form

The complete transition can be summarized as:

```text
S_n
  --R29(G_n)-->
R_n
  --τ[A_n,T_n,B_n]-->
B_n
  --ADM-->
B_n*
  --ENOUGH-->
S_n+1
```

with:

```text
S_n+1.A := B_n*
```

and all prior resolution provenance retained.

This defines the Triadic Compute Model Core 0.1 state machine.
