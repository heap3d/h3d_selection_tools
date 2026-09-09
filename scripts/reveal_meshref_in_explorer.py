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

from h3d_utilites.scripts.h3d_utils import reveal_in_explorer

from h3d_selection_tools.scripts.select_nonzero_meshrefs import is_meshref


def get_meshref_basename(meshref: modo.Item) -> str:
    if not is_meshref(meshref):
        return ''

    id = meshref.id
    if not id:
        return ''

    basename = id.split(':')[0]

    return basename


def get_subdir_files(dirpath: str) -> list[str]:
    filepaths: list[str] = []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            filepaths.append(os.path.join(root, file))

    return filepaths


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


if __name__ == '__main__':
    main()
