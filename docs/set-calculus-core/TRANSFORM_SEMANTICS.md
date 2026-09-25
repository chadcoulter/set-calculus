# Transform Semantics

**Status:** Canonical Set Calculus Core 0.1 transform contract  
**Scope:** Transform applicability, execution, preservation, change, provenance, failure, composition, reversibility, identity, closure, and reopening  
**Applies to:** Set Calculus Core

---

# 1. Purpose

A Transform must carry enough semantics for two independent implementers to decide:

```text
whether T may act on a State
what T requires before execution
what T guarantees after execution
what T preserves
what T changes
how provenance changes
how failure is represented
whether T is reversible
whether T can legally compose with another Transform
whether T may participate in resolution closure
```

A Transform is more than a mapping symbol.

```text
defined(T)
!=
applicable(T,s)
!=
successfully-applied(T,s)
```

The contract in this document is normative for Core 0.1.

---

# 2. Canonical Transform object

Define:

```text
T =
<
  D_T,
  A_T,
  τ_T,
  G_T,
  K_T,
  Δ_T,
  Π_T,
  F_T,
  R_T,
  C_T
>
```

where:

```text
D_T = input-domain and input-requirement contract
A_T = applicability predicate
τ_T = state-transition operation
G_T = output guarantees
K_T = preserved properties / invariants
Δ_T = declared changes
Π_T = provenance effect
F_T = failure contract
R_T = reversibility contract
C_T = closure effect
```

Every canonical Transform MUST define all ten components. A component may be empty where the empty value is mathematically meaningful, but it may not be omitted.

---

# 3. Input domain and requirements

Define:

```text
D_T =
<
  Type_T,
  Req_T,
  Scope_T,
  ContextReq_T,
  AuthorityReq_T
>
```

where `Req_T` is the set of materially required input predicates and evidence obligations.

A Transform is not blocked by unrelated unresolved structure.

For each required input obligation `q`:

```text
q ∈ Req_T
```

and:

```text
Satisfied(q,s | C,A) = VALID
```

is required for application.

Therefore:

```text
unresolved(s)
!-> inapplicable(T,s)
```

when the unresolved portion of `s` is outside `Req_T`.

But:

```text
required(q)
∧ Satisfied(q,s | C,A) ∈ {PARTIAL, UNRESOLVED}
->
T may not claim successful application
```

and:

```text
Satisfied(q,s | C,A) = INVALID
->
T is inapplicable for that input contract
```

---

# 4. Applicability

Define:

```text
Applicable(T,s | C,A)
```

iff:

```text
TypeCompatible(s,D_T)
∧
ScopeCompatible(s,Scope_T)
∧
ContextCompatible(C,ContextReq_T)
∧
AuthorityCompatible(A,AuthorityReq_T)
∧
∀q ∈ Req_T:
  Satisfied(q,s | C,A) = VALID
```

This preserves:

```text
defined(T)
!=
Applicable(T,s | C,A)
```

Applicability is evaluated before output guarantees are asserted.

---

# 5. Execution and TransformResult

Define:

```text
Apply(T,s | C,A)
```

only when `Applicable(T,s | C,A)` is true.

The canonical result form is:

```text
TransformResult
=
APPLIED
<
  s',
  E_T,
  P'
>
|
FAILURE
<
  reason,
  ρ_failure,
  E_failure,
  P'
>
```

where:

```text
s'        = produced State
E_T       = execution evidence
P'        = resulting provenance
ρ_failure = failure evidence state <P,N,C>
```

A `FAILURE` value does not itself define the public resolution state. The existing projection over `ρ=<P,N,C>` determines whether retained failure evidence projects to `PARTIAL`, `UNRESOLVED`, or `INVALID` under the active rule profile.

A failed Transform may not assert its output guarantees.

---

# 6. State transition determinism

The transition operation is:

```text
τ_T(s | C,A) = s'
```

when application succeeds.

For Core 0.1:

```text
same normalized input
+ same T
+ same C
+ same A
+ same evidence
->
same TransformResult
```

Missing required evidence remains unresolved evidence. It is not guessed.

---

# 7. Output guarantees

Let:

```text
G_T = {g_1, g_2, ..., g_n}
```

