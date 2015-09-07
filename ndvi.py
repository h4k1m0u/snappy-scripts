import sys

import numpy
from snappy import Product, ProductData, ProductIO, ProductUtils

if len(sys.argv) < 2:
    print 'Product file requires'
    sys.exit(1)

# input product & dimensions
input_product = ProductIO.readProduct(sys.argv[1])
width = input_product.getSceneRasterWidth()
height = input_product.getSceneRasterHeight()
product_name = input_product.getName()

# input product red & nir bands
red_band = input_product.getBand('B4')
nir_band = input_product.getBand('B8')

# output product (ndvi) & new band
output_product = Product('NDVI', 'NDVI', width, height)
ProductUtils.copyGeoCoding(input_product, output_product)
output_band = output_product.addBand('ndvi', ProductData.TYPE_FLOAT32)

# output writer
output_product_writer = ProductIO.getProductWriter('BEAM-DIMAP')
output_product.setProductWriter(output_product_writer)
output_product.writeHeader(product_name + '.ndvi.dim')

# compute & save ndvi line by line
red_row = numpy.zeros(width, dtype=numpy.float32)
nir_row = numpy.zeros(width, dtype=numpy.float32)

for y in xrange(height):
    red_row = red_band.readPixels(0, y, width, 1, red_row)
    nir_row = nir_band.readPixels(0, y, width, 1, nir_row)
    ndvi = (nir_row - red_row) / (nir_row + red_row)
    output_band.writePixels(0, y, width, 1, ndvi)

output_product.closeIO()
