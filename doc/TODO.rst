* STACK

  * modfile distribution

    * flags parsing centrally

  * plan

    * port all of 'externals' package to cmake
    * remove setups.explicit_setup
    * propagate cmake confix modules

* CMAKE PROJECT

  * relocated headers (at least, test it).
  * script plugin
  * archive vs. shared library?

    * library dependencies. we do not generate any dependencies when
      building shared libraries. how do we decide that? I suppose not
      at all since this is a user decision.

  * execute tests
  * interfaces:

    * TESTS_ENVIRONMENT is currently coupled to automake. probably
      introduce some property mechanism in Builder where we can hook
      any kind of information for the backends.

      this will require some extra work, and some tests.

  * Windows: how about CMAKE_INSTALL_PREFIX?
  * CPack

    * repo file in package
    * find-modules in package

  * remove kde-hack from automake.
  * remove fast-install crap from automake altogether.
  * confix-output

    * options

      ::

         --overlayroot
         --readonly-prefixes
         --trace
         --debug
         --verbose
         --message-prefix
         --print-timings

    * find a way to pass options in to the setups; candidates are

      ::

	 --short-libnames
         --use-libtool (?)
         --use-bulk-install
         --use-kde-hack
      
* TODO

  * Objects to relieve from automake stuff

    * TESTS_ENVIRONMENT? Move that to automake.

  * move core.hierarchy.* to core.machinery. possibly collapse related
    files into one, bigger file.
  
  * Unify the various setup classes

    * write a small utility that prints the setup object hierarchies
    * move libconfix/frontends/confix2/confix_setup.py to
      libconfix/setups/implicit_setup.py
    * rename libconfix/plugins/c/setups/default_setup.py to
      implicit_setup.py
    * from both implicit and explicit, rip out duplicates
      * ScriptSetup
      * MakeSetup
      * ... whatnot ...
      * and, above all, AutomakeSetup

  * Document the InterfaceProxy object that we have in the list below.

