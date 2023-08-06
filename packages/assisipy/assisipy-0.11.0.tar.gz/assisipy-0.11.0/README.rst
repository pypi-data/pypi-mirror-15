assisi-python
=============

Python API for the ASSISI|bf project.

Building the Python package and uploading it to PyPy
----------------------------------------------------

Assuming you have `~/.pypirc` already set up:

::

   python setup.py sdist
   twine upload dist/assisipy-x.y.z.tar.gz -p password


Installing the development version
----------------------------------

Local changes to the repo will be immediatelly visible in the
installed package (need to check this).

::

   sudo pip install -e .


To uninstall the development version:

::

   sudo python setup.py develop --uninstall


For more info see
http://python-packaging-user-guide.readthedocs.org/en/latest/distributing



============================================================
This release was sourced from:
	assisi-python git rev 30778f9b1d90298621f90f6eacd4850e78677257
	assisi-msg    git rev ed6c974cbd47b3d24386c7bb3acf20ac2459c41b
	assisi-python version 0.11.0
============================================================
