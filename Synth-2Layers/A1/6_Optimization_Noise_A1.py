# Testing optimization with noise case A1

import pygimli as pg
import numpy as np
import sys
sys.path.insert(1, '../../src')

from EM1D import EMf_2Lay_Opt_HVP

# Import the conductivities and thicknesses used to create the LU table
conds = np.load('../data/conds.npy')
thick = np.load('../data/thicks.npy')

# Load survey parameters
survey = np.load('../data/survey_2Lay.npy', allow_pickle=True).item()
offsets = survey['offsets']
height = survey['height']
freq = survey['freq']
lambd = survey['lambd']
filt = survey['filt']

# Import true models and data 
model = np.load('data/model_synth_2Lay_A1.npy')

# Data array for all the 1D stitched models
data = np.load('data/data_synth_2Lay_A1.npy')
npos = len(data) # number of positions

# Load data with added noise
data_noise_2 = np.load('data/data_A1_n2.npy')
data_noise_5 = np.load('data/data_A1_n5.npy')
data_noise_10 = np.load('data/data_A1_n10.npy')

# Optimization Q + IP noise 2.5 %
# Initialize the forward modelling class
EMf = EMf_2Lay_Opt_HVP(lambd, height, offsets, freq, filt)

# Create inversion
invEM = pg.Inversion()
invEM.setForwardOperator(EMf)

# Relative error array
error = 1e-3 # introduce here the error you want to test
relativeError = np.ones_like(data[0]) * error
model_noise_2 = np.zeros_like(model)

# Start inversion
# Perform inversion for each 1D model per position in stitched section
for pos in range(npos):
    model_est_pos = invEM.run(data_noise_2[pos], relativeError, verbose=False)
    model_noise_2[pos] = model_est_pos
    
# Optimization Q + IP noise 5 %
# Initialize the forward modelling class
EMf = EMf_2Lay_Opt_HVP(lambd, height, offsets, freq, filt)

# Create inversion
invEM = pg.Inversion()
invEM.setForwardOperator(EMf)

model_noise_5 = np.zeros_like(model)

# Start inversion
# Perform inversion for each 1D model per position in stitched section
for pos in range(npos):
    model_est_pos = invEM.run(data_noise_5[pos], relativeError, verbose=False)
    model_noise_5[pos] = model_est_pos
    
# Optimization Q + IP noise 10 %
# Initialize the forward modelling class
EMf = EMf_2Lay_Opt_HVP(lambd, height, offsets, freq, filt)

# Create inversion
invEM = pg.Inversion()
invEM.setForwardOperator(EMf)

model_noise_10 = np.zeros_like(model)

# Start inversion
# Perform inversion for each 1D model per position in stitched section
for pos in range(npos):
    model_est_pos = invEM.run(data_noise_10[pos], relativeError, verbose=False)
    model_noise_10[pos] = model_est_pos
    
# Save estimates
np.save('results/model_2Lay_A1_Opt_n2', model_noise_2)
np.save('results/model_2Lay_A1_Opt_n5', model_noise_5)
np.save('results/model_2Lay_A1_Opt_n10', model_noise_10)

