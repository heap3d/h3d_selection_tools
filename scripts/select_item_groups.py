#!/usr/bin/python
# ================================
# (C)2024 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# select texture locators
# ================================

import modo


def main():
    selected_items = modo.Scene().selected
    connected_items = set(selected_items)
    for item in selected_items:
        group_items = item.itemGraph('itemGroups').forward()
        if isinstance(group_items, list):
            connected_items.update(group_items)
    octane_overrides = [i for i in connected_items if i.type == 'material.octaneRenderer']
    for item in octane_overrides:
        connected_items.remove(item)

    for item in octane_overrides:
        item.select()
    for item in connected_items:
        item.select()


if __name__ == '__main__':
    main()
