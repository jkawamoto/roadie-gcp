Instruction file
===================

An instruction file is a YAML document. It has three top-level elements;
``apt``, ``source``, ``data``, ``run``, ``result``, and ``upload``.

apt
-----
The ``apt`` section specifies a package list to be installed via apt.

.. code-block:: yaml

  apt:
  - nodejs
  - package_a
  - package_b


souce
-------
The ``source`` section specifics how to obtain source codes.
It could have either git repository URL or normal URL.
A git repository URL is a URL ends with ``.git``.
Such URLs will be used with ``git clone``.
If you want to use ssh to connect your repository,
you may need to deploy valid ssh keys in ``/root/.ssh`` in this container.
For *normal URL*, in addition to the basic scheme ``http`` and ``https``,
this url supports ``gs`` which means an object in Google Cloud Storage, and ``dropbox``.
See the next section for detail.

Example
.........

Clone source code from a git repository:

.. code-block:: yaml

  source: https://github.com/itslab-kyushu/youtube-comment-scraper.git


Download source code from some web server:

.. code-block:: yaml

  source: https://exmaple.com/abc.txt


Download source code from Google Cloud Storage:

.. code-block:: yaml

  source: gs://your_bucket/path_to_object


Download source code from Dropbox:

.. code-block:: yaml

  source: dropbox://www.dropbox.com/sh/abcdefg/ABCDEFGHIJKLMN


data
------
The ``data`` section specifies URLs to be downloaded.
It must be a list of extended URLs and the format of extended URL is
``scheme://hostname/path`` or ``scheme://hostname/path:dest``
URL schemes Roadie-GCP supports are ``gs``, ``dropbox`` and schemes which ``curl`` supports.
To download objects, Roadie-GCP uses ``curl`` but uses ``gsutil`` for ``gs`` scheme.
``dropbox`` is a pseudo scheme to download objects from `Dropbox <https://www.dropbox.com/>`_.
To use this scheme, get public URL from Dropbox and then replace ``https`` to ``dropbox``.
When you download objects via Dropbox's public link, they are zipped.
Using ``dropbox`` scheme will unzip those objects.

Downloaded objects will be put in ``/data`` which is the default working directory.
You can also use the second format of URL to specify destinations of objects.


run
-----
The ``run`` section specifies what commands will be run.
It must be a list of commands.
Those commands will be executed via shell.
STDOUT of those commands will be stored to files named ``stdout*.txt`` and uploaded to Google Cloud Storage.
For example, the outputs of the first commands will be stored to ``stdout0.txt``.
On the other hands, STRERR will be outputted to docker logs.

result
--------
The ``result`` section specifies where outputted results should be stored.
Outputted results include STDOUT of each commands.
Roadie-GCP supports only a place in Google Cloud Storage, currently.
Thus, the value of the ``result`` element must be a URL of which scheme is ``gs``.

upload
--------
The ``upload`` section specifies other files to be uploaded as results.
This section consist of a list of glob patterns.
Objects matching to one of the patterns will be uploaded to the cloud storage.
Each glob pattern can have a destination after ``:``.
For example, ``"*.out:result`` means objects matching ``*.out`` will be uploaded to ``result`` folder.
