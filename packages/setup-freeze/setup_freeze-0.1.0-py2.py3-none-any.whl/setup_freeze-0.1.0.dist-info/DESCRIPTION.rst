setup-freeze
============

**What it does**: ``setup-freeze`` will edit your ``setup.py`` for you, pinning your ``install_requires`` to the exact version that you have installed.

**What it doesn't do**: Add or remove entries in your ``install_requires``. Touch any of the other arguments that specify requirements, like ``setup_requires`` or ``extras_require`` (yet).

**How to use it**: ``pip install setup-freeze``, then ``cd`` to a directory with a ``setup.py`` in it and run ``setup-freeze``.

**What you need to know**: Your ``setup.py`` needs to contain a call to ``setup()``, with an ``install_requires`` argument set to a list, tuple, or set literal that contains string literals. It also needs to be UTF-8 encoded, and parseable by the version of Python that ``setup-freeze`` is installed in (so, if you install ``setup-freeze`` globally in Python 2, your ``setup.py`` needs to be Python-2-friendly even if you're in a Python 3 virtualenv, or vice versa).

**What you can do with the source code**: Whatever you like, provided that you comply with the conditions of the MIT License.

**What you shouldn't blame me for**: This is beta software, and as such comes with no guarantee that it won't completely mess up your setup.py, delete your entire project, or set your computer on fire. I'm pretty sure it won't, but having version control, backups, and fire extinguishers is good practice anyway, right?


