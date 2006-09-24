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

from h import HeaderBuilder
from libconfix.core.builder import Builder
from libconfix.core.automake import helper_automake
from libconfix.core.automake.rule import Rule
from libconfix.core.utils import const

import re

class Installer(Builder):
    def __init__(self,
                 parentbuilder,
                 package):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)            
        
        self.install_directories_ = {}
        pass

    def enlarge(self):
        Builder.enlarge(self)
        
        # fixme: performance: maybe it is cheaper to keep the
        # information and just edit it. nobody knows.
        self.install_directories_ = {}
        curbuilders = self.parentbuilder().builders().values()
        for b in curbuilders:
            if not isinstance(b, HeaderBuilder):
                continue
            if b.install_path() is None:
                continue
            key = '/'.join(b.install_path())
            dirdef = self.install_directories_.setdefault(key, (b.install_path(), []))
            dirdef[1].append(b.file().name())
            pass
        return 0

##     def output(self):
##         Builder.output(self)

##         # register public header files for installation

##         for (installpath, files) in self.install_directories_.values():
##             if len(installpath) == 0:
##                 # no need to define subdirectory; take predefined
##                 symbolicname = ''
##             else:
##                 symbolicname = 'publicheader_'+compute_install_dirname_(installpath)
##                 self.parentbuilder().makefile_am().define_install_directory(
##                     symbolicname=symbolicname,
##                     dirname='/'.join(['$(includedir)']+installpath))
##                 pass
##             self.parentbuilder().makefile_am().add_to_install_directory(
##                 symbolicname=symbolicname,
##                 family='HEADERS',
##                 files=files)
##             pass

##         # now for the private header files. this is a bit more
##         # complicated as we have to do it by hand, using the all-local
##         # hook.

##         self.parentbuilder().makefile_am().add_all_local('confix-install-local')
##         self.parentbuilder().makefile_am().add_clean_local('confix-clean-local')

##         install_local_rule = Rule(targets=['confix-install-local'], prerequisites=[], commands=[])
##         clean_local_rule = Rule(targets=['confix-clean-local'], prerequisites=[], commands=[])
##         self.parentbuilder().makefile_am().add_element(install_local_rule)        
##         self.parentbuilder().makefile_am().add_element(clean_local_rule)

##         # add mkdir rules for every subdirectory
##         for (installpath, files) in self.install_directories_.values():
##             targetdir = '/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR] + installpath)
##             self.parentbuilder().makefile_am().add_element(
##                 Rule(targets=[targetdir],
##                      prerequisites=[],
##                      commands=['-$(mkinstalldirs) '+targetdir]))
##             pass

##         # copy files
##         for (installpath, files) in self.install_directories_.values():
##             targetdir = '/'.join(['$(top_builddir)', const.LOCAL_INCLUDE_DIR] + installpath)
##             for f in files:
##                 targetfile = '/'.join([targetdir, f])
##                 self.parentbuilder().makefile_am().add_element(
##                     Rule(targets=[targetfile],
##                          prerequisites=[targetdir, f],
##                          commands=['cp -fp $(srcdir)/'+f+' '+targetdir,
##                                    'chmod 0444 '+targetfile]))
##                 self.parentbuilder().makefile_am().add_element(
##                     Rule(targets=[targetfile+'-clean'],
##                          prerequisites=[],
##                          commands=['rm -f '+targetfile]))
##                 install_local_rule.add_prerequisite(targetfile)
##                 clean_local_rule.add_prerequisite(targetfile+'-clean')
##                 pass
##             pass
##         pass

    def output(self):
        Builder.output(self)

        # register public and private header files for installation

        # fixme: is it right to not distinguish between public and
        # private?

        for installpath, files in self.install_directories_.values():
            for f in files:
                self.parentbuilder().file_installer().add_public_header(filename=f, dir=installpath)
                self.parentbuilder().file_installer().add_private_header(filename=f, dir=installpath)
                pass
            pass
        pass

    pass        

re_subst = re.compile('(^[_\d]|\W)')
def compute_install_dirname_(path):
    relpathstr = '/'.join(path)
    return helper_automake.automake_name(re_subst.sub('', relpathstr))
