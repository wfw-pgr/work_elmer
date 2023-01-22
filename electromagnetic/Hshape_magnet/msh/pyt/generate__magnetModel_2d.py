import os, sys
import numpy                       as np
import gmsh_api.gmsh               as gmsh
import nkUtilities.load__constants as lcn
import nkGmshRoutines.generate__polygon as ply

# ------------------------------------------------- #
# --- [1] initialization of the gmsh            --- #
# ------------------------------------------------- #
gmsh.initialize()
gmsh.option.setNumber( "General.Terminal", 1 )
gmsh.option.setNumber( "Mesh.Algorithm"  , 6 )
gmsh.option.setNumber( "Mesh.Algorithm3D", 1 )
gmsh.model.add( "model" )

# ------------------------------------------------- #
# --- [2] initialize settings                   --- #
# ------------------------------------------------- #
ptsDim , lineDim , surfDim , voluDim  =  0,  1,  2,  3
pts    , line    , surf    , volu     = {}, {}, {}, {}
ptsPhys, linePhys, surfPhys, voluPhys = {}, {}, {}, {}
x_, y_, z_, lc_, tag_                 =  0,  1,  2,  3, 4


# ------------------------------------------------- #
# --- [3] Parameter Settings                    --- #
# ------------------------------------------------- #

tolerance       = 1.e-5
const           = lcn.load__constants( inpFile   ="dat/magnet.conf" )
mesh_conf       = lcn.load__constants( inpFile   ="dat/mesh.conf"   )

lc1             = mesh_conf["volu1_mesh"]
lc4             = mesh_conf["volu4_mesh"]
lc5             = mesh_conf["volu5_mesh"]
lc6             = mesh_conf["volu6_mesh"]
lc7             = mesh_conf["volu7_mesh"]
lc8             = mesh_conf["volu8_mesh"]

z_slotDepth     = const["z_medianPlane"] + const["z_airGap1"] + const["z_coilWidth"] + const["z_airGap2"]

rPole1          = const["r_poleRadius"]
zPole1          = const["z_medianPlane"]
zPole3          = const["z_poleGapMax"]
zPole4          = z_slotDepth

rBuff1          = const["r_poleRadius"]
rBuff2          = const["r_poleRadius"]  + const["r_airGap1"]
zBuff1          = const["z_medianPlane"]
zBuff2          = z_slotDepth

rCoil1          = const["r_poleRadius"]  + const["r_airGap1"]
rCoil2          = const["r_poleRadius"]  + const["r_airGap1"] + const["r_coilWidth"]
rCoil3          = const["r_poleRadius"]  + const["r_airGap1"] + const["r_coilWidth"] + const["r_airGap2"]
zCoil1          = const["z_medianPlane"]
zCoil2          = const["z_medianPlane"] + const["z_airGap1"]
zCoil3          = const["z_medianPlane"] + const["z_airGap1"] + const["z_coilWidth"]
zCoil4          = const["z_medianPlane"] + const["z_airGap1"] + const["z_coilWidth"] + const["z_airGap2"]

rYoke1          = const["r_poleRadius"]  + const["r_airGap1"] + const["r_coilWidth"] + const["r_airGap2"]
rYoke2          = rYoke1 + const["r_yokeWidth"] - const["r_yokeCorner"]
rYoke3          = rYoke1 + const["r_yokeWidth"]
zYoke1          = const["z_medianPlane"]
zYoke2          = z_slotDepth
zYoke3          = z_slotDepth + const["z_yokeWidth"] - const["z_yokeCorner"]
zYoke4          = z_slotDepth + const["z_yokeWidth"]

rAir1           = rYoke1 + const["r_yokeWidth"] - const["r_yokeCorner"]
rAir2           = rYoke1 + const["r_yokeWidth"]
rAir3           = rYoke1 + const["r_yokeWidth"] + const["r_outAirWidth"]
zAir1           = const["z_medianPlane"]
zAir2           = z_slotDepth + const["z_yokeWidth"] - const["z_yokeCorner"]
zAir3           = z_slotDepth + const["z_yokeWidth"]
zAir4           = z_slotDepth + const["z_yokeWidth"] + const["z_outAirWidth"]

zRegen          = const["z_regenCeil"]
zPeeler         = const["z_peelerBottom"]


# ------------------------------------------------- #
# --- [4] Modeling pole                         --- #
# ------------------------------------------------- #

inpFile = "dat/pole_cs.dat"
with open( inpFile, "r" ) as f:
    rData   = np.loadtxt( f )

pole_vertex        = np.zeros( (rData.shape[0]+2,3) )
pole_vertex[:-2,:] =   rData
pole_vertex[ -2,:] = [ rPole1, 0.0, zYoke2 ]
pole_vertex[ -1,:] = [    0.0, 0.0, zYoke2 ]

ret1 = ply.generate__polygon( lc=lc1, vertex=pole_vertex )


# ------------------------------------------------- #
# --- [5] Modeling yoke                         --- #
# ------------------------------------------------- #

xY1         = [    0.0, 0.0, zYoke2 ]
xY2         = [ rPole1, 0.0, zYoke2 ]
xY3         = [ rYoke1, 0.0, zYoke2 ]
xY4         = [ rYoke1, 0.0, zYoke1 ]
xY5         = [ rYoke3, 0.0, zYoke1 ]
xY6         = [ rYoke3, 0.0, zYoke3 ]
xY7         = [ rYoke2, 0.0, zYoke4 ]
xY8         = [    0.0, 0.0, zYoke4 ]
yoke_vertex = np.array( [ xY1, xY2, xY3, xY4, xY5, xY6, xY7, xY8 ] )

ret2        = ply.generate__polygon( lc=lc6, vertex=yoke_vertex )

    
# ------------------------------------------------- #
# --- [6] coil Modeling                         --- #
# ------------------------------------------------- #

xc1         = [ rCoil1, 0.0, zCoil2 ]
xc2         = [ rCoil2, 0.0, zCoil2 ]
xc3         = [ rCoil2, 0.0, zCoil3 ]
xc4         = [ rCoil1, 0.0, zCoil3 ]
coil_vertex = np.array( [ xc1, xc2, xc3, xc4 ] )

ret3        = ply.generate__polygon( lc=lc5, vertex=coil_vertex )


# ------------------------------------------------- #
# --- [7] simulation region                     --- #
# ------------------------------------------------- #

xS1         = [   0.0, 0.0,   0.0, lc1, 0 ] # lc1 should be used 
xS2         = [ rAir3, 0.0,   0.0, lc7, 0 ]
xS3         = [ rAir3, 0.0, zAir4, lc7, 0 ]
xS4         = [   0.0, 0.0, zAir4, lc7, 0 ]
simu_vertex = np.array( [ xS1, xS2, xS3, xS4 ] )

ret4        = ply.generate__polygon( lc=lc7, vertex=simu_vertex )


# ------------------------------------------------- #
# --- [8] remove Duplicates / physNum Grouping  --- #
# ------------------------------------------------- #
#  -- [8-1] remove Duplicates                   --  #
gmsh.model.occ.removeAllDuplicates()

#  -- [8-2] physical Grouping                   --  #

pntFile = "dat/physNumTable.conf"
import nkGmshRoutines.load__physNumTable as pnt
ret     = pnt.load__physNumTable( inpFile =pntFile , line    =line    , surf    =surf, volu=volu, \
                                  linePhys=linePhys, surfPhys=surfPhys, voluPhys=voluPhys )

# ------------------------------------------------- #
# --- [9] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
# gmsh.option.setNumber( "Mesh.BdfFieldFormat", 0 )
# gmsh.option.setNumber( "Mesh.SaveElementTagType", 2 )
# gmsh.write( "msh/model.bdf" )
gmsh.write( "msh/model.geo_unrolled" )
gmsh.write( "msh/model.msh" )
gmsh.finalize()





# Data        = np.zeros( (nData,5) )
# Data[:,0:3] = rData
# Data[:,  3] = lc1
# Data[:,  4] = 0

