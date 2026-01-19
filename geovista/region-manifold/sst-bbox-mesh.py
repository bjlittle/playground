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

# plot the mesh
plotter = gv.GeoPlotter()
sargs = {"title": f"{sample.name} / {sample.units}", "shadow": True}
opacity = 0.3
plotter.add_mesh(mesh, show_edges=False, scalar_bar_args=sargs, opacity=opacity)
# plotter.add_base_layer(texture=gv.natural_earth_1(), opacity=opacity)
plotter.add_mesh(bbox.boundary(), color="orange", line_width=5)
plotter.add_mesh(bbox.mesh, opacity=1.0)
plotter.add_coastlines("50m", color="black")
plotter.add_axes()
plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere (10m Coastlines)",
    position="upper_left",
    font_size=10,
    shadow=True,
)
plotter.view_xz(negative=True)
plotter.show()
