# REDΣ Progressive Resolution Compute Interface

## 1. Purpose

This document defines the REDΣ standard compute interface for progressive relational resolution.

The standard is intentionally compute-substrate agnostic.

It does not prescribe:

- processor architecture,
- instruction set,
- memory model,
- execution engine,
- compiler,
- programming language,
- hardware topology,
- or implementation strategy.

It defines the external contract that a conforming compute system must satisfy.

The purpose is to make REDΣ resolution portable across implementations while preserving:

```text
state
goal
progress
ambiguity
conflict
dangling structure
admissibility
provenance
termination
feedback
```

---

# 2. Standard Name

Canonical name:

```text
REDΣ Progressive Resolution Compute Interface
```

Short form:

```text
REDΣ Compute Interface
```

The standard belongs to the REDΣ / REDSigma architecture.

---

# 3. Core Principle

The interface defines:

```text
WHAT a conforming resolver must expose
```

not:

```text
HOW the resolver must compute internally
```

A conforming implementation may use any compute substrate capable of satisfying the interface contract.

Examples may include:

```text
CPU
GPU
FPGA
ASIC
photonic logic
distributed systems
symbolic engines
graph engines
set-calculus engines
neural systems
quantum systems
hybrid systems
future compute substrates
```

---

# 4. Interface Layers

The REDΣ Compute Interface defines eight contract layers:

```text
1. Input Contract
2. Session Contract
3. Progressive Resolution Contract
4. Conflict / Dangling Contract
5. Admissibility Contract
6. Enough Boundary Contract
7. Output Contract
8. Feedback Contract
```

Supporting all layers:

```text
Provenance Contract
Diagnostics Contract
```

---

# 5. Canonical Invocation

```text
resolve(
    input_state,
    goal,
    context?
)
    -> ResolutionSession
```

The session emits zero or more progress states and eventually a terminal result:

```text
ResolutionSession
    -> ProgressEvent*
    -> ResolutionResult
```

This separation allows implementations to resolve progressively rather than pretending all computation is atomic.

---

# 6. Resolution Request

```text
ResolutionRequest {
    request_id
    input_state
    goal
    context?
    constraints?
    provenance?
    options?
}
```

Required:

```text
request_id
input_state
goal
```

Optional:

```text
context
constraints
provenance
options
```

---

# 7. Input State Contract

The interface does not prescribe the payload format of a state.

It requires only that the state be:

```text
identifiable
versioned
referenceable
provenance-capable
```

Abstract form:

```text
ComputeState {
    state_id
    version
    payload
    provenance
}
```

The payload is implementation-defined.

---

# 8. Goal Contract

Every resolution session operates relative to a goal.

```text
Goal {
    goal_id
    expression
    scope?
    termination_policy?
}
```

The goal defines relevance.

The interface does not require a particular goal language.

---

# 9. Resolution Session

```text
ResolutionSession {
    session_id
    request
    current_progress
    state_history
    provenance
    diagnostics
}
```

A session has stable identity from request through final result.

---

# 10. Progressive Resolution Contract

A conforming engine must expose intermediate resolution state.

```text
ResolutionProgress {
    session_id
    step
    status

    relevant
    resolved
    unresolved
    dangling
    conflicts

    admissibility
    enough_boundary

    state_ref
    provenance_delta
    diagnostics
}
```

---

# 11. Progress Status

```text
ProgressStatus :=
    INITIALIZED
  | RESOLVING
  | PARTIAL
  | DANGLING
  | CONFLICT
  | REOPENED
  | SUFFICIENT
  | COMPLETE
  | INVALID
```

These statuses describe resolution state rather than internal compute state.

---

# 12. Resolution Categories

A conforming implementation must distinguish:

```text
RESOLVED
UNRESOLVED
DANGLING
CONFLICT
```

Definitions:

```text
RESOLVED
    sufficiently determined for the active goal

UNRESOLVED
    still capable of changing the relevant continuation

DANGLING
    unresolved but not currently relevant to the continuation

CONFLICT
    incompatible relevant relations remain simultaneously active
```

Dangling and conflicting information must remain explicit.

---

# 13. Distinction Representation

A resolution engine may use any internal representation, but the interface must expose addressable distinction references.

```text
DistinctionRef {
    id
    class?
    state_ref
    provenance
}
```

This permits later reopening or inspection.

---

# 14. Reopen Contract

A previously dangling distinction must be reopenable.

```text
reopen(
    session_id,
    distinction_ref
)
    -> ResolutionProgress
```

A distinction may become relevant because of:

```text
goal change
context change
new evidence
new relation
dependency activation
boundary instability
```

Reopening must retain prior provenance.

---

# 15. Conflict Contract

```text
Conflict {
    conflict_id
    participants
    relation
    reason
    provenance
}
```

A conforming implementation may:

```text
resolve
defer
branch
mark dangling
invalidate
```

but may not silently erase the conflict.

---

# 16. Resolution Delta

Each progressive step may emit a delta.

```text
ResolutionDelta {
    newly_resolved
    newly_unresolved
    newly_dangling
    reopened
    conflicts_added
    conflicts_resolved
    provenance_added
}
```

This allows consumers to observe change without requiring full-state replacement.

---

# 17. Admissibility Contract

Every candidate continuation must expose an admissibility decision before commit.

```text
AdmissibilityResult {
    accepted
    subject
    relation
    viability
    provenance
    reasons
}
```

Canonical REDΣ condition:

```text
accepted :=
    subject
AND relation
AND viability
AND provenance
```

The method used to compute these terms is implementation-defined.

---

# 18. Inadmissible Result

If admissibility fails:

```text
candidate state MUST NOT commit
```

The engine must return one of:

