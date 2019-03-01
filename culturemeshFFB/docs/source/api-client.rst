=============
API Client
=============

CultureMesh FFB communicates with CultureMesh via the CultureMesh API.
CultureMesh FFB contains a ``client`` class that gives easy programmatic
access to the resources available via the CultureMesh API -- these are things
like users, posts, networks, etc.

A typical usage of the ``client`` looks like this:

.. code-block:: python

  c = Client(mock=False)
  post = c.get_post(current_post_id)
  ...
  replies = c.get_post_replies(post["id"], NUM_REPLIES_TO_SHOW)

  # Both 'post' and 'replies' contain real data from the CultureMesh API.

Dig into ``culturemesh/client`` to get a better sense of how the client is
structured and to see all of the available methods.

API Spec
--------

We use a Swagger spec to define the CultureMesh API.  The file is publicly
available in the CultureMesh API
`repo <https://github.com/alanefl/culturemesh-api>`_. Link to file
`here <https://github.com/alanefl/culturemesh-api/blob/master/spec_swagger.yaml>`_.

.. note:: To view the the methods, data, and objects in a nice format,
    copy and paste the contents of the spec into the
    editor at https://editor.swagger.io/.

Acknowledgements
----------------

The CultureMesh Client class was modeled heavily after the client in
`this <https://github.com/googlemaps/google-maps-services-python>`_ project.

