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
from itertools import chain
from pathlib import Path
from pprint import pprint

import click
import dictdiffer as dictdiff
import requests
from deepmerge import always_merger

import upip
from firmware import Firmware

ROOT = (Path(__file__).parent).resolve()
PKG_ROOT = ROOT / 'packages'
def_files = PKG_ROOT.glob("**/info.json")
INFO = {
    'firmware': [],
    'device': [],
    'stats': [],
    'errors': []
}


def make_stubs(target_dir):
    """Call make_stub_files on a directory"""
    stub_dir = (ROOT / 'tools' / 'stubber' / 'runOnPc').resolve()
    py_file = stub_dir / 'make_stub_files.py'
    py_cfg = stub_dir / 'make_stub_files.cfg'
    target = Path(str(target_dir)).resolve()
    dirs = set([p.parent for p in target.rglob('*.py')])
    for d in dirs:
        args = ["python", str(py_file), "-c",
                str(py_cfg), "-u", f"{str(d)}/*.py"]
        subp.run(args, capture_output=True)


def get_git_module(repo, path, target_dir):
    """Download module from git"""
    print("Installing via Git")
    url = f"https://raw.githubusercontent.com/{repo}/master/{path}"
    data = requests.get(url).text
    target = target_dir / Path(path).name
    print(f"{url} => {target}")
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
    try:
        upip.install(module, str(target))
    except upip.NotFoundError:
        INFO['errors'].append({
            "type": "Module",
            "msg": f"Package {module} not found!"
        })


def get_file(path):
    """Get file by info path"""
    data = json.load(path.open())
    scope = data.get('scope', 'device')
    return (data, scope)


def update_file(orig, new):
    """Update Json"""
    update_diff = dictdiff.diff(orig, new)
    pprint("Update Diff:")
    changes = [i for i in update_diff if i[0] == 'change']
    removed = [i for i in update_diff if i[0] == 'remove']
    print("==============")
    print("CHANGES:")
    pprint(changes)
    print("==============")
    print("REMOVED:")
    pprint(removed)
    print("==============")
    path = orig['path']
    json.dump(new, Path(path).open('w'))
    return new


def sort_info(glob):
    """Sort info files by scope"""
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


def update_device(device_info):
    """update device info file"""
    path = Path(device_info['path']).parent
    frozen_path = path / 'frozen'
    if not frozen_path.exists():
        device_info = add_device(device_info)
    return device_info


def update_firmware_modules(firm):
    """Update firmware specific modules"""
    path = Path(firm['path']).parent / 'frozen'
    if path.exists():
        shutil.rmtree(str(path))
    path.mkdir(exist_ok=True, parents=True)
    modules = firm.get('modules')
    mod_prefix = firm.get('module_prefix', None)
    if not modules:
        return firm
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
    loaded = [update_device(d) for d in devices]
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
    fware_devs = [d for d in fware_info['devices']]
    port = list(set(fware_devs).intersection(port_ids))[0]
    fware_tag = dev_fware['version']
    fware_versions = [v['version'] for v in fware_info['versions']]
    if fware_tag not in fware_versions:
        fware_tag = fware_versions[0]
    fware = Firmware(firmware_info=fware_info, port=port, tag=fware_tag)
    mods_out = Path(device['path']).parent / 'frozen'
    mods_out.mkdir(exist_ok=True, parents=True)
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
    new = update_file(firm, updated_firm)
    fware_index = INFO['firmware'].index(firm)
    INFO['firmware'].pop(fware_index)
    INFO['firmware'].append(new)
    return new


def get_stub_name(stub):
    """return stub pkg name"""
    scope = stub.get('scope', 'device')
    if scope == 'firmware':
        return stub['firmware']
    dev_fware = stub['firmware']
    dev_name = dev_fware['sysname']
    name = f"{dev_name}-{dev_fware['name']}-{dev_fware['version']}"
    return name


def archive_device(device):
    """archive a device stub"""
    path = Path(device['path']).parent
    pkg_name = get_stub_name(device)
    return create_archive(path, pkg_name)


def archive_firmware(firmware):
    """archive a firmwre stub"""
    path = Path(firmware['path']).parent
    name = get_stub_name(firmware)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir) / name
        tmp_path.mkdir()
        shutil.copytree((path / 'frozen'), (tmp_path / 'frozen'))
        shutil.copy2((path / 'info.json'), tmp_path)
        return create_archive(tmp_path, name)


def archive_stub(stub):
    """archive given stub"""
    scope = stub.get('scope', 'device')
    if scope == 'firmware':
        return archive_firmware(stub)
    return archive_device(stub)


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
def cli():
    """Micropy Stubs Cli"""
    sort_info(def_files)


@cli.command()
@click.argument('stub_name', default=None, required=False)
@click.option('--all', 'do_all', default=False, is_flag=True,
              help="Archive all stubs")
@click.option('--clean', default=False, is_flag=True,
              help="Remove existing archives")
def archive(stub_name, **kwargs):
    """Archive Stubs"""
    stubs = [*INFO['device'], *INFO['firmware']]
    archives = []
    if kwargs.get('clean'):
        dist = ROOT / 'dist'
        if dist.exists():
            shutil.rmtree(dist)
        print("Cleaned dist folder")
    if kwargs.get('do_all'):
        print("Archiving all stubs...")
        archives.extend([archive_stub(s) for s in stubs])
    if stub_name:
        stub = resolve_stub(stub_name)
        archives.append(archive_stub(stub))
    if archives:
        archives = iter(archives)
        for a in archives:
            print("Archived:", a.name)
        print("Done!")


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
