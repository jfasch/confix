#!/usr/bin/env python

import unittest

from libconfix.fileprops import FilePropertiesSet, FileProperties
from libconfix.buildable_h import BuildableHeader
from libconfix.buildable_c_base import BuildableCBase

class FilePropertiesSetTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        fps = FilePropertiesSet()

        fps.add(filename='a', buildable_type=None, properties=FileProperties({'x': 0}))
        fps.add(filename='a', buildable_type=BuildableCBase, properties=FileProperties({'y': 0}))
        fps.add(filename=None, buildable_type=BuildableHeader, properties=FileProperties({'y': 1}))
        fps.add(filename='a', buildable_type=BuildableHeader, properties=FileProperties({'x': 1}))

        fps.add(filename='a*', buildable_type=BuildableHeader, properties=FileProperties({'z': 2}))


        fp = fps.get_by_filename_or_type(filename='a', buildable_type=None)
        self.failIf(fp.get('x') is None)
        self.failIf(fp.get('y') is None)
        self.failIf(fp.get('z') is None)
        self.failUnless(fp.get('x') == 1)
        self.failUnless(fp.get('y') == 0)
        self.failUnless(fp.get('z') == 2)

        fp = fps.get_by_filename_or_type(filename=None, buildable_type=BuildableHeader)
        self.failIf(fp.get('x') is None)
        self.failIf(fp.get('y') is None)
        self.failIf(fp.get('z') is None)
        self.failUnless(fp.get('x') == 1)
        self.failUnless(fp.get('y') == 1)
        self.failUnless(fp.get('z') == 2)

        fp = fps.get_by_filename_or_type(filename='a', buildable_type=BuildableHeader)
        self.failIf(fp.get('x') is None)
        self.failIf(fp.get('y') is None)
        self.failIf(fp.get('z') is None)
        self.failUnless(fp.get('x') == 1)
        self.failUnless(fp.get('y') == 1)
        self.failUnless(fp.get('z') == 2)

if __name__ == '__main__':
    unittest.main()
