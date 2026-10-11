Feature: Law X - Frontier Navigation
  Resolution traverses relevant distinctions and stops at the coarsest sufficient partition.

  Scenario: Navigation reaches the Enough Boundary
    Given a current partition above the sufficient frontier
    And a refinement path that reaches the coarsest sufficient partition
    When the collative evaluator evaluates Frontier Navigation
    Then Law X holds
    And the request closes at the Enough Boundary

  Scenario: Navigation claims closure while a block crosses result classes
    Given a claimed frontier partition with a block spanning multiple requested results
    When the collative evaluator evaluates Frontier Navigation
    Then Law X is violated
    And the closure claim reopens for further refinement
