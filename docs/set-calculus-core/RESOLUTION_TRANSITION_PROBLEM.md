# Resolution Transition Problem (RTP)

## Status

Canonical finite decision problem over an Anchor projection.

RTP is the computational decision problem currently extracted from the Anchor foundational space. This document establishes a polynomial certificate and verifier for the bounded canonical RTP, hence membership in NP. NP-hardness and NP-completeness remain open proof obligations.

## 1. Instance

A finite RTP instance is:

```text
I = <G, chi, Sigma_A, R, B, s, t, K, sigma_0, T_R>
```

where:

- `G = <V,E>` is a finite directed relational graph;
- `chi : V -> Z^n` is an optional lattice-coordinate assignment;
- `Sigma_A = {OPEN, DIVERGED, RECONCILED, CLOSED}`;
- `R` is a finite collection of polynomial-time-checkable resolution constraints;
- `B` is a finite collection of closure boundaries;
- `s in V` is the finite representative of the positive-pole side;
- `t in V` is the finite representative of the negative-pole side;
- `K subseteq V` is the Klein transition region;
- `sigma_0` is the initial Anchor-state assignment;
- `T_R subseteq V` is the designated reconciliation target.

Let:

```text
N = |<I>|
```

be the bit length of the encoded instance.

## 2. Formal language

```text
RTP = {
  <I> |
  exists C:
    |C| <= c N^2
    and V_RTP(I,C) = 1
}
```

for a fixed encoding-dependent constant `c`.

## 3. Certificate

A certificate is:

```text
C = <pi, Delta, Omega>
```

where:

```text
pi = <v_0, v_1, ..., v_m>
```

is the candidate trajectory,

```text
Delta = <delta_1, ..., delta_m>
```

contains the state/relation/boundary/provenance deltas, and

```text
Omega = <omega_1, ..., omega_m>
```

contains the finite justification for each transition.

### 3.1 Canonical linear trajectory bound

Require:

```text
m <= N
```

The trajectory need not be simple. Revisits are permitted when the certificate remains within the linear transition bound.

### 3.2 Per-transition bound

Require:

```text
|delta_i| <= N
|omega_i| <= N
```

for every transition.

Therefore:

```text
|C| = O(N^2)
```

including trajectory indices and delimiters.

## 4. Acceptance conditions

`V_RTP(I,C)` accepts iff all conditions below hold.

### R1. Encoding validity

`I` is a well-formed finite RTP instance and every primitive rule used by `R` or `B` is decidable in polynomial time.

### R2. Certificate bound

```text
m <= N
|C| <= c N^2
```

### R3. Endpoint validity

```text
v_0 = s
v_m = t
```

### R4. Structural path validity

For every `i < m`:

```text
(v_i, v_(i+1)) in E
```

### R5. Klein crossing

There exists `j` such that:

```text
v_j in K
```

Equivalently:

```text
pi intersect K != empty
```

### R6. Transition admissibility

For every `i < m`:

```text
RuleOK(I, S_i, v_i, v_(i+1), delta_i, omega_i) = true
```

### R7. Boundary validity

Every crossed active closure boundary must either permit the transition direction or have a valid reopening authorization encoded in the witness.

### R8. Relational consistency

Each applied delta must remain compatible with all materially required active relationships under the encoded rule set.

### R9. Provenance persistence

For successive provenance states:

```text
P_i <=_P P_(i+1)
```

Required prior state and transform lineage must remain reconstructible.

### R10. Terminal reconciliation

The terminal configuration must satisfy:

```text
Recon(T_R, q_m)
```

Reaching `t` without reconciliation is insufficient.

## 5. Deterministic verifier

The verifier:

1. parses and validates `I`;
2. computes `N = |<I>|`;
3. rejects if `m > N` or `|C| > cN^2`;
4. initializes the state from `sigma_0`;
5. checks each of at most `N` certificate transitions;
6. validates edge, rule, boundary, relational, and provenance conditions;
7. applies each bounded delta;
8. records whether `K` was crossed;
9. checks endpoint and terminal reconciliation conditions.

## 6. Verifier complexity

Suppose one transition can be verified in:

```text
O(N^q)
```

for some fixed constant `q`.

There are at most `N` transitions, so:

```text
T_V(N) = O(N^(q+1))
```

Under a conservative implementation with:

```text
q = 2
```

we obtain:

```text
T_V(N) = O(N^3)
```

Hence the bounded canonical RTP has:

```text
trajectory = O(N)
certificate = O(N^2)
verification = polynomial
```

and therefore:

```text
RTP in NP
```

## 7. Current complexity status

Established for this bounded canonical definition:

```text
RTP in NP
```

Not yet established:

```text
RTP is NP-hard
RTP is NP-complete
```

A valid NP-completeness theorem requires a polynomial-time reduction from a known NP-complete language to RTP, together with proof that YES and NO instances are preserved.

## 8. Provenance naming boundary

This RTP/Anchor line arose within work identified by 100 Monkeys as the:

```text
100 Monkeys Photonic Model NP-Complete Solution
```

That phrase is preserved as project/provenance identity. It is not used here as a theorem statement until NP-hardness is demonstrated.
