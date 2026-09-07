#!/usr/bin/python
# ================================
# (C)2024-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select instances of specified item
# ================================

import modo

from h3d_selection_tools.scripts.select_items_used import get_instances


def main():
    selected = modo.Scene().selected

    items_used: list[modo.Item] = []
    for item in selected:
        items_used.extend(get_instances(item))

    if not items_used:
        return

    modo.Scene().deselect()
    for item in items_used:
        item.select()


if __name__ == '__main__':
    main()
