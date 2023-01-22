import numpy as np
import os, sys
import gmsh_api.gmsh as gmsh

import nkGmshRoutines.generate__quadShape  as qua
import nkGmshRoutines.generate__squareTube as tub


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
x_, y_, z_, lc_, tag_                 =  0,  1,  2,  3, 4

# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #

lc_sim     =  0.800
lc_mag     =  0.010
lc_coil    =  0.010

gap        =  0.100
Lmag       =  0.500
Lsquare    =  0.200
coil_width =  0.020

# ------------------------------------------------- #
# --- C-shaped Magnet core                      --- #
# ------------------------------------------------- #

Ledge_out  =   0.5*Lmag + 0.5*Lsquare
Ledge_inn  =   0.5*Lmag - 0.5*Lsquare
Lhalf_gap  =   0.5*gap
y_minus    = - 0.5*Lsquare

pts["x1" ] = [ -Ledge_out, y_minus, -Ledge_out, lc_mag, 0 ]
pts["x2" ] = [ +Ledge_out, y_minus, -Ledge_out, lc_mag, 0 ]
pts["x3" ] = [ +Ledge_out, y_minus, -Lhalf_gap, lc_mag, 0 ]
pts["x4" ] = [ +Ledge_inn, y_minus, -Lhalf_gap, lc_mag, 0 ]
pts["x5" ] = [ +Ledge_inn, y_minus, -Ledge_inn, lc_mag, 0 ]
pts["x6" ] = [ -Ledge_inn, y_minus, -Ledge_inn, lc_mag, 0 ]
pts["x7" ] = [ -Ledge_inn, y_minus, +Ledge_inn, lc_mag, 0 ]
pts["x8" ] = [ +Ledge_inn, y_minus, +Ledge_inn, lc_mag, 0 ]
pts["x9" ] = [ +Ledge_inn, y_minus, +Lhalf_gap, lc_mag, 0 ]
pts["x10"] = [ +Ledge_out, y_minus, +Lhalf_gap, lc_mag, 0 ]
pts["x11"] = [ +Ledge_out, y_minus, +Ledge_out, lc_mag, 0 ]
pts["x12"] = [ -Ledge_out, y_minus, +Ledge_out, lc_mag, 0 ]

# -- add points -- #
for key in list( pts.keys() ):
    pts[key][4] = gmsh.model.occ.addPoint( pts[key][0], pts[key][1], pts[key][2], meshSize=pts[key][3] )

# -- add lines  -- #
lineLoop = []
index    = [ ik+1 for ik in range(12) ] + [1]
for ik in range( len( index )-1 ):
    ik1, ik2       = index[ik], index[ik+1]
    ptkey1, ptkey2 = "x{0}".format(ik1), "x{0}".format(ik2)
    linekey        = "line_{0}_{1}".format(ik1,ik2)
    line[linekey]  = gmsh.model.occ.addLine( pts[ptkey1][tag_], pts[ptkey2][tag_] )
    lineLoop.append( line[linekey] )

# -- add surface  -- #
lineGroup          = gmsh.model.occ.addCurveLoop( lineLoop )
surf["cMag"]       = gmsh.model.occ.addPlaneSurface( [ lineGroup ] )

# -- add volume   -- #
delta              = [ 0.0, Lsquare, 0.0 ]
ret1               = gmsh.model.occ.extrude( [ (surfDim,surf["cMag"]) ], delta[0], delta[1], delta[2] )
volu["cMag"]       = ret1[1][1]


# ------------------------------------------------- #
# --- coil around magnetic core                 --- #
# ------------------------------------------------- #

coil_length  = ( Lmag - Lsquare ) * 0.6
xcent        = - 0.5*Lmag
ycent        =   0.0
d_in         =   0.5*Lsquare
d_out        =   0.5*Lsquare + coil_width
z_bot        = - 0.5*coil_length
z_top        = + 0.5*coil_length

vL1_coil_1   = [ xcent-d_out, ycent-d_out, z_bot ]
vL1_coil_2   = [ xcent-d_in , ycent-d_out, z_bot ]
vL1_coil_3   = [ xcent-d_in , ycent-d_out, z_top ]
vL1_coil_4   = [ xcent-d_out, ycent-d_out, z_top ]
delta1       = [         0.0,   2.0*d_out,   0.0 ]

