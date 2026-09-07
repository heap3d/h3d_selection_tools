#!/usr/bin/python
# ================================
# (C)2025-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# EMAG
# modo python
# select items with zero transforms

from typing import Iterable

import modo
import modo.constants as c

from h3d_selection_tools.scripts.select_nonzero_transform_items import is_zero_transforms, TOLERANCE


def main():
    items = get_zero_items(modo.Scene().items(c.LOCATOR_TYPE, superType=True))

    modo.Scene().deselect()
    for item in items:
        item.select()


def get_zero_items(items: Iterable[modo.Item]) -> list[modo.Item]:
    return [
        item
        for item in items
        if is_zero_transforms(item, TOLERANCE)
    ]


if __name__ == '__main__':
    main()
