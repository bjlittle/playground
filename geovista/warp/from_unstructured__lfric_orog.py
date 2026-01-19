#!/usr/bin/env python3
"""Importable and runnable geovista example."""

from __future__ import annotations

import geovista as gv
from geovista.pantry import lfric_orog
import geovista.theme  # noqa: F401

# load the sample data
sample = lfric_orog()

# create the mesh from the sample data
mesh = gv.Transform.from_unstructured(
    sample.lons,
    sample.lats,
    connectivity=sample.connectivity,
    data=sample.data,
)

# plot the mesh
plotter = gv.GeoPlotter()
sargs = {"title": f"{sample.name} / {sample.units}", "shadow": True}
plotter.add_mesh(mesh, scalar_bar_args=sargs)
plotter.add_axes()
plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere",
    position="upper_left",
    font_size=10,
    shadow=True,
)
plotter.camera.zoom(1.3)
plotter.show()
