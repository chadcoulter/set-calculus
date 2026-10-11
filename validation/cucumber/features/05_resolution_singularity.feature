Feature: Law V - Resolution Singularity
  Resolution requires a singular relevant image, not a singleton possibility space.

  Scenario: Many possibilities share one requested result
    Given a non-singleton admissible possibility space
    And every possibility maps to one requested result
    When the collative evaluator evaluates Resolution Singularity
    Then Law V holds
    And the request is resolved
    And internal distinctions remain dangling

  Scenario: The relevant image contains multiple results
    Given an admissible possibility space with multiple requested results
    When the collative evaluator evaluates Resolution Singularity
    Then the request remains unresolved
    And recursive evaluation requires further relevant distinction
