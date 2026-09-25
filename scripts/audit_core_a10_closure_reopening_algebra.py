#!/usr/bin/env python3
"""Validate Core 0.1 A10 closure/reopening algebra and integration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SPEC = Path("docs/set-calculus-core/CLOSURE_REOPENING_ALGEBRA.md")

REQUIRED_FILES = (
    SPEC,
    Path("docs/set-calculus-core/README.md"),
    Path("docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md"),
    Path("docs/set-calculus-core/RESOLUTION_TRANSITION_SEMANTICS.md"),
    Path("docs/set-calculus-core/TRANSFORM_SEMANTICS.md"),
    Path("docs/set-calculus-core/STRUCTURAL_PROOF_RULES.md"),
    Path("docs/set-calculus-core/CORE_0.1_PATH_INDEX.md"),
    Path("docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.yaml"),
    Path("scripts/audit_core_g2_path_index.py"),
)

REQUIRED_OPERATIONS = (
    "CLOSE",
    "EXTEND",
    "REOPEN",
    "RECLOSE",
    "ID_Λ",
    "∘_Λ",
)

REQUIRED_LAWS = (
    "Close ∘ Close",
    "Reopen(OPEN, m)",
    "Reopen(C_superseded, m)",
    "epoch_(n+1) >= epoch_n",
    "Active(C)",
    "associativity where defined",
    "noncommutativity",
    "REOPEN ∘_Λ CLOSE",
    "CLOSE ∘_Λ REOPEN",
    "CLOSED = VALID",
    "local closures",
    "C_T = CLOSURE_PRODUCING",
)

CROSS_LINKS = {
    "docs/set-calculus-core/README.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "docs/set-calculus-core/RESOLUTION_TRANSITION_SEMANTICS.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "docs/set-calculus-core/TRANSFORM_SEMANTICS.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "docs/set-calculus-core/STRUCTURAL_PROOF_RULES.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "docs/set-calculus-core/CORE_0.1_PATH_INDEX.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.md": "CLOSURE_REOPENING_ALGEBRA.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.yaml": "CLOSURE_REOPENING_ALGEBRA.md",
}


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel.as_posix()}")

    if errors:
        return {
            "errors": errors,
            "operations": 0,
            "laws": 0,
            "cross_links": 0,
        }

    spec = (root / SPEC).read_text(encoding="utf-8")

    for token in REQUIRED_OPERATIONS:
        if token not in spec:
            errors.append(f"closure algebra missing operation: {token}")

    for token in REQUIRED_LAWS:
        if token not in spec:
            errors.append(f"closure algebra missing law token: {token}")

    linked = 0
    for path, token in CROSS_LINKS.items():
        content = (root / path).read_text(encoding="utf-8")
        if token not in content:
            errors.append(f"missing A10 cross-link: {path} -> {token}")
        else:
            linked += 1

    g2 = (root / "scripts/audit_core_g2_path_index.py").read_text(encoding="utf-8")
    if '"Closure and reopening algebra"' not in g2:
        errors.append("G2 path audit does not require Closure and reopening algebra")

    if "A10-18" not in spec:
        errors.append("A10 invariant set is incomplete")

    if "RECLOSE\n!=\nreactivate C_k" not in spec:
        errors.append("reclosure freshness law missing")

    if "REOPEN ∘_Λ CLOSE\n!=\nID_OPEN" not in spec:
        errors.append("non-inverse reopen/close law missing")

    return {
        "errors": errors,
        "operations": len(REQUIRED_OPERATIONS),
        "laws": len(REQUIRED_LAWS),
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
        print("Core 0.1 A10 Closure and Reopening Algebra audit")
        print(f"a10_errors={len(result['errors'])}")
        print(f"operations={result.get('operations', 0)}")
        print(f"laws={result.get('laws', 0)}")
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
