stringint
=========

.. image:: https://travis-ci.org/DasIch/stringint.svg?branch=master
   :target: https://travis-ci.org/DasIch/stringint

.. image:: https://readthedocs.org/projects/stringint/badge/?version=latest
   :target: https://stringint.readthedocs.io/en/latest/

stringint is a, BSD licensed, Python library that allows you to represent
strings as ints and vice versa.

>>> from stringint import *
>>> string_to_int('stringint')
2644870996275670454816921315419928710306414234893680756
>>> int_to_string(_)
'stringint'
>>> bytes_to_int(b'stringint')
6852132936324890586740
>>> int_to_bytes(_)
b'stringint'

Currently stringint supports Python 3.5. It's tested on CPython 3.5 and later.


