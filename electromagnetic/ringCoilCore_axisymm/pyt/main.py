import numpy as np
import os, sys
import gmsh
# import gmsh_api.gmsh as gmsh

# ------------------------------------------------- #
# --- [1] initialization of the gmsh            --- #
# ------------------------------------------------- #
gmsh.initialize()
gmsh.option.setNumber( "General.Terminal", 1 )
gmsh.model.add( "model" )

import nkUtilities.load__constants as lcn
cnsFile = "dat/parameter.conf"
const   = lcn.load__constants( inpFile=cnsFile )

# ------------------------------------------------- #
# --- [2] Modeling                              --- #
# ------------------------------------------------- #
import nkGmshRoutines.generate__quadShape as gqs
airn_xLeng   = const["air.near.xLeng"]
airn_zLeng   = const["air.near.zLeng"]
airf_xLeng   = const["air.far.xLeng"]
airf_zLeng   = const["air.far.zLeng"]
coil_xpos    = const["coil.xpos"]
coil_zpos    = const["coil.zpos"]
coil_xwdt    = const["coil.xwdt"]
coil_zwdt    = const["coil.zwdt"]
pole_xpos    = const["pole.xpos"]
pole_xwdt    = const["pole.xwdt"]
pole_zpos    = const["pole.zpos"]
pole_zwdt    = const["pole.zwdt"]

pole_left    = max( const["pole.xpos"] - 0.5*const["pole.xwdt"], 0.0 )
pole_right   =      const["pole.xpos"] + 0.5*const["pole.xwdt"]
pole_bot     = max( const["pole.zpos"] - 0.5*const["pole.zwdt"], 0.0 )
pole_top     =      const["pole.zpos"] + 0.5*const["pole.zwdt"]

air_near     = [ [                     0.0,  0.0, -airn_zLeng              ],
                 [              airn_xLeng,  0.0, -airn_zLeng              ],
                 [              airn_xLeng,  0.0, +airn_zLeng              ],
                 [                     0.0,  0.0, +airn_zLeng              ] ]
air_far      = [ [                     0.0,  0.0, -airf_zLeng              ],
                 [              airf_xLeng,  0.0, -airf_zLeng              ],
                 [              airf_xLeng,  0.0, +airf_zLeng              ],
                 [                     0.0,  0.0, +airf_zLeng              ] ]
pole_p       = [ [              pole_left ,  0.0, pole_bot                 ],
                 [              pole_right,  0.0, pole_bot                 ],
                 [              pole_right,  0.0, pole_top                 ],
                 [              pole_left ,  0.0, pole_top                 ] ]
pole_n       = [ [              pole_left ,  0.0, - pole_bot               ],
                 [              pole_right,  0.0, - pole_bot               ],
                 [              pole_right,  0.0, - pole_top               ],
                 [              pole_left ,  0.0, - pole_top               ] ]
coil_p       = [ [ coil_xpos-0.5*coil_xwdt,  0.0, +coil_zpos-0.5*coil_zwdt ], 
                 [ coil_xpos+0.5*coil_xwdt,  0.0, +coil_zpos-0.5*coil_zwdt ],
                 [ coil_xpos+0.5*coil_xwdt,  0.0, +coil_zpos+0.5*coil_zwdt ],
                 [ coil_xpos-0.5*coil_xwdt,  0.0, +coil_zpos+0.5*coil_zwdt ] ]
coil_n       = [ [ coil_xpos-0.5*coil_xwdt,  0.0, -coil_zpos-0.5*coil_zwdt ], 
                 [ coil_xpos+0.5*coil_xwdt,  0.0, -coil_zpos-0.5*coil_zwdt ], 
                 [ coil_xpos+0.5*coil_xwdt,  0.0, -coil_zpos+0.5*coil_zwdt ], 
                 [ coil_xpos-0.5*coil_xwdt,  0.0, -coil_zpos+0.5*coil_zwdt ] ]

import nkGmshRoutines.generate__polygon as pol
ret1         = pol.generate__polygon( vertex=coil_p )
ret2         = pol.generate__polygon( vertex=coil_n )
ret3         = pol.generate__polygon( vertex=pole_p )
ret4         = pol.generate__polygon( vertex=pole_n )
ret5         = pol.generate__polygon( vertex=air_near )
ret6         = pol.generate__polygon( vertex=air_far  )

gmsh.model.occ.removeAllDuplicates()

# ------------------------------------------------- #
# --- [3] Physical Numbering                    --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
meshFile = "dat/mesh.conf"
physFile = "dat/phys.conf"
import nkGmshRoutines.assign__meshsize as ams
ams.assign__meshsize( meshFile=meshFile, physFile=physFile, target="surf" )

# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write( "msh/model.msh" )
gmsh.finalize()

