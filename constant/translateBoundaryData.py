#!/usr/bin/env python
import sys,os
import numpy as np

# depends on https://github.com/NWTC/datatools
import datatools.SOWFA.constant.boundaryData as bd


if len(sys.argv) <= 2:
    sys.exit('Need to specify inlet patch name and vertical offset')
patchName = sys.argv[1]
zOffset = float(sys.argv[2])

# get 1-D arrays
x0,y1,z1 = bd.read_points(os.path.join('boundaryData',patchName,'points.original'),
                          return_const=True)

# generate patch
y,z = np.meshgrid(y1, z1, indexing='ij')
x = x0*np.ones(y.shape)

# transformation(s)
z += zOffset

# write out new points file
bd.write_points(os.path.join('boundaryData',patchName,'points'),
                x, y, z, patchName,
                fmt='%.1f', order='F')

