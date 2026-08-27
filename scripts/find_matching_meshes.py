#!/usr/bin/python
# ================================
# (C)2022 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# find a match between template and target meshes
# ================================

import copy
import modo
import modo.constants as c
import lx

from h3d_utilites.scripts.h3d_utils import get_user_value

import h3d_selection_tools.scripts.h3d_kit_constants as h3dc
from h3d_selection_tools.scripts.mesh_islands_to_items import is_mesh_similar, DetectOptions
from h3d_selection_tools.scripts.center_utilites import COLOR_PROCESSED


def place_center_at_polygons(mesh, polys, do_poly_triple):
    if not mesh:
        return
    if not polys:
        return

    parent = mesh.parent
    hierarchy_index = mesh.parentIndex if parent else mesh.rootIndex
    mesh.select(replace=True)
    lx.eval(f'item.editorColor {COLOR_PROCESSED}')

    # select center polygons
    lx.eval('select.type polygon')
    lx.eval('select.drop polygon')
    for poly in polys:
        poly.select()

    # create temporary polygons to correctly determine the center of the selection
    # enable select on paste

    lx.eval('copy')

    lx.eval('paste')

    if do_poly_triple:
        lx.eval('poly.triple')

    lx.eval('workPlane.fitSelect')

    # delete temporary polygons
    lx.eval('delete')

    # create locator and align it to work plane grid
    lx.eval('select.type item')
    tmp_loc = modo.Scene().addItem(itype=c.LOCATOR_TYPE)
    tmp_loc.select(replace=True)
    lx.eval('item.matchWorkplane pos')
    lx.eval('item.matchWorkplane rot')

    # rotate locator 180 degrees around Z axis
    rot_x, rot_y, rot_z = tmp_loc.rotation.get(degrees=True)
    tmp_loc.rotation.set((rot_x, rot_y, rot_z + 180.0), degrees=True)

    # parent mesh to locator in place
    mesh.select(replace=True)
    tmp_loc.select()
    lx.eval('item.parent inPlace:1')

    # freeze transforms to reset center of the selected mesh
    mesh.select(replace=True)
    lx.eval('transform.freeze')

    # unparent in place
    lx.eval(f'item.parent parent:{{}} inPlace:1 position:{hierarchy_index}')

    # restore parenting
    if parent is not None:
        parent.select()
        lx.eval(f'item.parent inPlace:1 position:{hierarchy_index}')

    tmp_loc.select(replace=True)
    lx.eval('item.delete')

    lx.eval('workPlane.reset')


def get_similar_mesh_center_polys(cur_mesh, cmp_mesh, center_polys, do_poly_triple):
    if not cur_mesh:
        return []
    if not center_polys:
        return []
    if cur_mesh.name == cmp_mesh.name:
        return [cur_mesh.geometry.polygons[get_user_value(h3dc.USER_VAL_NAME_CENTER_IDX)]]
    for poly in center_polys:
        # duplicate mesh
        test_mesh = modo.Scene().duplicateItem(cur_mesh)
        test_mesh.name = '{} [{}]'.format(cur_mesh.name, poly.index)  # type: ignore

        # select poly
        lx.eval('select.type polygon')
        lx.eval('select.drop polygon')
        test_polys = [(test_mesh.geometry.polygons[poly.index])]  # type: ignore

        # set center to selected poly
        place_center_at_polygons(test_mesh, test_polys, do_poly_triple)

        # test if duplicated mesh similar to template mesh
        if is_mesh_similar(test_mesh, cmp_mesh, detect_options):
            modo.Scene().removeItems(test_mesh)
            return [poly]
        modo.Scene().removeItems(test_mesh)
    return []