```text
DANGLING
REOPENED
CONFLICT
INVALID
```

with reasons and provenance.

---

# 19. Enough Boundary Contract

The REDΣ interface uses progressive termination rather than requiring exhaustive resolution.

```text
EnoughBoundaryResult :=
    ENOUGH
  | NOT_ENOUGH
  | REOPEN
```

A result is ENOUGH when:

```text
no unresolved distinction capable of changing
the relevant continuation remains
```

The internal mechanism used to determine this is implementation-defined.

---

# 20. Sufficient vs Complete

The standard distinguishes:

```text
SUFFICIENT
```

from:

```text
COMPLETE
```

SUFFICIENT means:

```text
the Enough Boundary has been reached
for the active goal
```

COMPLETE means:

```text
the session has emitted and committed
its accepted continuation
```

A state may be sufficient without every possible distinction in the model being globally resolved.

---

# 21. Output Contract

```text
ResolutionResult {
    session_id
    status
    input_state
    output_state
    goal

    unresolved
    dangling
    conflicts

    admissibility
    enough_boundary

    trace
    provenance
    diagnostics
}
```

Terminal status:

```text
ResolutionStatus :=
    RESOLVED
  | UNRESOLVED
  | BLOCKED
  | INVALID
  | COMPLETE
```

---

# 22. State Transition Contract

Accepted resolution produces a new state:

```text
S_n -> S_n+1
```

Required properties:

```text
S_n remains addressable
S_n+1 has new identity or version
transition provenance is retained
resolution evidence is retained
```

A conforming implementation must not require destructive overwrite of the prior state.

---

# 23. Feedback Contract

The accepted result may become the next input state.

```text
feedback(
    ResolutionResult
)
    -> ResolutionRequest
```

Canonical loop:

```text
S_n
  -> resolve
  -> S_n+1
  -> feedback
  -> resolve
  -> S_n+2
```

This enables persistent progressive world/model resolution.

---

# 24. Provenance Contract

Provenance is mandatory.

A conforming implementation must retain enough information to answer:

```text
what state did this come from?
what changed?
why did it change?
what relation or rule produced the change?
what evidence contributed?
what was left unresolved?
what was discarded from active relevance but preserved as dangling?
```

Minimum:

```text
ProvenanceRecord {
    source_state
    resulting_state
    goal
    operation_or_resolution_ref
    evidence_refs
    prior_provenance
}
```

---

# 25. Trace Contract

```text
ResolutionTrace {
    session_id
    events[]
}
```

Minimum event families:

```text
SESSION_START
STATE_ACCEPTED
PROGRESS
RESOLVED
UNRESOLVED
DANGLING
REOPEN
CONFLICT
ADMISSIBILITY_CHECK
ENOUGH_CHECK
STATE_TRANSITION
SESSION_COMPLETE
SESSION_INVALID
```

Implementation-specific events may be added.

---

# 26. Diagnostic Contract

```text
Diagnostic {
    code
    severity
    message
    source_ref?
    related_refs?
    provenance?
}
```

A conforming implementation must expose structured diagnostics rather than only unstructured error strings.

---

# 27. Capability Discovery

A REDΣ compute implementation should expose its supported capabilities.

```text
ComputeCapabilities {
    progressive_resolution
    reopen
    branching
    streaming_progress
    provenance
    trace
    conflict_reporting
    dangling_state
    deterministic_mode?
    parallel_resolution?
    hardware_acceleration?
}
```

Capabilities describe implementation features without redefining the standard.

---

# 28. Standard Interface Surface

Minimum required operations:

```text
create_session(request)
get_progress(session_id)
continue_resolution(session_id)
reopen(session_id, distinction_ref)
get_result(session_id)
get_trace(session_id)
get_provenance(ref)
get_capabilities()
```

An implementation may expose these as:

```text
library calls
object methods
IPC
RPC
REST
message bus
hardware interface
instruction protocol
```

The transport is not part of the semantic standard.

---

# 29. Conformance Levels

## REDΣ Core Conformance

Requires:

```text
input state
goal
progress
resolved/unresolved distinction
admissibility
Enough Boundary
output state
provenance
```

## REDΣ Progressive Conformance

Adds:

```text
dangling state
reopen
conflict reporting
progress deltas
trace
```

## REDΣ Complete Interface Conformance

Adds:

```text
feedback
capability discovery
cross-session provenance
structured diagnostics
full state lineage
```

These levels classify interface capability only.

They do not define processor architecture.

---

# 30. Relationship to the Triadic Compute Model

The Triadic Compute Model can implement this interface.

For that implementation:

```text
29-coordinate resolution
triadic projection
Prime Resolver
partition lattice
Enough Boundary
```

are internal compute mechanisms behind the REDΣ interface.

The REDΣ Compute Interface itself does not require a consumer to know those internal details.

This allows:

```text
Triadic Compute Engine
Set Calculus Engine
Distributed Resolver
Future Resolver
```

to present the same external compute contract.

---

# 31. Architectural Separation

```text
REDΣ Compute Interface
        |
        +-- semantic contract
        +-- progress contract
        +-- provenance contract
        +-- termination contract
        +-- feedback contract

Implementation
        |
        +-- Triadic Compute
        +-- other conforming resolver
```

This separation is intentional.

The standard interface should remain stable even if internal compute architectures evolve.

---

# 32. Core Standard Principle

A REDΣ-compatible compute system does not need to expose how it thinks.

It must expose enough information to establish:

```text
what went in
what remains unresolved
what was resolved
what became dangling
what conflicted
why the continuation is admissible
why resolution is sufficient
what state came out
where that state came from
```

That is the REDΣ progressive-resolution compute boundary.

This defines the REDΣ Progressive Resolution Compute Interface Core 0.1.
