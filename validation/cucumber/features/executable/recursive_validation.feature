Feature: Validate candidates after discovery with preserved recursive evidence
  Scenario Outline: A quickly found candidate receives an evidence-based result
    Given the finite candidate "<candidate>"
    When the recursive validator evaluates the candidate
    Then the validation result is "<status>"
    And every pass retains its input, evidence and consequences

    Examples:
      | candidate           | status     |
      | convergence         | CLOSED     |
      | subject-loss        | INVALID    |
      | relation-loss       | INVALID    |
      | branch-loss         | INVALID    |
      | history-loss        | INVALID    |
      | multiple-results    | UNRESOLVED |
      | missing-path        | UNRESOLVED |
      | path-split          | UNRESOLVED |
      | certificate         | CLOSED     |
      | false-certificate   | INVALID    |
      | safe-compression    | CLOSED     |
      | unsafe-compression  | INVALID    |
      | cause-removal       | CLOSED     |
      | false-reset         | INVALID    |
      | reopen              | UNRESOLVED |
      | boundary-refinement | CLOSED     |

  Scenario Outline: The finite law registry returns explicit conformance evidence
    Given the finite candidate "<candidate>"
    When law <law> evaluates the candidate
    Then its conformance status is "<status>"

    Examples:
      | law | candidate          | status     |
      | 1   | convergence        | PASS       |
      | 2   | convergence        | PASS       |
      | 2   | relation-loss      | FAIL       |
      | 3   | convergence        | PASS       |
      | 3   | branch-loss        | FAIL       |
      | 4   | convergence        | PASS       |
      | 4   | history-loss       | FAIL       |
      | 5   | convergence        | PASS       |
      | 5   | multiple-results   | UNRESOLVED |
      | 6   | convergence        | PASS       |
      | 6   | multiple-results   | UNRESOLVED |
      | 7   | convergence        | PASS       |
      | 7   | multiple-results   | UNRESOLVED |
      | 8   | convergence        | PASS       |
      | 9   | convergence        | PASS       |
      | 10  | convergence        | PASS       |
      | 11  | certificate        | PASS       |
      | 11  | false-certificate  | FAIL       |
      | 12  | reopen             | PASS       |
      | 13  | reopen             | PASS       |
      | 14  | convergence        | PASS       |
      | 14  | path-split         | UNRESOLVED |
      | 14  | missing-path       | UNKNOWN    |
      | 15  | convergence        | PASS       |
      | 15  | branch-loss        | FAIL       |
      | 16  | safe-compression   | PASS       |
      | 16  | unsafe-compression | FAIL       |
      | 17  | cause-removal      | PASS       |
      | 17  | false-reset        | FAIL       |
      | 18  | convergence        | PASS       |
      | 18  | subject-loss       | FAIL       |
