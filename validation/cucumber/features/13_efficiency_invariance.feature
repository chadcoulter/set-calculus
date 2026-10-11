Feature: Law XIII - Efficiency Invariance
  Raw possibility count does not determine required resolution distinction.

  Scenario: Added possibilities remain inside established result classes
    Given an admissible possibility space with a singular requested image
    And additional possibilities inside existing requested result classes
    When the collative evaluator evaluates Efficiency Invariance
    Then Law XIII holds
    And the required resolution multiplicity remains unchanged

  Scenario: Added possibilities create a new requested result class
    Given additional possibilities that enlarge the requested image
    When the collative evaluator evaluates Efficiency Invariance
    Then the request reopens
    And recursive evaluation records the new required distinction
