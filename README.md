# Example of calling Python procedures from Fortran via a callback with FFI

## Concept

The Python [FFI](https://cffi.readthedocs.io/en/latest/) module provides an interface to call C functions from Python, and to create Python callback functions that can be called from C. It can be used to interface with Fortran as well, provided that any Fortran procedures being called are compiled into a shared library and are C interoperable (i.e., declared with bind(c) and accept only C-compatible types as arguments). This requires a Fortran 2003-compliant compiler since it relies on the C interoperability features of Fortran 2003.

This repository provides a basic example of this functionality. It includes Fortran source code for subroutines that can be called from Python, Python code that calls the Fortran procedures, and a CMakeLists.txt file to compile the Fortran code to a shared library.

## Requirements

- CMake (have tried 3.10.2 and 3.20.2, but older versions probably work too)
- A Fortran compiler that supports Fortran 2003, in particular iso\_c\_binding and C function pointers (have tested gfortran 7.5 and 11)
- A python interpreter with numpy and cffi modules

## Usage

The example can be built and run with the following commands:

```bash
pip install numpy cffi
mkdir build
cmake ..
make
python test_callback.py
```

## Further reading

There are many references on writing C interoperable procedures in Fortran. A few good ones are below:

* GNU Fortran documentation [section on C interoperability](https://gcc.gnu.org/onlinedocs/gfortran/Interoperability-with-C.html). In particular look at [Interoperable Subroutines and Functions](https://gcc.gnu.org/onlinedocs/gfortran/Interoperable-Subroutines-and-Functions.html)
* [C interoperability page](http://fortranwiki.org/fortran/show/C+interoperability) at the Fortran Wiki
* [Standard Fortran and C Interoperability](https://software.intel.com/content/www/us/en/develop/documentation/fortran-compiler-oneapi-dev-guide-and-reference/top/compiler-reference/mixed-language-programming/standard-fortran-and-c-interoperability.html) page from Intel OneAPI documentation

Note some older tutorials on interfacing Fortran with C make no mention of iso_c_binding and tell you to add an underscore to the end of a procedure name rather than using bind(c) in the procedure declaration. Such techniques were widely employed before C interoperability was standardized in Fortran 2003, but since they were never part of the Fortran standard they are not guaranteed to work across different compilers and subtle differences between compilers may lead to unexpected behavior when attempting to interface with C without using iso\_c\_binding and bind(c).
