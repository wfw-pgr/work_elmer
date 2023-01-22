import sys

# ========================================================= #
# ===  Load Physical Number Table for Gmsh              === #
# ========================================================= #
def load__physNumTable( inpFile=None, line={}, surf={}, volu={} ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( inpFile is None ): sys.exit(" [LoadConst] inpFile == ?? ")
    
    # ------------------------------------------------- #
    # --- [2] Data Load                             --- #
    # ------------------------------------------------- #
    with open( inpFile ) as f:
        table = f.readlines()
        
    # ------------------------------------------------- #
    # --- [3] generate Dictionary                   --- #
    # ------------------------------------------------- #
    vdict = {}
    for row in table:
        if ( len( row.strip() ) == 0 ):
            continue
        if ( ( row[0] != "#" ) ):
            # -- [3-1] vname, vtype, value  -- #
            vname = ( row.split() )[0]
            vtype = ( row.split() )[1]
            value = ( row.split() )[2]
            
            # -- [3-2] vtype check          -- #
            if   ( vtype.lower() == 'line'   ):
                line[vname] = value
            elif ( vtype.lower() == 'surf'   ):
                surf[vname] = value
            elif ( vtype.lower() == 'volu'   ):
                volu[vname] = value
            else:
                print("[ERROR] Unknown Object in LoadConst :: {0} [ERROR]".format(inpFile) )

    ret = { "line":line, "surf":surf, "volu":volu }
    return( ret )
