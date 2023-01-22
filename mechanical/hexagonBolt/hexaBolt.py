import numpy as np
import sys
import gmsh

gmshlib = "/Users/kent/gmsh/pygmshLibrary/"
sys.path.append( gmshlib )
import generateRectangularBox  as box
import generateXYplaneArcCurve as arc

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
lc                                    = 1.0

# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #
radius    = 13.5
zoffset   = 0.0
zWidth    = 5.0
holeRatio = 0.3
nVerts    = 6
ptskeys   = []
linekeys  = []
#  -- [3-1] hexagon -- #
for ik in range( nVerts ):
    theta    = 2.0*np.pi * float( ik ) / float( nVerts )
    hvert    = [ radius*np.cos(theta), radius*np.sin(theta), zoffset, lc ]
    key      = "vert{0:02}".format(ik+1)
    pts[key] = gmsh.model.occ.addPoint( hvert[0], hvert[1], hvert[2], meshSize=hvert[3] )
    ptskeys.append( key )
for ik in range( nVerts ):
    ik1, ik2   = ik+1, ik+2
    if ( ik2 == nVerts+1 ): ik2 = 1
    key        = "line{0:02}{0:02}".format( ik1, ik2 )
    hpt1, hpt2 = pts["vert{0:02}".format(ik1)], pts["vert{0:02}".format(ik2)]
    line[key]  = gmsh.model.occ.addLine( hpt1, hpt2 )
    linekeys.append( key )
#  -- [3-2] circle  -- #
arc1 = arc.generateXYplaneArcCurve( radius=radius*holeRatio, zoffset=zoffset, lc=lc, ysign="+" )
arc2 = arc.generateXYplaneArcCurve( radius=radius*holeRatio, zoffset=zoffset, lc=lc, ysign="-" )
#  -- [3-3] generate surface -- #
hexLineLoop  = [ line[key] for key in linekeys ]
arcLineLoop  = [ + arc1["Lines"]["line1"], + arc1["Lines"]["line2"], \
                 - arc2["Lines"]["line2"], - arc2["Lines"]["line1"] ]
hexLoopGroup = gmsh.model.occ.addCurveLoop( hexLineLoop )
arcLoopGroup = gmsh.model.occ.addCurveLoop( arcLineLoop )
surf["hexa"] = gmsh.model.occ.addPlaneSurface( [hexLoopGroup] )
surf["hole"] = gmsh.model.occ.addPlaneSurface( [arcLoopGroup] )
#  -- [3-4] cut surface -- #
ret          = gmsh.model.occ.cut( [(surfDim,surf["hexa"])], [(surfDim,surf["hole"])] )
surf["bott"] = ( ( ret[0] )[0] )[1]
#  -- [3-5] extrude and make volume -- #
dx, dy, dz   = 0.0, 0.0, zWidth
ret          = gmsh.model.occ.extrude( [(surfDim,surf["bott"])], dx, dy, dz )
surf["ceil"]  = ( ret[0] )[1]
volu["nutv"]  = ( ret[1] )[1]
for ik in range( nVerts ):
    key       = "side{0:02}".format( ik+1 )
    surf[key] = ( ret[2+ik] )[1]

# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
sides             = [ surf["side{0:02}".format( ik+1 )] for ik in range( nVerts ) ]
surfPhys["botts"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["bott"] ], tag=201 )
surfPhys["ceils"] = gmsh.model.addPhysicalGroup( surfDim, [ surf["ceil"] ], tag=202 )
surfPhys["sides"] = gmsh.model.addPhysicalGroup( surfDim, sides           , tag=203 )
voluPhys["nut"  ] = gmsh.model.addPhysicalGroup( voluDim, [ volu["nutv"] ], tag=301 )

# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(3)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

