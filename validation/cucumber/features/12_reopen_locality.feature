Feature: Law XII - Reopen Locality
  A context shift reopens only the relation responsible for splitting a prior relevant image.

  Scenario: A context shift splits one previously singular relation
    Given a certified dangling domain
    And a context shift that splits one requested relation
    When the collative evaluator evaluates Reopen Locality
    Then Law XII holds
    And recursion reopens the responsible relation
    And unrelated dangling coordinates remain preserved

  Scenario: Reopening discards unrelated resolved structure
    Given a reopening step that resets unrelated coordinates
    When the collative evaluator evaluates Reopen Locality
    Then Law XII is violated
    And the derived state restores preserved unrelated structure
