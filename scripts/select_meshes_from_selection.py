#!/usr/bin/python
# ================================
# (C)2024-2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# select mesh items from selected
# ================================

import modo
from typing import Iterable

from h3d_utilites.scripts.h3d_utils import is_visible


def main():
    items = modo.Scene().selected

    to_select = get_meshes_from(items)

    modo.Scene().deselect()
    for item in to_select:
        item.select()


def get_meshes_from(items: Iterable[modo.Item]) -> list[modo.Item]:
    filtered_items = [i for i in items if i.type == 'mesh']
    filtered_items = [i for i in filtered_items if ':' not in i.id]
    filtered_items = [i for i in filtered_items if is_visible(i)]
    filtered_items = [i for i in filtered_items if i.geometry.polygons]
    return filtered_items


if __name__ == '__main__':
    main()
