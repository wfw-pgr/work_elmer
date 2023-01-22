
! ====================================================== !
! === calculate magnetization                        === !
! ====================================================== !

subroutine calculate__magnetization
  use DefUtils
  implicit none
  type(variable_t), pointer   :: mvec_ptr, bvec_ptr, hvec_ptr
  real(kind=dp)   , parameter :: mu_0 = 4.d-7 * atan( 1.d0 )

  ! ------------------------------------------------------ !
  ! --- [1] calculate variable magnetization           --- !
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
end subroutine calculate__magnetization
