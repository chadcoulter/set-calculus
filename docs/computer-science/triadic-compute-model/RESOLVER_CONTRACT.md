# Triadic Compute Model — Resolver Contract

## 1. Purpose

This document defines the conceptual contract that every one of the 29 required Triadic Compute Model resolver coordinates must satisfy.

The existing architecture already defines the 29 coordinate names and their broad functional groups.

This contract adds the missing executable shape:

```text
what each resolver receives
what it inspects
what it may resolve
what it must preserve
what it returns
how unresolved distinctions are represented
how provenance is retained
```

The contract does not replace the 29-coordinate architecture.

It gives each required coordinate a common operational form.

---

# 2. Canonical Resolver Form

Every resolver coordinate is an instance of:

```text
ResolverCoordinate<I,O> {
    id
    name
    group
    input_type
    output_type

    inspect
    constraints
    projection_rule
    success_condition
    dangling_condition
    conflict_condition

    preserves
    dependencies
    provenance_rule
}
```

Canonical execution:

```text
resolve_coordinate(
    coordinate,
    state,
    goal,
    partition,
    frontier,
    provenance
)
    -> CoordinateResult
```

---

# 3. Resolver Input

Every resolver receives the same execution envelope:

```text
ResolverInput {
    coordinate_id
    model_state
    active_goal
    current_partition
    active_frontier
    dangling_set
    prior_coordinate_results
    provenance
}
```

The coordinate may inspect only the subset relevant to its domain, but it must receive enough context to preserve consistency with the whole resolution pass.

---

# 4. Resolver Output

Every resolver returns:

```text
CoordinateResult {
    coordinate_id
    status

    inspected_relations
    relevant_relations
    resolved_relations
    unresolved_relations
    dangling_relations
    contradictions

    proposed_partition_delta
    proposed_frontier_delta
    admissibility_evidence

    confidence_or_sufficiency
    provenance
    diagnostics
}
```

---

# 5. Coordinate Status

```text
CoordinateStatus :=
    RESOLVED
  | PARTIAL
  | DANGLING
  | CONFLICT
  | INVALID
```

Interpretation:

```text
RESOLVED = all currently relevant distinctions in this coordinate resolved
PARTIAL  = some relevant distinctions remain
DANGLING = unresolved distinctions exist but are not relevant to current G
CONFLICT = incompatible relevant relations remain
INVALID  = coordinate cannot produce a valid result
```

---

# 6. Inspection Contract

Every resolver declares what relation family it inspects.

```text
inspect : ModelState -> RelationSubset
```

Conceptually:

```text
State Identity          -> identity relations
Temporal Continuity     -> temporal relations
Spatial Locality        -> spatial relations
Causal Provenance       -> causal lineage
...
```

The resolver must not silently claim to inspect relation classes outside its declared domain.

---

# 7. Relevance Contract

Each resolver determines which inspected distinctions can affect the active continuation goal.

```text
relevant(r, G) -> Bool
```

Result partition:

```text
inspected_relations
    -> relevant_relations
    + dangling_relations
```

A distinction that is irrelevant to the current G is not destroyed.

It becomes or remains dangling.

---

# 8. Resolution Contract

For each relevant relation, the resolver attempts:

```text
resolve(r, State, G)
    -> resolved
    | unresolved
    | conflict
```

The resolver may refine:

```text
partition
frontier
relation classification
local equivalence classes
```

but may not directly commit the global next state.

---

# 9. Projection Contract

Each resolver contributes evidence toward the projection axis T.

```text
projection_contribution(
    CoordinateResult,
    G
)
    -> ProjectionComponent
```

The complete projection axis is derived only after the full 29-coordinate pass.

```text
T =
combine(
    ProjectionComponent[1..29],
    G
)
```

No single non-prime resolver determines T alone.

---

# 10. Success Condition

Every coordinate defines:

```text
success_condition(
    CoordinateResult,
    G
) -> Bool
```

Generic condition:

```text
no unresolved distinction remains
that can still alter the continuation selected by G
within this coordinate's domain
```

