Run
=====

Letting ``conf.yml`` be an instruction file,

.. code-block:: sh

  $ docker run -i jkawamoto/roadie-gcp < conf.yml

starts Roadie-GCP with the instruction.
You also specify an instruction file instead of STDIN by

.. code-block:: sh

  $ docker run -i jkawamoto/roadie-gcp -c /path/to/conf.yml


Roadie-GCP will shutdown your VM after finishing instructions.
Thus, ``https://www.googleapis.com/auth/compute`` scope is required.
To prevent this behavior, use ``--no-shutdown`` option.

The full description of arguments is below.

.. code-block:: sh

  usage: docker run -i jkawamoto/roadie-gcp [-h] [-c CONF] [--no-shutdown]

  Read an instruction from STDIN and run programs in that way.

  optional arguments:
    -h, --help            show this help message and exit
    -c CONF, --conf CONF  Specify an instruction YAML file instead of STDIN.
    --no-shutdown         Not shutdown after finishing tasks.
    --no-unzip            Not unzip zipped files.
