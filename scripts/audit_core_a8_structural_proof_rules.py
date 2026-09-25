#!/usr/bin/env python3
"""Validate Core 0.1 A8 structural proof-rule status and integration."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SPEC = Path("docs/set-calculus-core/STRUCTURAL_PROOF_RULES.md")

EXPECTED = {
    "WEAKENING": "RESTRICTED",
    "CONTRACTION": "RESTRICTED",
    "EXCHANGE": "RESTRICTED",
    "CUT": "RESTRICTED",
    "SUBSTITUTION": "RESTRICTED",
}

REQUIRED_FILES = (
    SPEC,
    Path("docs/set-calculus-core/README.md"),
    Path("docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md"),
    Path("docs/set-calculus-core/TRANSFORM_SEMANTICS.md"),
    Path("docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md"),
    Path("docs/set-calculus-core/CORE_0.1_PATH_INDEX.md"),
    Path("docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.yaml"),
    Path("scripts/audit_core_g2_path_index.py"),
)

CROSS_LINKS = {
    "docs/set-calculus-core/README.md": "STRUCTURAL_PROOF_RULES.md",
    "docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md": "STRUCTURAL_PROOF_RULES.md",
    "docs/set-calculus-core/TRANSFORM_SEMANTICS.md": "STRUCTURAL_PROOF_RULES.md",
    "docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md": "STRUCTURAL_PROOF_RULES.md",
    "docs/set-calculus-core/CORE_0.1_PATH_INDEX.md": "STRUCTURAL_PROOF_RULES.md",
    "docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md": "STRUCTURAL_PROOF_RULES.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.md": "STRUCTURAL_PROOF_RULES.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.yaml": "STRUCTURAL_PROOF_RULES.md",
}

REQUIRED_CONCEPTS = (
    "SameEvidenceIdentity",
    "NoReopenTrigger",
    "proof-context exchange",
    "proof compression",
    "ValidateSubstitution",
    "property(T(x))",
    "PARTIAL",
    "UNRESOLVED",
    "six-witness",
    "closure-epoch",
)


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel.as_posix()}")

    if errors:
        return {"errors": errors, "status_rules": 0, "cross_links": 0}

    spec = (root / SPEC).read_text(encoding="utf-8")

    for rule, expected in EXPECTED.items():
        matches = re.findall(
            rf"^{rule}\s*=\s*(ADMISSIBLE|RESTRICTED|NOT_ADMISSIBLE|UNRESOLVED)\s*$",
            spec,
            re.MULTILINE,
        )
        unique = sorted(set(matches))
        if unique != [expected]:
            errors.append(
                f"{rule} must have exactly one status {expected}; found {unique}"
            )

    for token in REQUIRED_CONCEPTS:
        if token not in spec:
            errors.append(f"structural proof specification missing token: {token}")

    linked = 0
    for path, token in CROSS_LINKS.items():
        text = (root / path).read_text(encoding="utf-8")
        if token not in text:
            errors.append(f"missing A8 cross-link: {path} -> {token}")
        else:
            linked += 1

    g2 = (root / "scripts/audit_core_g2_path_index.py").read_text(encoding="utf-8")
    if '"Structural proof rules"' not in g2:
        errors.append("G2 path audit does not require Structural proof rules")

    return {
        "errors": errors,
        "status_rules": len(EXPECTED),
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
        print("Core 0.1 A8 Structural Proof Rules audit")
        print(f"a8_errors={len(result['errors'])}")
        print(f"status_rules={result.get('status_rules', 0)}")
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
