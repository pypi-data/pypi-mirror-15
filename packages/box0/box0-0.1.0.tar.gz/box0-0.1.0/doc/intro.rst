Introduction to pyBox0
======================

pyBox0 is a Python binding of libbox0.

Device
------

A device contain multiple Modules.

Open device
------------
.. code-block:: python

	import box0
	dev = box0.usb.open_supported()
	# ... do something with device

Module
------

A module is a block that provide interface to a hardware.

Open AIN module
---------------
.. code-block:: python

	import box0
	dev = box0.usb.open_supported()
	my_ain = dev.ain()
	# ... do something with "my_ain"

Open any type of module
----------------------

.. code-block:: python

	import box0
	dev = box0.usb.open_supported()

	# "<MODULE_TYPE>" can be "ain", "aout", "spi", "i2c", "dio", "pwm"
	mine = dev.<MODULE_TYPE>()
	# ... do something with "mine"

Reading data from AIN
---------------------

.. code-block:: python

	import box0
	import numpy

	# find thing to work with
	dev = box0.usb.open_supported()
	ain0 = dev.ain()
	ain0.static_prepare() # prepare for static mode (ie snapshot of signal)

	# do the work
	values = numpy.empty(100, dtype=numpy.float32) # count=100, can vary though
	ain0.static_start(values) # block till data not readed
	print(values)

	# dispose resources
	ain.close()
	dev.close()

Toggle pins using DIO
--------------------

.. code-block:: python

	import box0
	import time

	dev = box0.usb.open_supported()
	dio0 = dev.dio()
	dio0.static_prepare()

	#note: connect LED on "0" pin of "DIO0"
	pin0 = dio0.pin(0)
	pin0.output()
	pin0.high()
	pin0.enable()

	while True:
		try:
			pin0.toggle()
			time.sleep(0.1)
		except KeyboardInterrupt:
			break

	dio0.close()
	dev.close()

Generate Constant voltage
------------------------

.. code-block:: python

	import box0
	import numpy

	CONSTANT_VOLTAGE = 1.5

	dev = box0.usb.open_supported()
	aout0 = dev.aout()

	aout0.static_prepare()
	values = numpy.array([CONSTANT_VOLTAGE], dtype=numpy.float32)
	aout0.static_start(values) # non-blocking, return right after operation

	input("Press Enter to exit")

	aout0.static_stop()
	aout0.close()
	dev.close()
