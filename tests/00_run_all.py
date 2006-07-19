import unittest

import test_namespace
import test_configfile
import test_dummygen
import test_only_explicit_depinfo

import suite_resolve_packages
import suite_all_buildables_ok
import suite_cluster
import suite_fileprops
import suite_ifaces

if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(test_namespace.NamespaceTest())
    suite.addTest(test_configfile.ConfigFileOkTest())
    suite.addTest(test_dummygen.DummyGenTest())
    suite.addTest(test_only_explicit_depinfo.PackageWithOnlyExplicitDependencyInfoOkTest())

    suite.addTest(suite_ifaces.InterfacesSuite())
    suite.addTest(suite_all_buildables_ok.AllBuildablesOkSuite())
    suite.addTest(suite_resolve_packages.ResolveAllPackagesOkSuite())
    suite.addTest(suite_cluster.ClusterSuite())
    suite.addTest(suite_fileprops.FilePropertiesSuite())

    runner = unittest.TextTestRunner()
    runner.run(suite)
