# $Id: helper_configure_in.py,v 1.1 2005/11/06 22:01:11 jfasch Exp $

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

from paragraph import OrderedParagraphSet, Paragraph

# rough ordering scheme according to the recommendations in the
# autotools book , p.31

ORDER_BOILERPLATE = 0
ORDER_OPTIONS = 1000
ORDER_PROGRAMS = 2000
ORDER_LIBRARIES = 3000
ORDER_HEADERS = 4000
ORDER_TYPEDEFS_AND_STRUCTURES = 5000
ORDER_FUNCTIONS = 6000
ORDER_OUTPUT = 7000

AC_PROG_CC = OrderedParagraphSet()
AC_PROG_CC.add(
    paragraph=Paragraph(['AC_PROG_CC']),
    order=ORDER_PROGRAMS)

AC_PROG_CXX = OrderedParagraphSet()
AC_PROG_CXX.add(
    paragraph=Paragraph(['AC_PROG_CXX']),
    order=ORDER_PROGRAMS)

AC_PROG_RANLIB = OrderedParagraphSet()
AC_PROG_RANLIB.add(
    paragraph=Paragraph(['AC_PROG_RANLIB']),
    order=ORDER_PROGRAMS)

AC_PROG_LIBTOOL = OrderedParagraphSet()
AC_PROG_LIBTOOL.add(
    paragraph=Paragraph(['AC_LIBTOOL_DLOPEN',
                         'AC_LIBTOOL_WIN32_DLL',
                         'AC_PROG_LIBTOOL']),
    order=ORDER_PROGRAMS)

AM_PROG_LEX = OrderedParagraphSet()
AM_PROG_LEX.add(
    paragraph=Paragraph(['AM_PROG_LEX']),
    order=ORDER_PROGRAMS)

AC_PROG_YACC = OrderedParagraphSet()
AC_PROG_YACC.add(
    paragraph=Paragraph(['AC_PROG_YACC']),
    order=ORDER_PROGRAMS)
