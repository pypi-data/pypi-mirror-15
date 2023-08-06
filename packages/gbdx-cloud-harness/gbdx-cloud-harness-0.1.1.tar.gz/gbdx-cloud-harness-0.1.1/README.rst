====================================================
cloud-harness: Build custom GBDX tasks for beginners
====================================================

.. image:: https://badge.fury.io/py/gbdx-cloud-harness.svg
    :target: https://badge.fury.io/py/gbdx-cloud-harness


This package allows a user to build custom GBDX tasks that can be executed locally and also remotely on the platform. All from a python file and commandline tools.

To run remote tasks, this package uses the `gbdx-auth`_ package. Therefore the users credentials must be configured according to `gbdx-auth`_.

.. _gbdx-auth: https://github.com/TDG-Platform/gbdx-auth

Installation
------------

To install from pypi:

  pip install gbdx-cloud-harness

Usage
-----

The cloud-harness package has a template task with example usage inside. To create a new template:

    cloud-harness create my_app
    cd my_app/

In the new folder, there will be a `app.py` file which is the template. Open in your favorite editor to start building a new task. When ready to run the task::

    cloud-harness run app.py

Please note, to run the task locally, all port values must be valid filesystem locations. Otherwise errors will be raised. 

When the task is ready to be ran on the platform, use the `--remote` flag::

    cloud-harness run app.py --remote

This will run the task on the platform assuming all the port values are S3 locations. Otherwise errors will be raised. 

If there is local data that needs to be pushed to S3 for the remote run, then the `--upload` flag needs to be used::

    cloud-harness run app.py --remote --upload

This will push all local data the ports contain to the users account storage, prior to executing the workflow.


Development
-----------

**Contributing**

Please contribute! Please make pull requests directly to master. Before making a pull request, please:

* Ensure that all new functionality is covered by unit tests.
* Verify that all unit tests are passing.
* Ensure that all functionality is properly documented.t
* Ensure that all functions/classes have proper docstrings so sphinx can autogenerate documentation.
* Fix all versions in setup.py (and requirements.txt)

**Run Tests**

Tests use `pytest`_ framework

.. _pytest: http://pytest.org/latest/contents.html

::

  py.test [...]
  python -m pytest [...]

To generate coverage reports::

    py.test --cov cloud_harness --cov-report html test
    py.test --cov task_template --cov-report html task_template
    py.test --cov services --cov-report html services

**Create a new version**

To create a new version::

    bumpversion ( major | minor | patch )
    git push --tags

Don't forget to update the changelog and upload to pypi.