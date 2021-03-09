#!/usr/bin/env python

# set up
import os
import sys
import time
import pprint
import voluseg

if len(sys.argv) < 2:
    sys.exit('Usage: voluseg_submit.py [output-directory]')

dir_output = sys.argv[1]
file_output = os.path.join(dir_output, 'prepro.output')

#%%

# Get spark context
from pyspark.sql.session import SparkSession
spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext

with open(file_output, 'w') as fh:
    pprint.pprint(spark.sparkContext._conf.getAll(), fh)

#%%

# load parameters
parameters = voluseg.load_parameters(os.path.join(dir_output, 'parameters.pickle'))
with open(file_output, 'a') as fh:
    pprint.pprint(parameters, fh)

tic = time.time()
voluseg.step1_process_images(parameters)
with open(file_output, 'a') as fh:
    fh.write('step1_process_images: %.1f seconds\n'%(time.time() - tic))

tic = time.time()
voluseg.step2_align_images(parameters)
with open(file_output, 'a') as fh:
    fh.write('step2_align_images: %.1f seconds\n'%(time.time() - tic))

tic = time.time()
voluseg.step3_mask_images(parameters)
with open(file_output, 'a') as fh:
    fh.write('step3_mask_images: %.1f seconds\n'%(time.time() - tic))

tic = time.time()
voluseg.step4_detect_cells(parameters)
with open(file_output, 'a') as fh:
    fh.write('step4_detect_cells: %.1f seconds\n'%(time.time() - tic))

tic = time.time()
voluseg.step5_clean_cells(parameters)
with open(file_output, 'a') as fh:
    fh.write('step5_clean_cells: %.1f seconds\n'%(time.time() - tic))
