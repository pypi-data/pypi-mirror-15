Stirplate.io Data Upload Helper
===============================

Sequencing data may be sent to Stirplate several ways.

1. Manual data upload via `stirplate.io <https://stirplate.io>`__.
2. **RECOMMENDED**: Automatic upload from a local computer directly to
   Stirplate without user interaction (outlined in this document).

Prerequisites:
--------------

-  To setup and run automated data upload to Stirplate, be sure you have
   your Stirplate User Credentials (please contact keith@stirplate.io to
   obtain these).
-  Python 2.7.x (untested on Python >= 3).
-  Python packages ``boto3`` and ``mando``.

   -  To install ``boto3`` to your python environment, use PIP:
      ``pip install boto3``
   -  To install ``mando`` to your python environment, use PIP:
      ``pip install mando``

Configure Access:
-----------------

Configure your Stirplate Access Credentials.

1. **Interactive**: Simply type:

   ::

       python stirplate.py configure

2. **Automatic**: (Recommended) "Install" the supplied configuration
   file automatically from a downloaded config file:

   ::

       python stirplate.py configure --install /path/to/stirplate/config

-  Alternatively, you may pass your access credentials as parameters
   during the upload phase (not recommended).

Uploading and starting the Stirplate RNA-Seq protocol:
------------------------------------------------------

There are two ways to run the data upload helper for the Stirplate
RNA-Seq (DESeq2) protocol:

1. **Interactive**. Simply type:

   ::

       python stirplate.py rna

   -  You will be prompted for the input directory containing your
      sequencing data, as well as additional meta data (species, single
      stranded protocol) information.

2. **Automatic**. Simply run:

   ::

       python stirplate.py rna
       --directory /path/to/input/sequencing/data/
       --project_name MyProjectName
       --species SPECIES

   -  Species choices are: ``C_ELEGANS`` (worms), ``D_RERIO``
      (zebrafish), ``H_SAPIENS`` (humans), ``M_MUSCULUS`` (mouse), or
      ``R_NORVEGICUS`` (rat).
   -  If the experiment was performed using a single strand protocol,
      pass the ``--single_stranded_protocol`` flag as well.
   -  Upon running, all files in your input sequence data ``directory``
      will be uploaded to Stirplate.io. The uploading is optimized for
      speed so your data will be transferred in the least amount of
      time. **Processing will begin at Stirplate as soon as the last
      file transfer has completed**.

Help
----

At any point you may get additional command line usage help by typing:

-  ``python stirplate.py -h``
-  ``python stirplate.py rna -h``
