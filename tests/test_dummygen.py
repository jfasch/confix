#!/usr/bin/env python

import unittest

from libconfix.buildable_gen_demo_single import \
     BuildableGeneratorDemo_SingleGeneratorCreator

filename = 'dummygen.dummygen'

class DummyGenTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """Dummy/test BUILT_SOURCES generator"""

        c = BuildableGeneratorDemo_SingleGeneratorCreator()
        b = c.create_from_file(dir='data/buildables/ok',
                               filename=filename)
        b.scan(None)
        b.validate()

        buildables = b.generate()
        self.failUnless('dummygen.h' in [b.filename() for b in buildables],
                        filename+' did not generate "dummygen.h"')
        self.failUnless('dummygen.cc' in [b.filename() for b in buildables],
                        filename+' did not generate "dummygen.h"')

if __name__ == '__main__':
    unittest.main()