# polekeys = []
# for ik in range( nData ):
#     key            = "pole_{0:06}".format( ik )
#     pts[key]       = [ Data[ik,x_], Data[ik,y_], Data[ik,z_], Data[ik,lc_], Data[ik,tag_] ]
#     pts[key][tag_] = gmsh.model.occ.addPoint( pts[key][x_], pts[key][y_], pts[key][z_], \
#                                               meshSize=pts[key][lc_] )
#     polekeys.append( key )
# pts["poleRoot1"] = [ Data[ 0,x_], Data[ 0,y_], zYoke2, lc1, 0 ]
# pts["poleRoot2"] = [ Data[-1,x_], Data[-1,y_], zYoke2, lc1, 0 ]
# for key in ["poleRoot2","poleRoot1"]:
#     pts[key][tag_] = gmsh.model.occ.addPoint( pts[key][x_], pts[key][y_], pts[key][z_], \
#                                               meshSize=pts[key][lc_] )
#     polekeys.append( key )

# lineLoop = []
# keys_1   = np.roll( np.array( polekeys ),  0 )
# keys_2   = np.roll( np.array( polekeys ), -1 )
# for ik in range( keys_1.shape[0] ):
#     linekey        = "line_{0}".format( ik )
#     line[linekey]  = gmsh.model.occ.addLine( pts[keys_1[ik]][tag_], pts[keys_2[ik]][tag_] )
#     lineLoop.append( line[linekey] )

# #  -- [2-3] generate surfaces                   --  #
# lineGroup          = gmsh.model.occ.addCurveLoop( lineLoop )
# surf["quad"]       = gmsh.model.occ.addPlaneSurface( [ lineGroup ] )


# pts["xSim_1"] = [   0.0, 0.0,   0.0, lc1, 0 ]
# pts["xSim_2"] = [ rAir3, 0.0,   0.0, lc7, 0 ]
# pts["xSim_3"] = [ rAir3, 0.0, zAir4, lc7, 0 ]
# pts["xSim_4"] = [   0.0, 0.0, zAir4, lc7, 0 ]
# for ik in [ i+1 for i in range(4) ]:
#     key            = "xSim_{0}".format(ik)
#     pts[key][tag_] = gmsh.model.occ.addPoint( pts[key][x_], pts[key][y_], pts[key][z_], \
#                                               meshSize=pts[key][lc_] )

# lineLoop = []
# for ik1,ik2 in [ (1,2), (2,3), (3,4), (4,1) ]:
#     ptkey1, ptkey2 = "xSim_{0}".format(ik1), "xSim_{0}".format(ik2)
#     linekey        = "xSim_line_{0}_{1}".format(ik1,ik2)
#     line[linekey]  = gmsh.model.occ.addLine( pts[ptkey1][tag_], pts[ptkey2][tag_] )
#     lineLoop.append( line[linekey] )

# lineGroup          = gmsh.model.occ.addCurveLoop( lineLoop )
# surf["simu"]       = gmsh.model.occ.addPlaneSurface( [ lineGroup ] )


# ------------------------------------------------- #
# --- [6] Physical Grouping                     --- #
# ------------------------------------------------- #

# gmsh.model.occ.synchronize()
# voluPhys["poleGap"]    = gmsh.model.addPhysicalGroup( voluDim, [ volu["poleGap"] ] , tag=301 )
# voluPhys["poleTip"]    = gmsh.model.addPhysicalGroup( voluDim, [ volu["poleTip"] ] , tag=302 )
# voluPhys["poleBody"]   = gmsh.model.addPhysicalGroup( voluDim, [ volu["poleBody"] ], tag=303 )
# voluPhys["coilAirGap"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["airGap_inn"], volu["airGap_bot"], \
#                                                                  volu["airGap_out"], volu["airGap_upr"]  ], tag=304 )
# voluPhys["coil"]       = gmsh.model.addPhysicalGroup( voluDim, [ volu["coil"] ]    , tag=305 )
# voluPhys["yoke"]       = gmsh.model.addPhysicalGroup( voluDim, [ volu["yoke1"], volu["yoke2"], volu["yoke3"] ], tag=306 )
# voluPhys["outsideAir"] = gmsh.model.addPhysicalGroup( voluDim, [ volu["air1"], volu["air2"] ], tag=307 )

