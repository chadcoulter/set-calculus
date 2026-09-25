# Closure and Reopening Algebra

**Status:** Canonical Set Calculus Core 0.1 closure-layer algebra  
**Scope:** Closure, active closure, evidence extension, reopening, reclosure, epoch order, receipt order, and provenance-preserving composition  
**Applies to:** Set Calculus Core

---

# 1. Purpose

The Core already defines:

```text
first-terminal-prefix stopping
closure receipts
evidence-driven reopening
protected residual conservation
four-state resolution transitions
```

This document defines how those operations compose.

Closure is a layer over resolution history. It is not a fifth public resolution state.

```text
closure state
!=
public resolution state
```

The algebra must determine, from the current closure-layer configuration alone, whether the next closure-layer operation is legal and what history it produces.

---

# 2. Closure-layer configuration

Define the closure-layer configuration:

```text
Λ =
<
  id_x,
  k,
  phase,
  Θ_x,
  Ω,
  h,
  C_active,
  P
>
```

where:

```text
id_x     = target identity
k        = active resolution epoch
phase    ∈ {OPEN, CLOSED}
Θ_x      = terminal contract
Ω        = active rule profile / version
h        = current admitted evidence horizon
C_active = active closure receipt or ∅
P        = accumulated provenance
```

The phase invariant is:

```text
phase = OPEN
iff
C_active = ∅

phase = CLOSED
iff
Active(C_active)
```

A reopening is an event between closure-layer configurations, not a persistent third phase.

---

# 3. Closure receipts

Use the existing receipt form:

```text
C_k =
<
  id_x,
  k,
  n_k^*,
  Θ_x,
  Ω_k,
  S_(n_k^*),
  R_(n_k^*),
  P_(n_k^*),
  W_k
>
```

The receipt is immutable once emitted.

Later provenance may say:

```text
Active(C_k)
Superseded(C_k)
```

but may not rewrite the receipt's original target, epoch, first-terminal horizon, rule profile, State, residual structure, provenance snapshot, or closure witness.

---

# 4. Primitive closure-layer operations

Core 0.1 defines four primitive closure-layer operations:

```text
CLOSE
EXTEND
REOPEN
RECLOSE
```

`RECLOSE` is a semantically named application of `CLOSE` in an epoch created by a prior `REOPEN`.

The algebra also admits an identity operation:

```text
ID_Λ
```

which changes no closure-layer semantics.

---

# 5. CLOSE

Define:

```text
Close(Λ_open,q_n)
```

only when:

```text
Λ_open.phase = OPEN
∧ id(q_n) = Λ_open.id_x
∧ epoch(q_n) = Λ_open.k
∧ Terminal_Θx(q_n)
∧ n = n_k^*
∧ ProtectedResidualConservation(q_(n-1),q_n)
∧ closure witness W_k is valid
∧ provenance through n is reconstructible
```

where:

```text
n_k^*
=
min {
  n |
  n >= start_k
  ∧ Terminal_Θx(q_n)
}
```

The result is:

```text
Close(Λ_open,q_(n_k^*))
=
Λ_closed
```

with:

```text
Λ_closed.phase = CLOSED
Λ_closed.C_active = C_k
Λ_closed.h = n_k^*
P_open <=_P P_closed
```

and the resolver stops active resolution for epoch `k`.

---

# 6. Closure is first-terminal, not arbitrary-terminal

If:

```text
Terminal(q_j)
```

for some `j > n_k^*`, that later terminal horizon cannot replace the original closure horizon.

```text
first terminal prefix
!=
any later terminal prefix
```

Therefore:

```text
Close_k(q_j)
```

cannot emit a second epoch-`k` receipt once `C_k` already exists.

---

# 7. Duplicate closure law

For the same target, epoch, terminal contract, rule profile, and material basis:

```text
Close(CLOSED<C_k>)
=
CLOSED<C_k>
```

as a closure-layer semantic no-op.

It MUST NOT emit:

```text
C_k'
```

as a duplicate closure receipt.