This is local sufficiency, not the global Enough Boundary.

---

# 11. Dangling Condition

```text
dangling_condition(r, G) -> Bool
```

A relation may be dangling if:

```text
it is unresolved
AND
it cannot currently change the relevant continuation
```

Dangling relations remain:

```text
addressable
provenance-preserved
reopenable
```

---

# 12. Conflict Condition

```text
conflict_condition(
    relation_set,
    constraints
) -> Bool
```

A coordinate returns CONFLICT when:

```text
two or more currently relevant relations
cannot simultaneously satisfy the coordinate's required constraints
```

Conflict is preserved as evidence.

It is not collapsed into arbitrary resolution.

---

# 13. Preservation Contract

Every resolver declares invariants it must preserve.

```text
preserves : Set<Invariant>
```

Possible invariant classes include:

```text
identity
causal lineage
temporal ordering
conservation relation
information lineage
equivalence class membership
boundary validity
admissibility
```

A resolver may not produce a resolved relation by erasing an invariant it is required to preserve.

---

# 14. Dependency Contract

Each coordinate may depend on prior or peer evidence.

```text
dependencies : Set<CoordinateID | RelationClass | Invariant>
```

Dependencies do not make the overall architecture sequential.

They define logical dependency, not necessarily execution order.

The 29-coordinate pass may remain parallel while dependency reconciliation occurs during merge.

---

# 15. Provenance Contract

Every CoordinateResult must retain:

```text
input state identity
coordinate identity
relations inspected
relations resolved
relations left unresolved
relations marked dangling
conflicts
constraints applied
goal G
result provenance
```

Minimum provenance entry:

```text
CoordinateProvenance {
    coordinate_id
    source_state
    goal
    inspected
    decisions
    preserved_invariants
    resulting_relations
}
```

---

# 16. Partition Delta Contract

Resolvers do not rewrite the partition lattice directly.

They propose:

```text
PartitionDelta {
    merge_classes
    split_classes
    preserve_classes
    reopen_classes
}
```

The global resolution pass reconciles all coordinate deltas.

---

# 17. Frontier Delta Contract

Resolvers may propose:

```text
FrontierDelta {
    add_relations
    remove_relations
    reopen_relations
    preserve_relations
}
```

The active frontier is updated only after coordinate-result merge.

---

# 18. Admissibility Evidence

Each coordinate contributes evidence used by the Prime Resolver.

```text
AdmissibilityEvidence {
    subject
    relation
    viability
    provenance
}
```

The Prime Resolver evaluates the combined evidence against:

```text
Adm_G(T, Ω)
    =
P_subject
∧ P_relation
∧ P_viability
∧ P_provenance
```

---

# 19. Coordinate Group Mapping

The existing 29 coordinates map into the common contract as follows.

## Physical Primitives

```text
1  State Identity
2  Temporal Continuity
3  Spatial Locality
4  Causal Provenance
```

Primary concern:

```text
preserve coherent physical/world-state identity
```

---

## Conservation Laws

```text
5  Energy
6  Momentum
7  Charge
8  Spin
9  Mass-Energy Equivalence
```

Primary concern:

```text
preserve conservation-compatible transitions
```

---

## Quantum / Information Laws

```text
10 Superposition
11 Entanglement
12 Wavefunction Collapse
13 Entropy
14 Information Conservation
```

Primary concern:

```text
preserve relational/information consistency across unresolved and resolved state
```

---

## Logical Relations

```text
15 Goal Interpretation
16 Boundary Conditions
17 Contextual Relevance
18 Viability
19 Sufficiency
```

Primary concern:

```text
determine what matters for the active continuation
and whether current resolution is usable
```

---

## Lattice Navigation

```text
20 Quotient Termination
21 Frontier Navigation
22 Dangling Compression
23 Reopen Locality
24 Path-Relativity
```

Primary concern:

```text
navigate Π(Ω) without traversing irrelevant structure
```

---

## Persistence Laws

