#!/usr/bin/python
# ================================
# (C)2025 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# EMAG
# modo python
# select meshrefs with nonzero transforms

from typing import Iterable

import lx
import modo
import modo.constants as c

from h3d_utilites.scripts.h3d_utils import get_user_value, execution_time_alarm


Transforms = tuple[modo.Vector3, modo.Vector3, modo.Vector3]

USERVAL_NAME_TOLERANCE = 'h3d_mtl_zero_treshold'


def get_meshrefs(items: Iterable) -> list[modo.Item]:
    if not items:
        return []

    return [item for item in items if is_meshref(item)]


def is_meshref(item: modo.Item) -> bool:
    if not item:
        return False

    if not item.id:
        print(f'{item.name=} has no id')
        return False

    return True if ':' in item.id else False


def get_nonzero_items(items: Iterable[modo.Item], tolerance: float) -> list[modo.Item]:
    return [
        item
        for item in items
        if not is_zero_transforms(item, tolerance)
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


@execution_time_alarm()
def main():
    TOLERANCE = get_user_value(USERVAL_NAME_TOLERANCE)

    meshrefs = get_meshrefs(modo.Scene().items(itype=c.LOCATOR_TYPE, superType=True))
    nonzero_meshrefs = get_nonzero_items(meshrefs, TOLERANCE)

    modo.Scene().deselect()
    for item in nonzero_meshrefs:
        item.select()


if __name__ == '__main__':
    main()
