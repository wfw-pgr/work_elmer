import numpy as np
import os, sys
import gmsh

gmshlib = os.environ["gmshLibraryPath"]
sys.path.append( gmshlib )

import generate__quadShape as qua

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
lc                                    = 0.1
x_, y_, z_, lc_, tag_                 = 0, 1, 2, 3, 4


# ------------------------------------------------- #
# --- [3] Modeling                              --- #
# ------------------------------------------------- #

#  -- [3-1] modeling parameters                 --  #

sim_boundary__x1    = -1.0
sim_boundary__x2    = +1.0
sim_boundary__y1    = -1.0
sim_boundary__y2    = +1.0

capacitor_length    = 0.60
capacitor_thickness = 0.05
capacitor_gap       = 0.10

lc_sim = 0.10
lc_plt = 0.02

#  -- [3-2] draw upper capacitor plate          --  #

x1_upr = [ - 0.5*capacitor_length, + ( capacitor_gap                     ), 0.0 ]
x2_upr = [ + 0.5*capacitor_length, + ( capacitor_gap                     ), 0.0 ]
x3_upr = [ + 0.5*capacitor_length, + ( capacitor_gap+capacitor_thickness ), 0.0 ]
x4_upr = [ - 0.5*capacitor_length, + ( capacitor_gap+capacitor_thickness ), 0.0 ]

ret1             = qua.generate__quadShape( lc=lc_plt, x1=x1_upr, x2=x2_upr, x3=x3_upr, x4=x4_upr )
line["upr_12"]   = ret1["line"]["line_1_2"]
line["upr_23"]   = ret1["line"]["line_2_3"]
line["upr_34"]   = ret1["line"]["line_3_4"]
line["upr_41"]   = ret1["line"]["line_4_1"]
surf["uprPlate"] = ret1["surf"]["quad"]

#  -- [3-3] draw lower capacitor plate          --  #

x1_lwr = [ - 0.5*capacitor_length, - ( capacitor_gap                     ), 0.0 ]
x2_lwr = [ + 0.5*capacitor_length, - ( capacitor_gap                     ), 0.0 ]
x3_lwr = [ + 0.5*capacitor_length, - ( capacitor_gap+capacitor_thickness ), 0.0 ]
x4_lwr = [ - 0.5*capacitor_length, - ( capacitor_gap+capacitor_thickness ), 0.0 ]

ret2             = qua.generate__quadShape( lc=lc_plt, x1=x1_lwr, x2=x2_lwr, x3=x3_lwr, x4=x4_lwr )
line["lwr_12"]   = ret2["line"]["line_1_2"]
line["lwr_23"]   = ret2["line"]["line_2_3"]
line["lwr_34"]   = ret2["line"]["line_3_4"]
line["lwr_41"]   = ret2["line"]["line_4_1"]
surf["lwrPlate"] = ret2["surf"]["quad"]

#  -- [3-4] draw simulation region              --  #

x1_sim = [ sim_boundary__x1, sim_boundary__y1, 0.0 ]
x2_sim = [ sim_boundary__x2, sim_boundary__y1, 0.0 ]
x3_sim = [ sim_boundary__x2, sim_boundary__y2, 0.0 ]
x4_sim = [ sim_boundary__x1, sim_boundary__y2, 0.0 ]

ret3             = qua.generate__quadShape( lc=lc_sim, x1=x1_sim, x2=x2_sim, x3=x3_sim, x4=x4_sim )
line["sim_12"]   = ret3["line"]["line_1_2"]
line["sim_23"]   = ret3["line"]["line_2_3"]
line["sim_34"]   = ret3["line"]["line_3_4"]
line["sim_41"]   = ret3["line"]["line_4_1"]
surf["air"]      = ret3["surf"]["quad"]

#  -- [3-5] remove duplicated region            --  #
gmsh.model.occ.removeAllDuplicates()

# ------------------------------------------------- #
# --- [4] Physical Grouping                     --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
# sim_boundary             = [ line["sim_12"], line["sim_23"], line["sim_34"], line["sim_41"] ]
# upr_boundary             = [ line["upr_12"], line["upr_23"], line["upr_34"], line["upr_41"] ]
# lwr_boundary             = [ line["lwr_12"], line["lwr_23"], line["lwr_34"], line["lwr_41"] ]
upr_boundary = [ 9, 10, 11, 12 ]
lwr_boundary = [ 5,  6,  7,  8 ]
sim_boundary = [ 1,  2,  3,  4 ]
linePhys["upr_boundary"] = gmsh.model.addPhysicalGroup( lineDim, upr_boundary        , tag=101 )
linePhys["lwr_boundary"] = gmsh.model.addPhysicalGroup( lineDim, lwr_boundary        , tag=102 )
linePhys["sim_boundary"] = gmsh.model.addPhysicalGroup( lineDim, sim_boundary        , tag=103 )
surfPhys["uprPlate"]     = gmsh.model.addPhysicalGroup( surfDim, [ surf["uprPlate"] ], tag=201 )
surfPhys["lwrPlate"]     = gmsh.model.addPhysicalGroup( surfDim, [ surf["lwrPlate"] ], tag=202 )
surfPhys["air"]          = gmsh.model.addPhysicalGroup( surfDim, [ surf["air"     ] ], tag=203 )




# ------------------------------------------------- #
# --- [2] post process                          --- #
# ------------------------------------------------- #
gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
gmsh.write( "model.geo_unrolled" )
gmsh.write( "model.msh" )
gmsh.finalize()

