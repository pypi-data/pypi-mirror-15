The pyBox0 API Reference
************************

The "box0" module
=================

.. automodule:: box0

Device
^^^^^^

.. autoclass:: box0.Device
   :members:
   :member-order: bysource
   :exclude-members: name, manuf, serial, modules

   .. autoattribute:: name
      :annotation:
   .. autoattribute:: manuf
      :annotation:
   .. autoattribute:: serial
      :annotation:
   .. autoattribute:: modules
      :annotation:

.. autoclass:: box0.LogLevel
   :member-order: bysource

   .. autoattribute:: DEBUG
      :annotation:
   .. autoattribute:: INFO
      :annotation:
   .. autoattribute:: WARN
      :annotation:
   .. autoattribute:: ERROR
      :annotation:
   .. autoattribute:: NONE
      :annotation:

ResultException
^^^^^^^^^^^^^^^

.. autoexception:: box0.ResultException
   :members:
   :member-order: bysource
   :exclude-members: act

Version
^^^^^^^

.. autoclass:: box0.Version
   :members:
   :member-order: bysource
   :exclude-members: code, major, minor, patch

   .. autoattribute:: code
      :annotation:
   .. autoattribute:: major
      :annotation:
   .. autoattribute:: minor
      :annotation:
   .. autoattribute:: patch
      :annotation:

The "module" module
===================

.. automodule:: box0.module

Module
^^^^^^

.. autoclass:: Module
   :members:
   :member-order: bysource
   :inherited-members:
   :exclude-members: index, type, name

   .. autoattribute:: index
      :annotation:

   .. autoattribute:: type
      :annotation:

   .. autoattribute:: name
      :annotation:

Analog In
^^^^^^^^^

.. autoclass:: box0.module.Ain
   :members:
   :member-order: bysource
   :inherited-members:
   :exclude-members: ref, bitsize, speed, chan_config, chan_seq, count, capab, label, stream, buffer

   .. autoattribute:: ref
      :annotation:

   .. autoattribute:: bitsize
      :annotation:

   .. autoattribute:: speed
      :annotation:

   .. autoattribute:: chan_config
      :annotation:

   .. autoattribute:: chan_seq
      :annotation:

   .. autoattribute:: count
      :annotation:

   .. autoattribute:: capab
      :annotation:

   .. autoattribute:: label
      :annotation:

   .. autoattribute:: stream
      :annotation:

   .. autoattribute:: buffer
      :annotation:

Analog Out
^^^^^^^^^^

.. autoclass:: box0.module.Aout
   :members:
   :member-order: bysource
   :exclude-members: ref, bitsize, speed, chan_config, chan_seq, count, capab, label, stream, buffer, repeat


   .. autoattribute::  ref
      :annotation:

   .. autoattribute::  bitsize
      :annotation:

   .. autoattribute::  count
      :annotation:

   .. autoattribute::  capab
      :annotation:

   .. autoattribute::  chan_config
      :annotation:

   .. autoattribute::  chan_seq
      :annotation:

   .. autoattribute::  repeat
      :annotation:

   .. autoattribute::  buffer
      :annotation:

   .. autoattribute::  speed
      :annotation:

   .. autoattribute::  stream
      :annotation:

   .. autoattribute::  label
      :annotation:

Digital Input/Output
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: box0.module.Dio
   :members:
   :member-order: bysource
   :exclude-members: ref, capab, count, label

   .. autoattribute::  ref
      :annotation:

   .. autoattribute::  capab
      :annotation:

   .. autoattribute::  count
      :annotation:

   .. autoattribute::  label
      :annotation:

The "property" module
=====================

.. automodule:: box0.property

The "backend" module
====================

.. automodule:: box0.backend
