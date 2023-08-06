Decorating: A Meta Repo To Decorators
=====================================

|Build Status| |codecov| |Requirements Status| |PyPi version| |PyPI
pyversions| |PyPI status| |HitCount|

Usage
=====

Collection of decorators, a properly README will be write in soon. For
now only we have few functionalities, the main usage is the
``@animated`` decorator.

Animated
--------

Using as decorator and mixed with contextmanagers |animation|

Using with nested contextmanagers |contextmanager|

Installation
------------

**WARNING**: This project is still in current development at alpha!
Don't use in serious/production application yet.

Users
^^^^^

stable: ``sudo pip install decorating``

bleeding-edge:
``sudo pip install git+https://www.github.com/ryukinix/decorating``

Developers
^^^^^^^^^^

.. code:: bash

    sudo git clone https://www.github.com/ryukinix/decorating
    cd decorating
    sudo make develop

The develop mode creates a .egg-info (egg-link) as symlink with your
standard ``site-packages``/``dist-packages`` directory. Don't be worry
with the ``decorating.egg-info``, is only information for the package
egg to link with your ``PYTHONPATH``. For that, the usage is dynamic,
you can modify the code in test on the command line always using
absolute imports in anywhere (like the first example)

License
-------

|PyPi License|

MIT

.. |Build Status| image:: https://travis-ci.org/ryukinix/decorating.svg?branch=master
   :target: https://travis-ci.org/ryukinix/decorating
.. |codecov| image:: https://codecov.io/gh/ryukinix/decorating/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ryukinix/decorating
.. |Requirements Status| image:: https://requires.io/github/ryukinix/decorating/requirements.svg?branch=master
   :target: https://requires.io/github/ryukinix/decorating/requirements/?branch=master
.. |PyPi version| image:: https://img.shields.io/pypi/v/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/
.. |PyPI status| image:: https://img.shields.io/pypi/status/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/
.. |HitCount| image:: https://hitt.herokuapp.com/ryukinix/decorating.svg
   :target: https://github.com/ryukinix/decorating
.. |animation| image:: https://i.imgur.com/hjkNvEE.gif
.. |contextmanager| image:: https://i.imgur.com/EeVnDyy.gif
.. |PyPi License| image:: https://img.shields.io/pypi/l/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/


