import numpy as np
import sys
import gmsh


# ------------------------------------------------- #
# --- [1] initialization of the gmsh            --- #
# ------------------------------------------------- #
gmsh.initialize()
gmsh.option.setNumber( "General.Terminal", 1 )
gmsh.model.add( "model" )

# ------------------------------------------------- #
# --- [2] rectangular box model                 --- #
# ------------------------------------------------- #
lineDim , surfDim , voluDim  =  1,  2,  3
xc, yc, zc = 0.0 , 0.0, 0.0
dx, dy     = 0.05, 0.3
ret        = gmsh.model.addRectangular( xc, yc, zc, dx, dy )
dimtags    = { "bar":[(surfDim,ret)] }
gmsh.model.occ.synchronize()


# ------------------------------------------------- #
# --- [3] Physical Grouping                     --- #
# ------------------------------------------------- #
uniform = True
if ( uniform ):
    
else:    
    surfPhys["bar"]  = gmsh.model.addPhysicalGroup( surfDim, [ dimtags["bar"][1] ], tag=201 )
    surfPhys["bot"]  = gmsh.model.addPhysicalGroup( lineDim, [ 1 ], tag=101 )
    surfPhys["top"]  = gmsh.model.addPhysicalGroup( lineDim, [ 2 ], tag=102 )


# ------------------------------------------------- #
# --- [4] meshing & save file                   --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write( "model.msh" )
gmsh.finalize()

