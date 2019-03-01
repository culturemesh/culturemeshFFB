=====================
Developer Quick Start
=====================

This section will get you up and running with CultureMesh FFB.

.. _getting-started:

Getting Started
===============

CultureMesh FFB is a project to bring CultureMesh to the Facebook
Free Basics platform.  Facebook Free Basics (FFB) is an initiative at Facebook
that provides free light weight (no JavaScript, no large images, etc. )
web services to as many cellphones around the world as possible.
CultureMesh FFB is a Python-Flask web app.

Because the intended audience for this service may not be very technically
inclined, it is very important to design the site and it's functions to be
as straightforward as possible.

It is equally important to keep in mind that the site is to use **NO JAVASCRIPT**,
and that it will benefit from being as light (in memory and computation)
as possible. Please keep this in mind as you contribute to the project.

Running Locally
---------------

All our code (save secrets) lives
on `GitHub <https://github.com/Code-The-Change/culturemeshFFB>`_.

Follow these steps to run the website locally.

#. Get the code -- choose a directory and run

    .. code-block:: console

      $ git clone https://github.com/Code-The-Change/culturemeshFFB

#. Install python from https://python.org or via your favorite package manager

#. Install ``virtualenv``

    .. code-block:: console

      $ pip3 install virtualenv

#. If you get a note from ``pip`` about ``virtualenv`` not being in your
   ``PATH``, you need to perform this step. ``PATH`` is a variable accessible
   from any bash terminal you run, and it tells bash where to look for the
   commands you enter. It is a list of directories separated by ``:``. You can
   see yours by running ``echo $PATH``. To run ``virtualenv`` commands, you need
   to add python's packages to your ``PATH`` by editing or creating the file
   ``~/.bash_profile`` on MacOS. To that file add the following lines:

    .. code-block:: console

      PATH="<Path from pip message>:$PATH"
      export PATH

#. Then you can install dependencies into a virtual environment

    .. code-block:: console

      $ cd culturemeshFFB
      $ virtualenv .env
      $ source .env/bin/activate
      $ pip install -r requirements.txt

#. You also need to set some required environment variables
   (see :ref:`env-vars`)

    .. code-block:: console

      $ export WTF_CSRF_SECRET_KEY=...
      $ export CULTUREMESH_API_KEY=...

#. Start the Flask App.

    .. code-block:: console

      $ python -u run.py

As an alternative to combine the above two steps, you can create a simple bash
script to set the environment variables and start up the app for you. To do so,
create a file ``run.sh`` with the following contents, filling in the missing
information:

    .. code-block:: bash

        #!/usr/bin/env bash

        export CULTUREMESH_API_KEY=<API Key>
        export WTF_CSRF_SECRET_KEY=<CSRF Secret>
        export CULTUREMESH_API_BASE_ENDPOINT=<API Base>

        python -u run.py

Then make the app executable:

    .. code-block:: console

        chmod 700 run.sh

Whenever you want to start the app, just execute the script:

    .. code-block:: console

        ./run.sh

You'll see something like this on the terminal:

    .. code-block:: console

      $ python run.py
       * Restarting with stat
       * Debugger is active!
       * Debugger PIN: 202-914-549
       * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)

You can then head over to your browser and type in ```http://127.0.0.1:8080/```
on the address bar.

.. note:: By default, the website (even if running locally) really
  communicates with the live CultureMesh API.  However, the CultureMesh API
  itself currently reads and writes from a staging/dev database. "Flipping
  the switch" and enabling CultureMesh FFB in production would mean
  making the CultureMesh API point to the production database. No changes
  in FFB are required.

Contributing
------------

.. note:: Before contributing or writing code, be sure to scan the codebase
   first.  There are certain recurring paradigms (e.g. blueprint-specific util
   and config files) that you should follow.

All changes you make to the directory should go into a separate branch
which you push and submit a pull request for:

1. Install dependencies

    .. code-block:: console

      $ cd culturemeshFFB
      $ virtualenv .env
      $ source .env/bin/activate
      $ pip install -r requirements.txt

2. Create a new branch

    .. code-block:: console

      $ git checkout -b my-new-branch

3. Set environment variables (see :ref:`env-vars`)

    .. code-block:: console

      $ export WTF_CSRF_SECRET_KEY=...
      $ export CULTUREMESH_API_KEY=...

4. Make some awesome commits

5. Push the branch:

    .. code-block:: console

      $ git push -u origin my-new-branch

6. Make sure there are no merge conflicts with master
7. Submit a pull request.

  .. warning:: When opening the Pull Request choose the ``Code-The-Change``
    base fork, not ``ericshong``'s

8. Select your reviewers

9. Wait until at least one other person submits a positive review
(or make the requested changes).  Once a positive review is submitted,
you can merge the branch yourself from the GitHub website if your reviewer
has not already done so. You should also make sure that your Travis CI build
is green.

10. Update your local master branch and delete the old one

    .. code-block:: console

      $ git checkout master && git pull
      $ git branch -d my-new-branch

CultureMesh FFB is a Python-Flask webapp. I will not go into the details of
the Flask microframework (blueprints, templates, routes, etc.)
-- there is already plenty of documentation for all of this online.

.. _simulating-mobile-web:

Simulating Mobile Web
---------------------

CultureMesh FFB is meant to be accessed from low-end mobile devices and it
runs without JavaScript.

You can simulate this type of environment from Chrome.

1. Run the webapp locally
2. Open the developer tools on chrome
3. Select the mobile view option (top left on the developer tools pane)
4. On the 'Network' tab, switch from 'Online' to 'Slow 3G' on the drop-down menu
5. Click on the three vertical dots on the top right of the developer tools pane
6. Go to 'settings' and select 'Disable JavaScript' under the 'Debugger' section

.. _env-vars:

Environment Variables
=====================

You need to define two environment variables before you can start the
application.

======================  ====================================================================
  Variable                   Purpose
======================  ====================================================================
WTF_CSRF_SECRET_KEY     A secret of your choosing for generating and validating CSRF tokens
CULTUREMESH_API_KEY     The key to access the CultureMesh API (contact us for the key)
======================  ====================================================================
