#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to bump the version number in addon.xml
Usage: python bump_version.py [major|minor|patch]
"""

import os
import re
import sys
from datetime import datetime

def bump_version():
    """Bump the version number in addon.xml"""
    if len(sys.argv) != 2 or sys.argv[1] not in ['major', 'minor', 'patch']:
        print("Usage: python bump_version.py [major|minor|patch]")
        return
    
    bump_type = sys.argv[1]
    
    # Read addon.xml
    with open('addon.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract current version
    version_match = re.search(r'version="(\d+)\.(\d+)\.(\d+)"', content)
    if not version_match:
        print("Could not find version in addon.xml")
        return
    
    major, minor, patch = map(int, version_match.groups())
    
    # Bump version according to type
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    
    new_version = f"{major}.{minor}.{patch}"
    
    # Replace version in addon.xml
    content = re.sub(r'version="[\d\.]+"', f'version="{new_version}"', content)
    
    with open('addon.xml', 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Update changelog.txt
    today = datetime.now().strftime('%Y-%m-%d')
    with open('changelog.txt', 'r', encoding='utf-8') as f:
        changelog = f.read()
    
    # Add new version entry to changelog
    new_entry = f"v{new_version} ({today})\n- Version bump\n\n"
    changelog = new_entry + changelog
    
    with open('changelog.txt', 'w', encoding='utf-8') as f:
        f.write(changelog)
    
    print(f"Version bumped to {new_version}")

if __name__ == '__main__':
    bump_version()