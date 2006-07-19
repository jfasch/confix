import unittest
import os

from libconfix.package import Package

class PackageWithNoDependencyInfoOkTest(unittest.TestCase):

    """ Ensure that a package builds a dependency graph even if no
    module has dependency information. """

    def setUp(self):

        self.cwd_ = os.getcwd()
        os.chdir('data/packages/ok/no-depinfo')

    def tearDown(self):

        os.chdir(self.cwd_)

    def test(self): self.runTest()

    def runTest(self):

        """ Package with no dependency info:
        data/packages/ok/no-depinfo """

        p = Package(dir='data/packages/ok/no-depinfo')

        p.scan()
        p.resolve_dependencies()

        mod = None
        for m in p.buildmods():
            print '.'.join(m.name())
            if m.name() == ['no-depinfo', 'no-depinfo']:
                mod = m

        self.failIf(mod is None)
        self.failIf(p.depgraph() is None)

if __name__ == '__main__':
    unittest.main()

