import pygimli as pg
import numpy as np
import sys
sys.path.insert(1, '../../src')

from EM1D import EMf_3Lay_GSplusOpt_HVP

# Import the conductivities and thicknesses used to create the LU table
conds = np.load('../data/conds.npy')
thick = np.load('../data/thicks.npy')

# Load survey parameters
survey = np.load('../data/survey_3Lay.npy', allow_pickle=True).item()
offsets = survey['offsets']
height = survey['height']
freq = survey['freq']
lambd = survey['lambd']
filt = survey['filt']

# Data array for all the 1D stitched models
data = np.load('data/data_synth_3Lay_B1.npy')
npos = len(data) # number of positions

# Import model from Global search
model_GS = np.load('results/model_3Lay_B1_GS.npy')

# Optimization Q + IP

# Relative error array
error = 1e-3 # introduce here the error you want to test
relativeError = np.ones_like(data[0]) * error
model_est = np.zeros_like(model_GS)

# Start inversion
# Perform inversion for each 1D model per position in stitched section
for pos in range(npos):
    # Set the initial model from the global search
    m0 = model_GS[pos]
    
    # Initialize the forward modelling class
    EMf = EMf_3Lay_GSplusOpt_HVP(lambd, height, offsets, freq, filt, m0)

    # Create inversion
    invEM = pg.Inversion()
    invEM.setForwardOperator(EMf)
    
    # Setting a lower boundary of conductivities 10 mS/m
    transModel = pg.trans.TransLogLU(0.001,7) 
    invEM.modelTrans = transModel

    dataE = data[pos].copy()
    model_est_pos = invEM.run(dataE, relativeError, verbose=False)
    model_est[pos] = model_est_pos
#    if (model_est[pos, (model_est[pos,0] >1)]).any():
#        model_est[pos,0] = 1
#    if (model_est[pos, (model_est[pos,1] >1)]).any():
#        model_est[pos,1] = 1
#    if (model_est[pos, (model_est[pos,2] >1)]).any():
#        model_est[pos,2] = 1
#    if (model_est[pos, (model_est[pos,3] >10)]).any():
#        model_est[pos,3] = 10
#    if (model_est[pos, (model_est[pos,3] >10)]).any():
#        model_est[pos,4] = 10
        
np.save('results/model_3Lay_GSplusOpt_B1', model_est)