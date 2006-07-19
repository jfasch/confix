# $Id: rule.py,v 1.1 2006/07/04 14:36:48 jfasch Exp $

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

class Rule:

    """ A Makefile rule. A rule consists of one or more targets, zero
    or more prerequisites (or dependencies), and zero or more
    commands.

    @param targets: the rule's targets

    @type targets: list of strings

    @param prerequisites: the rule's prerequisites (dependencies)

    @type prerequisites: list of strings

    @param commands: the rule's commands.

    @type commands: list of strings and lists. The latter form must
    still be a shell-executable commandline, and the fact the a
    command is a list of strings is merely used for line wrapping."""

    def __init__(self, targets, prerequisites=None, commands=None):
        self.targets_ = targets
        self.prerequisites_ = prerequisites
        self.commands_ = commands
        pass

    def targets(self):
        return self.targets_

    def prerequisites(self):
        return self.prerequisites_

    def commands(self):
        return self.commands_

    def lines(self):

        """ Compose a list of lines that constitute the rule as it is
        written in a Makefile(.am). Breaks the targets and
        prerequisites into multiple lines, with line continuations
        ('\\'), if necessary.

        @return: a list of lines suitable for Makefile.am

        @rtype: list of strings

        """

        assert len(self.targets_)
        targs = self.targets_[:]
        targs[-1] = targs[-1] + ':'

        list = targs[:]
        if self.prerequisites_ is not None:
            list.extend(self.prerequisites_)
        retlist = helper_automake.format_word_list(list)

        if commands is not None:
            for c in commands:
                if type(c) is types.StringType:
                    retlist.append('\t'+c)
                elif (type(c) is types.ListType) or (type(c) is types.TupleType):
                    retlist.extend(['\t'+l for l in __format_word_list(c)])
                else: assert 0
                pass
            pass
        
        return retlist
        
