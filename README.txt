MaxScope
========

MaxScope is a simple Python GUI for reading and logging peak measurements from a Tektronix oscilloscope using PyVISA.

It detects the peak current on CH4 and records the corresponding voltage on CH3.

Features
--------
- Live oscilloscope connection over TCP/IP
- Peak current detection on CH4
- Corresponding voltage capture on CH3
- Automatic history logging (no duplicate values)
- Clear history or selected rows
- Export measurements to CSV
- Classic Windows-style GUI

Requirements
------------
- Python 3.8+
- Tektronix oscilloscope with SCPI + TCP/IP
- NI-VISA or Keysight VISA installed

Python packages:
    pip install pyvisa numpy

Usage
-----
1. Update the oscilloscope IP address in the script
2. Run the program:
       python maxscope.py
3. Readings update every second
4. Use buttons or right-click menu to clear or export data

CSV Export
----------
- File: xscope_data.csv
- Includes measurement number, CH4 current, CH3 voltage, and timestamp

Notes
-----
- CH4 = current, CH3 = voltage
- Logs only when values change
- Acquisition stops automatically when closing the app

Author
------
Indura Rathnamalala
