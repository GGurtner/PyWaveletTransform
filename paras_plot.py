import sys as _sys

# Folder to put the results in (relative or absolute path)
# Put '.' to put it where the script is.
results_dir = 'results'

# Input file (can an absolute or relative path)
input_file = 'results/cup.pic'

# Figure size
figure_size = (20, 10)

# colormap to use
cmap = 'hot'

# log scale for y?
ylog = True

# Show plot?
show_plot = True

# Output file name
output_file = 'cup.png'

# dpi
dpi = 150

#### DO NOT MODIFY THIS !!!! #####
paras = {k:v for k,v in vars().items() if k[:1]!='_' and k!='version' and k!='Paras' and not k in [key for key in locals().keys()
           if key in locals().keys() and isinstance(locals()[key], type(_sys)) and not key.startswith('__')]}