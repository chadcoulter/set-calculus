Feature: Law XVII - Consequence Persistence
  Ending a cause does not reverse the state transformation it already produced.

  Scenario: Cause removal leaves its prior transformed consequence present
    Given a cause that produced a recorded state transformation
    And a later step that removes the cause
    When the collative evaluator evaluates Consequence Persistence
    Then Law XVII holds
    And the prior state transformation remains present
    And reversal requires a separate valid transform

  Scenario: A claim treats cause removal as automatic reversal
    Given a state with a persisted causal consequence
    And a claim that cause removal restores the prior state
    When the collative evaluator evaluates Consequence Persistence
    Then Law XVII is violated
    And recursive evaluation requires evidence of a restoring transform
