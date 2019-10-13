#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Micropy-Stubs
Copyright (c) 2019 Braden Mars

Crawls file tree looking for info.json files,
sorting them by either firmware or device.

If a firmware file is found, it creates the file structure required.
If a device file is found, it will then download its required modules
and freeze them. The stubs and info file must be added manually

Note: This is currently a WIP. The end goal is to have a mostly automated
method of creating 'stub packages' with device-specific and firmware-specific
modules included for micropy-cli.
Also, yes script very much needs to be refactored.
I will do this along with some tests soon.

"""

import json
import shutil
import subprocess as subp
import sys
import tarfile
import tempfile
from contextlib import contextmanager
from itertools import chain
from pathlib import Path
from pprint import pprint

import click
import dictdiffer as dictdiff
import requests
from deepmerge import always_merger

import packages as pkg
import upip
from firmware import Firmware
from logbook import Logger, StreamHandler
from logbook.more import ColorizingStreamHandlerMixin

# Paths / State
ROOT = (Path(__file__).parent).resolve()
PKG_ROOT = ROOT / 'packages'
def_files = PKG_ROOT.glob("**/info.json")
INFO = {
    'firmware': [],
    'device': [],
    'stats': [],
    'errors': []
}

# Logging Setup


class LogHandler(ColorizingStreamHandlerMixin, StreamHandler):
    """Colorized Stream Handler"""


log_handler = LogHandler(sys.stdout, level="INFO").push_application()
log = Logger('micropy')


@contextmanager
def file_backups(target_dir, glob_pattern):
    """Backup Files in Case of Failure

    Creates temporary backup file which is used
    to restore the original file if it is not
    updated/recreated on exiting the context.

    Args:
        target_dir (os.Pathlike): Path to target
        glob_pattern (str): Glob Pattern of Files to Backups
    """
    target = Path(target_dir)
    files = list(target.rglob(glob_pattern))
    backups = []
    for file in files:
        log.debug(f"Backup: {file.name}")
        backup = file.with_suffix(file.suffix + ".back")
        file.rename(backup)
        backups.append((file, backup))
    try:
        yield backups
    finally:
        for orig, backup in backups:
            if not orig.exists():
                log.warning(f"Restoring {orig.name} to backup.")
                rel_path = orig.relative_to(target_dir.parent)
                INFO['errors'].append({
                    "type": "Module",
                    "msg": f"{rel_path} was restored from backup."
                })
                backup.replace(orig)
            if backup.exists():
                backup.unlink()


def make_stubs(target_dir):
    """Call make_stub_files on a directory"""
    stub_dir = (ROOT / 'tools' / 'stubber' / 'runOnPc').resolve()
    py_file = stub_dir / 'make_stub_files.py'
    py_cfg = stub_dir / 'make_stub_files.cfg'
    target = Path(str(target_dir)).resolve()
    dirs = set([p.parent for p in target.rglob('*.py')])
    with file_backups(target, "*.pyi"):
        for d in dirs:
            args = ["python", str(py_file), "-c",
                    str(py_cfg), "-u", f"{str(d)}/*.py"]
            subp.run(args, capture_output=True)


def get_git_module(repo, path, target_dir):
    """Download module from git"""
    url = f"https://raw.githubusercontent.com/{repo}/master/{path}"
    data = requests.get(url).text
    mod_path = Path(path)
    log.notice(f"Installing {mod_path.name} via Git")
    target = target_dir / mod_path.name
    log.info(f"{repo}:{mod_path.name} => {target.relative_to(PKG_ROOT)}")
    log.debug(f"Retrieving {mod_path.name} from {url} to {target}")
    with target.open('w+') as f:
        f.write(data)


def get_module(module, target_dir, prefix=None):
    """Download module from pypi or url"""
    _module = module.split("@")
    target = Path(str(target_dir)).resolve()
    if len(_module) > 1:
        return get_git_module(*_module, target)
    _prefix = prefix or "micropython"
    module = f"{_prefix}-{module}"
    log.notice(f"Installing {module} via upip...")
    log.info(f"{module} => {target.relative_to(PKG_ROOT)}")
    try:
        upip.print = log.debug
        upip.install(module, str(target))
    except upip.NotFoundError:
        INFO['errors'].append({
            "type": "Module",
            "msg": f"Package {module} not found!"
        })
    except Exception:
        INFO['errors'].append({
            "type": "Module",
            "msg": f"Package {module} failed to install!"
        })
    else:
        return module


def get_file(path):
    """Get file by info path"""
    log.debug(f"Found: {path}")
    data = json.load(path.open())
    scope = data.get('scope', 'device')
    return (data, scope)


def sort_info(glob):
    """Sort info files by scope"""
    log.notice("Searching for Info Files...")
    for f in glob:
        data, scope = get_file(f)
        data['path'] = str(f.relative_to(ROOT))
        if not INFO[scope]:
            INFO[scope] = []
        INFO[scope].append(data)
    return INFO


def get_devices_by_firm(fware):
    """get devices by firmware file"""
    devices = [f for f in INFO['device'] if f['firmware']['name'] == fware]
    return devices


def get_firm_by_device(device):
    """get firmware info from device"""
    fwares = INFO['firmware']
    dev_fware = device['firmware']['name']
    firm = next((f for f in fwares if f['firmware'] == dev_fware))
    return firm


def update_device(device_info, existing):
    """update device info file"""
    path = Path(device_info['path']).parent
    frozen_path = path / 'frozen'
    if not frozen_path.exists() or existing:
        device_info = add_device(device_info)
    return device_info


def update_firmware_modules(firm):
    """Update firmware specific modules"""
    path = Path(firm['path']).parent / 'frozen'
    path.mkdir(exist_ok=True, parents=True)
    modules = firm.get('modules')
    mod_prefix = firm.get('module_prefix', None)
    if not modules:
        placeholder = path / 'none.txt'
        placeholder.touch()
        return firm
    with file_backups(path, "*.py"):
        modules = [get_module(m, path, prefix=mod_prefix) for m in modules]
    make_stubs(path)
    return firm


def update_firmware(firm, existing=False):
    """update firmware info file"""
    versions = firm.get('versions', None)
    if not versions or existing:
        firm = add_firmware(firm)
        update_firmware_modules(firm)
    else:
        if existing:
            update_firmware_modules(firm)
    fware = firm['firmware']
    devices = get_devices_by_firm(fware)
    loaded = [update_device(d, existing) for d in devices]
    versions = firm['versions']
    possible = len([d for v in versions for d in v['devices']])
    INFO['stats'].append({
        'firmware': fware,
        'loaded': len(loaded),
        'possible': possible
    })
    return firm


def add_device(device):
    """add device from info file"""
    fware_info = get_firm_by_device(device)
    dev_fware = device['firmware']
    # Find a suitable port
    _port_attrs = ['machine', 'sysname', 'nodename']
    _port_ids = [dev_fware.get(a).lower().split() for a in _port_attrs]
    port_ids = set(chain.from_iterable(_port_ids))
    fware_devs = [d.lower() for d in fware_info['devices']]
    port = list(set(fware_devs).intersection(port_ids))[0]
    fware_tag = dev_fware['version']
    fware_versions = [v['version'] for v in fware_info['versions']]
    if fware_tag not in fware_versions:
        try:
            fware_tag = fware_versions[0]
        except IndexError:
            fware_tag = "master"
    fware = Firmware(firmware_info=fware_info, port=port, tag=fware_tag)
    device_root = Path(device['path']).parent
    mods_out = device_root / 'frozen'
    with file_backups(mods_out, "*.py"):
        mods_out.mkdir(exist_ok=True, parents=True)
        fware.retrieve_license(device_root)
        mod_paths = fware_info['module_path']
        if isinstance(
                mod_paths, list) and any(
                (i for i in mod_paths if '@' in i)):
            for mod_path in mod_paths:
                out_append, repo_path = mod_path.split('@')
                submod_out = mods_out / out_append / repo_path
                mods_out.mkdir(exist_ok=True, parents=True)
                fware.module_path = [Path(repo_path)]
                fware.retrieve_modules(submod_out)
        else:
            fware.retrieve_modules(mods_out)
    make_stubs(mods_out)
    return device


def add_firmware(firm):
    """add firmware from info file"""
    ports = firm['devices']
    path = Path(firm['path']).parent
    versions = []
    updated_firm = firm.copy()
    for p in ports:
        fware = Firmware(port=p, firmware_info=firm)
        licenses = firm.get('licenses', [])
        for file in licenses:
            repo, file_path = file.split(':')
            fware.retrieve_license(path, repository=repo, repo_path=file_path)
        compat = fware.get_compatible_tags()
        for cmp in compat:
            prev_compat = next(
                (v for v in versions if v['version'] == cmp['version']), None)
            if prev_compat:
                always_merger.merge(prev_compat, cmp)
            else:
                versions.append(cmp)
    updated_firm['versions'] = versions
    for vers in versions:
        devices = vers.get('devices')
        if len(vers['devices']) >= 0:
            v_dir = path / vers['git_tag']
            dev_dirs = [Path(v_dir / dev) for dev in devices]
            [d.mkdir(exist_ok=True, parents=True) for d in dev_dirs]
    json.dump(updated_firm, Path(updated_firm['path']).open(
        'w'), indent=2, sort_keys=False)
    fware_index = INFO['firmware'].index(firm)
    INFO['firmware'].pop(fware_index)
    INFO['firmware'].append(updated_firm)
    return updated_firm


def get_stub_name(stub):
    """return stub pkg name"""
    scope = stub.get('scope', 'device')
    if scope == 'firmware':
        return stub['firmware']
    dev_fware = stub['firmware']
    dev_name = dev_fware['sysname']
    name = f"{dev_name}-{dev_fware['name']}-{dev_fware['version']}"
    return name


def archive_device(device, name, commit=False, **kwargs):
    """archive a device stub"""
    path = Path(device['path']).parent
    if commit:
        pkg.create_or_update_package_branch(path, name, **kwargs)
    pkg.add_package(path, name)
    return create_archive(path, name)


def archive_firmware(firmware, name, commit=False, **kwargs):
    """archive a firmware stub"""
    path = Path(firmware['path']).parent
    if commit:
        pkg.create_or_update_package_branch(path, name, **kwargs)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / name
        tmp_path.mkdir()
        shutil.copytree((path / 'frozen'), (tmp_path / 'frozen'))
        shutil.copy2((path / 'info.json'), tmp_path)
        pkg.add_package(tmp_path, name, stub_type='firmware')
        return create_archive(tmp_path, name)


def archive_stub(stub, **kwargs):
    """archive given stub"""
    scope = stub.get('scope', 'device')
    name = get_stub_name(stub)
    with pkg.with_package_log(name):
        if scope == 'firmware':
            return archive_firmware(stub, name, **kwargs)
        return archive_device(stub, name, **kwargs)


def create_archive(path, archive_name, **kwargs):
    """archive given path to tarfile at dest"""
    dist_path = ROOT / 'dist'
    dist_path.mkdir(exist_ok=True, parents=True)
    archive_path = dist_path / (archive_name + '.tar.gz')
    if archive_path.exists():
        archive_path.unlink()
    with tarfile.open(str(archive_path), 'w:gz') as tar:
        tar.add(str(path), arcname=archive_name, **kwargs)
    return archive_path


def resolve_stub(stub_name):
    stubs = [*INFO['device'], *INFO['firmware']]
    avail_stubs = set((get_stub_name(i) for i in stubs))
    try:
        stub = next(
            (i for i in stubs if get_stub_name(i) == stub_name.strip()))
    except StopIteration:
        print(f"Could not find: {stub_name}")
        avail = "\n".join(avail_stubs)
        print(f"Available Stubs:")
        print(avail)
        sys.exit(1)
    else:
        return stub


@click.group()
@click.option('--verbose', '-v', is_flag=True,
              default=False, help="Enable verbose output.")
def cli(verbose=False):
    """Micropy Stubs Cli"""
    if verbose:
        LogHandler(sys.stdout, level="DEBUG").push_application()
    sort_info(def_files)


@cli.command()
@click.argument('stub_name', default=None, required=False)
@click.option('--all', 'do_all', default=False, is_flag=True,
              help="Archive all stubs")
@click.option('--clean', default=False, is_flag=True,
              help="Remove existing archives")
@click.option('--commit', default=False, is_flag=True,
              help="Commit Changes to Package Branches")
@click.option('--force', default=False, is_flag=True,
              help="Update Package Branch even if no changes were made")
def archive(stub_name, **kwargs):
    """Archive Stubs"""
    stubs = [*INFO['device'], *INFO['firmware']]
    archives = []
    do_commit = kwargs.get('commit', False)
    force = kwargs.get('force', False)
    if kwargs.get('clean'):
        dist = ROOT / 'dist'
        if dist.exists():
            shutil.rmtree(dist)
        log.debug("Cleaned dist folder")
    if kwargs.get('do_all'):
        log.notice("Archiving all stubs...")
        archives.extend(
            [archive_stub(s, commit=do_commit, force=force) for s in stubs])
    if stub_name:
        stub = resolve_stub(stub_name)
        archives.append(archive_stub(stub, commit=do_commit, force=force))
    if archives:
        archives = iter(archives)
        for a in archives:
            log.notice("Archived:", a.name)
        print("Done!")
    pkg.update_package_source()


@cli.command()
@click.option('-f', '--firmware', default=None,
              help="Specific firmware to generate")
@click.option('-u', '--update', is_flag=True,
              help="Update existing firmware modules")
def generate(firmware, update):
    """Generate Stubs"""
    files = sort_info(def_files)
    fwares = files['firmware']
    if firmware:
        fwares = [resolve_stub(firmware)]
    for firm in fwares:
        update_firmware(firm, existing=update)
    stats = INFO['stats']
    errors = INFO['errors']
    pkg.format_info_files()
    print("Report:")
    for s in stats:
        print(f"\n{s['firmware']}:")
        print(f"Devices Loaded: {s['loaded']}/{s['possible']}")
    if errors:
        print("\nThe following errors occured:")
        for e in errors:
            print("\nType:", e['type'])
            print("Message:", e.get('msg'))


if __name__ == '__main__':
    cli()
