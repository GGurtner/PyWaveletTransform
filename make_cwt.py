#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from os.path import join as jn
import pywt
from scipy.io.wavfile import read

from numpy import *
from scipy import signal, ndimage
from stl_tools import numpy2stl
import pickle
from pylab import *
import matplotlib.image as mpimg

from plot_cwt import do_plots, read_paras

def prepare_signal(paras):
	a = read(paras['input_file'])
	# Initial sampling frequency
	f_s_i = a[0]
	if not paras['stereo']:
		# Get mono signal
		b = a[1]
		if len(a[1])==2:
			raise Exception("You have probably passed a stereo signal. \nChoose stereo=True in the paras file")
		
		# Downsample the signal
		b = b[::paras['downsampling_signal']]

		# New sampling frequency after downsampling
		fs = a[0]/paras['downsampling_signal']

		# Array of time in seconds
		times = array(list(arange(len(b))))/fs

	else:
		raise Exception("Stereo not implemented yet...")

	# Select part of the signal:
	idx_start = next((i for i, t in enumerate(times) if t > paras['start']), -1) - 1
	idx_start = max(0, idx_start)
	if paras['end']!=-1:
		idx_end = next((i for i, t in enumerate(times) if t > paras['end']), -1)
	else:
		idx_end = -1

	if idx_start == idx_end:
		raise Exception("The signal is empty. Check the bounds ('start' and 'end')")

	b = b[idx_start:idx_end]
	times = times[idx_start:idx_end]

	print ("Selected", len(b), "points between", "{:04.2f}s and".format(times[0]), "{:04.2f}s".format(times[-1]), "at sampling frequency {:04.1f}Hz".format(fs))

	return b, fs, times

def do_cwt(paras, b, fs):
	if paras['log_scale']:
		space_gen = logspace
	else:
		space_gen = linspace

	# Choose frequencies
	freqs = array(space_gen(paras['lower_bound'], paras['upper_bound'], paras['n_freq'], base=paras['base_log']))
	
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
	if not paras['save_array'] is None:
		with open(jn(paras['results_dir'], paras['save_array']), 'wb') as f:
			pickle.dump((b, zz, times, freqs), f)

	# Save stl file
	numpy2stl(zz, jn(paras['results_dir'], paras['output_file']), **paras['stl_options']) 

	return b, zz, times, freqs

if __name__=='__main__':
	if len(sys.argv)<2:
		print("You did not specify a paras file, I try to use: paras.py")
		paras_file_name = 'paras.py'
	else:
		paras_file_name = sys.argv[1]

	# Read parameter file
	paras = read_paras(paras_file=paras_file_name)
	os.system('mkdir -p ' + paras['results_dir'])
	
	# Prepare signal
	b, fs, times = prepare_signal(paras)

	# Do the cwt
	cwtmatr, freqs = do_cwt(paras, b, fs)

	# Post-process and save files
	b, zz, times, freqs = post_process(paras, cwtmatr, b, fs, times, freqs)

	# Do plots (or not)
	if paras['do_plots_too']:
		paras_plots = read_paras(paras_file=paras['paras_file_plots'])
		do_plots(paras_plots, b, zz, times, freqs)

		print ("I can't show the image in this script for some reason.")
		print ("Fire up ./plot_cwt.py if you want to see it, or go and see your png file directly")