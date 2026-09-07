#!/usr/bin/python
# ================================
# (C)2024 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select item usage
# ================================

import modo


def main():
    selected = modo.Scene().selected

    used_items: list[modo.Item] = []
    for item in selected:
        used_items.extend(get_instances(item))
        used_items.extend(get_replicators(item))

    if not used_items:
        return

    modo.Scene().deselect()
    for item in used_items:
        item.select()


def get_instances(item: modo.Item) -> list[modo.Item]:
    item_graph_items = item.itemGraph('source').reverse()

    if not isinstance(item_graph_items, list):
        raise TypeError("Expected a list of items from itemGraph")

    return item_graph_items


def get_replicators(item: modo.Item) -> list[modo.Item]:
    used_items: list[modo.Item] = []

    reverse_items = item.itemGraph('particle').reverse()

    if not isinstance(reverse_items, list):
        raise TypeError("Expected a list of items from itemGraph")

    forward_items = item.itemGraph('particle').forward()
    if not isinstance(forward_items, list):
        raise TypeError("Expected a list of items from itemGraph")

    used_items.extend(reverse_items)
    used_items.extend(forward_items)

    return used_items


if __name__ == '__main__':
    main()
