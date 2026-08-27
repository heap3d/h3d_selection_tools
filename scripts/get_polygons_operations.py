#!/usr/bin/python
# ================================
# (C)2022-2026 Dmytro Holub
# heap3d@gmail.com
# --------------------------------
# modo python
# EMAG
# get_polygons_xxx() operations
# ================================

from typing import Iterable

import modo
import lx
import modo.constants as c
from modo.mathutils import math

from h3d_utilites.scripts.h3d_utils import (
    get_full_mesh_area,
    select_polygons,
    set_selection_mode,
    SELECTION_MODE,
    remove_if_exist,
    drop_selection,
    parent_items_to,
    )

import h3d_selection_tools.scripts.h3d_kit_constants as h3dc
from h3d_selection_tools.scripts.center_utilites import create_loc_at_selection


def remove_item_selection_set(name: str) -> None:
    lx.eval(f'select.pickWorkingSet "{name}"')
    lx.eval('select.deleteWorkingSet')


def get_margin_low(percentage, threshold):
    margin_low = percentage - threshold / 2.0
    if margin_low < 0.0:
        margin_low = 0.0
    return margin_low


def get_margin_high(percentage, threshold):
    margin_high = percentage + threshold / 2.0
    if margin_high > 1.0:
        margin_high = 1.0
    return margin_high


def get_polygons_find_by_percentage(mesh, percentage, threshold):
    if percentage <= 0.0:
        return []
    if threshold < 0.0:
        return []

    margin_low = get_margin_low(percentage, threshold)
    margin_high = get_margin_high(percentage, threshold)
    polys = get_polygons_find_by_margins(mesh, threshold, margin_low, margin_high, do_multipoly=True)
    return polys


def get_polygons_find_by_largest(mesh):
    """ return matched polygon or [] if none
    """
    if not mesh:
        return []
    polys = get_polygons_find_by_margins(mesh=mesh, percentage=1.0, margin_low=0.0, margin_high=1.0)
    return polys


def get_polygons_find_by_margins(mesh, percentage, margin_low, margin_high, do_multipoly=False):
    if not mesh:
        return []
    min_difference = 1
    polys = []
    full_area = get_full_mesh_area(mesh)
    for polygon in mesh.geometry.polygons:
        poly_percentage = polygon.area / full_area
        if margin_low < poly_percentage < margin_high:
            if do_multipoly:
                polys.append(polygon)
            else:
                difference = abs(percentage - poly_percentage)
                if difference < min_difference:
                    min_difference = difference
                    polys = [polygon]
    return polys


def get_polygons_find_by_selected(mesh, selected_polys):
    if not mesh:
        return []
    if not selected_polys:
        print('<{}>: No polygons selected'.format(mesh.name))
        return []
    return selected_polys


def get_polygons_most_vertex_count(mesh):
    if not mesh:
        return []
    polygons = sorted(mesh.geometry.polygons, key=lambda poly: poly.numVertices, reverse=True)
    if not polygons:
        return []
    max_vertexcount = polygons[0].numVertices
    polys = []
    for polygon in polygons:
        if polygon.numVertices != max_vertexcount:
            break
        polys.append(polygon)
    return polys


def get_polygons_by_flat_area(mesh: modo.Mesh, angle: float) -> tuple[tuple[tuple[modo.MeshPolygon, ...], float], ...]:
    if not mesh:
        raise ValueError('Invalid mesh provided')

    geometry = mesh.geometry
    if not geometry:
        raise ValueError('Mesh has no geometry')

    geo_polygons = geometry.polygons
    if not geo_polygons:
        return ()

    polygons_area: dict[tuple[modo.MeshPolygon, ...], float] = dict()

    polygons = set(geo_polygons)
    processed = set()

    while polygons:
        polygon = polygons.pop()
        connected_polygons = get_connected_polygons_by_angle(polygon, angle, exclude=processed)

        connected_polygons.append(polygon)
        processed.update(connected_polygons)

        polygons.difference_update(processed)

        polygons_area[tuple(connected_polygons)] = sum(p.area for p in connected_polygons)

    sorted_polygons_area = sorted(polygons_area.items(), key=lambda item: item[1], reverse=True)

    return tuple(sorted_polygons_area)


def get_polygons_by_largest_flat_area(mesh: modo.Mesh, angle: float) -> tuple[modo.MeshPolygon, ...]:
    sorted_polygons_flat_area = get_polygons_by_flat_area(mesh, angle)
    if sorted_polygons_flat_area:
        return sorted_polygons_flat_area[0][0]

    return ()


def get_angle(poly1: modo.MeshPolygon, poly2: modo.MeshPolygon) -> float:
    """ return angle in degrees between two polygons
    """
    if not poly1 or not poly2:
        raise ValueError('Invalid polygon(s) provided')

    normal1 = modo.Vector3(poly1.normal).normal()
    normal2 = modo.Vector3(poly2.normal).normal()

    try:
        angle = math.degrees(normal1.angle(normal2))
    except ValueError:
        angle = 90.0

    return angle


def get_nearest_polygons_by_angle(polygon: modo.MeshPolygon, angle: float, exclude: Iterable[modo.MeshPolygon]) -> list[modo.MeshPolygon]:
    valid_polygons: list[modo.MeshPolygon] = []
    polygons = set(polygon.neighbours) - set(exclude)

    for neighbour in polygons:
        if get_angle(polygon, neighbour) <= angle:
            valid_polygons.append(neighbour)

    return valid_polygons


