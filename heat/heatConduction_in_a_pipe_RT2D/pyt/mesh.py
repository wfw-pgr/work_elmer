import numpy as np
import os, sys
import gmsh

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__geometry( dimtags={} ):

    xc, yc, zc = 0.0, 0.0, 0.0
    r1, r2, r3 = 0.2, 0.8, 1.0
    disk1      = gmsh.model.occ.addDisk( xc, yc, zc, r1, r1 )
    disk2      = gmsh.model.occ.addDisk( xc, yc, zc, r2, r2 )
    disk3      = gmsh.model.occ.addDisk( xc, yc, zc, r3, r3 )
    disk1      = [(2,disk1)]
    disk2      = [(2,disk2)]
    disk3      = [(2,disk3)]
    disk3,bmap = gmsh.model.occ.cut( disk3, disk2, removeObject=True, removeTool=False )
    disk2,bmap = gmsh.model.occ.cut( disk2, disk1, removeObject=True, removeTool=False )
    dimtags["outer"]   = disk3
    dimtags["gap"]     = disk2
    dimtags["inner"]   = disk1
    dimtags["circle1"] = [(1,1)]
    dimtags["circle2"] = [(1,2)]
    dimtags["circle3"] = [(1,3)]
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
    gmsh.model.occ.synchronize()
    
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = True         # from nkGMshRoutines/test/mesh.conf, phys.conf
    uniform_size     = 0.1
    if ( mesh_from_config ):
        meshFile = "dat/mesh.conf"
        physFile = "dat/phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, \
                                       dimtags=dimtags, target="surf" )
    else:
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( uniform=uniform_size, dimtags=dimtags )

    # ------------------------------------------------- #
    # --- [4] post process                          --- #
    # ------------------------------------------------- #
    gmsh.model.occ.synchronize()
    gmsh.model.mesh.generate(3)
    gmsh.write( "msh/model.msh" )
    gmsh.finalize()

