# $Id: h.py,v 1.8 2006/06/27 15:08:59 jfasch Exp $

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

from base import CBaseBuilder
from dependency import Provide_CInclude
import namespace

from libconfix.core.iface import InterfacePiece
from libconfix.core.utils.error import Error

import os

class HeaderBuilder(CBaseBuilder):
    PROPERTY_INSTALLPATH = 'INSTALLPATH_CINCLUDE'
    
    class InstallPathConflict(Error):
        def __init__(self, old, new):
            Error.__init__(self, 'Cannot set install path to '+'/'.join(new)+' '
                           '(has already been set to '+'/'.join(old)+')')
            pass
        pass
                           
    def __init__(self, file, parentbuilder, package):
        # we exec the iface in the ctor, so the relevant members have
        # to be available before this.
        self.install_path_ = None
        
        CBaseBuilder.__init__(
            self,
            file=file,
            parentbuilder=parentbuilder,
            package=package)

        installpath = file.get_property(HeaderBuilder.PROPERTY_INSTALLPATH)
        if installpath is not None:
            self.check_installpath_(installpath)
            self.set_install_path(installpath)
            pass
        
        if self.install_path_ is None:
            self.set_install_path(namespace.find_unique_namespace(file.lines()))
            pass

        # provide ourselves.

        # we potentially have to provide ourselves in a twofold way:

        # in any case, we provide ourselves to the outside world. for
        # example, if we (the file we manage) is named "file.h", and
        # our install path is "some/directory", then we have to
        # provide our file like "some/directory/file.h". if our
        # install path is empty, we'll provide the file as "file.h",
        # of course. in short, we provide the file as it is included
        # by OTHERS: they'll say, #include <some/directory/file.h>, or
        # #include <file.h>, respectively.

        # on the other hand, local users - those which reside in the
        # same directory as we do - have to say #include "file.h",
        # regardless where it is installed.

        filename = self.file().name()
        outside_name = '/'.join(self.install_path() + [filename])
        self.add_provide(Provide_CInclude(outside_name))

        if outside_name != filename:
            self.add_internal_provide(Provide_CInclude(filename))
            pass
        
        pass

    def install_path(self):
        return self.install_path_
    def set_install_path(self, path):
        if self.install_path_ is not None:
            raise HeaderBuilder.InstallPathConflict(old=self.install_path_, new=path)
        self.install_path_ = path
        pass
    
    def iface_pieces(self):
        return CBaseBuilder.iface_pieces(self) + \
               [InterfacePiece(globals={'CHEADERBUILDER_': self},
                               lines=[code_])]

    def check_installpath_(self, path):
        for d in path:
            if len(d) == 0:
                raise Error(os.sep.join(self.file().relpath())+': '
                            'empty path component in install path '+str(path))
            pass
        pass
    pass


code_ = """
def INSTALLPATH(path):
    CHEADERBUILDER_.set_install_path(path)
    pass
"""
