filesysobjects
==============

The 'filesysobjects' package provides utilities for the application of
basic object oriented features onto filesystems.
This includes basic coverage of the 'inspect' package for the simplified
gathering of information on packages, modules, and files.

The provided feature modules comprise the following list.
For code examples refer to 'filesysobjects.UseCases'.

The package 'filesysobjects' is a spin off from the project 'UnifiedSessionsManager-2.0'.
 
The main interface classes are:

* **FileSysObjects** - Filesystem objects.

For the compliance tests extracted from IETF and ECMA standards refer to the directories:

* UseCases
 
**Downloads**:

* Sourceforge.net: https://sourceforge.net/projects/pyfilesysobjetcs/files/
  
**REMARK**: The pathname on sourceforge.net is a little odd for now
  because this could not changed on-the-fly: 'filesysobjeTCcs' instead 'filesysobjeCTs' 


* Github: https://github.com/ArnoCan/pyfilesysobjects/

**Online documentation**:

* https://pypi.python.org/pypi/pyfilesysobjects/
* https://pythonhosted.org/pyfilesysobjects/

setup.py
--------

The installer adds a few options to the standard setuptools options.

* *build_sphinx*: Creates documentation for runtime system by Sphinx, html only. Calls 'callDocSphinx.sh'.

* *build_epydoc*: Creates documentation for runtime system by Epydoc, html only. Calls 'callDocEpydoc.sh'.

* *test*: Runs PyUnit tests by discovery.

* *--help-filesysobjects*: Displays this help.

* *--no-install-required*: Suppresses installation dependency checks, requires appropriate PYTHONPATH.

* *--offline*: Sets online dependencies to offline, or ignores online dependencies.

* *--exit*: Exit 'setup.py'.

After successful installation the 'selftest' verifies basic checks by:

  *filesysobjects --selftest*

with the exit value '0' when OK.

The option '-v' raises the degree of verbosity for inspection

  *filesysobjects --selftest -v -v -v -v*
 

Project Data
------------

* PROJECT: 'filesysobjects'

* MISSION: Extend the standard PyUnit package for arbitrary ExecUnits.

* VERSION: 00.00

* RELEASE: 00.00

* NICKNAME: 'Yggdrasil'

* STATUS: pre-alpha

* AUTHOR: Arno-Can Uestuensoez

* COPYRIGHT: Copyright (C) 2010,2011,2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

* LICENSE: Artistic-License-2.0 + Forced-Fairplay-Constraints
  Refer to enclose documents:
  
  *  ArtisticLicense20.html - for base license: Artistic-License-2.0 

  *  licenses-amendments.txt - for amendments: Forced-Fairplay-Constraints

VERSIONS and RELEASES
---------------------

**Planned Releases:**

* RELEASE: 00.00.00x - Pre-Alpha: Extraction of the features from hard-coded application into a reusable package.

* RELEASE: 00.01.00x - Alpha: Completion of basic features. 

* RELEASE: 00.02.00x - Alpha: Completion of features, stable interface. 

* RELEASE: 00.03.00x - Beta: Accomplish test cases for medium to high complexity.

* RELEASE: 00.04.00x - Production: First production release. Estimated number of UnitTests := 250.

* RELEASE: 00.05.00x - Production: Various performance enhancements.


**Current Release: 00.00.006 - Pre-Alpha:**

OS-Support:

* Linux: OK(Fedora)

* UNIX: todo(should work)

* Windows: todo(issues with normpath)

* Mac-OS: todo


Major Changes:

* Split into generic FileSysObjects, and Python Source code RTTI/inspect PySourceInfo.

* Extend on Linux platform.

* Did some basic concept work on PATH names in conformance to IEEE/1003.1, including URIs for 'file://'

Current test status:

* UnitTests: >70

* Use-Cases as UnitTests: >56

**Total**: >120

