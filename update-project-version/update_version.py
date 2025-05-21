"""Wrapper for ``poetry version`` that implements the "dev" bump rule.

This script is a workaround for https://github.com/python-poetry/poetry/issues/8718 - "Add 'dev' as
version bump rule for developmental releases."
"""

import argparse
import re
import subprocess
import sys


def _bump_dev_version(version: str) -> str:
    """Bump the "dev" version number, if present.

    >>> _bump_dev_version("1.0.0")
    '1.0.0'
    >>> _bump_dev_version("1.0.0.dev0")
    '1.0.0.dev1'
    >>> _bump_dev_version("1.0.0-dev0")
    '1.0.0-dev1'
    >>> _bump_dev_version("1.0.0_dev0")
    '1.0.0_dev1'
    >>> _bump_dev_version("1.0.0dev0")
    '1.0.0dev1'
    >>> _bump_dev_version("1.0.0.dev99")
    '1.0.0.dev100'
    """
    # Dot, dash, and underscore are all valid. Do not bother normalizing to dot.
    match = re.match(r"^(.*[\.-_]?dev)(\d+)$", version)
    if match:
        version = f"{match.group(1)}{int(match.group(2))+1}"
    return version


def main(args: list[str]) -> None:
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("rule")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()

    version = subprocess.check_output(["poetry", "version", "--short"], text=True).strip()

    if args.dev:
        if "dev" in version:
            new_version = _bump_dev_version(version)
            subprocess.run(["poetry", "version", new_version])
        else:
            # Run `poetry version` to update the version using the specified bump rule (e.g. "1.0.0"
            # -> "2.0.0", "1.1.0", or "1.0.1"), then add ".dev0" to the end.
            subprocess.run(["poetry", "version", args.rule])
            new_version = subprocess.check_output(
                ["poetry", "version", "--short"], text=True
            ).strip()
            new_version += ".dev0"
            subprocess.run(["poetry", "version", new_version])
    else:
        subprocess.run(["poetry", "version", args.rule])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
