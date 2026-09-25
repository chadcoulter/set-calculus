# Structural Proof Rules

**Status:** Canonical Set Calculus Core 0.1 structural proof-rule contract  
**Scope:** Weakening, contraction, exchange, cut, and substitution  
**Applies to:** Core proof contexts, tie-break sequents, Transform reasoning, and provenance-bearing derivations

---

# 1. Purpose

Set Calculus uses provenance-bearing evidence, explicit scope, Context, Authority, identity, ordered Transforms, and unresolved states.

Classical structural proof rules therefore cannot be assumed globally.

For Core 0.1, each required structural rule has exactly one status:

```text
weakening   = RESTRICTED
contraction = RESTRICTED
exchange    = RESTRICTED
cut         = RESTRICTED
substitution = RESTRICTED
```

No unrestricted form of these rules is admitted by default.

---

# 2. Proof context

Use the tie-break sequent form:

```text
Γ ; Q ⊢Ω κ
```

where:

```text
Γ = provenance-bearing evidence/context
Q = active rule profile
Ω = resolved or contested scope
κ = derived result
```

For structural-rule evaluation, model the proof context as:

```text
Γ =
<
  E,
  D,
  O,
  C,
  A,
  P
>
```

where:

```text
E = evidence entries
D = dependency relations among entries
O = materially relevant ordering constraints
C = active Context
A = active Authority
P = provenance graph / trace
```

A structural operation is legal only when it preserves every materially relevant component or records an authorized, explicit change.

---

# 3. General structural-rule law

For any structural operation `S`:

```text
StructuralLegal(S, Γ ; Q ⊢Ω κ)
```

requires:

```text
ScopePreservedOrExplicit(S,Ω)
∧ DependencyIntegrity(S,D)
∧ ProvenancePreserved(S,P)
∧ ContextCompatible(S,C)
∧ AuthorityCompatible(S,A)
∧ IdentityIntegrity(S)
∧ InvariantIntegrity(S)
∧ NoHiddenResolution(S)
∧ NoConflictErasure(S)
```

If any materially required condition is unresolved:

```text
StructuralLegal(S,...) = UNRESOLVED
```

If a required condition is violated:

```text
StructuralLegal(S,...) = INVALID
```

A rule status of `RESTRICTED` means the rule is available only when its rule-specific legality conditions are VALID.

---

# 4. Weakening

## Status

```text
WEAKENING = RESTRICTED
```

Classical weakening would infer:

```text
Γ ⊢ κ
----------------
Γ, e ⊢ κ
```

for arbitrary additional `e`.

That unrestricted form is not admissible in Set Calculus because new admissible evidence can:

```text
change completeness
introduce decisive conflict
change scope
change Authority applicability
change provenance requirements
trigger reopening after closure
```

## 4.1 Restricted weakening rule

```text
Γ ; Q ⊢Ω κ
IrrelevantToConclusion(e,κ,Ω)
DependencyIndependent(e,Derivation(κ))
NoAuthorityChange(e)
NoContextChange(e)
NoIdentityChange(e)
NoProtectedResidualEffect(e)
NoReopenTrigger(e)
------------------------------------------------ WEAKEN
Γ + e ; Q ⊢Ω κ
```

The added evidence remains in provenance.

If any relevance condition cannot be established, the prior conclusion must be re-evaluated under the expanded context.

```text
new material evidence
->
recompute resolution
```

Therefore:

```text
adding evidence
!-> conclusion preservation
```

---

# 5. Contraction

## Status

```text
CONTRACTION = RESTRICTED
```

Classical contraction would infer:

```text
Γ, e, e ⊢ κ
----------------
Γ, e ⊢ κ
```

Set Calculus distinguishes duplicate references from independent evidence that happens to assert the same proposition.

## 5.1 Evidence identity

Define:

```text
SameEvidenceIdentity(e1,e2)
```

only when both entries refer to the same underlying evidence object / occurrence and the same provenance identity.

Semantic equivalence is insufficient.

```text
Claim(e1) = Claim(e2)
!-> SameEvidenceIdentity(e1,e2)
```

Two independent witnesses supporting the same claim remain two witnesses.

## 5.2 Restricted contraction rule

```text
Γ, e1, e2 ; Q ⊢Ω κ
SameEvidenceIdentity(e1,e2)
NoMultiplicitySemantics(e1,e2,κ)
PreserveProvenanceReference(e1,e2)
--------------------------------------------- CONTRACT
Γ, e ; Q ⊢Ω κ
```

Contraction may normalize duplicate references, but it may not collapse:

```text
independent witnesses
distinct source passages
distinct Transform executions
distinct closure receipts
distinct conflict records
distinct temporal observations
```

---

# 6. Exchange

## Status

