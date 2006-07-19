import unittest
import os

from libconfix.modbuild import BuildableModule

class ModuleIfaceOkTest(unittest.TestCase):

    def setUp(self):

        self.cwd_ = os.getcwd()
        os.chdir('data/modules/ok')

    def tearDown(self):

        os.chdir(self.cwd_)

    def test(self): self.runTest()

    def runTest(self):

        """ Module interface: data/modules/ok/iface """

        mod = BuildableModule(
            packagename=['the_package'],
            dir='iface',
            ifacename='Makefile.py',
            use_libtool=1)

        mod.scan()

        found_acinclude = 0
        for a in mod.acinclude_m4().parts():
            if a.id() == 'blah-id': found_acinclude = 1
        self.failUnless(found_acinclude)

        found_configure_in = 0
        for c in mod.configure_in():
            if c.id() == 'blah-id': found_configure_in = 1
        self.failUnless(found_configure_in)

if __name__ == '__main__':
    unittest.main()

