.. vim: set fileencoding=utf-8 :
.. Andre Anjos <andre.anjos@idiap.ch>
.. Mon 13 Aug 2012 12:36:40 CEST 

========================================================================
Heterogeneous Face Recognition using Inter-Session Variability Modelling
========================================================================


This package provides the source code to run the experiments published in the paper `Heterogeneous Face Recognition using Inter-Session Variability Modelling <http://publications.idiap.ch/index.php/publications/show/3370>`_.

If you use this package and/or its results, please cite the following publications:

1. The original paper with the counter-measure explained in details::

    @inproceedings{Pereira_CVPRW2016,
      author = {Pereira, Tiago de Freitas and Marcel, S{\'{e}}bastien},
      keywords = {Face Recognition, Session Variability Modelling, Heterogeneous Face Recognition},
      month = jun,
      year = {2016},
      title = {Heterogeneous Face Recognition using Inter-Session Variability Modelling},
      journal = {IEEE Computer Society Workshop on Biometrics - CVPRW 2016},
    }


2. Bob as the core framework used to run the experiments::

    @inproceedings{Anjos_ACMMM_2012,
      author = {A. Anjos AND L. El Shafey AND R. Wallace AND M. G\"unther AND C. McCool AND S. Marcel},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = oct,
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
    }





Raw Data
--------
 
This package does not provide the dataset used in the paper.
They must be downloaded separately from CUHK_CUFS (`<http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html>`_) and CBSR NIR-VIS-2.0 (`<http://www.cbsr.ia.ac.cn/english/NIR-VIS-2.0-Database.html>`_).

 

Installation
------------

.. note:: 

  If you are reading this page through our GitHub portal and not through PyPI,
  note **the development tip of the package may not be stable** or become
  unstable in a matter of moments.

  Go to `http://pypi.python.org/pypi/antispoofing.lbptop
  <http://pypi.python.org/pypi/bob.paper.CVPRW_2016>`_ to download the latest
  stable version of this package.

There are 2 options you can follow to get this package installed and
operational on your computer: you can use automatic installers like `pip
<http://pypi.python.org/pypi/pip/>`_ (or `easy_install
<http://pypi.python.org/pypi/setuptools>`_) or manually download, unpack and
use `zc.buildout <http://pypi.python.org/pypi/zc.buildout>`_ to create a
virtual work environment just for this package.



Using an automatic installer
============================

Using ``pip`` is the easiest (shell commands are marked with a ``$`` signal)::

  $ pip install bob.paper.CVPRW_2016

You can also do the same with ``easy_install``::

  $ easy_install bob.paper.CVPRW_2016

This will download and install this package plus any other required
dependencies. It will also verify if the version of Bob you have installed
is compatible.

This scheme works well with virtual environments by `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ or if you have root access to your
machine. Otherwise, we recommend you use the next option.

Using ``zc.buildout``
=====================

Download the latest version of this package from `PyPI
<http://pypi.python.org/pypi/bob.paper.CVPRW_2016>`_ and unpack it in your
working area. The installation of the toolkit itself uses `buildout
<http://www.buildout.org/>`_. You don't need to understand its inner workings
to use this package. Here is a recipe to get you started::
  
  $ python bootstrap.py 
  $ ./bin/buildout



Documentation
-------------

.. toctree::
   :maxdepth: 2

   guide
   py_api

