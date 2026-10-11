Feature: Law VI - Quotient Termination
  Resolution reaches the outcome-induced quotient required by the request.

  Scenario: The evaluator reaches the request quotient
    Given a request-relative equivalence relation
    And a current partition equal to the induced quotient
    When the collative evaluator evaluates Quotient Termination
    Then Law VI holds
    And the receipt records the quotient partition

  Scenario: Current partition remains coarser than the request quotient
    Given a current partition whose blocks cross requested result classes
    When the collative evaluator evaluates Quotient Termination
    Then the request remains unresolved
    And the derived state requests refinement of the crossing blocks