def get_connected_polygons_by_angle(polygon: modo.MeshPolygon, angle: float, exclude: Iterable[modo.MeshPolygon]) -> list[modo.MeshPolygon]:
    valid_polygons: set[modo.MeshPolygon] = set()

    processed: set[modo.MeshPolygon] = set()
    processed.update(exclude)

    polygons: set[modo.MeshPolygon] = set([polygon,])
    while polygons:
        current_polygon = polygons.pop()
        nearest_polygons = get_nearest_polygons_by_angle(current_polygon, angle, exclude=processed)

        valid_polygons.update(nearest_polygons)
        polygons.update(nearest_polygons)
        processed.add(current_polygon)

    return list(valid_polygons)


def get_polygons_by_middle_flat_area(mesh: modo.Mesh, angle: float) -> tuple[modo.MeshPolygon, ...]:
    LOC_NAME = 'Flat Area loc'
    BB_LOC_NAME = 'BB loc'

    sorted_polygons_flat_area = get_polygons_by_flat_area(mesh, angle)
    if not sorted_polygons_flat_area:
        return ()

    drop_selection(SELECTION_MODE.POLYGON.value)
    set_selection_mode(SELECTION_MODE.POLYGON.value)
    geometry = mesh.geometry
    if not geometry:
        return ()
    geo_polygons = geometry.polygons
    if not geo_polygons:
        return ()
    select_polygons(list(geo_polygons))

    bb_loc = create_loc_at_selection(mesh, SELECTION_MODE.POLYGON.value, name=BB_LOC_NAME)

    middle_flat_area_polygons = sorted_polygons_flat_area[0][0]
    set_selection_mode(SELECTION_MODE.POLYGON.value)
    select_polygons(middle_flat_area_polygons)
    flat_area_loc = create_loc_at_selection(mesh, SELECTION_MODE.POLYGON.value, name=LOC_NAME)

    bb_pos = modo.Vector3(bb_loc.position.get())
    flat_area_pos = modo.Vector3(flat_area_loc.position.get())
    min_bb_offset = bb_pos.distanceBetweenPoints(flat_area_pos)

    largest_flat_area_normal = get_normal_vector(flat_area_loc, mesh).normal()

    remove_if_exist(flat_area_loc, True)
    remove_if_exist(bb_loc, True)

    for flat_area_polygons in sorted_polygons_flat_area[1:]:
        polygons = flat_area_polygons[0]
        if len(polygons) < 2:
            continue

        polygon_normal = modo.Vector3(polygons[0].normal).normal()
        cross_res = largest_flat_area_normal.cross(polygon_normal)

        diff_angle = math.degrees(math.asin(cross_res.length()))
        if diff_angle > angle:
            continue


        set_selection_mode(SELECTION_MODE.POLYGON.value)
        select_polygons(polygons)
        flat_area_loc = create_loc_at_selection(mesh, SELECTION_MODE.POLYGON.value, name=LOC_NAME)
        flat_area_pos = modo.Vector3(flat_area_loc.position.get())

        bb_offset = bb_pos.distanceBetweenPoints(flat_area_pos)
        if bb_offset < min_bb_offset:
            min_bb_offset = bb_offset
            middle_flat_area_polygons = polygons[:]

        remove_if_exist(flat_area_loc, True)

    return middle_flat_area_polygons


def create_plane() -> modo.Item:
    lx.eval('layer.new')
    lx.eval('@MakePlane.py')
    plane = modo.Scene().selectedByType(itype=c.MESH_TYPE)[0]

    return plane


def get_normal_vector(item: modo.Item, zero_item: modo.Item) -> modo.Vector3:
    plane = create_plane()
    parent_items_to((plane,), item, inplace=False)
    parent_items_to((plane,), zero_item, inplace=True)

    plane.select(replace=True)
    lx.eval('transform.freeze rotation')

    geometry = plane.geometry
    if not geometry:
        raise ValueError('Plane item has no geometry.')
    polygons = geometry.polygons
    if not polygons:
        raise ValueError('Plane item has no polygons')

    normal = polygons[0].normal

    remove_if_exist(plane, True)

    return modo.Vector3(normal).normal()


def get_polygons_by_2nd_largest_flat_area(mesh: modo.Mesh, angle: float) -> tuple[modo.MeshPolygon, ...]:
    sorted_polygons_flat_area = get_polygons_by_flat_area(mesh, angle)
    if not sorted_polygons_flat_area:
        return ()

    middle_flat_area_polygons = sorted_polygons_flat_area[0][0]

    largest_flat_area_normal = modo.Vector3(middle_flat_area_polygons[0].normal).normal()

    for flat_area_polygons in sorted_polygons_flat_area[1:]:
        polygons = flat_area_polygons[0]
        if len(polygons) < 2:
            continue

        polygon_normal = modo.Vector3(polygons[0].normal).normal()
        cross_res = largest_flat_area_normal.cross(polygon_normal)

        diff_angle = math.degrees(math.asin(cross_res.length()))
        if diff_angle < angle:
            middle_flat_area_polygons = polygons[:]
            break


    return middle_flat_area_polygons
