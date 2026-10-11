@planned @ctrl @observability
Feature: Observability governs closure selection and evidence of continuity
  These scenarios specify planned behavior and are not in the executable suite.

  @CTRL-02 @CTRL-03
  Scenario: Observable but irrelevant structure stays outside required closure
    Given a delivery request that asks only whether the package arrived
    And arrival is observed with an applicable witness
    And package color is observed but cannot change the delivery result
    When the validator selects the portion necessary for the delivery request
    Then arrival belongs to the required resolution portion
    And color need not be closed for that request
    And the color relationship remains represented in the remainder

  @CTRL-02 @CTRL-03
  Scenario: A hidden relevant relationship prevents unsupported certification
    Given a delivery request that requires the correct recipient
    And the recipient relationship is not observable in the current context
    And its admissible alternatives are Alice and Bob
    And no applicable witness establishes which recipient received the package
    When the candidate claims that delivery to Alice is resolved
    Then recipient sufficiency is unknown
    And the requested closure is not certified
    And both recipient alternatives remain represented

  @CTRL-02 @CTRL-03
  Scenario: A requested relation resolves without constituent observation
    Given actors a and b whose individual values are not observed
    And an applicable constraint witness establishes that a plus b equals 10
    And the request asks only for their sum
    When the validator evaluates the requested relationship
    Then the requested result is 10
    And the receipt identifies constraint evidence rather than direct observation
    And the individual actor values remain dangling

  @CTRL-03
  Scenario: Hidden outcome-equivalent alternatives remain outside required closure
    Given a delivery request that asks only whether the package arrived
    And arrival has an applicable witness
    And the route is not observed
    And witnessed admissible route alternatives north and south both establish arrival
    When the validator selects the sufficient portion
    Then the route alternatives do not require individual resolution
    And their equivalence evidence is retained
    And neither route is deleted from the represented state

  @CTRL-04
  Scenario: Continuity is supported despite loss of direct visibility
    Given an observed ownership relationship before a boundary traversal
    And ownership is not directly observable after the traversal
    And an applicable transition witness establishes preservation of that relationship
    When the validator evaluates relational continuity
    Then continuity is supported by the transition witness
    And direct observation remains unavailable in the resulting context

  @CTRL-04
  Scenario: Missing observation is not proof of continuity or discontinuity
    Given a required relationship that is not observable after a transformation
    And no applicable evidence establishes preservation or destruction
    When the validator evaluates relational continuity
    Then continuity is unknown
    And the relationship is not classified as absent
    And the required continuity obligation prevents certification

  @CTRL-04 @CTRL-08
  Scenario: An observed violation defeats a continuity claim
    Given a traversal required to preserve ownership by Alice
    And an applicable observation witness establishes ownership by Bob afterward
    When the candidate claims that required ownership continuity holds
    Then the ownership preservation requirement fails
    And the report retains the counterexample and both state references

  @CTRL-02 @CTRL-08 @CTRL-09
  Scenario: Context change exposes a previously dangling relationship
    Given a prior arrival-only closure with unresolved recipient alternatives
    And a new context requests delivery specifically to Alice
    When the validator evaluates the new request
    Then the prior arrival receipt retains its original scope
    And the recipient distinction enters the active resolution portion
    And unrelated witnessed arrival structure remains represented

  @CTRL-08
  Scenario: Out-of-scope evidence cannot certify a relationship
    Given a witness of ownership for package P in context morning
    And a candidate requiring ownership for package Q in context evening
    When the validator checks that witness against the candidate
    Then the witness does not discharge the candidate's ownership obligation
    And the report identifies the subject and context mismatch
