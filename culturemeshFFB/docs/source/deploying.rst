=========================
Deploying CultureMesh FFB
=========================

.. _deploying-ffb:

How it works now
================

We have been using Heroku to deploy CultureMesh FFB for developing and
testing -- the site can be accessed at https://culturemesh-ffb.herokuapp.com/.
If you'd like to deploy the application as well, you can just make your
own Heroku account, download the CLI tools, and follow one of the myriad
tutorials online.  Don't forget to set the required :ref:`env-vars`
on Heroku as well, or your deploy won't work.

Deploying to FFB is as easy as submitting the URL of CultureMesh FFB via
the Facebook Free Basics website and making sure that you meet the requirements
of the platform.


How it should probably work in the future
=========================================

In the near future, CultureMesh FFB should be available at
https://lite.culturemesh.com and run on the same serving infrastructure as
the CultureMesh API and CultureMesh for web.  Currently, this is Bluehost.
Once this is the case, the ``client`` in CultureMesh FFB class could
point to the localhost even directly speak to the database -- this will
greatly reduce latency in API calls.

It would also be a good idea to look into AWS hosting in the future.  We also
suggest Dockerizing the website, the FFB site, and the API.