Thus closure is idempotent over an already active identical closure basis:

```text
Close ∘ Close
=
Close
```

only in this no-new-receipt sense.

This law does not authorize closure under changed material evidence.

---

# 8. EXTEND

New admitted evidence may arrive while a closure remains active.

Define:

```text
Extend(C_k,e_r)
```

for `r > n_k^*` when the evidence is admitted into the current history and the terminal contract remains satisfied after incorporation.

The extension result is:

```text
C_active remains C_k
phase remains CLOSED
h becomes r
P grows
```

Formally:

```text
Active(C_k)
∧ Admissible(e_r,Ω)
∧ Terminal_Θx(q_r)
->
Extend(C_k,e_r)
```

with:

```text
P_(r-1) <=_P P_r
```

and:

```text
C_k remains immutable
```

Evidence extension does not produce a new closure receipt.

---

# 9. Irrelevant evidence law

If new evidence is admissible but irrelevant to the target and terminal contract:

```text
Admissible(e_r,Ω)
∧ ¬Relevant(e_r,id_x,Θ_x)
```

then it cannot reopen `C_k`.

It may still be appended to the wider provenance record.

```text
irrelevant evidence
!-> REOPEN
```

---

# 10. REOPEN

Define:

```text
Reopen(C_k,m)
```

only when:

```text
Active(C_k)
∧ CauseAdmissible(m)
∧ Material(m,Λ_closed)
∧ Relevant(m,id_x,Θ_x)
∧ incorporation of m makes Terminal_Θx false
```

The result is:

```text
Λ_closed(k,C_k)
--REOPEN(m)-->
Λ_open(k+1,∅)
```

with:

```text
Superseded(C_k)
C_k ∈ P_(k+1)
phase = OPEN
C_active = ∅
epoch = k+1
P_k <=_P P_(k+1)
```

Reopening does not choose the new public resolution state.

A9 recomputation determines the public state after reopening.

---

# 11. Reopen domain law

REOPEN is defined only for the active closure receipt.

Therefore:

```text
Reopen(OPEN, m)
=
undefined

Reopen(C_superseded, m)
=
undefined
```

A historical closure receipt cannot be reopened a second time after it has already been superseded.

A later material cause operates on the then-current active configuration.

---

# 12. Single-reopen law

For one active receipt `C_k` and one admitted material cause `m`:

```text
Reopen(C_k,m)
```

may supersede `C_k` once.

After that event:

```text
Active(C_k) = false
```

and the same receipt is outside the domain of REOPEN.

This prevents repeated epoch increments from the same already-consumed active closure.

---

# 13. RECLOSE

RECLOSE is closure in an epoch created by reopening.

Given:

```text
Λ_closed(k,C_k)
--REOPEN(m)-->
Λ_open(k+1,∅)
```

and a later first terminal prefix `n_(k+1)^*` satisfying the full closure contract:

```text
Reclose(Λ_open(k+1),q_(n_(k+1)^*))
=
Close(Λ_open(k+1),q_(n_(k+1)^*))
```

emits:

```text
C_(k+1)
```

with:

```text
C_k <_P C_(k+1)
```

Both receipts remain reconstructible.

---

# 14. Reclosure freshness law

Reclosure MUST emit a fresh receipt.

```text
RECLOSE
!=
reactivate C_k
```

and:

```text
C_(k+1)
!=
C_k
```

because at minimum the epoch and evidence horizon differ.

Even if the resulting public state and resolved State are extensionally equivalent to those recorded in `C_k`, the closure event is new.

---

# 15. Epoch monotonicity

Epoch number changes only through REOPEN.

```text
CLOSE:
k -> k

EXTEND:
k -> k

REOPEN:
k -> k+1

RECLOSE:
k+1 -> k+1
```

Thus:

```text
epoch_(n+1) >= epoch_n
```

and:

```text
epoch decreases
```

is not a legal closure-layer transition.

---

# 16. Active-closure uniqueness

For one target identity and one active closure-layer history:

```text
| { C | Active(C) } |
<=
1
```