```text
25 Consequence Persistence
26 Equivalence-Admissibility
27 Coordinate Agnosticism
28 Boundary Stability
```

Primary concern:

```text
preserve valid consequences and stable relational structure
across projection and feedback
```

---

## Prime Resolver

```text
29 Prime Resolver
```

Primary concern:

```text
align all coordinate results with G
combine admissibility evidence
reject inadmissible projection
prevent provenance erasure
gate commit
```

---

# 20. Conceptual Coordinate Template

Each coordinate may now be specified using:

```text
ResolverCoordinate {
    id: 1
    name: StateIdentity
    group: PhysicalPrimitives

    inspect:
        identity_relations

    constraints:
        identity_continuity

    projection_rule:
        preserve identity-relevant distinctions

    success_condition:
        no identity ambiguity capable of changing G remains

    dangling_condition:
        identity distinction unresolved but irrelevant to G

    conflict_condition:
        incompatible identity assignments

    preserves:
        provenance
        prior valid identity relations

    dependencies:
        causal provenance
        temporal continuity
}
```

This is conceptual structure only.

The detailed rule content for each of the 29 coordinates should come from source material or later formalization.

---

# 21. Prime Resolver Contract

Coordinate 29 has additional requirements.

```text
PrimeResolver {
    inputs:
        CoordinateResult[1..28]
        G
        Ω
        proposed T

    outputs:
        aligned_projection_axis
        combined_admissibility
        gate_decision
}
```

Gate decision:

```text
ACCEPT
REOPEN
SAFE_DANGLING
INVALID
```

The Prime Resolver may not mark ACCEPT if any required admissibility term is false.

---

# 22. Complete 29-Pass Contract

A complete pass requires:

```text
for i in 1..29:
    result[i] exists
    result[i].coordinate_id == i
    result[i].provenance exists
```

Then:

```text
MergedResolution =
merge(result[1..28])
```

followed by:

```text
PrimeDecision =
resolve_coordinate_29(
    MergedResolution,
    G,
    Ω
)
```

Missing coordinate:

```text
=> INVALID PASS
```

---

# 23. Global Merge Contract

The global merge must preserve disagreement.

```text
merge(CoordinateResult[1..28])
```

must not:

```text
erase conflict
erase provenance
silently prioritize one coordinate
silently discard dangling relations
```

The merge may produce:

```text
compatible resolution
unresolved cross-coordinate dependency
cross-coordinate conflict
reopen request
```

---

# 24. Relationship to Enough Boundary

Coordinate 19 may contribute local sufficiency evidence.

Coordinate 20 may contribute quotient-termination evidence.

Coordinate 28 may contribute boundary-stability evidence.

But the global Enough Boundary is evaluated only after:

```text
all 29 coordinate results
+ triadic projection
+ Prime Resolver admissibility
```

Global rule:

```text
ENOUGH :=
    all relevant distinctions sufficiently resolved
    AND projection singular
    AND admissibility accepted
    AND boundary stable
```

---

# 25. Relationship to Feedback

Every accepted coordinate result contributes to the next-state provenance.

```text
S_n
  -> CoordinateResult[1..29]
  -> projection
  -> admissibility
  -> Enough Boundary
  -> S_n+1
```

The next state retains the resolver evidence that produced it.

---

# 26. Conceptual Completeness

This contract is complete as a common resolver interface when:

```text
every one of the 29 coordinates can be expressed
without changing the contract shape
```

It does not require each resolver's domain-specific rules to be fully formalized yet.

---

# 27. Current Boundary

The architecture currently gives us:

```text
29 required resolver names
group membership
broad functional purpose
Prime Resolver role
```

This document adds:

```text
common resolver input
common resolver output
resolution status
relevance behavior
dangling behavior
conflict behavior
projection contribution
partition/frontier deltas
invariant preservation
dependency declaration
admissibility evidence
provenance contract
```

The detailed internal rules for each coordinate remain a separate formalization task where the source architecture does not already define them.

This defines the Triadic Compute Model Core 0.1 Resolver Contract.
