@planned @ctrl @co_transformation
Feature: Partial closure retains both transformed products and their continuity
  These scenarios specify planned behavior and are not in the executable suite.

  @CTRL-05
  Scenario: A point expands into a set without losing viability
    Given point actor a with retained history h
    And a typed transform whose declared output is the set containing b and c
    And a witnessed transition from a to both products
    And b and c both satisfy the requested result
    When the validator evaluates the candidate transform
    Then the different input and output counts do not imply viability loss
    And both products retain lineage to a and the execution
    And requested multiplicity is one

  @CTRL-05
  Scenario: Convergence retains every source history
    Given actors a and b with distinct histories
    And a typed transform that maps both actors to visible configuration y
    When the validator checks the convergence
    Then both source traversals remain reconstructible
    And equal visible outputs do not erase the historical distinction

  @CTRL-05
  Scenario: A missing source transition is not convergence
    Given viable admitted actors a and b
    And a candidate result with a transition from a but none representing b
    When the validator checks source lineage
    Then the viability representation requirement fails
    And the missing source b is named in the report

  @CTRL-06 @CTRL-07
  Scenario: Partial closure co-transforms the remainder
    Given state S with required portion S_R and remaining portion S_K
    And an applicable witness that S_R is sufficient for the request
    And a boundary projection that invokes partial closure on S_R before traversal
    And the projection changes S_K into remainder K_prime
    When the validator evaluates the paired products
    Then the result retains resolved portion S_R_prime and remainder K_prime
    And both products reference the same transform execution
    And their required cross-portion relationships remain witnessed
    And closure is partial with the directed arrow
    And full-state closure is not inferred

  @CTRL-06
  Scenario: Open arrow does not assert invertibility
    Given an open transform with a many-to-one operation
    When its notation is rendered before closure invocation
    Then the open arrow is displayed
    And no inverse function is asserted by that notation

  @CTRL-06
  Scenario: Reflection requires invocation of its partial boundary
    Given a candidate reflection across a boundary
    And no record invokes partial closure of the required portion before traversal
    When the validator evaluates the reflection requirements
    Then the required boundary invocation fails
    And a singular visible output alone cannot certify the traversal

  @CTRL-07 @CTRL-08
  Scenario: A witness cannot replace a remainder
    Given a transform that produces persistent consequence damage
    And a result containing only a witness that damage occurred
    And no retained state represents the damage consequence
    When the validator evaluates residual persistence
    Then the required remainder representation fails
    And the witness remains classified as evidence

  @CTRL-07 @CTRL-08
  Scenario: Cause removal cannot silently erase its co-transformed consequence
    Given a retained damage consequence from an earlier transform
    And a later transform ends the initiating cause
    And no applicable restoring transition is witnessed
    When the candidate omits the damage consequence
    Then consequence preservation fails
    And cause termination does not serve as restoration evidence

  @CTRL-08
  Scenario: A nonempty restoration reference is insufficient evidence
    Given a retained damage consequence
    And a candidate removes damage using only the string repaired as evidence
    When the validator checks the restoration claim
    Then restoration is not certified
    And the report requests the applicable restoring transition witness

  @CTRL-09
  Scenario: Composition carries the changed remainder to the next function
    Given a first transform producing resolved portion R1 and changed remainder K1
    And a compatible second transform whose input includes R1 and K1
    When the validator evaluates the composite traversal
    Then the second execution records both input products
    And the composite retains both execution witnesses and source histories
    And the second remainder is related to K1 by its declared carry rule

  @CTRL-09
  Scenario: Type-incompatible composition cannot become valid by dropping a product
    Given a first transform producing a point and a set-valued remainder
    And a second transform whose domain admits only the point
    And the candidate silently discards the remainder to invoke the second transform
    When the validator checks composition
    Then the candidate fails the typed effective-state and residual requirements
    And the discarded remainder remains identified in the failed receipt

  @CTRL-09
  Scenario: A later continuation splits an apparently sufficient local result
    Given a locally resolved portion with two retained hidden routes
    And the declared continuation produces arrival before noon for one route and after noon for the other
    And the request requires arrival before noon
    When the validator evaluates the continuation
    Then local closure does not certify the final request
    And the responsible route or joint relation reopens
    And unrelated certified relationships are retained

  @CTRL-10
  Scenario: A quickly discovered candidate is stored before certification
    Given a candidate found by the quick discovery route
    And its boundary invocation, products and witnesses are recorded
    When the validator evaluates the candidate after discovery
    Then the candidate's initial existence is not treated as a validity certificate
    And admissibility and requested sufficiency are evaluated from its evidence

  @CTRL-01 @CTRL-10
  Scenario: Partial closure and logical partial progress are separate statuses
    Given a sufficient requested portion with a retained open remainder
    And applicable evidence establishes all requirements for that scoped request
    When the validator reports the result
    Then scoped request validity may be valid
    And whole-state closure remains partial
    And no logical partial status is assigned solely from the closure label

  @CTRL-11
  Scenario: An applicable unimplemented law prevents unsupported certification
    Given a candidate requiring the Law 28 co-transformation check
    And that evaluator is registered as unimplemented
    When the validator evaluates the required laws
    Then the Law 28 obligation is reported as unsupported
    And it is not reported as not applicable
    And closure is not certified
