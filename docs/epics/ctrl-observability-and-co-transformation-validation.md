# Epic: CTRL Observability and Co-Transformation Validation

## Goal

Extend the Cucumber validator to evaluate transformations under updated CTRL Book I,
including observable and unobservable relationships, partial closure, retained
co-transformed products, and evidence of relational continuity.

As a researcher, I need to submit a candidate found by any discovery route and
determine what is resolved, what remains open, what transformed with it, and what
evidence supports those conclusions.

This is a work specification. It does not implement new evaluators or claim that
the scenarios below pass. Companion Gherkin is in
`validation/cucumber/features/planned/ctrl_observability.feature` and
`validation/cucumber/features/planned/ctrl_co_transformation.feature`.

## Authority and interpretation

Source: `RED_Sigma_Book_I_CTRL_v0.1_updated.docx`, REDSigma 1.0 Book I, document v0.1.
SHA-256: `7f4684ee87ec448254d9cc7a40ae6f686e18f6944bacd24edf829f3f594757bf`.
Its defining additions are Law 0.1 and Law 28, with corresponding changes to Laws
9, 14, 17, 23, 25, 26 and 27. Laws 0 and 19-27 also extend the existing law registry.

The user's clarification establishes that observability governs both selection
of the resolved portion and establishment of continuity. Observable, relevant,
resolved and admissible must remain distinct. Missing observation is not evidence
of absence or discontinuity. Unobserved relationships can affect the request or
remain dangling when evidence establishes their outcome equivalence.

Field names and scenario predicates below are proposed implementation contracts,
not additional mathematical laws. Continuity means preservation of the declared
required relationship across the traversal; a topological continuity definition
is not assumed.

## Current implementation gaps

| Current behavior | Required work |
|---|---|
| Registry is an array of Laws 1-18 | Stable law ids for 0-28 and translation rule 0.1; explicit applicability and coverage |
| Values and relation ids are supplied without observation scope | Context-bound observation and inference records, including unknown evidence |
| Boundary minimization selects coordinates | Select and witness a request-sufficient portion, retaining its relationship to the remainder |
| One transform image per source | Typed point/set configurations with lineage for branching and convergence |
| Branch counts stand in for viability | Validate represented source-to-product transitions rather than requiring equal counts |
| Closure is one report status | Separate validity, request sufficiency, closure scope and execution boundary |
| No explicit residual state | Retain and carry the co-transformed product as state, not merely a trace string |
| Preservation compares ids and history prefixes | Validate scoped witnesses binding input, output, context, transform and residual |
| A truthy restoration reference permits effect removal | Require an applicable restoring transition with checked evidence |
| Future results are supplied maps | Validate continuation scope and all relevant declared transform alternatives |
| 47 concrete scenarios exercise the first slice | Add independent examples for extended CTRL; account for original abstract scenarios |

## Story CTRL-01: Versioned evidence and status model

As a validator user, I need a versioned input and result contract so that evidence,
closure and validity cannot be mistaken for one another.

Priority: first. Dependencies: none.

Acceptance criteria:

- Introduce named contracts for CoreTransform, EffectiveState, TransformResult,
  Relationship, Observation, ContinuityWitness, ClosureReceipt and Residual.
- Model transform definition separately from its executions. Include identity,
  domain, relational specification, operation, codomain and witness specification.
- Validate identity references and context/request/version scope before evaluation.
- Track observation availability separately from request relevance, evidence
  sufficiency, transform admissibility and portion closure.
- Represent OPEN/PARTIAL/CLOSED closure separately from VALID/PARTIAL/UNRESOLVED/
  CONFLICTED/INVALID logical status. PARTIAL in one axis must not set the other.
- Keep max-depth/repeated-state bounds as execution metadata, not a new CTRL law.
- Provide an explicit migration for legacy fixtures; do not infer observation or
  witnesses from raw value presence.

## Story CTRL-02: Context-bound observability

As a researcher, I need to distinguish a relationship's observation status from
its existence and relevance so that hidden structure is neither deleted nor invented.

Priority: first. Dependencies: CTRL-01.

Acceptance criteria:

- Observation refers to relationship identity, context, observation method,
  evidence horizon and supported value or constraint.
- Distinguish observed, not observed and conflicting evidence. Record whether the
  observation method could expose the relationship in that context.
- Test observable/relevant, observable/irrelevant, unobservable/relevant and
  unobservable/irrelevant relationships as separate fixtures.
- An irrelevant observed relationship need not enter the required closure portion.
- A relevant unobserved relationship blocks certification if its alternatives can
  change the result and no valid constraint or other evidence resolves them.
- A valid relational constraint can establish a requested result without observing
  each constituent. The receipt identifies inference rather than direct observation.
