# Resolution Transition Semantics

**Status:** Canonical Set Calculus Core 0.1 resolution-transition contract  
**Scope:** Public resolution-state transitions, reclassification, supersession, reopening, material cause, and provenance preservation  
**Applies to:** Set Calculus Core

---

# 1. Purpose

Set Calculus has four public resolution states:

```text
UNRESOLVED
PARTIAL
VALID
INVALID
```

This document defines when the active resolution may move from one public state to another.

A public-state transition is never a label replacement.

It is the result of:

```text
prior resolution basis
+ explicit material cause
+ recomputation under the active rules
+ preserved proof history
->
new resolution state
```

The central Core 0.1 law is:

```text
state change
requires
material cause
```

and:

```text
conclusion change
never deletes
proof history
```

---

# 2. Public state and internal evidence state

The internal evidence state remains:

```text
ρ = <P,N,C>
```

where:

```text
P = established positive support
N = established negative support
C = completeness of materially required resolution
```

The public state is the deterministic projection:

```text
σ = Project_Q(ρ)
```

under the active rule profile `Q`.

Therefore:

```text
same ρ
+ same Q
->
same σ
```

A transition between public states must be justified by a change to the material resolution basis or to the valid rule profile used to project that basis.

---

# 3. Resolution configuration

Define the transition-relevant resolution configuration:

```text
q =
<
  id_x,
  E,
  ρ,
  σ,
  Ctx,
  Auth,
  Q,
  epoch,
  closure,
  P
>
```

where:

```text
id_x    = target identity
E       = admitted evidence
ρ       = internal evidence state
σ       = public state
Ctx     = active Context
Auth    = active Authority
Q       = active rule profile / version
epoch   = active resolution epoch
closure = active closure receipt, if any
P       = accumulated provenance
```

The transition relation is:

```text
q_n
--m-->
q_(n+1)
```

where `m` is the material transition cause.

---

# 4. Material transition cause

Define:

```text
m =
<
  kind,
  subject,
  scope,
  before_ref,
  after_ref,
  authority,
  evidence,
  provenance
>
```

The Core 0.1 material-cause kinds are:

```text
NEW_MATERIAL_EVIDENCE
EVIDENCE_CORRECTION
VALID_SUPERSESSION
TRANSFORM_RESULT
CONTEXT_CHANGE
AUTHORITY_CHANGE
RULE_PROFILE_CHANGE
```

These kinds describe what materially changed in the active resolution basis.

Reopening and reclassification are transition operations produced from a valid cause. They are not permission to change a state without one.

---

# 5. Materiality

A cause is material only when it can affect at least one active resolution obligation.

Define:

```text
Material(m,q)
```

when the cause can alter one or more of:

```text
positive support P
negative support N
resolution completeness C
witness validity
dependency validity
identity compatibility
Context compatibility
Authority applicability
rule applicability / precedence
provenance validity
Transform applicability or result
protected residual status
terminal-contract satisfaction
closure / reopening status
```

A change that has no possible effect on any active obligation is immaterial to the current resolution.

```text
Immaterial(m,q)
->
public state must not change because of m
```

Immaterial evidence remains recordable in provenance.

---

# 6. New material evidence

For evidence `e` to support a resolution transition:

```text
Admissible(e,Q)
∧ Relevant(e,id_x,scope)
∧ Material(e,q)
```

must hold.

New evidence does not automatically change the public state.

It changes the evidence basis, after which the resolver recomputes:

```text
E' = E + e
ρ' = ResolveEvidence(E' | Ctx,Auth,Q)
σ' = Project_Q(ρ')
```

If:

```text
σ' = σ
```

the configuration changed but no public-state reclassification occurred.

If:

```text
σ' != σ
```

a transition record is required.

---

# 7. Evidence correction

Evidence correction does not erase the corrected evidence.

Define:

```text
Correct(e_old,e_new,w)
```

only when:

```text
CorrectionWitnessValid(w)
∧ SameEvidenceSubject(e_old,e_new)
∧ CorrectionScopeExplicit(w)
∧ AuthorityValid(w)
∧ ProvenanceValid(w)
```

The prior evidence remains in provenance as superseded or corrected history.

```text
correction
!= deletion
```

The active evidence basis may use the corrected evidence after the correction witness validates.

---

# 8. Valid supersession

Define:

```text
Supersede(b_old,b_new,w_s)
```

where `b_old` and `b_new` may be evidence, a rule, a witness, a closure receipt, or another resolution basis object.

Valid supersession requires:

```text
SupersessionRelationExplicit(w_s)
∧ ScopeOverlapValid(w_s)
∧ AuthorityValid(w_s)
∧ ProvenanceValid(w_s)
∧ NewBasisEligible(b_new)
∧ PrecedenceJustifies(b_new,b_old)
```

Supersession changes which basis is active.

It does not rewrite history.

```text
Superseded(b_old)
∧ b_old ∈ provenance
```

must both remain true after valid supersession.

---

# 9. Reclassification

Reclassification is the public-state change produced by recomputation after a valid material cause.

Define:

```text
Reclassify(q_n,m,q_(n+1))
```

iff:

```text
Material(m,q_n)
∧ CauseAdmissible(m)
∧ ResolutionBasisUpdated(q_n,m,q_(n+1))
∧ ρ_(n+1) = ResolveEvidence(Basis(q_(n+1)))
∧ σ_(n+1) = Project_Q(ρ_(n+1))
∧ σ_(n+1) != σ_n
∧ TransitionWitnessRecorded
∧ P_n <=_P P_(n+1)
```

Therefore:

```text
manual relabeling
!= reclassification
```

and:

```text
same material basis
+ same rule profile
->
same public state
```

---

# 10. Transition witness

Every public-state change produces a transition witness:

```text
W_transition =
<
  target_identity,
  from_state,
  to_state,
  cause,
  before_basis,
  after_basis,
  ρ_before,
  ρ_after,
  Context_before,
  Context_after,
  Authority_before,
  Authority_after,
  rule_profile_before,
  rule_profile_after,
  epoch_before,
  epoch_after,
  closure_effect,
  supersession_refs,
  proof_refs,
  provenance
>
```

The witness must make the state change reconstructible.

A transition lacking a reconstructible witness is not a valid Core transition.

---

# 11. Public-state transition matrix

Every off-diagonal transition among the four public states is conditionally legal when the stated material conditions are satisfied and recomputation projects to the destination state.

| From | To | Minimum transition condition |
|---|---|---|
| UNRESOLVED | PARTIAL | new or corrected admissible material evidence resolves at least one required positive obligation while at least one materially required obligation remains unresolved and no decisive invalidation governs |
| UNRESOLVED | VALID | admissible material evidence, valid supersession, Transform result, or rule/context/authority change yields a positively resolved state under the active rule profile |
| UNRESOLVED | INVALID | admissible material evidence, valid supersession, Transform result, or rule/context/authority change yields decisive invalidation under the active rule profile |
| PARTIAL | UNRESOLVED | previously active partial support is validly corrected, superseded, made inapplicable, or placed into unresolved conflict so that positive partial resolution no longer holds |
| PARTIAL | VALID | remaining material obligations resolve sufficiently for positive resolution under the active rule profile |
| PARTIAL | INVALID | new material evidence or another valid cause establishes decisive invalidation |
| VALID | PARTIAL | a valid material cause defeats terminality or positive completeness while preserving some positively resolved structure |
| VALID | UNRESOLVED | a valid material cause defeats the governing positive resolution and leaves no sufficient partial positive projection, including unresolved decisive conflict |
| VALID | INVALID | a valid material cause plus recomputation yields decisive negative resolution; an active closure, if present, is reopened before the new classification becomes active |
| INVALID | UNRESOLVED | the decisive negative basis is validly corrected, superseded, or made inapplicable, and the remaining evidence is insufficient for PARTIAL or VALID |
| INVALID | PARTIAL | the decisive negative basis is validly corrected, superseded, or made inapplicable while some positive obligations remain resolved and others remain open |
| INVALID | VALID | valid correction, supersession, new material evidence, Transform result, or rule/context/authority change removes the governing invalidation and recomputation yields positive resolution |

