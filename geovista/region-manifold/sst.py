#!/usr/bin/env python3
"""Importable and runnable geovista example."""

from __future__ import annotations

import geovista as gv
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

# plot the mesh
plotter = gv.GeoPlotter()

plotter.camera.position = (
    -0.007183810134534151,
    4.696847770301366,
    -0.11131701285363166,
)

sargs = {"title": f"{sample.name} / {sample.units}", "shadow": True}
plotter.add_mesh(mesh, show_edges=True, scalar_bar_args=sargs)
plotter.add_base_layer(texture=gv.natural_earth_1())
plotter.add_coastlines()
plotter.add_axes()
plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere (10m Coastlines)",
    position="upper_left",
    font_size=10,
    shadow=True,
)
plotter.show()
