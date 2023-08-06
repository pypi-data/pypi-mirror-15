.. image:: https://img.shields.io/codeship/5f0d5a50-2194-0134-4a97-1eef50e7a565/default.svg
   :target: https://bitbucket.org/hellwig/coveralls-hg
.. image:: https://coveralls.io/repos/bitbucket/hellwig/coveralls-hg/badge.svg?branch=default 
   :target: https://coveralls.io/bitbucket/hellwig/coveralls-hg?branch=default
.. image:: https://img.shields.io/pypi/v/coveralls-hg.svg
   :target: https://pypi.python.org/pypi/Coveralls-HG/
.. image:: https://img.shields.io/badge/Donate-PayPal-blue.svg
   :target: https://paypal.me/MartinHellwig
.. image:: https://img.shields.io/badge/Donate-Patreon-orange.svg
   :target: https://www.patreon.com/hellwig
   
############
Coveralls HG
############

What is it?
===========
- An api library to coveralls.io
- A script for uploading coverage data from a Codeship build environment


What problem does it solve?
===========================
Other coveralls library require git, this one is more dvcs agnostic with the
upload script specifically made for codeship/bitbucket combination. 

How do I install it?
====================
::

  $ pip install coveralls-hg


How do I use it?
================
There are two uses; as a library or as a script.

Library
-------
::

  # The user, repo are the bitbucket variables
  # The token is the coveralls project token
  >>> from coveralls_hg.api import API
  >>> api = API(user, repo, token)
  >>> api.set_source_files(path_to_coverage_data)
  >>> api.upload_coverage()

Script
------
The script requires COVERALLS_REPO_TOKEN to be set in then environment.
Then run your test with coverage and run the script, for example:

::

  $ coverage run test.py
  $ upload_coveralls_csbb

For the curious, csbb stands for Codeship BitBucket


What license is this?
=====================
Two-clause BSD

How can I get support?
======================
The tools I publish have already taken me considerable effort which I have given
away free of charge, if you require guaranteed support please contact me via
e-mail so we can discuss my fee.

How can I give you support?
===========================
Feedback, suggestions and comments via the repo's bug tracker are always
appreciated. Time permitting I will have a serious look at any pull requests. 

Can I do something more that this?
----------------------------------
Wow! Are you sure? Well if you are really sure, and that would be fantastic,
you can leave your donation via patreon
http://patreon.com/hellwig 
or paypal
https://paypal.me/MartinHellwig

Thank you very much! Your donation will help me towards my end-goal of a
grid-independent small holding where I automate the sh*t out of it :-). In the
mean time I'll keep building stuff and where possible and practical open-source
them under the BSD license.  

