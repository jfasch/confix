import unittest

from test_module_iface import ModuleIfaceOkTest
from test_buildable_iface import \
     BuildableIfaceOkTest, \
     BuildableIfaceNOkTest

class InterfacesSuite(unittest.TestSuite):

    def __init__(self):

        unittest.TestSuite.__init__(self)

        self.addTest(ModuleIfaceOkTest())
        self.addTest(BuildableIfaceOkTest())
        self.addTest(BuildableIfaceNOkTest())
