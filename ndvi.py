import sys

import numpy
from snappy import Product
from snappy import ProductData
from snappy import ProductIO
from snappy import ProductUtils

if len(sys.argv) != 2:
    print("usage: %s <file>" % sys.argv[0])
    sys.exit(1)

print("Reading...")
product = ProductIO.readProduct(sys.argv[1])
width = product.getSceneRasterWidth()
height = product.getSceneRasterHeight()
name = product.getName()
description = product.getDescription()
band_names = product.getBandNames()

print("Product:     %s, %s" % (name, description))
print("Raster size: %d x %d pixels" % (width, height))
print("Bands:       %s" % (list(band_names)))

red = product.getBand('B4')
nir = product.getBand('B8')
ndviProduct = Product('NDVI', 'NDVI', width, height)
ndviBand = ndviProduct.addBand('ndvi', ProductData.TYPE_FLOAT32)
writer = ProductIO.getProductWriter('BEAM-DIMAP')

ProductUtils.copyGeoCoding(product, ndviProduct)

ndviProduct.setProductWriter(writer)
ndviProduct.writeHeader('snappy_ndvi_output.dim')

row4 = numpy.zeros(width, dtype=numpy.float32)
row8 = numpy.zeros(width, dtype=numpy.float32)

print("Writing...")

for y in range(height):
    print("processing line ", y, " of ", height)
    row4 = red.readPixels(0, y, width, 1, row4)
    row8 = nir.readPixels(0, y, width, 1, row8)

    ndvi = (row8 - row4) / (row8 + row4)
    ndviBand.writePixels(0, y, width, 1, ndvi)

ndviProduct.closeIO()

print("Done.")
