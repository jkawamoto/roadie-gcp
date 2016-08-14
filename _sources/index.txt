Roadie-GCP
===========
A helper container to execute a program on `Google Cloud Platform <https://cloud.google.com/>`_.

Features:
  * downloads necessary files from web and `Google Cloud Storage <https://cloud.google.com/storage/>`_,
  * runs commands,
  * uploads results to Google Cloud Storage.

Roadie-GCP takes one instruction file.
The instruction file is simple YAML documents like

.. code-block:: yaml

  apt:
  - nodejs
  source: https://github.com/itslab-kyushu/youtube-comment-scraper.git
  data:
  - http://sample.com/run.sh
  - gs://a-project/input/data:/tmp
  run:
  - npm install
  - run.sh /tmp/data
  result: gs://a-project/result/
  upload:
  - "*.out"

This example commands Roadie-GCP to install ``nodejs`` via apt,
and download source codes from a Github repository. Then,
it prepares to data from some web server and Google Cloud Storage,
and run a command ``run.sh /tmp/data``.
Finally, it uploads stdout and results which have extension ``.out`` to a bucket in Google Cloud Storage.
Roadie-GCP automatically shutdowns the virtual machine Roadie-GCP is running on, so you can minimize charge.

Usage
-------

.. toctree::
   :maxdepth: 1

   run
   instruction


API Reference
---------------

.. toctree::
   :glob:
   :maxdepth: 2

   modules/*


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

License
========
This software is released under the MIT License.
