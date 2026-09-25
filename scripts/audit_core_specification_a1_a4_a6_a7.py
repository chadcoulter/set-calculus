#!/usr/bin/env python3
"""Validate Core 0.1 specification gates A1-A4, A6, and A7."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TRAJ = Path("docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md")
README = Path("docs/set-calculus-core/README.md")
LEDGER = Path("docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md")
CHECKLIST = Path("CORE_0.1_COMPLETENESS_CHECKLIST.md")
CHECKLIST_YAML = Path("CORE_0.1_COMPLETENESS_CHECKLIST.yaml")
REPORT = Path("docs/audits/CORE_0.1_SPECIFICATION_AUDIT_A1_A4_A6_A7.md")

PRIMITIVES = (
    "Set",
    "Member",
    "Relationship",
    "Identity",
    "State",
    "Transform",
    "Resolution",
    "Provenance",
)

REQUIRED_FILES = (
    TRAJ,
    README,
    LEDGER,
    CHECKLIST,
    CHECKLIST_YAML,
    REPORT,
)

GATE_TOKENS = {
    "A1": (
        "## Canonical primitives",
        "Identity != State",
    ),
    "A2": (
        "rho = <P,N,C>",
        "PARTIAL",
        "UNRESOLVED",
        "### 27.1.1 Deterministic coordinate construction",
        "P = (Σ_o Pos(o)) / m",
        "N = (Σ_o Neg(o)) / m",
        "C = (Σ_o Done(o)) / m",
        "ρ1 ⪯ ρ2",
        "ρ1 ∨ ρ2",
        "ρ1 ∧ ρ2",
        "ρ1 ∥ ρ2",
    ),
    "A3": (
        "DecisivePositive",
        "DecisiveNegative",
        "Constructive Positive Closure",
        "proof that D- is false",
        "Conflict(ρ,Q)",
    ),
    "A4": (
        "## 24.3 Canonical six-witness typed payloads",
        "IdentityWitnessPayload",
        "StateWitnessPayload",
        "ContextWitnessPayload",
        "AuthorityWitnessPayload",
        "InvariantWitnessPayload",
        "ProvenanceWitnessPayload",
        "## 24.5 Canonical four-state witness validation",
        "ValidateBoundary6(E_B6)",
    ),
    "A6": (
        "## 26.1 Canonical trajectory and concatenation semantics",
        "π = <s0,T1,s1,...,Tn,sn>",
        "Adm4(π | C,A)",
        "ValidateBoundary6(E_B6(π1,π2 | C,A))",
        "local admissibility",
        "PARTIAL trajectory",
    ),
    "A7": (
        "Γ ; Q ⊢Ω κ",
        "AdmissibleTieBreak",
        "r1 ≻t r2",
        "MaxΩ(R*)",
        "POSITIVE_RESOLVED",
        "NEGATIVE_RESOLVED",
        "PARTIALLY_RESOLVED",
        "UNRESOLVED_CONFLICT",
        "A losing witness remains preserved",
    ),
}


def canonical_rows(ledger: str, primitive: str) -> list[str]:
    prefix = f"| **{primitive}** |"
    return [line for line in ledger.splitlines() if line.startswith(prefix)]


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []
    gates: dict[str, str] = {}

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel.as_posix()}")

    if errors:
        return {"errors": errors, "gates": gates}

    traj = (root / TRAJ).read_text(encoding="utf-8")
    readme = (root / README).read_text(encoding="utf-8")
    ledger = (root / LEDGER).read_text(encoding="utf-8")
    checklist = (root / CHECKLIST).read_text(encoding="utf-8")
    checklist_yaml = (root / CHECKLIST_YAML).read_text(encoding="utf-8")
    report = (root / REPORT).read_text(encoding="utf-8")

    # A1
    a1_errors: list[str] = []
    for primitive in PRIMITIVES:
        rows = canonical_rows(ledger, primitive)
        if len(rows) != 1:
            a1_errors.append(
                f"{primitive} must have exactly one canonical ledger row; found {len(rows)}"
            )
        if primitive not in readme:
            a1_errors.append(f"README primitive list missing {primitive}")

    if "## Candidate primitives" in readme or "remain candidates until formally defined" in readme:
        a1_errors.append("README still describes Core primitives as undefined candidates")

    if "Identity != State" not in readme:
        a1_errors.append("README does not state Identity != State")

    # Other gates
    sources = {
        "A2": traj,
        "A3": traj,
        "A4": traj,
        "A6": traj,
        "A7": traj,
    }

    gate_errors: dict[str, list[str]] = {"A1": a1_errors}
    for gate, source in sources.items():
        missing = [token for token in GATE_TOKENS[gate] if token not in source]
        gate_errors[gate] = [f"missing required token: {token}" for token in missing]

    # Current-vs-historical guardrails.
    if "# 2. Trajectory Admissibility" in traj and "Historical status-vocabulary note" not in traj:
        gate_errors["A6"].append("historical three-state trajectory section is not marked historical")

    if "Historical Five-Component Baseline" not in traj:
        gate_errors["A4"].append("historical five-component boundary baseline is not marked")

    if "PARTIAL\n!=\nUNRESOLVED" not in traj:
        gate_errors["A2"].append("PARTIAL != UNRESOLVED is not explicit")

    for gate in ("A1", "A2", "A3", "A4", "A6", "A7"):
        if f"## {gate}." not in checklist:
            gate_errors[gate].append("human checklist gate missing")
        if f'id: "{gate}"' not in checklist_yaml:
            gate_errors[gate].append("machine-readable checklist gate missing")
        if gate not in report:
            gate_errors[gate].append("audit report section missing")

        if gate_errors[gate]:
            errors.extend(f"{gate}: {item}" for item in gate_errors[gate])
            gates[gate] = "FAIL"
        else:
            gates[gate] = "PASS"

    return {
        "errors": errors,
        "gates": gates,
        "primitive_count": len(PRIMITIVES),
        "validated_gate_count": len(gates),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(args.root.resolve())

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Core 0.1 specification audit: A1-A4, A6, A7")
        for gate, status in sorted(result.get("gates", {}).items()):
            print(f"{gate}={status}")
        print(f"errors={len(result['errors'])}")
        for error in result["errors"]:
            print(f"ERROR: {error}")

    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
