# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

from libconfix.core.setup import Setup
from libconfix.core.builder import Builder
from libconfix.core.automake import helper_automake

class InterixSetup(Setup):
    def setup_directory(self, directory_builder):
        super(InterixSetup, self).setup_directory(directory_builder)
        directory_builder.add_builder(
            InterixMacroDefiner(parentbuilder=directory_builder,
                                package=directory_builder.package()))
        pass
    pass

class InterixMacroDefiner(Builder):
    def __init__(self, parentbuilder, package):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        self.macroname_ = '_COMPILING_'+helper_automake.automake_name('_'.join(
            [self.package().name()]+\
            self.parentbuilder().directory().relpath(self.package().rootdirectory())))
        # tell everyone who's interested
        self.parentbuilder().directory().set_property('INTERIX_SHARED_COMPILING_MACRO', self.macroname_)
        pass

    def output(self):
        super(InterixMacroDefiner, self).output()
        self.parentbuilder().makefile_am().add_cmdlinemacro(self.macroname_, '1')
        pass
    pass