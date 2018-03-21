#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use this file like this:
./make_plot_cwt.py my_paras.py
or this:
./make_plot_cwt.py
to produce the plot of the cwt of a signal, stored in a pickle file.
Parameters are read from the corresponding my_paras.py file
or the default paras.py file in the second case.
"""

import os
import sys
from os.path import join as jn
import pickle
import imp
from matplotlib.colors import LightSource, Normalize, LogNorm
from matplotlib import colors, ticker, cm
import matplotlib.gridspec as gridspec
from pylab import *

def read_paras(paras_file=None, post_process=None):
	"""
	Reads parameter file for a single simulation.    
	"""

	if paras_file==None:
		import my_paras as paras_mod
	else:
		paras_mod = imp.load_source("paras", paras_file)

	paras = paras_mod.paras

	if post_process!=None:
		paras = post_process_paras(paras)

	return paras

def get_data(paras):
	with open(paras['input_file_pic'], 'rb') as f:
			b, zz, times, freqs = pickle.load(f)

	return b, zz, times, freqs

def do_plots(paras, b, zz, times, freqs):
	fig = figure(figsize=paras['figure_size'])
	gs = gridspec.GridSpec(2, 1, width_ratios=[1], height_ratios=[3, 1])

	ax1 = subplot(gs[0])
	ax2 = subplot(gs[1], sharex=ax1)

	ax1.pcolormesh(times, freqs, zz, cmap=paras['cmap'])
	if paras['log_scale']:
		ax1.set_yscale('log')

	ax2.plot(times, b)

	print ('Saving .png file as:', jn(paras['results_dir'], paras['output_png']))
	savefig(jn(paras['results_dir'], paras['output_png']), dpi=paras['dpi'])

	if paras['show_plot']:
		show()	

if __name__=='__main__':
	if len(sys.argv)<2:
		print("You did not specify a paras file, I try to use: paras_plot.py")
		paras_file_name = 'paras.py'
	else:
		paras_file_name = sys.argv[1]

	# Read parameter file
	paras = read_paras(paras_file=paras_file_name)
	os.makedirs(paras['results_dir'], exist_ok=True)
	
	# Do plots
	b, zz, times, freqs = get_data(paras)
	do_plots(paras, b, zz, times, freqs)