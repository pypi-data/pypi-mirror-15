Chirp Python SDK
================

The Chirp Python SDK enables the user to create, send and query chirps,
using the Chirp audio protocol.

Requirements
------------

The Chirp SDK supports Python 2 and Python 3.

- `Python 2.6+`_, or `Python 3.5`_.

.. _Python 2.6+: https://docs.python.org/2/
.. _Python 3.5: https://docs.python.org/3/

Usage
-----

You'll need to install PortAudio:

::

   sudo apt-get install portaudio19-dev

or for MacOS:

::

   brew install portaudio

To install the SDK and its dependencies:

::

   python setup.py install

To create a chirp identifier encapsulating an arbitrary dictionary:

.. code:: python

   import chirpsdk
   
   sdk = chirpsdk.ChirpSDK(YOUR_APP_KEY, YOUR_APP_SECRET)
   chirp = sdk.create_chirp({'key': 'value'})
   print chirp.shortcode

To send this chirp via the inbuilt speaker:

.. code:: python

   chirp.chirp()


To construct and send a new chirp:

.. code:: python

   chirp = sdk.create_chirp('parrotbill')
   chirp.chirp()
   chirp.save_wav()

To query an existing chirp:

.. code:: python

   chirp = sdk.get_chirp('parrotbill')
   print chirp.longcode
   print chirp.data

Further Information
-------------------

For help, see:

::

   pydoc chirpsdk

----

This file is part of the Chirp Python SDK.
For full information on usage and licensing, see http://chirp.io/

Copyright (c) 2011-2016, Asio Ltd.
All rights reserved.

For commercial usage, commercial licences apply. Please `contact us`_.

For non-commercial projects these files are licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. _contact us: contact@chirp.io
