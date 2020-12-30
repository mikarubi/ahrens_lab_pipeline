#!/usr/bin/env python

# set up
import os
import sys
import time
import pprint
import voluseg

if len(sys.argv) < 4:
    sys.exit('Usage: voluseg_submit.py [number-of-nodes] [output-directory] [master-url]')

n_workers = sys.argv[1]
dir_output = sys.argv[2]
url_master = sys.argv[3]
file_output = os.path.join(dir_output, 'prepro.output')

#%%

# import the required classes
from pyspark.sql.session import SparkSession
spark = SparkSession.builder.getOrCreate()

# Update the default configurations
conf = spark.sparkContext._conf.setAll([
        ('spark.master', url_master),
        ('spark.default.parallelism', str(int(n_workers) * 50))])

# Create a new spark Session
spark.sparkContext.stop()
spark = SparkSession.builder.config(conf=conf).getOrCreate()
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