Two receipts may coexist in provenance.

They may not both be active for the same target history.

```text
historical multiplicity
!=
active multiplicity
```

---

# 17. Closure-history grammar

A valid single-target closure history has the alternating form:

```text
OPEN_0
(
  CLOSE_0
  CLOSED_0
  (
    EXTEND*
    REOPEN_0
    OPEN_1
    CLOSE_1
    CLOSED_1
  )*
)?
```

More compactly:

```text
OPEN
-> CLOSED
-> OPEN
-> CLOSED
-> ...
```

where:

```text
OPEN -> CLOSED
only by CLOSE / RECLOSE

CLOSED -> OPEN
only by REOPEN

CLOSED -> CLOSED
only by EXTEND or closure-layer identity

OPEN -> OPEN
by ordinary resolution work or closure-layer identity
```

No valid history contains:

```text
OPEN -> OPEN by REOPEN

CLOSED -> CLOSED by a new duplicate CLOSE receipt

CLOSED_k -> CLOSED_(k+1) without REOPEN

OPEN_k -> CLOSED_(k+1) without an epoch-k+1 origin
```

---

# 18. Partial composition operator

Let closure-layer events be typed arrows between closure-layer configurations.

Define partial composition:

```text
g ∘_Λ f
```

iff:

```text
codomain(f) = domain(g)
∧ target_identity(f) = target_identity(g)
∧ epoch continuity holds
∧ provenance horizon is nondecreasing
```

For example:

```text
REOPEN_m ∘_Λ CLOSE
```

is defined only when CLOSE produced the active receipt consumed by REOPEN.

And:

```text
RECLOSE ∘_Λ REOPEN_m
```

is defined only when RECLOSE operates in the epoch created by that REOPEN.

---

# 19. Associativity where defined

For legal typed closure-layer operations `f`, `g`, and `h`:

```text
(h ∘_Λ g) ∘_Λ f
=
h ∘_Λ (g ∘_Λ f)
```

whenever both sides are defined.

The resulting closure-layer configuration, active receipt, epoch, and provenance order must agree.

Associativity does not imply commutativity.

---

# 20. Noncommutativity

Closure-layer operations are ordered.

```text
REOPEN ∘_Λ CLOSE
!=
CLOSE ∘_Λ REOPEN
```

and in general the right-hand expression is undefined because REOPEN requires an active closure before CLOSE can consume the reopened epoch.

Likewise:

```text
EXTEND ∘_Λ CLOSE
```

may be defined, while:

```text
CLOSE ∘_Λ EXTEND
```

has a different domain and meaning.

---

# 21. Identity operation

For every legal closure-layer configuration `Λ` define:

```text
ID_Λ : Λ -> Λ
```

such that:

```text
ID_Λ ∘_Λ f = f
f ∘_Λ ID_Λ = f
```

where the compositions are typed.

The identity operation creates no closure receipt, no reopening event, no epoch increment, and no semantic provenance event.

An implementation may record execution metadata externally, but that metadata is not a closure-layer transition.

---

# 22. CLOSE and REOPEN are not inverses

Although:

```text
OPEN
--CLOSE-->
CLOSED
--REOPEN-->
OPEN
```

returns to phase OPEN, it does not return to the original closure-layer configuration.

After REOPEN:

```text
epoch increased
closure receipt C_k remains in provenance
C_k is superseded
evidence horizon increased
material cause is recorded
```

Therefore:

```text
REOPEN ∘_Λ CLOSE
!=
ID_OPEN
```

Similarly:

```text
CLOSE ∘_Λ REOPEN
!=
ID_CLOSED
```

when the latter composition is defined through RECLOSE.

Reclosure emits a new receipt and preserves the superseded one.

---

# 23. No cancellation law

Because CLOSE and REOPEN are not inverses:

```text
g ∘_Λ f = h ∘_Λ f
```

does not generally permit cancellation of `f` by erasing its historical event.

Similarly, a later reclosure cannot cancel the prior reopen event.

```text
historical event composition
is append-only
```

