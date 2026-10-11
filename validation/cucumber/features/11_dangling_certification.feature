Feature: Law XI - Dangling Certification
  A singular unresolved domain may carry a closure certificate without internal collapse.

  Scenario: A singular unresolved domain receives a closure certificate
    Given a domain whose requested image is singular
    And unresolved internal distinctions with retained provenance
    When the collative evaluator evaluates Dangling Certification
    Then Law XI holds
    And a closure certificate records the domain and requested relation

  Scenario: Certification erases internal distinctions or provenance
    Given a proposed closure certificate that removes underlying distinction evidence
    When the collative evaluator evaluates Dangling Certification
    Then Law XI is violated
    And the certificate is rejected
