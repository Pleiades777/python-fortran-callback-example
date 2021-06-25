cmake_minimum_required(VERSION 3.0.2)

project(callbacks Fortran)

add_library(callbacks SHARED callbacks.f90)

configure_file(setup.py setup.py COPYONLY)
configure_file(test_callback.py test_callback.py COPYONLY)