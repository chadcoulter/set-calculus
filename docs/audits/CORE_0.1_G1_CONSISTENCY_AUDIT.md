# Core 0.1 G1 Legacy Consistency Audit

**Integration base:** `afb8afc6b57e8d9d26803bf370dab5bdcf9bda25` (`main` at integration start)  
**Scope:** repository consistency evidence for \`CORE_0.1_COMPLETENESS_CHECKLIST.md\` gate G1  
**Status:** legacy findings are preserved and explicitly marked historical/superseded on this branch; maintainer review remains required; this document does not mark G1 as passed

## Purpose

G1 requires a repository-wide audit for active contradictions between legacy and current Set Calculus formalization. The required minimum search categories are:

- three-state admissibility as canonical;
- five-witness boundary model;
- \`IDENTITY\` inside a State relation;
- negative-exhaustion requirement;
- obsolete boundary aggregation;
- three-valued witness-validation return type.

This audit preserves the repository's authority boundary. It identifies evidence for maintainer review but does not decide canonical mathematics, rewrite provenance, or change the G1 checkbox.

## Current canonical correction anchors

The current Core contains the following active correction anchors:

- `docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md`, Section 24, separates Identity compatibility from State compatibility.
- Section 24 expands the boundary witness discriminator to six types: Identity, State, Context, Authority, Invariant, and Provenance.
- Section 25 makes PARTIAL a first-class resolution state and defines four-state validation/admissibility/entailment patterns.
- Section 26 labels the current boundary model as the "Six-Witness Four-State Boundary Model."
- Section 27 defines the three-axis resolution profile, independent Decisive Positive / Decisive Negative predicates, constructive positive closure, decisive conflict handling, and tie-break precedence without negative exhaustion.
- `docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md` extends the current resolution model with first-terminal-prefix closure, closure receipts, resolution epochs, evidence-driven reopening, protected residual conservation, and provenance-monotonic history.

These anchors jointly define the current Core behavior used by this audit.

## Current Core integration check

The G1 cleanup is evaluated against the Core as it exists on this branch, including the later closure/reopening formalization.

The integrated consistency conditions are:

```text
Identity != State
PARTIAL != UNRESOLVED
public resolution states = {VALID, PARTIAL, UNRESOLVED, INVALID}
boundary witness dimensions = {IDENTITY, STATE, CONTEXT, AUTHORITY, INVARIANT, PROVENANCE}
DecisivePositive != !DecisiveNegative
DecisiveNegative != !DecisivePositive
constructive positive closure !-> negative exhaustion
reopening changes active resolution state without deleting prior proof/provenance
protected residual worsening requires explicit authorized exchange
```

The closure/reopening layer is consistent with the four-state resolution model: after reopening, the active public state is recomputed by the normal resolution algebra and may become PARTIAL, UNRESOLVED, or INVALID. Historical closure receipts remain preserved in provenance.

The G1 audit therefore treats the early three-state/five-witness material as historical development and the later six-witness/four-state plus closure/reopening structures as the current Core.

## Current findings and branch disposition

All confirmed findings below occur in:

\`docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md\`

### 1. Earlier three-state admissibility remains active-looking

The early trajectory and boundary definitions use only:

\`ADMISSIBLE / INADMISSIBLE / UNRESOLVED\`

The early admissibility-composition table is likewise three-state.

Later Section 25 introduces four-valued admissibility with \`PARTIAL\`, and Section 26 identifies four-state resolution as the current model.

**Baseline classification:** active contradiction candidate. **Branch disposition:** preserved in place and explicitly marked as a historical/superseded three-state baseline.

### 2. Three-valued entailment remains active-looking

Section 14.5 is titled "Three-valued entailment" and defines:

\`ENTAILS / DOES_NOT_ENTAIL / UNRESOLVED\`

Section 25 later defines the domain-specific entailment states as:

\`ENTAILS / PARTIALLY_ENTAILS / UNRESOLVED / DOES_NOT_ENTAIL\`

**Baseline classification:** active contradiction candidate. **Branch disposition:** Section 14.5 is preserved and explicitly marked as a historical baseline superseded by the four-state entailment model in Section 25.

### 3. Five-witness common envelope remains active-looking

Section 21 states:

> All five witness types share a common outer form

and its discriminator contains State, Context, Authority, Invariant, and Provenance, but no Identity.

Section 24 later separates Identity from State and expands the discriminator to six witness types.

**Baseline classification:** direct G1 five-witness finding. **Branch disposition:** the five-witness envelope is preserved and explicitly marked as a historical baseline superseded by the six-witness model.

### 4. Common witness status remains three-state

Section 21 gives the witness status set as:

\`VALID / INVALID / UNRESOLVED\`

Section 25 later defines witness validation as:

\`VALID / PARTIAL / UNRESOLVED / INVALID\`

**Baseline classification:** active contradiction candidate. **Branch disposition:** the three-state witness status is preserved within an explicitly historical five-witness baseline.

### 5. Uniform witness validation returns only three states

Section 22 defines \`ValidateWitness(W)\` with only:

\`VALID / INVALID / UNRESOLVED\`

and later says the typed validator returns those same three values.

Section 25 makes \`PARTIAL\` first-class.

**Baseline classification:** direct G1 three-valued witness-validation finding. **Branch disposition:** Section 22 is preserved and explicitly marked as a historical three-state validation baseline.

### 6. Identity is still handled inside the earlier State witness path

The earlier typed-payload dispatch says:

\`STATE -> identity / compatibility / authorized projection\`

Section 24 later states:

\`IdentityCompat != StateCompat\`

and gives Identity its own witness payload.

**Baseline classification:** direct G1 Identity-inside-State finding. **Branch disposition:** the pre-Identity State witness and validation path are preserved under explicitly historical pre-Identity sections; Section 24 remains the current correction anchor.

### 7. Earlier aggregate boundary evidence contains five witnesses

Section 22.2 constructs \`E_B\` from:

- State
- Context
- Authority
- Invariant
- Provenance

and validates those five components.

Section 24 later expands the boundary evidence object to include Identity as a separate sixth component.

**Baseline classification:** direct G1 obsolete-boundary-aggregation finding. **Branch disposition:** the five-component aggregation is preserved and explicitly marked as a historical baseline superseded by the six-component Identity-aware boundary object.

### 8. Earlier aggregate text still says "all five VALID"

The earlier aggregation rule uses "all five VALID" as the positive boundary condition.

The later six-witness checkpoint supersedes that dimensionality.

**Baseline classification:** direct G1 five-witness/aggregation finding. **Branch disposition:** the wording remains preserved inside the explicitly historical aggregation block.

## Negative-exhaustion search

The targeted search found the later canonical text rejecting negative exhaustion and explicitly describing that assumption as superseded. No separate unmarked rule requiring negative exhaustion was confirmed in this audit pass.

This is not a proof that no such wording exists anywhere. The repository-wide script remains responsible for continuing to search for positive requirement forms.

## Executable branch evidence

The repository-wide audit is enforced by `.github/workflows/core-g1-consistency-audit.yml`.

The workflow watches the Core specification, philosophy/terminology material, this audit report, and the audit script. Because `docs/set-calculus-core/**` is included, later Core files such as `RESOLUTION_CLOSURE_AND_REOPENING.md` are part of the same consistency gate.

A strict run succeeds only when the scanner finds zero `REVIEW_REQUIRED` matches. Historical/superseded material remains visible and is reported separately rather than deleted.

The final PR head must pass the strict audit. The audit result is evidence for G1 review; the G1 checkbox remains under the named maintainer's authority.

## Conservative cleanup path

The least destructive correction is:

1. preserve the earlier derivation;
2. mark incompatible earlier blocks as historical/superseded;
3. point readers directly to Sections 24-27 for the current working model;
4. avoid silently deleting earlier development history;
5. rerun the repository-wide audit;
6. leave the formal G1 PASS decision to the named maintainer.

This approach follows the repository's non-erasure and human-authority rules while removing ambiguity for an independent implementer.

## Reproducible audit tool

Run:

\`\`\`bash
python scripts/audit_core_g1_consistency.py
\`\`\`

Structured output:

\`\`\`bash
python scripts/audit_core_g1_consistency.py --json
\`\`\`

Strict mode returns a nonzero exit code when unmarked review-required candidates remain:

\`\`\`bash
python scripts/audit_core_g1_consistency.py --strict
\`\`\`

The script intentionally classifies findings conservatively:

- \`REVIEW_REQUIRED\` — matched text is not locally marked as historical/superseded;
- \`MARKED_HISTORICAL\` — nearby text explicitly marks the material historical, legacy, obsolete, or superseded;
- \`CONTROL_REFERENCE\` — the match occurs in the checklist, this audit, or the audit script itself.

A clean strict run is evidence for review. It is not, by itself, authority to check G1 PASS.
