import unittest

import test_fileprops 
import test_fileprops_package 
import test_filepropsset 

class FilePropertiesSuite(unittest.TestSuite):

    def __init__(self):

        unittest.TestSuite.__init__(self)

        self.addTest(test_fileprops.FilePropsTest())
        self.addTest(test_fileprops_package.FilePropsPackageTest())
        self.addTest(test_filepropsset.FilePropertiesSetTest())
        
