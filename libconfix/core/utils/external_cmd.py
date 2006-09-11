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

from error import Error

import os

def exec_program(program, dir, args=None, env=None, path=None):
    if os.path.isabs(program):
        the_program = program
    else:
        the_program = search_program(program=program, path=path)
        if the_program is None:
            raise Error('Program "'+program+'" not found in path')
        pass

    if args is None:
        the_args = []
    else:
        the_args = args
        pass

    if env is None:
        the_env = os.environ
    else:
        the_env = env
        pass
    
    chdirbackto = os.getcwd()
    os.chdir(dir)
    try:
        rv = os.spawnve(os.P_WAIT, the_program, [the_program] + the_args, the_env)
        if rv != 0:
            raise Error("spawnve("+the_program+") returned non-null ("+str(rv)+")")
        pass
    except Exception, e:
        os.chdir(chdirbackto)
        raise Error("Could not execute '"+the_program+' '+' '.join(the_args)+"' in directory '"+dir, [e])
    os.chdir(chdirbackto)
    pass

def search_program(program, path):
    ret = None
    if path is None:
        env_path = os.environ.get('PATH')
        if env_path is None:
            the_path = []
        else:
            the_path = env_path.split(os.pathsep)
            pass
        pass
    for dir in the_path:
        file = os.path.join(dir, program)
        if os.path.exists(file) and os.path.isfile(file) and os.access(file, os.X_OK):
            ret = file
            break
        pass
    return ret
