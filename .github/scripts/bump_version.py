#!/usr/bin/env python3
"""
Automated Semantic Versioning Script
====================================

This script implements automated semantic versioning for the DemoTWinCAT repository.
It reads the current version from the VERSION file, applies appropriate version bumps
based on branch and merge context, and updates the VERSION file accordingly.

Version Format: MAJOR.MINOR.PATCH.BUILD (e.g., 1.0.0.0)

Versioning Rules:
- main branch merges: 
  - Major: Breaking changes or significant new features
  - Minor: New features, enhancements
  - Patch: Bug fixes, hotfixes
- development branch merges:
  - Build: Development features, continuous integration builds

Usage:
    python bump_version.py --branch <branch_name> --bump-type <type>
    python bump_version.py --branch main --bump-type minor
    python bump_version.py --branch development --bump-type build
"""

import argparse
import sys
import os
import re
from pathlib import Path
from typing import Tuple, Optional


class VersionBumper:
    """Handles semantic version bumping operations."""
    
    def __init__(self, version_file: str = "VERSION"):
        """
        Initialize the version bumper.
        
        Args:
            version_file: Path to the VERSION file relative to repo root
        """
        self.repo_root = Path(__file__).parent.parent.parent
        self.version_file = self.repo_root / version_file
        
    def read_version(self) -> Tuple[int, int, int, int]:
        """
        Read the current version from the VERSION file.
        
        Returns:
            Tuple of (major, minor, patch, build) version numbers
            
        Raises:
            FileNotFoundError: If VERSION file doesn't exist
            ValueError: If version format is invalid
        """
        if not self.version_file.exists():
            raise FileNotFoundError(f"VERSION file not found at {self.version_file}")
            
        version_text = self.version_file.read_text().strip()
        
        # Validate version format (MAJOR.MINOR.PATCH.BUILD)
        version_pattern = r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$"
        match = re.match(version_pattern, version_text)
        
        if not match:
            raise ValueError(f"Invalid version format: '{version_text}'. Expected: MAJOR.MINOR.PATCH.BUILD")
            
        return tuple(int(x) for x in match.groups())
    
    def write_version(self, major: int, minor: int, patch: int, build: int) -> None:
        """
        Write the new version to the VERSION file.
        
        Args:
            major: Major version number
            minor: Minor version number  
            patch: Patch version number
            build: Build version number
        """
        version_string = f"{major}.{minor}.{patch}.{build}"
        self.version_file.write_text(version_string + "\n")
        print(f"✅ Version updated to: {version_string}")
    
    def bump_version(self, bump_type: str, branch: str) -> Tuple[int, int, int, int]:
        """
        Bump the version according to the specified type and branch context.
        """
        current = self.read_version()
        major, minor, patch, build = current
        
        print(f"📋 Current version: {major}.{minor}.{patch}.{build}")
        print(f"🔧 Bump type: {bump_type}")
        print(f"🌿 Branch: {branch}")
        
        # Auto-detect bump type based on branch if not specified
        if bump_type == "auto":
            bump_type = self._auto_detect_bump_type(branch)
        
        # Apply version bump logic with proper resets
        if bump_type == "major":
            major += 1
            minor = 0  # Reset minor
            patch = 0  # Reset patch  
            build = 0  # Reset build
        elif bump_type == "minor":
            minor += 1
            patch = 0  # Reset patch
            build = 0  # Reset build
        elif bump_type == "patch":
            patch += 1
            build = 0  # Reset build
        elif bump_type == "build":
            build += 1
        else:
            raise ValueError(f"Invalid bump type: {bump_type}")
        
        return (major, minor, patch, build)
    
    def _auto_detect_bump_type(self, branch: str) -> str:
        """Auto-detect the appropriate bump type based on branch name."""
        branch_lower = branch.lower()
        
        # Main branch - minor releases (not major during normal development)
        if branch_lower in ["main", "master"]:
            return "minor"  # Changed from "major" to "minor"
        
        # Release branch - minor releases for version releases
        elif branch_lower.startswith("release/"):
            return "minor"
        
        # Development branch - patch releases
        elif branch_lower in ["development", "develop", "dev"]:
            return "patch"
        
        # Hotfix branches - build releases
        elif branch_lower.startswith(("hotfix/", "fix/")):
            return "build"
        
        # Feature branches - build releases
        elif branch_lower.startswith(("feature/", "feat/")):
            return "build"
        
        else:
            print(f"⚠️  Unknown branch pattern: {branch}. Defaulting to build bump.")
            return "build"


def is_fork_pr() -> bool:
    """
    Check if the current context is a pull request from a fork.
    
    Returns:
        True if this is a fork PR, False otherwise
    """
    # Check GitHub Actions environment variables
    github_event_name = os.getenv("GITHUB_EVENT_NAME", "")
    github_head_ref = os.getenv("GITHUB_HEAD_REF", "")
    github_repository = os.getenv("GITHUB_REPOSITORY", "")
    pr_head_repo = os.getenv("GITHUB_EVENT_PULL_REQUEST_HEAD_REPO_FULL_NAME", "")
    
    # If it's a pull request and the head repository is different from base repository
    if github_event_name == "pull_request":
        if pr_head_repo and pr_head_repo != github_repository:
            print(f"🚫 Fork PR detected: {pr_head_repo} -> {github_repository}")
            return True
            
    # Additional check for head ref (external branches often have different patterns)
    if github_head_ref and github_repository:
        # This is a basic check - could be enhanced based on specific fork patterns
        pass
    
    return False


def main():
    """Main entry point for the version bump script."""
    parser = argparse.ArgumentParser(
        description="Bump semantic version based on branch and merge context",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bump_version.py --branch main --bump-type minor
  python bump_version.py --branch development --bump-type build  
  python bump_version.py --branch main --bump-type auto
  python bump_version.py --dry-run --branch main --bump-type patch
        """
    )
    
    parser.add_argument(
        "--branch",
        required=True,
        help="Git branch name for context-aware version bumping"
    )
    
    parser.add_argument(
        "--bump-type",
        choices=["major", "minor", "patch", "build", "auto"],
        default="auto",
        help="Type of version bump to apply (default: auto)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes"
    )
    
    parser.add_argument(
        "--skip-fork-check",
        action="store_true",
        help="Skip fork detection and proceed with version bump"
    )
    
    args = parser.parse_args()
    
    try:
        # Check if this is a fork PR and skip if so
        if not args.skip_fork_check and is_fork_pr():
            print("🚫 Skipping version bump for fork PR")
            return 0
        
        # Initialize version bumper
        bumper = VersionBumper()
        
        # Calculate new version
        new_version = bumper.bump_version(args.bump_type, args.branch)
        
        if args.dry_run:
            print(f"🔍 Dry run: Would update version to {'.'.join(map(str, new_version))}")
            return 0
        
        # Write new version
        bumper.write_version(*new_version)
        
        print(f"🎉 Version bump completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())