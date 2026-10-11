Feature: Law XV - Transformational Resolution
  Admissible convergence can resolve multiplicity without selecting a pre-transform branch.

  Scenario: An admissible transform converges viable branches
    Given multiple viable admissible possibilities
    And a transform that preserves subject, relations, viability, and provenance
    And one requested result after the transform
    When the collative evaluator evaluates Transformational Resolution
    Then Law XV holds
    And the transform resolves the requested multiplicity

  Scenario: Convergence occurs through branch deletion
    Given a transform that produces one requested result by eliminating a viable branch
    When the collative evaluator evaluates Transformational Resolution
    Then Law XV is violated
    And the derived state records destructive convergence
