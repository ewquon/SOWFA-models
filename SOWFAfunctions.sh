# Define some functions for mesh refinement.
# Local refinement performed on one core.
refineMeshLocal()
{
   i=$1
   while [ $i -ge 1 ]
   do
      echo "   -Performing level $i local refinement with topoSet/refineHexMesh"
      echo "      *selecting cells to refine..."
      topoSet -dict system/topoSetDict.local.$i > log.topoSet.local.$i 2>&1

      echo "      *refining cells..."
      refineHexMesh local -overwrite > log.refineHexMesh.local.$i 2>&1

      let i=i-1
   done
}

# Global refinement performed in parallel.
refineMeshGlobal()
{
   i=1
   while [ $i -le $1 ]
   do
      echo "   -Performing level $i global refinement with refineMesh"
      echo "      *refining cells..."
      mpirun -np $cores refineMesh -all -parallel -overwrite > log.refineMesh.global.$i 2>&1

      let i=i+1
   done
}

