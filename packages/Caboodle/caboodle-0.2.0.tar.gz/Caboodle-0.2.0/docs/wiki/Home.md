Caboodle Wiki
-------------

Caboodle is a Python module for web browsing or web scraping developed to
provide an all-in-one (kit and caboodle) utility for anything the web has
to offer.

> [kuh-bood-l] **noun**, *Informal*
> 
> 1. the lot, pack, or crowd

Install
-------

To install Caboodle, you will unfortunately have to install some Python modules
from your package manager if you are using Linux or from the
[Unofficial Windows Binaries] list if you are using Windows. This is because of
the image processing capabilities that the optical character recognition (OCR)
solver uses and the fact that pip usually always fails at building them.

Please note however, Caboodle was tested and developed in a Linux environment
and there is no guarantee it will work on Windows.

Required:

- numpy

- scipy

- scikit-image

You will also need to install Google's tesseract-ocr. For Linux users, it should
be listed in your package manager. However, for Windows you will need to
download it from the [tesseract GitHub].

In addition, you will need to install SoX. For Linux users, again, it is as easy
as installing it from your package manager. For Windows, you will need to
download it from the [SoX Sourceforge] page.

Once all the dependencies are installed, proceed to install Caboodle:

	pip install caboodle

Examples
--------

[Searching for Caboodle on PyPi]

[Solving a CAPTCHA]

Resources
---------

[Selenium Documentation]

[Segmenting letters in a CAPTCHA image]

[Unofficial Windows Binaries]: http://www.lfd.uci.edu/~gohlke/pythonlibs
[tesseract GitHub]: https://github.com/tesseract-ocr/tesseract/wiki/Downloads
[SoX Sourceforge]: http://sox.sourceforge.net
[Searching for Caboodle on PyPi]: https://bitbucket.org/bkvaluemeal/caboodle/wiki/examples/pypi
[Solving a CAPTCHA]: https://bitbucket.org/bkvaluemeal/caboodle/wiki/examples/captcha
[Selenium Documentation]: http://selenium-python.readthedocs.io
[Segmenting letters in a CAPTCHA image]: http://stackoverflow.com/questions/33294595/segmenting-letters-in-a-captcha-image
