"""Tree canopy coverage and change for West Orange, NJ.

Reads the binary tree masks (1 = tree, 0 = non-tree, NaN = outside the
township) for each year and reports canopy coverage plus pixel-level loss and
gain between years.

Coverage is computed over cells that are inside the township in *every* year
compared, so all years share one denominator. Cells outside the boundary are
NaN; the rasters carry no NoData value, so NaN has to be masked explicitly.
(An earlier version of this script counted those NaN cells in the
denominator, which understated coverage: 30% -> 27% instead of 51% -> 46%.)

The rasters are about 2.4 billion cells each, so they are read in row blocks
rather than all at once.

Usage (from the repository root):
    python scripts/canopy_statistics.py
    python scripts/canopy_statistics.py "raster-files/2015 VST.vrt" "raster-files/2022 VST.vrt"

Requires: numpy and the GDAL Python bindings (osgeo), e.g. the Python that
ships with QGIS, or `conda install gdal`.
"""

import math
import os
import sys

import numpy as np
from osgeo import gdal

gdal.UseExceptions()

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_RASTERS = [
    os.path.join(REPO, "raster-files", f"{year} VST.vrt") for year in ("2015", "2018", "2022")
]
BLOCK_ROWS = 2048


def year_of(path):
    return os.path.splitext(os.path.basename(path))[0].replace(" VST", "")


def main(paths):
    datasets = [gdal.Open(p) for p in paths]
    bands = [ds.GetRasterBand(1) for ds in datasets]
    names = [year_of(p) for p in paths]

    first = datasets[0]
    width, height = first.RasterXSize, first.RasterYSize
    for ds, name in zip(datasets, names):
        if (ds.RasterXSize, ds.RasterYSize) != (width, height) or ds.GetGeoTransform() != first.GetGeoTransform():
            sys.exit(f"{name} is not on the same grid as {names[0]}")

    valid = 0
    tree = [0] * len(paths)
    pairs = [(i, i + 1) for i in range(len(paths) - 1)]
    if len(paths) > 2:
        pairs.append((0, len(paths) - 1))
    loss = {p: 0 for p in pairs}
    gain = {p: 0 for p in pairs}

    for row in range(0, height, BLOCK_ROWS):
        rows = min(BLOCK_ROWS, height - row)
        blocks = [b.ReadAsArray(0, row, width, rows) for b in bands]
        inside = np.logical_and.reduce([np.isfinite(a) for a in blocks])
        for a, band in zip(blocks, bands):
            nodata = band.GetNoDataValue()
            if nodata is not None and not math.isnan(nodata):
                inside &= a != nodata
        valid += int(inside.sum())
        is_tree = [inside & (a == 1) for a in blocks]
        is_open = [inside & (a == 0) for a in blocks]
        for i in range(len(blocks)):
            tree[i] += int(is_tree[i].sum())
        for i, j in pairs:
            loss[(i, j)] += int((is_tree[i] & is_open[j]).sum())
            gain[(i, j)] += int((is_open[i] & is_tree[j]).sum())

    # EPSG:3857 pixels are 0.2 m on the map but smaller on the ground at this latitude.
    _, px, _, top, _, _ = first.GetGeoTransform()
    lat = math.degrees(2 * math.atan(math.exp(top / 6378137.0)) - math.pi / 2)
    ground_px = abs(px) * math.cos(math.radians(lat))
    area_km2 = valid * ground_px ** 2 / 1e6

    print(f"Cells inside the township in all years: {valid:,} (~{area_km2:.1f} km2, {area_km2 / 2.59:.1f} sq mi)")
    print()
    print("Canopy coverage")
    for name, t in zip(names, tree):
        print(f"  {name}: {t / valid * 100:.2f}%")
    print()
    print("Change (percentage points of township area)")
    for i, j in pairs:
        net = (tree[j] - tree[i]) / valid * 100
        rel = (tree[j] - tree[i]) / tree[i] * 100
        print(
            f"  {names[i]} -> {names[j]}: net {net:+.2f} pp ({rel:+.1f}% of {names[i]} canopy), "
            f"gross loss {loss[(i, j)] / valid * 100:.2f}%, gross gain {gain[(i, j)] / valid * 100:.2f}%"
        )


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT_RASTERS)
