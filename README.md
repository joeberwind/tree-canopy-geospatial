# Tree Canopy Change Analysis – West Orange, NJ

I measured how much tree canopy West Orange, NJ lost between 2015 and 2022, and where, for the West Orange Environmental Commission. The analysis is the 2023 study cited in the findings (§28-2a) of the township's Tree Protection, Removal and Replacement Ordinance, [Ordinance 2846-24](https://westorange.org/DocumentCenter/View/5658/2846-24-Tree-Ordinance), adopted June 10, 2024.

## Results

Canopy coverage is measured over the same 12.2 sq mi (31.7 km²) of township land in every year.

| Year | Tree canopy | Imagery product |
|---|---|---|
| 2015 | 51.4% | `all_h`, 2015 imagery |
| 2018 | 50.3% | `all_h`, 2016–2018 imagery |
| 2022 | 46.5% | `all_mr`, 2022 imagery |

| Period | Net change | Gross loss | Gross gain |
|---|---|---|---|
| 2015 → 2018 | −1.1 pp | 4.2% | 3.1% |
| 2018 → 2022 | −3.8 pp | 6.5% | 2.7% |
| 2015 → 2022 | −4.9 pp (−9.5% of 2015 canopy) | 8.5% | 3.6% |

pp = percentage points of township area. Gross loss and gain are the share of township area that changed from tree to non-tree, or the reverse. They include classification and registration noise, so the net change is the more reliable figure.

The decline appears on consistent imagery between 2015 and 2018. Most of the measured drop comes after 2018, the same period in which the source product changes (see Limitations).

### Correction (November 2026)

The 2023 presentations reported canopy of 30% in 2015 and 27% in 2022, a drop of about 3 points. That calculation counted the cells outside the township boundary, which are NaN in the rasters, as part of the total area. The rasters carry no NoData value, so those cells were never masked out, and coverage was understated by roughly 40%. `scripts/canopy_statistics.py` now masks NaN explicitly. The direction of the finding is unchanged, and the corrected decline is larger.

## Data

The inputs are binary tree masks at 0.2 m pixels (EPSG:3857), exported from Google Earth Engine in May 2023. They were produced by a semantic segmentation model applied to aerial RGB imagery. The model is not mine, and its weights are not public.

| Value | Meaning |
|---|---|
| 1 | Tree |
| 0 | Non-tree |
| NaN | Outside the township |

Each year comes as four GeoTIFF tiles on an identical 46,844 × 50,850 grid, which makes about 2.4 billion cells per year, 1.38 billion of them inside the township. The tile file names carry the export parameters: `tc0p6` (tree threshold 0.6), `wc0p85`, `pf` and `s0p2` (0.2 m scale).

The rasters are not included in this repository. To reproduce the analysis, place the tiles here:

```
data/2015/west_orange_new_jersey_united_states_tree_mask_mosaic_all_h_tc0p6_wc0p85_pf_s0p2_2015_cutoff-*.tif
data/2018/west_orange_new_jersey_united_states_tree_mask_mosaic_all_h_tc0p6_wc0p85_pf_s0p2_2016_2018-*.tif
data/2022/west_orange_new_jersey_united_states_tree_mask_mosaic_all_mr_tc0p6_wc0p85_pf_s0p2-*.tif
```

## Repository contents

| Path | What it is |
|---|---|
| `raster-files/2015 VST.vrt`, `2018 VST.vrt`, `2022 VST.vrt` | GDAL virtual rasters that mosaic each year's four tiles from `data/` (relative paths) |
| `scripts/canopy_statistics.py` | Coverage, net change, and gross loss and gain across years; reads in blocks, masks NaN |
| `scripts/canopy_change_qgis.py` | PyQGIS script that writes canopy loss and gain rasters to `outputs/` and adds them to the map |
| `West Orange Tree Canopy Project.qgz` | QGIS 3.36 project with the tree masks, VRTs, loss and gain layers, basemaps and the FEMA flood hazard layer |
| `docs/` | 2015 and 2022 canopy maps |

## How to run

Statistics (any Python with numpy and the GDAL bindings, including the one that ships with QGIS):

```
python scripts/canopy_statistics.py
```

To compare specific years:

```
python scripts/canopy_statistics.py "raster-files/2015 VST.vrt" "raster-files/2022 VST.vrt"
```

Loss and gain maps: open `West Orange Tree Canopy Project.qgz` in QGIS, then run `scripts/canopy_change_qgis.py` from the Python console. It writes compressed 0/1 rasters (about 12 MB each; under a minute on a laptop) to `outputs/`. Edit `EARLIER` and `LATER` at the top of the script to compare other years. Tested with QGIS 3.44 LTR.

## Limitations

- **Different source products.** 2022 comes from a different imagery and model product (`all_mr`) than 2015 and 2018 (`all_h`), so part of the post-2018 change may come from the source data rather than the trees. The 2015 → 2018 comparison uses one product.
- **Points in time.** This compares three dates, not a continuous time series.
- **No accuracy assessment.** The masks were not validated against ground truth, and pixel-level change at 0.2 m is sensitive to small misalignments between years. Township-wide totals are more robust than individual pixels.
- **Flood hazard layers are context only.** The FEMA flood hazard layer was overlaid for visual inspection. No statistical analysis of canopy loss against flood zones was done.

## Contributors

Joseph Berwind, West Orange Environmental Commission

## License

MIT
