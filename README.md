MaxScope
MaxScope is a simple Python GUI for reading and logging peak measurements from a Tektronix oscilloscope using PyVISA.
It finds the peak current on CH4, reads the corresponding voltage on CH3, and logs changes automatically.

Features

Live oscilloscope connection over TCP/IP
Peak detection on CH4 (current)
Corresponding voltage capture on CH3
Automatic history logging (no duplicate values)
Clear history or selected rows
Export measurements to CSV
Classic Windows-style GUI


Requirements

Python 3.8+
Tektronix oscilloscope (SCPI + TCP/IP)
NI‑VISA or Keysight VISA installed

Python packages
Shellpip install pyvisa numpyShow more lines

Usage

Update the oscilloscope IP address in the script:
Pythonrm.open_resource('TCPIP0::10.200.22.14::INSTR')Show more lines

Run the script:
Shellpython maxscope.pyShow more lines

Readings update every second
Right‑click the table or use buttons to clear or export data


CSV Export

File: xscope_data.csv
Includes:

Measurement number
CH4 current (A)
CH3 voltage (V)
Timestamp




Notes

CH4 = current, CH3 = voltage
Logs only when values change
Automatically stops acquisition on close
