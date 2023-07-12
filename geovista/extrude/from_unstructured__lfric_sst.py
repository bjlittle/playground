#!/usr/bin/env python3
"""Importable and runnable geovista example."""
from __future__ import annotations

from pyproj import CRS

import geovista as gv
from geovista.common import cast_UnstructuredGrid_to_PolyData as cast
from geovista.pantry import lfric_sst
import geovista.theme  # noqa: F401
from geovista.transform import transform_mesh

# load the sample data
sample = lfric_sst()

# create the mesh from the sample data
mesh = gv.Transform.from_unstructured(
    sample.lons,
    sample.lats,
    connectivity=sample.connectivity,
    data=sample.data,
)

# remove cells from the mesh with nan values
mesh = cast(mesh.threshold())

crs = CRS.from_user_input("+proj=robin")
mesh = transform_mesh(mesh, crs)


mesh = mesh.extrude((0, 0, -1000000), capping=True)


# plot the mesh
plotter = gv.GeoPlotter(crs=crs)
sargs = {"title": f"{sample.name} / {sample.units}", "shadow": True}
plotter.add_mesh(mesh, show_edges=False, scalar_bar_args=sargs)
plotter.add_coastlines(color="black")
plotter.add_axes()
plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere (proj=robin, 10m Coastlines)",
    position="upper_left",
    font_size=10,
    shadow=True,
)
plotter.show()
