Feature: Law IV - Provenance Persistence
  Present convergence retains traversal provenance and historical distinction.

  Scenario: Distinct histories converge into one current state
    Given two possibilities with distinct traversal provenance
    And an admissible transform that converges their current state
    When the collative evaluator evaluates Provenance Persistence
    Then Law IV holds
    And both provenance paths remain reconstructible

  Scenario: A transform claims resolution after erasing evidence
    Given a transform that removes the traversal evidence for a distinction
    When the collative evaluator evaluates Provenance Persistence
    Then Law IV is violated
    And the derived state records provenance loss
    And the claimed resolution is invalid
