Microsecrets, a lightweight secrets manager powered by S3 + KMS
===============================================================

.. image:: https://img.shields.io/pypi/v/microsecrets.svg
    :target: https://pypi.python.org/pypi/microsecrets

**Microsecrets** is a secrets distribution tool powered by Amazon S3 and Amazon
KMS. It provides a bare-bones approach to passing credentials securely in an
Amazon Web Services environment. Credentials are uploaded to S3 and encrypted
at rest by KMS. They can then be passed to programs through environment
variables.

Installation
------------

.. code-block:: bash

    $ pip install microsecrets

Usage
-----

Setup
~~~~~

1. Create the S3 bucket you'll use for secrets storage. You may want one bucket
   per organization, such as ``example.com-microsecrets``.

2. Create one KMS master key for each service that will be using microsecrets.
   The key should by default be named ``microsecrets-myservice`` for a service
   called myservice. Users uploading the credentials and systems downloading
   the credentials will need privileges to encrypt/decrypt data using this key.
   None of the normal users need key administration privileges.

Uploading environment and files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Upload environment variable data. Environment variables may be passed as
   ``=`` separated pairs on stdin or in a file. *NB: whitespace is stripped and
   all other characters are treated literally.* Or pass them as a JSON dict
   with the ``--json`` flag.

   .. code-block:: bash

        $ microsecrets-upload -b example-microsecrets -s myservice <<EOM
        DB_URL=db://user:pass@example.com:123
        PASSWORD=hunter2
        EOM

2. Upload a raw file. Usage is the same as uploading environment variables, but
   you pass a -f LABEL to determine where to upload the file. This example
   uploads a file from ``~/documents/train.txt`` with label ``train.txt``.

   .. code-block:: bash

        $ microsecrets-upload -b example-microsecrets -s myservice -f train.txt ~/documents/train.txt

Downloading files to show status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO: flesh out this section

1. List latest versions of current files available for download

   .. code-block:: bash

        $ microsecrets-download -b example-microsecrets -s myservice --list

2. Download the environment

   .. code-block:: bash

        $ microsecrets-download -b example-microsecrets -s myservice

3. Download files with the environment

   .. code-block:: bash

        $ microsecrets-download -b example-microsecrets -s myservice -f train.txt:/tmp/train.txt

Running programs under environment with secrets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Run a program with the credentials in the environment. To verify the
   integrity of data in S3, you must specify the checksum of the environment
   file (output by the upload tool) or whitelist specific environment
   variables. Or, if integrity is not a concern, whitelist all environment
   variables. The whitelist is designed to avoid accidentally allowing code
   execution through ``LD_PRELOAD`` or similar, which may or may not be a
   concern in your system layout.

   .. code-block:: bash

        $ microsecrets-with-env -b example-microsecrets -s myservice -w 'DB_URL PASSWORD' -- /bin/myserver

See also
--------

There is a variety of other recent work in this space that may be of interest:

* Confidant — https://github.com/lyft/confidant
* Sops — https://github.com/mozilla/sops
* Sneaker — https://github.com/codahale/sneaker
* Credstash — https://github.com/fugue/credstash
* Vault — https://github.com/hashicorp/vault
* Keywhiz — https://github.com/square/keywhiz

License
-------

`The project is in the public domain`_, and all contributions will also be
released in the public domain. By submitting a pull request, you are agreeing
to waive all rights to your contribution under the terms of the `CC0 Public
Domain Dedication`_.

This project constitutes an original work of the United States Government.

.. _`The project is in the public domain`: ./LICENSE.md
.. _`CC0 Public Domain Dedication`: http://creativecommons.org/publicdomain/zero/1.0/
