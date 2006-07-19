import unittest

class BuildableTest(unittest.TestCase):

    def __init__(self, b):

        unittest.TestCase.__init__(self)

        assert b is not None
        self.buildable_ = b

    def test(self): self.runTest()

    def runTest(self):

        """Buildable test"""

        self.buildable_.scan(buildmod=None)
        self.buildable_.validate()

    def shortDescription(self):

        return 'Scan and validate buildable object "'+self.buildable_.name()+'"'
