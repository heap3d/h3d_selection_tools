#!/usr/bin/python
# ================================
# (C)2024-2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select item source
# ================================

from typing import Optional

import modo


def main():
    selected = modo.Scene().selected

    source_items: list[modo.Item] = []
    for item in selected:
        source = get_instance_source(item)
        if source:
            source_items.append(source)
        sources = get_replicator_prototypes(item)
        source_items.extend(sources)

    if not source_items:
        return

    modo.Scene().deselect()
    for item in source_items:
        item.select()


def get_instance_source(instance: modo.Item) -> Optional[modo.Item]:
    source_forward = instance.itemGraph('source').forward()

    if not (isinstance(source_forward, list)):
        return source_forward

    if not source_forward:
        return None

    return source_forward[0]


def get_replicator_prototypes(replicator: modo.Item) -> list[modo.Item]:
    forward_items = replicator.itemGraph('particle').forward()
    if not isinstance(forward_items, list):
        raise TypeError("Expected a list of items from itemGraph")

    prototypes = [
        item
        for item in forward_items
        if (item.type != 'replicator' or replicator.type == 'replicator')
    ]

    return prototypes


def get_replicator_point_source(replicator: modo.Item) -> Optional[modo.Item]:
    reverse_items = replicator.itemGraph('particle').reverse()

    if not isinstance(reverse_items, list):
        return reverse_items

    if not reverse_items:
        return None

    source_item = reverse_items[0]
    if (source_item.type == 'replicator' and replicator.type != 'replicator'):
        return None

    return source_item


if __name__ == '__main__':
    main()
