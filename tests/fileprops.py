#!/usr/bin/env python

import unittest

import libconfix.buildable_c
import libconfix.buildable_cxx
import libconfix.buildable_h
import libconfix.error

class FilePropsTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """Explicit file properties (no shortcuts)"""

        c = libconfix.buildable_c.create('fileprops.c', 'data/buildables/ok', 'fileprops.c', None)
        self.do_ok_buildable(c)

        cxx = libconfix.buildable_cxx.create('fileprops.cc', 'data/buildables/ok', 'fileprops.cc', None)
        self.do_ok_buildable(cxx)

        h = libconfix.buildable_h.create('fileprops.h', 'data/buildables/nok', 'fileprops.h', None)
        h.scan()

        self.assertRaises(libconfix.error.InvalidProperty, h.validate)

    def do_ok_buildable(self, b):

        """ See if the C or C++ buildable has read all of its
        FILE_PROPERTIES() calls. """

        b.scan()
        b.validate()

        self.assert_(b.fileproperties().get_main() is not None)
        self.assert_(b.fileproperties().get_main() == 1);

        self.assert_(b.fileproperties().get_exename() is not None)
        self.assert_(b.fileproperties().get_exename() == 'blah');


if __name__ == '__main__':
    unittest.main()