* InterfaceProxy objects

  Make one dedicated object of each method/function. This gives us the
  possibility to provide documentation/typing for each.

  * Confix2.dir Interface

    Make three setup objects for the backend-neutral part:

    * Common
    * Explicit
    * Implicit

    The rest (those that don't fit in one of the above) are probably
    future automake plugin candidates.

    * Confix2_dir_ExplicitInterface

      * Files

        * core/hierarchy/explicit_iface.py

      * Used by

        * Confix2_dir_ExplicitInterface(Confix2_dir_Contributor)

      * Methods

        * DIRECTORY

    * CommonDirectoryInterface_Confix2_dir.DirectoryBuilderInterfaceProxy

      * Files

        * core/hierarchy/common_iface.py

      * Used by

        * CommonDirectoryInterface_Confix2_dir(Confix2_dir_Contributor)

      * Methods

        * CURRENT_BUILDER: return current directory-builder; tested
        * CURRENT_DIRECTORY: tested
        * ADD_DIRECTORY(name): adds an empty directory with name; tested
	* IGNORE_ENTRIES: tested
        * IGNORE_FILE: tested
        * FIND_ENTRY: tested
        * GET_ENTRIES: tested
        * RESCAN_CURRENT_DIRECTORY: tested
        * ADD_EXTRA_DIST: tested
        * MAKEFILE_AM: tested
        * ADD_BUILDER: tested
        * SET_FILE_PROPERTIES: tested
        * SET_FILE_PROPERTY: tested
      
  * FileBuilderInterfaceProxy

    * Files

      * core/machinery/filebuilder.py

    * Used by

      * FileBuilder

    * Methods

      * SET_FILE_PROPERTIES
      * SET_FILE_PROPERTY

  * BuilderInterfaceProxy

    * Files

      * core/machinery/builder.py

    * Used by

      * Builder

    * Methods

      * PARENTBUILDER: function
      * PACKAGE: function
      * PROVIDE: add provide object (blah type must be imported)
      * REQUIRE: add require object (blah type must be imported)
      * PROVIDE_SYMBOL

        * match: one of

          * EXACT_MATCH: Provide_String.EXACT_MATCH
          * PREFIX_MATCH: Provide_String.PREFIX_MATCH
          * GLOB_MATCH: Provide_String.GLOB_MATCH
          * AUTO_MATCH: Provide_String.AUTO_MATCH

      * REQUIRE_SYMBOL

        * urgency: one of

          * URGENCY_IGNORE: Require.URGENCY_ERROR
          * URGENCY_WARN: Require.URGENCY_WARN
          * URGENCY_ERROR: Require.URGENCY_ERROR

      * PROVIDE_CALLABLE
      * REQUIRE_CALLABLE

        * urgency: see REQUIRE_SYMBOL

      * BUILDINFORMATION: add BuildInformation object of any type
      * CONFIGURE_AC: blah

        * order: one of

          * AC_BOILERPLATE
          * AC_OPTIONS
          * AC_PROGRAMS
          * AC_LIBRARIES
          * AC_HEADERS
          * AC_TYPEDEFS_AND_STRUCTURES
          * AC_FUNCTIONS
          * AC_OUTPUT

        * flags: set of

	  * LOCAL
          * PROPAGATE

	  (None means both)

        * ACINCLUDE_M4: blah

          * flags: see CONFIGURE_AC        

  * PackageInterfaceProxy

    * Files

      * core/machinery/local_package.py

    * Used by:

      * LocalPackage (not a Builder, to be viewed separately)

    * Methods:

      * PACKAGE_NAME
      * PACKAGE_VERSION
      * ADD_SETUP
      * SETUPS

  * HeaderBuilderInterfaceProxy

    * Files

      * plugins/c/h.py

    * Used by:

      * HeaderBuilder

    * Methods:

      * INSTALLPATH

  * PKG_CONFIG_LIBRARY

    * Files

      * plugins/c/pkg_config/setup.py

    * Used by:

      * PkgConfigInterface_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * PKG_CONFIG_LIBRARY

  * CompiledCBuilderInterfaceProxy

    * Files

      * plugins/c/compiled.py

    * Used by:

      * CompiledCBuilder

    * Methods:

      * EXENAME

  * INSTALLDIR_H

    * Files

      * plugins/c/explicit_install.py

    * Used by:

      * ExplicitInstaller_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * INSTALLDIR_H: talks to ExplicitInstaller object (unique per
        directory) which sets it into every HeaderBuilder of the
        directory.

  * RelocatorInterfaceProxy

    * Files

      * plugins/c/relocated_headers/iface.py

    * Used by:

      * Relocator_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * RELOCATE_HEADER

  * CClustererInterfaceProxy

    * Files

      * plugins/c/clusterer.py

    * Used by:

      * CClusterer_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * LIBNAME
      * LIBTOOL_LIBRARY_VERSION

  * (C) ExplicitInterfaceProxy

    * Files

      * plugins/c/explicit_iface.py

    * Used by:

      * ExplicitInterface_Confix2_dir(Confix2_dir_Contributor) (which
        is in turn used by ExplicitInterfaceSetup)

    * Methods:

      * H
      * C
      * CXX
      * LIBRARY
      * EXECUTABLE

        * what: one of

          * EXECUTABLE_BIN
          * EXECUTABLE_CHECK
          * EXECUTABLE_NOINST

  * EXTERNAL_LIBRARY

    * Files

      * plugins/c/common_iface.py

    * Used by:

      * CommonInterface_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * EXTERNAL_LIBRARY

  * REQUIRE_H

    * Files

      * plugins/c/common_iface.py

    * Used by:

      * CommonInterface_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * REQUIRE_H

  * PROVIDE_H

    * Files

      * plugins/c/common_iface.py

    * Used by:

      * CommonInterface_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * PROVIDE_H

  * TESTS_ENVIRONMENT

    * Files

      * plugins/c/common_iface.py

    * Used by:

      * CommonInterface_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * TESTS_ENVIRONMENT

  * MakeCallerInterfaceProxy

    * Files

      * plugins/make/setup.py

    * Used by:

      * _MakeInterface_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * CALL_MAKE_AND_RESCAN
      * CALL_MAKE_AND_RESCAN_SYNC
      
  * ADD_PLAINFILE

    * Files

      * plugins/plainfile/iface.py

    * Used by:

      * ADD_PLAINFILE_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * ADD_PLAINFILE

  * ADD_SCRIPT

    * Files

      * plugins/script/setup.py

    * Used by:

      * ScriptInterface_Confix2_dir(Confix2_dir_Contributor)

    * Methods:

      * ADD_SCRIPT

