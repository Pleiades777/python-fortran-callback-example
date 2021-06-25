module callbacks

  use iso_c_binding, ONLY: c_double, c_int, c_funptr, c_f_procpointer
  implicit none

  ! C-compatible type to store a pointer to a callback procedure
  type, bind(c)::mgr
     type(c_funptr)::callback
  end type mgr

  ! Declare signature of callback
  abstract interface
     subroutine callback_signature(size,arr)

       ! Callback function that modifies an array

       use iso_c_binding, ONLY: c_double, c_int

       integer(c_int), value::size
           !! Size of array

       real(c_double)::arr(size)
           !! Array data

     end subroutine callback_signature
  end interface

contains

  subroutine register_callback(manager, callback) bind(c)

    ! Register a callback by storing it in mgr

    type(mgr), intent(inout)::manager
    type(c_funptr), intent(in), value::callback

    manager%callback=callback

  end subroutine register_callback

  subroutine use_callback(manager,size,arr) bind(c)

    type(mgr)::manager
    integer(c_int)::size
    real(c_double)::arr
    procedure(callback_signature), pointer::callback

    call c_f_procpointer(manager%callback, callback)

    call callback(size,arr)

  end subroutine use_callback

end module callbacks
