#!/usr/bin/env python

import unittest
import os

from libconfix.buildable_c import BuildableC
from libconfix.buildable_gen_demo_single import \
     BuildableGeneratorDemo_SingleGenerator
from libconfix.buildable_gen_demo_cluster import \
     BuildableGeneratorDemo_SingleClusterable, \
     BuildableGeneratorDemo_Clusterer, \
     BuildableGeneratorDemo_Cluster
     
from libconfix.buildable_lib_base import BuildableLibraryBase
from libconfix.buildable_exe import BuildableExecutable
from libconfix.buildable_mgr import BuildableManager
from libconfix.fileprops import FileProperties
from libconfix.modbuild import BuildableModule


DIR = os.path.join('data', 'buildables', 'ok')

class ClusterTest1_DummyGenerator(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        buildables = []

        buildables.append(
            BuildableC(dir=DIR,
                       filename='c1.c',
                       is_shallow=1))
        buildables.append(
            BuildableC(dir=DIR,
                       filename='c2.c',
                       is_shallow=1))
        buildables.append(
            BuildableGeneratorDemo_SingleClusterable(dir=DIR,
                                                     filename='d1.dummy',
                                                     is_shallow=1))
        buildables.append(
            BuildableGeneratorDemo_SingleClusterable(dir=DIR,
                                                     filename='d2.dummy',
                                                     is_shallow=1))
        buildables.append(
            BuildableGeneratorDemo_SingleGenerator(dir=DIR,
                                                   filename='dg.dummygen',
                                                   is_shallow=1))

        module = BuildableModule(packagename=['package'],
                                 dir=DIR,
                                 ifacename='Makefile.py',
                                 use_libtool=1)

        bmgr = BuildableManager()
        bmgr.register_clusterer(BuildableGeneratorDemo_Clusterer())
        new_buildables = bmgr.create_clusters(buildables=buildables,
                                              module=module)

        # I've played it through, must yield 11 buildables :-)

        self.failUnless(len(new_buildables)==11,
                        "# buildables is not 11, but rather "+`len(new_buildables)`)

        # namely, as there are:

        lib = None
        for b in new_buildables:
            if isinstance(b, BuildableLibraryBase):
                lib = b
                break
            pass
        self.failIf(lib is None)
        self.failUnless(len(lib.members())==6)
        
        comp_dummygen = None
        for b in new_buildables:
            if isinstance(b, BuildableGeneratorDemo_Cluster):
                comp_dummygen = b
                break

        self.failIf(comp_dummygen is None)

class ClusterTest2_DummyGenerator(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        buildables = []

        center1 = BuildableC(dir=DIR,
                             filename='main1.c',
                             is_shallow=1)
        center1.set_has_main(1)

        center2 = BuildableC(dir=DIR,
                             filename='main2.c',
                             is_shallow=1)
        center2.set_has_main(1)

        buildables.append(center1)
        buildables.append(center2)
        buildables.append(
            BuildableC(dir=DIR,
                       filename='c.c',
                       is_shallow=1))
        buildables.append(
            BuildableGeneratorDemo_SingleClusterable(dir=DIR,
                                                     filename='d1.dummy',
                                                     is_shallow=1))
        buildables.append(
            BuildableGeneratorDemo_SingleClusterable(dir=DIR,
                                                     filename='d2.dummy',
                                                     is_shallow=1))
        buildables.append(
            BuildableGeneratorDemo_SingleGenerator(dir=DIR,
                                                   filename='dg.dummygen',
                                                   is_shallow=1))

        module = BuildableModule(packagename=['package'],
                                 dir=DIR,
                                 ifacename='Makefile.py',
                                 use_libtool=1)

        bmgr = BuildableManager()
        bmgr.register_clusterer(BuildableGeneratorDemo_Clusterer())
        new_buildables = bmgr.create_clusters(buildables=buildables,
                                              module=module)

        # I've played it through, must yield 13 buildables :-)

        self.failUnless(len(new_buildables)==13,
                        "# buildables is not 13, but rather "+`len(new_buildables)`)

        # namely, as there are:

        exe1 = None
        exe2 = None
        for b in new_buildables:
            if isinstance(b, BuildableExecutable):
                if b.center() is center1: exe1 = b
                if b.center() is center2: exe2 = b

        self.failIf(exe1 is None)
        self.failIf(exe2 is None)

        self.failUnless(len(exe1.members()) == 6)
        self.failUnless(len(exe2.members()) == 6)

        comp_dummygen = None
        for b in new_buildables:
            if isinstance(b, BuildableGeneratorDemo_Cluster):
                comp_dummygen = b
                break

        self.failIf(comp_dummygen is None)

if __name__ == '__main__':
    unittest.main()
