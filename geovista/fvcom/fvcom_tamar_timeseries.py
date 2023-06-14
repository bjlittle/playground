import netCDF4 as nc
from cf_units import Unit

import geovista as gv
from geovista.qt import GeoBackgroundPlotter
import geovista.theme


def callback():
    global t
    global mesh
    global layer
    global time
    global actor
    global fmt
    global normals
    global eta
    global sigma
    global depth
    global points
    global factor

    t = (t + 1) % 49
    mesh["data"] = temp[t, layer, :]
    mesh["Normals"] = normals
    mesh.GetPointData().SetActiveNormals("Normals")
    mesh.points = points
    tmp = eta[t].data
    ocean = tmp + sigma*(depth+tmp)
    mesh.point_data["ocean"] = ocean
    mesh.warp_by_scalar(scalars="ocean", inplace=True, factor=factor)

    mesh.active_scalars_name = "data"
    actor.SetText(3, time[t].strftime(fmt))


fname = "./tamar_v2_reduced_var.nc"
ds = nc.Dataset(fname)

lons = ds.variables["lon"][:]
lats = ds.variables["lat"][:]
connectivity = ds.variables["nv"][:] - 1

layer = 0
t = 0
factor = 3e-6

unit = Unit("days since 1858-11-17 00:00:00")
fmt = "%Y-%m-%d %H:%M"

temp = ds.variables["salinity"]
time = unit.num2date(ds.variables["time"][:].data)
sigma = ds.variables["siglay"][layer].data
eta = ds.variables["zeta"]
depth = ds.variables["h"][:].data

mesh = gv.Transform.from_unstructured(lons, lats, connectivity.T)

tmp = eta[t].data
ocean = tmp + sigma*(depth+tmp)

mesh.point_data["ocean"] = ocean
mesh.compute_normals(cell_normals=False, point_normals=True, inplace=True, flip_normals=True)
normals = mesh["Normals"]
points = mesh.points.copy()
mesh.warp_by_scalar(scalars="ocean", inplace=True, factor=factor)
mesh.point_data["data"] = temp[t, layer, :]

clim_temp = (7.790735, 16.898006)
clim_salinity = (1.0, 35.182487)

plotter = GeoBackgroundPlotter()
sargs = dict(title=f"Sea Water Salinity / 1e-3")
cmap = "haline"
plotter.add_mesh(mesh, show_edges=True, cmap=cmap, clim=clim_salinity, scalar_bar_args=sargs)
text = time[t].strftime(fmt)
actor = plotter.add_text(text, position="upper_right", font_size=10, shadow=True)
plotter.add_callback(callback, interval=250)
plotter.add_axes()
