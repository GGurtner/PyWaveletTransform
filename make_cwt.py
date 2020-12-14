#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use this file like this:
./make_cwt.py my_paras.py
or this:
./make_cwt.py
to produce a cwt of a signal. Parameters are read from the corresponding my_paras.py file
or the default paras.py file in the second case.
"""

from pylab import *

import os
import sys
from os.path import join as jn
import pywt
from scipy.io.wavfile import read

from scipy import signal, ndimage
from stl_tools import numpy2stl
import pickle
import matplotlib.image as mpimg
from math import log # because numpy log has no base argument...
from stl import mesh

from make_plot_cwt import do_plots, read_paras

def prepare_signal(paras):
	print (paras['input_file'])
	a = read(paras['input_file'])
	# Initial sampling frequency
	f_s_i = a[0]

	# Signal
	if type(a[1][0]) in [tuple, list, array, ndarray]:
		if len(a[1][0])==2:
			print ('Detected stereo signal, transforming', paras['stereo_side'], 'channel.')
			if paras['stereo_side']=='left':
				b = list(zip(*a[1]))[0]
			else:
				b = list(zip(*a[1]))[1]
		else:
			raise Exception('Could not recognise the type of signal.')
	else:
		print ('Detected mono signal.')
		b = a[1]
		
	# Downsample the signal
	b = b[::paras['downsampling_signal']]

	# New sampling frequency after downsampling
	fs = a[0]/paras['downsampling_signal']

	# Array of time in seconds
	times = array(list(arange(len(b))))/fs

	# Select part of the signal:
	idx_start = next((i for i, t in enumerate(times) if t > paras['start']), -1) - 1
	idx_start = max(0, idx_start)
	if paras['end']!=-1:
		idx_end = next((i for i, t in enumerate(times) if t > paras['end']), -1)
	else:
		idx_end = -1

	if idx_start == idx_end:
		raise Exception("The signal selected is empty. Check the bounds ('start' and 'end')")

	b = b[idx_start:idx_end]
	times = times[idx_start:idx_end]

	print ("Selected", len(b), "points between", "{:04.2f}s and".format(times[0]), "{:04.2f}s".format(times[-1]), "at sampling frequency {:04.1f}Hz".format(fs))

	return b, fs, times

def do_cwt(paras, b, fs):
	if paras['log_scale']:
		space_gen = logspace
		kwarg = {'base':paras['base_log']}
		lb = log(paras['lower_bound'], paras['base_log'])
		ub = log(paras['upper_bound'], paras['base_log'])
	else:
		space_gen = linspace
		kwarg = {}
		lb, ub = paras['lower_bound'], paras['upper_bound']

	# Choose frequencies
	freqs = array(space_gen(lb, ub, paras['n_freq'], **kwarg))
	
	# Transform them in scales
	scales = fs/freqs

	# Compute the transformation
	cwtmatr = signal.cwt(b, signal.ricker, scales)

	return cwtmatr, freqs

def post_process(paras, cwtmatr, b, fs, times, freqs):
	zz = sqrt(cwtmatr**2)

	# Smooth out the output with gaussian kernel
	if paras['filter_gaussian'] != [1, 1]:
		zz = ndimage.filters.gaussian_filter(zz, paras['filter_gaussian'], mode='constant')

	# Downsampling output:
	zz = zz[::paras['downsampling_array'][0],::paras['downsampling_array'][1]]
	times = times[::paras['downsampling_array'][0]]
	freqs = freqs[::paras['downsampling_array'][1]]
	b = b[::paras['downsampling_array'][0]]

	# Save numpy array
	if not paras['output_pic'] is None:
		path = jn(paras['results_dir'], paras['output_pic'])
		print ('Saving .pic file as', path)
		with open(path, 'wb') as f:
			pickle.dump((b, zz, times, freqs), f)

	# Save stl file
	path = jn(paras['results_dir'], paras['output_stl'])
	print ('Saving .stl file as', path)
	numpy2stl(zz, path, **paras['stl_options'])

	# Rescale x/y axis
	the_mesh = mesh.Mesh.from_file(path)
	xsize =	the_mesh.x.max() -	the_mesh.x.min()
	ysize =	the_mesh.y.max() -	the_mesh.y.min()

	the_mesh.y = the_mesh.y*(xsize/ysize)/paras['ratio_xy']

	the_mesh.save(path)

	return b, zz, times, freqs

if __name__=='__main__':
	if len(sys.argv)<2:
		print("You did not specify a paras file, I try to use: paras.py")
		paras_file_name = 'paras.py'
	else:
		paras_file_name = sys.argv[1]

	# Read parameter file
	paras = read_paras(paras_file=paras_file_name)
	os.makedirs(paras['results_dir'], exist_ok=True)
	
	# Prepare signal
	b, fs, times = prepare_signal(paras)

	# Do the cwt
	cwtmatr, freqs = do_cwt(paras, b, fs)

	# Post-process and save files
	b, zz, times, freqs = post_process(paras, cwtmatr, b, fs, times, freqs)

	# Do plots (or not)
	if paras['do_plots_too']:
		#paras_plots = read_paras(paras_file=paras['paras_file_plots'])
		do_plots(paras, b, zz, times, freqs)

		print ("Sometimes I can't show the image in this script for some reason.")
		print ("Fire up ./make_plot_cwt.py if you want to see an interactive version, or go and see the .png file directly.")
