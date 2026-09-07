#!/usr/bin/python
# ================================
# (C)2024-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select source of specified instance item
# ================================

import modo

from h3d_selection_tools.scripts.select_item_source import get_instance_source


def main():
    items: list[modo.Item] = modo.Scene().selected
    sources: list[modo.Item] = []
    for item in items:
        source_item = get_instance_source(item)
        if source_item:
            sources.append(source_item)

    if not sources:
        return

    modo.Scene().deselect()
    for item in set(sources):
        if item:
            item.select()


if __name__ == '__main__':
    main()
