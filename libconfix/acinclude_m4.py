# $Id: acinclude_m4.py,v 1.3 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2005 Salomon Automation

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

from core.error import Error
from paragraph import ParagraphSet
import const
import core.helper

import types

class ACInclude_m4:

    """ Encapsulates everything a package's acinclude.m4 file does,
    including writing that file. """

    def __init__(self):
        self.paragraphs_ = ParagraphSet()
        pass

    def add_paragraph(self, paragraph):
        self.paragraphs_.add(paragraph)
        
    def add_paragraphs(self, paragraphset):
        self.paragraphs_ += paragraphset
        
    def output(self):

        """ Write the contents to the file acinclude.m4 in the current
        working directory. """

        lines = []
        lines.append('# DO NOT EDIT! This file was automatically generated')
        lines.append('# by Confix version '+const.CONFIX_VERSION)
        lines.extend(self.paragraphs_.lines_for_acinclude_m4())

        try:
            core.helper.write_lines_to_file_if_changed('acinclude.m4', lines)
        except Error, e:
            raise Error("Could not write acinclude.m4", [e])
        
