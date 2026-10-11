Feature: Law VIII - Coordinate Agnosticism
  Any coordinate may remain dangling when its variation preserves the relevant image.

  Scenario: A varying coordinate leaves the requested image singular
    Given a possibility space with an unresolved coordinate
    And coordinate variation that preserves the requested result
    When the collative evaluator evaluates Coordinate Agnosticism
    Then Law VIII holds
    And the coordinate remains dangling

  Scenario: A varying coordinate expands the requested image
    Given a coordinate whose variation changes the requested result
    When the collative evaluator evaluates Coordinate Agnosticism
    Then the coordinate enters the active resolution boundary
    And recursive evaluation requires its refinement
