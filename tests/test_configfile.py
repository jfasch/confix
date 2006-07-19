#!/usr/bin/env python

import unittest

import libconfix.configfile

class ConfigFileOkTest(unittest.TestCase):

    def test(self): self.runTest()

    def runTest(self):

        """Configuration file"""

        file = libconfix.configfile.ConfigFile('data/configfiles/ok/confixfile')
        profile = file.get_profile('profile')

if __name__ == '__main__':
    unittest.main()
