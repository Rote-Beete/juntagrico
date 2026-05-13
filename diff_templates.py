#!/usr/bin/env python3
"""
diff_templates.py — Compare juntagrico and rotebeete template files.

Usage (template path only):
    python diff_templates.py juntagrico/menu/admin/lists.html
    python diff_templates.py juntagrico/menu/admin/lists.html --output diff.patch

Usage (explicit paths):
    python diff_templates.py <original> <override>
"""

import argparse
import difflib
import sys
from pathlib import Path


def diff_files(original: Path, override: Path) -> list[str]:
    original_lines = original.read_text(encoding="utf-8").splitlines(keepends=True)
    override_lines = override.read_text(encoding="utf-8").splitlines(keepends=True)

    return list(
        difflib.unified_diff(
            original_lines,
            override_lines,
            fromfile=str(original),
            tofile=str(override),
        )
    )


def resolve_paths(template_path: str, override_path: str | None) -> tuple[Path, Path]:
    """
    Resolve template paths. If override_path is None, construct both paths automatically.
    Assumes juntagrico and rotebeete are sibling directories.
    """
    if override_path is None:
        # Single path mode: construct both from template_path
        cwd = Path.cwd()
        original = (
            cwd.parent / "juntagrico" / "juntagrico" / "templates" / template_path
        )
        override = cwd / "rotebeete" / "templates" / template_path
    else:
        # Explicit paths mode
        original = Path(template_path)
        override = Path(override_path)

    return original, override


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Unified diff between juntagrico and rotebeete templates.",
    )
    parser.add_argument(
        "template",
        type=str,
        help="Template path (e.g. juntagrico/menu/admin/lists.html); or original file path",
    )
    parser.add_argument(
        "override",
        nargs="?",
        default=None,
        type=str,
        help="Override file path (if omitted, auto-constructs both paths)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Write diff to this file instead of stdout (e.g. diff.patch)",
    )

    args = parser.parse_args()

    original, override = resolve_paths(args.template, args.override)

    for path in (original, override):
        if not path.exists():
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)

    diff = diff_files(original, override)

    if not diff:
        print("Files are identical.")
        sys.exit(0)

    output = "".join(diff)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Diff written to {args.output}")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
