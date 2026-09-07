#!/usr/bin/python
# ================================
# (C)2025-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# EMAG
# modo python
# select items with nonzero transforms

from typing import Iterable

import lx
import modo
import modo.constants as c

from h3d_utilites.scripts.h3d_utils import get_user_value


USERVAL_NAME_TOLERANCE = 'h3d_mhs_tolerance'
TOLERANCE = get_user_value(USERVAL_NAME_TOLERANCE)

Transforms = tuple[modo.Vector3, modo.Vector3, modo.Vector3]


def main():
    items = get_nonzero_items(modo.Scene().items(itype=c.LOCATOR_TYPE, superType=True))

    modo.Scene().deselect()
    for item in items:
        item.select()


def get_nonzero_items(items: Iterable[modo.Item]) -> list[modo.Item]:
    return [
        item
        for item in items
        if not is_zero_transforms(item, TOLERANCE)
    ]


def is_zero_transforms(item: modo.Item, tolerance: float) -> bool:
    pos, rot, scl = get_transforms(item)

    if not pos.equals(modo.Vector3(), tolerance):
        return False

    if not rot.equals(modo.Vector3(), tolerance):
        return False

    return scl.equals(modo.Vector3(1, 1, 1), tolerance)


def get_transforms(item: modo.Item) -> Transforms:
    pos = modo.Vector3()
    pos.x = lx.eval(f'transform.channel pos.X ? item:{{{item.id}}}')
    pos.y = lx.eval(f'transform.channel pos.Y ? item:{{{item.id}}}')
    pos.z = lx.eval(f'transform.channel pos.Z ? item:{{{item.id}}}')
    rot = modo.Vector3()
    rot.x = lx.eval(f'transform.channel rot.X ? item:{{{item.id}}}')
    rot.y = lx.eval(f'transform.channel rot.Y ? item:{{{item.id}}}')
    rot.z = lx.eval(f'transform.channel rot.Z ? item:{{{item.id}}}')
    scl = modo.Vector3()
    scl.x = lx.eval(f'transform.channel scl.X ? item:{{{item.id}}}')
    scl.y = lx.eval(f'transform.channel scl.Y ? item:{{{item.id}}}')
    scl.z = lx.eval(f'transform.channel scl.Z ? item:{{{item.id}}}')

    return (pos, rot, scl)


if __name__ == '__main__':
    main()
