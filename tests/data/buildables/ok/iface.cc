// -*- mode: C++; c-basic-offset: 4 -*-
// 
// $Id: iface.cc,v 1.3 2004/09/07 15:45:13 jfasch Exp $
//

// this test simply calls all buildable interface functions which are
// available for C++ impl files (except for FILE_PROPERTIES() for
// which we have an extra test).

// CONFIX:REQUIRE_H('xxx.h')

// CONFIX:REQUIRE_SYMBOL('xxx')

// CONFIX:MAIN('no')
// CONFIX:MAIN('No')
// CONFIX:MAIN('n')
// CONFIX:MAIN('false')
// CONFIX:MAIN('f')
// CONFIX:MAIN('0')
// CONFIX:MAIN(0)
// CONFIX:MAIN('yes')
// CONFIX:MAIN('Yes')
// CONFIX:MAIN('y')
// CONFIX:MAIN('true')
// CONFIX:MAIN('t')
// CONFIX:MAIN('1')
// CONFIX:MAIN(1)

// CONFIX:EXENAME('xxx')

// CONFIX:CONFIGURE_IN(
// CONFIX:    lines=['AC_CHECK_LIB(crypt,crypt)'],
// CONFIX:    order=AC_LIBRARIES,
// CONFIX:    id='my_cryptlib_here')

// CONFIX:ACINCLUDE_M4(
// CONFIX:    lines=['beitl'],
// CONFIX:    id='beitl')
