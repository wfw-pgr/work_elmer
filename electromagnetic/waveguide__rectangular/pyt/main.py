import os, sys
import numpy         as np
import gmsh_api.gmsh as gmsh

# ------------------------------------------------- #
# --- [1] initialization of the gmsh            --- #
# ------------------------------------------------- #
gmsh.initialize()
gmsh.option.setNumber( "General.Terminal", 1 )
gmsh.model.add( "model" )

# ------------------------------------------------- #
# --- [2] initialize settings                   --- #
# ------------------------------------------------- #
ptsDim , lineDim , surfDim , voluDim  =  0,  1,  2, 3
pts    , line    , surf    , volu     = {}, {}, {}, {}
ptsPhys, linePhys, surfPhys, voluPhys = {}, {}, {}, {}
x_, y_, z_, lc_, tag_                 = 0, 1, 2, 3, 4

# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #

import nkGmshRoutines.generate__quadShape as gqs

lc_inner     = 0.0300

wg_a         = 0.3810
wg_b         = 0.1905
wg_L         = 1.2138478633282366

x1_wg_i      = [  0.0,   0.0,  0.0 ]
x2_wg_i      = [ wg_a,   0.0,  0.0 ]
x3_wg_i      = [ wg_a,  wg_b,  0.0 ]
x4_wg_i      = [  0.0,  wg_b,  0.0 ]

ex_delta     = [  0.0,   0.0, wg_L ]

ret1         = gqs.generate__quadShape( lc=lc_inner, defineVolu=True, extrude_delta=ex_delta, \
                                        x1=x1_wg_i , x2=x2_wg_i, \
                                        x3=x3_wg_i , x4=x4_wg_i, recombine=False )


# ------------------------------------------------- #
# --- [4] attribute physical number             --- #
# ------------------------------------------------- #

import nkGmshRoutines.load__physNumTable as pnt
pnt.load__physNumTable( inpFile="physNumTable.dat", line=line, surf=surf )


# ------------------------------------------------- #
# --- [5] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

