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

from libconfix.core.entrybuilder import EntryBuilder
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.builder import BuilderSet
from libconfix.core.automake.makefile_am import Makefile_am
from libconfix.core.automake.file_installer import FileInstaller
from libconfix.core.local_node import LocalNode

from iface import DirectoryBuilderInterfaceProxy

class DirectoryBuilder(EntryBuilder):
    def __init__(self,
                 directory,
                 parentbuilder,
                 package):
        assert isinstance(directory, Directory)

        EntryBuilder.__init__(
            self,
            id=str(self.__class__) + '(' + '/'.join(directory.relpath(package.rootdirectory())) + ')',
            entry=directory,
            parentbuilder=parentbuilder,
            package=package)
        
        self.directory_ = directory
        self.configurator_ = None
        self.builders_ = BuilderSet()
        
        # names of files and directories that are to be ignored
        self.ignored_entries_ = set()

        # the (contents of the) Makefile.am we will be writing on
        # output()
        self.makefile_am_ = Makefile_am()

        # a helper that we use to install files intelligently (well,
        # more or less so).
        self.file_installer_ = FileInstaller()

        pass

    def directory(self):
        return self.entry()

    def makefile_am(self):
        return self.makefile_am_

    def file_installer(self):
        return self.file_installer_

    def add_ignored_entries(self, names):
        self.ignored_entries_ |= set(names)
        pass

    def entries(self):
        ret = []
        for name, entry in self.directory().entries():
            if name not in self.ignored_entries_:
                ret.append((name, entry))
                pass
            pass
        return ret

    def builders(self):
        return self.builders_

    def add_builder(self, b):
        self.builders_.add(b)
        pass

    def add_builders(self, builderlist):
        for b in builderlist:
            self.add_builder(b)
            pass
        pass

    def remove_builder(self, b):
        self.builders_.remove(b)
        pass

    def configurator(self):
        return self.configurator_

    def set_configurator(self, c):
        assert self.configurator_ is None
        self.configurator_ = c
        self.add_builder(c)
        pass

    def enlarge(self):
        super(DirectoryBuilder, self).enlarge()
        # have my configurator fiddle with me
        if self.configurator_ is not None:
            self.configurator_.enlarge()
            pass
        pass

    def node(self):
        managed_builders = []
        for b in self.builders_:
            if not isinstance(b, DirectoryBuilder):
                managed_builders.append(b)
                pass
            pass
        return LocalNode(responsible_builder=self,
                         managed_builders=managed_builders)

    def output(self):
        EntryBuilder.output(self)

        # 'make maintainer-clean' should remove the file we generate

        self.makefile_am_.add_maintainercleanfiles('Makefile.am')
        self.makefile_am_.add_maintainercleanfiles('Makefile.in')

        # let our builders write their output, recursively
        for b in self.builders_:
            b.output()
            assert b.base_output_called() == True, str(b)
            pass

        # the file installer is a little helper that relieves our
        # builders from having to care of how files are installed. our
        # builders use it to format their install wishes down to our
        # Makefile.am. so, basically, what I want to say is that we
        # have to flush the file installer into self.makefile_am_
        # *after* flushing the builders, and before flushing
        # self.makefile_am_

        # prepare the raw file object, and wrap a Makefile_am instance
        # around it.

        self.file_installer_.output(makefile_am=self.makefile_am_)

        # finally, write our Makefile.am.
        
        mf_am = self.directory_.find(['Makefile.am'])
        if mf_am is None:
            mf_am = File()
            self.directory_.add(name='Makefile.am', entry=mf_am)
        else:
            mf_am.truncate()
            pass

        mf_am.add_lines(self.makefile_am_.lines())

        pass
     
    def iface_pieces(self):
        return EntryBuilder.iface_pieces(self) + \
               [DirectoryBuilderInterfaceProxy(directory_builder=self)]
    pass
