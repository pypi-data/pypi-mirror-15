wundertool-py
==============
Tool for working with `Docker <https://www.docker.com/>`_ containers.

Requirements:

- python 3 or later

Installation
------------
You can always install the tool from PyPI with::

  pip install wundertool

*Note: OS X doesn't have python 3 or pip installed by default. You should install them with `brew` first and then install `wundertool`*::

  brew install python3
  pip3 install wundertool

Development
-----------
Requirements:

- python 3.4 or later

You can clone this module locally and install it in development mode in an virtual environment like this::

  git clone https://github.com/aleksijohansson/wundertool-py.git
  cd wundertool-py
  pyvenv .
  source bin/activate
  pip install -e ".[dev]"

You always need to activate the wundertool-py virtual environment when opening a new terminal for development::

  source <DIR>/wundertool-py/bin/activate
