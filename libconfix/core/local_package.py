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
from makefile_py import Makefile_py
from iface import InterfacePiece
from hierarchy import DirectoryBuilder
from edgefinder import EdgeFinder
from filebuilder import FileBuilder

from libconfix.core.digraph.digraph import DirectedGraph
from libconfix.core import digraph
from libconfix.core.automake.configure_ac import Configure_ac 
from libconfix.core.automake.auxdir import AutoconfAuxDir
from libconfix.core.filesys.file import File
from libconfix.core.filesys.directory import Directory
from libconfix.core.utils.error import Error
from libconfix.core.utils import const

import os

class LocalPackage(Package):

    def __init__(self, root, setups):
        self.name_ = None
        self.version_ = None
        self.rootdirectory_ = root

        self.digraph_ = None
        self.local_nodes_ = None

        # the (contents of the) configure.ac we will be writing
        self.configure_ac_ = Configure_ac()

        # setup rootbuilder, and configure it with the setups we have.
        self.rootbuilder_ = DirectoryBuilder(
            directory=root,
            parentbuilder=None,
            package=self)
        for s in setups:
            self.rootbuilder_.add_setup(s.create(parentbuilder=self.rootbuilder_, package=self))
            pass

        # slurp in Makefile.py
        try:
            mfpyfile = root.get(const.MAKEFILE_PY)
            if mfpyfile is None:
                raise Error(const.MAKEFILE_PY+' missing in '+os.sep.join(root.abspath()))
            if not isinstance(mfpyfile, File):
                raise Error(os.sep.join(mfpyfile.abspath())+' is not a file')

            mfpy = PackageMakefile_py(file=mfpyfile, parentbuilder=self.rootbuilder_, package=self)
            self.rootbuilder_.add_configurator(mfpy)

            pass
        except Error, e:
            raise Error('Cannot initialize package in '+'/'.join(root.abspath()), [e])

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

    def configure_ac(self):
        return self.configure_ac_

    def rootbuilder(self):
        return self.rootbuilder_

    def digraph(self):
        assert self.digraph_ is not None, 'FIXME: nothing enlarged'
        return self.digraph_

    def nodes(self):
        assert self.digraph_ is not None, 'FIXME: nothing enlarged'
        return self.local_nodes_

    def enlarge(self, external_nodes):
        while True:
            num_enlarged = self.rootbuilder_.enlarge()
            if num_enlarged == 0:
                break
            self.local_nodes_ = self.rootbuilder_.nodes()
            all_nodes = set(self.local_nodes_)
            for n in external_nodes:
                all_nodes.add(n)
                pass
            self.digraph_ = DirectedGraph(nodes=all_nodes, edgefinder=EdgeFinder(all_nodes))
            for n in self.local_nodes_:
                n.relate(digraph=self.digraph_)
                pass
            pass
        pass

    def output(self):

        # PackageMakefile_py is supposed to have set package name and version
        if self.name_ is None:
            raise Error(mfpyfile.abspath()+': package name not set')
        if self.version_ is None:
            raise Error(mfpyfile.abspath()+': package version not set')

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

        # write my configure.ac
        
        cfg_ac = self.rootdirectory_.find(['configure.ac'])
        if cfg_ac is None:
            cfg_ac = File()
            self.rootdirectory_.add(name='configure.ac', entry=cfg_ac)
        else:
            cfg_ac.truncate()
            pass
        cfg_ac.add_lines(self.configure_ac_.lines())
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
        for n in self.digraph_.nodes():
            if n.responsible_builder() in dirbuilders:
                subdir_nodes.add(n)
                pass
            pass

        graph = digraph.utils.subgraph(digraph=self.digraph_,
                                       nodes=subdir_nodes)
        for n in digraph.toposort.toposort(digraph=graph, nodes=subdir_nodes):
            dirbuilder = n.responsible_builder()
            assert isinstance(dirbuilder, DirectoryBuilder)
            relpath = dirbuilder.directory().relpath()
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

        repofile = self.name() + '.repo'

        # jjjj write stuff
##         RepositoryFile(repofile).dump(self.install())

##         reponame = 'confixrepo'
##         self.makefile_am().add_lines(
##             self.makefile_am().define_directory(symbolicname=reponame,
##                                                 dirname=repo_automake.dir_for_automake()))
##         self.makefile_am().add_dir_primary(dir=reponame, primary='DATA', filename=repofile)

        self.rootbuilder_.makefile_am().add_extra_dist(repofile)
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
            if b.file().name() == const.MAKEFILE_PY:
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

        self.configure_ac_.set_unique_file_in_srcdir('/'.join(unique_file.relpath()))
        pass

    def collect_builders_(self):
        builders = set()
        self.collect_builders_recursive_(self.rootbuilder_, builders)
        return builders

    def collect_dirbuilders_(self):
        # argh. this could be much more intelligently
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

class PackageMakefile_py(Makefile_py):
    def __init__(self, file, parentbuilder, package):
        Makefile_py.__init__(self, file=file, parentbuilder=parentbuilder, package=package)
        pass

    def iface_pieces(self):
        return Makefile_py.iface_pieces(self) + [InterfacePiece(globals={'PACKAGE_': self.package()},
                                                                lines=[code_])]
    pass

code_ = """
from libconfix.core.utils.error import Error
import types

def PACKAGE_NAME(name):
    global PACKAGE_
    if PACKAGE_ is None:
        raise Error('PACKAGE_NAME() is only available in the toplevel Makefile.py')
    if type(name) is not types.StringType:
        raise Error('PACKAGE_NAME(): argument must be a string')
    PACKAGE_.set_name(name)
    pass

def PACKAGE_VERSION(version):
    global PACKAGE_
    if PACKAGE_ is None:
        raise Error('PACKAGE_VERSION() is only available in the toplevel Makefile.py')
    if type(version) is not types.StringType:
        raise Error('PACKAGE_VERSION(): argument must be a string')
    PACKAGE_.set_version(version)
    pass
"""
