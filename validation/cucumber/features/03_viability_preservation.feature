Feature: Law III - Viability Preservation
  Valid transformation keeps admissible possibilities inside the viable resolution space.

  Scenario: A transform preserves every viable admissible branch
    Given an admissible possibility space with viable branches
    And a transform whose image remains within the viable resolution space
    When the collative evaluator evaluates Viability Preservation
    Then Law III holds
    And every viable branch remains represented

  Scenario: A transform removes a viable admissible branch
    Given a transform that eliminates a viable admissible possibility
    When the collative evaluator evaluates Viability Preservation
    Then Law III is violated
    And the derived state records viability loss
    And recursive evaluation receives the viability consequence
