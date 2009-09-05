# Copyright (C) 2009 Joerg Faschingbauer

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

from libconfix.plugins.cmake.setup import CMakeSetup
from libconfix.plugins.cmake.modules_dir_builder import ModulesDirectoryBuilder

from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.machinery.local_package import LocalPackage
from libconfix.core.hierarchy.explicit_setup import ExplicitDirectorySetup
from libconfix.core.utils import const

import unittest

class ModulesInMemorySuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(ModulesInMemoryTest('test_ok'))
        self.addTest(ModulesInMemoryTest('test_good_duplicate'))
        self.addTest(ModulesInMemoryTest('test_bad_duplicate'))
        self.addTest(ModulesInMemoryTest('test_live'))
        pass
    pass

class ModulesInMemoryTest(unittest.TestCase):
    def test_ok(self):
        modules_dir_builder = ModulesDirectoryBuilder(directory=Directory())
        modules_dir_builder.add_module_file(name='mod1.cmake', lines=['mod1'])
        modules_dir_builder.add_module_file(name='mod2.cmake', lines=['mod2'])

        mod1 = modules_dir_builder.directory().get('mod1.cmake')
        mod2 = modules_dir_builder.directory().get('mod2.cmake')
        self.failIfEqual(mod1, None)
        self.failIfEqual(mod2, None)

        self.failUnlessEqual(mod1.lines(), ['mod1'])        
        self.failUnlessEqual(mod2.lines(), ['mod2'])        
        pass
    
    def test_good_duplicate(self):
        modules_dir_builder = ModulesDirectoryBuilder(directory=Directory())
        modules_dir_builder.add_module_file(name='mod1.cmake', lines=['mod1'])
        modules_dir_builder.add_module_file(name='mod1.cmake', lines=['mod1'])

        mod1 = modules_dir_builder.directory().get('mod1.cmake')
        self.failIfEqual(mod1, None)
        self.failUnlessEqual(mod1.lines(), ['mod1'])        
        pass

    def test_bad_duplicate(self):
        modules_dir_builder = ModulesDirectoryBuilder(directory=Directory())
        modules_dir_builder.add_module_file(name='mod1.cmake', lines=['mod1'])
        try:
            modules_dir_builder.add_module_file(name='mod1.cmake', lines=['mod2'])
        except ModulesDirectoryBuilder.DuplicateError:
            return
        self.fail()
        pass

    def test_live(self):
        fs = FileSystem(path=[])
        fs.rootdirectory().add(
            name=const.CONFIX2_PKG,
            entry=File(lines=['PACKAGE_NAME("ModulesInMemoryTest")',
                              'PACKAGE_VERSION("1.2.3")']))
        fs.rootdirectory().add(
            name=const.CONFIX2_DIR,
            entry=File(lines=['from libconfix.plugins.cmake.out_cmake import find_cmake_output_builder',
                              'from libconfix.core.machinery.builder import Builder',
                              'class ModuleAdder(Builder):',
                              '     def output(self):',
                              '         super(ModuleAdder, self).output()',
                              '         cmake_out = find_cmake_output_builder(self.parentbuilder())',
                              '         cmake_out.add_module_file(name="TestModule.cmake",',
                              '                                   lines=["my content"])',
                              '         pass',
                              '     pass',
                              '     def locally_unique_id(self):',
                              '         return str(self.__class__)',
                              'ADD_BUILDER(ModuleAdder())']))
        package = LocalPackage(rootdirectory=fs.rootdirectory(), setups=[CMakeSetup(), ExplicitDirectorySetup()])
        package.boil(external_nodes=[])
        package.output()

        modulefile = fs.rootdirectory().find(['confix-admin', 'cmake', 'Modules', 'TestModule.cmake'])
        self.failIf(modulefile is None)
        self.failIf(modulefile.lines()[0] != 'my content')

        pass

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(ModulesInMemorySuite())
    pass
