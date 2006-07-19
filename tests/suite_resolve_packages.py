import os
import dircache
import unittest

import test_package

data = 'data'
packages = 'packages'
ok = 'ok'
nok = 'nok'

package_dir = os.path.join('data', 'packages')
package_ok_dir = os.path.join(package_dir, ok)
package_nok_dir = os.path.join(package_dir, nok)

if not os.path.isdir(package_ok_dir):
    raise package_ok_dir+' is not a directory'

class ResolveAllPackagesSuite(unittest.TestSuite):

    def __init__(self, packagedir, expectation):

        unittest.TestSuite.__init__(self)

        if os.path.isdir(packagedir):
            for d in dircache.listdir(packagedir):
                if d == 'CVS': continue
                dir = os.path.join(packagedir, d)
                if not os.path.isdir(dir): continue
                self.addTest(
                    test_package.ResolveTest(os.path.join(packagedir, d),
                                             expectation))

class ResolveAllPackagesOkSuite(ResolveAllPackagesSuite):

    def __init__(self):

        ResolveAllPackagesSuite.__init__(
            self,
            package_ok_dir,
            test_package.ConfixTest.EXPECT_OK)
        
