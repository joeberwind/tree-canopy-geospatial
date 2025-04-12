# Tree Canopy Geospatial Analysis – West Orange, NJ

This project, conducted in collaboration with the **West Orange Energy Commission**, analyzes urban tree canopy using geospatial raster data, machine learning outputs, and QGIS tools. The analysis focuses on identifying **canopy change between 2015 and 2022**, using aerial imagery and semantic segmentation to identify trees vs non-trees across time.

## Project Goals
- Visualize and quantify **tree canopy loss/gain** over time
- Enable decision-makers to track environmental and zoning impacts
- Provide reproducible steps using **QGIS**, **Python**, and **GDAL**

## Repository Contents

| Folder | Description |
|--------|-------------|
| `scripts/` | Python scripts for statistics, change detection, and data prep |
| `data/` | Mosaic folders from different time periods (TIFF-based) |
| `qgis_project/` | QGIS project file with all layers and symbology pre-configured |
| `vrt/` | Steps and notes on building Virtual Raster Tables (VRTs) |
| `docs/` | Optional screenshots, diagrams, or maps |

## Data Description

All raster images:
- `1`: Tree
- `0`: Non-tree
- `NaN`: Outside study boundary

Coordinate system: **EPSG:4326**, optionally reprojected to **EPSG:3857** for basemap alignment.

## Key Tools & Technologies
- QGIS 3.x
- GDAL (gdalbuildvrt)
- Python 3.x
- Semantic segmentation model (not publicly available)
- Google Satellite Basemap

## Key Insights
- Tree canopy loss/gain was mapped from mosaics of 2015 and 2022 data
- Tree classification is binary, derived from aerial RGB imagery and machine learning
- Due to inconsistent image acquisition, the project does not represent a full time-series analysis, but it offers strong year-over-year comparisons in select areas

## Notes
- Model weights are **not available**
- Imagery coverage varies by year
- Classification predictions should be interpreted with caution outside of central coverage zones

## Sample Metrics
- **Tree Cells (2022):** 1.28B
- **Non-Tree Cells (2022):** 1.48B

## Contributors
- Joseph Berwind (West Orange Energy Commission)

## License
MIT
