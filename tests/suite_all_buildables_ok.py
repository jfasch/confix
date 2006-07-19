import unittest
import dircache
import os

from libconfix.buildable_mgr import BuildableManager
from libconfix.buildable_gen_demo_single import \
     BuildableGeneratorDemo_SingleGeneratorCreator
from libconfix.fileprops import FilePropertiesSet

from test_buildable import BuildableTest

buildables_ok_dir = 'data/buildables/ok'

class AllBuildablesOkSuite(unittest.TestSuite):

    def __init__(self):

        unittest.TestSuite.__init__(self)

        bmgr = BuildableManager()
        bmgr.register_creator('\.dummygen$', BuildableGeneratorDemo_SingleGeneratorCreator())
        
        if os.path.isdir(buildables_ok_dir):
            for n in dircache.listdir(buildables_ok_dir):
                if n in ['CVS', '.cvsignore']: continue
                if n.endswith('~'): continue
                if n.startswith('.#'): continue
                filename = os.path.join(buildables_ok_dir, n)
                if not os.path.isfile(filename): continue
                b = bmgr.create_from_file(dir=buildables_ok_dir,
                                          filename=n)
                assert b
                self.addTest(BuildableTest(b))
