# $Id: helper_automake.py,v 1.2 2006/07/04 14:36:48 jfasch Exp $

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

import types

def automake_name(name):

    """ If name contains letters which do not appear to be valid
    automake identifiers (m4 macros?), substitute them with
    '_'. automake complains (because of the '-') something like
    
    12: bad macro name `libentitycontainer_xmi-nsuml_a_SOURCES'
    
    FIXME: are there more characters which are invalid?

    @return: a copy of the input parameter with all the offending
    characters replaced

    """

    clean = name.replace('-', '_')
    clean = clean.replace('.', '_')
    clean = clean.replace('@', '_')
    clean = clean.replace('$', '_')
    clean = clean.replace('/', '_')
    clean = clean.replace('+', '_')
    return clean.replace('%', '_')

## def format_rule(targets, prerequisites=None, commands=None):

##     """ Format a Makefile rule. A rule consists of one or more
##     targets, zero or more prerequisites (or dependencies), and zero or
##     more commands.

##     Breaks the targets and prerequisites into multiple lines, with
##     line continuations ('\\'), if necessary.

##     @param targets: the rule's targets

##     @type targets: list of strings

##     @param prerequisites: the rule's prerequisites (dependencies)

##     @type prerequisites: list of strings

##     @param commands: the rule's commands.

##     @type commands: list of strings and lists. The latter form must
##     still be a shell-executable commandline, and the fact the a
##     command is a list of strings is merely used for line wrapping.
    
##     @return: a list of lines suitable for Makefile.am

##     @rtype: list of strings

##     """

##     assert len(targets)
##     targs = targets[:]
##     targs[-1] = targs[-1] + ':'

##     list = targs[:]
##     if prerequisites is not None:
##         list.extend(prerequisites)
##     retlist = __format_word_list(list)
    
##     if commands is not None:
##         for c in commands:
##             if type(c) is types.StringType:
##                 retlist.append('\t'+c)
##             elif (type(c) is types.ListType) or (type(c) is types.TupleType):
##                 retlist.extend(['\t'+l for l in __format_word_list(c)])
##             else: assert 0                
##     return retlist

## def format_dir(name, value):

##     """ Use this to format somthing like "confixrepodir =
##     $(datadir)/confix/repo" """

##     return format_list(name, [value])

## def format_make_macro(name, values):

##     # BACKSLASH_MITIGATOR: we wrap long lines with backslashes, so
##     # that various tools are happy. for example, config.status scans
##     # Makefile.in using grep. on several Unices (AIX, HP-UX I seem to
##     # remember), grep does not accept lines of inifinite length.

##     # certain make macros - AM_CPPFLAGS for example - end up being
##     # long lists of items most of which are autoconf @blah@
##     # substitutions, some of which end up being substituted with the
##     # empty string. if such an empty substitution is on a single line
##     # at the end of such a long list, the previous line contains a
##     # trailing backslash, followed by an empty line. some make
##     # implementations (HP-UX, again) handle this kind of consciousless
##     # and scan through until they find something meaningful, which
##     # they then consider part of th list. argh.

##     # however, the solution is to terminate every list with a macro
##     # that expands to nothing, just to make bogus make's scan
##     # algorithm happy.

##     return format_list(name, values + ['$(CONFIX_BACKSLASH_MITIGATOR)'])    

## def format_list(name, values):
##     return format_word_list([name+' ='] + values)