```text
EXCHANGE = RESTRICTED
```

Classical exchange would permit arbitrary permutation:

```text
Γ1, e1, e2, Γ2 ⊢ κ
-----------------------
Γ1, e2, e1, Γ2 ⊢ κ
```

Unrestricted exchange is invalid where order carries meaning.

Material order includes:

```text
Transform execution order
dependency order
temporal order
causal order
supersession order
closure / reopening epoch order
provenance sequence
```

## 6.1 Restricted exchange rule

```text
Γ1, e1, e2, Γ2 ; Q ⊢Ω κ
Independent(e1,e2)
NoOrderingConstraint(e1,e2)
NoTransformSequenceChange(e1,e2)
NoSupersessionChange(e1,e2)
NoEpochChange(e1,e2)
--------------------------------------------- EXCHANGE
Γ1, e2, e1, Γ2 ; Q ⊢Ω κ
```

This exchanges proof-context presentation only.

It does not rewrite historical provenance order.

```text
proof-context exchange
!=
provenance-history exchange
```

If the provenance trace records `e1` before `e2`, that history remains unchanged.

---

# 7. Cut

## Status

```text
CUT = RESTRICTED
```

The classical form:

```text
Γ ⊢ φ
Γ, φ ⊢ κ
---------------- CUT
Γ ⊢ κ
```

may hide the derivation of `φ` if treated as mere proof compression.

Set Calculus permits cut only as provenance-preserving derivation composition.

## 7.1 Restricted cut rule

```text
Γ1 ; Q1 ⊢Ω1 φ
Γ2, φ ; Q2 ⊢Ω2 κ
ScopeCompatible(Ω1,Ω2)
AuthorityCompatible(Q1,Q2)
ProvenanceValid(Derivation(φ))
DependenciesPreserved(φ)
NoUnresolvedPremiseHidden(φ)
NoConflictHidden(φ)
NoEpochBoundaryBypassed(φ)
------------------------------------------------ CUT
Γ1 ⊕ Γ2 ; Q* ⊢Ω2 κ
```

where `Q*` preserves all materially required restrictions from both derivations.

The cut conclusion retains the complete derivation path:

```text
Γ1
-> φ
-> κ
```

Cut may abbreviate proof presentation.

```text
proof compression
!=
provenance compression
```

A cut is invalid if it makes an intermediate unresolved, partial, conflicting, unauthorized, or provenance-invalid result appear fully established.

---

# 8. Substitution

## Status

```text
SUBSTITUTION = RESTRICTED
```

Substitution requires an explicit valid relation between the replaced and replacement objects.

Define a substitution witness:

```text
W_sub =
<
  source,
  replacement,
  relation,
  scope,
  type,
  Context,
  Authority,
  invariants,
  provenance,
  validity
>
```

## 8.1 Restricted substitution rule

```text
Γ ; Q ⊢Ω κ[x]
ValidateSubstitution(W_sub) = VALID
TypeCompatible(x,y)
IdentityCompatible(x,y,W_sub)
ScopeCompatible(Ω,W_sub.scope)
ContextCompatible(C,W_sub.Context)
AuthorityCompatible(A,W_sub.Authority)
InvariantPreserving(W_sub)
ProvenancePreserving(W_sub)
--------------------------------------------- SUBSTITUTE
Γ + W_sub ; Q ⊢Ω κ[y]
```

Substitution may use a declared equivalence, authorized projection, identity relation, or other explicit relation whose scope supports the replacement.

It may not infer identity from similarity.

```text
equivalent-for-purpose
!=
identical
```

It may not project a Transform-produced property backward onto its input.

```text
property(T(x))
!-> property(x)
```

unless the substitution witness includes a valid backward rule recognized by `TRANSFORM_SEMANTICS.md`.

---

# 9. Rule interaction with the four-state model

Structural-rule applicability itself is evidence-sensitive.

For a proposed structural operation:

```text
VALID
PARTIAL
UNRESOLVED
INVALID
```

retain their current Core meanings.

A structural operation may execute only when its legality resolves to `VALID`.

```text
StructuralLegal(S,...) = PARTIAL
!-> execute S

StructuralLegal(S,...) = UNRESOLVED
!-> execute S

StructuralLegal(S,...) = INVALID
!-> execute S
```

The unresolved or partial structural proof remains representable and provenance-bearing.

---

# 10. Rule interaction with decisive conflict

Structural rules may not decide a conflict merely by changing proof shape.

In particular:

```text
weakening
!-> hide D-

contraction
!-> merge independent D+ / D- witnesses

exchange
!-> reorder precedence history

cut
!-> hide conflicting intermediate result

substitution
!-> replace contested identity without witness
```

Tie-break precedence remains governed by the active conflict calculus.

---

