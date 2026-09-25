#!/usr/bin/env python3
"""Validate Core 0.1 A9 resolution-transition semantics and integration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SPEC = Path("docs/set-calculus-core/RESOLUTION_TRANSITION_SEMANTICS.md")

REQUIRED_FILES = (
    SPEC,
    Path("docs/set-calculus-core/README.md"),
    Path("docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md"),
    Path("docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md"),
    Path("docs/set-calculus-core/TRANSFORM_SEMANTICS.md"),
    Path("docs/set-calculus-core/STRUCTURAL_PROOF_RULES.md"),
    Path("docs/set-calculus-core/CORE_0.1_PATH_INDEX.md"),
    Path("docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.yaml"),
    Path("scripts/audit_core_g2_path_index.py"),
)

STATES = ("UNRESOLVED", "PARTIAL", "VALID", "INVALID")

REQUIRED_TRANSITIONS = tuple(
    f"{src} -> {dst}"
    for src in STATES
    for dst in STATES
    if src != dst
)

REQUIRED_CAUSES = (
    "NEW_MATERIAL_EVIDENCE",
    "EVIDENCE_CORRECTION",
    "VALID_SUPERSESSION",
    "TRANSFORM_RESULT",
    "CONTEXT_CHANGE",
    "AUTHORITY_CHANGE",
    "RULE_PROFILE_CHANGE",
)

REQUIRED_CONCEPTS = (
    "ρ = <P,N,C>",
    "Project_Q(ρ)",
    "Material(m,q)",
    "Reclassify(q_n,m,q_(n+1))",
    "W_transition",
    "Reopen(C_k,m)",
    "correction",
    "supersession",
    "P_n <=_P P_(n+1)",
    "same material basis",
    "manual relabeling",
    "destination state must equal Project_Q(ρ_after)",
)

CROSS_LINKS = {
    "docs/set-calculus-core/README.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "docs/set-calculus-core/TRANSFORM_SEMANTICS.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "docs/set-calculus-core/STRUCTURAL_PROOF_RULES.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "docs/set-calculus-core/CORE_0.1_PATH_INDEX.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.md": "RESOLUTION_TRANSITION_SEMANTICS.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.yaml": "RESOLUTION_TRANSITION_SEMANTICS.md",
}


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel.as_posix()}")

    if errors:
        return {
            "errors": errors,
            "off_diagonal_transitions": 0,
            "material_causes": 0,
            "cross_links": 0,
        }

    spec = (root / SPEC).read_text(encoding="utf-8")

    missing_transitions = [
        transition
        for transition in REQUIRED_TRANSITIONS
        if transition not in spec
    ]
    for transition in missing_transitions:
        errors.append(f"missing public-state transition: {transition}")

    missing_causes = [
        cause
        for cause in REQUIRED_CAUSES
        if cause not in spec
    ]
    for cause in missing_causes:
        errors.append(f"missing material-cause kind: {cause}")

    for concept in REQUIRED_CONCEPTS:
        if concept not in spec:
            errors.append(f"resolution-transition specification missing: {concept}")

    linked = 0
    for path, token in CROSS_LINKS.items():
        text = (root / path).read_text(encoding="utf-8")
        if token not in text:
            errors.append(f"missing A9 cross-link: {path} -> {token}")
        else:
            linked += 1

    g2 = (root / "scripts/audit_core_g2_path_index.py").read_text(encoding="utf-8")
    if '"Resolution transition semantics"' not in g2:
        errors.append("G2 path audit does not require Resolution transition semantics")

    if "state change\nrequires\nmaterial cause" not in spec:
        errors.append("material-cause transition invariant missing")

    if "conclusion change\nnever deletes\nproof history" not in spec:
        errors.append("proof-history preservation invariant missing")

    return {
        "errors": errors,
        "off_diagonal_transitions": len(REQUIRED_TRANSITIONS),
        "material_causes": len(REQUIRED_CAUSES),
        "cross_links": linked,
        "cross_links_total": len(CROSS_LINKS),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured validation output.",
    )
    args = parser.parse_args()

    result = validate(args.root.resolve())

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("Core 0.1 A9 Resolution Transition Semantics audit")
        print(f"a9_errors={len(result['errors'])}")
        print(
            "off_diagonal_transitions="
            f"{result.get('off_diagonal_transitions', 0)}"
        )
        print(f"material_causes={result.get('material_causes', 0)}")
        print(
            "cross_links="
            f"{result.get('cross_links', 0)}/"
            f"{result.get('cross_links_total', len(CROSS_LINKS))}"
        )
        for error in result["errors"]:
            print(f"ERROR: {error}")

    return 1 if result["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
