from osgeo import gdal
import numpy as np

def calculate_coverage(raster_file):
    raster = gdal.Open(raster_file)
    band = raster.GetRasterBand(1)  # Assuming you want the first band

    # Read raster data as numerical array
    data = band.ReadAsArray()

    # Get NoData value of the raster data
    no_data_value = band.GetNoDataValue()

    # Create a mask for NoData values
    if no_data_value is not None:
        mask = (data == no_data_value)
    else:
        mask = np.zeros_like(data, dtype=bool)

    # Count total valid (not NoData) cells
    total_cells = np.count_nonzero(~mask)

    # Ensure that values are either 0 or 1
    data = np.where((data != 0) & (data != 1), 0, data)

    # Count tree cells (where value is 1)
    tree_cells = np.count_nonzero(data == 1)

    # Calculate percentage
    tree_percent_total = (tree_cells / total_cells) * 100
    return tree_percent_total

# File paths
raster_2015_path = "/Users/josephberwind/Desktop/2015 VST.vrt"
raster_2022_path = "/Users/josephberwind/Desktop/2022 VST.vrt"

# Calculate coverage for both years
coverage_2015 = calculate_coverage(raster_2015_path)
coverage_2022 = calculate_coverage(raster_2022_path)

print(f"Tree cover in 2015: {coverage_2015}%")
print(f"Tree cover in 2022: {coverage_2022}%")

# Calculate loss and gain
loss = coverage_2015 - coverage_2022
gain = coverage_2022 - coverage_2015

print(f"Tree canopy loss from 2015 to 2022: {loss}%")
print(f"Tree canopy gain from 2015 to 2022: {gain}%")