Then:

```text
Apply(T,s | C,A) = APPLIED<s',E_T,P'>
->
∀g ∈ G_T:
  Holds(g,s')
```

A guarantee is a postcondition.

```text
Holds(g,s')
!-> Holds(g,s)
```

unless an explicit backward rule establishes that relation.

---

# 8. Preservation

Let:

```text
K_T = {k_1, k_2, ..., k_m}
```

For every `k ∈ K_T`:

```text
Holds(k,s)
∧ Apply(T,s | C,A) = APPLIED<s',E_T,P'>
->
Holds(k,s')
```

For every materially required invariant `i` active at the Transform boundary:

```text
Preserve(T,i)
∨
AuthorizedChange(T,i,C,A)
```

must be established.

Silence is not preservation evidence.

```text
i ∉ K_T
∧ i ∉ DeclaredChange(Δ_T)
->
PreservationStatus(T,i) = UNRESOLVED
```

when `i` is materially required.

---

# 9. Declared change

Define:

```text
Δ_T = {δ_1, δ_2, ..., δ_n}
```

with each change descriptor:

```text
δ =
<
  property,
  before_constraint,
  after_constraint,
  direction_or_bound,
  scope,
  authority_requirement,
  evidence_requirement
>
```

A declaration of change describes intended semantics. It does not create authority.

```text
δ ∈ Δ_T
!-> AuthorizedChange(T,δ,C,A)
```

For protected residuals, `RESOLUTION_CLOSURE_AND_REOPENING.md` remains governing:

```text
protected residual worsens
∧ no AuthorizedExchange
->
transform result cannot support valid closure
```

---

# 10. Provenance effect

Define:

```text
Π_T(P,s,s',E_T | C,A) = P'
```

with:

```text
P <=_P P'
```

Successful execution records at minimum:

```text
Transform identity / version
input-State provenance reference
active Context
active Authority
input-requirement evidence
declared preserved obligations
declared changes and their authority
output-guarantee evidence
resulting State reference
closure effect, if any
```

Failure also extends provenance and retains what was attempted, why it failed, which requirements resolved, and which Context and Authority were active.

Therefore:

```text
failure
!-> provenance deletion

reversal
!-> provenance erasure
```

---

# 11. Failure contract

The canonical failure object is:

```text
F =
<
  code,
  unmet_or_violated_obligations,
  evidence,
  ρ_failure,
  provenance
>
```

Core 0.1 defines the following minimum failure classes:

```text
INPUT_REQUIREMENT_UNRESOLVED
INPUT_REQUIREMENT_INVALID
AUTHORITY_FAILURE
CONTEXT_FAILURE
INVARIANT_VIOLATION
PROVENANCE_FAILURE
OUTPUT_GUARANTEE_FAILURE
PROTECTED_RESIDUAL_VIOLATION
COMPOSITION_FAILURE
```

Failure code and public resolution state are distinct.

```text
failure code
!=
resolution state
```

The public state is derived from retained evidence through the active four-state resolution algebra.

---

# 12. Reversibility

`R_T` is one of:

```text
REVERSIBLE
PARTIALLY_REVERSIBLE
IRREVERSIBLE
```

## 12.1 Reversible

`T` is REVERSIBLE over scope `Ω` only when an inverse Transform `T^-1` is declared and:

```text
StateEquivalent_Ω(
  Apply(T^-1, Apply(T,s)),
  s
)
```

for every applicable `s` in the declared reversible domain.

The inverse must satisfy this full Transform contract.

State restoration does not restore provenance to an earlier value.

```text
StateEquivalent_Ω(s'',s)
∧
P <_P P''
```

may both hold.

## 12.2 Partially reversible

`T` is PARTIALLY_REVERSIBLE when the inverse is valid only over an explicit subset, projection, Context, Authority, or evidence condition.

The reversible scope and conditions must be explicit.

## 12.3 Irreversible

`T` is IRREVERSIBLE when no inverse satisfying the declared State-equivalence obligation exists.

```text
compensation
!=
reversal
```

---

# 13. Identity Transform

For scope `Ω` define:

```text
Id_Ω
```

with:

