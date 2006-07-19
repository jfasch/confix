#!/usr/bin/env python

import unittest

from libconfix.buildable_c import BuildableCCreator
from libconfix.buildable_cxx import BuildableCXXCreator
from libconfix.buildable_h import BuildableHeaderCreator
from libconfix.error import Error

class FilePropsTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """Explicit file properties (no shortcuts)"""
        
        c_c = BuildableCCreator()
        c_cxx = BuildableCXXCreator()
        c_h = BuildableHeaderCreator()

        c = c_c.create_from_file(
            dir='data/buildables/ok',
            filename='fileprops.c')
        self.do_ok_buildable(c)

        cxx = c_cxx.create_from_file(
            dir='data/buildables/ok',
            filename='fileprops.cc')
        self.do_ok_buildable(cxx)

        ok = 0
        try:
            h = c_h.create_from_file(
                dir='data/buildables/nok',
                filename='fileprops.h')
            h.scan(buildmod=None)
            h.validate()
        except Error, e:
            ok = 1

        self.failUnless(ok, 'data/buildables/nok/fileprops.h was ok')

    def do_ok_buildable(self, b):

        """ See if the C or C++ buildable has read all of its
        FILE_PROPERTIES() calls. """

        b.scan(buildmod=None)
        b.validate()

        self.assert_(b.has_main() is not None)
        self.assert_(b.has_main() == 1);

        self.assert_(b.exename() is not None)
        self.assert_(b.exename() == 'blah');


if __name__ == '__main__':
    unittest.main()