- A context change never silently reuses an out-of-scope observation.

## Story CTRL-03: Select the sufficient portion and retain the remainder

As a researcher, I need observability and request relevance to govern which portion
can close, while retaining all remaining relationships for later transformations.

Priority: first. Dependencies: CTRL-02.

Acceptance criteria:

- Identify S_R, S_K and cross-portion relationship identities for the request.
- Record why each selected relationship is required and how its evidence permits
  the requested distinction to resolve.
- Do not assume S_R equals everything observed or S_K equals everything unobserved.
- Unobserved outcome-equivalent alternatives may remain dangling with their
  equivalence evidence retained.
- Witness coverage of the represented input; no portion or cross-portion relation
  disappears during selection.
- Preserve multiple incomparable sufficient selections; identify the selected
  minimal boundary without claiming it is unique.
- Define whether portions are disjoint actor subsets, coordinate selections or
  relational views before implementing their union and overlap checks.

## Story CTRL-04: Establish relational continuity

As a researcher, I need continuity evaluated from scoped evidence so that loss of
visibility does not masquerade as loss of relationship.

Priority: first. Dependencies: CTRL-02, CTRL-03.

Acceptance criteria:

- Continuity witnesses bind the input/output relationship, transform execution,
  context and preserved invariant or declared change.
- Direct observation and validated transformation evidence are distinct witness kinds.
- Lack of direct observation produces UNKNOWN unless another applicable witness
  establishes continuity or discontinuity.
- A counterexample to a required continuity invariant fails that requirement.
- A changed relation under a permitted transformation is evaluated against its
  declared continuity contract, not rejected solely for unequal visible values.
- Links between S_R and S_K remain represented and checked after traversal.

## Story CTRL-05: Typed actor configurations and lineage

As an implementer, I need branching and convergence to retain lineage without
equating actor count with resolution multiplicity.

Priority: first. Dependencies: CTRL-01.
Law mapping: 0, 3, 4, 19, 21, 24.

Acceptance criteria:

- Supply valid point-to-point, point-to-set, set-to-point and set-to-set examples.
- One source may produce several products; several sources may share a product.
- Every admitted source has a represented transition, and every product references
  its actual source lineage and execution witness.
- Convergence preserves separate histories even with equal visible configurations.
- Missing lineage is distinguished from permitted branching or convergence.
- Domain/codomain violations fail typing rather than being repaired by dropping rows.
- Test a point-to-set result with a singular requested image and another with
  several requested outcomes.

## Story CTRL-06: Scoped partial closure and arrow notation

As a reader or validator user, I need arrows to report closure scope accurately.

Priority: next. Dependencies: CTRL-03, CTRL-04, CTRL-05.
Law mapping: 0.1, 9, 25, 27, 28.

Acceptance criteria:

- An open traversal displays the open arrow (U+2194); invoked partial or complete
  closure displays the directed arrow (U+2192).
- The record independently states PARTIAL versus CLOSED and identifies the portion.
- Partial closure on S_R never certifies full-state closure when S_K remains open.
- Arrows make no claim about mathematical invertibility.
- Reflection/projection records invocation of the necessary partial boundary before
  traversal; missing invocation fails the traversal requirement.
- Invocation is retained as an event; successful certification still requires
  admissibility and sufficiency evidence.

## Story CTRL-07: Co-transform both products

As a researcher, I need boundary traversal to produce the resolved portion and the
co-transformed remainder together rather than dropping or freezing the remainder.

Priority: next. Dependencies: CTRL-05, CTRL-06.
Law mapping: 14, 17, 23, 27, 28.

Acceptance criteria:

- TransformResult contains the pair (S'_R, K') from one execution.
- Include a fixture where K' changes and another where it remains unchanged under
  an explicit transform rule. Unresolved does not imply unchanged.
- Each product retains its lineage, continuity evidence, witness and provenance.
- Reject a candidate that omits a required remainder or replaces it with its witness.
- Cause removal does not erase K'; checked restoration requires another transition.
- A later request can inspect K' without reconstructing discarded information.

## Story CTRL-08: Validate witnesses and restoration claims

As a validator user, I need evidence checked for its specific traversal and scope
so that a label or nonempty reference cannot certify a candidate.

Priority: next. Dependencies: CTRL-01, CTRL-04, CTRL-07.
Law mapping: 17, 22, 23, 24.

Acceptance criteria:

- Reject a witness for a different subject, context, transform execution or product.
- Missing evidence is UNKNOWN; incompatible evidence is CONFLICTED; an established
  violation is INVALID. No missing-data default produces PASS.
