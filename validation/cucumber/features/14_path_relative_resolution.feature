Feature: Law XIV - Path-Relative Resolution
  Local singularity remains subject to the relevant remaining transform path.

  Scenario: A local singularity survives every remaining continuation
    Given an intermediate state with a singular local projection
    And a remaining continuation preserving requested equivalence
    When the collative evaluator evaluates Path-Relative Resolution
    Then Law XIV holds
    And the distinction remains safely dangling

  Scenario: A later continuation separates a locally singular distinction
    Given an intermediate state with a singular local projection
    And a remaining continuation that produces multiple requested results
    When the collative evaluator evaluates Path-Relative Resolution
    Then the local closure claim fails
    And recursive evaluation reopens the hidden distinction
