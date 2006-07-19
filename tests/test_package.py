import unittest
import os
import sys
import fnmatch

BUILDDIR='/tmp/confix-tests-'+`os.getpid()`
CONFIGFILE_BASE = '00REMOVE-THIS-CONFIGFILE'
CONFIGFILE_CONTENT = """

prof = {}

PROFILES = {
    'default': prof
    }

"""

def walkfun_files(patterns, dir, names):
    for n in names:
        fullname = os.path.join(dir, n)
        if not os.path.isfile(fullname): continue
        for p in patterns:
            if fnmatch.fnmatchcase(n, p):
                rm_file(os.path.join(dir, n))

def rm_file(file):
    os.remove(file)

def recursive_rm_dir(dir):
    # that's an easy way, but is there a built in easy way?
    os.system('rm -rf '+dir)

def rm_patterns_files(patterns, dir):
    if os.path.isdir(dir):
        walkfun_files(patterns, dir, dircache.listdir(dir))        

def recursive_rm_patterns_files(patterns, dir):
    os.path.walk(dir, walkfun_files, patterns)

class ConfixTest(unittest.TestCase):

    EXPECT_OK = 1
    EXPECT_FAIL = 2

    def __init__(self, expectation):

        unittest.TestCase.__init__(self)

        self.expectation_ = expectation
        assert expectation in [ConfixTest.EXPECT_OK,
                               ConfixTest.EXPECT_FAIL]

        self.cwd_ = os.getcwd()

        self.orig_pypath_ = None
        if os.environ.has_key('PYTHONPATH'):
            self.orig_pypath_ = os.environ['PYTHONPATH']

        self.configfilename_ = os.path.join(self.cwd_, CONFIGFILE_BASE)

        self.confix_ = os.path.join(self.cwd_, os.pardir, 'scripts', 'confix.py')
        self.argv_ = [self.confix_,
                      '--quiet',
                      '--packageversion=1.1.1',
                      '--configfile='+self.configfilename_,
                      ]

    def add_argv(self, arg):
        self.argv_.append(arg)

    def run_confix(self):
        cmdline = ' '.join([self.confix_]+self.argv_)
        rv = os.spawnv(os.P_WAIT, self.confix_, self.argv_)
        self.failIf(rv!=0 and self.expectation_==ConfixTest.EXPECT_OK,
                    "Confix failed: "+cmdline)

    def setUp(self):

        # set PYTHONPATH to the src dir

        if self.orig_pypath_ is None:
            new_pypath = os.path.join(self.cwd_, os.pardir)
        else:
            new_pypath = ':'.join((self.orig_pypath_, os.path.join(self.cwd_, os.pardir)))

        os.environ['PYTHONPATH'] = new_pypath

        # write config file

        file = open(self.configfilename_, 'w')
        file.write(CONFIGFILE_CONTENT)
        file.close()

    def tearDown(self):

        # restore original PYTHONPATH

        if self.orig_pypath_ is None:
            del os.environ['PYTHONPATH']
        else:
            os.environ['PYTHONPATH'] = self.orig_pypath_

        # remove config file

        os.remove(self.configfilename_)

    def test(self): self.runTest()
    def runTest(self): self.run_confix()

class PackageTest(ConfixTest):

    def __init__(self, packageroot, expectation):

        ConfixTest.__init__(self, expectation)

        self.packageroot_ = os.path.join(self.cwd_, packageroot) 
        if not os.path.isdir(self.packageroot_):
            raise self.packageroot_ + " is not a directory"

        self.add_argv('--packageroot='+self.packageroot_)

    def packageroot(self): return self.packageroot_

class ResolveTest(PackageTest):

    def __init__(self, packageroot, expectation):

        PackageTest.__init__(self, packageroot, expectation)

    def setUp(self):

        ConfixTest.setUp(self)
        self.add_argv('--resolve')

class OutputTest(ResolveTest):

    def __init__(self, packageroot, expectation):

        ResolveTest.__init__(self, packageroot, expectation)

    def setUp(self):

        ResolveTest.setUp(self)
        self.add_argv('--output')

    def tearDown(self):

        ResolveTest.tearDown(self)

        # --output generates all Makefile.am's, configure.in, and the module
        # description files. remove them.

        # for the names of module description files, we apply a
        # heuristic. we hope that nobody changes the way these names
        # are generated, and that they'll never get in conflict with
        # the module's interface names (currently Makefile.py).

        pkg_base = os.path.basename(self.packageroot())
        mod_desc_pat = pkg_base+'_*.py'

        recursive_rm_patterns_files(['Makefile.am', 'configure.in', 'acinclude.m4', mod_desc_pat],
                                    self.packageroot())

class BootstrapTest(OutputTest):

    def __init__(self, packageroot, expectation):

        OutputTest.__init__(self, packageroot, expectation)

    def setUp(self):

        OutputTest.setUp(self)
        self.add_argv('--bootstrap')

    def tearDown(self):

        OutputTest.tearDown(self)

        # bootstrap generates a whole bunch of files. we don't exactly
        # know how they are named, and we can only try to remove all
        # of them.

        recursive_rm_patterns_files(['Makefile.in',
                                     'configure',
                                     'aclocal.m4',
                                     'config.guess',
                                     'config.h.in',
                                     'config.sub',
                                     'depcomp',
                                     'install-sh',
                                     'ltmain.sh',
                                     'missing',
                                     'mkinstalldirs'
                                     ],
                                    self.packageroot())

        recursive_rm_dir(os.path.join(self.packageroot(), 'autom4te.cache'))

class ConfigureTest(BootstrapTest):

    def __init__(self, packageroot, expectation):

        BootstrapTest.__init__(self, packageroot, expectation)

    def setUp(self):

        BootstrapTest.setUp(self)
        self.add_argv('--configure')
        self.add_argv('--builddir='+BUILDDIR)

        # if anyone left over the BUILDDIR (maybe because he
        # interrupted the test run before tearDown()), we don't
        # complain.
        
        try: os.makedirs(BUILDDIR)
        except: pass

    def tearDown(self):

        BootstrapTest.tearDown(self)
        recursive_rm_dir(BUILDDIR)

class BuildTest(ConfigureTest):

    def __init__(self, packageroot, expectation):

        ConfigureTest.__init__(self, packageroot, expectation)

    def setUp(self):

        ConfigureTest.setUp(self)
        self.add_argv('--make')

class CheckTest(BuildTest):

    def __init__(self, packageroot, expectation):

        BuildTest.__init__(self, packageroot, expectation)

    def setUp(self):

        BuildTest.setUp(self)
        self.add_argv('--targets=check')


if __name__ == '__main__':

    what = sys.argv[1]
    pkgs = sys.argv[2:]

    suite = unittest.TestSuite()

    for pkg in pkgs:
        if what == 'resolve':
            test = ResolveTest(pkg, ConfixTest.EXPECT_OK)
        elif what == 'output':
            test = OutputTest(pkg, ConfixTest.EXPECT_OK)
        elif what == 'bootstrap':
            test = BootstrapTest(pkg, ConfixTest.EXPECT_OK)
        elif what == 'configure':
            test = ConfigureTest(pkg, ConfixTest.EXPECT_OK)
        elif what == 'build':
            test = BuildTest(pkg, ConfixTest.EXPECT_OK)
        elif what == 'check':
            test = CheckTest(pkg, ConfixTest.EXPECT_OK)
        else:
            raise "unknown action '"+what+'"'

        suite.addTest(test)

    runner = unittest.TextTestRunner()
    runner.run(suite)