- Preserve superseded witnesses with their original scope and horizon.
- A restoration witness binds the restoring transform to the before/after consequence.
- A truthy restoration string alone cannot authorize consequence erasure.
- Historical evidence, current actor state and persistent remainder are independently
  inspectable in the report.

## Story CTRL-09: Compose transformations and continuations

As a researcher, I need the next function to receive the complete effective state,
including the co-transformed remainder and cross-portion relationships.

Priority: next. Dependencies: CTRL-07, CTRL-08.
Law mapping: 14, 16, 21, 26.

Acceptance criteria:

- Check codomain/domain compatibility before composition.
- Carry state, history, witnesses and remainder through both component executions.
- A continuation that separates a dangling distinction reopens only its affected
  portion or joint relation; unrelated certified structure remains intact.
- Compression checks the declared preserved continuation family, not just the
  equality of visible current outcomes.
- An undeclared or insufficiently evidenced continuation family cannot certify
  unrestricted future safety.
- Retain both component executions when the composite visible output equals its input.

## Story CTRL-10: Candidate-first validation and recursive consequences

As a researcher, I need discovery before validation to remain possible without
promoting a candidate to a certified solution prematurely.

Priority: next. Dependencies: CTRL-06 through CTRL-09.
Law mapping: 18, 24, 27, 28.

Acceptance criteria:

- Exercise the same candidate under all three discovery routes with equal evidence;
  route choice alone never changes its validity.
- Store a discovered candidate before running validation. Required boundary invocation
  can be recorded during generation without requiring advance certification.
- Apply consequences to full effective state, then re-evaluate that state.
- Local sufficiency, scoped closure and whole-request validity have separate assertions.
- Conflicting consequences retain both alternatives without evaluator-order selection.
- Termination retains every evaluated pass and reports stable unresolved, invalid,
  sufficient, conflicted, repeated-state or depth-bound outcomes explicitly.

## Story CTRL-11: Stable law registry and applicability coverage

As a maintainer, I need every CTRL position accounted for without confusing an
unimplemented evaluator with an inapplicable law.

Priority: first for coverage infrastructure; finish after CTRL-10.
Dependencies: CTRL-01.

Acceptance criteria:

- Register law ids 0 through 28 plus translation rule 0.1 by explicit id, not array
  index. Attach source version and implementation/coverage state.
- Applicable but unimplemented checks block certification; NOT_APPLICABLE requires
  an evidence-backed applicability decision.
- Revisit diagnostics for Laws 1, 7, 8 and 13: distinguish measured facts from
  validation of a claimed relevance, sufficiency or invariance property.
- Account for each original law scenario, extended law scenario and harness scenario
  in a coverage manifest with planned/implemented/passing status.
- At least one positive, violation/unsupported-claim, and missing-evidence case per
  applicable requirement; conditional laws include an inapplicable case.

## Story CTRL-12: Promote stories to independent executable examples

As a maintainer, I need passing Cucumber results to identify implemented behavior
and leave planned coverage visible.

Priority: final integration. Dependencies: CTRL-01 through CTRL-11.

Acceptance criteria:

- Implement steps using input observations, transitions and witnesses, not preset
  expected result statuses or evaluator-generated fixtures.
- Assert selected portions, products, continuity evidence and receipt scope in
  addition to top-level status.
- Cover false witnesses, lost remainder, hidden relevant relationships, point/set
  expansion, convergence, joint reopening and incompatible composition.
- Keep planned scenarios tagged and outside the default executable path until
  steps and evaluators exist. Report planned counts separately from passing counts.
- Promote completed stories to executable coverage, retaining story id links.
- Keep the existing finite regression suite; use an explicit compatibility adapter
  rather than silently broadening what legacy PASS proves.
- Reconcile current Core contracts on main separately; do not merge the older
  branch wholesale as part of this test work.

## Delivery order

1. Evidence/status contracts and registry accounting: CTRL-01, CTRL-11 foundation.
2. Observability, portion selection, continuity and typed lineage: CTRL-02 to CTRL-05.
3. Partial closure, paired products and scoped witnesses: CTRL-06 to CTRL-08.
4. Composition, continuation and recursive candidate validation: CTRL-09, CTRL-10.
5. Coverage promotion and regression integration: finish CTRL-11, CTRL-12.

## Model decisions to settle during the first stories

- Representation of portions and shared relations, including overlap semantics.
- Concrete observation methods and admissible inference witnesses for the first domain.
- The continuity predicate and evidence required for each transform type.
- What establishes that the declared continuation family covers the requested horizon.
- Mapping between CTRL logical statuses and existing Core public states; scoped
  closure remains a separate axis in either mapping.

These decisions require concrete examples; the stories preserve them explicitly
rather than silently selecting a stronger interpretation of the theory.
