Feature: Law IX - Boundary Stability
  The active boundary contains a minimally sufficient coordinate set.

  Scenario: A selected boundary determines the requested resolution class
    Given a coordinate set sufficient for requested resolution
    And no proper subset of that coordinate set is sufficient
    When the collative evaluator evaluates Boundary Stability
    Then Law IX holds
    And the coordinate set becomes the active boundary

  Scenario: An active boundary omits a required coordinate
    Given a boundary whose equality permits different requested results
    When the collative evaluator evaluates Boundary Stability
    Then Law IX is violated
    And the derived state expands the boundary with the required coordinate
