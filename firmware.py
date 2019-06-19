# -*- coding: utf-8 -*-

"""
Handles Stub Firmwares
and module retrieval

Copyright (c) 2019 Braden Mars
"""


from github import Github
from packaging import version
from pathlib import Path
from os import environ


class Firmware:
    """MicroPython Firmware"""

    def __init__(self, name, port, firmware_info, tag=None, **kwargs):
        self.tag = version.parse(tag) if tag else None
        self.port = port
        self.__dict__.update(firmware_info)
        self.module_path = Path(self.module_path.format(self.port))
        self.git = Github(environ.get("GIT_API_TOKEN"))

    @staticmethod
    def parse_version(text):
        """Validate Version Number"""
        # TODO: Open PR on createstubs.py to use sys.implementation for version
        ver = version.parse(str(text))
        if not isinstance(ver, version.Version) and text != 'master':
            raise Exception("Invalid Version")
        return ver

    def get_compatible_tags(self):
        """returns tags compatible with current device"""
        repo = self.git.get_repo(self.repo)
        repo_tag_objs = list(repo.get_tags())
        repo_tag_objs.append(repo.get_branch('master'))
        compat = {}
        for tag in repo_tag_objs:
            version = str(self.parse_version(tag.name))
            compat[version] = {
                'git_tag': tag.name,
                'sha': tag.commit.sha,
                'latest': repo_tag_objs.index(tag) == 0,
                'devices': []
            }
            try:
                repo.get_contents(str(self.module_path), ref=tag.name)
            except Exception:
                pass
            else:
                if len(compat[version]['devices']) == 0:
                    compat[version]['devices'] = []
                compat[version]['devices'].append(self.port)
        return compat

    def fetch_modules(self, exclude=None):
        """Fetch modules from git repository"""
        exclude = exclude or self.excluded_modules
        repo = self.git.get_repo(self.repo)
        repo_tags_objs = repo.get_tags()
        tag_obj = next(
            (i for i in repo_tags_objs
                if self.parse_version(i.name) == self.tag))
        self.tag_obj = tag_obj
        repo_mods = repo.get_contents(str(self.module_path), ref=tag_obj.name)
        subdirs = [repo.get_contents(i.path)
                   for i in repo_mods if i.type == 'dir']
        for files in subdirs:
            repo_mods.extend(files)
        modules = [i
                   for i in repo_mods if i.name not in exclude
                   and i.type != "dir"]
        return modules

    def write_module(self, content, path):
        """Write module content to file path"""
        parent = path.parent
        if not parent.exists():
            parent.mkdir(exist_ok=True, parents=True)
        path.write_bytes(content)
        return path

    def retrieve_modules(self, output_dir):
        """Retrieve Frozen Modules"""
        modules = self.fetch_modules()
        for mod in modules:
            out_dir = Path(str(output_dir))
            mod_path = Path(mod.path)
            out_path = out_dir / Path(*mod_path.parts[3:])
            print("OUT: ", str(out_path))
            if not out_path.parent.exists():
                out_path.parent.mkdir(exist_ok=True)
                print(out_path)
            name = str(out_path.name)
            try:
                content = mod.decoded_content
            except AssertionError:
                print(f"Could not decode {name}")
                repo = self.git.get_repo(self.repo)
                file = repo.get_file_contents(mod.path, ref=self.tag_obj.name)
                try:
                    print("Trying Again with:", file.path)
                    content = file.decoded_content
                    self.write_module(content, out_path)
                except AssertionError:
                    print(f"Failed to write {name}")
                    self.write_module(b"ERROR", out_path)
            else:
                print(f"Module: {name} => {str(out_path)}")
                self.write_module(content, out_path)
        return modules
