"""Render FVCOM of Tamar & Sound (PML)."""

import netCDF4 as nc

import geovista as gv
import geovista.theme

fname = "./tamar_v2_2tsteps.nc"
ds = nc.Dataset(fname)

lons = ds.variables["lon"][:]
lats = ds.variables["lat"][:]
connectivity = ds.variables["nv"][:] - 1
elements = ds.variables["h_center"][:]
nodes = ds.variables["h"][:]

mesh = gv.Transform.from_unstructured(lons, lats, connectivity.T, data=elements)
mesh.point_data["nodes"] = nodes
mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True)
mesh.warp_by_scalar(scalars="nodes", inplace=True, factor=2e-5)

plotter = gv.GeoPlotter()  # (lighting="three lights")
sargs = {"title": "Bathymetry / m"}
plotter.add_mesh(
    mesh, cmap="balance", show_edges=False, scalar_bar_args=sargs, smooth_shading=True
)
plotter.view_yz()
plotter.add_axes()
plotter.show()
