# Scripture as Compute — Computer Science

## Status

Core 0.1 conceptual stack is now defined through the interpreter and execution engine.

See:

- [Core 0.1 Anchor](./ANCHOR_CORE_0.1.md)
- [Core Types and Transforms](./CORE_TYPES_AND_TRANSFORMS.md)
- [Typed Grammar](./TYPED_GRAMMAR.md)
- [AST and Parser](./AST_AND_PARSER.md)
- [Type Checker](./TYPE_CHECKER.md)
- [Interpreter and Execution Engine](./INTERPRETER_AND_EXECUTION_ENGINE.md)

The original white-paper framing is preserved separately under:

```text
docs/scripture-as-compute/scripture-as-software-whitepaper.txt
```

## Core Model

A scriptural unit is modeled as an operation over contextual state:

```text
ScriptureUnit(Context, Actor, State) -> State'
```

Canonical typed form:

```text
(C:Context, A:Actor, S0:State)
    --[K:Constraint]
    O:Operation<State,State>
-->
S1:State
```

with optional post-transform checks:

```text
I:Integrity<State>(S1)
Q:Completion<State>(S1)
```

## Core Types

```text
State
Context
Actor
Constraint
Operation
Handler
Mediator
Scope
Migration
Integrity
Variant
Completion
```

## Execution Outcomes

```text
RESOLVED
UNRESOLVED
BLOCKED
INVALID
COMPLETE
```

## Current Architecture

```text
source
  -> lexer
  -> parser
  -> AST
  -> binder
  -> generic type resolution
  -> type checker
  -> typed AST
  -> interpreter
  -> execution trace
```

The runtime enforces scope, applies mediators, evaluates constraints, executes operations, dispatches handlers, applies migrations and variants, validates integrity, evaluates completion, and preserves provenance across immutable state transitions.

## Source Extraction

The model began by extracting computational structure from the Scripture as Software white paper. That source introduced the initial firmware/runtime, migration, language-build-target, textual-variant, integrity, mediation, event-handler, and completion concepts that were then formalized here.

## Core 0.1 Boundary

The current baseline is recorded in [ANCHOR_CORE_0.1.md](./ANCHOR_CORE_0.1.md).

The anchor records what has been defined so far. Additional work may extend this area later, but no next-step stack or priority is implied.
