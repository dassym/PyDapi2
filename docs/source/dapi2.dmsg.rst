dapi2.dmsg package
==================

Implementation of DAPI2 message.

DAPI2 message format
--------------------

The DAPI protocol uses 3 control char: [SOH] to beginning a message, [ACK] or [NAK] to give an acknowledgment (good or bad).
The value of the fields is sent in ASCII representing hexadecimal. Allowed characters are numbers from 0 to 9 and letters from A to F.
For example if we want to send the value 161 (0xA1), we shall write A1 on the serial port.

+------+------+-----+-+------+------+-----+
| Char | Hex  | Dec | | Char | Hex  | Dec |
+======+======+=====+=+======+======+=====+
| SOH  | 0x01 | 1   | | 7    | 0x37 | 1   |
+------+------+-----+-+------+------+-----+
| ACK  | 0x06 | 6   | | 8    | 0x38 | 6   |
+------+------+-----+-+------+------+-----+
| NAK  | 0x15 | 21  | | 9    | 0x39 | 21  |
+------+------+-----+-+------+------+-----+
| 0    | 0x30 | 48  | | A    | 0x41 | 65  |
+------+------+-----+-+------+------+-----+
| 1    | 0x31 | 49  | | B    | 0x42 | 66  |
+------+------+-----+-+------+------+-----+
| 2    | 0x32 | 50  | | C    | 0x43 | 67  |
+------+------+-----+-+------+------+-----+
| 3    | 0x33 | 51  | | D    | 0x44 | 68  |
+------+------+-----+-+------+------+-----+
| 4    | 0x34 | 52  | | E    | 0x45 | 69  |
+------+------+-----+-+------+------+-----+
| 5    | 0x35 | 53  | | F    | 0x46 | 70  |
+------+------+-----+-+------+------+-----+
| 6    | 0x36 | 54  | |      |      |     |
+------+------+-----+-+------+------+-----+
  
Message structure
.................

The message structure in standard mode is:

.. image:: _static/img/api-msg-standard.svg
   :height: 64pt
   :alt: Standard message structure
   

The message structure in extended mode is:

.. image:: _static/img/api-msg-extended.svg
   :height: 64pt
   :alt: Extended message structure
  

Submodules
----------

dapi2.dmsg.common module
------------------------

.. automodule:: dapi2.dmsg.common
    :members:
    :undoc-members:
    :show-inheritance:

dapi2.dmsg.message module
-------------------------

.. automodule:: dapi2.dmsg.message
    :members:
    :undoc-members:
    :show-inheritance:

dapi2.dmsg.reader module
------------------------

.. automodule:: dapi2.dmsg.reader
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: dapi2.dmsg
    :members:
    :undoc-members:
    :show-inheritance:
