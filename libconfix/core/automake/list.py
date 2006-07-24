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

class List:

    # BACKSLASH_MITIGATOR: we wrap long lines with backslashes, so
    # that various tools are happy. for example, config.status scans
    # Makefile.in using grep. on several Unices (AIX, HP-UX I seem to
    # remember), grep does not accept lines of inifinite length.

    # certain make macros - AM_CPPFLAGS for example - end up being
    # long lists of items most of which are autoconf @blah@
    # substitutions, some of which end up being substituted with the
    # empty string. if such an empty substitution is on a single line
    # at the end of such a long list, the previous line contains a
    # trailing backslash, followed by an empty line. some make
    # implementations (HP-UX, again) handle this kind of consciousless
    # and scan through until they find something meaningful, which
    # they then consider part of th list. argh.

    # however, the solution is to terminate every list with a macro
    # that expands to nothing, just to make bogus make's scan
    # algorithm happy.
    
    def __init__(self, name, values, mitigate):
        self.name_ = name
        self.values_ = values[:]
        self.mitigate_ = mitigate
        pass
    def __iter__(self):
        return self.values_.__iter__()
    def __len__(self):
        return self.values_.__len__()
    def __getitem__(self, index):
        return self.values_.__getitem__(index)
    def name(self):
        return self.name_
    def values(self):
        return self.values_
    def add_value(self, value):
        self.values_.append(value)
        pass
    def lines(self):
        if len(self.values_) == 0:
            return []
        list = [self.name_+' ='] + self.values_
        if self.mitigate_:
            list.append('$(CONFIX_BACKSLASH_MITIGATOR)')
            pass
        return format_word_list_(list)
    pass

def format_word_list_(words):
    bare_lines = []

    line = ''
    for w in words:
        if len(line) + len(w) + 1 < 70:
            # word won't overflow the current line; consume word
            if len(line): line = line + ' ' + w
            else: line = w
        else:
            if len(line) > 0:
                # line is already full; flush it and consume word
                bare_lines.append(line)
                line = w
            else:
                # word is longer than max line length. make a single
                # line of it.
                line = w

    if len(line):
        bare_lines.append(line)

    # prepend spaces to all but the first line. append '\' to all but
    # the last line. add line to return value.

    ret_lines = []

    for i in range(len(bare_lines)):
        line = bare_lines[i]
        if i != 0: line = '    ' + line
        if i < len(bare_lines)-1:
            line = line + ' \\'
        ret_lines.append(line)

    return ret_lines

