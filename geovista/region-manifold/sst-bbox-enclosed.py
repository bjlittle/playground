#!/usr/bin/env python3
"""Importable and runnable geovista example."""
from __future__ import annotations

import geovista as gv
from geovista.geodesic import panel
from geovista.pantry import lfric_sst
import geovista.theme  # noqa: F401

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
mesh = mesh.threshold()

bbox = panel("asia")

region = bbox.enclosed(mesh)

# plot the mesh
plotter = gv.GeoPlotter(crs="+proj=eqc")
sargs = {"title": f"{sample.name} / {sample.units}", "shadow": True}
plotter.add_mesh(region, show_edges=True, scalar_bar_args=sargs)
plotter.add_base_layer(texture=gv.natural_earth_1())
plotter.add_coastlines()
plotter.add_axes()
plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere (+proj=eqc)",
    position="upper_left",
    font_size=10,
    shadow=True,
)
plotter.view_xy()
plotter.show()
