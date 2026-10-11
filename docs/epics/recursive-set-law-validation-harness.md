# Epic: Recursive Set Law Validation Harness

## Goal

Create a Cucumber-based validation project that tests every Set Law against evolving state, applies consequence logic when a law is violated, and recursively evaluates the resulting current state until it reaches closure, invalidity, or a declared recursion boundary.

## Core story

As a Set Calculus researcher or implementer, I need each law expressed as executable behavior so that I can submit a state and transform, see which laws hold, see which consequences follow from violations, and trace recursive resolution across every resulting state.

## Scope

- One Gherkin feature per Set Law.
- A shared state model.
- Law-specific step definitions and evaluators.
- A collative recursive evaluator.
- Provenance-preserving trace records.
- Fixture scenarios for valid, violated, reopened, and recursive states.
- Human-readable result reports.

## State contract

```text
CurrentState
  identity
  possibility_space
  requested_resolution
  relationships
  transform_path
  context
  viability
  provenance
  active_boundary
  resolution_status
  prior_evaluations
```

## Collative recursion

```text
evaluate(current_state)
  -> identify applicable laws
  -> evaluate every applicable law
  -> collect evidence and consequences
  -> derive next current state
  -> append trace receipt
  -> recurse
  -> return closure, invalidity, or boundary result
```

## Law result contract

```text
LawEvaluation
  law_id
  metaphor_name
  holds
  evidence
  violated_constraint
  consequence
  derived_state_changes
  provenance_receipt
```

## Feature structure

```gherkin
Feature: Law II - Transformation Preservation

  Scenario: A transform preserves subject and required relations
    Given an admissible possibility space
    And a requested resolution
    And a transform that preserves the subject and required relations
    When the collative evaluator applies Law II
    Then Law II holds
    And the transform remains admissible
    And the evaluation receipt is retained

  Scenario: A transform produces singularity through destruction
    Given an admissible possibility space with viable branches
    And a transform that removes a required relation
    When the collative evaluator applies Law II
    Then Law II is violated
    And the result is destructive singularity
    And the transform becomes inadmissible
    And the consequence state enters the recursive evaluation trace
```

## Acceptance criteria

- Every Set Law has a dedicated feature file and executable scenarios.
- Every scenario produces a structured evaluation receipt.
- Violations derive explicit consequence states.
- Recursive evaluation receives the full current state after each pass.
- The trace preserves all prior states, transforms, evidence, and provenance.
- Closure identifies a singular relevant image with admissible preservation.
- The project remains an external validation application consuming Set Calculus Core definitions.

## First executable milestone

`validation/cucumber/README.md` documents the finite validator, candidate discovery
routes, evidence limits, CLI, conformance statuses and executable examples.
The original law stories remain specification targets; the concrete suite under
`validation/cucumber/features/executable/` exercises all 18 registered evaluators
and recursive validation. Core contract integration and complete translation of
the abstract stories remain open work.

## Updated CTRL follow-up

See [CTRL Observability and Co-Transformation Validation](ctrl-observability-and-co-transformation-validation.md)
for the next twelve stories and planned Cucumber scenarios covering updated Book I,
observable/unobservable relationships, partial closure, typed actor configurations,
witnesses, co-transformed remainders and continuing graph analysis.