Self-state updates:

```text
UNRESOLVED -> UNRESOLVED
PARTIAL    -> PARTIAL
VALID      -> VALID
INVALID    -> INVALID
```

are configuration updates rather than reclassifications.

They may still require provenance when the underlying basis changed.

---

# 12. Transition laws by source state

## 12.1 From UNRESOLVED

### UNRESOLVED -> PARTIAL

```text
σ_n = UNRESOLVED
Material(m,q_n)
ρ_(n+1) contains positive resolved structure
material obligations remain unresolved
no decisive invalidation governs
Project_Q(ρ_(n+1)) = PARTIAL
------------------------------------------------
UNRESOLVED -> PARTIAL
```

### UNRESOLVED -> VALID

```text
σ_n = UNRESOLVED
Material(m,q_n)
Project_Q(ρ_(n+1)) = VALID
------------------------------------------------
UNRESOLVED -> VALID
```

### UNRESOLVED -> INVALID

```text
σ_n = UNRESOLVED
Material(m,q_n)
Project_Q(ρ_(n+1)) = INVALID
------------------------------------------------
UNRESOLVED -> INVALID
```

---

# 13. From PARTIAL

## 13.1 PARTIAL -> UNRESOLVED

This transition requires loss of the active basis for partial positive resolution.

The prior support is not deleted.

One of the following must occur:

```text
valid evidence correction
valid supersession
dependency invalidation
provenance invalidation
Context or Authority inapplicability
unresolved decisive conflict
```

and recomputation must yield:

```text
Project_Q(ρ_(n+1)) = UNRESOLVED
```

## 13.2 PARTIAL -> VALID

```text
σ_n = PARTIAL
Material(m,q_n)
Project_Q(ρ_(n+1)) = VALID
------------------------------------------------
PARTIAL -> VALID
```

The unresolved remainder must be discharged or rendered immaterial under a valid rule.

## 13.3 PARTIAL -> INVALID

```text
σ_n = PARTIAL
Material(m,q_n)
Project_Q(ρ_(n+1)) = INVALID
------------------------------------------------
PARTIAL -> INVALID
```

A partial positive structure does not block later decisive invalidation.

---

# 14. From VALID

VALID does not imply permanence.

If an active closure receipt exists, the reopening contract in `RESOLUTION_CLOSURE_AND_REOPENING.md` governs before a non-VALID classification becomes active.

## 14.1 VALID -> PARTIAL

```text
σ_n = VALID
Material(m,q_n)
active closure implies Reopen(C_k,m)
Project_Q(ρ_(n+1)) = PARTIAL
------------------------------------------------
VALID -> PARTIAL
```

## 14.2 VALID -> UNRESOLVED

```text
σ_n = VALID
Material(m,q_n)
active closure implies Reopen(C_k,m)
Project_Q(ρ_(n+1)) = UNRESOLVED
------------------------------------------------
VALID -> UNRESOLVED
```

## 14.3 VALID -> INVALID

```text
σ_n = VALID
Material(m,q_n)
active closure implies Reopen(C_k,m)
Project_Q(ρ_(n+1)) = INVALID
------------------------------------------------
VALID -> INVALID
```

This may occur when new material evidence establishes decisive negative support, when prior positive evidence is validly superseded, or when a materially governing Context, Authority, provenance, or rule condition changes.

The old VALID proof remains reconstructible.

---

# 15. From INVALID

INVALID is a resolved public classification under its active basis. It is not an instruction to erase contrary or later evidence.

## 15.1 INVALID -> UNRESOLVED

