#!/usr/bin/env python

import unittest
import os
import dircache

from libconfix.buildable_ltlibrary import BuildableLibtoolLibrary
from libconfix.buildable_exe import BuildableExecutable
from libconfix.buildable_h import BuildableHeader
from libconfix.buildable_c import BuildableC
from libconfix.fileprops import FileProperties
from libconfix.buildable_clusterer_c import BuildableClusterer_C
from libconfix.buildable_mgr_bases import BuildableCluster
from libconfix.modbuild import BuildableModule
import libconfix.debug

DIR = os.path.join('data', 'buildables', 'ok')

def basic_c_buildables():

    buildables = []
    buildables.append(
        BuildableC(dir=DIR,
                   filename='c.c',
                   is_shallow=1
                   )
        )
    buildables.append(
        BuildableHeader(dir=DIR,
                        filename='h.h',
                        is_shallow=1
                        )
        )
    return buildables

class ClusterTest_Library(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """Clustering C type buildables into one library"""

        buildables = basic_c_buildables()

        module = BuildableModule(packagename=['package'],
                                 dir=DIR,
                                 ifacename='Makefile.py',
                                 use_libtool=1)

        clusterer = BuildableClusterer_C()

        clusters = []
        clusters = clusterer.make_clusters(buildables, clusters, module)

        self.failUnless(len(clusters)==1)
        self.failUnless(isinstance(clusters[0], BuildableLibtoolLibrary))
        self.failUnless(len(clusters[0].members())==0)

        lib = clusters[0]

        # a library is supposed to eat its members exclusively ...

        for b in buildables:
            rv = lib.cluster_add(b)
            self.failUnless(rv==BuildableCluster.ADD_EXCLUSIVE)

        for b in buildables:
            self.failUnless(b in lib.members())

        # ... and re-adding them should raise an assertion of the most
        # evil kind

        for b in buildables:
            self.failUnlessRaises(AssertionError, lib.cluster_add, b)

        self.failUnless(len(lib.members())==len(buildables))

class ClusterTest_Executable(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """Clustering C type buildables into executables"""

        buildables = basic_c_buildables()

        center1 = BuildableC(dir=DIR,
                             filename='main1.c',
                             is_shallow=1
                             )
        center1.set_has_main(1)

        center2 = BuildableC(dir=DIR,
                             filename='main2.c',
                             is_shallow=1
                             )
        center2.set_has_main(1)

        module = BuildableModule(packagename=['package'],
                                 dir=DIR,
                                 ifacename='Makefile.py',
                                 use_libtool=1)

        clusterer = BuildableClusterer_C()
        clusters = []
        clusters = clusterer.make_clusters(buildables+[center1, center2], clusters, module)

        self.failUnless(len(clusters)==2)
        self.failUnless(isinstance(clusters[0], BuildableExecutable))
        self.failUnless(isinstance(clusters[1], BuildableExecutable))
        self.failUnless(len(clusters[0].members())==0)
        self.failUnless(len(clusters[1].members())==0)

        exe1 = None
        exe2 = None
        for c in clusters:
            if c.center() is center1:
                exe1 = c
            if c.center() is center2:
                exe2 = c

        self.failIf(exe1 is exe2)
        self.failUnless(exe1 and exe2)

        # add non-main buildables to both executables
        
        for b in buildables:
            rv = exe1.cluster_add(b)
            self.failUnless(rv == BuildableCluster.ADD_SHARED)
            rv = exe2.cluster_add(b)
            self.failUnless(rv == BuildableCluster.ADD_SHARED)
            pass

        # add centers to both executables. exe1 must not accept
        # center2 and vice versa.

        rv = exe1.cluster_add(center1)
        self.failUnless(rv == BuildableCluster.ADD_EXCLUSIVE)

        rv = exe2.cluster_add(center2)
        self.failUnless(rv == BuildableCluster.ADD_EXCLUSIVE)

        rv = exe1.cluster_add(center2)
        self.failUnless(rv == BuildableCluster.ADD_REJECT)

        rv = exe2.cluster_add(center1)
        self.failUnless(rv == BuildableCluster.ADD_REJECT)

        # non-main buildables must have become members of both
        # executables ...

        for b in buildables:
            self.failUnless(b in exe1.members())
            self.failUnless(b in exe2.members())

        # ... and adding them twice must have a special return value

        for b in buildables:
            rv = exe1.cluster_add(b)
            self.failUnless(rv == BuildableCluster.ADD_NOCHANGE)
            rv = exe2.cluster_add(b)
            self.failUnless(rv == BuildableCluster.ADD_NOCHANGE)

        # re-adding the center must raise an AssertionError

        self.failUnlessRaises(AssertionError, exe1.cluster_add, center1)
        self.failUnlessRaises(AssertionError, exe2.cluster_add, center2)

        # centers must have become members of their respective
        # executables

        self.failUnless(center1 in exe1.members())
        self.failUnless(center2 in exe2.members())

        # any header files that are part of an executable must not be
        # installed

        for b in exe1.members()+exe2.members():
            self.failIf(isinstance(b, BuildableHeader) and \
                        b.provide_mode()!=BuildableHeader.PROVIDE_NOTATALL,
                        "Header files that are part of an executable must not be installed")

if __name__ == '__main__':
    unittest.main()
