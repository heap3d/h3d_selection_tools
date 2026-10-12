#!/usr/bin/python
# ================================
# (C)2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# EMAG
# modo python
# reveal reference scene of selected meshref in explorer

import os

import modo
import modo.constants as c

from h3d_utilites.scripts.h3d_utils import (
    reveal_in_explorer,
    execution_time_alarm,
)

from h3d_selection_tools.scripts.select_nonzero_meshrefs import is_meshref


@execution_time_alarm('Revealing meshrefs in explorer')
def main():
    selected = modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
    meshrefs = [item for item in selected if is_meshref(item)]

    if not meshrefs:
        print('No meshrefs selected')
        return

    scenepath = modo.Scene().filename
    scenedir = os.path.dirname(scenepath)
    subdir_files = get_subdir_files(scenedir)

    filepaths: set[str] = set()
    for meshref in meshrefs:
        basename = get_meshref_basename(meshref)
        for filepath in subdir_files:
            if os.path.basename(filepath) == f'{basename}.lxo':
                filepaths.add(filepath)

    for filepath in filepaths:
        reveal_in_explorer(filepath)


def get_meshref_basename(meshref: modo.Item) -> str:
    if not is_meshref(meshref):
        return ''

    id = meshref.id
    if not id:
        return ''

    basename = id.split(':')[0]

    return basename


def get_subdir_files(dirpath: str) -> list[str]:
    """Get all files in a directory and its subdirectories.
    In case of duplicates, the earliest occurrence is kept.

    Args:
        dirpath (str): path to the directory to search for files

    Returns:
        list[str]: list of file paths
    """
    filepaths: list[str] = []
    file_mod_times: dict[str, float] = {}
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            filepath = os.path.join(root, file)
            mod_time = os.path.getmtime(filepath)
            if filepath not in file_mod_times or mod_time < file_mod_times[filepath]:
                file_mod_times[filepath] = mod_time

    filepaths = list(file_mod_times.keys())
    return filepaths


if __name__ == '__main__':
    main()
