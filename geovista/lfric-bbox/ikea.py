"""Extract C48 panels and render as flat-pack."""
import sys

import numpy as np
import pyvista as pv

import geovista
from geovista.common import cast_UnstructuredGrid_to_PolyData as cast
import geovista.theme


def africa_panel():
    """Extract the africa cube-sphere panel and flatten."""
    bbox = geovista.geodesic.panel("africa")
    panel = bbox.enclosed(mesh)
    N = np.sqrt(panel.n_points)
    sample = np.linspace(-1, 1, num=int(N))
    xs = np.tile(sample, (49, 1))
    ys = xs[:, ::-1].T

    xa = xs[:-1, :-1].ravel()
    xb = xs[:, -1]
    xc = xs[-1, :-1][::-1]

    ya = ys[:-1, :-1].ravel()
    yb = ys[:, -1]
    yc = ys[-1, :-1][::-1]

    xs = np.concatenate([xa, xb, xc])
    ys = np.concatenate([ya, yb, yc])

    panel.points[:, 0] = 1
    panel.points[:, 1] = xs
    panel.points[:, 2] = ys

    return panel


def asia_panel():
    """Extract the asia cube-sphere panel and flatten."""
    bbox = geovista.geodesic.panel("asia")
    panel = bbox.enclosed(mesh)
    N = np.sqrt(panel.n_points)
    sample = np.linspace(-1, 1, num=int(N))
    xs = np.tile(sample[::-1], (49, 1))
    ys = xs.T

    xa = xs[:-1, :-1].ravel()
    xb = xs[:-1, -1]
    xc = xs[-1, :]

    ya = ys[:-1, :-1].ravel()
    yb = ys[:-1, -1]
    yc = ys[-1, :]

    xs = np.concatenate([xa, xb, xc])
    ys = np.concatenate([ya, yb, yc])

    panel.points[:, 0] = xs
    panel.points[:, 1] = 1
    panel.points[:, 2] = ys

    return panel


def pacific_panel():
    """Extract the pacific cube-sphere panel and flatten."""
    bbox = geovista.geodesic.panel("pacific")
    panel = bbox.enclosed(mesh)
    N = np.sqrt(panel.n_points)
    sample = np.linspace(-1, 1, num=int(N))
    xs = np.tile(sample[::-1], (49, 1))
    ys = xs.T

    xa = xs[:-1, :-1].ravel()
    xb = xs[:-1, -1]
    xc = xs[-1, :]

    ya = ys[:-1, :-1].ravel()
    yb = ys[:-1, -1]
    yc = ys[-1, :]

    xs = np.concatenate([xa, xb, xc])
    ys = np.concatenate([ya, yb, yc])

    panel.points[:, 0] = -1
    panel.points[:, 1] = xs
    panel.points[:, 2] = ys

    return panel


def americas_panel():
    """Extract the americas cube-sphere panel and flatten."""
    bbox = geovista.geodesic.panel("americas")
    panel = bbox.enclosed(mesh)
    N = np.sqrt(panel.n_points)
    sample = np.linspace(-1, 1, num=int(N))
    xs = np.tile(sample, (49, 1))
    ys = xs[:, ::-1].T

    xa = xs[:-1, -1]
    xb = xs[:-1, :-1].ravel()
    xc = xs[-1, :][::-1]

    ya = ys[:-1, -1]
    yb = ys[:-1, :-1].ravel()
    yc = ys[-1, :][::-1]

    xs = np.concatenate([xa, xb, xc])
    ys = np.concatenate([ya, yb, yc])

    panel.points[:, 0] = xs
    panel.points[:, 1] = -1
    panel.points[:, 2] = ys

    return panel