---

# 24. Provenance order

Every non-identity closure-layer event extends provenance.

For successive legal events:

```text
P_0
<=_P
P_1
<=_P
...
<=_P
P_n
```

If event `a` occurs before event `b` in the closure history:

```text
a <_P b
```

The provenance order cannot be rewritten by A8 exchange.

```text
proof-context exchange
!-> closure-history exchange
```

---

# 25. Evidence-horizon order

Within a single target history:

```text
h_(n+1) >= h_n
```

for admitted evidence horizons.

A new closure receipt may reference its own first-terminal horizon, but the global history still preserves the earlier evidence horizons.

A later receipt cannot claim an earlier historical event as newly occurring later.

---

# 26. Closure stability under evidence extension

For active `C_k` and later admitted evidence `e_r`:

```text
Terminal_Θx(q_r)
->
C_k remains active
```

subject to all other active closure conditions, including protected residual conservation.

If incorporation of the evidence causes the terminal contract to fail:

```text
¬Terminal_Θx(q_r)
∧ admissible
∧ material
∧ relevant
->
REOPEN
```

Thus the algebra partitions admitted post-closure evidence into:

```text
closure-preserving extension
or
closure-breaking reopening cause
```

according to the terminal contract after incorporation.

---

# 27. Protected residual law

CLOSE and RECLOSE require Protected Residual Conservation.

```text
CLOSE defined
->
PRC holds

RECLOSE defined
->
PRC holds
```

If later admitted material evidence establishes that a protected residual condition required by the active terminal contract is no longer satisfied:

```text
Active(C_k)
∧ protected residual failure
∧ terminal contract becomes false
->
REOPEN
```

No algebraic composition may hide a protected residual worsening.

---

# 28. Public resolution state is orthogonal

The closure layer and A9 public resolution layer are related but distinct.

Define:

```text
closure phase χ ∈ {OPEN,CLOSED}

public state σ ∈ {
  UNRESOLVED,
  PARTIAL,
  VALID,
  INVALID
}
```

Then the Core configuration may be viewed as carrying:

```text
<χ,σ>
```

subject to the terminal contract.

The algebra does not assert:

```text
CLOSED = VALID
```

or:

```text
INVALID = OPEN
```

A terminal contract may encode the conditions for a resolved negative classification as well as a resolved positive classification.

A9 determines `σ`.

A10 determines closure history `χ` and receipt/epoch legality.

---

# 29. A9 interaction

When REOPEN occurs:

```text
Λ_closed
--REOPEN(m)-->
Λ_open
```

the active public-state basis is recomputed under A9.

A10 supplies:

```text
active receipt supersession
epoch increment
closure-history provenance
```

A9 supplies:

```text
ρ_after
Project_Q(ρ_after)
transition witness
new public state σ_after
```

Neither layer may substitute for the other.

---

# 30. A5 Transform interaction

A Transform declared `CLOSURE_PRODUCING` may propose a configuration eligible for CLOSE.

It cannot directly emit an active receipt unless the A10 CLOSE domain is satisfied.

```text
C_T = CLOSURE_PRODUCING
!-> CLOSE is defined
```

Likewise, a material post-closure Transform effect may trigger REOPEN only through the normal A10 reopening domain and A9 material-cause rules.

---

# 31. A8 structural-proof interaction

A8 structural proof operations cannot rewrite closure algebra history.

In particular:

```text
weakening !-> suppress a material reopen cause

contraction !-> merge distinct closure receipts

exchange !-> reorder CLOSE / REOPEN / RECLOSE history

cut !-> bypass a reopening event

substitution !-> replace closure target identity without a valid witness
```

Closure-layer event order remains provenance-bearing.

---

# 32. Scoped closure non-promotion

A closure receipt proves closure only for its declared target identity, terminal contract, rule profile, evidence horizon, and represented scope.

Therefore:

```text
Closed(scope_a)
!-> Closed(scope_b)

Closed(local scope)
!-> Closed(larger relational scope)
```

