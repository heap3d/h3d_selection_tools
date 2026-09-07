#!/usr/bin/python
# ================================
# (C)2024-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select prototype for specified replicator item
# ================================

import modo

from h3d_selection_tools.scripts.select_item_source import get_replicator_prototypes


def main():
    items: list[modo.Item] = modo.Scene().selected
    sources: set[modo.Item] = set()
    for item in items:
        sources.update(get_replicator_prototypes(item))

    if not sources:
        return

    modo.Scene().deselect()
    for item in sources:
        item.select()


if __name__ == '__main__':
    main()
