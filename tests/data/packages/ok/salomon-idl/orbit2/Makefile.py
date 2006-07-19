# -*- python -*-

# $Id: Makefile.py,v 1.2 2004/09/07 15:45:14 jfasch Exp $

PROVIDE_H('orbit/*')

PROVIDE_SYMBOL('ORBit2')
REQUIRE_SYMBOL('glib2')

orbit_file = open('ORBit2.m4')
m4text = orbit_file.readlines()
for i in range(len(m4text)):
    m4text[i] = m4text[i].replace('\n', '')
orbit_file.close()

ACINCLUDE_M4(
    lines=m4text,
    id='ORBit2')

CONFIGURE_IN(
    lines=['AM_PATH_ORBIT2'],
    order=AC_PROGRAMS,
    id='AM_PATH_ORBIT2')

EXTERNAL_LIBRARY2(
    lib='@ORBIT_LIBS@',
    cflags=['@ORBIT_CFLAGS@'])
