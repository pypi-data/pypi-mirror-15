/**
 * author:  Manuel Gunther <siebenkopf@googlemail.com>
 * date:    Wed May 25 10:55:42 MDT 2016
 * license: BSD-3, see LICENSE file
 *
 * This file shows an exemplary usage of the Bob C++ interface, and is just here for test purposes.
 */

// include some Bob header files
#include <bob.io.image/png.h>
#include <bob.io.base/HDF5File.h>
#include <iostream>

int main(int argc, const char** argv){
  // Load the image using the C++ interface of bob.io.image
  blitz::Array<uint8_t, 3> image = bob::io::image::read_png<uint8_t,3>("test.png");

  // Save the image as HDF5 using the C++ interface of bob.io.base
  bob::io::base::HDF5File h("test.hdf5", 'w');
  h.setArray("Test", image);

  // Done.
  std::cout << "Successfully converted test.png into test.hdf5" << std::endl;
}