vL2_coil_1   = [ xcent-d_in , ycent-d_out, z_bot ]
vL2_coil_2   = [ xcent+d_in , ycent-d_out, z_bot ]
vL2_coil_3   = [ xcent+d_in , ycent-d_out, z_top ]
vL2_coil_4   = [ xcent-d_in , ycent-d_out, z_top ]
delta2       = [         0.0,  coil_width,   0.0 ]

vL3_coil_1   = [ xcent-d_in , ycent+d_in , z_bot ]
vL3_coil_2   = [ xcent+d_in , ycent+d_in , z_bot ]
vL3_coil_3   = [ xcent+d_in , ycent+d_in , z_top ]
vL3_coil_4   = [ xcent-d_in , ycent+d_in , z_top ]
delta3       = [         0.0,  coil_width,   0.0 ]

vL4_coil_1   = [ xcent+d_in , ycent-d_out, z_bot ]
vL4_coil_2   = [ xcent+d_out, ycent-d_out, z_bot ]
vL4_coil_3   = [ xcent+d_out, ycent-d_out, z_top ]
vL4_coil_4   = [ xcent+d_in , ycent-d_out, z_top ]
delta4       = [         0.0,   2.0*d_out,   0.0 ]

ret2_1       = qua.generate__quadShape( lc=lc_coil, extrude_delta=delta1, defineVolu=True, \
                                        x1=vL1_coil_1, x2=vL1_coil_2, \
                                        x3=vL1_coil_3, x4=vL1_coil_4  )
ret2_2       = qua.generate__quadShape( lc=lc_coil, extrude_delta=delta2, defineVolu=True, \
                                        x1=vL2_coil_1, x2=vL2_coil_2, \
                                        x3=vL2_coil_3, x4=vL2_coil_4  )
ret2_3       = qua.generate__quadShape( lc=lc_coil, extrude_delta=delta3, defineVolu=True, \
                                        x1=vL3_coil_1, x2=vL3_coil_2, \
                                        x3=vL3_coil_3, x4=vL3_coil_4  )
ret2_4       = qua.generate__quadShape( lc=lc_coil, extrude_delta=delta4, defineVolu=True, \
                                        x1=vL4_coil_1, x2=vL4_coil_2, \
                                        x3=vL4_coil_3, x4=vL4_coil_4  )
volu["coil1"] = ret2_1["volu"]["quad"]
volu["coil2"] = ret2_2["volu"]["quad"]
volu["coil3"] = ret2_3["volu"]["quad"]
volu["coil4"] = ret2_4["volu"]["quad"]

# ------------------------------------------------- #
# --- simulation region                         --- #
# ------------------------------------------------- #

simulation_region = "box"

if ( simulation_region == "box" ):
    xSim    = 2.0
    ySim    = 2.0
    zSim    = 2.0

    x1_sim  = [ -xSim, -ySim,    -zSim ]
    x2_sim  = [ -xSim, +ySim,    -zSim ]
    x3_sim  = [ +xSim, +ySim,    -zSim ]
    x4_sim  = [ +xSim, -ySim,    -zSim ]
    delta   = [   0.0,   0.0, 2.0*zSim ]
    ret3    = qua.generate__quadShape( lc=lc_sim, x1=x1_sim, x2=x2_sim, x3=x3_sim, x4=x4_sim, \
                                       extrude_delta=delta, defineVolu=True )
    volu["air"] = ret3["volu"]["quad"]

elif ( simulation_region == "sphere" ):
    sph     = [ 0.0, 0.0, 0.0, 2.0 ]
    ret     = gmsh.model.occ.addSphere( sph[0], sph[1], sph[2], sph[3] )
    volu["air"] = ret

    
# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #

gmsh.model.occ.removeAllDuplicates()

farBCs  = [ 28, 29, 30, 31, 32, 33 ]

gmsh.model.occ.synchronize()
voluPhys["cMag"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["cMag"] ], tag=301 )
voluPhys["coil"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil1"], volu["coil2"], \
                                                           volu["coil3"], volu["coil4"] ], tag=302 )
voluPhys["air"]  = gmsh.model.addPhysicalGroup( voluDim, [ volu["air"]  ], tag=303 )

surfPhys["far"]  = gmsh.model.addPhysicalGroup( surfDim, farBCs, tag=201 )

# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

