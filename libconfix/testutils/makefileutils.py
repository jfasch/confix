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

import re

rex_macro = re.compile(r'^([\w_\.]+)\s*=\s(.*)$')
rex_listsep = re.compile(r'\s+')
rex_target_prerequisite = re.compile(r'^\s*(.*)\s*:\s*(.*)\s*$')

def collapse_continuations(lines):
    ret = []
    cur_line = None
    for l in lines:
        if cur_line:
            cur_line += l
        else:
            cur_line = l
            pass
        if not cur_line.endswith('\\'):
            ret.append(cur_line)
            cur_line = None
        else:
            cur_line = cur_line[0:-1]
            pass
        pass
    assert cur_line is None
    return ret

def find_macro(name, lines):
    for l in collapse_continuations(lines):
        match = rex_macro.search(l)
        if not match:
            continue
        if match.group(1) == name:
            return match.group(2)
        continue
    return None

def find_list(name, lines):
    value = find_macro(name, lines)
    if value:
        values = rex_listsep.split(value)
        # some lists are terminated by
        # $(CONFIX_BACKSLASH_MITIGATOR). eliminate that.
        if len(values) > 0 and values[-1] == '$(CONFIX_BACKSLASH_MITIGATOR)':
            del values[-1]
            pass
        return values
    return None

## def find_rules(targets, lines):
##     for l in collapse_continuations(lines):
##         match = rex_target_prerequisite.search(l)
##         if match:
            
