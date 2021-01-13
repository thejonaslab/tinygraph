.. _quickstart:

Quickstart
==========

Eager to get started?  This page gives a first introduction to Eve.

Prerequisites
-------------
- You already have Eve installed. If you do not, head over to the
  :ref:`install` section.
- MongoDB is installed_.
- An instance of MongoDB is running_.

A Minimal Application
---------------------

A minimal Eve application looks something like this::

    from eve import Eve
    app = Eve()

    if __name__ == '__main__':
        app.run()

Just save it as run.py. Next, create a new text file with the following
content:

