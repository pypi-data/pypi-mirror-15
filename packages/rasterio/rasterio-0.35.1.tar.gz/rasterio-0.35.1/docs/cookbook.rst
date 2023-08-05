=================
Rasterio Cookbook
=================

.. todo::

    Fill out examples of using rasterio to handle tasks from typical
    GIS and remote sensing workflows.

The Rasterio cookbook is intended to provide in-depth examples of rasterio usage
that are not covered by the basic usage in the User's Manual. Before using code
from the cookbook, you should be familar with the basic usage of rasterio; see
"Reading Datasets", "Working with Datasets" and "Writing Datasets" to brush up on
the fundamentals.

Generating summary statistics for each band
-------------------------------------------

.. literalinclude:: recipes/band_summary_stats.py
    :language: python
    :linenos:

.. code::

    $ python docs/recipes/band_summary_stats.py
    [{'max': 255, 'mean': 29.94772668847656, 'median': 13.0, 'min': 0},
     {'max': 255, 'mean': 44.516147889382289, 'median': 30.0, 'min': 0},
     {'max': 255, 'mean': 48.113056354742945, 'median': 30.0, 'min': 0}]

Raster algebra
--------------

Resampling rasters to a different cell size
--------------------------------------------

Reproject/warp a raster to a different CRS
------------------------------------------

Reproject to a Transverse Mercator projection, Hawaii zone 3 (ftUS),
aka EPSG code 3759. 

.. literalinclude:: recipes/reproject.py
    :language: python
    :linenos:

.. code::

    $ python docs/recipes/reproject.py


The original image

.. image:: img/world.jpg
    :scale: 100 %

Warped to ``EPSG:3759``. Notice that the bounds are contrainted to the new projection's
valid region (``CHECK_WITH_INVERT_PROJ=True`` on line 13) and the new raster is wrapped seamlessly across the anti-meridian.

.. image:: img/reproject.jpg
    :scale: 100 %

Raster to polygon features
--------------------------

Rasterizing GeoJSON features
----------------------------

Masking raster with a polygon feature
-------------------------------------

Using ``rasterio`` with ``fiona``, we can open a shapefile, read geometries, and
mask out regions of a raster that are outside the polygons defined in the shapefile.

This shapefile contains a single polygon, a box near the center of the raster,
so in this case, our list of geometries is one element long.

Applying the features in the shapefile as a mask on the raster sets all pixels outside
of the features to be zero. Since ``crop=True`` in this example, the extent of the raster
is also set to be the extent of the features in the shapefile.

We can then use the updated spatial transform and raster height and width
to write the masked raster to a new file.

.. literalinclude:: recipes/mask_shp.py
    :language: python
    :linenos:

.. code::

    $ python docs/recipes/mask_shp.py


The original image with the shapefile overlayed

.. image:: img/box_rgb.png
    :scale: 80 %

Masked and cropped to the geometry

.. image:: img/box_masked_rgb.png
    :scale: 80 %

Creating valid data bounding polygons
-------------------------------------

Raster to vector line feature
-----------------------------

Creating raster from numpy array
--------------------------------

Creating a least cost path
--------------------------

Using a scipy filter to smooth a raster
---------------------------------------

This recipe demonstrates the use of scipy's `signal processing filters <http://docs.scipy.org/doc/scipy/reference/signal.html#signal-processing-scipy-signal>`_ to manipulate multi-band raster imagery
and save the results to a new GeoTIFF. Here we apply a median filter to smooth
the image and remove small inclusions (at the expense of some sharpness and detail).

.. literalinclude:: recipes/filter.py
    :language: python
    :linenos:

.. code::

    $ python docs/recipes/filter.py


The original image

.. image:: img/RGB.byte.jpg
    :scale: 50 %

With median filter applied

.. image:: img/filtered.jpg
    :scale: 50 %

Using skimage to adjust the saturation of a RGB raster
------------------------------------------------------

This recipe demonstrates the use of manipulating color with the scikit image `color module <http://scikit-image.org/docs/stable/api/skimage.color.html>`_.

.. literalinclude:: recipes/saturation.py
    :language: python
    :linenos:

.. code::

    $ python docs/recipes/saturation.py


The original image

.. image:: img/RGB.byte.jpg
    :scale: 50 %

With increased saturation

.. image:: img/saturation.jpg
    :scale: 50 %


Generating a KMZ from a raster
------------------------------

A raster can be converted to a KMZ and opened in Google Earth using ``rasterio`` to access the raster metadata. Executing

.. code::

    $ python docs/recipes/raster_to_kmz.py

creates the file ``green_box.tif``, which is a green image that extends from longitude -36 to -35 and latitude 74 to 75 in ``EPSG:4326`` projection, and then embeds this raster in a KMZ file ``green_box.kmz``. In Google Earth, we can see the box inside Greenland (screenshot below).

.. image:: img/green_box_kmz.png
    :scale: 50 %
