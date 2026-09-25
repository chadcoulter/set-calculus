#!/usr/bin/env python3
"""Validate Core 0.1 A5 Transform-semantics structure and integration."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SPEC = Path("docs/set-calculus-core/TRANSFORM_SEMANTICS.md")

REQUIRED_FILES = (
    SPEC,
    Path("docs/set-calculus-core/README.md"),
    Path("docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md"),
    Path("docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md"),
    Path("docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md"),
    Path("docs/set-calculus-core/CORE_0.1_PATH_INDEX.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.md"),
    Path("CORE_0.1_COMPLETENESS_CHECKLIST.yaml"),
    Path("scripts/audit_core_g2_path_index.py"),
)

REQUIRED_SPEC_TOKENS = (
    "D_T",
    "A_T",
    "τ_T",
    "G_T",
    "K_T",
    "Δ_T",
    "Π_T",
    "F_T",
    "R_T",
    "C_T",
    "Applicable(T,s | C,A)",
    "TransformResult",
    "APPLIED",
    "FAILURE",
    "AuthorizedChange",
    "P <=_P P'",
    "REVERSIBLE",
    "PARTIALLY_REVERSIBLE",
    "IRREVERSIBLE",
    "Id_Ω",
    "Composable(T2,T1 | C,A)",
    "IDENTITY",
    "STATE",
    "CONTEXT",
    "AUTHORITY",
    "INVARIANT",
    "PROVENANCE",
    "CLOSURE_PRODUCING",
    "Reopen",
    "property(T(s))",
    "protected residual",
)

CROSS_LINKS = {
    "docs/set-calculus-core/README.md": "TRANSFORM_SEMANTICS.md",
    "docs/set-calculus-core/TRAJECTORY_ADMISSIBILITY_AND_RESOLUTION_DEPTH.md": "TRANSFORM_SEMANTICS.md",
    "docs/set-calculus-core/RESOLUTION_CLOSURE_AND_REOPENING.md": "TRANSFORM_SEMANTICS.md",
    "docs/philosophy-of-set-calculus/CANONICAL_TERMINOLOGY_LEDGER.md": "TRANSFORM_SEMANTICS.md",
    "docs/set-calculus-core/CORE_0.1_PATH_INDEX.md": "TRANSFORM_SEMANTICS.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.md": "TRANSFORM_SEMANTICS.md",
    "CORE_0.1_COMPLETENESS_CHECKLIST.yaml": "TRANSFORM_SEMANTICS.md",
}


def validate(root: Path) -> dict[str, object]:
    errors: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel.as_posix()}")

    if errors:
        return {
            "errors": errors,
            "required_tokens": 0,
            "cross_links": 0,
            "cross_links_total": len(CROSS_LINKS),
        }

    spec = (root / SPEC).read_text(encoding="utf-8")

    for token in REQUIRED_SPEC_TOKENS:
        if token not in spec:
            errors.append(f"transform specification missing token: {token}")

    linked = 0
    for path, token in CROSS_LINKS.items():
        text = (root / path).read_text(encoding="utf-8")
        if token not in text:
            errors.append(f"missing A5 cross-link: {path} -> {token}")
        else:
            linked += 1

    if "C_T = CLOSURE_PRODUCING\n!-> closure" not in spec:
        errors.append(
            "closure-producing transforms must not imply closure by declaration"
        )

    if "declared change != authorized change" not in spec:
        errors.append("declared-change/authorized-change distinction missing")

    if "reversible != provenance-erasing" not in spec:
        errors.append("reversibility/provenance distinction missing")

    g2_audit = (root / "scripts/audit_core_g2_path_index.py").read_text(encoding="utf-8")
    if '"Transform semantics"' not in g2_audit:
        errors.append("G2 path audit does not require Transform semantics")

    return {
        "errors": errors,
        "required_tokens": len(REQUIRED_SPEC_TOKENS),
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
        print("Core 0.1 A5 Transform Semantics audit")
        print(f"a5_errors={len(result['errors'])}")
        print(f"required_tokens={result.get('required_tokens', 0)}")
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