# 11. Rule interaction with Transform semantics

Structural proof operations that reason across Transform boundaries inherit the A5 contract.

Therefore:

```text
structural proof step across T
->
Transform applicability preserved
∧ Transform guarantees preserved
∧ declared-change / authorized-change distinction preserved
∧ six-witness boundary compatibility preserved
∧ provenance continuity preserved
```

Exchange may not reorder noncommuting Transforms.

Cut may not bypass an intermediate Transform failure.

Substitution may not alter Transform input identity, type, scope, or required invariants without a valid substitution witness.

Weakening with material post-closure evidence invokes the reopening rules rather than preserving the old closed conclusion.

---

# 12. Rule interaction with closure and reopening

Closure does not freeze the proof context against material evidence.

```text
closed epoch
+ material admissible evidence
->
Reopen evaluation
```

Therefore restricted weakening after closure is legal without reopening only when the added evidence is proven immaterial to the closure contract and protected residuals.

Cut and substitution may not cross a closure-epoch boundary while concealing the receipt, material reopening cause, or new epoch.

Contraction may not collapse distinct closure receipts.

Exchange may not reorder closure and reopening history.

---

# 13. Structural rule table

| Rule | Core 0.1 status | Legal only when |
|---|---|---|
| Weakening | RESTRICTED | added evidence is proven immaterial to the current conclusion, or the conclusion is recomputed under the expanded context |
| Contraction | RESTRICTED | duplicate entries have the same evidence identity and multiplicity has no semantics |
| Exchange | RESTRICTED | exchanged entries are independent and no material ordering, Transform, supersession, epoch, or provenance constraint changes |
| Cut | RESTRICTED | the intermediate derivation remains fully reconstructible and no unresolved, conflicting, authority, scope, dependency, provenance, or epoch condition is hidden |
| Substitution | RESTRICTED | a VALID typed, scoped, authority-compatible, identity-aware, invariant- and provenance-preserving substitution witness exists |

Exactly one status is declared for each required A8 rule.

---

# 14. Minimal counterexamples

## 14.1 Unrestricted weakening fails

```text
Γ ⊢ VALID

add admissible evidence e establishing D-

Γ,e
->
DecisiveConflict
```

The original conclusion cannot be preserved by weakening.

## 14.2 Unrestricted contraction fails

```text
w1 = independent witness from source A
w2 = independent witness from source B
Claim(w1) = Claim(w2)
```

Collapsing `w1,w2` into one witness destroys evidence multiplicity and provenance.

## 14.3 Unrestricted exchange fails

```text
T1 = open account
T2 = debit account
```

`T2 ∘ T1` may be legal while `T1 ∘ T2` is not. Exchange cannot reorder them.

## 14.4 Unrestricted cut fails

If `φ` is PARTIAL and a later derivation treats `φ` as fully established, cut would manufacture resolution.

```text
PARTIAL φ
!-> established φ
```

## 14.5 Unrestricted substitution fails

If `x` and `y` are state-compatible for one operation but have distinct identity:

```text
CompatibleState(x,y)
!-> Identity(x,y)
```

Substitution of `y` for `x` outside the witnessed compatibility scope is invalid.

---

# 15. Core A8 invariants

```text
A8-1 unrestricted weakening is not admissible

A8-2 unrestricted contraction is not admissible

A8-3 unrestricted exchange is not admissible

A8-4 unrestricted cut is not admissible

A8-5 unrestricted substitution is not admissible

A8-6 proof compression never deletes provenance

A8-7 semantic equality of claims does not imply evidence identity

A8-8 proof-context order may be exchanged only when material order is irrelevant

A8-9 cut preserves intermediate derivation, scope, authority, dependencies, conflict, and epoch information

A8-10 substitution requires an explicit valid witness

A8-11 structural rules cannot manufacture resolution from PARTIAL or UNRESOLVED evidence

A8-12 structural rules cannot bypass Transform or closure/reopening contracts
```

---

# 16. Resolution-transition interaction

Structural proof operations cannot create, suppress, or rewrite a public-state transition merely by changing proof shape.

`RESOLUTION_TRANSITION_SEMANTICS.md` governs any reclassification whose proof basis is affected by weakening, contraction, exchange, cut, or substitution.

```text
structural proof change
!-> material transition cause
```

A valid state change still requires an admissible material cause, recomputation, a transition witness, and provenance preservation.

---

# 17. A8 release evidence boundary

This document supplies the explicit structural proof-rule statuses and restrictions required by Core 0.1 A8.

The A8 audit may establish that all five rules have exactly one declared status, their restrictions are explicit, and the Core cross-links are present.

The A8 PASS checkbox remains a maintainer decision under `CORE_0.1_COMPLETENESS_CHECKLIST.md`.