without an explicit valid composition rule establishing the larger closure.

Closure does not spread by semantic proximity.

---

# 33. Independent closure composition

Two closures over independent scopes may coexist in provenance:

```text
C_a
C_b
```

Their coexistence does not automatically produce:

```text
C_(a∪b)
```

A larger closure requires its own terminal contract and closure witness.

Thus:

```text
local closures
!-> relational/global closure
```

unless the larger contract explicitly proves that composition.

---

# 34. Minimal algebra examples

## 34.1 Close, extend, remain closed

```text
OPEN_0
-> CLOSE
-> CLOSED<C_0>
-> admissible evidence e_1
-> terminal contract remains true
-> EXTEND
-> CLOSED<C_0>
```

The evidence horizon and provenance grow. No new receipt is emitted.

## 34.2 Close, reopen, reclose

```text
OPEN_0
-> CLOSE
-> CLOSED<C_0>
-> material cause m
-> terminal contract fails
-> REOPEN
-> OPEN_1
-> later first terminal prefix
-> RECLOSE
-> CLOSED<C_1>
```

with:

```text
C_0 <_P C_1
```

## 34.3 Duplicate close rejected

```text
CLOSED<C_0>
-> CLOSE
```

does not emit `C_0'`.

The closure-layer result remains `CLOSED<C_0>` if the basis is unchanged.

## 34.4 Stale receipt cannot reopen

```text
C_0 superseded
C_1 active
```

Then:

```text
Reopen(C_0,m)
=
undefined
```

A material cause must be evaluated against the active configuration.

## 34.5 Reclose is not undo

```text
C_0
-> REOPEN
-> C_1
```

does not erase the middle event.

History remains:

```text
C_0
< reopen event
< C_1
```

---

# 35. Canonical algebra summary

The closure/reopening algebra is the partial algebra:

```text
A_Λ =
<
  Λ,
  CLOSE,
  EXTEND,
  REOPEN,
  RECLOSE,
  ID,
  ∘_Λ
>
```

with laws:

```text
typed partial composition

associativity where defined

identity where typed

noncommutativity

CLOSE idempotence on identical already-closed basis without duplicate receipt

REOPEN domain restricted to active closure

single active closure per target history

single reopen consumption per active receipt

epoch monotonicity

evidence-horizon monotonicity

provenance monotonicity

CLOSE and REOPEN are not inverses

RECLOSE emits a fresh receipt

historical closure events are not cancellable

scope does not expand without proof
```

---

# 36. Core A10 invariants

```text
A10-1  closure phase ∈ {OPEN,CLOSED}

A10-2  reopening is an event, not a persistent closure phase

A10-3  CLOSE is defined only at the first terminal prefix with PRC satisfied

A10-4  identical duplicate CLOSE does not emit a new receipt

A10-5  EXTEND preserves the active receipt when the terminal contract remains true

A10-6  REOPEN is defined only for the active receipt

A10-7  one active receipt can be consumed by REOPEN only once

A10-8  REOPEN increments epoch exactly once

A10-9  RECLOSE emits a fresh receipt in the reopened epoch

A10-10 at most one closure receipt is active for one target history

A10-11 closure-layer event composition is associative where defined

A10-12 closure-layer event composition is not commutative in general

A10-13 CLOSE and REOPEN are not inverses

A10-14 provenance and evidence horizons do not move backward

A10-15 A8 proof operations cannot reorder closure history

A10-16 A9 chooses the public state after reopening

A10-17 CLOSURE_PRODUCING Transform != automatic CLOSE

A10-18 scoped closure does not automatically promote to larger-scope closure
```

---

# 37. A10 release evidence boundary

This document supplies the canonical closure/reopening algebra required by Core 0.1 A10.

The A10 audit may establish that the primitive operations, domains, composition laws, epoch laws, receipt laws, provenance laws, A5/A8/A9 integration, and scope laws are present and linked from the current Core.

The A10 PASS checkbox remains a maintainer decision under `CORE_0.1_COMPLETENESS_CHECKLIST.md`.
