.. vim: set fileencoding=utf-8 :
.. Manuel Gunther <siebenkopf@googlemail.com>
.. Wed May 25 10:55:42 MDT 2016

.. image:: http://travis-ci.org/bioidiap/bob.example.cmake.svg?branch=v1.0.1
   :target: https://travis-ci.org/bioidiap/bob.example.cmake?branch=v1.0.1
.. image:: https://img.shields.io/badge/github-master-0000c0.png
   :target: https://github.com/bioidiap/bob.example.cmake/tree/master

===========================================
 Example project using Bob's C++ interface
===========================================

This example project shows a way to incorporate Bob's C++ libraries into a C++ project.
For this, is uses the CMake_ interface, and a home-developed ``FindBob.cmake`` file.
It relies on the python interface to download and install Bob_.
More information about the Bob installation can be found on its `webpage <http://www.idiap.ch/software/bob>`_.

This package is licensed under a BSD-3 license with a copyright of the Regents of the University of Colorado on behalf of the University of Colorado Colorado Springs.
Please see LICENSE file for details.

Building this example
---------------------

As the example requires some Bob_ packages to be installed, we first run one of the ways to install Bob_, i.e., using `buildout <https://github.com/idiap/bob/wiki/Installation#using-zcbuildout-for-production>`_.
For that, simply go to the main directory of this package and call::

  $ python bootstrap-buildout.py
  $ ./bin/buildout

This will checkout some of the packages to the ``src`` directory, and download some into the ``eggs`` directory.
If you have Bob installed globally, it will use the globally installed packages instead of downloading new eggs.
If you have Bob installed in a non-default directory, for example in an `virtual environment <https://github.com/idiap/bob/wiki/Installation#using-pip-for-experts>`_, you can use that python version to bootstrap.

Inside of this package I have prepared a small CMake_ project that includes some of the Bob_ packages.
It uses the ``FindBob.cmake`` to locate Bob's include directories and libraries.
To enable that, you can use the ``find_package(Bob COMPONENTS <package(s)> REQUIRED)`` command to find the list of bob ``package(s)``.
Later, you can use three CMake_ variables ``Bob_INCLUDE_DIRS``, ``Bob_LIBRARY_DIRS``, ``Bob_LIBRARIES`` and ``Bob_DEFINITIONS`` and add it to your project::

  cmake_minimum_required(VERSION 2.8)
  project(test)

  # Set the module path so that "FindBob.cmake" is found
  set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR})

  # Find all Bob packages recursively
  find_package(Bob COMPONENTS bob.io.image REQUIRED)

  # Add Bob's include directories
  include_directories(${Bob_INCLUDE_DIRS})
  # Add Bob's library directories
  link_directories(${Bob_LIBRARY_DIRS})
  # Add Bob's libraries
  link_libraries(${Bob_LIBRARIES} boost_system)
  # Add Bob's definitions
  add_definitions(${Bob_DEFINITIONS})

  # create an "my_test" executable from file "test.cpp"
  add_executable(my_test test.cpp)

For some reason (that I do not understand) we also need to add the ``boost_system`` library, although it should theoretically be linked to the Bob_ libraries already.

So, now we can go ahead and compile our package using CMake_::

  $ mkdir build
  $ cd build
  $ cmake ..
  $ make

and we should get an executable ``my_test`` inside the build directory.
Note that you can pass a variable to CMake to use a custom Bob_ installation::

  $ cmake .. -DBOB_PREFIX_PATH=/path/to/your/bob/installation

or set the ``BOB_PREFIX_PATH`` environment variable accordingly.
If you have a local directory containing (some of) the Bob packages inside ``src`` or ``eggs`` sub-directories, you can set the ``BOB_SOURCE_DIR`` variable, which defaults to the directory where the ``CMakeLists.txt`` is located::

  $ cmake .. -DBOB_SOURCE_DIR=/path/to/your/local/bob/packages

The evaluation order of the directories is:

1. ``${BOB_SOURCE_DIR}/src``
2. ``${BOB_SOURCE_DIR}/eggs``
3. ``${BOB_PREFIX_PATH}/lib/*/site-packages`` (where * typically is your python version)
4. the system path

To run the example, go back to the package base directory (otherwise it will not find the example image) and call::

  $ ./build/my_test

This should create an HDF5 file called ``test.hdf5`` inside the current directory.


.. _cmake: http://cmake.org
.. _bob: http://www.idiap.ch/software/bob
