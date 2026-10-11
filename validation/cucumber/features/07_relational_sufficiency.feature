Feature: Law VII - Relational Sufficiency
  A requested relationship can resolve while constituent values remain unresolved.

  Scenario: An unresolved pair has a resolved requested relationship
    Given unresolved constituent values
    And a requested relation established across every admissible possibility
    When the collative evaluator evaluates Relational Sufficiency
    Then Law VII holds
    And the requested relation is resolved
    And the constituent uncertainty remains dangling

  Scenario: Constituent uncertainty changes the requested relationship
    Given unresolved constituent values that yield multiple requested relations
    When the collative evaluator evaluates Relational Sufficiency
    Then the relationship remains unresolved
    And recursive evaluation identifies the needed relation evidence
