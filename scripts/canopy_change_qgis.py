"""Canopy loss and gain rasters for the QGIS project (run in the QGIS Python console).

Builds two rasters from the yearly tree masks loaded in the project:
  loss: tree in the earlier year, non-tree in the later year
  gain: non-tree in the earlier year, tree in the later year
and adds them to the map. Outside the township (NaN in the masks) both
formulas evaluate to 0, so the outputs show change only inside the boundary.

Outputs are written to outputs/ next to the project file. Change EARLIER and
LATER to compare other years (layer names as they appear in the Layers panel).
For coverage percentages, run scripts/canopy_statistics.py instead.
"""

import os

import processing
from qgis.core import QgsProject
from qgis.utils import iface

EARLIER = "2015 VST"
LATER = "2022 VST"

project = QgsProject.instance()
out_dir = os.path.join(project.homePath() or os.path.expanduser("~"), "outputs")
os.makedirs(out_dir, exist_ok=True)


def layer(name):
    found = project.mapLayersByName(name)
    if not found:
        raise RuntimeError(f"Layer '{name}' is not in the project")
    return found[0]


earlier, later = layer(EARLIER), layer(LATER)
tag = f"{EARLIER.split()[0]}_{LATER.split()[0]}"

for kind, formula in (("loss", "(A==1)*(B==0)"), ("gain", "(A==0)*(B==1)")):
    out_path = os.path.join(out_dir, f"canopy_{kind}_{tag}.tif")
    processing.run("gdal:rastercalculator", {
        "INPUT_A": earlier.source(),
        "BAND_A": 1,
        "INPUT_B": later.source(),
        "BAND_B": 1,
        "FORMULA": formula,
        "NO_DATA": -9999,
        "RTYPE": 5,  # Float32
        "OUTPUT": out_path,
    })
    result = iface.addRasterLayer(out_path, f"Canopy {kind.title()} {tag.replace('_', '-')}")
    if not result or not result.isValid():
        raise RuntimeError(f"Could not load {out_path}")
    print(f"Canopy {kind} written to {out_path}")
