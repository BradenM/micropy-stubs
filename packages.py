#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Micropy-Stubs
Copyright (c) 2019 Braden Mars

Module for creating/updating stub package git branches.

"""


import hashlib
import json
import subprocess as sp
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from shutil import copytree

REPO_SOURCE = Path(__file__).parent / 'source.json'
REPO = json.loads(REPO_SOURCE.read_text())
REPO_ROOT = Path(__file__).parent
WORK_DIR = Path.cwd()


@contextmanager
def create_or_reset_branch(ref=None):
    """Create or Reset a Git Branch

    Args:
        ref (str, optional): Git ref of branch.
         Defaults to None. If None, master is used.
    """
    branch_ref = ref or 'master'
    current_branch = execute(
        'git rev-parse --abbrev-ref HEAD', shell=True, text=True).stdout
    execute(f"git checkout -B {branch_ref}", shell=True)
    try:
        yield ref
    finally:
        execute(f'git checkout --force {current_branch}', shell=True)


@contextmanager
def temp_repo():
    """Creates a temporary copy of repo to use."""
    global WORK_DIR
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        dest = tmp_path / 'micropy-stubs'
        copytree(REPO_ROOT, dest)
        WORK_DIR = dest
        execute(f"git rm --cached --ignore-unmatch tools/stubber", shell=True)
        yield WORK_DIR
    WORK_DIR = Path.cwd()


def get_change_count(root_path=None):
    """Get the num of git file changes.

    Args:
        root_path (str, optional): Root path to check from.
         Defaults to None. If none, current dir is used.

    Returns:
        int: Num of Changes.
    """
    root_path = root_path or Path.cwd()
    _cmd = (f"git diff --cached --numstat {root_path} | wc -l")
    result = execute(_cmd, text=True, shell=True).stdout
    count = int(result.strip())
    return count


def execute(cmd, **kwargs):
    """Subprocess Wrapper

    Args:
        cmd (list): Command to Execute.

    """
    global WORK_DIR
    check = kwargs.pop('check', True)
    print("[CMD]: ", cmd)
    print("[CWD]: ", WORK_DIR)
    if not kwargs.get('shell', None):
        cmd = cmd.split()
    proc = sp.run(cmd, capture_output=True,
                  check=check, cwd=WORK_DIR, **kwargs)
    print("[RESULT]: ", proc.stdout)
    print("[ERROR]: ", proc.stderr)
    return proc


def create_or_update_package_branch(root_path, name, force=False):
    """Creates or Updates a Stub Package Branch.

    Args:
        root_path (str): Root Path to Stub Package.
        name (str): Stub Package Name.
        force (bool, optional): Force update even
            if no changes are found. Defaults to False.
    """
    ref_path = f"pkg/{name}"
    if Path(root_path).is_absolute():
        root_path = root_path.relative_to(Path.cwd())
    print(f"\nCREATING PACKAGE BRANCH: {root_path} - {ref_path}")
    with temp_repo():
        with create_or_reset_branch(ref=ref_path) as ref:
            execute((
                "git filter-branch --force --prune-empty "
                f"--subdirectory-filter {root_path} "
                "--index-filter 'git rm --cached --ignore-unmatch "
                '"v*/**/*"\''
            ), shell=True)
            execute(f"git push --force -u origin {ref}:{ref}", shell=True)
    print("Done.")


def update_package_source():
    """Updates Repos source.json file"""
    now = datetime.now().strftime("%m/%d/%y")
    commit_msg = "chore({}): Update Package Sources"
    commit_msg = commit_msg.format(now)
    REPO_SOURCE.write_text(json.dumps(REPO, indent=2, sort_keys=False))
    print("Updating repo source...")
    execute("pre-commit run --hook-stage commit -a", shell=True, check=False)
    execute("git add source.json", shell=True)
    if get_change_count():
        execute("git add source.json", shell=True)
        print("Commiting updates...")
        execute(f"git commit -m '{commit_msg}'", shell=True, check=False)
    current_branch = execute(
        'git rev-parse --abbrev-ref HEAD', shell=True, text=True).stdout
    execute(f"git push origin {current_branch}", shell=True)


def calc_package_checksum(path):
    """Calculates checksum of given package path.

    Args:
        path (str): Path to generate checksum of.

    """
    print("\nCalculating Package Checksum...")
    cksum = hashlib.sha256()
    glob = Path(path).rglob("*")
    files = [f for f in glob if f.is_file()]
    for file in files:
        print("Hashing: ", file.name)
        cksum.update(file.read_bytes())
    hdigest = cksum.hexdigest()
    print("Checksum Calculated: ", hdigest, "\n")
    return hdigest


def add_package(path, name, stub_type='device', queue=True):
    """Adds Package to Repos source.json file

    Args:
        path (str): Path to package root.
        name (str): Package name
        stub_type (str, optional): Stub Type. Defaults to 'device'.
        queue (bool, optional): Queues changes rather
            than executing immediately. Defaults to True.

    Returns:
        [type]: [description]
    """
    cksum = calc_package_checksum(path)
    pkg = {
        'name': name,
        'type': stub_type,
        'sha256sum': cksum
    }
    existing = next(
        (pkg for pkg in REPO['packages'] if pkg['name'] == name), None)
    if existing:
        print("Updating existing package...")
        REPO['packages'].remove(existing)
    print("Adding package...")
    REPO['packages'].append(pkg)
    return pkg


def format_info_files():
    """Executes pre-commit prettier hook"""
    print("[INFO]: Formatting Info Files...")
    return execute("pre-commit run --hook-stage commit -a",
                   shell=True, check=False)
