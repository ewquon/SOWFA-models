#!/usr/bin/env python
import os
import numpy as np

# depends on https://github.com/NWTC/datatools
import datatools.SOWFA.constant.boundaryData as bd

patchName = 'west'
x0 = -6000.

# get 1-D arrays
y1,z1 = bd.read_points(os.path.join('boundaryData',patchName,'points.original'))

# generate patch
y,z = np.meshgrid(y1, z1, indexing='ij')
x = x0*np.ones(y.shape)

# transformation(s)
z += 406.

# write out new points file
bd.write_points(os.path.join('boundaryData',patchName,'points'),
                x, y, z, patchName,
                fmt='%.1f', order='F')

