module callbacks

  use iso_c_binding, ONLY: c_double, c_int
  implicit none

  ! C-compatible type to store a pointer to a callback procedure
  type, bind(c)::mgr
     procedure(callback_signature), pointer::callback=>null()
  end type mgr

  ! Declare signature of callback
  abstract interface
     subroutine callback_signature(size,arr)
       ! Callback function that modifies an array
       integer(c_int), value::size
           !! Size of array
       real(c_double)::arr
           !! Array data
     end subroutine callback_signature
  end interface

contains

  subroutine register_callback(mgr, callback) bind(c)

    ! Register a callback by storing it in mgr

    type(mgr), pointer::mgr
    procedure(callback_signature), pointer::callback

    ! Store the callback (Note that we could just call the callback from here
    ! directly instead of storing it)
    mgr%callback=callback

  end subroutine register_callback

  subroutine use_callback(mgr,size,arr) bind(c)

    call mgr%callback(size,arr)

  end subroutine use_callback

end module callbacks
