Feature: Law I - Resolution Relevance
  Resolution follows distinctions that survive into the requested result.

  Scenario: A distinction that changes the requested result requires resolution
    Given two admissible possibilities with different requested results
    When the collative evaluator evaluates Resolution Relevance
    Then Law I holds
    And the distinction is placed inside the active resolution boundary
    And the receipt records the relevant result divergence

  Scenario: An intermediate distinction has no requested-result effect
    Given two admissible possibilities with the same requested result
    When the collative evaluator evaluates Resolution Relevance
    Then the distinction remains dangling
    And no further resolution is required for that distinction
