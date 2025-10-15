#!/usr/bin/env python3
"""
rename_user.py

This script renames a Linux user account using the `usermod` command.
It ensures the user exists before renaming and prints helpful status messages.

Example usage:
    sudo ./rename_user.py --old kevin --new kevinveenbirkenbach
"""

import argparse
import subprocess
import sys
import pwd


def user_exists(username):
    """Check if a given username exists on the system."""
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False


def run_command(command):
    """Run a system command and handle errors."""
    try:
        subprocess.run(command, check=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {' '.join(command)}")
        print(f"Error: {e}")
        sys.exit(1)


def rename_user(old_username, new_username):
    """Rename a user using usermod."""
    print(f"🔍 Checking if '{old_username}' exists...")
    if not user_exists(old_username):
        print(f"❌ The user '{old_username}' does not exist.")
        sys.exit(1)

    print(f"🔍 Checking if '{new_username}' already exists...")
    if user_exists(new_username):
        print(f"❌ The user '{new_username}' already exists.")
        sys.exit(1)

    print(f"🔧 Renaming user '{old_username}' → '{new_username}'...")
    run_command(["usermod", "-l", new_username, old_username])

    print(f"📁 Renaming home directory if it exists...")
    old_home = f"/home/{old_username}"
    new_home = f"/home/{new_username}"

    run_command(["usermod", "-d", new_home, "-m", new_username])

    print(f"✅ Successfully renamed user '{old_username}' to '{new_username}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Rename a Linux user account safely."
    )
    parser.add_argument("--old", required=True, help="Old username")
    parser.add_argument("--new", required=True, help="New username")

    args = parser.parse_args()

    rename_user(args.old, args.new)


if __name__ == "__main__":
    if not (sys.platform.startswith("linux")):
        print("❌ This script can only run on Linux systems.")
        sys.exit(1)

    if not (os.geteuid() == 0):
        print("❌ You must run this script as root (use sudo).")
        sys.exit(1)

    import os
    main()