```text
τ_Id(s) = s
Δ_Id = ∅
K_Id = all materially relevant properties in Ω
R_Id = REVERSIBLE
Id_Ω^-1 = Id_Ω
C_Id = NON_CLOSING
```

The identity Transform preserves State semantics. Its execution may still append an execution record to provenance.

Therefore the identity laws are State-semantic:

```text
StateEquivalent(
  Apply(Id_Ω, Apply(T,s)),
  Apply(T,s)
)

StateEquivalent(
  Apply(T, Apply(Id_Ω,s)),
  Apply(T,s)
)
```

while provenance retains the ordered execution trace.

---

# 14. Composition

For:

```text
T1 : s0 -> s1
T2 : s1 -> s2
```

define:

```text
T2 ∘ T1
```

only when:

```text
Composable(T2,T1 | C,A)
```

holds.

## 14.1 Composition legality

`Composable(T2,T1 | C,A)` is VALID only when all materially required conditions below are established.

### C1. First Transform applicability

```text
Applicable(T1,s0 | C,A)
```

must hold.

### C2. Second Transform applicability after T1

If:

```text
Apply(T1,s0 | C,A) = APPLIED<s1,E1,P1>
```

then:

```text
Applicable(T2,s1 | C,A)
```

must hold.

Static guarantee entailment may discharge a second-stage requirement:

```text
G_T1 ⊨ q
∧ q ∈ Req_T2
->
q is satisfied by T1 output guarantee
```

Otherwise the requirement must be validated from the produced intermediate State and evidence.

### C3. Boundary compatibility

The intermediate boundary must satisfy the current six-witness model:

```text
IDENTITY
STATE
CONTEXT
AUTHORITY
INVARIANT
PROVENANCE
```

No Transform composition bypasses boundary validation.

### C4. Invariant and declared-change compatibility

Every materially required invariant across the composite is preserved or explicitly changed under valid authority.

### C5. Provenance composability

```text
Π_T2(Π_T1(P,...),...)
```

must be defined and preserve both Transform records in order.

### C6. Protected residual conservation

```text
ProtectedResidualAffected(T1 or T2)
->
ProtectedResidualConservation holds
∨ AuthorizedExchange exists
```

### C7. Closure-epoch legality

A closed resolution epoch is not silently extended by a later material Transform.

If T1 produces actual closure and T2 materially changes active evidence, State, protected residuals, Context, or Authority:

```text
T2 after closure
->
Reopen condition must hold
->
new resolution epoch
```

### C8. Failure propagation

If T1 returns FAILURE, T2 cannot consume its result unless T2 explicitly declares the failure object as an accepted input type.

A composition cannot manufacture an APPLIED result by ignoring a failed required prefix.

---

# 15. Composite execution

When composition is legal:

```text
Apply(T2 ∘ T1, s0 | C,A)
=
Apply(
  T2,
  StateOf(Apply(T1,s0 | C,A))
  | C,A
)
```

Composite provenance is ordered:

```text
P0
<_P
P1
<_P
P2
```

The final guarantees include `G_T2` and any `G_T1` guarantees proven preserved through T2.

```text
g ∈ G_T1
∧ g ∉ K_T2
∧ g not re-established by G_T2
->
g is not a composite guarantee
```

Composition is ordered:

```text
T2 ∘ T1
!=
T1 ∘ T2
```

in general.

For legally typed compositions under unchanged Context and Authority:

```text
(T3 ∘ T2) ∘ T1
≡_State
T3 ∘ (T2 ∘ T1)
```

while provenance preserves the same ordered Transform sequence.

---

# 16. Backward projection rule

The Core invariant is normative:

```text
property(T(s))
!-> property(s)
```

If:

```text
Apply(T,s) = APPLIED<s',E,P'>
∧ Holds(p,s')
```

then `Holds(p,s)` may be asserted only when at least one explicit rule establishes the backward relation, such as preservation, a valid inverse/backprojection theorem, or independent evidence.

Output production alone is insufficient.

---

# 17. Closure-producing Transforms

The closure effect is:

```text
C_T ∈ {
  NON_CLOSING,
  CLOSURE_PRODUCING
}
```

