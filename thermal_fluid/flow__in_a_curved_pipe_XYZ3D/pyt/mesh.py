import numpy as np
import os, sys
import gmsh

# ========================================================= #
# ===  make__geometry                                   === #
# ========================================================= #

def make__geometry( dimtags={} ):

    surfDim, voluDim = 2, 3
    
    # ------------------------------------------------- #
    # --- [1] parameter                             --- #
    # ------------------------------------------------- #
    radius_1    = 0.1
    radius_2    = 0.08
    radius_3    = 0.15
    heater_s    = 0.30
    heater_e    = 0.70
    angle       = 90.0 * np.pi/180.0
    
    # ------------------------------------------------- #
    # --- [2] design pipe1                          --- #
    # ------------------------------------------------- #
    cylinder_1s = gmsh.model.occ.addCylinder( 0,0,0, 1.0, 0,0, radius_1 )
    disk_1      = gmsh.model.occ.addDisk( 1,0,0, radius_1, radius_1 )
    rotate      = gmsh.model.occ.rotate( [(surfDim,disk_1)], 1,0,0, 0,1,0, angle )
    revolve_1   = gmsh.model.occ.revolve( [(surfDim,disk_1)],  1,1,0,  0,0,1,  angle )
    cylinder_1e = gmsh.model.occ.addCylinder( 2,1,0,  0,1,0,  radius_1 )
    object_1    = [ (dim,tag) for dim,tag in revolve_1 if ( dim == 3 ) ]
    tools_1     = [ (voluDim,cylinder_1s), (voluDim,cylinder_1e) ]
    gmsh.model.occ.synchronize()
    pipe1,maps  = gmsh.model.occ.fuse( object_1, tools_1, removeObject=True, removeTool=True )
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] design pipe2                          --- #
    # ------------------------------------------------- #
    cylinder_2s = gmsh.model.occ.addCylinder( 0,0,0, 1.0, 0,0, radius_2 )
    disk_2      = gmsh.model.occ.addDisk( 1,0,0, radius_2, radius_2 )
    rotate      = gmsh.model.occ.rotate( [(surfDim,disk_2)], 1,0,0, 0,1,0, angle )
    revolve_2   = gmsh.model.occ.revolve( [(surfDim,disk_2)],  1,1,0,  0,0,1,  angle )
    cylinder_2e = gmsh.model.occ.addCylinder( 2,1,0,  0,1,0,  radius_2 )
    object_2    = [ (dim,tag) for dim,tag in revolve_2 if ( dim == 3 ) ]
    tools_2     = [ (voluDim,cylinder_2s), (voluDim,cylinder_2e) ]
    gmsh.model.occ.synchronize()
    pipe2,maps  = gmsh.model.occ.fuse( object_2, tools_2, removeObject=True, removeTool=True  )
    gmsh.model.occ.synchronize()

    pipe1,maps  = gmsh.model.occ.cut ( pipe1, pipe2, removeObject=True, removeTool=False )
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [4] design heater                         --- #
    # ------------------------------------------------- #
    length      = heater_e - heater_s
    cylinder_3o = gmsh.model.occ.addCylinder( heater_s,0,0, length, 0,0, radius_3 )
    cylinder_3i = gmsh.model.occ.addCylinder( heater_s,0,0, length, 0,0, radius_1 )
    heater,maps = gmsh.model.occ.cut( [(voluDim,cylinder_3o)], [(voluDim,cylinder_3i)], \
                                      removeObject=True, removeTool=True )
    gmsh.model.occ.synchronize()
    
    # ------------------------------------------------- #
    # --- [3] register dimtags                      --- #
    # ------------------------------------------------- #
    dimtags["pipe"]           = pipe1
    dimtags["fluid"]          = pipe2
    dimtags["heater"]         = heater
    dimtags["inlet"]          = [(2,9)]
    dimtags["outlet"]         = [(2,10)]
    dimtags["inner_pipe"]     = [(2,6),(2,7),(2,8)]
    dimtags["outer_pipe"]     = [(2,23),(2,24),(2,25),(2,26)]
    dimtags["pipeEnd_inlet"]  = [(2,27)]
    dimtags["pipeEnd_outlet"] = [(2,28)]
    dimtags["heater_contact"] = [(2,19)]
    dimtags["heater_surface"] = [(2,20),(2,21),(2,22)]
    
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
    sample__model = "make"     #  -- [ "import" / "make" ] --  #

    if   ( sample__model == "import" ):
        dimtagsFile = None
        stpFile     = "msh/model.stp"
        import nkGmshRoutines.import__stepFile as isf
        dimtags     = isf.import__stepFile( inpFile=stpFile, dimtagsFile=dimtagsFile )
        
    elif ( sample__model == "make"   ):
        dimtags = {}
        dimtags = make__geometry( dimtags=dimtags )
        gmsh.model.occ.synchronize()
    
    gmsh.model.occ.synchronize()
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()

    # ------------------------------------------------- #
    # --- [3] Mesh settings                         --- #
    # ------------------------------------------------- #
    mesh_from_config = True         # from nkGMshRoutines/test/mesh.conf, phys.conf
    uniform_size     = 0.05
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

