import processing
from qgis.core import QgsProject, QgsRasterLayer

# Paths to the raster layers in the QGIS project
raster_2015_layer_name = "2015 VST"
raster_2022_layer_name = "2022 VST"
output_loss_path = "/Users/josephberwind/Desktop/canopy_loss.tif"
output_gain_path = "/Users/josephberwind/Desktop/canopy_gain.tif"

# Get the QGIS project instance
project = QgsProject.instance()

# Load the raster layers from the QGIS project
raster_2015_layer = project.mapLayersByName(raster_2015_layer_name)[0]
raster_2022_layer = project.mapLayersByName(raster_2022_layer_name)[0]

# Check if layers are loaded correctly
if not raster_2015_layer or not raster_2022_layer:
    print("Error: One or both raster layers could not be loaded.")
else:
    # Calculate canopy loss: areas where there was canopy in 2015 but not in 2022
    print("Calculating canopy loss...")
    loss_result = processing.run("gdal:rastercalculator", {
        'INPUT_A': raster_2015_layer.source(),
        'BAND_A': 1,
        'INPUT_B': raster_2022_layer.source(),
        'BAND_B': 1,
        'FORMULA': '(A=1)*(B=0)',
        'NO_DATA': -9999,
        'RTYPE': 5,
        'OUTPUT': output_loss_path
    })
    print("Canopy loss calculation complete.")

    # Calculate canopy gain: areas where there was no canopy in 2015 but there is in 2022
    print("Calculating canopy gain...")
    gain_result = processing.run("gdal:rastercalculator", {
        'INPUT_A': raster_2015_layer.source(),
        'BAND_A': 1,
        'INPUT_B': raster_2022_layer.source(),
        'BAND_B': 1,
        'FORMULA': '(A=0)*(B=1)',
        'NO_DATA': -9999,
        'RTYPE': 5,
        'OUTPUT': output_gain_path
    })
    print("Canopy gain calculation complete.")

    # Verify the result of raster calculation
    if not loss_result['OUTPUT'] or not gain_result['OUTPUT']:
        print("Error: One or both raster calculations failed.")
    else:
        print(f"Canopy loss raster saved to: {output_loss_path}")
        print(f"Canopy gain raster saved to: {output_gain_path}")

        # Load the generated layers into QGIS
        canopy_loss_layer = iface.addRasterLayer(output_loss_path, "Canopy Loss")
        canopy_gain_layer = iface.addRasterLayer(output_gain_path, "Canopy Gain")

        # Check if the layers are valid
        if canopy_loss_layer.isValid() and canopy_gain_layer.isValid():
            print("Canopy loss and gain layers loaded successfully.")

            # Check raster statistics
            canopy_loss_stats = canopy_loss_layer.dataProvider().bandStatistics(1)
            canopy_gain_stats = canopy_gain_layer.dataProvider().bandStatistics(1)

            print("Canopy Loss Statistics:")
            print(f"Minimum Value: {canopy_loss_stats.minimumValue}")
            print(f"Maximum Value: {canopy_loss_stats.maximumValue}")
            print(f"Mean Value: {canopy_loss_stats.mean}")
            print(f"Standard Deviation: {canopy_loss_stats.stdDev}")

            print("Canopy Gain Statistics:")
            print(f"Minimum Value: {canopy_gain_stats.minimumValue}")
            print(f"Maximum Value: {canopy_gain_stats.maximumValue}")
            print(f"Mean Value: {canopy_gain_stats.mean}")
            print(f"Standard Deviation: {canopy_gain_stats.stdDev}")

        else:
            print("Error: One or both generated layers could not be loaded into QGIS.")
