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

from package import Package
from installed_package import InstalledPackage
from confix2_in import Confix2_in
from iface import InterfacePiece
from hierarchy import DirectoryBuilder
from edgefinder import EdgeFinder
from filebuilder import FileBuilder

from libconfix.core import digraph
from libconfix.core.automake import repo_automake
from libconfix.core.automake.auxdir import AutoconfAuxDir
from libconfix.core.automake.configure_ac import Configure_ac 
from libconfix.core.automake.acinclude_m4 import ACInclude_m4 
from libconfix.core.digraph.digraph import DirectedGraph
from libconfix.core.filesys.directory import Directory
from libconfix.core.filesys.file import File
from libconfix.core.repo.repofile import RepositoryFile
from libconfix.core.utils import const
from libconfix.core.utils.error import Error

import os

class LocalPackage(Package):

    def __init__(self, rootdirectory, setups):
        self.name_ = None
        self.version_ = None
        self.rootdirectory_ = rootdirectory

        self.digraph_ = None
        self.local_nodes_ = None

        # the (contents of) configure.ac and acinclude.m4 we will be
        # writing
        self.configure_ac_ = Configure_ac()
        self.acinclude_m4_ = ACInclude_m4()

        # setup rootbuilder, and configure it with the setups we have.
        self.rootbuilder_ = DirectoryBuilder(
            directory=rootdirectory,
            parentbuilder=None,
            package=self)
        for s in setups:
            self.rootbuilder_.add_setup(s.create(parentbuilder=self.rootbuilder_, package=self))
            pass

        # slurp in Confix2.in
        try:
            confix2_in_file = rootdirectory.get(const.CONFIX2_IN)
            if confix2_in_file is None:
                raise Error(const.CONFIX2_IN+' missing in '+os.sep.join(rootdirectory.abspath()))
            if not isinstance(confix2_in_file, File):
                raise Error(os.sep.join(confix2_in_file.abspath())+' is not a file')

            confix2_in = PackageConfix2_in(file=confix2_in_file, parentbuilder=self.rootbuilder_, package=self)
            self.rootbuilder_.add_configurator(confix2_in)

            pass
        except Error, e:
            raise Error('Cannot initialize package in '+'/'.join(rootdirectory.abspath()), [e])

        # setup our autoconf auxiliary directory. this a regular
        # builder by itself, but plays a special role for us because
        # we use it to put, well, auxiliary files in.
        dir = self.rootdirectory_.find([const.AUXDIR])
        if dir is None:
            dir = Directory()
            self.rootdirectory_.add(name=const.AUXDIR, entry=dir)
            pass
        self.auxdir_ = AutoconfAuxDir(directory=dir, parentbuilder=self.rootbuilder_, package=self)
        self.rootbuilder_.add_builder(self.auxdir_)
        pass

    def __str__(self):
        return 'LocalPackage:'+str(self.name_)
    
    def name(self):
        return self.name_
    def set_name(self, name):
        assert self.name_ is None
        self.name_ = name
        pass
    def version(self):
        return self.version_
    def set_version(self, version):
        assert self.version_ is None
        self.version_ = version
        pass

    def rootdirectory(self):
        return self.rootdirectory_

    def configure_ac(self):
        return self.configure_ac_
    def acinclude_m4(self):
        return self.acinclude_m4_

    def rootbuilder(self):
        return self.rootbuilder_

    def digraph(self):
        assert self.digraph_ is not None, 'FIXME: nothing enlarged'
        return self.digraph_

    def nodes(self):
        assert self.digraph_ is not None, 'FIXME: nothing enlarged'
        return self.local_nodes_

    def enlarge(self, external_nodes):
        self.rootbuilder_.enlarge()
        while True:
            self.local_nodes_ = self.rootbuilder_.nodes()
            all_nodes = set(self.local_nodes_)
            for n in external_nodes:
                all_nodes.add(n)
                pass
            self.digraph_ = DirectedGraph(nodes=all_nodes, edgefinder=EdgeFinder(all_nodes))
            for n in self.local_nodes_:
                n.relate(digraph=self.digraph_)
                pass
            if self.rootbuilder_.enlarge() == 0:
                break
            pass
            
        # <paranoia>
        for b in self.collect_builders_():
            assert b.base_relate_called() == True, str(b)
            pass
        # </paranoia>
        pass

    def output(self):

        # PackageConfix2_in is supposed to have set package name and version
        if self.name_ is None:
            raise Error(confix2_in_file.abspath()+': package name not set')
        if self.version_ is None:
            raise Error(confix2_in_file.abspath()+': package version not set')

        # we will be writing two files in the package's root
        # directory. configure.ac is our responsbility - we will have
        # to create it etc.. the other file, Makefile.am, is not our
        # responsbility, but that of our rootbuilder; we only use it
        # to put our stuff in (SUBDIRS, for example).

        self.output_stock_autoconf_()
        self.output_options_()
        self.output_subdirs_()
        self.output_repo_()
        self.output_unique_file_()

        # recursively write the package's output
        self.rootbuilder_.output()

        # write my configure.ac and acinclude.m4
        
        configure_ac = self.rootdirectory_.find(['configure.ac'])
        if configure_ac is None:
            configure_ac = self.rootdirectory_.add(name='configure.ac', entry=File())
        else:
            configure_ac.truncate()
            pass
        configure_ac.add_lines(self.configure_ac_.lines())

        acinclude_m4 = self.rootdirectory_.find(['acinclude.m4'])
        if acinclude_m4 is None:
            acinclude_m4 = self.rootdirectory_.add(name='acinclude.m4', entry=File())
        else:
            acinclude_m4.truncate()
            pass
        acinclude_m4.add_lines(self.acinclude_m4_.lines())
        pass

    def install(self):
        return InstalledPackage(
            name=self.name(),
            version=self.version(),
            nodes=[n.install() for n in self.nodes()])
    
    def output_stock_autoconf_(self):
        self.configure_ac_.set_packagename(self.name())
        self.configure_ac_.set_packageversion(self.version())

        # we require autoconf 2.52 because it has (possibly among
        # others) AC_HELP_STRING(), and can go into subsubdirs from
        # the toplevel.

        self.configure_ac_.set_minimum_autoconf_version('2.52')

        # we never pass AC_DEFINE'd macros on the commandline

        self.configure_ac_.add_ac_config_headers('config.h')
        pass

    def output_options_(self):
        # our minimum required automake version is 1.9 
        self.rootbuilder_.makefile_am().add_automake_options('1.9')

        # enable dist'ing in the following formats
        self.rootbuilder_.makefile_am().add_automake_options('dist-bzip2')
        self.rootbuilder_.makefile_am().add_automake_options('dist-shar')
        self.rootbuilder_.makefile_am().add_automake_options('dist-zip')
        pass

    def output_subdirs_(self):

        # there is mention of our subdirectories in both the toplevel
        # Makefile.am and configure.ac.

        # arrange to compose the SUBDIRS variable of the package root
        # directory ('.') and all the other directories in the
        # package.
        
        # SUBDIRS has to be topologically correct. sort out all nodes
        # that correspond to subdirectories of the package. from the
        # global digraph, make a subgraph with those nodes. compute
        # the topological order, and from that list, generate the
        # output.

        dirbuilders = self.collect_dirbuilders_()

        subdir_nodes = set()
        for n in self.local_nodes_:
            if n.responsible_builder() in dirbuilders:
                subdir_nodes.add(n)
                pass
            pass

        graph = digraph.utils.subgraph(digraph=self.digraph_,
                                       nodes=subdir_nodes)
        for n in digraph.toposort.toposort(digraph=graph, nodes=subdir_nodes):
            dirbuilder = n.responsible_builder()
            assert isinstance(dirbuilder, DirectoryBuilder)
            relpath = dirbuilder.directory().relpath(self.rootdirectory_)
            if len(relpath):
                dirstr = '/'.join(relpath)
            else:
                dirstr = '.'
                pass
            self.rootbuilder_.makefile_am().add_subdir(dirstr)
            self.configure_ac().add_ac_config_files('/'.join([dirstr, 'Makefile']))
            pass

        pass

    def output_repo_(self):
        # write package description file. add stuff to Makefile.am
        # that takes care to install it. put it into the dist-package.

        repofilename = self.name() + '.repo'
        repofile = self.rootdirectory_.add(name=repofilename, entry=File())

        RepositoryFile(file=repofile).dump(package=self.install())

        self.rootbuilder_.makefile_am().define_install_directory(
            symbolicname='confixrepo',
            dirname=repo_automake.dir_for_automake())
        self.rootbuilder_.makefile_am().add_to_install_directory(
            symbolicname='confixrepo',
            family='DATA',
            files=[repofilename])
        self.rootbuilder_.makefile_am().add_extra_dist(
            name=repofilename)
        
        pass

    def output_unique_file_(self):
        
        # AC_CONFIG_SRCDIR (for paranoia and sanity checks): we need
        # one unique file in the tree, as a meaningful argument to
        # AC_CONFIG_SRCDIR.

        goodfile = notsogoodfile = None
        for b in self.collect_builders_():
            if not isinstance(b, FileBuilder):
                continue
            goodfile = None
            notsogoodfile = None
            if b.file().name() == const.CONFIX2_IN:
                notsogoodfile = b.file()
            else:
                goodfile = b.file()
                break
            pass
        if goodfile:
            unique_file = goodfile
        elif notsogoodfile:
            unique_file = notsogoodfile
        else:
            raise Error('Not even one file handled by any submodule of '
                        'package '+self.name()+"; "
                        "probably the current working directory "
                        "("+os.getcwd()+") is not "
                        "the package root directory?")

        self.configure_ac_.set_unique_file_in_srcdir('/'.join(unique_file.relpath(self.rootdirectory_)))
        pass

    def collect_builders_(self):
        builders = set()
        self.collect_builders_recursive_(self.rootbuilder_, builders)
        return builders

    def collect_dirbuilders_(self):
        # argh. this could be done much more intelligently
        dirbuilders = set()
        for b in self.collect_builders_():
            if isinstance(b, DirectoryBuilder):
                dirbuilders.add(b)
                pass
            pass
        return dirbuilders
    
    def collect_builders_recursive_(self, builder, found):
        found.add(builder)
        if isinstance(builder, DirectoryBuilder):
            for b in builder.builders():
                self.collect_builders_recursive_(b, found)
                pass
            pass
        pass

    pass

class PackageConfix2_in(Confix2_in):
    def __init__(self, file, parentbuilder, package):
        Confix2_in.__init__(self, file=file, parentbuilder=parentbuilder, package=package)
        pass

    def iface_pieces(self):
        return Confix2_in.iface_pieces(self) + [InterfacePiece(globals={'PACKAGE_': self.package()},
                                                               lines=[code_])]
    pass

code_ = """
from libconfix.core.utils.error import Error
import types

def PACKAGE_NAME(name):
    global PACKAGE_
    if PACKAGE_ is None:
        raise Error('PACKAGE_NAME() is only available in the toplevel Confix2.in')
    if type(name) is not types.StringType:
        raise Error('PACKAGE_NAME(): argument must be a string')
    PACKAGE_.set_name(name)
    pass

def PACKAGE_VERSION(version):
    global PACKAGE_
    if PACKAGE_ is None:
        raise Error('PACKAGE_VERSION() is only available in the toplevel Confix2.in')
    if type(version) is not types.StringType:
        raise Error('PACKAGE_VERSION(): argument must be a string')
    PACKAGE_.set_version(version)
    pass
"""
