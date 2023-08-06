Decorating: A Meta Repo To Decorators
=====================================

|Build Status| |PyPi version| |Requirements Status| |PyPi License| |PyPI
pyversions| |PyPI status| |HitCount|

Collection of decorators, a properly README will be write in soon. For
now only have that functionality:

.. figure:: https://i.imgur.com/8mAXdhu.gif
   :alt: animation

   animation

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

MIT

.. |Build Status| image:: https://travis-ci.org/ryukinix/decorating.svg?branch=master
   :target: https://travis-ci.org/ryukinix/decorating
.. |PyPi version| image:: https://img.shields.io/pypi/v/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/
.. |Requirements Status| image:: https://requires.io/github/ryukinix/decorating/requirements.svg?branch=master
   :target: https://requires.io/github/ryukinix/decorating/requirements/?branch=master
.. |PyPi License| image:: https://img.shields.io/pypi/l/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/
.. |PyPI status| image:: https://img.shields.io/pypi/status/decorating.svg
   :target: https://pypi.python.org/pypi/decorating/
.. |HitCount| image:: https://hitt.herokuapp.com/ryukinix/decorating.svg
   :target: https://github.com/ryukinix/decorating


