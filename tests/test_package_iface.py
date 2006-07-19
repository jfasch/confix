import unittest
import os

from libconfix.package import Package

class PackageIfaceOkTest(unittest.TestCase):

    def setUp(self):

        self.cwd_ = os.getcwd()
        os.chdir('data/packages/ok/iface')

    def tearDown(self):

        os.chdir(self.cwd_)

    def test(self): self.runTest()

    def runTest(self):

        """ Package interface: data/packages/ok/iface """

        p = Package(dir='data/packages/ok/iface')

        p.scan()

        found_acinclude = 0
        for a in p.acinclude_m4().parts():
            if a.id() == 'blah-id': found_acinclude = 1
        self.failUnless(found_acinclude)

        found_configure_in = 0
        for c in p.configure_in():
            if c.id() == 'blah-id': found_configure_in = 1
        self.failUnless(found_configure_in)

if __name__ == '__main__':
    unittest.main()

