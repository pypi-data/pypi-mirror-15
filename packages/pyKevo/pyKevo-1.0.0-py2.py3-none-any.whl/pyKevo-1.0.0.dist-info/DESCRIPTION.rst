pyKevo
======
This is a small little library that allows you to control your Kevo Smartlock from python code.  This is a stopgap until Kevo provides some APIs::

Example
-------

.. code:: python

    import pyKevo

    frontDoor = pyKevo('kevo_email@gmail.com','password')

    frontDoor.connect()

    print frontDoor.lockState()

    print frontDoor.unlockLock()


Requirements
------------

  * you require a Kevo Smartlock::
  * you require the Kevo Plus be installed and configured::
  * Your account credentials for `MyKevo https:mykevo.com//`.  You must have this registered::

License
-------
This work pyKevo by Jeremy Foran is licensed under a `Creative Commons Attribution-ShareAlike 3.0 Unported License <http://creativecommons.org/licenses/by-sa/3.0/deed.en_US>`_.::



