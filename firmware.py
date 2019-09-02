# -*- coding: utf-8 -*-

"""
Handles Stub Firmwares
and module retrieval

Copyright (c) 2019 Braden Mars
"""


from os import environ
from pathlib import Path

from github import Github
from packaging import version


class Firmware:
    """MicroPython Firmware"""

    def __init__(self, port, firmware_info, tag=None, **kwargs):
        self.tag = version.parse(tag) if tag else None
        self.port = port
        self.name = kwargs.get('name', firmware_info.get('firmware'))
        self.__dict__.update(firmware_info)
        if not isinstance(self.module_path, list):
            self.module_path = [self.module_path]
        self.module_path = [Path(p.format(self.port))
                            for p in self.module_path]
        git_token = environ.get("GITHUB_TOKEN").strip()
        self.git = Github(login_or_token=git_token)

    @staticmethod
    def parse_version(text):
        """Validate Version Number"""
        ver = version.parse(str(text))
        if not isinstance(ver, version.Version) and text != 'master':
            return None
        if len(str(ver).split('.')) == 2:
            ver = version.parse(str(ver) + '.0')
        return ver

    def get_modules(self, repo, **kwargs):
        """get modules from module paths"""
        for path in self.module_path:
            contents = repo.get_contents(str(path), **kwargs)
            for c in contents:
                yield c

    def get_refs(self):
        """get tags/branch refs"""
        repo = self.git.get_repo(self.repo)
        repo_tag_objs = list(repo.get_tags())
        if not repo_tag_objs:
            repo_tag_objs.append(repo.get_branch('master'))
        exclusions = ('rc', 'post', 'b', 'r')
        repo_tag_objs = [t for t in repo_tag_objs if not any(
            i in t.name for i in exclusions)]
        repo_tag_objs = [
            t for t in repo_tag_objs if self.parse_version(t.name)]
        return (repo, repo_tag_objs)

    def get_compatible_tags(self):
        """returns tags compatible with current device"""
        repo, repo_tag_objs = self.get_refs()
        compat = []
        for tag in repo_tag_objs:
            version = str(self.parse_version(tag.name))
            vers_obj = {
                'version': version,
                'git_tag': tag.name,
                'sha': tag.commit.sha,
                'latest': repo_tag_objs.index(tag) == 0,
                'devices': []
            }
            try:
                list(self.get_modules(repo, ref=tag.name))
            except Exception:
                pass
            else:
                if len(vers_obj['devices']) == 0:
                    vers_obj['devices'] = []
                vers_obj['devices'].append(self.port)
            finally:
                compat.append(vers_obj)
        return compat

    def retrieve_license(self, dest, repository=None, repo_path="LICENSE"):
        """Attempt to find and download repo license"""
        _repo = repository or self.repo
        repo = self.git.get_repo(_repo)
        repo_path = Path(repo_path)
        if len(repo_path.parts) == 1:
            license_file = next(
                (i for i in repo.get_contents('/')
                 if i.path == repo_path.name), None)
        try:
            license_file = repo.get_contents(str(repo_path))
        except Exception:
            print("Failed to retrieve license:", str(repo_path))
            license_file = None
        # Lazy unique names
        file_name = str(repo_path).replace("/", "_")
        if license_file:
            file_dest = dest / file_name
            contents = repo.get_contents(
                license_file.path)
            return self.write_file_bytes(contents.decoded_content,
                                         file_dest)

    def fetch_modules(self, exclude=None):
        """Fetch modules from git repository"""
        exclude = exclude or self.excluded_modules
        repo, repo_tags_objs = self.get_refs()
        tag_obj = next(
            (i for i in repo_tags_objs
                if self.parse_version(i.name) == self.tag))
        self.tag_obj = tag_obj
        repo_mods = list(self.get_modules(repo, ref=tag_obj.name))
        subdirs = [repo.get_contents(i.path)
                   for i in repo_mods if i.type == 'dir']
        for files in subdirs:
            repo_mods.extend(files)
        modules = [i
                   for i in repo_mods if i.name not in exclude
                   and i.type != "dir"
                   and Path(i.name).suffix == ".py"
                   ]
        return modules

    def write_file_bytes(self, content, path):
        """Write bytes to file path"""
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
            failed_out = out_dir / 'failed.txt'
            mod_path = Path(mod.path)
            index_ref = self.module_path[0].name
            if len(self.module_path) > 1:
                index_ref = mod_path.parent.name
            mod_index = list(mod_path.parts).index(index_ref) + 1
            mod_stem = Path(*mod_path.parts[mod_index:])
            out_path = out_dir / mod_stem
            if out_path.parent.is_dir():
                out_path.parent.mkdir(exist_ok=True, parents=True)
            name = str(out_path.name)
            try:
                content = mod.decoded_content
            except AssertionError:
                print(f"Could not decode {name}")
                repo = self.git.get_repo(self.repo)
                file = repo.get_contents(mod.path, ref=self.tag_obj.name)
                try:
                    print("Trying Again with:", file.path)
                    content = file.decoded_content
                    self.write_file_bytes(content, out_path)
                except AssertionError:
                    with failed_out.open('a+') as f:
                        f.write(
                            f'\nFailed to retrieve: {name} from {mod.path}')
            else:
                print(f"Module: {name} => {str(out_path)}")
                self.write_file_bytes(content, out_path)
        return modules
