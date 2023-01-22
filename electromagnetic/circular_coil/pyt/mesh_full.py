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

lc_coil        = 0.02
lc_roi         = 0.05
lc_sim         = 1.00

simBoundary__r = 5.0
simBoundary__z = 5.0
roiBoundary__r = 1.0
roiBoundary__z = 1.0

rCoil1         = 0.45
rCoil2         = 0.55

th1            =   0.0
th2            = 180.0
gap            =  0.20
hCoil          =  0.10

ret1 = fan.generate__fanShape   ( lc=lc_coil, r1=rCoil1, r2=rCoil2, th1=th1, th2=th2, \
                                  zoffset=+gap, height=+hCoil, defineVolu=True, side="+" )
ret2 = fan.generate__fanShape   ( lc=lc_coil, r1=rCoil1, r2=rCoil2, th1=th1, th2=th2, \
                                  zoffset=+gap, height=+hCoil, defineVolu=True, side="-" )
ret3 = fan.generate__fanShape   ( lc=lc_coil, r1=rCoil1, r2=rCoil2, th1=th1, th2=th2, \
                                  zoffset=-gap, height=-hCoil, defineVolu=True, side="+" )
ret4 = fan.generate__fanShape   ( lc=lc_coil, r1=rCoil1, r2=rCoil2, th1=th1, th2=th2, \
                                  zoffset=-gap, height=-hCoil, defineVolu=True, side="-" )

ret5 = fan.generate__fanShape   ( lc=lc_roi , r1=0.0, r2=roiBoundary__r, th1=th1, th2=th2, \
                                  zoffset=-roiBoundary__z, height=2.0*roiBoundary__z, \
                                  defineVolu=True, side="+" )
ret6 = fan.generate__fanShape   ( lc=lc_roi , r1=0.0, r2=roiBoundary__r, th1=th1, th2=th2, \
                                  zoffset=-roiBoundary__z, height=2.0*roiBoundary__z, \
                                  defineVolu=True, side="-" )
ret7 = fan.generate__fanShape   ( lc=lc_sim , r1=0.0, r2=simBoundary__r, th1=th1, th2=th2, \
                                  zoffset=-simBoundary__z, height=2.0*simBoundary__z, \
                                  defineVolu=True, side="+" )
ret8 = fan.generate__fanShape   ( lc=lc_sim , r1=0.0, r2=simBoundary__r, th1=th1, th2=th2, \
                                  zoffset=-simBoundary__z, height=2.0*simBoundary__z, \
                                  defineVolu=True, side="-" )

gmsh.model.occ.addPoint( 0.0, 0.0, 0.0, meshSize=lc_coil )
gmsh.model.occ.removeAllDuplicates()

volu["coil_upr1"] = ret1["volu"]["fan"]
volu["coil_upr2"] = ret2["volu"]["fan"]
volu["coil_lwr1"] = ret3["volu"]["fan"]
volu["coil_lwr2"] = ret4["volu"]["fan"]
volu["roi_Area1"] = ret5["volu"]["fan"]
volu["roi_Area2"] = ret6["volu"]["fan"]
volu["sim_Area1"] = ret7["volu"]["fan"]
volu["sim_Area2"] = ret8["volu"]["fan"]

surf["sim_top1"]  = 38
surf["sim_bot1"]  = 36
surf["sim_bot2"]  = 41
surf["sim_top2"]  = 43
surf["sim_side1"] = 37
surf["sim_side2"] = 40
surf["sim_side3"] = 44
surf["sim_side4"] = 42

surf["coil_upr_in"]   = 45
surf["coil_upr_out"]  = 46
surf["coil_lwr_in"]   = 47
surf["coil_lwr_out"]  = 48

# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
voluPhys["coil_upr1"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil_upr1"] ], tag=301 )
voluPhys["coil_upr2"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil_upr2"] ], tag=302 )
voluPhys["coil_lwr1"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil_lwr1"] ], tag=303 )
voluPhys["coil_lwr2"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil_lwr2"] ], tag=304 )
voluPhys["roi_Area1"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["roi_Area1"] ], tag=305 )
voluPhys["roi_Area2"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["roi_Area2"] ], tag=306 )
voluPhys["sim_Area1"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["sim_Area1"] ], tag=307 )
voluPhys["sim_Area2"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["sim_Area2"] ], tag=308 )

surfPhys["sim_bot1"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_bot1" ] ], tag=201 )
surfPhys["sim_bot2"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_bot2" ] ], tag=202 )
surfPhys["sim_top1"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_top1" ] ], tag=203 )
surfPhys["sim_top2"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_top2" ] ], tag=204 )
surfPhys["sim_side1"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_side1"] ], tag=205 )
surfPhys["sim_side2"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_side2"] ], tag=206 )
surfPhys["sim_side3"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_side3"] ], tag=207 )
surfPhys["sim_side4"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["sim_side4"] ], tag=208 )

surfPhys["coil_upr_in"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_upr_in" ] ], tag=209 )
surfPhys["coil_upr_out"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_upr_out"] ], tag=210 )
surfPhys["coil_lwr_in"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_lwr_in" ] ], tag=211 )
surfPhys["coil_lwr_out"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["coil_lwr_out"] ], tag=212 )

# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

