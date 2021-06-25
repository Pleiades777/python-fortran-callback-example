
# This is a demonstration of how to use the FFI module to create a callback
# function that can be used from Fortran

import numpy as np
from cffi import FFI

# Initialize FFI
ffi=FFI()

# Define FFI types
ffi.cdef("""

/* Function pointer for callback */
typedef void (*callback_t)(int,double*);

/* Struct to hold callback */
typedef struct mgr{
  callback_t callback;
} mgr;

/* Function to register callback */
void register_callback(mgr*,callback_t);

/* Function to use callback */
void use_callback(mgr*,int,double*);
""")

import os
import sys

# Determine shared library extension based on OS
is_windows = os.name == "nt"
is_apple = sys.platform == "darwin"
if is_windows:
    libsuffix= ".dll"
elif is_apple:
    libsuffix = ".dylib"
else:
    libsuffix = ".so"

# Open the Fortran library
lib = ffi.dlopen('./libcallbacks'+libsuffix)

# Mapping of numpy data types to C data types
ctype2dtype = {}

# Integer types
for prefix in ('int', 'uint'):
    for log_bytes in range(4):
        ctype = '%s%d_t' % (prefix, 8 * (2**log_bytes))
        dtype = '%s%d' % (prefix[0], 2**log_bytes)
        ctype2dtype[ctype] = np.dtype(dtype)

# Floating point types
ctype2dtype['float'] = np.dtype('f4')
ctype2dtype['double'] = np.dtype('f8')

def ptr_to_array(ptr,shape,**kwargs):

    """
    Convert a C pointer to a numpy array

    ptr: C pointer
    shape: Shape of array
    
    Additional keyword arguments are passed to np.frombuffer

    Returns: Numpy array object wrapping the data pointed to by ptr.
    """

    import numpy as np
    length = np.prod(shape)
    # Get the canonical C type of the elements of ptr as a string.
    T = ffi.getctype(ffi.typeof(ptr).item)
    # print( T )
    # print( ffi.sizeof( T ) )

    if T not in ctype2dtype:
        raise RuntimeError("Cannot create an array for element type: %s" % T)

    a = np.frombuffer(ffi.buffer(ptr, length * ffi.sizeof(T)), ctype2dtype[T])\
          .reshape(shape, **kwargs)
    return a

@ffi.callback("void(*)(int,double*)")
def modify_array(size,ptr):

    """
    Adds 1 to a 1-D array passed from Fortran

    Arguments:
    size: Array length
    ptr: Pointer to the array
    """

    # Numpy array wrapping ptr
    arr=ptr_to_array(ptr,[size])

    # Add 1 to array
    # (note we operate on a slice to ensure that we modify the data in-place)
    arr[:]+=1

def test_callback():

    a=np.zeros([10],dtype=np.float64)

    # For a pointer to this array to work in Fortran, the array must be
    # contiguous in memory (and if it's multidimensional it needs to be in
    # Fortran order)
    assert a.flags['F_CONTIGUOUS'], 'a is not contiguous in memory (F order)'

    # Get a pointer to the array data
    a_ptr=ffi.cast('double*',a.ctypes.data)

    # Create a new mgr struct
    mgr=ffi.new('struct mgr *')

    # Register the callback to be used from the Fortran side
    lib.register_callback(mgr,modify_array)

    # Call a routine that uses the callback
    lib.use_callback(mgr,len(a),a_ptr)

    # Check that the callback did what we expected
    assert np.all(a==1)

if __name__=='__main__':
    test_callback()
