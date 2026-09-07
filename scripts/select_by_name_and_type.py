#!/usr/bin/python
# ================================
# (C)2019-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select items by type and search string in the name
# ================================

import modo
import lx

import h3d_utilites.scripts.h3d_utils as h3du


USERVAL_NAME_SEARCH_TYPE = 'h3d_sbnt_search_type'
USERVAL_NAME_SEARCH_STR = 'h3d_sbnt_search_str'


def select_items(from_items, search_str='', itype=None):
    for item in from_items:
        if item.type != itype and itype is not None:
            continue
        if search_str.lower() not in item.name.lower():
            continue

        item.select()


def main():
    USERVAL_VAL_SEARCH_TYPE = h3du.get_user_value(USERVAL_NAME_SEARCH_TYPE)
    SEARCH_TYPE = None if USERVAL_VAL_SEARCH_TYPE == '' else USERVAL_VAL_SEARCH_TYPE
    SEARCH_STR = h3du.get_user_value(USERVAL_NAME_SEARCH_STR)

    args = lx.args()
    if not args or not isinstance(args, tuple):
        items = modo.Scene().items(itype=SEARCH_TYPE)
    elif args[0] == 'selected':
        items = modo.Scene().selected
    else:
        items = modo.Scene().items(itype=SEARCH_TYPE)

    modo.Scene().deselect()
    select_items(from_items=items, search_str=SEARCH_STR, itype=SEARCH_TYPE)


if __name__ == '__main__':
    main()
