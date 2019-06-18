* Convert to git, push to github

  * Fix testsuite failures (00inmem.py has none, 00build.py has some)

    * python /home/jfasch/work/confix/git-svn-conversion/libconfix/plugins/c/setups/tests/explicit/check_build.py

  * move to python3 (local imports, mainly)

* libconfix.core.utils.helper.find_confix_root(): fix that fucking
  shit; it is not comprehensive at all. if you don't point PATH into
  the uninstalled-tree, it won't be able to detect the root of the
  checkout.

  most elegant solution: bubble up from dirname(argv0) until either
  setup.py is found, or / is reached.
