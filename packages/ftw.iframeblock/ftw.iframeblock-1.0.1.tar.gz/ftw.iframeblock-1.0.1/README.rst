Introduction
============

``ftw.iframeblock`` privides a block for ``ftw.simplelayout``, which renders a iframe using
`iframeResizer.js <https://github.com/davidjbradshaw/iframe-resizer#typical-setup>`_.
Read carefully the setup instroctions of iframeresizer, you need a implementation on both domains.


.. contents:: Table of Contents

Installation local development-environment
------------------------------------------

.. code:: bash

    $ git clone git@github.com:4teamwork/ftw.iframeblock.git
    $ cd ftw.iframeblock
    $ ln -s development.cfg buildout.cfg
    $ python2.7 bootstrap.py
    $ bin/buildout
    $ bin/instance fg

Dev-Test-Release-Process
------------------------

If you want to develop features, you must follow this guide

First checkout the package and create a new branch from the master:

.. code:: bash

    $ git clone git@github.com:4teamwork/ftw.iframeblock.git
    $ cd ftw.iframeblock
    $ git checkout -b my-mew-feature
    $ git push origin -u my-new-feature

If you are finnished and the feature is working fine, you can merge it into the
master branch after the quality-check:

.. code:: bash

    $ git checkout master
    $ git merge my-mew-feature
    $ git push

Now, the feature is available for other developers.


Compatibility
-------------

Runs with `Plone <http://www.plone.org/>`_ `4.3.x`.


Links
-----

- Github: https://github.com/4teamwork/ftw.iframeblock
- Issues: https://github.com/4teamwork/ftw.iframeblock/issues
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.iframeblock

Copyright
---------

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.iframeblock`` is licensed under GNU General Public License, version 2.
