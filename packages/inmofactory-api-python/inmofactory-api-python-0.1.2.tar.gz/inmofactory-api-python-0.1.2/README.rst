===============
Inmofactory API
===============

This package upload properties to Inmofactory using INMOFACTORY API.

License
-------

The package is released under the New BSD license.

Example of use
--------------

.. code-block:: python

    from inmofactory import api

    inmofactory_api = api.InmofactoryAPI('user', 'password', 'agency_id', 'agent_id')

    result = inmofactory_api.insert({}) # Insert a property

    print result
