import numpy as np
import os, sys
import gmsh
import nkGmshRoutines.geometrize__fromTable as geo
import nkGmshRoutines.boolean__fromTable  as bol
import nkGmshRoutines.load__dimtags as ldt


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
    bdrFile = "dat/boundary.json"
    dimtags = geo.geometrize__fromTable( inpFile=inpFile, dimtags=dimtags )
    dimtags = ldt.load__dimtags( dimtags=dimtags, inpFile=bdrFile )
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()

    fluid_bdr            = gmsh.model.getBoundary( dimtags["fluid"] )
    dimtags["fluid_bdr"] = list( set( fluid_bdr ) - set( dimtags["inlet"] ) \
                                 - set( dimtags["outlet"] ) )

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = True            # from nkGMshRoutines/test/mesh.conf, phys.conf
    uniform_size     = 0.05
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
    gmsh.model.mesh.generate(2)
    gmsh.write( "msh/model.msh" )
    gmsh.finalize()

