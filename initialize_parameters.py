# set up
import os
import pprint
import voluseg


### set these parameters ###
dir_data = 'fish1-1s2s17s_20190125_160126'
dir_input = os.path.join('/nrs/ahrens/EnYang/whole brain/20190125/', dir_data)
dir_output = os.path.join('/groups/ahrens/ahrenslab/mika/', dir_data)
channel_file = os.path.join(dir_input,'ch0.xml')
stack_file = os.path.join(dir_input,'Stack_frequency.txt')
### end set these parameters ###


# get default parameters and set directories
parameters0 = voluseg.parameter_dictionary()
parameters0['dir_input'] = dir_input
parameters0['dir_output'] = dir_output

# retrieve metadata from channel and stack files
parameters0 = voluseg.load_metadata(parameters0, channel_file, stack_file)

# set other parameters as necessary
parameters0['diam_cell'] = 5.0

# create parameter file with metadata
voluseg.step0_process_parameters(parameters0)

# check saved parameters
parameters = voluseg.load_parameters(os.path.join(dir_output, 'parameters.pickle'))
pprint.pprint(parameters)
