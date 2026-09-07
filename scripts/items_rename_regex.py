#!/usr/bin/python
# ================================
# (C)2025-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# renames selected items using regex pattern

import modo
import re

from h3d_utilites.scripts.h3d_utils import get_user_value


USERVAL_PATTERN = 'h3d_irr_pattern'
USERVAL_REPLACEMENT = 'h3d_irr_replacement'


def main():
    pattern = get_user_value(USERVAL_PATTERN)
    if not pattern:
        return
    replace_str = get_user_value(USERVAL_REPLACEMENT)
    items = modo.Scene().selected
    for item in items:
        name = item.name
        if not name:
            continue
        new_name = re.sub(pattern, replace_str, name)
        item.name = new_name


if __name__ == '__main__':
    main()
