Release History
===============

0.3.0 (XXX)
-----------

* Adding `transform_bounding_box` to calculate the largest projected bounding box given the four corners on a local coordinate system.
* Removing GDAL, Shapely from the hard requirements in setup.py.  This will allow pygeoprocessing to be built by package managers like pip without these two packages being installed.  GDAL and Shapely will still need to be installed for pygeoprocessing to run as expected.
* Fixed a defect in ``pygeoprocessing.testing.assert_checksums_equal`` preventing BSD-style checksum files from being analyzed correctly.
* Fixed an issue in reclassify_dataset_uri that would cause an exception if the incoming raster didn't have a nodata value defined.
* Fixed a defect in ``pygeoprocessing.geoprocessing.get_lookup_from_csv`` where the dialect was unable to be detected when analyzing a CSV that was larger than 1K in size.  This fix enables the correct detection of comma or semicolon delimited CSV files, so long as the header row by itself is not larger than 1K.
* Intra-package imports are now relative.  Addresses an import issue for users with multiple copies of pygeoprocessing installed across multiple Python installations.
* Exposed cython routing functions so they may be imported from C modules.
* `get_lookup_from_csv` attempts to determine the dialect of the CSV instead of assuming comma delimited.
* Added relative numerical tolerance parameters to the PyGeoprocessing raster and csv tests with in the same API style as `numpy.testing.allclose`.
* Fixed an incomparability with GDAL 1.11.3 bindings that expects a boolean type in `band.ComputeStatistics`.  Before this fix PyGeoprocessing would crash with a TypeError on many operations.
* Fixed a defect in pygeoprocessing.routing.calculate_transport where the nodata types were cast as int even though the base type of the routing rasters were floats.  In extreme cases this could cause a crash on a type that could not be converted to an int, like an `inf`, and in subtle cases this would result in nodata values in the raster being ignored during routing.
* Added functions to construct raster and vectors on disk from reasonable datatypes (numpy matrices for rasters, lists of Shapely geometries for vectors).
* Fixed an issue where reproject_datasource_uri would add geometry that couldn't be projected directly into the output datasource.  Function now only adds geometries that transformed without error and reports if any features failed to transform.
* Added file flushing and dataset swig deletion in reproject_datasource_uri to handle a race condition that might have been occuring.
* Fixed an issue when "None" was passed in on new raster creation that would attempt to directly set that value as the nodata value in the raster.
* Added basic filetype-specific assertions for many geospatial filetypes, and tests for these assertions.  These assertions are exposed in `pygeoprocessing.testing`.
* Pygeoprocessing package tests can be run by invoking `python setup.py nosetests`.  A subset of tests may also be run from an installed pygeoprocessing distribution by calling `pygeoprocessing.test()`.
* Fixed an issue with reclassify dataset that would occur when small rasters whose first memory block would extend beyond the size of the raster thus passing in "0" values in the out of bounds area. Reclassify dataset identified these as valid pixels, even though vectorize_datsets would mask them out later.  Now vectorize_datasets only passes memory blocks that contain valid pixel data to its kernel op.
* Added support for very small AOIs that result in rasters less than a pixel wide.  Additionally an `all_touched` flag was added to allow the ALL_TOUCHED=TRUE option to be passed to RasterizeLayer in the AOI mask calculation.
* Added watershed delination routine to pygeoprocessing.routing.delineate_watershed.  Operates on a DEM and point shapefile, optionally snaps outlet points to nearest stream as defined by a thresholded flow accumulation raster and copies the oulet point fields into the constructed watershed shapefile.
* Fixing a memory leak in block caches that held on to dataset, band, and block references even after the object was destroyed.
* Add an option to route_flux that lets the current pixel's source be included in the flux, or not.  Previous version would include on the source no matter what.
* Now using natcap.versioner for versioning instead of local versioning logic.

0.2.2 (2015-05-07)
------------------

* Adding MinGW-specific compiler flags for statically linking pygeoprocessing binaries against libstdc++ and libgcc.  Fixes an issue on many user's computers when installing from a wheel on the Python Package Index without having two needed DLLs on the PATH, resuling in an ImportError on pygeoprocessing.geoprocessing_core.pyd.
* Fixing an issue with versioning where 'dev' was displayed instead of the version recorded in pygeoprocessing/__init__.py.
* Adding all pygeoprocessing.geoprocessing functions to pygeoprocessing.__all__, which allows those functions to appear when calling help(pygeoprocessing).
* Adding routing_core.pxd to the manifest.  This fixes an issue where some users were unable to compiler pygeoprocessing from source.

0.2.1 (2015-04-23)
------------------

* Fixed a bug on the test that determines if a raster should be memory blocked.  Rasters were not getting square blocked if the memory block was row aligned.  Now creates 256x256 blocks on rasters larger than 256x256.
* Updates to reclassify_dataset_uri to use numpy.digitize rather than Python loops across the number of keys.
* More informative error messages raised on incorrect bounding box mode.
* Updated docstring on get_lookup_from_table to indicate the headers are case insensitive.
* Added updates to align dataset list that report which dataset is being aligned.  This is helpful for logging feedback when many datasets are passed in that don't take long enough to get a report from the underlying reproject dataset function.
* pygeoprocessing.routing.routing_core includes pxd to be \`cimport`able from a Cython module.

0.2.0 (2015-04-14)
------------------

* Fixed a library wide issue relating to the underlying numpy types of GDT_Byte Datasets.  Now correctly identify the signed and unsigned versions and removed all instances where code used to mod byte data to unsigned data and correctly creates signed/unsigned byte datasets during resampling.
* Removed extract_band_and_nodata function since it exposes the underlying GDAL types.
* Removed reclassify_by_dictionary since reclassify_dataset_uri provided almost the same functionality and was widely used.
* Removed the class OrderedDict that was not used.
* Removed the function calculate_value_not_in_dataset since it loaded the entire dataset into memory and was not useful.

0.1.8 (2015-04-13)
------------------

* Fixed an issue on reclassifying signed byte rasters that had negative nodata values but the internal type stored for vectorize datasets was unsigned.

0.1.7 (2015-04-02)
------------------

* Package logger objects are now identified by python heirarchical package paths (e.g. pygeoprocessing.routing)
* Fixed an issue where rasters that had undefined nodata values caused striping in the reclassify_dataset_uri function.

0.1.6 (2015-03-24)
------------------

* Fixing LICENSE.TXT to .txt issue that keeps reoccuring.

0.1.5 (2015-03-16)
------------------

* Fixed an issue where int32 dems with INT_MIN as the nodata value were being treated as real DEM values because of an internal cast to a float for the nodata type, but a cast to double for the DEM values.
* Fixed an issue where flat regions, such as reservoirs, that could only drain off the edge of the DEM now correctly drain as opposed to having undefined flow directions.

0.1.4 (2015-03-13)
------------------

* Fixed a memory issue for DEMs on the order of 25k X 25k, still may have issues with larger DEMs.

0.1.3 (2015-03-08)
------------------

* Fixed an issue so tox correctly executes on the repository.
* Created a history file to document current and previous releases.
* Created an informative README.rst.

0.1.2 (2015-03-04)
------------------

* Fixing issue that caused "LICENSE.TXT not found" during pip install.

0.1.1 (2015-03-04)
------------------

* Fixing issue with automatic versioning scheme.

0.1.0 (2015-02-26)
------------------

* First release on PyPI.
