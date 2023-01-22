import numpy as np
import os, sys
import gmsh
# import gmsh_api.gmsh as gmsh

# ------------------------------------------------- #
# --- [1] initialization of the gmsh            --- #
# ------------------------------------------------- #
gmsh.initialize()
gmsh.option.setNumber( "General.Terminal", 1 )
gmsh.model.add( "model" )


# ------------------------------------------------- #
# --- [2] initialize settings                   --- #
# ------------------------------------------------- #
ptsDim , lineDim , surfDim , voluDim  =  0,  1,  2,  3
pts    , line    , surf    , volu     = {}, {}, {}, {}
ptsPhys, linePhys, surfPhys, voluPhys = {}, {}, {}, {}
x_, y_, z_, lc_, tag_                 = 0, 1, 2, 3, 4


# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #

import nkGmshRoutines.generate__quadShape as gqs

lc_sim       = 0.30
lc_coil      = 0.02

yplain       = 0.0
xSimLeng     = 5.0
zSimLeng     = 5.0

x1_sim       = [      0.0,  0.0, -zSimLeng ]
x2_sim       = [ xSimLeng,  0.0, -zSimLeng ]
x3_sim       = [ xSimLeng,  0.0, +zSimLeng ]
x4_sim       = [      0.0,  0.0, +zSimLeng ]

coil_xpos    = 0.6
coil_xwdt    = 0.1
coil_zpos    = 0.3
coil_zwdt    = 0.1

x1_coil_p    = [ coil_xpos-coil_xwdt,  0.0, +coil_zpos-coil_zwdt ]
x2_coil_p    = [ coil_xpos+coil_xwdt,  0.0, +coil_zpos-coil_zwdt ]
x3_coil_p    = [ coil_xpos+coil_xwdt,  0.0, +coil_zpos+coil_zwdt ]
x4_coil_p    = [ coil_xpos-coil_xwdt,  0.0, +coil_zpos+coil_zwdt ]

x1_coil_n    = [ coil_xpos-coil_xwdt,  0.0, -coil_zpos-coil_zwdt ]
x2_coil_n    = [ coil_xpos+coil_xwdt,  0.0, -coil_zpos-coil_zwdt ]
x3_coil_n    = [ coil_xpos+coil_xwdt,  0.0, -coil_zpos+coil_zwdt ]
x4_coil_n    = [ coil_xpos-coil_xwdt,  0.0, -coil_zpos+coil_zwdt ]

ret1         = gqs.generate__quadShape( lc=lc_sim , x1=x1_sim, x2=x2_sim, x3=x3_sim, x4=x4_sim )
ret2         = gqs.generate__quadShape( lc=lc_coil, x1=x1_coil_p, x2=x2_coil_p, \
                                        x3=x3_coil_p, x4=x4_coil_p )
ret3         = gqs.generate__quadShape( lc=lc_coil, x1=x1_coil_n, x2=x2_coil_n, \
                                        x3=x3_coil_n, x4=x4_coil_n )

gmsh.model.occ.removeAllDuplicates()

import load__physNumTable as pnt

pnt.load__physNumTable( inpFile="physNumTable.dat", line=line, surf=surf )

# import nkUtilities.load__constants as lcn
# const        = lcn.load__constants( inpFile="physNumTable.dat" )

# for key in const.keys():
#     surf[key] = const[key]

print( surf )
print( line )

# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
surfPhys["air"]   = gmsh.model.addPhysicalGroup( surfDim, [ surf["air"  ] ], tag=201 )
surfPhys["coil+"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil+"] ], tag=202 )
surfPhys["coil-"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil-"] ], tag=203 )
linePhys["air1"]  = gmsh.model.addPhysicalGroup( lineDim, [ line["air1" ] ], tag=101 )
linePhys["air2"]  = gmsh.model.addPhysicalGroup( lineDim, [ line["air2" ] ], tag=102 )
linePhys["air3"]  = gmsh.model.addPhysicalGroup( lineDim, [ line["air3" ] ], tag=103 )
linePhys["air4"]  = gmsh.model.addPhysicalGroup( lineDim, [ line["air4" ] ], tag=104 )

# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

