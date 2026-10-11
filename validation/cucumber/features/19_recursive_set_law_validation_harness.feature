Feature: Recursive Set Law Validation Harness
  The harness consumes Set Law feature stories, evaluates every applicable law
  against the current state, collates consequences, and recursively evaluates
  each derived state with preserved provenance.

  Scenario: The harness evaluates all applicable laws against a current state
    Given a current state with identity, possibility space, requested resolution,
      relationships, context, viability, provenance, and an active boundary
    And a registry containing every Set Law evaluator
    When the collative evaluator runs against the current state
    Then every applicable law receives the same current state
    And every law returns a structured LawEvaluation
    And the trace receipt records every evaluation and its evidence

  Scenario: The harness collates compatible law consequences
    Given a current state with multiple applicable laws
    And law evaluations with compatible derived state changes
    When the collative evaluator collates the evaluations
    Then it derives one next current state
    And the next state retains the prior evaluations
    And the trace receipt preserves the input state and derived state

  Scenario: The harness preserves a conflict between law consequences
    Given law evaluations with incompatible derived state changes
    When the collative evaluator collates the evaluations
    Then the resulting state is CONFLICTED
    And both consequence paths remain present in provenance
    And the trace receipt identifies the conflicting law evaluations

  Scenario: The harness reaches valid closure
    Given a current state with a singular requested image
    And every required preservation and admissibility evaluation holds
    When the collative evaluator runs recursively
    Then it returns a closure result
    And the final receipt contains the complete recursive trace

  Scenario: The harness reaches invalidity
    Given a current state with a violated preservation, viability, or provenance law
    When the collative evaluator runs recursively
    Then it returns an invalid result
    And the final receipt identifies the violated constraint and consequence

  Scenario: The harness reaches an explicit recursion boundary
    Given a current state that remains unresolved
    And a declared recursion depth or repeated-state boundary
    When the collative evaluator reaches that boundary
    Then it returns a bounded unresolved result
    And the final receipt preserves the full recursive trace
