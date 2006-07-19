import unittest
import os

from libconfix.package import Package
from libconfix.buildable_single import BuildableSingle
from libconfix.buildable_h import BuildableHeader
from libconfix.error import Error

ROOT = "data/packages/ok/fileprops"

class FilePropsPackageTest(unittest.TestCase):

    def setUp(self):

        self.curdir_ = os.getcwd()
        os.chdir(ROOT)

    def tearDown(self):

        os.chdir(self.curdir_)

    def test(self): self.runTest()

    def runTest(self):

        "See what happens to file properties in package "+ROOT

        try:
            package = Package('fileprops')
            package.scan()
        except Error, e:
            print `e`
            self.fail()

        have_mod_iface_rules = 0
        have_mod_iface_rules2 = 0
        have_buildable_rules = 0
        have_buildable_rules2 = 0
        have_installdir_h = 0

        for m in package.buildmods():

            if m.name() == ['fileprops', 'mod_iface_rules']:
                have_mod_iface_rules = 1

                have_main1 = 0
                have_main2 = 0

                for b in m.buildables():

                    if not isinstance(b, BuildableSingle):
                        continue

                    if b.filename() == 'main1.cc':
                        have_main1 = 1

                        self.failIf(b.has_main())

                    if b.filename() == 'main2.cc':
                        have_main2 = 1

                        self.failUnless(b.has_main())
                        self.failUnless(b.exename() == 'main2')

                self.failUnless(have_main1)
                self.failUnless(have_main2)
                
            if m.name() == ['fileprops', 'mod_iface_rules2']:
                have_mod_iface_rules2 = 1

                have_h1_h = 0

                for b in m.buildables():

                    if not isinstance(b, BuildableSingle):
                        continue

                    if b.filename() == 'h1.h':
                        have_h1_h = 1

                        self.failUnless(b.install_path() == 'installpath')
                        self.failUnless(b.provide_mode() == BuildableHeader.PROVIDE_PACKAGE)

                self.failUnless(have_h1_h)
                
            if m.name() == ['fileprops', 'buildable_rules']:
                have_buildable_rules = 1

                have_main3 = 0
                have_main4 = 0

                for b in m.buildables():

                    if not isinstance(b, BuildableSingle):
                        continue

                    if b.filename() == 'main3.cc':
                        have_main3 = 1

                        self.failUnless(b.has_main())

                    if b.filename() == 'main4.cc':
                        have_main4 = 1

                        self.failUnless(b.has_main())
                        self.failUnless(b.exename() == 'nixbeitl')

                self.failUnless(have_main3, 'main3.cc not seen')
                self.failUnless(have_main4, 'main4.cc not seen')

            if m.name() == ['fileprops', 'buildable_rules2']:
                have_buildable_rules2 = 1

                have_h2_h = 0

                for b in m.buildables():

                    if not isinstance(b, BuildableSingle):
                        continue

                    if b.filename() == 'h2.h':
                        have_h2_h = 1

                        self.failUnless(b.install_path() == 'y')
                        self.failUnless(b.provide_mode() == BuildableHeader.PROVIDE_PUBLIC)

                self.failUnless(have_h2_h, 'h2.h not seen')

            if m.name() == ['fileprops', 'installdir_h']:
                have_installdir_h = 1

                have_install_h = 0

                for b in m.buildables():

                    if not isinstance(b, BuildableSingle):
                        continue

                    if b.filename() == 'install.h':
                        have_install_h = 1

                        self.failUnless(b.install_path() == 'x')

                self.failUnless(have_install_h)
                

        self.failUnless(have_mod_iface_rules)
        self.failUnless(have_mod_iface_rules2)
        self.failUnless(have_buildable_rules)
        self.failUnless(have_buildable_rules2)
        self.failUnless(have_installdir_h)

if __name__ == '__main__':
    unittest.main()

