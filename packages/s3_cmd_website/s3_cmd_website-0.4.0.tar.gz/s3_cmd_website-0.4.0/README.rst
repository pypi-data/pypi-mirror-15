Create, Update and Delete static websites in S3
===============================================

.. image:: https://travis-ci.org/theidledeveloper/s3-cmd-website.svg?branch=master
   :alt: Build Status
   :target: https://travis-ci.org/theidledeveloper/s3-cmd-website

.. image:: https://badge.fury.io/py/s3-cmd-website.svg
   :alt: PyPI badge
   :target: http://badge.fury.io/py/s3-cmd-website

.. image:: https://coveralls.io/repos/theidledeveloper/s3-cmd-website/badge.svg?branch=master&service=github
   :alt: Test coverage
   :target: https://coveralls.io/github/theidledeveloper/s3-cmd-website?branch=master

This tool is a wrapper around the s3_cmd_ command line tool to provide
easy configuration for creating, maintaining and deleting s3 static websites
via a yaml based configuration.

The complexity of using the s3cmd comes when you need to apply configuration
to different paths or file types within your static website. This tool aims to
reduce that complexity and provide an easier to work with interface.

See the ``.s3_website_cfg.example`` for a sample copy of the configuration
used by the tool.

.. _s3_cmd: https://github.com/s3tools/s3cmd

Setup
-----------

As this tool relies on the s3cmd configuration as it is the interface to AWS.
To do this you can use the s3cmd in built configuration helper by executing:

.. code-block:: shell

    $ s3cmd --configure

You will need to provide your AWS credentials (Access and Secret Key) unless
you are using IAM roles from an AWS instance whereby you can leave this
configuration blank. All other configuration can be left as default but you
may want to set the AWS region to the location where your s3 website will be
hosted.

Configuration file
------------------

**site**
    The directory containing your static website to be uploaded to s3. This
     path needs to be relative to your current location i.e. where you are
     executing the tool from.

**s3_bucket**
    The name of the S3 bucket used by the static website that can be created or
    deleted and where the files will be uploaded to. In order to manipulate the
    bucket you will need to allow the actions ``s3:GetObject``,
    ``s3:PutObject``, ``s3:DeleteObject`` and ``s3:ListBucket`` on the bucket,
    Access keys or IAM role.

**cloudfront_distribution_id**
    The CloudFront distribution to mange. When creating the distribution the
    id will be displayed for you to add into the configuration.

**cache_rules**
    A list of rules to determine the configuration of the uploaded files.
    Valid configuration is ``match`` which is the files or paths you want wish
    to effect, ``maxage`` the cache age of the files, ``gzip`` for defining
    if gzip compression is to be turned on for these files and ``exclude`` to
    remove files or paths from the match.

**maxage**
    The default cache for files where it is not explicitly defined

**gzip**
    If gzip is to be turn enabled ort disabled if not defined in the match.

Usage
-----

Set the log level:

``s3_website -L debug``

Set the location of the:

``s3_website --s3_cmd_config ~/.s3cfg``

Set the location of the website configuration file:

``s3_website --s3_website_config ~/static_website.yaml``

Display the website information:

``s3_website information``

Display create the s3 website and bucket:

``s3_website create --make_bucket``

Display update the contents of the static website in the bucket:

``s3_website upload``

Considerations
--------------

When defining multiple matches and one includes ``*`` ensure you explicitly
exclude other paths to ensure you do not overwrite the changes.
i.e. Where ``*`` matches everything and would change the cache and gzip options
for the ``/css/*`` matched files.

.. code-block:: yaml

  - match: "/css/*"
    maxage: 30 days
    gzip: true

  - match: "*"
    exclude: "/assets"
    maxage: 1 hour
    gzip: false

Similar software
----------------

The tool was inspired by s3_deploy_website_ which provided the basis for the
yaml configuration file and required functionality.

.. _s3_deploy_website: https://github.com/jonls/s3-deploy-website

Licence
-------

MIT.
