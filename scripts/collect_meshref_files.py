#!/usr/bin/python
# ================================
# (C)2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# EMAG
# modo python
# reveal reference scene of selected meshref in explorer

import os
import shutil

import modo
import modo.constants as c

from h3d_utilites.scripts.h3d_utils import (
    execution_time_alarm,
    reveal_in_explorer,
    get_user_value,
    set_user_value,
    is_defined_user_value,
    def_new_user_value,
)

from h3d_selection_tools.scripts.select_nonzero_meshrefs import is_meshref
from h3d_selection_tools.scripts.reveal_meshref_in_explorer import get_subdir_files, get_meshref_basename


USERVAL_MESHREF_STORE_DIR = 'h3d_cmf_collect_dir'


def main():
    selected = modo.Scene().selectedByType(itype=c.LOCATOR_TYPE, superType=True)
    meshrefs = [item for item in selected if is_meshref(item)]

    if not meshrefs:
        print('No meshrefs selected')
        return

    define_user_values()

    scene_dir = get_scene_root_dir()
    start_dir = get_user_value(USERVAL_MESHREF_STORE_DIR)
    if not start_dir:
        start_dir = scene_dir
    store_dir = get_store_subdir(start_dir)
    if not store_dir:
        return

    process_meshrefs(meshrefs, scene_dir, store_dir)

    set_user_value(USERVAL_MESHREF_STORE_DIR, store_dir)
    reveal_in_explorer(f'{store_dir}\\.')


def define_user_values():
    if not is_defined_user_value(USERVAL_MESHREF_STORE_DIR):
        def_new_user_value(USERVAL_MESHREF_STORE_DIR, 'string', 'temporary')


@execution_time_alarm('Collecting meshrefs')
def process_meshrefs(meshrefs: list[modo.Item], scandir: str, store_dir: str):
    create_subdir_if_not_exists(store_dir)
    subdir_files = get_subdir_files(scandir)

    filepaths: set[str] = set()
    for meshref in meshrefs:
        basename = get_meshref_basename(meshref)
        for filepath in subdir_files:
            if os.path.basename(filepath) == f'{basename}.lxo':
                filepaths.add(filepath)

    for filepath in filepaths:
        copy_file_to_dir(filepath, store_dir)


def get_scene_root_dir() -> str:
    scenepath = modo.Scene().filename

    return os.path.dirname(scenepath)


def get_store_subdir(start_dir: str) -> str:
    COLLECTED_MESHREFS_SUBDIR = '_collected_meshrefs'

    root_dir = get_scene_root_dir()

    store_subdir = modo.dialogs.dirBrowse(title='Select directory to store collected meshrefs', path=start_dir)
    if not store_subdir:
        store_subdir = ''
    if store_subdir == root_dir:
        store_subdir = os.path.join(root_dir, COLLECTED_MESHREFS_SUBDIR)

    return store_subdir


def create_subdir_if_not_exists(folder_path: str):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def copy_file_to_dir(src_file: str, dest_dir: str):
    create_subdir_if_not_exists(dest_dir)
    src_basename = os.path.basename(src_file)
    dest_file = os.path.join(dest_dir, src_basename)
    if os.path.exists(dest_file):
        if os.path.samefile(src_file, dest_file):
            return
        os.remove(dest_file)

    shutil.copy(src_file, dest_dir)


if __name__ == '__main__':
    main()
