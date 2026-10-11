# Finite Set Law Validator Harness

This is the first executable slice of the recursive validation epic on
`core-set-calculus-0.2`. It is an external validation application, not a replacement
for Set Calculus Core. It implements finite evidence checks corresponding to all
18 law stories, a collative evaluator, trace receipts, a JSON CLI, and concrete
Cucumber scenarios.

## Find a candidate, then validate

Candidate discovery and validation are independent:

```text
KNOWLEDGE / CAUTIOUS_TRANSFORM / QUICK_CANDIDATE
  -> supplied candidate and finite evidence
  -> evaluate applicable laws against one current-state snapshot
  -> collate compatible consequences or preserve conflict
  -> append receipt and evaluate the derived state
  -> CLOSED / INVALID / UNRESOLVED / CONFLICTED / BOUNDED_UNRESOLVED
```

`QUICK_CANDIDATE` allows discovery before checking preservation. It never changes
the acceptance conditions. The harness does not invent candidates or perform
physical actions; it validates the supplied before/after representation.

## Run

Requires Node.js 24 or later. Install the locked dependency and run:

```sh
cd validation/cucumber
npm ci --ignore-scripts
npm test
npm run validate -- examples/quick-candidate.json
npm run validate -- examples/quick-candidate.json --json
```

The text report lists each pass and law status. `--json` includes the entire trace
with input states, evaluations, evidence, consequences and derived states.
CLI exit codes are 0 for closure, 1 for invalidity, 2 for unresolved/conflicted/
bounded results and 3 for malformed input.

The original 19 abstract `.feature` files remain unchanged. They describe the
target behavior, but lack concrete data and step definitions. The default runner
executes `features/executable/`, where concrete examples cover every law and the
recursive loop. Passing this suite does not certify the abstract epic as complete.

## Input contract

`examples/quick-candidate.json` is a complete finite example. Input is JSON only;
empty initial domains, nonfinite numbers, duplicate ids, unknown transform sources,
missing requested values and malformed partitions are rejected.

* `identity`: the subject identifier.
* `possibility_space`: nonempty admissible rows, each with `id`, `identity`,
  `values`, `relations`, `viable`, and ordered `provenance`.
* `requested_resolution.coordinate`: the supplied outcome coordinate. Its values
  represent the requested result, not necessarily an intermediate observation.
* `required_relations`: relation identifiers which must remain represented.
* `candidate_transform.images`: optional post-transform rows with a `source` id.
  One image per source preserves branch lineage even when state values converge.
  Missing sources are detected as branch loss rather than successful convergence.
* `active_boundary`: represented coordinates; defaults to all represented
  coordinates. An empty boundary is sufficient when every outcome agrees.
* `partition`: blocks of current row ids; defaults to one block. Refinement splits
  crossing blocks without discarding existing distinctions.
* `continuations`: named or unnamed maps with `outcomes` covering every current
  row. `[]` explicitly declares that no remaining continuation needs checking.
  Omission yields UNKNOWN and blocks closure.
* `closure_certificate`: optional `{domain, request, image}` for the current rows.
* `previous_resolution.outcomes`: optional prior row-id/outcome mapping used to
  report reopening and image changes.
* `compression.labels`: optional row-id/label map. Compression must preserve both
  the current requested result and every supplied continuation.
* `causal_record`: optional `cause_removed`, `before_effects`, `after_effects`, and
  a `restoration_evidence` reference when an effect is removed.
* `provenance`, `prior_evaluations`: retained historical records.

## Evaluation semantics

`status` distinguishes PASS, FAIL, UNRESOLVED, UNKNOWN and NOT_APPLICABLE.
The compatibility field `holds` is true for PASS, false for FAIL, and null otherwise.
It describes candidate conformance, not whether a mathematical law is true.
Several laws compute evidence rather than rejecting a state: relevance, relational
sufficiency, coordinate relevance, quotient sufficiency and image invariance.
Multiple requested outcomes mean UNRESOLVED, not a violation of Law V.

Closure requires a singular requested image, complete declared continuation
checks, admissible subject/relation/viability/provenance preservation, a sufficient
partition and boundary, and no failed or unknown applicable evaluations. A finer
sufficient partition is accepted. Boundary minimization is an efficiency operation;
only one redundant coordinate is removed per pass to preserve joint sufficiency.

Every law receives an isolated copy of the same state. Compatible consequences
are applied together; incompatible values produce CONFLICTED and retain the
alternatives rather than selecting by evaluator order. Derived changes are checked
again before closure. Invalidity retains the failed candidate and its evidence; it
does not manufacture an undo operation. Iteration ends at stability, repeated
semantic state, or `maxPasses` (default 32). Full historical receipts are immutable
snapshots; the current state carries compact prior-evaluation references.

## Evidence limits and next work

This validates explicitly supplied finite evidence, not universal proofs over
infinite spaces, authenticated provenance, or the completeness of a future-path
family. Relation identifiers and causal-restoration references are declared
evidence; their real-world truth must be established by a domain adapter.
The harness cannot recover information already erased by an actual compression.

The immediate next work is to freeze the formal JSON schema, map the branch's
law model to current Core contracts on `main`, supply domain-specific proof/evidence
adapters, and turn each original abstract scenario into an independently grounded
example. Laws XII/XIII currently compare domains by row identity; a general
coordinate/joint-relation reopening witness remains to be formalized.
Law I/VII/VIII/XIII are finite diagnostics, not independent theorem proofs.
Closure here is a validator result, not a new Core public resolution state.

The dependency is the official [Cucumber-JS implementation](https://github.com/cucumber/cucumber-js).

## Updated CTRL test-work stories

The next work is specified in
[`docs/epics/ctrl-observability-and-co-transformation-validation.md`](../../docs/epics/ctrl-observability-and-co-transformation-validation.md).
It includes twelve stories with dependencies and acceptance criteria. Companion
Gherkin lives under `features/planned/` with the `@planned` tag. These scenarios
are intentionally outside the executable runner's configured path and are not
included in passing coverage counts. They specify observability, continuity,
partial closure, co-transformed products and extended CTRL law coverage.
