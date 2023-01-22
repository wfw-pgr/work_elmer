import numpy as np
import os, sys
import gmsh

gmshlib = os.environ["gmshLibraryPath"]
sys.path.append( gmshlib )
import generate__quadShape as qua
import generate__cylinder  as cyl

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
lc                                    = 0.2
x_, y_, z_, lc_, tag_                 = 0, 1, 2, 3, 4

# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #

zLeng   =   5.0
wire_r  =   0.3
sim__r  =   3.0

xc      = [    0.0,    0.0,   0.0 ]
delta   = [    0.0,    0.0, zLeng ]

lc_sim  = 0.50
lc_wire = 0.05

ret          = cyl.generate__cylinder ( lc=lc_sim, xc=xc, radius=sim__r, \
                                        defineVolu=True, extrude_delta=delta )
volu["Air"]  = ret["volu"]["cylinder"]

ret          = cyl.generate__cylinder ( lc=lc_wire, xc=xc, radius=wire_r, \
                                        defineVolu=True, extrude_delta=delta )
volu["wire"] = ret["volu"]["cylinder"]
gmsh.model.occ.removeAllDuplicates()

volu["wire"]     = 2
volu["Air"]      = 3

surf["wireIn"]   = 4
surf["wireOut"]  = 6
surf["wireSide"] = 5
surf["AirIn"]    = 8
surf["AirOut"]   = 9
surf["AirSide"]  = 7

# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
surfPhys["wireIn"]   = gmsh.model.addPhysicalGroup( surfDim, [ surf["wireIn"] ]  , tag=201 )
surfPhys["wireSide"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["wireSide"] ], tag=202 )
surfPhys["wireOut"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["wireOut"] ] , tag=203 )
surfPhys["AirIn"]    = gmsh.model.addPhysicalGroup( surfDim, [ surf["AirIn"] ]   , tag=204 )
surfPhys["AirSide"]  = gmsh.model.addPhysicalGroup( surfDim, [ surf["AirSide"] ] , tag=205 )
surfPhys["AirOut"]   = gmsh.model.addPhysicalGroup( surfDim, [ surf["AirOut"] ]  , tag=206 )

voluPhys["wire"]     = gmsh.model.addPhysicalGroup( voluDim, [ volu["wire"] ]    , tag=301 )
voluPhys["Air"]      = gmsh.model.addPhysicalGroup( voluDim, [ volu["Air"] ]     , tag=302 )


# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

