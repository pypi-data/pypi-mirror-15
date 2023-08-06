spm2olca
========
spm2olca is a simple command line tool that converts a SimaPro LCIA method files
to a `olca-schema <https://github.com/GreenDelta/olca-schema>`_  (JSON-LD) package.


Installation
------------
The installation of the package requires that Python >= 3.4 is 
`installed <https://docs.python.org/3/using/>`_ on your system and that the Python
`Scripts` folder is in your system path. If this is the case you just need to
install it from the command shell via:

.. code-block:: bash

    pip install spm2olca
    
After this you should be able to run the tool anywhere on your system. You can 
test this by executing the following command:

.. code-block:: bash

    spm2olca -h
    
If you want to modify or improve the tool you can download the source and create
an egg-link with pip:
 
.. code-block:: bash

    git clone https://github.com/GreenDelta/spm2olca
    cd spm2olca
    pip install -e .

This will install the tool but with a link to this source code folder where you
can modify the respective functions.


Usage
-----
Just type the `spm2olca` command followed by the SimaPro CSV file with LCIA
methods you want to convert:

.. code-block:: bash
 
    spm2olca <SimaPro CSV file with LCIA methods>

This will generate the `olca-schema` package which will have the same file name
but with a `.zip` extension. This file can be then imported into openLCA.

To see additional options use the help flag `-h`:

.. code-block:: bash

    spm2olca -h

Additional options:

* `-out`: define the name of the output file
* `-skip_unmapped`: LCIA factors with unmapped flows are not included
* `-log`: define the log level (e.g. 'all' will log everything)


Unit mappings
-------------
Units are mapped by name to openLCA units and flow properties ...


Flow mappings
-------------
The SimaPro flows are mapped to openLCA reference flows with a CSV mapping file
with the following columns:

==  =======================================================================
0.  SimaPro name of the flow (string)
1.  SimaPro compartment of the flow (string)
2.  SimaPro sub-compartment of the flow (string)
3.  SimaPro unit of the flow (string)
4.  openLCA reference ID of the flow (UUID)
5.  openLCA name of the flow (string)
6.  openLCA reference ID of the reference flow property of the flow (UUID)
7.  openLCA name of the reference flow property of the flow (string)
8.  openLCA reference ID of the reference unit of the flow (UUID)
9.  openLCA name of the reference unit of the flow (string)
10. conversion factor: amount_simapro * factor = amount_openlca (double)
==  =======================================================================

This is the same file as in the openLCA reference data. The conversion factor
:math:`f` converts a flow amount from SimaPro :math:`a_s` in the SimaPro 
reference unit to the respective amount of the flow in the openLCA reference
unit :math:`a_o`:

.. math::

    a_o = f * a_s

e.g. 
    
.. math::

    a_o = [m3] = 0.001 * [kg] with a_s = [kg]
    
Thus the value of an SimaPro LCIA factor is *divided* by the conversion factor
for such a mapped flow when converted to openLCA, e.g.:

.. math::

    lcia_o = 2000/[m3] = 2/(0.001*[kg]) with a_s = [kg] 

