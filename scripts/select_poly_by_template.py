#!/usr/bin/python
# ================================
# (C)2022-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# select polygons for selected meshes by matching to template
# ================================

import modo
import modo.constants as c
import lx
import uuid

import h3d_selection_tools.scripts.h3d_kit_constants as h3dc
from h3d_selection_tools.scripts.find_matching_meshes import get_similar_mesh_center_polys
from h3d_selection_tools.scripts.geometry_stats_operations import (
    get_polygons_find_by_percentage,
    remove_item_selection_set,
)

from h3d_utilites.scripts.h3d_utils import execution_time_alarm, get_user_value


@execution_time_alarm('Select Polygons by Template')
def main():
    scene = modo.Scene()
    # get user values from UI
    area_percentage = get_user_value(h3dc.USER_VAL_NAME_CENTER_AREA_PERC)
    area_threshold = get_user_value(h3dc.USER_VAL_NAME_AREA_THRESHOLD)
    do_poly_triple = get_user_value(h3dc.USER_VAL_NAME_POLY_TRIPLE)

    selected_meshes = scene.selectedByType(itype=c.MESH_TYPE)
    set_uuid = str(uuid.uuid4())
    selection_set_name = '{} - {}'.format(h3dc.SELECTION_SET_BASE_NAME, set_uuid)
    matched_polys = []

    for mesh in selected_meshes:
        item_name = get_user_value(h3dc.USER_VAL_NAME_TEMPLATE_MESH)
        try:
            cmp_mesh = scene.item(item_name)
        except LookupError:
            print(f'Template mesh <{item_name}> not found.')
            return
        poly_candidates = get_polygons_find_by_percentage(mesh, area_percentage, area_threshold)

        # get polygons for full detect options list
        center_polys = get_similar_mesh_center_polys(mesh, cmp_mesh, poly_candidates, do_poly_triple)

        # skip if mesh doesn't matches to template (returned index is -1)
        if not center_polys:
            continue
        # add matched polygons to collection
        matched_polys += center_polys
        # enter item mode and add matched mesh to selection set
        lx.eval('select.type item')
        lx.eval('select.editSet {{{}}} add item:{}'.format(selection_set_name, mesh.id))

    # select processed meshes
    try:
        lx.eval('!select.useSet "{}" replace'.format(selection_set_name))
        remove_item_selection_set(selection_set_name)
    except RuntimeError:
        print('No meshes were processed.')
        print('Try to update template mesh info')
    # select matched polygons
    lx.eval('select.type polygon')
    lx.eval('select.drop polygon')
    for polygon in matched_polys:
        polygon.select()

    print('done.')


if __name__ == '__main__':
    main()
