#PhilUtils

This library contains a bunch of small miscellaneous functions,
I've built over time but didn't seem to fit in their own package.

All the functions in this library will only require the python
standard library - not any third party libraries.

For the foreseeable future, this library will undergo too many
changes for me to suggest that anyone use this library and I plan
on regularly shuffle things out of this library when I feel that
they would be better organized in their own package.

Use at your own risk.

##About

This project was created automatically using Philip Zerull's python_package
newproj template.  Therefore it's organization matches Philip Zerull's
personal preferences.

##Requirements for setup.py

You should run `hg init` in the same directory where you ran
`newproj python_pacakge` to create a mercurial repository in this directory.
setup.py uses the repository's version (using hgtools) to perform the build.

If you don't want to use the repository's version then remove the
_setup\_requires_ and _use\_vcs\_version_ parameters from setup.py

##Running the tests

PhilUtils uses python's coverage utility to perform the tests and provide
a coverage report.  If you have coverage installed then you can just execute
`./runtests.sh` to perform all the tests against your current version of
python.

if you wish to test against other versions of python you can simply run `tox`


Author: Philip Zerull <przerull@gmail.com\>
