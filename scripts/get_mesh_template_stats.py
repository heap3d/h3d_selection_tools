#!/usr/bin/python
# ================================
# (C)2022-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# get template statistics from selected mesh
# ================================

import modo
import modo.constants as c
import lx

from h3d_utilites.scripts.h3d_utils import set_user_value, get_full_mesh_area

import h3d_selection_tools.scripts.h3d_kit_constants as h3dc


def get_selected_mesh():
    selected = modo.Scene().selectedByType(itype=c.MESH_TYPE)
    return selected[:1]


def main():
    selected_mesh = get_selected_mesh()
    for test_mesh in selected_mesh[:1]:
        set_user_value(h3dc.USER_VAL_NAME_TEMPLATE_MESH, test_mesh.name)
        selected_polys = test_mesh.geometry.polygons.selected

        if not selected_polys:
            print('mesh:<{}>  has no selected polygons'.format(test_mesh.name))
            continue

        center_poly = selected_polys[0]
        set_user_value(h3dc.USER_VAL_NAME_CENTER_IDX, center_poly.index)
        full_area = get_full_mesh_area(test_mesh)
        percentage = center_poly.area / full_area
        set_user_value(h3dc.USER_VAL_NAME_CENTER_AREA_PERC, percentage)
        lx.eval('@{scripts/set_center_by_selected_polys.py}')


if __name__ == '__main__':
    main()
