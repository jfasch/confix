# $Id: subdirs.py,v 1.1 2006/07/04 14:36:48 jfasch Exp $

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

import helper_automake

class SubDir:

    def __init__(self, directory):
        self.directory_ = directory
        pass

    def makefile_am_lines(self):
        dir = self.dirname()
        cond = self.conditional()
        macro = self.make_macro()
        return ['if '+cond,
                macro+' = '+dir,
                'else',
                macro+' = ',
                'endif',
                '#kdevelop: '+macro+' = '+dir]

    def dirname(self):
        if len(self.directory_.relpath()):
            return '/'.join(self.directory_.relpath())
        else:
            return '.'
        pass

    def make_macro(self):

        """ Return a make macro that is supposed to be listed in the
        SUBDIRS variable."""

        return 'confix_subdir_'+helper_automake.automake_name('/'.join(self.directory_.relpath()))

    def enabled_shell_variable(self):

        """ Return a shell variable that signals whether the subdir is
        enabled or not."""

        return 'confix_subdir_enabled_'+helper_automake.automake_name(self.relpath_)

    def conditional(self):

        """ The automake conditional that signals whether the
        subdirectory is enabled or not."""

        return 'CONFIX_COND_SUBDIR_'+helper_automake.automake_name('/'.join(self.directory_.relpath())).upper()

    pass

class SubDirList:

    def __init__(self):
        self.subdirs_ = []
        pass

    def makefile_am_lines(self):
        ret = []
        if len(self.subdirs_):
            ret = helper_automake.format_make_macro(
                name='SUBDIRS',
                values=['$('+subdir.make_macro()+')' for subdir in self.subdirs_])
            ret.append('')
            for subdir in self.subdirs_:
                ret.extend(subdir.makefile_am_lines())
                pass
            pass
        return ret

    def append(self, s):
        assert isinstance(s, SubDir)
        self.subdirs_.append(s)
        pass

    def __getitem__(self, i):
        return self.subdirs_[i]

    def __iter__(self):
        return self.subdirs_.__iter__()

    def __len__(self):
        return len(self.subdirs_)

    pass