```text
σ_n = INVALID
Material(m,q_n)
governing negative basis no longer validly decisive
Project_Q(ρ_(n+1)) = UNRESOLVED
------------------------------------------------
INVALID -> UNRESOLVED
```

## 15.2 INVALID -> PARTIAL

```text
σ_n = INVALID
Material(m,q_n)
governing negative basis no longer validly decisive
positive resolved structure remains
Project_Q(ρ_(n+1)) = PARTIAL
------------------------------------------------
INVALID -> PARTIAL
```

## 15.3 INVALID -> VALID

```text
σ_n = INVALID
Material(m,q_n)
governing negative basis is validly corrected, superseded, or defeated under the active rules
Project_Q(ρ_(n+1)) = VALID
------------------------------------------------
INVALID -> VALID
```

The prior invalidation remains provenance-bearing even when superseded.

---

# 16. Reopening

Reopening applies to an active closure receipt, not to a public-state label by itself.

Therefore:

```text
VALID
!-> necessarily closed

INVALID
!-> necessarily closed
```

and:

```text
closed
!-> permanently immutable
```

When `Active(C_k)` holds and a new admissible material cause makes the terminal contract false:

```text
Reopen(C_k,m)
```

must occur before a new nonterminal active resolution configuration is installed.

Reopening:

```text
supersedes the active closure receipt
preserves the old receipt
starts a new resolution epoch
recomputes the active public state
```

Reopening itself does not choose the new public state.

```text
REOPEN != PARTIAL
REOPEN != UNRESOLVED
REOPEN != INVALID
```

The four-state projection chooses the state.

---

# 17. Reclosure

After reopening, later material evidence may again satisfy the terminal contract.

Then:

```text
epoch k
-> closure C_k
-> material cause
-> reopen
-> epoch k+1
-> new terminal prefix
-> closure C_(k+1)
```

with:

```text
C_k <_P C_(k+1)
```

Both receipts remain reconstructible.

Reclosure is not restoration of the old closure receipt.

It is a new closure event under a later evidence horizon.

---

# 18. Rule-profile, Context, and Authority changes

A rule-profile, Context, or Authority change may be a material transition cause only when the change is itself validly authorized and provenance-bearing.

Define:

```text
RuleProfileChange(Q_old,Q_new,w)
ContextChange(C_old,C_new,w)
AuthorityChange(A_old,A_new,w)
```

with explicit witness `w`.

A changed interpretation with no recorded rule, Context, Authority, evidence, or supersession basis is not a material cause.

```text
different conclusion
because "reevaluated"
!= valid transition
```

---

# 19. Transform-caused transitions

A successful A5 Transform may materially change the resolution basis.

For:

```text
Apply(T,s | C,A) = APPLIED<s',E_T,P'>
```

the Transform result may cause a resolution-state transition only when:

```text
Transform contract is satisfied
∧ six-witness boundary conditions are satisfied where required
∧ protected residual conservation holds or authorized exchange exists
∧ resulting evidence/state is admitted into the resolution basis
∧ recomputation projects to the new public state
```

A Transform failure does not directly assign a public state.

Its retained failure evidence participates in normal resolution projection.

---

# 20. Structural-proof interaction

A8 structural proof operations may reorganize or compose proof derivations only under `STRUCTURAL_PROOF_RULES.md`.

They cannot create a material transition cause by proof-shape manipulation.

In particular:

```text
weakening !-> silently preserve a conclusion after material evidence

contraction !-> delete independent support or conflict

exchange !-> reorder material transition history

cut !-> hide the material cause of reclassification

substitution !-> replace the target or evidence identity without a valid witness
```

Every transition remains reconstructible through provenance.

---

# 21. Supersession and proof history

When a basis object is superseded:

```text
active(b_old) -> false
active(b_new) -> true
```

may occur.

But:

```text
b_old ∈ provenance
```

remains true.

A later state may therefore disagree with an earlier state without declaring the earlier record nonexistent.

Canonical pattern:

