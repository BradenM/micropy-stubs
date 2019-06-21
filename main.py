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


import dictdiffer as dictdiff
from pathlib import Path
import json
from pprint import pprint
from firmware import Firmware
from deepmerge import always_merger
import subprocess as subp
import upip
from shutil import rmtree, copy2, copytree
import click
import tarfile
import tempfile

ROOT = (Path(__file__).parent).resolve()
PKG_ROOT = ROOT / 'packages'
def_files = PKG_ROOT.glob("**/info.json")
INFO = {
    'firmware': [],
    'device': [],
    'stats': {}
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


def get_module(module, target_dir):
    """Download module from pypi"""
    target = Path(str(target_dir)).resolve()
    module = f"micropython-{module}"
    return upip.install(module, str(target))


def get_file(path):
    """Get file by info path"""
    data = json.load(path.open())
    scope = data.get('scope')
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
        pprint(data)
        if not INFO[scope]:
            INFO[scope] = []
        INFO[scope].append(data)
    return INFO


def get_devices_by_firm(fware):
    """get devices by firmware file"""
    devices = [f for f in INFO['device'] if f['firmware'] == fware]
    return devices


def get_firm_by_device(device):
    """get firmware info from device"""
    fwares = INFO['firmware']
    dev_fware = device['firmware']
    firm = next((f for f in fwares if f['firmware'] == dev_fware))
    return firm


def update_device(device_info):
    """update device info file"""
    def update_files(key, path):
        for m in path.iterdir():
            if m.suffix == '.py':
                file = {
                    "name": m.stem,
                    "path": str(m.relative_to(path.parent))
                }
                new_device[key].append(file)
        new_device[key] = list(
            {v['name']: v for v in new_device[key]}.values())
    path = Path(device_info['path']).parent
    dev_mods = device_info.get('modules', None)
    if not dev_mods or len(dev_mods) == 0:
        device_info = add_device(device_info)
    modules = path / 'modules'
    stubs = path / 'stubs'
    new_device = device_info.copy()
    update_files('modules', modules)
    update_files('stubs', stubs)
    return update_file(device_info, new_device)


def update_firmware_modules(firm):
    """Update firmware specific modules"""
    path = Path(firm['path']).parent / 'common' / 'modules'
    if path.exists():
        rmtree(str(path))
    path.mkdir(exist_ok=True, parents=True)
    modules = firm.get('modules')
    if not modules:
        return firm
    modules = [get_module(m, path) for m in modules]
    make_stubs(path)
    return firm


def update_firmware(firm):
    """update firmware info file"""
    versions = firm.get('versions', None)
    if not versions or len(versions.keys()) == 0:
        firm = add_firmware(firm)
    update_firmware_modules(firm)
    fware = firm['firmware']
    devices = get_devices_by_firm(fware)
    updated = [update_device(d) for d in devices]
    versions = firm['versions'].items()
    possible = [v for v, data in versions if len(data['devices']) > 0]
    INFO['stats'][fware] = {
        'loaded': len(updated),
        'missing': len(possible) - len(updated)
    }
    return firm


def add_device(device):
    """add device from info file"""
    fware_info = get_firm_by_device(device)
    # Find a suitable port
    _port_attrs = ['machine', 'sysname', 'nodename']
    _port_ids = [device['device'].get(a).lower().strip() for a in _port_attrs]
    port_ids = set([item for sublist in _port_ids for item in _port_ids])
    port = list(set(fware_info['devices']).intersection(port_ids))[0]
    fware_tag = device['version']
    fware = Firmware(firmware_info=fware_info, port=port, tag=fware_tag)
    mods_out = Path(device['path']).parent / 'modules'
    mods_out.mkdir(exist_ok=True, parents=True)
    fware.retrieve_modules(mods_out)
    make_stubs(mods_out)
    return device


def add_firmware(firm):
    """add firmware from info file"""
    ports = firm['devices']
    path = Path(firm['path']).parent
    versions = {}
    updated_firm = firm.copy()
    for p in ports:
        fware = Firmware(port=p, firmware_info=firm)
        compat = fware.get_compatible_tags()
        versions = always_merger.merge(versions, compat)
    updated_firm['versions'] = versions
    for vers, info in versions.items():
        devices = info.get('devices')
        if len(info['devices']) >= 0:
            v_dir = path / info['git_tag']
            dev_dirs = [Path(v_dir / dev) for dev in devices]
            [d.mkdir(exist_ok=True, parents=True) for d in dev_dirs]
    return update_file(firm, updated_firm)


def get_stub_name(device):
    """return stub pkg name"""
    fware = get_firm_by_device(device)
    dev_name = device['device']['sysname']
    name = f"{dev_name}-{fware['firmware']}@{device['version']}"
    return name


def archive_device(device):
    """Create archive from device"""
    fware = get_firm_by_device(device)
    fware_mods = Path(fware['path']).parent / 'common' / 'modules'
    dev_mods = Path(device['path']).parent / 'modules'
    dev_stubs = Path(device['path']).parent / 'stubs'
    modules = [*fware_mods.iterdir(), *dev_mods.iterdir()]
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        copytree(str(dev_stubs), str((tmp_path / 'stubs')))
        frozen = tmp_path / 'frozen'
        copy2(device['path'], str(tmp_path))
        for mod in modules:
            out_path = frozen / mod.name
            if mod.is_dir():
                copytree(str(mod), str(out_path))
            else:
                copy2(str(mod), str(out_path))
            print(out_path)
        archive_name = get_stub_name(device)
        tar_out = ROOT / 'dist' / f"{archive_name}.tar.gz"
        tar_out.parent.mkdir(exist_ok=True)
        with tarfile.open(str(tar_out), 'w:gz') as tar:
            tar.add(str(tmp_path), arcname=archive_name)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('stub_name', required=True)
def archive(stub_name=""):
    """Archive Stubs"""
    files = sort_info(def_files)
    avail_stubs = set((get_stub_name(i) for i in files['device']))
    try:
        device = next(
            (i for i in files['device'] if get_stub_name(i) == stub_name))
    except StopIteration:
        print(f"Could not find {stub_name}")
        avail = "\n".join(avail_stubs)
        print(f"Available Stubs:\n", avail)
        return
    return archive_device(device)


@cli.command()
def generate():
    """Generate Stubs"""
    files = sort_info(def_files)
    for firm in files['firmware']:
        update_firmware(firm)
    pprint(INFO['stats'])


if __name__ == '__main__':
    cli()
