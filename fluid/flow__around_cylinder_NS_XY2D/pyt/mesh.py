import numpy as np
import os, sys
import gmsh

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__geometry( dimtags={} ):

    Lx,Ly            =     0.2,    0.05
    x0,y0,z0         = -0.5*Lx, -0.5*Ly, 0.0
    xC,yC,zC         = -0.2*Lx,     0.0, 0.0
    rc               =  0.10*min( Lx, Ly )
    rect             = gmsh.model.occ.addRectangle( x0, y0, z0, Lx, Ly )
    circ             = gmsh.model.occ.addDisk     ( xC, yC, zC, rc, rc )
    rect             = [(2,rect)]
    circ             = [(2,circ)]
    ret, fmap        = gmsh.model.occ.cut( rect, circ, \
                                           removeObject=True, removeTool=True )
    dimtags["fluid"]  = ret
    dimtags["circle"] = [(1,5)]
    dimtags["bottom"] = [(1,6)]
    dimtags["left"]   = [(1,7)]
    dimtags["right"]  = [(1,8)]
    dimtags["top"]    = [(1,9)]
    return( dimtags )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] initialization of the gmsh            --- #
    # ------------------------------------------------- #
    gmsh.initialize()
    gmsh.option.setNumber( "General.Terminal", 1 )
    gmsh.option.setNumber( "Mesh.Algorithm"  , 5 )
    gmsh.option.setNumber( "Mesh.Algorithm3D", 4 )
    gmsh.option.setNumber( "Mesh.SubdivisionAlgorithm", 0 )
    gmsh.model.add( "model" )
    
    # ------------------------------------------------- #
    # --- [2] Modeling                              --- #
    # ------------------------------------------------- #
    dimtags = {}
    dimtags = make__geometry( dimtags=dimtags )
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = True           # from nkGMshRoutines/test/mesh.conf, phys.conf
    uniform_size     = 0.05
    if ( mesh_from_config ):
        meshFile = "dat/mesh.conf"
        physFile = "dat/phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        print( dimtags )
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, \
                                       dimtags=dimtags, target="surf" )
    else:
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( uniform=uniform_size, dimtags=dimtags )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(2)
    gmsh.write( "msh/model.msh" )
    gmsh.finalize()

