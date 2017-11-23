"""
Parameter file template for make_cwt.py. It is suggested to make a copy and modify the copy instead of this file.
"""

import sys as _sys

# Folder to put the results in (relative or absolute path)
# Put '.' to put it where the script is.
results_dir = 'results'

# Name of input file. Must be a wav (I think)
# Can indicate a full path, like 'this/is/where/Ifind/love.wav'
input_file = 'input/cup.wav'

# If signal is stereo, put 'left' or 'right' to transform one channel or the other.
# Ignored if mono
stereo_side = 'left' 

# Downsampling factor of initial signal
# For instance, downsampling = 2 takes half the points.
downsampling_signal = 2

# Part of signal to be considered (in seconds)
start = 0 # 0 is start of signal
end = -1 # -1 is end of signal

# Freq to consider
log_scale = True # True for log scale, False for linear one 
lower_bound = 1.9 # in Hertz for lin, or exponent for log scale
upper_bound = 4 # idem
base_log = 10 # Base for log scale. Ignored if linear.
n_freq = 300 # Number of frequencies to consider (-> resolution in freq.)

# Gaussian filter to smooth out the output
# First value is std in number of point in the frequency direction
# Second value is std in number of point in the temporal direction
# Put [1, 1] for not filter.
filter_gaussian = [1, 30]

# Downsampling factor for the output array
# First value is for time, last for frequency
# Put [1, 1] for no downsampling
downsampling_array = [3, 3]

# Save numpy array or not (pickle file).
# Put 'None' if you don't want to save the array, a string for its name otherwise
# If saved, the vectors of times and frequencies are also saved, as well as the signal.
# Do this if you want to plot with plot_cwt.py script!
save_array = 'cup.pic' # None

# Name of output file (stl)
output_file = 'cup.stl'

# Additional stl options
# I don't really know what they do, see 
# stl_tools.numpy2stl documentation.
stl_options = {'scale':0.05,
				'mask_val':5.,
				'solid':True}

# Do the plots as well or not
do_plots_too = True
paras_file_plots = 'paras_plot.py' # name of paras file for plots


#### DO NOT MODIFY THIS !!!! #####
paras = {k:v for k,v in vars().items() if k[:1]!='_' and k!='version' and k!='Paras' and not k in [key for key in locals().keys()
           if key in locals().keys() and isinstance(locals()[key], type(_sys)) and not key.startswith('__')]}