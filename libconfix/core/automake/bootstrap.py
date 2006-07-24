# $Id: FILE-HEADER,v 1.4 2006/02/06 21:07:44 jfasch Exp $

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

from libconfix.core.utils.error import Error
from libconfix.core.utils import external_cmd

import os

def bootstrap(packageroot, aclocal_includedirs):
    aclocal(packageroot=packageroot, includedirs=aclocal_includedirs)
    autoheader(packageroot=packageroot)
    automake(packageroot=packageroot)
    autoconf(packageroot=packageroot)
    pass

def aclocal(packageroot, includedirs):
    aclocal_args = []
    for d in includedirs:
        aclocal_args.extend(['-I', d])
        pass
    external_cmd.exec_program(program='aclocal', args=aclocal_args, dir=packageroot)
    pass

def autoheader(packageroot):
    external_cmd.exec_program(program='autoheader', dir=packageroot)
    pass

def automake(packageroot):
    external_cmd.exec_program(program='automake',
                              args=['--foreign', '--add-missing', '--copy'],
                              dir=packageroot)
    pass

def autoconf(packageroot):
    external_cmd.exec_program(program='autoconf', dir=packageroot)
    pass