def arctic_panel():
    """Extract the arctic cube-sphere panel and flatten."""
    bbox = geovista.geodesic.panel("arctic")
    panel = bbox.enclosed(mesh)
    N = np.sqrt(panel.n_points)
    sample = np.linspace(-1, 1, num=int(N))
    xs = np.tile(sample, (49, 1))
    ys = xs.T

    xa = xs[-1, :]
    xb = xs[:-1, -1][::-1]
    xc = xs[0, :-1][::-1]
    xd = xs[1:-1, 0]
    xe = xs[1:-1, 1:-1].T[:, ::-1].ravel()

    ya = ys[-1, :]
    yb = ys[:-1, -1][::-1]
    yc = ys[0, :-1][::-1]
    yd = ys[1:-1, 0]
    ye = ys[1:-1, 1:-1].T[:, ::-1].ravel()

    xs = np.concatenate([xa, xb, xc, xd, xe])
    ys = np.concatenate([ya, yb, yc, yd, ye])

    panel.points[:, 0] = ys
    panel.points[:, 1] = xs
    panel.points[:, 2] = 1

    return panel


def antarctic_panel():
    """Extract the antarctic cube-sphere panel and flatten."""
    bbox = geovista.geodesic.panel("antarctic")
    panel = bbox.enclosed(mesh)
    N = np.sqrt(panel.n_points)
    sample = np.linspace(-1, 1, num=int(N))
    xs = np.tile(sample, (49, 1))
    ys = xs[:, ::-1].T

    xa = xs[:-1, ::-1].T.ravel()
    xb = xs[-1, :][::-1]

    ya = ys[:-1, ::-1].T.ravel()
    yb = ys[-1, :][::-1]

    xs = np.concatenate([xa, xb])
    ys = np.concatenate([ya, yb])

    panel.points[:, 0] = ys
    panel.points[:, 1] = xs
    panel.points[:, 2] = -1

    return panel


threshold = False
if len(sys.argv) == 2:
    arg = sys.argv[1]
    if arg in ["-t", "--threshold"]:
        threshold = True

mesh = geovista.samples.lfric_sst()
name = "Surface Temperature"
sst = mesh[name]
clim = (np.nanmin(sst), np.nanmax(sst))

plotter = pv.Plotter()

kwargs = {
    "lighting": False,
    "show_scalar_bar": False,
    "clim": clim,
    "show_edges": False,
}


africa = africa_panel()
africa = africa.rotate_y(-90).translate((0, 0, -1))

asia = asia_panel()
asia = asia.rotate_z(-90).rotate_y(-90).translate((0, 2, -1))

pacific = pacific_panel()
pacific = pacific.rotate_z(-180).rotate_y(-90).translate((0, 4, -1))

americas = americas_panel()
americas = americas.rotate_z(90).rotate_y(-90).translate((0, -2, -1))

arctic = arctic_panel()
arctic = arctic.translate((-2, 0, -1))

antarctic = antarctic_panel()
antarctic = antarctic.rotate_y(180).translate((2, 0, -1))

if threshold:
    africa = cast(africa.threshold())
    asia = cast(asia.threshold())
    pacific = cast(pacific.threshold())
    americas = cast(americas.threshold())
    arctic = cast(arctic.threshold())
    antarctic = cast(antarctic.threshold())

vector = (0, 0, -0.25)
africa.extrude(vector, capping=True, inplace=True)
asia.extrude(vector, capping=True, inplace=True)
pacific.extrude(vector, capping=True, inplace=True)
americas.extrude(vector, capping=True, inplace=True)
arctic.extrude(vector, capping=True, inplace=True)
antarctic.extrude(vector, capping=True, inplace=True)

_ = plotter.add_mesh(africa, **kwargs)
_ = plotter.add_mesh(asia, **kwargs)
_ = plotter.add_mesh(pacific, **kwargs)
_ = plotter.add_mesh(americas, **kwargs)
_ = plotter.add_mesh(arctic, **kwargs)
_ = plotter.add_mesh(antarctic, **kwargs)

plotter.add_text(
    "LFRic C48 Unstructured Cube-Sphere (IKEA)",
    position="upper_left",
    font_size=10,
    shadow=True,
)

plotter.add_axes()
plotter.camera.zoom(1.5)
plotter.show()
