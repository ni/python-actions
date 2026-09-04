#!/usr/bin/env python3

import argparse
import ipaddress
import os
import re
import sys
from urllib.parse import urlsplit


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect trusted project URLs from pyproject.toml files."
    )
    parser.add_argument(
        "project_directory", help="Directory containing project pyproject.toml files."
    )
    parser.add_argument("allowed_domains", help="Comma-separated list of allowed domains.")
    parser.add_argument("output_path", help="Path to write discovered URLs.")
    return parser.parse_args()


def _is_allowed(hostname: str, allowed: set[str]) -> bool:
    """Check if the given hostname is allowed based on the provided set of allowed domains.

    >>> _is_allowed('example.com', {'example.com'})
    True

    >>> _is_allowed('sub.example.com', {'example.com'})
    False

    >>> _is_allowed('sub.example.com', {'*.example.com'})
    True
    """
    if not hostname:
        return False

    host = hostname.lower().rstrip(".")
    if host == "localhost" or host.endswith(".localhost"):
        return False

    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None

    if ip is not None:
        return False

    if host in allowed:
        return True

    if any(
        host.endswith(f'.{domain.lstrip(".*")}') for domain in allowed if domain.startswith("*.")
    ):
        return True

    return False


def _safe_under(base_dir: str, candidate_path: str) -> str:
    """Return a canonical path that stays under base_dir, or raise ValueError."""
    safe_base = os.path.realpath(base_dir)
    safe_candidate = os.path.realpath(candidate_path)

    try:
        if os.path.commonpath([safe_base, safe_candidate]) != safe_base:
            raise ValueError(f"Path escapes base directory: {candidate_path!r}")
    except ValueError as exc:
        raise ValueError(f"Path escapes base directory: {candidate_path!r}") from exc

    return safe_candidate


_URL_RE = re.compile(r'(https://.+?)(?:"|\s)')


def _extract_links_from_line(line: str) -> list[str]:
    """Extract URLs from a single line, stopping before a quote or whitespace."""
    matches: list[str] = []
    for match in re.finditer(_URL_RE, line):
        url = match.group(1)
        if url:
            matches.append(url)
    return matches


def _find_project_links(manifest_path: str, results: set[str], allowed: set[str]) -> None:
    """Find URLs within a pyproject.toml file without parsing TOML."""
    try:
        with open(manifest_path, "r", encoding="utf-8") as manifest_file:
            for line in manifest_file:
                for url in _extract_links_from_line(line):
                    host = urlsplit(url).hostname
                    if host and _is_allowed(host, allowed):
                        results.add(url)
    except OSError:
        print(f"Warning: Failed to read pyproject.toml at {manifest_path}", file=sys.stderr)


def _main() -> int:
    args = _parse_args()
    safe_project_directory = _safe_under(os.getcwd(), args.project_directory)
    allowed_domains = args.allowed_domains
    output_path = args.output_path

    allowed: set[str] = set()
    for raw_domain in allowed_domains.split(","):
        domain = raw_domain.strip().lower().rstrip(".")
        if domain:
            allowed.add(domain)

    results: set[str] = set()

    for root, _, files in os.walk(safe_project_directory):
        for file_name in files:
            if file_name != "pyproject.toml":
                continue

            manifest_path = _safe_under(safe_project_directory, os.path.join(root, file_name))
            _find_project_links(manifest_path, results, allowed)

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as output_file:
        for url in sorted(results):
            output_file.write(f"{url}\n")

    return 0


if __name__ == "__main__":
    sys.exit(_main())
