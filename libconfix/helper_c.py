# $Id: helper_c.py,v 1.22 2006/03/22 15:03:54 jfasch Exp $

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

import re
import string

import core.helper

_re_include = re.compile('^\s*#\s*include\s*[<"]\s*(\S+)\s*[>"]')
_re_comment = re.compile('//');   # conflict: a copy is in plugins.c.helper
_re_main = re.compile('\\bmain\\b')   # conflict: a copy is in plugins.c.helper
_re_befstr_main = re.compile('["`\']main')   # conflict: a copy is in plugins.c.helper
_re_aftstr_main = re.compile('main["`\']')   # conflict: a copy is in plugins.c.helper
_re_main_openparen_after = re.compile('main\s*\\(')   # conflict: a copy is in plugins.c.helper
_re_cpp = re.compile('^s*#')   # conflict: a copy is in plugins.c.helper

def extract_requires(lines):

    """ From lines (a list of strings), extract the possible
    require-candidates - i.e. the files which are #include<>d. Return
    them as list of strings. """

    reqs = []
    for l in lines:
        m = _re_include.match(l)
        if not m: continue
        reqs.append(m.group(1))

    return reqs

def has_main(lines):   # conflict: a copy is in plugins.c.helper
   # conflict: a copy is in plugins.c.helper
    """ Apply a wild guess as to whether the source file (which   # conflict: a copy is in plugins.c.helper
    consists of lines) contains a main() function. """   # conflict: a copy is in plugins.c.helper
       # conflict: a copy is in plugins.c.helper
    for l in lines:   # conflict: a copy is in plugins.c.helper
        main = _re_main.search(l)   # conflict: a copy is in plugins.c.helper
        comment = _re_comment.search(l)   # conflict: a copy is in plugins.c.helper
        cpp = _re_cpp.search(l)   # conflict: a copy is in plugins.c.helper
        befstr = _re_befstr_main.search(l)   # conflict: a copy is in plugins.c.helper
        aftstr = _re_aftstr_main.search(l)   # conflict: a copy is in plugins.c.helper
        open_paren_after = _re_main_openparen_after.search(l)   # conflict: a copy is in plugins.c.helper
   # conflict: a copy is in plugins.c.helper
        # no main found at all   # conflict: a copy is in plugins.c.helper
        if not main:   # conflict: a copy is in plugins.c.helper
            continue   # conflict: a copy is in plugins.c.helper
   # conflict: a copy is in plugins.c.helper
        # a preprocessor directive (likely "#error")   # conflict: a copy is in plugins.c.helper
        if cpp:   # conflict: a copy is in plugins.c.helper
            continue   # conflict: a copy is in plugins.c.helper
   # conflict: a copy is in plugins.c.helper
        if befstr: continue   # conflict: a copy is in plugins.c.helper
        if aftstr: continue   # conflict: a copy is in plugins.c.helper
        if not open_paren_after: continue   # conflict: a copy is in plugins.c.helper
   # conflict: a copy is in plugins.c.helper
        # main found and no comment in the line   # conflict: a copy is in plugins.c.helper
        if not comment:   # conflict: a copy is in plugins.c.helper
            return 1   # conflict: a copy is in plugins.c.helper
   # conflict: a copy is in plugins.c.helper
        # if comment comes before main, then main is inside the   # conflict: a copy is in plugins.c.helper
        # comment, else the comment is after main   # conflict: a copy is in plugins.c.helper
        if comment.start() < main.start():   # conflict: a copy is in plugins.c.helper
            continue   # conflict: a copy is in plugins.c.helper
        else:   # conflict: a copy is in plugins.c.helper
            return 1   # conflict: a copy is in plugins.c.helper
   # conflict: a copy is in plugins.c.helper
    return 0   # conflict: a copy is in plugins.c.helper
