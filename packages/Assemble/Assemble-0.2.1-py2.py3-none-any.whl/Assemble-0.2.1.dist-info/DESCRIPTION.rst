Assemble: Assemble the packages!
=============================================

.. teaser-begin

``Assemble`` is an `MIT <http://choosealicense.com/licenses/mit/>`_-licensed Python package that allows you to
simplify package building.

A quick example::

    # file: setup.py
    from assemble import get_package

    package = get_package()

    keywords = [
        "about", "this", "package"
    ]
    classifiers = [
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",

        "Topic :: Software Development :: Libraries :: Python Modules",
    ]

    if __name__ == "__main__":
        package.setup(keywords, classifiers)


While developing your package, you can use the `test` command to run all your written tests
and you can use `requirements-scan` to build a list of all used packages.

.. code-block:: bash

    assemble test
    assemble requirements-scan > requirements.txt

When your package is ready and your repository is up-to-date, you can
register your package, patch the version, build your distribution,
upload it to PyPi and tag your repository.

.. code-block:: bash

    assemble version
    assemble build
    assemble upload
    assemble tag

When you have a clean GIT repository, ran your tests and want to publish right-away, you
can use the `publish` shortcut to run `version`, `build`, `upload` and `tag`.

.. code-block:: bash

    assemble publish

To register your package with PyPI, simple call `register` and Assemble will do the rest.

.. code-block:: bash

    assemble register


