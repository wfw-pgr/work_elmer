
Area  = 0.6
eps_r = 1.0
eps_0 = 8.85e-12
gap   = 0.10
dphi  = 1.0e4

Force = 0.5 * eps_r * eps_0 * Area / gap**2 * dphi
Capac =       eps_r * eps_0 * Area / gap

print( "[ElecForce_theoretical]       Force :: {0} ".format( Force ) )
print( "[ElecForce_theoretical] Capacitance :: {0} ".format( Capac ) )
