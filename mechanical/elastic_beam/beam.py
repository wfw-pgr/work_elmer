import numpy as np
import sys
import gmsh

gmshlib = "/Users/kent/gmsh/pygmshLibrary/"
sys.path.append( gmshlib )
import generateRectangularBox as box

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
lc                                    = 0.01

# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #
v0  = [    0.0,   0.0,   0.0   ]
v1  = [    1.0,   0.0,   0.0   ]
v2  = [    0.0,   0.1,   0.0   ]
v3  = [    0.0,   0.0,   0.030 ]
ret = box.generateRectangularBox( origin=v0, v1=v1, v2=v2, v3=v3, lc=lc )
lft = ret["surfs"]["side2"]
rgt = ret["surfs"]["side4"]
bot = ret["surfs"]["bottom"]
box = ret["volus"]["box"]

# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
surfPhys["fixed"] = gmsh.model.addPhysicalGroup( surfDim, [ lft ], tag=201 )
surfPhys["free" ] = gmsh.model.addPhysicalGroup( surfDim, [ rgt ], tag=202 )
surfPhys["bot"  ] = gmsh.model.addPhysicalGroup( surfDim, [ bot ], tag=203 )
voluPhys["box"  ] = gmsh.model.addPhysicalGroup( voluDim, [ box ], tag=301 )

# ------------------------------------------------- #
# --- [5] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

