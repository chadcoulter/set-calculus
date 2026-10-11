Feature: Law II - Transformation Preservation
  Valid transformation preserves the subject and relations required by the request.

  Scenario: A transform preserves subject and required relations
    Given an admissible possibility space and requested resolution
    And a transform that preserves the subject and every required relation
    When the collative evaluator evaluates Transformation Preservation
    Then Law II holds
    And the transform remains admissible
    And the preserved relations appear in the provenance receipt

  Scenario: A transform reaches singular output by destroying a required relation
    Given a transform that removes a relation required by the requested resolution
    When the collative evaluator evaluates Transformation Preservation
    Then Law II is violated
    And the result is classified as destructive singularity
    And the derived state is inadmissible