def get_similar_mesh_center_polys_Y_axis(cur_mesh, cmp_mesh, center_polys, do_poly_triple):
    if not cur_mesh:
        return []
    if not center_polys:
        return []
    if cur_mesh.name == cmp_mesh.name:
        return [cur_mesh.geometry.polygons[get_user_value(h3dc.USER_VAL_NAME_CENTER_IDX)]]
    for poly in center_polys:
        # duplicate mesh
        test_mesh = modo.Scene().duplicateItem(cur_mesh)
        test_mesh.name = '{} [{}]'.format(cur_mesh.name, poly.index)  # type: ignore

        # select poly
        lx.eval('select.type polygon')
        lx.eval('select.drop polygon')
        test_polys = [(test_mesh.geometry.polygons[poly.index])]  # type: ignore

        # set center to selected poly
        place_center_at_polygons(test_mesh, test_polys, do_poly_triple)

        # modify detect options to using Y axis only
        modified_detect_options = copy.copy(detect_options)
        modified_detect_options.do_bounding_box.x = False
        modified_detect_options.do_bounding_box.z = False
        modified_detect_options.do_center_pos.x = False
        modified_detect_options.do_center_pos.z = False
        modified_detect_options.do_com_pos.x = False
        modified_detect_options.do_com_pos.z = False

        # test if duplicated mesh similar to template mesh
        if is_mesh_similar(test_mesh, cmp_mesh, modified_detect_options):
            modo.Scene().removeItems(test_mesh)
            return [poly]
        modo.Scene().removeItems(test_mesh)
    return []


do_bb = modo.mathutils.Vector3()
do_bb.x = get_user_value(h3dc.USER_VAL_NAME_DO_BOUNDING_BOX_X)
do_bb.y = get_user_value(h3dc.USER_VAL_NAME_DO_BOUNDING_BOX_Y)
do_bb.z = get_user_value(h3dc.USER_VAL_NAME_DO_BOUNDING_BOX_Z)
bb_thld = modo.mathutils.Vector3()
bb_thld.x = get_user_value(h3dc.USER_VAL_NAME_BB_THRESHOLD_X)
bb_thld.y = get_user_value(h3dc.USER_VAL_NAME_BB_THRESHOLD_Y)
bb_thld.z = get_user_value(h3dc.USER_VAL_NAME_BB_THRESHOLD_Z)

do_ctr = modo.mathutils.Vector3()
do_ctr.x = get_user_value(h3dc.USER_VAL_NAME_DO_CENTER_POS_X)
do_ctr.y = get_user_value(h3dc.USER_VAL_NAME_DO_CENTER_POS_Y)
do_ctr.z = get_user_value(h3dc.USER_VAL_NAME_DO_CENTER_POS_Z)
ctr_thld = modo.mathutils.Vector3()
ctr_thld.x = get_user_value(h3dc.USER_VAL_NAME_CENTER_THRESHOLD_X)
ctr_thld.y = get_user_value(h3dc.USER_VAL_NAME_CENTER_THRESHOLD_Y)
ctr_thld.z = get_user_value(h3dc.USER_VAL_NAME_CENTER_THRESHOLD_Z)

do_com = modo.mathutils.Vector3()
do_com.x = get_user_value(h3dc.USER_VAL_NAME_DO_COM_POS_X)
do_com.y = get_user_value(h3dc.USER_VAL_NAME_DO_COM_POS_Y)
do_com.z = get_user_value(h3dc.USER_VAL_NAME_DO_COM_POS_Z)
com_thld = modo.mathutils.Vector3()
com_thld.x = get_user_value(h3dc.USER_VAL_NAME_COM_THRESHOLD_X)
com_thld.y = get_user_value(h3dc.USER_VAL_NAME_COM_THRESHOLD_Y)
com_thld.z = get_user_value(h3dc.USER_VAL_NAME_COM_THRESHOLD_Z)

do_vol = get_user_value(h3dc.USER_VAL_NAME_DO_MESH_VOL)
vol_thld = get_user_value(h3dc.USER_VAL_NAME_VOL_THRESHOLD)

detect_options = DetectOptions(do_bounding_box=do_bb,
                               do_center_pos=do_ctr,
                               do_com_pos=do_com,
                               do_mesh_vol=do_vol,
                               bb_threshold=bb_thld,
                               center_threshold=ctr_thld,
                               com_threshold=com_thld,
                               vol_threshold=vol_thld)
