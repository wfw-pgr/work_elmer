import numpy as np
import os, sys
import gmsh
import nkGmshRoutines.geometrize__fromTable as gft
import nkGmshRoutines.load__dimtags         as ldt

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
    inpFile = "dat/geometry.conf"
    dimtags = gft.geometrize__fromTable( inpFile=inpFile )
    inpFile = "dat/boundary.json"
    dimtags = ldt.load__dimtags( inpFile=inpFile, dimtags=dimtags )
    print( dimtags )
    
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = True          # from nkGMshRoutines/test/mesh.conf, phys.conf
    uniform_size     = 0.010
    if ( mesh_from_config ):
        meshFile = "dat/mesh.conf"
        physFile = "dat/phys.conf"
        import nkGmshRoutines.assign__meshsize as ams
        meshes = ams.assign__meshsize( meshFile=meshFile, physFile=physFile, dimtags=dimtags )
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

