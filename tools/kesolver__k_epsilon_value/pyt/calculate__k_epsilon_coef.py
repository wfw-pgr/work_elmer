import os, sys, json
import numpy as np

# ========================================================= #
# ===  calculate__k_epsilon_coef.py                     === #
# ========================================================= #

def calculate__k_epsilon_coef( inpFile=None, outFile=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): inpFile = "dat/parameter.conf"
    import nkUtilities.load__constants as lcn
    inpFile = "dat/parameter.conf"
    const   = lcn.load__constants( inpFile=inpFile )

    # ------------------------------------------------- #
    # --- [2] const check                           --- #
    # ------------------------------------------------- #
    checkkeys = [ "rho__density", "dh__diameter", "mu__viscosity", "u__velocity" ]
    for key in checkkeys:
        if ( not( key in const ) ): sys.exit( " ERROR!!!  cannot find {}.".format( key ) )

    if ( not( "Cmu__coef" in const ) ):
        print( "[calculate__k_epsilon_coef.py] default Cmu == 0.09 will be used. [CAUTION] " )
        const["Cmu__coef"] = 0.09
    
    # ------------------------------------------------- #
    # --- [2] calculation                           --- #
    # ------------------------------------------------- #
    const["Re.dh__Reynolds"]    = const["rho__density"] * const["u__velocity"] \
        * const["dh__diameter"] / const["mu__viscosity"]
    const["I__intensity"]       =  0.16 * const["Re.dh__Reynolds"]**(-0.125)
    const["l__turbulentLength"] = 0.038 * const["dh__diameter"]
    const["k__KineticEnergy"]   = 1.5 * ( const["u__velocity"] * const["I__intensity"] )**2
    const["eps__dissipation"]   = const["Cmu__coef"] * const["k__KineticEnergy"]**(1.5) \
        / const["l__turbulentLength"]
    
    # ------------------------------------------------- #
    # --- [3] output                                --- #
    # ------------------------------------------------- #
    if ( outFile is None ):
        for key,item in const.items():
            print( "{0:>20} : {1:<}".format( key, item ) )
    else:
        json.dump( const, outFile )
    return()


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    calculate__k_epsilon_coef()
    
