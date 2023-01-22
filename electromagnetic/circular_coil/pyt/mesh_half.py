import numpy as np
import os, sys
import gmsh

gmshlib = os.environ["gmshLibraryPath"]
sys.path.append( gmshlib )

import generate__fanShape    as fan
import generate__sectorShape as sct

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
lc                                    = 10.0
x_, y_, z_, lc_, tag_                 = 0, 1, 2, 3, 4


# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #

lc_coil        =   0.02
lc_roi         =   0.05
lc_sim         =   1.0

simBoundary__r = 5.0
simBoundary__z = 5.0
roiBoundary__r = 1.0
roiBoundary__z = 1.0

rCoil1         =  0.45
rCoil2         =  0.55

th1            =   0.0
th2            = 180.0
gap            =  0.20
hCoil          =  0.10

ret1 = fan.generate__fanShape   ( lc=lc_coil, r1=rCoil1, r2=rCoil2, th1=th1, th2=th2, \
                                  zoffset=+gap, height=+hCoil, defineVolu=True )
ret2 = fan.generate__fanShape   ( lc=lc_coil, r1=rCoil1, r2=rCoil2, th1=th1, th2=th2, \
                                  zoffset=-gap, height=-hCoil, defineVolu=True )

ret3 = fan.generate__fanShape   ( lc=lc_roi , r1=0.0, r2=roiBoundary__r, th1=th1, th2=th2, \
                                  zoffset=-roiBoundary__z, height=2.0*roiBoundary__z, \
                                  defineVolu=True )
ret4 = fan.generate__fanShape   ( lc=lc_sim , r1=0.0, r2=simBoundary__r, th1=th1, th2=th2, \
                                  zoffset=-simBoundary__z, height=2.0*simBoundary__z, \
                                  defineVolu=True )
gmsh.model.occ.addPoint( 0.0, 0.0, 0.0, meshSize=lc_coil  )
gmsh.model.occ.removeAllDuplicates()

volu["coil_upr"] = ret1["volu"]["fan"]
volu["coil_lwr"] = ret2["volu"]["fan"]
volu["roi_Area"] = ret3["volu"]["fan"]
volu["sim_Area"] = ret4["volu"]["fan"]

surf["coil_upr_in"]   = 4
surf["coil_upr_out"]  = 7
surf["coil_lwr_in"]   = 12
surf["coil_lwr_out"]  = 15

surf["sim_bot"]       = 24
surf["sim_side1"]     = 25
surf["sim_top"]       = 26
surf["sim_side2"]     = 28

surf["x=0_roi1"]      = 17
surf["x=0_roi2"]      = 18
surf["x=0_sim1"]      = 23
surf["x=0_sim2"]      = 27


# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
voluPhys["coil_upr"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil_upr"] ], tag=301 )
voluPhys["coil_lwr"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil_lwr"] ], tag=302 )
voluPhys["roi_Area"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["roi_Area"] ], tag=303 )
voluPhys["sim_Area"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["sim_Area"] ], tag=304 )


surfPhys["sim_bot"]      = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_bot"     ] ], tag=201 )
surfPhys["sim_top"]      = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_top"     ] ], tag=202 )
surfPhys["sim_side1"]    = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_side1"   ] ], tag=203 )
surfPhys["sim_side2"]    = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_side2"   ] ], tag=204 )

surfPhys["coil_upr_in"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_upr_in" ] ], tag=205 )
surfPhys["coil_upr_out"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_upr_out"] ], tag=206 )
surfPhys["coil_lwr_in"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_lwr_in" ] ], tag=207 )
surfPhys["coil_lwr_out"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_lwr_out"] ], tag=208 )

surfPhys["x=0_roi1"]     = gmsh.model.addPhysicalGroup( surfDim, [ surf["x=0_roi1"    ] ], tag=209 )
surfPhys["x=0_roi2"]     = gmsh.model.addPhysicalGroup( surfDim, [ surf["x=0_roi2"    ] ], tag=210 )
surfPhys["x=0_sim1"]     = gmsh.model.addPhysicalGroup( surfDim, [ surf["x=0_sim1"    ] ], tag=211 )
surfPhys["x=0_sim2"]     = gmsh.model.addPhysicalGroup( surfDim, [ surf["x=0_sim2"    ] ], tag=212 )


# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

