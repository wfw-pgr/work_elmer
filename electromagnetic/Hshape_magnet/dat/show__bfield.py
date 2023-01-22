import sys
import numpy                      as np
import nkUtilities.LoadConfig     as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display( datFile=None, pngFile=None, config=None ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( datFile is None ): datFile = "bfield_xAxis.dat"
    if ( pngFile is None ): pngFile = "bfield_xAxis.png"
    if ( config  is None ): config  = lcf.LoadConfig()

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    with open( datFile, "r" ) as f:
        Data = np.loadtxt( f )
    xAxis = Data[:,3]
    yAxis = Data[:,8]
    
    index = np.argsort( xAxis )
    xAxis = xAxis[index]
    yAxis = yAxis[index]
        
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "r (m)"
    config["yTitle"]         = "B (T)"
    config["plt_xAutoRange"] = True
    config["plt_yAutoRange"] = True
    config["plt_xRange"]     = [-5.0,+5.0]
    config["plt_yRange"]     = [-5.0,+5.0]
    config["plt_linewidth"]  = 1.0
    config["xMajor_Nticks"]  = 5
    config["yMajor_Nticks"]  = 5
    config["plt_marker"]     = "o"
    config["plt_linewidth"]  = 0.5
    
    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=xAxis, yAxis=yAxis, label="ans" )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()
    

# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display()
    

