temp-utils
===========

temp-utils is a set of convenient python utilities for dealing with temporary files and folders. It is built on top of the builtin tempfile module.

Context Managers
-----------------

Changing Working Directory
+++++++++++++++++++++++++++
Use the context manager :code:`chdir` to change your working directory temporarily, changing it back at the end of the context.

.. code-block:: python

    from temp_utils.contextmanagers import chdir

    with chdir('path/to/directory'):
        ...


Temporary File
++++++++++++++++
Use the context manager :code:`temp_file` to create a new temporary file. This file gets deleted at the end of the context.

.. code-block:: python

    from temp_utils.contextmanagers import temp_file

    with temp_file() as file_path:
        ...

Temporary Folder
+++++++++++++++++
Use the context manager :code:`temp_dir` to create a new temporary folder. This folder gets deleted, along with everything in it, at the end of the context.

.. code-block:: python

    from temp_utils.contextmanagers import temp_dir

    with temp_dir() as dir_path:
        ...
