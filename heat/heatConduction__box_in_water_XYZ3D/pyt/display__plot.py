import sys
import numpy                      as np
import nkUtilities.load__config   as lcf
import nkUtilities.plot1D         as pl1
import nkUtilities.configSettings as cfs


# ========================================================= #
# ===  display                                          === #
# ========================================================= #
def display():

    x_,y_ = 0, 1

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    config   = lcf.load__config()
    datFiles = [ "png/plot_t0000.csv", "png/plot_t0009.csv", "png/plot_t0019.csv", \
                 "png/plot_t0029.csv", "png/plot_t0039.csv", "png/plot_t0049.csv" ]
    labels   = [ "t={0} (s)".format(stime) for stime in [ 0, 200, 400, 600, 800, 1000 ]  ]
    pngFile  = "png/temperature_zAxis.png"

    # ------------------------------------------------- #
    # --- [2] Fetch Data                            --- #
    # ------------------------------------------------- #
    import pandas as pd
    Data_list        = [ pd.read_csv( datFile ) for datFile in datFiles ]
    zAxis_list       = [ np.array( Data["Points_2"]    )[:,None] for Data in Data_list ]
    temperature_list = [ np.array( Data["temperature"] )[:,None] for Data in Data_list ]
    zAxis            = np.concatenate( zAxis_list      , axis=1 )
    temperature      = np.concatenate( temperature_list, axis=1 )
    
    # ------------------------------------------------- #
    # --- [3] config Settings                       --- #
    # ------------------------------------------------- #
    cfs.configSettings( configType="plot1D_def", config=config )
    config["xTitle"]         = "Z (m)"
    config["yTitle"]         = "temperature (K)"
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [0.0,0.5]
    config["plt_yRange"]     = [+280,+380]
    config["plt_linestyle"]  = "-"
    config["plt_linewidth"]  = 1.0
    config["xMajor_Nticks"]  = 6
    config["yMajor_Nticks"]  = 6

    # ------------------------------------------------- #
    # --- [4] plot Figure                           --- #
    # ------------------------------------------------- #
    fig = pl1.plot1D( config=config, pngFile=pngFile )
    for ik in range( len( datFiles ) ):
        fig.add__plot( xAxis=zAxis[:,ik], yAxis=temperature[:,ik], label=labels[ik] )
    fig.add__legend()
    fig.set__axis()
    fig.save__figure()


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    display()

