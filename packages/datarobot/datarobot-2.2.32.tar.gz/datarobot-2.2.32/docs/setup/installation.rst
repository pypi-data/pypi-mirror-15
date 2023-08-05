############
Installation
############

Installing the SDK
******************

Getting Started
===============
You will need the following

- GitHub
- Python 2.7 or 3.4+
- DataRobot account
- pip

Installing from a source distribution
*************************************

You should receieve a `.tar.gz` file that you will install from.
We recommend installing the DataRobot Python SDK using a virtual
environment to avoid having dependency conflicts with existing
packages on your system.

.. code-block:: shell

    pip install datarobot-0.1.23.tar.gz

.. note::
   If you are not running in a Python ``virtualenv``, you may need to run
   the above commands with ``sudo`` permissions.

Installing pyOpenSSL
====================
On versions of Python earlier than 2.7.9 you might have InsecurePlatformWarning_ in your output.
To prevent this without updating your Python version you should install pyOpenSSL_ package:

.. _pyOpenSSL: https://urllib3.readthedocs.org/en/latest/security.html#pyopenssl
.. _InsecurePlatformWarning: https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning

.. code-block:: shell

    pip install pyopenssl ndg-httpsclient pyasn1

Configure the SDK
*****************
Each authentication method will specify credentials for DataRobot, as well as
the location of the DataRobot deployment. We currently support configuration
of the SDK using a configuration file, by setting environment variables, or
within the code itself.

Credentials
===========
You will have to specify an API token and an endpoint in order to use the client.  You can manage
your API tokens in the DataRobot webapp, in your profile.

.. note::

    If you access the DataRobot webapp at
    `https://app.datarobot.com`, then the correct endpoint to specify would be
    `https://app.datarobot.com/api/v2`.  If you have a local installation, update the endpoint
    accordingly to point at the installation of DataRobot available on your local network.

Use a Configuration File
========================
You can use a configuration file to specify the client setup.

The following is an example configuration file that should be saved as ``~/.config/datarobot/drconfig.yaml``:

.. code-block:: yaml

    token: yourtoken
    endpoint: https://app.datarobot.com/api/v2

You can specify a different location for the DataRobot configuration file by setting
the ``DATAROBOT_CONFIG_FILE`` environment variable.  Note that if you specify a filepath, you should
use an absolute path so that the API client will work when run from any location.

Set Credentials Explicitly in Code
==================================

Explicitly set credentials in code:

.. code-block:: python

   import datarobot as dr
   dr.Client(token='your_token', endpoint='https://app.datarobot.com/api/v2')

You can also point to a YAML config file to use:

.. code-block:: python

   import datarobot as dr
   dr.Client(config_path='/home/user/my_datarobot_config.yaml')


Set Credentials Using Environment Variables
===========================================

Set up an endpoint by setting environment variables in the UNIX shell:

.. code-block:: shell

   export DATAROBOT_ENDPOINT='https://app.datarobot.com/api/v2'
   export DATAROBOT_API_TOKEN=your_token
