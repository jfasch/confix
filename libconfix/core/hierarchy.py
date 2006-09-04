# $Id: hierarchy.py,v 1.15 2006/07/13 20:27:24 jfasch Exp $

# Copyright (C) 2002-2006 Salomon Automation

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

from builder import Builder, BuilderSet
from entrybuilder import EntryBuilder
from setup import SetupFactory, Setup
from makefile_py import Makefile_py
from depindex import ProvideMap
from local_node import LocalNode

from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.automake.makefile_am import Makefile_am
from libconfix.core.utils.error import Error
from libconfix.core.utils import const
from libconfix.core.digraph import utils, toposort

import re
import types
import os

class DirectorySetupFactory(SetupFactory):
    def __init__(self):
        SetupFactory.__init__(self)
        pass
    def create(self, parentbuilder, package):
        return DirectorySetup(parentbuilder=parentbuilder, package=package)
    pass

class DirectorySetup(Setup):
    def __init__(self, parentbuilder, package):
        assert isinstance(parentbuilder, DirectoryBuilder)
        Setup.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        self.handled_directories_ = set()
        pass

    def clone(self, parentbuilder, package):
        return DirectorySetup(
            parentbuilder=parentbuilder,
            package=package)

    def enlarge(self):
        newbuilders = []
        errors = []
        for name, entry in self.parentbuilder().entries():
            if not isinstance(entry, Directory):
                continue
            if entry in self.handled_directories_:
                continue
            mfpyfile = entry.get(const.MAKEFILE_PY)
            if mfpyfile is None:
                continue
            if not isinstance(mfpyfile, File):
                errors.append(Error(mfpyfile.relpath()+' is not a file'))
                continue
            try:
                dirbuilder = DirectoryBuilder(
                    directory=entry,
                    parentbuilder=self.parentbuilder(),
                    package=self.package())
                for b in self.parentbuilder().setups():
                    dirbuilder.add_setup(b.clone(parentbuilder=dirbuilder,
                                                 package=self.package()))
                    pass
                mfpy = Makefile_py(file=mfpyfile,
                                   parentbuilder=dirbuilder,
                                   package=self.package())
                dirbuilder.add_configurator(mfpy)
                newbuilders.append((entry, dirbuilder))
            except Error, e:
                errors.append(Error('Error executing '+os.sep.join(mfpyfile.relpath()), [e]))
                pass
            pass
        if len(errors):
            raise Error('There were errors in directory '+\
                        os.sep.join(self.parentbuilder().directory().relpath()), errors)
        for dir, b in newbuilders:
            self.handled_directories_.add(dir)
            self.parentbuilder().add_builder(b)
            pass
        return len(newbuilders) + Setup.enlarge(self)
    
    pass

class DirectoryBuilder(EntryBuilder):
    def __init__(self,
                 directory,
                 parentbuilder,
                 package):
        assert isinstance(directory, Directory)

        EntryBuilder.__init__(
            self,
            id=str(self.__class__) + '(' + '/'.join(directory.relpath()) + ')',
            entry=directory,
            parentbuilder=parentbuilder,
            package=package)
        
        self.directory_ = directory
        self.configurators_ = []
        self.setups_ = []
        self.builders_ = BuilderSet()
        
        # names of files and directories that are to be ignored
        self.ignored_entries_ = set()

        # the (contents of the) Makefile.am we will be writing on output()
        self.makefile_am_ = Makefile_am()

        pass

    def directory(self):
        return self.entry()

    def makefile_am(self):
        return self.makefile_am_

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

    def remove_builder(self, b):
        self.builders_.remove(b)
        pass

    def add_configurator(self, c):
        self.configurators_.append(c)
        self.add_builder(c)
        pass

    def add_setup(self, b):
        self.setups_.append(b)
        self.add_builder(b)
        pass

    def setups(self):
        return self.setups_

    def enlarge(self):
        # first of all, enlarge() our configurators. at the time of
        # this writing, the only configurator I see is the Makefile.py
        # object, configuring all setups.

        for c in self.configurators_:
            c.enlarge()
            pass
        
        total_more = 0
        while True:
            more = 0
            # copy what we will be iterating over because we will
            # enlarge self.builders_ as we go.
            builders = self.builders_.values()[:]
            for b in builders:
                more += b.enlarge()
                assert b.base_enlarge_called(), str(b)
                pass
            if more == 0:
                break
            total_more += more
            pass
        return total_more + Builder.enlarge(self)

    def nodes(self):

        ret_nodes = set()
        
        all_builders = set([self] + self.builders().values())
        builders_with_nodes = set()

        # collect nodes of builders which have their own nodes.

        for b in self.builders():
            nodes = b.nodes()
            if len(nodes):
                ret_nodes |= nodes
                builders_with_nodes.add(b)
                pass
            pass
        
        # compose our own node that will manage our builders which
        # don't have their own node.

        ret_nodes.add(LocalNode(responsible_builder=self,
                                managed_builders=all_builders-builders_with_nodes))

        return ret_nodes

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
        pass

        # prepare the raw file object, and wrap a Makefile_am instance
        # around it.
        
        mf_am = self.directory_.find(['Makefile.am'])
        if mf_am is None:
            mf_am = File()
            self.directory_.add(name='Makefile.am', entry=mf_am)
        else:
            mf_am.truncate()
            pass

        mf_am.add_lines(self.makefile_am_.lines())

        pass
     
    pass

