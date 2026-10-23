#!/usr/bin/python
# ================================
# (C)2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# select one level deeper children for selected items
# ================================

import modo


def main():
    scene = modo.Scene()
    items = scene.selected
    modo.Scene().deselect()
    for item in items:
        if item.children():
            for child in item.children():
                child.select()


if __name__ == '__main__':
    main()
