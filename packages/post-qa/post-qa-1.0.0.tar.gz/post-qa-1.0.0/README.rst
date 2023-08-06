.. image:: https://img.shields.io/pypi/v/post-qa.svg
.. image:: https://img.shields.io/travis/lsst-sqre/post-qa.svg

#######
post-qa
#######

Upload QA datasets from tools like `validate_drp <https://github.com/lsst/validate_drp>`_ to the SQuaSH database and web app.
``post-qa`` is meant to run in a CI workflow, like LSST Data Management's Jenkins CI.

Install
=======

::

   pip install post-qa

Command Line Interface
======================

::

  usage: post-qa [-h] --lsstsw LSSTSW_DIRNAME --qa-json QA_JSON_PATH --api-url
                 API_URL --api-user API_USER --api-password API_PASSWORD
  
  optional arguments:
    -h, --help            show this help message and exit
    --lsstsw LSSTSW_DIRNAME
                          Path of lsstsw directory
    --qa-json QA_JSON_PATH
                          Filename of QA JSON output file
    --api-url API_URL     URL of SQuaSH API endpoint for job submission
    --api-user API_USER   Username for SQuaSH API
    --api-password API_PASSWORD
                          Password for SQuaSH API

Further Reading
===============

- `SQR-008: SQUASH QA database <http://sqr-008.lsst.io>`_.
- `SQR-009: SQUASH dashboard prototype <http://sqr-009.lsst.io>`_.

License Info
============

Copyright 2016 AURA/LSST

MIT licensed open source.
