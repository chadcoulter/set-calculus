Feature: Law XVIII - Equivalence-Admissibility Independence
  Equal requested results and valid transform movement are independent conditions.

  Scenario: Equivalent outcomes arise from an admissible transform
    Given a transform with a singular requested image
    And preservation of subject, required relations, viability, and provenance
    When the collative evaluator evaluates Equivalence-Admissibility Independence
    Then Law XVIII holds
    And transformed closure is valid

  Scenario: Equivalent outcomes arise from a destructive transform
    Given a transform with a singular requested image
    And failure of subject, relation, viability, or provenance preservation
    When the collative evaluator evaluates Equivalence-Admissibility Independence
    Then Law XVIII is violated
    And the transform is inadmissible
    And the closure claim is invalid
