# $Id: base.py,v 1.7 2006/06/27 15:08:59 jfasch Exp $

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

from dependency import Require_CInclude
import helper

from libconfix.core.filebuilder import FileBuilder
from libconfix.core.iface import InterfaceExecutor, InterfacePiece, CodePiece
from libconfix.core.utils.error import Error

import os
import re

# argh: '$' does not hit doze-like carriage return, but rather leaves
# it at the end of the match.

_re_confix = re.compile('//\s*CONFIX:([^\r\n]*)')

class CBaseBuilder(FileBuilder):
    def __init__(self, file, parentbuilder, coordinator):
        FileBuilder.__init__(
            self,
            file=file,
            parentbuilder=parentbuilder,
            coordinator=coordinator)

        for h_file in helper.extract_requires(file.lines()):
            self.add_require(
                Require_CInclude(filename=h_file,
                                 found_in='/'.join(self.file().relpath())))
            pass

        self.eval_iface_()
        
        pass

    def iface_pieces(self):
        return FileBuilder.iface_pieces(self) + \
               [InterfacePiece(globals={'CBASEBUILDER_': self},
                               lines=[code_])]

    def eval_iface_(self):

        # extract python lines from the file and evaluate them. search
        # for 'CONFIX:' lines, gathering blocks of consecutive
        # lines. 'blocks' is a dictionary, with the key being the
        # starting line number, and the value being a list of lines.

        lines = self.file().lines()

        codepieces = []

        lineno = 0
        current_startline = -1
        current_lines = None

        for l in lines:
            lineno = lineno + 1
            match = _re_confix.match(l)

            if match:
                # start new block if we don't yet have one
                if current_startline == -1:
                    current_startline = lineno
                    current_lines = []
                    pass
                current_lines.append(match.group(1))
            else:
                # terminate current block if any
                if current_startline != -1:
                    codepieces.append(CodePiece(start_lineno=current_startline, lines=current_lines))
                    current_startline = -1
                    current_lines = None
                    pass
                pass
            pass
        if current_startline != -1:
            codepieces.append(CodePiece(start_lineno=current_startline, lines=current_lines))
            pass

        try:
            execer = InterfaceExecutor(iface_pieces=self.iface_pieces())
            execer.execute_pieces(pieces=codepieces)
        except Error, e:
            raise Error('could not execute Confix code in '+'/'.join(self.file().relpath()), [e])

        pass
    pass

code_ = """
from libconfix.core.require import Require
from libconfix.plugins.c.dependency import Require_CInclude

def REQUIRE_H(filename, urgency=Require.URGENCY_IGNORE):
    if not filename:
        raise Error("REQUIRE_H(): need a non-null 'filename' parameter")
    if type(filename) is not types.StringType:
        raise Error("REQUIRE_H(): 'filename' parameter must be a string")
    if len(filename)==0:
        raise Error("REQUIRE_H(): need a non-zero 'filename' parameter")
    if not urgency in [URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR]:
        raise Error('REQUIRE_H(): urgency must be one of URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR')
    CBASEBUILDER_.add_require(Require_CInclude(
        filename=filename,
        found_in='/'.join(CBASEBUILDER_.file().relpath()),
        urgency=urgency))
"""
