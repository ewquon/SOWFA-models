#!/usr/bin/env python
import sys,os
import numpy as np
import matplotlib.pyplot as plt
# depends on https://github.com/NWTC/datatools
from datatools.SOWFA.postProcessing.sourceHistory import SourceHistory


if len(sys.argv) <= 2:
    sys.exit('Need to specify precursor directory and start time')
precdir = sys.argv[1]
startTime = float(sys.argv[2])

srchist = SourceHistory(os.path.join(precdir,'postProcessing','SourceHistory'))

if not np.all(srchist.UZ == 0):
    print('Note: z-momentum source non-zero')

if startTime >= srchist.t[-1]:
    print('Warning: specified start time exceeds source history!')
    startTime = 0.

tmin,tmax = np.min(srchist.t), np.max(srchist.t)
inrange = np.where(srchist.t >= startTime)
UXmean = np.mean(srchist.UX[inrange])
UYmean = np.mean(srchist.UY[inrange])
UZmean = np.mean(srchist.UZ[inrange])

print('({:g} {:g} {:g})'.format(UXmean,UYmean,UZmean))

outpath = os.path.join('{:g}'.format(startTime), 'uniform', 'gradP.raw')
if os.path.isfile(outpath):
    print('NOTE:',outpath,'already exists; will not overwrite.')
    with open(outpath,'r') as f:
        print('From file:',f.readline())
else:
    outdir = os.path.dirname(outpath)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    with open(outpath,'w') as f:
        f.write(('({:g} {:g} {:g})'.format(UXmean,UYmean,UZmean)))
    print('Wrote',outpath)


fig,ax = plt.subplots(nrows=2, sharex=True, figsize=(8,6))
ax[0].plot(srchist.t, srchist.UX, label='precursor')
ax[1].plot(srchist.t, srchist.UY)
ax[0].axhline(UXmean, color='k', ls='--', label='estimated')
ax[1].axhline(UYmean, color='k', ls='--')
ax[0].axvspan(tmin, startTime, color='0.5', alpha=0.5)
ax[1].axvspan(tmin, startTime, color='0.5', alpha=0.5)
ax[0].set_xlim((tmin,tmax))
ax[0].set_ylabel('UX')
ax[1].set_ylabel('UY')
ax[0].legend(loc='best')
ax[-1].set_xlabel('simulation time [s]')
fig.savefig(os.path.join('constant','gradP.png'), bbox_inches='tight')
plt.show()

