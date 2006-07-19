#!/usr/bin/env python

# Copyright (C) 2002 Salomon Automation
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# $Id: confix.py,v 1.67 2006/03/22 15:03:53 jfasch Exp $

import sys
import os

import libconfix.const
import libconfix.todo
import libconfix.args

from libconfix.core.error import Error
from libconfix.buildable_mgr import BuildableManager
from libconfix.buildable_cxx import BuildableCXXCreator
from libconfix.buildable_c import BuildableCCreator
from libconfix.buildable_lex import BuildableLexCreator
from libconfix.buildable_yacc import BuildableYaccCreator
from libconfix.buildable_h import BuildableHeaderCreator
from libconfix.buildable_clusterer_c import BuildableClusterer_C
from libconfix.plugins.idl.creator import BuildableIDLCreator

def main():
    CONFIGFILES = libconfix.const.ARG_CONFIGFILES
    PROFILE = libconfix.const.ARG_PROFILE

    # set up default behaviour

    BuildableManager.instance.register_creator(r'\.(cxx|cc|cpp|C)$', BuildableCXXCreator())
    BuildableManager.instance.register_creator(r'\.(h|hpp)$', BuildableHeaderCreator())
    BuildableManager.instance.register_creator(r'\.c$', BuildableCCreator())
    BuildableManager.instance.register_creator(r'\.(l|ll)$', BuildableLexCreator())
    BuildableManager.instance.register_creator(r'\.(y|yy)$', BuildableYaccCreator())
    BuildableManager.instance.register_creator(r'\.idl$', BuildableIDLCreator())
    BuildableManager.instance.register_clusterer(BuildableClusterer_C())
    

    try:

        # bootstrap (:-) the args first time, only to get configfile
        # and profile name.

        bootstrap_params = libconfix.args.initial_params()
        (cmdline_params, cmdline_actions) = libconfix.args.parse_cmdline()
        libconfix.args.merge_params(bootstrap_params, cmdline_params)
        libconfix.args.finalize_params(bootstrap_params)

        configfiles = bootstrap_params[CONFIGFILES]
        profile = bootstrap_params[PROFILE]

        # second time, now for real.

        working_params = libconfix.args.initial_params()
        working_actions = []

        libconfix.args.merge_params(
            working_params,
            libconfix.args.conffile(configfiles, profile))

        (cmdline_params, cmdline_actions) = libconfix.args.parse_cmdline()
        libconfix.args.merge_params(working_params, cmdline_params)
        libconfix.args.merge_actions(working_actions, cmdline_actions)
        libconfix.args.finalize_params(working_params)
        libconfix.args.execute_params(working_params)

        # tell 'em what todo.
        libconfix.todo.TODO = working_actions
        libconfix.todo.ARGS = working_params

        # normally todo failures will throw exceptions, but this is in here just
        # as a safety measure.
        if libconfix.todo.todo():
            sys.exit(1)

    except Error, e:
        sys.stderr.write('***ERROR***\n')
        sys.stderr.write(`e`+'\n')
        sys.exit(1)

if __name__ == "__main__":
    main()
