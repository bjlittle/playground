#!/usr/bin/env python3
"""Importable and runnable geovista example."""

from __future__ import annotations

from pyproj import CRS

import geovista as gv
from geovista.pantry import lfric_orog
import geovista.theme  # noqa: F401
from geovista.transform import transform_mesh

# load the sample data
sample = lfric_orog()

# create the mesh from the sample data
mesh = gv.Transform.from_unstructured(
    sample.lons,
    sample.lats,
    connectivity=sample.connectivity,
    data=sample.data,
    name=sample.name,
)

crs = CRS.from_user_input("+proj=eqc")
mesh = transform_mesh(mesh, crs)

# warp the mesh nodes by the surface altitude
mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True)
mesh.warp_by_scalar(scalars=sample.name, inplace=True, factor=200)

# plot the mesh
plotter = gv.GeoPlotter(crs=crs)
sargs = {"title": f"{sample.name} / {sample.units}", "shadow": True}
plotter.add_mesh(mesh, show_edges=False, scalar_bar_args=sargs)
plotter.add_axes()
plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere",
    position="upper_left",
    font_size=10,
    shadow=True,
)
plotter.camera.position = (41765188.91567403, -19595227.412923645, 20684232.927517064)
plotter.show()
# print(plotter.camera.position)
