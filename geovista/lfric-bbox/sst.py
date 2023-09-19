#!/usr/bin/env python3
"""Extract C48 panels and render as cube."""
import sys

import geovista
import geovista.theme

threshold = False
if len(sys.argv) == 2:
    arg = sys.argv[1]
    if arg in ["-t", "--threshold"]:
        threshold = True

mesh = geovista.samples.lfric_sst()

plotter = geovista.GeoPlotter()

kwargs = {
    "lighting": False,
    "show_scalar_bar": False,
    "show_edges": False,
}

if threshold:
    mesh = mesh.threshold()

for name in geovista.geodesic.PANEL_IDX_BY_NAME:
    bbox = geovista.geodesic.panel(name)
    _ = plotter.add_mesh(bbox.boundary(mesh), color="black", line_width=5)

_ = plotter.add_mesh(mesh, **kwargs)

plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere",
    position="upper_left",
    font_size=10,
    shadow=True,
)

plotter.add_axes()
plotter.show()