`CLOSURE_PRODUCING` means successful application may place the resolver in a State where the terminal contract can be satisfied. It does not grant closure by declaration.

Actual closure requires:

```text
Apply(T,s) = APPLIED<s',E,P'>
∧
Terminal_Θx(q')
∧
ProtectedResidualConservation
```

under `RESOLUTION_CLOSURE_AND_REOPENING.md`.

Therefore:

```text
C_T = CLOSURE_PRODUCING
!-> closure
```

Later material evidence may reopen the result under the existing reopening rules.

---

# 18. Interaction with trajectory admissibility

For:

```text
π = <s0,T1,s1,...,Tn,sn>
```

Transform validity requires:

```text
∀Ti ∈ π:
  Applicable(Ti,s_(i-1) | C,A)

∧

∀ adjacent Ti,T_(i+1):
  Composable(T_(i+1),Ti | C,A)
```

before the trajectory can claim admissibility from Transform semantics.

Transform validity alone does not establish whole-trajectory admissibility.

---

# 19. Minimal conformance examples

## 19.1 Legal composition

If T1 guarantees `p`, T2 requires `p`, all six boundary witnesses validate, protected invariants are preserved or authorized, and provenance composition is defined, then `T2 ∘ T1` may be composable subject to the remaining composition conditions.

## 19.2 Illegal invariant change

```text
i is protected
i ∈ Δ_T1
no AuthorizedChange(T1,i,C,A)
```

prevents T1 from supporting a valid admissible trajectory across that invariant.

## 19.3 Output does not back-project

```text
p in output
!-> p in input
```

without preservation, inversion, backprojection, or independent evidence.

## 19.4 Reversal preserves history

If T is REVERSIBLE and the inverse restores State equivalence, provenance still records:

```text
s0
-> T
-> s1
-> T^-1
-> s2
```

## 19.5 Closure and reopening

```text
closed epoch
-> admissible material evidence
-> Reopen
-> new epoch
```

The prior closure receipt remains in provenance.

---

# 20. Core A5 invariants

```text
A5-1  defined(T) != applicable(T,s)

A5-2  successful output guarantees are explicit

A5-3  preservation is explicit; silence is not preservation evidence

A5-4  declared change != authorized change

A5-5  provenance grows through success, failure, reversal, and composition

A5-6  Transform failure != public resolution state

A5-7  reversible != provenance-erasing

A5-8  identity preserves State semantics while provenance may grow

A5-9  composition requires six-witness boundary compatibility

A5-10 composition preserves ordered provenance

A5-11 property(T(s)) !-> property(s) without an explicit backward rule

A5-12 closure-producing != automatically closed

A5-13 material post-closure transformation requires legal reopening

A5-14 protected residual sacrifice requires explicit authorized exchange
```

---

# 21. Structural proof-rule interaction

Proof-context transformations used to establish applicability, composition, preservation, substitution, or closure obligations are governed by `STRUCTURAL_PROOF_RULES.md`.

In particular:

```text
exchange !-> reorder noncommuting Transforms

cut !-> bypass intermediate Transform failure

substitution !-> replace Transform input identity/type/scope without a VALID witness

weakening after closure !-> preserve the prior closed conclusion when the added evidence is material

contraction !-> merge independent execution evidence or provenance records
```

A5 Transform legality therefore depends on both the Transform contract and valid A8 structural proof operations.

---

# 22. Resolution-transition interaction

A successful Transform may change the material resolution basis. Public-state changes caused by Transform results are governed by `RESOLUTION_TRANSITION_SEMANTICS.md`.

```text
TransformResult
+ admitted material effect
-> recompute ρ
-> Project_Q(ρ)
-> witnessed public-state transition, if classification changes
```

A Transform failure does not directly assign `VALID`, `PARTIAL`, `UNRESOLVED`, or `INVALID`. Its retained evidence participates in the normal A9 transition and projection rules.

---

# 23. A5 release evidence boundary

This document supplies the canonical Transform semantics required by Core 0.1 A5.

The repository audit may establish that the required contract elements and cross-links are present and internally referenced.

The A5 PASS checkbox remains a maintainer decision under `CORE_0.1_COMPLETENESS_CHECKLIST.md`.
