import unittest
import os

from libconfix.package import Package

class PackageWithOnlyExplicitDependencyInfoOkTest(unittest.TestCase):

    """ Once there was a bug: a package did not calculate its depgraph
    if a package's modules had only explicit dependency
    information. This test ensures that the bug does not show up
    again. """

    def setUp(self):

        self.cwd_ = os.getcwd()
        os.chdir('data/packages/ok/only-explicit-depinfo')

    def tearDown(self):

        os.chdir(self.cwd_)

    def test(self): self.runTest()

    def runTest(self):

        """ Package with only explicit dependency info:
        data/packages/ok/only-explicit-depinfo """

        p = Package(dir='data/packages/ok/only-explicit-depinfo')

        p.scan()
        p.resolve_dependencies()

        higher = None
        for m in p.buildmods():
            if m.name() == ['only-explicit-depinfo', 'higher']:
                higher = m
            if m.name() == ['only-explicit-depinfo', 'basic']:
                basic = m

        self.failIf(higher is None)
        self.failIf(basic is None)
        self.failIf(p.depgraph() is None)

        topolist = p.depgraph().toposort(higher)
        self.failIf(topolist[0].module() is not basic)

if __name__ == '__main__':
    unittest.main()

