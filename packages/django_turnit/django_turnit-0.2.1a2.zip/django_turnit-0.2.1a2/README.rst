`Turn.js <http://www.turnjs.com/>`_ integration to django projects
==================================================================

`django_turnit` provides a way to display PDF files in a `turn.js <http://www.turnjs.com/>`_ player.

Requirements
------------

With django_turnit, you can choose between several backends for PDF image extraction :

+ ghostscript :

    This method does not seems to support threading...
    The `Ghostscript <http://www.ghostscript.com/>`_ application / library. It can be installed as a package in linux
     distributions, such an in debian / ubuntu :

    .. code:: sh

        $ sudo apt install ghostscript  # on debian
        $ sudo apt-get install ghostscript  # on ubuntu


+ pdftocairo : Prefered method

    - `pdftocairo <http://manpages.ubuntu.com/manpages/precise/man1/pdftocairo.1.html>`_ through subprocess

+ pdftoppm : Prefered method

    - `pdftoppm <http://manpages.ubuntu.com/manpages/precise/man1/pdftoppm.1.html>`_ through subprocess

+ poppler : I've no clue on how to use it directly, which would be great, I was net able to setup the library at all...


Installation
------------

.. code:: sh

    $ pip install django-turnit

This installs the packages that are required by django_turnit:

    - `django <https://www.djangoproject.com/>`_ (< 1.10, I haven't yet tested django 1.10)
    - `django-appconf <https://github.com/django-compressor/django-appconf>`_: Helper for configuration of applications
    - `easy-thumbnails <https://github.com/SmileyChris/easy-thumbnails>`_: Creates thumbnails from images
    - `pdfminer <https://github.com/euske/pdfminer>`_: Extract texts from PDF files

Those requirements may also be needed:

    - `python-ghostscript <https://bitbucket.org/htgoebel/python-ghostscript>`_:
     C python binding for the Ghostscript library, if you choose ghostscript as backend
    -

.. code:: sh

    $ python manage.py migrate django_turnit  # Creates the table needed for caching the names of the page images

Usage
-----

`django_turnit` can create and manage page images for PDF files. This images are stored in the `media` folder, a database stores .

Management command
^^^^^^^^^^^^^^^^^^

The `turnit` command creates the missing thumbnails for each FileField containing a PDF file.

.. code:: sh

    $ ./manage.py turnit <app_label>[.<model_name>[.<pk>[.<field_name>]]] [arg]

Where:

- <app_label> is the application label. If set, the whole application is scanned for PDF files, and they are thumbnailed.
- <model_name> is the madel name. If set, the model is scanned.
- <pk> is the row pk. If set, the row is scanned
- <field_name> field name.

Signals processing
^^^^^^^^^^^^^^^^^^

Settings
--------

`TURNIT_INPUT_SUPPORTED_FILE_TYPES`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Supported file MIME types.

.. code:: python

    TURNIT_INPUT_SUPPORTED_FILE_TYPES = ['application/pdf', ]

`TURNIT_OUTPUT_MEDIA_ROOT`
^^^^^^^^^^^^^^^^^^^^^^^^^^

Name of the sub-folder created under the MEDIA_ROOT folder, to store the output image files.

.. code:: python

    TURNIT_OUTPUT_MEDIA_ROOT = 'django_turnit'

`TURNIT_OUTPUT_FILE_FMT`
^^^^^^^^^^^^^^^^^^^^^^^^

Ghostscript output file name format.

.. code:: python

    TURNIT_OUTPUT_FILE_FMT = '%(basename)s.%(i)03d.%(ext)s'


`TURNIT_OUTPUT_IMAGE_FORMAT`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ghostscript output file format, as defined in `Ghostscript documentation <http://ghostscript.com/doc/current/Devices.htm#File_formats>`_.

You can choose between:

- PNG

    - `png16m`: 24 bit color PNG (default value)
    - `pnggray`: 8 bit gray scale PNG
    - `png256`: 256 colors PNG
    - `png16`: 16 colors PNG
    - `pngmonod`: Black and white monochrome PNG

- JPEG

    - `jpeg`: jpeg standard output

- TIFF

    - `tiffgray`: 8-bit gray output.
    - `tiff12nc`: 12-bit RGB output (4 bits per component).
    - `tiff24nc`: 24-bit RGB output (8 bits per component).
    - `tiff48nc`: 48-bit RGB output (16 bits per component).
    - `tiff32nc`: 32-bit CMYK output (8 bits per component).
    - `tiff64nc`: 64-bit CMYK output (16 bits per component).

.. code:: python

    TURNIT_OUTPUT_IMAGE_FORMAT = 'png16m'

`TURNIT_GHOSTSCRIPT_GLOBAL_ARGS`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Global settings for ghostscript library.

.. note::

    Global arguments order in important in ghostscript !
    **You MUST start with the `-q` argument !**

.. code:: python

    TURNIT_GHOSTSCRIPT_GLOBAL_ARGS = ['-q',
                                      '-dNOPROMPT',
                                      '-dNOPAUSE',
                                      '-dBATCH',
                                      '-dSAFER', ]

`TURNIT_GHOSTSCRIPT_EXTRA_ARGS`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Extra parameters for ghostscript. You can add format options here.

.. code:: python

    TURNIT_GHOSTSCRIPT_EXTRA_ARGS = []

