import numpy as np

# ========================================================= #
# ===  wavelength calculater                            === #
# ========================================================= #

def wavelength():

    import nkUtilities.load__constants as lcn
    inpFile  = "dat/wave.conf"
    const    = lcn.load__constants( inpFile=inpFile )

    mu0      = 4.0*np.pi*1.e-7
    epsilon0 = 8.854e-12
    c0       = 1.0 / np.sqrt( epsilon0 * mu0 )

    omega    = 2.0 * np.pi * const["freq"]
    k0       = omega / c0
    kx       = const["mmode"] * np.pi / const["wg_a"]
    ky       = const["nmode"] * np.pi / const["wg_b"]
    kc       = np.sqrt( kx**2 + ky**2 )
    beta0    = np.sqrt( k0**2 - kc**2 )
    Acoef    = omega * mu0 * kc * const["waveAmp"] / kc**2

    Zp_m     = np.sqrt( 0.5 * mu0 * omega / const["conductivity"] )
    alpha_m  = 0.5 * omega * mu0 / Zp_m

    lambda_w = 2.0 * np.pi / beta0


    print( "[wavelength] ----  settings ---- " )
    print()
    print( "[wavelength]   {0:<12}  :: {1} ".format( "freq"        , const["freq"]         ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "wg_a"        , const["wg_a"]         ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "wg_b"        , const["wg_b"]         ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "wg_L"        , const["wg_L"]         ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "waveAmp"     , const["waveAmp"]      ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "mmode"       , const["mmode"]        ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "nmode"       , const["nmode"]        ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "conductivity", const["conductivity"] ) )
    print()

    print( "[wavelength]   {0:<12}  :: {1} ".format( "omega"       , omega          ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "k0"          , k0             ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "kx"          , kx             ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "ky"          , ky             ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "kc"          , kc             ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "beta0"       , beta0          ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "lambda_w"    , lambda_w       ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "Acoef"       , Acoef          ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "Zp_m"        , Zp_m           ) )
    print( "[wavelength]   {0:<12}  :: {1} ".format( "alpha_m"     , alpha_m        ) )
    print()
    print( " ( 1 + 1/4 ) lambda_w = {0}".format( 1.25 * lambda_w ) )
    print()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    wavelength()
