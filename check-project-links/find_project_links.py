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


def is_allowed(hostname: str, allowed: list[str]) -> bool:
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

    for domain in allowed:
        if domain.startswith('*.'):
            suffix = domain[2:]
            if host == suffix or host.endswith(f'.{suffix}'):
                return True
        else:
            if host == domain:
                return True
    return False


def walk_metadata(value, results, allowed):
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
    allowed_domains = args.allowed_domains
    output_path = args.output_path

    allowed = {}
    for raw_domain in allowed_domains.split(','):
        domain = raw_domain.strip().lower().rstrip('.')
        if domain:
            allowed.add(domain)

    results: set[str] = set()

    for root, _, files in os.walk(project_directory):
        for file_name in files:
            if file_name != 'pyproject.toml':
                continue

            manifest_path = os.path.join(root, file_name)
            try:
                with open(manifest_path, 'rb') as manifest_file:
                    metadata = tomllib.load(manifest_file)
            except (OSError, tomllib.TOMLDecodeError):
                print(f"Warning: Failed to read or parse pyproject.toml at {manifest_path}", file=sys.stderr)
                continue

            walk_metadata(metadata, results, allowed)

    with open(output_path, 'w', encoding='utf-8') as output_file:
        for url in sorted(results):
            output_file.write(f'{url}\n')

    return 0


if __name__ == '__main__':
    sys.exit(main())
