import unittest

import test_cluster_c 
import test_cluster_dummygen 

class ClusterSuite(unittest.TestSuite):

    def __init__(self):

        unittest.TestSuite.__init__(self)

        self.addTest(test_cluster_c.ClusterTest_Library())
        self.addTest(test_cluster_c.ClusterTest_Executable())
        self.addTest(test_cluster_dummygen.ClusterTest1_DummyGenerator())
        self.addTest(test_cluster_dummygen.ClusterTest2_DummyGenerator())
        
