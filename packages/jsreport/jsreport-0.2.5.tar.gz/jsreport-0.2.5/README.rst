JustServe Reports
=================
A simple tool to pull basic reporting data out of JustServe 
(https://www.justserve.org/). 

Background
----------
JustServe is a wonderful resource to bring volunteers and service organizations 
together. For those that are responsible for training and awareness, however, 
the reporting tools are...lacking. How is one to measure whether more projects 
are being added to the site? This script aims to help answer that question.

What It Does
------------
The ``jsreport`` module contains code that uses Selenium to interact with the
JustServe website to retrieve data, typically for reporting purposes.

``js-zipcode.py`` is a script that interacts with the ``jsreport`` module
to tell you how many projects are listed near a specific zipcode. You can 
specify the zipcode and search radius, along with some technical details.

Installation
------------
First, I highly recommend using a ``virtualenv``.

The preferred method of installation is to use ``pip``::

    $ pip install jsreport

``pip`` will install the ``jsreport`` package to the proper location and it
will install the ``js-zipcode.py`` script to the proper ``bin`` location on
your PATH.
    
``pip`` will also install the selenium package, if it is not already installed.

The default web driver for Selenium is Firefox. If you want to use one of the 
other web drivers, you must install them to your system yourself. You may
consider installing the ``chromedriver-installer`` package using ``pip``.
Information on the PhantomJS web driver can be found at http://phantomjs.org/.

Script Usage
------------
This usage is available, as demonstrated below, from the command-line::

    $ js-zipcode.py --help
    usage: js-zipcode.py [-h] [-r {5,10,15,25,50,75}]
                       [-d {firefox,chrome,phantomjs}] [-o {human,csv,json}]
                       zipcode
    
    Retrieve the number of JustServe projects at a zipcode.
    
    positional arguments:
      zipcode               The five digit zipcode at the center of the search
                            radius.
    
    optional arguments:
      -h, --help            show this help message and exit
      -r {5,10,15,25,50,75}, --radius {5,10,15,25,50,75}
                            The search radius, in miles. Defaults to 5.
      -d {firefox,chrome,phantomjs}, --driver {firefox,chrome,phantomjs}
                            The WebDriver to use. Defaults to firefox.
      -o {human,csv,json}, --output {human,csv,json}
                            The output format. Defaults to human-readable.

                        
                        
Examples
--------
Example of running ``js-zipcode`` to pull data::

    $ js-zipcode.py 20500
    6 projects within a 5 mile radius of 20500
    $ js-zipcode.py -r 10 20500
    29 projects within a 10 mile radius of 20500
    $ js-zipcode.py -r 15 20500
    48 projects within a 15 mile radius of 20500
    $ js-zipcode.py -r 25 20500
    70 projects within a 25 mile radius of 20500
    $ js-zipcode.py -r 50 20500
    96 projects within a 50 mile radius of 20500
    $ js-zipcode.py -r 75 20500
    106 projects within a 75 mile radius of 20500


Other Notes/Disclaimers
-----------------------

- This is a Python script, tested with version 2.7.11, but it should work with 
  others
- Please note: I do not provide technical support for environment setup; you 
  are on your own for that. 
- I will respond to pull requests for bug fixes, though.