```text
state at horizon n
= VALID

later admissible material cause

state at horizon r
= INVALID

history:
VALID@n
-> cause
-> REOPEN if required
-> INVALID@r
```

The earlier state remains a historical resolution record scoped to its earlier basis.

---

# 22. Determinism

For a fixed normalized transition basis:

```text
same target identity
+ same admitted evidence
+ same Context
+ same Authority
+ same rule profile
+ same Transform results
+ same supersession relations
->
same ρ
->
same public state
```

Therefore:

```text
same basis
!-> different classification
```

without a recorded material difference.

---

# 23. Illegal transitions

A public-state change is INVALID when any of the following holds:

```text
no material cause is recorded

cause is inadmissible

cause is irrelevant to the active resolution

target identity changes without a valid identity/projection witness

rule-profile change lacks authority/provenance

supersession is asserted without valid precedence

active closure is bypassed instead of legally reopened

proof history is deleted

old evidence is erased rather than retained as corrected/superseded history

structural proof manipulation manufactures a new state

Transform output is used despite failed applicability or composition

protected residual violation is hidden

destination state does not equal Project_Q(ρ_after)
```

---

# 24. Minimal transition examples

## 24.1 UNRESOLVED -> PARTIAL

A required object has three material obligations.

Before:

```text
resolved positive obligations = 0
unresolved obligations = 3
state = UNRESOLVED
```

New admissible evidence resolves one obligation positively.

After:

```text
resolved positive obligations = 1
unresolved obligations = 2
no decisive invalidation
state = PARTIAL
```

## 24.2 PARTIAL -> VALID

The remaining required obligations resolve positively and the active rule profile establishes positive resolution.

```text
PARTIAL
-> new material evidence
-> VALID
```

## 24.3 VALID -> UNRESOLVED

A closed VALID result receives admissible material evidence establishing an unresolved decisive conflict.

```text
VALID
-> material evidence
-> Reopen
-> UNRESOLVED
```

The old closure receipt remains in provenance.

## 24.4 VALID -> INVALID

A later admissible material witness establishes decisive invalidation.

```text
VALID
-> material witness
-> Reopen if closed
-> INVALID
```

## 24.5 INVALID -> PARTIAL

The evidence supporting decisive invalidation is validly superseded after a provenance defect is established. Some positive obligations remain established while others remain unresolved.

```text
INVALID
-> valid supersession
-> PARTIAL
```

The invalidating evidence and its supersession record both remain in provenance.

## 24.6 INVALID -> VALID

A valid correction establishes that the governing negative basis referred to the wrong target identity, while the remaining active evidence satisfies positive resolution.

```text
INVALID
-> identity correction witness
-> recompute
-> VALID
```

The earlier INVALID state remains historically reconstructible.

---

# 25. Core A9 invariants

```text
A9-1  public-state change requires a material cause

A9-2  same material basis + same rule profile -> same public state

A9-3  all 12 off-diagonal transitions are conditional, witnessed, and provenance-bearing

A9-4  reclassification is recomputation, not manual relabeling

A9-5  evidence correction never deletes the corrected record

A9-6  supersession changes active basis without erasing prior basis

A9-7  reopening applies to closure receipts, not public-state labels by themselves

A9-8  reopening never chooses the destination public state

A9-9  active closure cannot be bypassed by reclassification

A9-10 Transform failure does not directly assign a public state

A9-11 structural proof operations cannot manufacture a state transition

A9-12 destination state must equal Project_Q(ρ_after)

A9-13 conclusion change never deletes proof history

A9-14 provenance may remain monotone while resolution state changes non-monotonically
```

---

# 26. A9 release evidence boundary

This document supplies the canonical resolution-transition semantics required by Core 0.1 A9.

The A9 audit may establish that the transition matrix, material-cause model, reopening, reclassification, supersession, and provenance requirements are present and integrated.

The A9 PASS checkbox remains a maintainer decision under `CORE_0.1_COMPLETENESS_CHECKLIST.md`.
