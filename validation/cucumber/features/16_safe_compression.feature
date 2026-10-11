Feature: Law XVI - Safe Compression
  Compression preserves distinctions required by every continuation it claims to preserve.

  Scenario: Compressed states remain equivalent across preserved continuations
    Given a compression of two states
    And every preserved continuation maps those states to the same requested result
    When the collative evaluator evaluates Safe Compression
    Then Law XVI holds
    And the compression remains admissible

  Scenario: A preserved continuation separates compressed states
    Given a compression that merges two states
    And a preserved continuation that produces different requested results
    When the collative evaluator evaluates Safe Compression
    Then Law XVI is violated
    And the compression is rejected
    And recursive evaluation restores the distinction
