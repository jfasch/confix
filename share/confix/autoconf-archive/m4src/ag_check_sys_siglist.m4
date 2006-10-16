dnl @synopsis AG_CHECK_SYS_SIGLIST
dnl
dnl Check that the POSIX compliant regular expression compiler is
dnl available in the POSIX specified manner, and it works.
dnl
dnl @category C
dnl @author Bruce Korb <bkorb@gnu.org>
dnl @version 2001-12-01
dnl @license GPLWithACException

dnl DO NOT EDIT THIS FILE   (ag_check_sys_siglist.m4)
dnl
dnl It has been AutoGen-ed  Saturday December  1, 2001 at 09:21:28 PM PST
dnl From the definitions    bkorb.def
dnl and the template file   conftest.tpl
dnl See: http://autogen.sf.net for a description of the AutoGen project

AC_DEFUN([AG_CHECK_SYS_SIGLIST],[
  AC_MSG_CHECKING([whether there is a global text array sys_siglist])
  AC_CACHE_VAL([ag_cv_sys_siglist],[
  AC_TRY_RUN([#include <signal.h>
int main() {
  const char* pz = sys_siglist[1];
  return (pz != 0) ? 0 : 1; }],[ag_cv_sys_siglist=yes],[ag_cv_sys_siglist=no],[ag_cv_sys_siglist=no]
  ) # end of TRY_RUN]) # end of CACHE_VAL

  AC_MSG_RESULT([$ag_cv_sys_siglist])
  if test x$ag_cv_sys_siglist = xyes
  then
    AC_DEFINE(HAVE_SYS_SIGLIST, 1,
       [Define this if there is a global text array sys_siglist])
    NEED_SYS_SIGLIST=false
  else
    NEED_SYS_SIGLIST=true
  fi
  AC_SUBST(NEED_SYS_SIGLIST)
]) # end of AC_DEFUN of AG_CHECK_SYS_SIGLIST