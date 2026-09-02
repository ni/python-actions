#!/usr/bin/env python3

import argparse
import ipaddress
import os
import sys
from urllib.parse import urlsplit

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    raise Exception('tomllib is not available. Please use Python 3.11 or later.')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Collect trusted project URLs from pyproject.toml files.')
    parser.add_argument('project_directory', help='Directory containing project pyproject.toml files.')
    parser.add_argument('allowed_domains', help='Comma-separated list of allowed domains.')
    parser.add_argument('output_path', help='Path to write discovered URLs.')
    return parser.parse_args()


def is_allowed(hostname: str, allowed: set[str]) -> bool:
    """
    Check if the given hostname is allowed based on the provided set of allowed domains.

    >>> is_allowed('example.com', {'example.com'})
    True

    >>> is_allowed('sub.example.com', {'example.com'})
    False

    >>> is_allowed('sub.example.com', {'*.example.com'})
    True
    """
    if not hostname:
        return False

    host = hostname.lower().rstrip('.')
    if host == 'localhost' or host.endswith('.localhost'):
        return False

    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None

    if ip is not None:
        return False

    if host in allowed:
        return True

    if any(host.endswith(f'.{domain.lstrip(".*")}') for domain in allowed if domain.startswith('*.')):
        return True

    return False


def safe_under(base_dir: str, candidate_path: str) -> str:
    """Return a canonical path that stays under base_dir, or raise ValueError."""
    safe_base = os.path.realpath(base_dir)
    safe_candidate = os.path.realpath(candidate_path)

    try:
        if os.path.commonpath([safe_base, safe_candidate]) != safe_base:
            raise ValueError(f"Path escapes base directory: {candidate_path!r}")
    except ValueError as exc:
        raise ValueError(f"Path escapes base directory: {candidate_path!r}") from exc

    return safe_candidate


def walk_metadata(value, results: set[str], allowed: set[str]) -> None:
    if isinstance(value, dict):
        for item in value.values():
            walk_metadata(item, results, allowed)
    elif isinstance(value, list):
        for item in value:
            walk_metadata(item, results, allowed)
    elif isinstance(value, str):
        if not value.startswith('https://'):
            return
        host = urlsplit(value).hostname
        if host and is_allowed(host, allowed):
            results.add(value)


def main() -> int:
    args = parse_args()
    project_directory = args.project_directory
    safe_project_directory = os.path.realpath(project_directory, strict=True)
    safe_project_directory = safe_under(os.getcwd(), safe_project_directory)
    allowed_domains = args.allowed_domains
    safe_output_path = safe_under("/tmp", os.path.realpath(args.output_path, strict=True))

    allowed: set[str] = set()
    for raw_domain in allowed_domains.split(','):
        domain = raw_domain.strip().lower().rstrip('.')
        if domain:
            allowed.add(domain)

    results: set[str] = set()

    for root, _, files in os.walk(safe_project_directory):
        for file_name in files:
            if file_name != 'pyproject.toml':
                continue

            manifest_path = safe_under(safe_project_directory, os.path.join(root, file_name))
            try:
                with open(manifest_path, 'rb') as manifest_file:
                    metadata = tomllib.load(manifest_file)
            except (OSError, tomllib.TOMLDecodeError):
                print(f"Warning: Failed to read or parse pyproject.toml at {manifest_path}", file=sys.stderr)
                continue

            walk_metadata(metadata, results, allowed)
            # Also find any commented URLs in the pyproject.toml file
            try:
                with open(manifest_path, 'r', encoding='utf-8') as manifest_file:
                    for line in manifest_file:
                        line = line.strip()
                        prefix, comment = line.split('#', maxsplit=1) if '#' in line else (line, '')
                        if comment.strip():
                            comment = comment.strip()
                            if comment.startswith('https://'):
                                host = urlsplit(comment).hostname  # handles extra at the end just fine
                                if host and is_allowed(host, allowed):
                                    results.add(comment)
            except OSError:
                print(f"Warning: Failed to read pyproject.toml at {manifest_path}", file=sys.stderr)
                continue

    output_directory = os.path.dirname(safe_output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    with open(safe_output_path, 'w', encoding='utf-8') as output_file:
        for url in sorted(results):
            output_file.write(f'{url}\n')

    return 0


if __name__ == '__main__':
    sys.exit(main())
