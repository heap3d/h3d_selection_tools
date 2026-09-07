#!/usr/bin/python
# ================================
# (C)2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# select 2nd largest polygons 'flat' area in selected mesh
# ================================

import modo
import modo.constants as c
import lx
import uuid

from h3d_utilites.scripts.h3d_utils import get_user_value

import h3d_selection_tools.scripts.h3d_kit_constants as h3dc
from h3d_selection_tools.scripts.geometry_stats_operations import (
    get_polygons_by_2nd_largest_flat_area,
    remove_item_selection_set,
)

from h3d_utilites.scripts.h3d_utils import execution_time_alarm


@execution_time_alarm('Select 2nd Largest Polygons Area')
def main():
    scene = modo.Scene()

    selected_meshes = scene.selectedByType(itype=c.MESH_TYPE)
    set_uuid = str(uuid.uuid4())
    selection_set_name = '{} - {}'.format(h3dc.SELECTION_SET_BASE_NAME, set_uuid)

    matched_polys = []

    ANGLE_THRESHOLD = get_user_value(h3dc.USER_VAL_NAME_COPLANAR_ANGLE)
    for mesh in selected_meshes:
        center_polys = get_polygons_by_2nd_largest_flat_area(mesh, ANGLE_THRESHOLD)
        if not center_polys:
            continue
        matched_polys += center_polys
        lx.eval('select.editSet {{{}}} add item:{}'.format(selection_set_name, mesh.id))

    # select processed meshes
    try:
        lx.eval('!select.useSet "{}" replace'.format(selection_set_name))
        remove_item_selection_set(selection_set_name)
    except RuntimeError:
        print('No meshes were processed.')
        print('Try to update template mesh info')

    lx.eval('select.type polygon')
    lx.eval('select.drop polygon')
    for polygon in matched_polys:
        polygon.select()


if __name__ == '__main__':
    main()
