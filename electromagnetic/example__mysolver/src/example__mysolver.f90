subroutine example__mysolver
  ! -- Fundamental module to use elmer solver -- !
  use DefUtils
  implicit none

  type(solver_t)   , pointer  :: solver_type
  type(ValueList_t), pointer  :: solver, simulation, constants, material
  type(element_t)  , pointer  :: element
  character(Len=Max_Name_Len) :: variable, coordSystem, name, materialname
  real(kind=dp)               :: permeability
  real(kind=dp), allocatable  :: radius(:,:), coord_x(:,:), coord(:,:,:), field_var(:)
  type(nodes_t)               :: elementNodes
  integer                     :: iE, iN, nNodes, nElements, nMaxNodes, elementNumber
  logical                     :: Found, Found1, Found2, Found3
  integer, parameter          :: x_=1, y_=2, z_=3
  
  type(variable_t), pointer   :: coordx_ptr
  real(kind=dp)   , pointer   :: values(:), values_(:)
  integer         , pointer   :: perm(:)

  type(variable_t), pointer   :: mvec_ptr, bvec_ptr, hvec_ptr
  real(kind=dp), allocatable  :: mvec(:), bvec(:), hvec(:)
  double precision, parameter :: mu_0 = 4.d-7 * atan( 1.d0 )


  ! ------------------------------------------------------ !
  ! --- [1] Get .sif parameters                        --- !
  ! ------------------------------------------------------ !
  solver       => GetSolverParams()
  simulation   => GetSimulation()
  constants    => GetConstants()
  material     => GetMaterial()
  
  variable     =  GetString   ( solver    , "variable"              , Found1 )
  coordSystem  =  GetString   ( simulation, "coordinate system"     , Found2 )
  permeability =  GetConstReal( constants , "permeability of vacuum", Found3 )
  materialname =  GetString   ( material  , "Name"                  , Found  )

  write(6,*) materialname
  
  if ( .not.Found1 ) then
     call FATAL( "example__mysolver", "variable not found" )
  else
     write(6,*) variable
  endif
  
  if ( .not.Found2 ) then
     call FATAL( "example__mysolver", "variable not found" )
  else
     write(6,*) coordSystem
  endif
  
  if ( .not.Found3 ) then
     call FATAL( "example__mysolver", "variable not found" )
  else
     write(6,*) permeability
  endif

  ! ------------------------------------------------------ !
  ! --- [2] Get Element related .sif values            --- !
  ! ------------------------------------------------------ !
  
  ElementNumber =  2                                              ! Element Number to fetch.
  element       => GetActiveElement( ElementNumber )              ! Get Element.
  nElements     =  CurrentModel % Solver % NumberOfActiveElements ! Num. of Elements
  nMaxNodes     =  CurrentModel % MaxElementNodes                 ! Max. num. of nodes for all elements
  
  write(6,*)
  write(6,*) "Num. of Element     :: ", nElements
  write(6,*) "Element Number      :: ", ElementNumber
  write(6,*) "Max. num. of nodes  :: ", nMaxNodes
  write(6,*)
  allocate( radius( nMaxNodes, nElements ), coord_x( nMaxNodes, nElements ) )

  do iE=1, nElements
     element       => GetActiveElement( iE )
     radius (:,iE) =  GetReal( solver, "radius" , Found )
     coord_x(:,iE) =  GetReal( solver, "coord_x", Found )
  enddo
  write(6,*) " radius    : (min,max) :: ", minval( radius  ), maxval( radius  )
  write(6,*) " coord_x   : (min,max) :: ", minval( coord_x ), maxval( coord_x )
  write(6,*)

  ! ------------------------------------------------------ !
  ! --- [3] Get Nodal Coordinates for element          --- !
  ! ------------------------------------------------------ !
  
  allocate( coord(3,nMaxNodes,nElements) )
  
  do iE=1, nElements
     element       => GetActiveElement( iE )
     call GetElementNodes( ElementNodes, Element )
     coord(x_,:,iE) = elementNodes % x(:)
     coord(y_,:,iE) = elementNodes % y(:)
     coord(z_,:,iE) = elementNodes % z(:)
  end do
  write(6,*) " coord(x_) : (min,max) :: ", minval( coord(x_,:,:) ), maxval( coord(x_,:,:) )
  write(6,*) " coord(y_) : (min,max) :: ", minval( coord(y_,:,:) ), maxval( coord(y_,:,:) )
  write(6,*) " coord(z_) : (min,max) :: ", minval( coord(z_,:,:) ), maxval( coord(z_,:,:) )
  write(6,*)

  ! ------------------------------------------------------ !
  ! --- [4] Get Nodal values of field variables for e  --- !
  ! ------------------------------------------------------ !
  allocate( field_var( nMaxNodes ) )
  element => GetActiveElement( 1 )
  call GetScalarLocalSolution( field_var, "coordinate 1", element )
  write(6,*) " field_var :: ", field_var

  ! ------------------------------------------------------ !
  ! --- [5] Get ALL Nodal values of field variables    --- !
  ! ------------------------------------------------------ !
  coordx_ptr => variableGet( CurrentModel % Solver % Mesh % Variables, "coordinate 1" )

  if ( associated( coordx_ptr ) ) then
     perm   => coordx_ptr % perm
     values => coordx_ptr % values
  else
     call Fatal( "MySolver", "No variable Temperature Found" )
  endif

  ! ------------------------------------------------------ !
  ! --- [6] calculate variable magnetization           --- !
  ! ------------------------------------------------------ !
  !
  ! define  -- variable      = string "magnetization" -- 
  !         -- variable DOFs = 3                      -- in .sif file
  !
  bvec_ptr => variableGet( CurrentModel % Solver % Mesh % Variables, "magnetic flux density"   )
  hvec_ptr => variableGet( CurrentModel % Solver % Mesh % Variables, "magnetic field strength" )
  mvec_ptr => variableGet( CurrentModel % Solver % Mesh % Variables, "magnetization"           )

  mvec_ptr % values(:) =  bvec_ptr % values(:) - mu_0 * hvec_ptr % values(:)
  
  return
end subroutine example__mysolver
