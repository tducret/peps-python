# PEPS Python

[![Travis](https://img.shields.io/travis/tducret/peps-python.svg)](https://travis-ci.org/tducret/peps-python)
[![Coveralls github](https://img.shields.io/coveralls/github/tducret/peps-python.svg)](https://coveralls.io/github/tducret/peps-python)
[![PyPI](https://img.shields.io/pypi/v/peps.svg)](https://pypi.org/project/peps/)
![License](https://img.shields.io/github/license/tducret/peps-python.svg)

## Description

Python wrapper for peps.cnes.fr.

# Requirements

- Python 3
- pip3

## Installation

```bash
pip3 install -U peps
```

## Package usage

Basic example

```python
# -*- coding: utf-8 -*-
import peps

results = peps.find_products(nb_resultats_max=2)
print(results)
```

Example output :

```bash
id : ca025549-2a12-51bc-bac8-301dafdf2f6b, title : S3A_OL_2_LFR____20181012T063955_20181012T064255_20181012T081800_0179_036_362_3960_SVL_O_NR_002, collection
 : S3, acquisition_date : 2018-10-12T06:39:54.756Z, platform : S3A, instrument : OLCI, sensor_mode : Earth Observation, absolute_orbit_number : 13810, relative_orbit_number : 362, orbit_direction : descending, resource_size : 83453508, publication_date : 2018-10-12T08:41:34.476Z, cloud_cover : 0, ingestion_date :
 2018-10-12T08:39:11.296Z, product_type : OL_2_LFR___, processing_level : LEVEL2, snow_cover : None, storage_mode : disk, tile_id : , country : , continent : ,
id : 601054bd-0ce9-555f-8cc5-5500ca9eb4d4, title : S3A_OL_2_LFR____20181012T063655_20181012T063955_20181012T081807_0179_036_362_3780_SVL_O_NR_002, collection
 : S3, acquisition_date : 2018-10-12T06:36:54.756Z, platform : S3A, instrument : OLCI, sensor_mode : Earth Observation, absolute_orbit_number : 13810, relative_orbit_number : 362, orbit_direction : descending, resource_size : 83158262, publication_date : 2018-10-12T08:39:50.975Z, cloud_cover : 0, ingestion_date :
 2018-10-12T08:38:25.728Z, product_type : OL_2_LFR___, processing_level : LEVEL2, snow_cover : None, storage_mode : disk, tile_id : , country : Afrique Du Sud, continent : Afrique,
```

---

Extract specific info to CSV format :

```python
# -*- coding: utf-8 -*-
import peps

results = peps.find_products(collection="S2ST", nb_resultats_max=10)

print("platform, tile_id, title, acquisition_date")
for result in results:
    print(",".join([result.platform, result.tile_id, result.title, result.acquisition_date]))
```

Example output :

```bash
platform, tile_id, title, acquisition_date
S2A,46WFB,S2A_MSIL1C_20181012T052741_N0206_R105_T46WFB_20181012T063644,2018-10-12T05:27:41.024Z
S2A,47WMR,S2A_MSIL1C_20181012T052741_N0206_R105_T47WMR_20181012T063644,2018-10-12T05:27:41.024Z
S2A,48WWE,S2A_MSIL1C_20181012T052741_N0206_R105_T48WWE_20181012T063644,2018-10-12T05:27:41.024Z
S2A,47WMS,S2A_MSIL1C_20181012T052741_N0206_R105_T47WMS_20181012T063644,2018-10-12T05:27:41.024Z
S2A,49WDV,S2A_MSIL1C_20181012T052741_N0206_R105_T49WDV_20181012T063644,2018-10-12T05:27:41.024Z
S2A,46WFC,S2A_MSIL1C_20181012T052741_N0206_R105_T46WFC_20181012T063644,2018-10-12T05:27:41.024Z
S2A,47WNQ,S2A_MSIL1C_20181012T052741_N0206_R105_T47WNQ_20181012T063644,2018-10-12T05:27:41.024Z
S2A,47WNR,S2A_MSIL1C_20181012T052741_N0206_R105_T47WNR_20181012T063644,2018-10-12T05:27:41.024Z
S2A,46WED,S2A_MSIL1C_20181012T052741_N0206_R105_T46WED_20181012T063644,2018-10-12T05:27:41.024Z
S2A,47XPA,S2A_MSIL1C_20181012T052741_N0206_R105_T47XPA_20181012T063644,2018-10-12T05:27:41.024Z
```

## TODO

- [ ] Add multithreading?
- [ ] Publish package to pypi
- [ ] Calculate center of polygon and extract it for Kibana (geo_point), with shapely package
- [ ] Add other search parameters : instrument, platform, level, product, sensor_mode, nrt, orbit (min, max, ascending/descending, location, keywords, area of interest)
- [ ] Add possibility to download products