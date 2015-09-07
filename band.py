#!/usr/bin/env python
import sys
from snappy import Product, ProductIO, ProductUtils, ProductData

# check if product file & band index given
if len(sys.argv) < 3:
    print 'Product file and band index required'
    sys.exit(1)

# check if band index given is correct
if not sys.argv[2] in ['2', '3', '4', '8']:
    print 'Incorrect band index'

# get cli arguments
product_file = sys.argv[1]
band_index = sys.argv[2]
band_name = 'B' + band_index
product_name = {
    'B2': 'blue',
    'B3': 'green',
    'B4': 'red',
    'B8': 'nir',
}[band_name]

# input product: open and get dimensions & name
input_product = ProductIO.readProduct(product_file)
product_width = input_product.getSceneRasterWidth()
product_height = input_product.getSceneRasterHeight()
product_name = input_product.getName()

# output product: copy selected band & save product
output_product = Product(product_name, product_name, product_width, product_height)
ProductUtils.copyGeoCoding(input_product, output_product)
ProductUtils.copyBand(band_name, input_product, output_product, True)
ProductIO.writeProduct(output_product, product_name + '.band.dim', 'BEAM-DIMAP')
output_product.closeIO()
