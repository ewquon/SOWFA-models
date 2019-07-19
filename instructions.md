# Terrain Cases

These are simulations of flow over complex terrain through a finite domain. The
starting point is a converged precursor solution (assuming stationary
conditions), assumed to have been run for 23600 s, with boundary sampling over
last hour (from t=20000 to 23600 s). The boundary data were generated using
  `$precursorPath/postProcessing/makeBoundaryDataFiles.*.sh`
to generate
  `$precursorPath/postProcessing/boundaryData`.

Dependencies:
- In order for the `constant/translateBoundaryData.py` and
  `constant/estimateGradP.py` scripts to work, the NWTC datatools python library
  is needed. This may be cloned from [here](https://github.com/NWTC/datatools).

Instructions:
1. Symbolically link the first available boundary-data time step to the restart
   time. E.g., `ln -s 20000.5 20000` where 20000 is the $startTime for the
   terrain simulation.
2. Generate an stl file of the simulated topography, which should be saved in
   `constant/triSurface/terrain.stl`. Note that the mesh motion performed in
   the preprocessing step here assumes that the precursor "inlet" boundary
   (actually a cyclic boundary) is coincident with the inlet boundary of the
   terrain-resolving mesh. It is up to the user to smooth, blend, and flatten
   the ground surface (within terrain.stl) such that the resulting mesh meets
   these requirements.
3. Set parameters within `runscript.preprocess.terrain`. Important parameters:
   - `$inletElevation` in `runscript.preprocess.terrain` to be the elevation
     of the lower edge of the inlet patch. Since the terrian has been flattened
     near the inlet, this elevation will be constant (and no boundary data
     manipulation is necessary to guarantee one-to-one face mappings between
     the generated boundaryData and the inlet mesh).
   - `$meshMotionTime` dictates the maximum displacement of any point of the
     mesh. Since the velocity in `0.original.meshMotion/pointDisplacement` is
     10 by default, the mesh motion time should be greater than the maximum
     difference in surface elevation, relative to $inletElevation, divided by
     10.
4. Run *in parallel* `runscript.preprocess.terrain`. Among other things, this
   script will:
   - Translate the original precursor mesh
   - Translate the boundaryData points by the same amount
   - Optionally refine the original mesh
   - Perform the mesh motion, conformng the lower surface of the mesh to the
     terrain and redistributing points to preserve mesh quality
   - Estimate `$startTime/uniform/gradP.raw` from the precursor source history;
     check `constant/gradP.png` to verify that the estimated driving pressure 
     gradient makes sense.
5. Run `runscript.solve.*` in parallel.

