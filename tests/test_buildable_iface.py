import unittest

from libconfix.buildable_cxx import BuildableCXXCreator
from libconfix.require_h import Require_CInclude
from libconfix.require_symbol import Require_Symbol
from libconfix.error import Error 

class BuildableIfaceOkTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """ Buildable interface: data/buildables/ok/iface.cc """

        c = BuildableCXXCreator()

        ok = c.create_from_file(dir='data/buildables/ok',
                                filename='iface.cc')
        ok.scan(buildmod=None)
        ok.validate()

        found_req_h = 0
        found_req_sym = 0

        depinfo = ok.reap_dependency_info()
        for r in depinfo.requires():
            if isinstance(r, Require_CInclude) and r.filename() == 'xxx.h':
                found_req_h = 1
            if isinstance(r, Require_Symbol) and r.symbol() == 'xxx':
                found_req_sym = 1
        self.failUnless(found_req_h)
        self.failUnless(found_req_sym)

        self.failUnless(ok.has_main()==1)
        self.failUnless(ok.exename() == 'xxx')

        found_check_my_cryptlib_here = 0
        for c in ok.gather_configure_in():
            if c.id() == 'my_cryptlib_here':
                found_check_my_cryptlib_here = 1
        self.failUnless(found_check_my_cryptlib_here)

        found_acinclude_beitl = 0
        for a in ok.gather_acinclude_m4():
            if a.id() == 'beitl':
                found_acinclude_beitl = 1
        self.failUnless(found_acinclude_beitl)

class BuildableIfaceNOkTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """ Buildable interface: data/buildables/nok/iface.cc """

        c = BuildableCXXCreator()

        nok = c.create_from_file(dir='data/buildables/nok',
                                 filename='iface.cc')
        nok.scan(buildmod=None)
        self.failUnlessRaises(Error, nok.validate)

if __name__ == '__main__':
    unittest.main()
