pyAPNG
======

A python module to deal with APNG file.

Features
--------

-  Merge multiple images into one APNG file. (It use Pillow to convert image into PNG format)
-  Read APNG file and extract each frames into PNG file.
-  It doesn't do any optimization but only concat the images. This might be changed in the future.

Dependencies
------------

-  `Pillow <https://github.com/python-pillow/Pillow>`__ - **Optional**. You can still use pyAPNG without PIL but it can only read PNG files.

Install
-------

::

    pip install apng

Usage
-----

Convert a series of images into APNG animation:

.. code:: python

    from apng import APNG
    
    APNG.from_files(["1.jpg", "2.jpg", "3.jpg"], delay=100).save("result.png")
    
Use different delay:

.. code:: python

    from apng import APNG
    
    files = [
        ("1.jpg", 100),
        ("2.jpg", 200),
        ("3.jpg", 300)
    ]
    
    im = APNG()
    for file, delay in files:
        im.append(file, delay=delay)
    im.save("result.png")

Extract frames from APNG file:
    
.. code:: python

    from apng import APNG
    
    im = APNG.open("animation.png")
    i = 0
    for png, control in im.frames:
        png.save("{i}.png".format(i=i))
        i += 1
        
Checkout the source for the details.

Todos
-----

-  Add optimizer?

Changelog
---------

-  0.1.0 (May 30, 2016)

   -  First release.
   
