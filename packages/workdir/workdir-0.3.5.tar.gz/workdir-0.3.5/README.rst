=======
workdir
=======

|Latest Version| |Travis Status| |Coveralls Status|

A simple module for easily isolating temporary file I/O to a directory.  Ever developed a command-line tool which required a lot of file manipulation?  Caching, perhaps?  You don't want to use the cwd and keeping all of your paths straight if you're working outside of it can be a pain.  This tool may be the pain-reliever you need!

A tale of sin and woe
=====================

Well, not really.  I've just developed a bunch of tools that rely on various bits of temporary or isolated file I/O, and found myself implementing this pattern over and over again.  Eventually, I got tired of doing it and decided to develop this handy module.  Now I'm passing the savings on to you!

Compatibility
=============

As far as I know, ``workdir`` is compatible with every version of Python from 2.6 through 3.5.  It should also be compatible with all major platforms including Linux, OSX, and Windows.  If not, let me know!

Installation
============

.. code-block ::

    pip install workdir

Examples
========

Use it as a staging area for downloaded archives:

.. code:: python

    import workdir
    import shutil
    workdir.options.path = '~/.myfilecache'
    with workdir.as_cwd():
        download_remote_archive('somefile')
        unpack_archive('somefile', 'somedir')
    shutil.copy(workdir.path_to_file('somedir', 'unpackedfilefromarchive'),
                os.path.join('otherdir', 'unpackedfilefromarchive'))

Use it as a working directory in your git repo (added to `.gitignore`, of course):

.. code:: python

    import workdir
    workdir.options.path = '.gitrepo.work'
    workdir.sync()
    with workdir.as_cwd():
        futz_with_source_tree()
        more_futzing()

.. |Latest Version| image:: https://img.shields.io/pypi/v/workdir.svg
    :target: https://pypi.python.org/pypi/workdir
    :alt: Latest Version
.. |Travis Status| image:: https://img.shields.io/travis/ajk8/workdir-python/master.svg
    :target: https://travis-ci.org/ajk8/workdir-python
    :alt: Travis-ci build status
.. |Coveralls Status| image:: https://coveralls.io/repos/github/ajk8/workdir-python/badge.svg?branch=master 
    :target: https://coveralls.io/github/ajk8/workdir-python?branch=master 
    :alt: Coveralls test coverage
