import numpy as np
import nkUtilities.equiSpaceGrid as esg
x1MinMaxNum = [ 0.0, 0.8, 51 ]
x2MinMaxNum = [ 0.0, 0.0,  1 ]
x3MinMaxNum = [ 0.0, 0.0,  1 ]
ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                 x3MinMaxNum=x3MinMaxNum, returnType = "point" )
np.savetxt( "dat/coordinates.dat", ret )
